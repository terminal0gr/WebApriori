#include <iostream>
#include <iomanip> // Required for setprecision and fixed
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <bit> // For std::popcount (C++20)
#include <omp.h>
#include <winscard.h>

#ifdef _WIN32
#include <windows.h>
#include <psapi.h>
#else
#include <sys/resource.h>
#endif

size_t getPeakRSS() {
#ifdef _WIN32
    PROCESS_MEMORY_COUNTERS info;
    GetProcessMemoryInfo(GetCurrentProcess(), &info, sizeof(info));
    return (size_t)info.PeakWorkingSetSize;
#else
    struct rusage usage;
    getrusage(RUSAGE_SELF, &usage);
    return (size_t)(usage.ru_maxrss * 1024); // Convert KB to Bytes
#endif
}


// ==========================================
// 1. DATA STRUCTURES
// ==========================================

// Corresponds to entries in 'topKFI' (Global Results)
struct TopKFIM {
    std::vector<int> items; 
    int support;

    // For sorting topKFI by Support Descending
    bool operator>(const TopKFIM& other) const {
        if (support != other.support) return support > other.support;
        return items < other.items; // Tie-breaker
    }
};

// High-Performance BitSet (for Vertical Representation)
struct DynamicBitSet {
    std::vector<uint64_t> data;
    size_t num_bits;

    DynamicBitSet() : num_bits(0) {}
    void resize(size_t n_bits) {
        num_bits = n_bits;
        // Allocate only what is needed. Initialize to 0.
        data.assign((n_bits + 63) / 64, 0);
    }
    void set(size_t index) {
        data[index / 64] |= (1ULL << (index % 64));
    }
    // Fast Population Count using Hardware Instructions
    size_t count() const {
        size_t c = 0;
        for (uint64_t val : data) {
            #if defined(__cpp_lib_bitops)
                c += std::popcount(val);
            #elif defined(__GNUC__) || defined(__clang__)
                c += __builtin_popcountll(val);
            #else
                // Fallback software implementation
                val = val - ((val >> 1) & 0x5555555555555555ULL);
                val = (val & 0x3333333333333333ULL) + ((val >> 2) & 0x3333333333333333ULL);
                c += (((val + (val >> 4)) & 0x0F0F0F0F0F0F0F0FULL) * 0x0101010101010101ULL) >> 56;
            #endif
        }
        return c;
    }
    // Intersection: A & B
    static void intersect(const DynamicBitSet& a, const DynamicBitSet& b, DynamicBitSet& newBits) {
        if (newBits.data.size() != a.data.size()) {
           newBits.data.resize(a.data.size());
        }
        for (size_t i = 0; i < a.data.size(); ++i) {
        	newBits.data[i] = a.data[i] & b.data[i];
        }
    }
    // Difference: B & (~A) -> Items in B that are NOT in A
    static void diff(const DynamicBitSet& a, const DynamicBitSet& b, DynamicBitSet& newBits) {
        if (newBits.data.size() != a.data.size()) {
            newBits.data.resize(a.data.size());
        }
        for (size_t i = 0; i < a.data.size(); ++i) {
        	newBits.data[i] = a.data[i] & (~b.data[i]);
		}
    }
};

// Candidate for the Mining Loop
struct Candidate {
    std::vector<int> itemset; // Using Rank IDs
    DynamicBitSet bits;
    int support;

    // [CRITICAL CHANGE]: Pure Support Sort (Descending)
    // Lexicographical is only a tie-breaker.
    bool operator<(const Candidate& other) const {
        if (support != other.support) {
            return support > other.support; // Higher support comes first
        }
        return itemset < other.itemset; // Tie-breaker
    }
};

// ==========================================
// 2. QUICK HEAP (Optimized)
// ==========================================
class QuickHeap {
    int K;
    std::vector<int> heapList;

public:
    QuickHeap(int k) : K(k) { 
    	heapList.reserve(K + 1); 
    }

    // Matches Python: self.heap.initialFill(list(item1TopK.values()))
    void initialFill(const std::vector<int>& supports) {
        heapList = supports;
        
        //Gives gain %5-10 on large datasets
        std::sort(heapList.begin(), heapList.end(), std::greater<int>());

        if (heapList.size() > K) {
        	heapList.resize(K);
        }
    }

    // Matches Python: self.heap.insert(support)
    int insert(int value) {

        // Optimization: Early exit if value is worse than the worst item
        if (heapList.size() >= K && value <= heapList.back()) {
        	return heapList.back();
        }

        // Binary Search for insertion point (Descending Order)
        auto it = std::upper_bound(heapList.begin(), heapList.end(), value, std::greater<int>());
        heapList.insert(it, value);

        if (heapList.size() > K) {
        	heapList.pop_back();
        }
        return (heapList.size() == K) ? heapList.back() : 0;
    }
    
    int getMinSup() const { 
        return (heapList.size() < K) ? 0 : heapList.back(); 
    }
};





// ==========================================
// 2. THE HTK-Miner CLASS
// ==========================================
class HTKMiner {
	
private:
    // Mappings (The 3-Tier System)
    std::unordered_map<int, std::string> idToItem; // RawID -> Name
    std::vector<int> rankToRaw;                    // Rank -> RawID
    
    std::vector<TopKFIM> topKFI; // The global Top-K results (matches Python 'topKFI')
    QuickHeap heap;
    int min_count = 0;
    int topK;
    int num_of_transactions = 0;
    int num_of_items = 0;
    int tidSet; // 1 = BSN mode, 0 = DBSN mode
    std::string delimiter=" "; // Default delimiter (can be changed if needed)

    using TimePoint = std::chrono::steady_clock::time_point;
    TimePoint start_time;
    TimePoint reading_time;
    TimePoint bitset_time;
    TimePoint end_time;

    using ItemStat = std::pair<int, int>; // {Support, RawID}

public:
    HTKMiner(int k, bool mode = true, std::string delim = " ") : heap(k), topK(k), tidSet(mode), delimiter(delim) {}

    void mine(const std::string& filepath) {
        start_time = std::chrono::steady_clock::now();

        // Step 1: Read, Rank and bitset conversion
        std::vector<Candidate> currentLevelData= readAndRank(filepath);
 
        // Initial Pruning/Threshold update
        performGetTopKFI(currentLevelData); // Update min_count and prune currentLevel

        // std::cout << "Level 1 Frequent Items: " << currentLevelData.size() << "\n";
        // std::cout << "Initial MinSup: " << min_count << "\n";

// 2. Main Mining Loop
        int level = 1;
        while (!currentLevelData.empty()) {
            std::vector<Candidate> nextLevelData;
            int n = currentLevelData.size();
            
            // Determine number of threads and create local storage to avoid push_back contention
            int num_threads = omp_get_max_threads();
            std::vector<std::vector<Candidate>> localNextLevelData(num_threads);

            #pragma omp parallel
            {
                int tid = omp_get_thread_num();

                DynamicBitSet newBits; // Reusable workspace for bitset operations
                std::vector<int> newKey; // Reusable workspace for itemset generation

                // SMART ITERATION MECHANISM (SIME) - Parallelized
                // Using 'dynamic' schedule because mining tasks are often unbalanced
                //#pragma omp for schedule(dynamic, 8)
                #pragma omp for schedule(dynamic, 8)
                for (int j = 1; j < n; ++j) {
                    // Pruning A: In parallel, we use 'continue' for the outer loop 
                    // as threads handle non-contiguous chunks.
                    //break cannot be used here because of the
                    if (currentLevelData[j].support < min_count) continue;

                    for (int i = 0; i < j; ++i) {
                        // Pruning B: Inner loop can still 'break' because it is local to the thread
                        if (currentLevelData[i].support < min_count) break;

                        // Pruning C: Prefix Matching 
                        bool match = true;
                        for (int k = 0; k < level - 1; ++k) {
                            if (currentLevelData[i].itemset[k] != currentLevelData[j].itemset[k]) {
                                match = false; 
                                break;
                            }
                        }

                        if (match) {
                            // Intersection Logic
                            DynamicBitSet::intersect(currentLevelData[i].bits, currentLevelData[j].bits, newBits);
                            int newSup = newBits.count();

                            if (newSup >= min_count) {
                                // 1. Update Heap & Threshold (Must be thread-safe)
                                if (newSup > min_count) {
                                    #pragma omp critical 
                                    {
                                        min_count = heap.insert(newSup);
                                    }
                                }

                                // 2. Create Itemset Key
                                newKey = currentLevelData[i].itemset;
                                newKey.push_back(currentLevelData[j].itemset.back());

                                // 4. Add to Thread-Local storage (Lock-free)
                                localNextLevelData[tid].push_back({std::move(newKey), std::move(newBits), newSup});
                            }
                        }
                    }
                }
            }

            // Merge thread-local results back into the main nextLevelData
            // Use move iterators to avoid expensive vector copies
            for (auto& localVec : localNextLevelData) {
                nextLevelData.insert(nextLevelData.end(), 
                                    std::make_move_iterator(localVec.begin()), 
                                    std::make_move_iterator(localVec.end()));
            }

            // 1. Merge nextLevelTopK into topKFI
            for (const auto& cand : nextLevelData) {
                topKFI.push_back({cand.itemset, cand.support});
            }
            
            // 2. Execute the Global Pruning & Update MinSup
            performGetTopKFI(nextLevelData);

            // Move to next level
            currentLevelData = std::move(nextLevelData);
            
            // Sort to enable Prefix Optimization for next pass
            std::sort(currentLevelData.begin(), currentLevelData.end()); 

            level++;
            
        }

        end_time = std::chrono::steady_clock::now();
        std::cout << "FI mining time 15c: " << std::chrono::duration_cast<std::chrono::milliseconds>(end_time-bitset_time).count() / 1000.0 << " s\n";

		//Statistics
        double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count() / 1000.0;
        std::cout << "Total Execution Time: " << elapsed << " s\n";
        std::cout << "FIM found: " << topKFI.size() << "\n";
        std::cout << "Absolute minSup: " << std::setprecision(0) << min_count << "\n";
        std::cout << "Relative minSup: " << std::fixed << std::setprecision(15) << (double)min_count / num_of_transactions << "\n";
    }

    void saveResults(const std::string& path) {
        std::ofstream out(path);
        for (const auto& res : topKFI) {
            for (size_t i = 0; i < res.items.size(); ++i) {
                out << idToItem[rankToRaw[res.items[i]]] << (i == res.items.size()-1 ? "" : " ");
            }
            out << " #SUP: " << res.support << "\n";
        }
    }

    // Faster integer parsing helper
    inline int fast_atoi(const char*& p, const char* end) {
        int val = 0;
        // Skip any non-digit characters (spaces, tabs, etc.)
        while (p < end && (*p < '0' || *p > '9')) p++;
        if (p >= end) return -1; // Signifies end of line/chunk
        
        // Parse the number
        while (p < end && *p >= '0' && *p <= '9') {
            val = val * 10 + (*p - '0');
            p++;
        }
        return val;
    }

    inline std::string_view fast_get_token(const char*& p, const char* end) {
        // Skip whitespace, tabs, and carriage returns
        while (p < end && (*p == delimiter[0] || *p == '\r' )) p++;
        
        // If we hit the end of the line/chunk, force 'p' to advance to avoid infinite loops
        if (p >= end || *p == '\n') {
            p = end; 
            return {};
        }

        const char* start = p;
        
        // Find the end of the word
        while (p < end && *p != delimiter[0] && *p != '\n' && *p != '\r') p++;
        
        return std::string_view(start, p - start);
    }    

    std::vector<Candidate> readAndRank(const std::string& path) {

        std::cout << "Read dataset 15c Started\n";

        // [Part 1: Fast I/O - Load file into memory]
        // Open the file in binary mode and move the file pointer to the end immediately to find the size.
        std::ifstream in(path, std::ios::binary | std::ios::ate);
        // If the file couldn't be opened (e.g., wrong path), return an empty result to avoid crashing.
        if (!in.is_open()) return {};
        
        // Get the current position of the file pointer, which represents the total file size in bytes.
        size_t fileSize = in.tellg();
        // Allocate a buffer large enough to hold the entire file plus one extra byte to accomodate a null terminator for safety.
        std::vector<char> buffer(fileSize + 1);
        // Move the file pointer back to the beginning of the file to start reading.
        in.seekg(0);
        // Read the entire file content directly into the allocated memory buffer.
        in.read(buffer.data(), fileSize);
        // Explicitly add a null terminator at the end to make the buffer safe for string operations.
        buffer[fileSize] = '\0'; 
        // Close the file stream since the data is now safely in memory.
        in.close();

        // Create a pointer to the start of our memory buffer for data processing.
        const char* start_ptr = buffer.data();
        // Create a pointer to the end of our data to define the search boundaries.
        const char* end_ptr = start_ptr + fileSize;
        // Ask OpenMP for the maximum number of hardware threads available for parallel work.
        int num_threads = omp_get_max_threads();

        // [Determine chunk boundaries for each thread (align to newlines)]
        // Prepare a list of memory addresses to divide the file into equal chunks for each thread.
        std::vector<const char*> boundaries(num_threads + 1);
        // The first chunk always starts at the beginning of the file.
        boundaries[0] = start_ptr;
        // The last chunk boundary always ends at the physical end of the file data.
        boundaries[num_threads] = end_ptr;
        // Divide the file into segments, ensuring no thread starts in the middle of a line.
        for (int i = 1; i < num_threads; ++i) {
            // Calculate a rough starting point based on an even split of the file size.
            const char* p = start_ptr + (fileSize / num_threads) * i;
            // Advance the pointer until we hit a newline character so the next thread starts at a clean line.
            while (p < end_ptr && *p != '\n') p++;
            // Set the boundary: if we found a newline, start after it; otherwise, go to the end.
            boundaries[i] = (p < end_ptr) ? p + 1 : end_ptr;
        }

        // [Part 2: Pass 1 - Parallel ID Discovery]
        // Create thread-local sets to store unique items found in each chunk without cross-thread locking.
        std::vector<std::unordered_set<std::string_view>> local_sets(num_threads);
        // Create thread-local counters to track how many lines (transactions) each thread processes.
        std::vector<int> local_trans_counts(num_threads, 0);

        // Tell OpenMP to spawn multiple threads to run the following block of code in parallel.
        #pragma omp parallel num_threads(num_threads)
        {
            // Identify which thread index (ID) is currently running this specific block.
            int tid = omp_get_thread_num();
            // Assign this thread its specific starting point in the memory buffer.
            const char* p = boundaries[tid];
            // Assign this thread its specific ending point so it doesn't process other threads' data.
            const char* end = boundaries[tid + 1];

            // Continue processing as long as the current pointer hasn't reached the end of the chunk.
            while (p < end) {
                // Initialize a pointer to find the end of the current line.
                const char* line_end = p;
                // Move the pointer forward until a newline or the end of the chunk is reached.
                while (line_end < end && *line_end != '\n') line_end++;
                
                // Increment the transaction count for this thread every time a new line is identified.
                local_trans_counts[tid]++;
                // Extract every word (token) from the current line.
                while (p < line_end) {
                    // Use a fast tokenizer to get the next item as a lightweight string_view.
                    std::string_view item = fast_get_token(p, line_end);
                    // If the token isn't empty, add it to the thread's local set of unique items.
                    if (!item.empty()) {
                        local_sets[tid].insert(item);
                    }
                }
                // Skip the newline character to move to the next transaction.
                p = line_end + 1;
            }
        }

        // [Part 3: Serial Merge - Assign Global IDs]
        // Initialize a global counter for the total number of transactions in the entire file.
        int total_trans = 0;
        // Prepare a list of offsets so we know where each thread's transaction IDs begin.
        std::vector<int> trans_offsets(num_threads, 0);
        // Create a single global set to merge all unique items from all threads.
        std::unordered_set<std::string_view> global_distinct_items;
        
        // Loop through each thread's results to consolidate them.
        for (int i = 0; i < num_threads; ++i) {
            // Store the starting ID for this thread's transactions.
            trans_offsets[i] = total_trans;
            // Add this thread's count to the running total.
            total_trans += local_trans_counts[i];
            // Insert all unique items found by this thread into the global set.
            global_distinct_items.insert(local_sets[i].begin(), local_sets[i].end());
            // Clear the thread-local set immediately to free up memory.
            local_sets[i].clear(); 
        }

        // Initialize a counter to assign a unique integer ID to every unique string item.
        int itemIdx = 0;
        // Create a temporary map to look up integer IDs using string names.
        std::unordered_map<std::string_view, int> intToId; 
        
        // Iterate through the final list of all distinct items found in the file.
        for (const auto& val : global_distinct_items) {
            // Map the current item name to the current index value.
            intToId[val] = itemIdx;
            
            // we will use itemIdx as the unique integer ID for this item in all future processing.
            // The real item name can be retrieved later using 'idToItem' when we need to output results.
            this->idToItem[itemIdx] = std::string(val); 
            
            // Increment the index for the next unique item.
            itemIdx++;
        }
        // Save the total count of transactions found in the file to the class state.
        this->num_of_transactions = total_trans;
        // Save the total count of unique items found to the class state.
        this->num_of_items = itemIdx;

        // [Part 4: Pass 2 - Populate Vertical DB (vR)]
        // Pre-allocate a 3D structure: [thread_id][item_id][list_of_transaction_ids].
        std::vector<std::vector<std::vector<int>>> local_vR_vec(num_threads, 
                                                 std::vector<std::vector<int>>(num_of_items));

        // Start the second parallel pass to map items to their specific transaction IDs.
        #pragma omp parallel num_threads(num_threads)
        {
            // Get the current thread's ID.
            int tid = omp_get_thread_num();
            // Set the pointer to the start of this thread's assigned chunk.
            const char* p = boundaries[tid];
            // Set the pointer to the end of this thread's assigned chunk.
            const char* end = boundaries[tid + 1];
            // Initialize the current transaction ID using the pre-calculated offset for this thread.
            int current_trans = trans_offsets[tid];

            // Loop through the chunk again to record item occurrences.
            while (p < end) {
                // Locate the end of the current line.
                const char* line_end = p;
                // Move forward until the newline character.
                while (line_end < end && *line_end != '\n') line_end++;
                
                // Process each item in the current line.
                while (p < line_end) {
                    // Extract the item name.
                    std::string_view item = fast_get_token(p, line_end);
                    
                    // Proceed only if the extracted item is valid.
                    if (!item.empty()) {
                        // Find the previously assigned integer ID for this string name.
                        auto it = intToId.find(item);
                        // If the item exists in our global map (it should), process it.
                        if (it != intToId.end()) {
                            // Get the integer ID.
                            int id = it->second;
                            // Reference the list of transaction IDs for this specific item and thread.
                            auto& tids = local_vR_vec[tid][id];
                            
                            // To handle data duplicates in the same line, only add the transaction ID if it's new.
                            if (tids.empty() || tids.back() != current_trans) {
                                tids.push_back(current_trans);
                            }
                        }
                    }
                }
                // Increment the transaction counter for the next line.
                current_trans++;
                // Move to the start of the next line.
                p = line_end + 1; 
            }
        }

        // [Part 5: Final Merge - Consolidate results into global vR]
        // Create the final global vertical database map.
        std::unordered_map<int, std::vector<int>> vR; 
        // Iterate through every unique item to merge its occurrences from all threads.
        for (int id = 0; id < num_of_items; ++id) {
            // Initialize a counter to find out how many total transactions this item appears in.
            size_t total_size = 0;
            // Sum up the sizes from every thread's local list for this specific item.
            for (int tid = 0; tid < num_threads; ++tid) {
                total_size += local_vR_vec[tid][id].size();
            }

            // Pre-allocate the vector for this item to avoid expensive memory reallocations during merging.
            vR[id].reserve(total_size);
            // Append each thread's local list of transaction IDs into the global list.
            for (int tid = 0; tid < num_threads; ++tid) {
                // Only merge if the thread actually found this item.
                if (!local_vR_vec[tid][id].empty()) {
                    // Efficiently copy the thread's local data into the global database.
                    vR[id].insert(vR[id].end(), 
                                local_vR_vec[tid][id].begin(), 
                                local_vR_vec[tid][id].end());
                    
                    // Clear the thread-local data immediately to keep memory usage as low as possible.
                    local_vR_vec[tid][id].clear();
                    // Force the vector to release its allocated memory back to the system.
                    local_vR_vec[tid][id].shrink_to_fit();
                }
            }
        }
        reading_time = std::chrono::steady_clock::now();
        std::cout << "Dataset reading 15d ended: " << std::chrono::duration_cast<std::chrono::milliseconds>(reading_time - start_time).count() / 1000.0 << " s\n";


        // Rank items by support
        std::vector<ItemStat> stats;
        for (auto& [id, tids] : vR) stats.push_back({(int)tids.size(), id});
        
        std::sort(stats.begin(), stats.end(), [](const ItemStat& a, const ItemStat& b) {
            return a.first > b.first; 
        });

        // Determine Initial min_count and Cutoff
        int mS = (stats.size() >= topK) ? stats[topK-1].first : 0;
        this->min_count = mS;

        // [Part 3: Determine Cutoff & Pre-allocate - Serial]
        // We calculate exactly how many items we need to process (cutoff) to avoid 'break' inside parallel loop
        int cutoff=0;
        if (stats.size() >= (size_t)topK) {
            this->min_count = stats[topK - 1].first;
            cutoff=topK - 1;
        }
        while(cutoff < stats.size() && stats[cutoff].first >= min_count) {
            cutoff++;
        }
        
        // Pre-allocate memory to allow safe parallel writing
        // This removes the need for 'push_back' and locks
        rankToRaw.resize(cutoff);
        std::vector<Candidate> l1(cutoff);
        std::vector<int> heapInit(cutoff);
        topKFI.resize(cutoff);


        if (cutoff>=1000){
            omp_set_num_threads(omp_get_num_procs()); // Force use of all logical cores
        }else{ 
            omp_set_num_threads(1); // For small values of K (<1000), use single thread to avoid overhead
        }

        #pragma omp parallel
        {

            //DynamicBitSet bs;
            //bs.resize(num_of_transactions);
            // Every thread creates ONE workspace bitset once
            DynamicBitSet workspace;
            workspace.resize(num_of_transactions);

            // [Part 4: Parallel Bitset Creation - The Optimization]
            // Process multiple items in parallel. Each thread gets its own 'i' index.
            // No Race Conditions because every thread writes to a unique index 'i'.
            #pragma omp for schedule(dynamic)
            //#pragma omp for schedule(static)
            for (int i = 0; i < cutoff; ++i) {
                
                int rawID = stats[i].second;
                int sup = stats[i].first;

                rankToRaw[i]=rawID;
                heapInit[i]=sup;

                // Reset the workspace instead of reallocating
                std::fill(workspace.data.begin(), workspace.data.end(), 0);
                
                //This inner loop runs serially, but multiple threads
                //const std::vector<int>& tids = vR.at(stats[i].second);
                const std::vector<int>& tids = vR[rawID];
                for (int t : tids) workspace.set(t);

                topKFI[i]={{i}, sup};
                l1[i]={{i}, workspace, sup};

            }
        }

        bitset_time = std::chrono::steady_clock::now();
        std::cout << "bitset transformation 15c: " << std::chrono::duration_cast<std::chrono::milliseconds>(bitset_time - reading_time).count() / 1000.0 << " s\n";

        heap.initialFill(heapInit);
        std::sort(l1.begin(), l1.end());
        return l1;
    }

    // Updates 'topKFI', 'min_count', and prunes 'nextLevelData' in place.
    void performGetTopKFI(std::vector<Candidate>& nextLevelData) {
        // 1. Sort Global Results by Support Descending
        std::sort(topKFI.begin(), topKFI.end(), std::greater<TopKFIM>());

        // 2. Calculate New Threshold (K-th item logic)
        // We keep items equal to the K-th support (Ties)
        if (topKFI.size() > (size_t)topK) {
            int kSup = topKFI[topK - 1].support;
            
            // Find the cutoff point (include all ties of K-th item)
            size_t cutoff = topK;
            while (cutoff < topKFI.size() && topKFI[cutoff].support == kSup) {
                cutoff++;
            }
            
            // Update min_count
            min_count = topKFI[cutoff - 1].support;

            // Prune Global Results (topKFI)
            topKFI.resize(cutoff);
        } 

        // 3. Prune Candidates (nextLevelData) - MEMORY OPTIMIZATION
        // Remove candidates that fell below the NEW min_count.
        // Their bitsets will be destroyed here, freeing memory.
        nextLevelData.erase(
            std::remove_if(nextLevelData.begin(), nextLevelData.end(),
                [this](const Candidate& c) { return c.support < min_count; }),
            nextLevelData.end()
        );
    }

};

// ==========================================
// 4. MAIN ENTRY POINT
// ==========================================
int main(int argc, char** argv) {

    //omp_set_dynamic(0);                      // disable dynamic adjustment

    if (argc < 3) {
        std::cout << "Usage: ./htkminer <dataset_path> <K> [bitset_mode 1/0]\n";
        return 1;
    }

    std::string delim = (argc >= 5) ? argv[4] : " ";

    //argv[2] --> Top-K
    //argv[3] --> Bitset Mode (1 for Intersection, 0 for Diffset) not working in this version
    //argv[4] --> Delimiter (optional, default is space)
    HTKMiner miner(std::stoi(argv[2]), true, delim); 
    miner.mine(argv[1]);
    std::cout << "Peak Memory Usage: " << std::setprecision(0) << getPeakRSS() / (1024.0 * 1024.0) << " MB" << std::endl;
    miner.saveResults("output.txt");
    return 0;
}