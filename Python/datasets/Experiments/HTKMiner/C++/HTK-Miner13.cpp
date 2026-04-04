#include <iostream>
#include <iomanip> // Required for setprecision and fixed
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <chrono>
#include <bit> // For std::popcount (C++20)
#include <omp.h>

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
    static DynamicBitSet intersect(const DynamicBitSet& a, const DynamicBitSet& b) {
        DynamicBitSet res;
        res.num_bits = a.num_bits;
        res.data.resize(a.data.size());
        for (size_t i = 0; i < a.data.size(); ++i) {
        	res.data[i] = a.data[i] & b.data[i];
        }
        return res;
    }
    // Difference: B & (~A) -> Items in B that are NOT in A
    static DynamicBitSet diff(const DynamicBitSet& a, const DynamicBitSet& b) {
        DynamicBitSet res;
        res.num_bits = a.num_bits;
        res.data.resize(a.data.size());
        for (size_t i = 0; i < a.data.size(); ++i) {
        	res.data[i] = a.data[i] & (~b.data[i]);
		}
        return res;
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
// 2. THE Htk-Miner CLASS
// ==========================================

class HTKMiner {
	
private:
    // Mappings (The 3-Tier System)
    std::unordered_map<std::string, int> itemToId; // Name -> RawID
    std::unordered_map<int, std::string> idToItem; // RawID -> Name
    std::vector<int> rankToRaw;                    // Rank -> RawID
    
    std::vector<TopKFIM> topKFI; // The global Top-K results (matches Python 'topKFI')
    QuickHeap heap;
    int min_count = 0;
    int topK;
    int num_of_transactions = 0;
    int num_of_items = 0;
    bool tidSet; // true = intersection mode, false = diffset mode

    // Time variables for statistics (C++20 chrono)
    using TimePoint = std::chrono::steady_clock::time_point;
    TimePoint start_time;
    TimePoint reading_time;
    TimePoint bitset_time;
    TimePoint end_time;

    using ItemStat = std::pair<int, int>; // {Support, RawID}

public:
    HTKMiner(int k, bool mode = true) : heap(k), topK(k), tidSet(mode) {}

    void mine(const std::string& filepath) {
        start_time = std::chrono::steady_clock::now();

        // Step 1: Read, Rank and bitset conversion
        std::vector<Candidate> currentLevelData= readAndRank(filepath);
 
        // Initial Pruning/Threshold update
        performGetTopKFI(currentLevelData); // Update min_count and prune currentLevel

        // 2. Main Mining Loop
        int level = 1;
        while (!currentLevelData.empty()) {
            std::vector<Candidate> nextLevelData;
            int n = currentLevelData.size();
            // Reserve memory heuristic: next level usually smaller or similar
            // nextLevelData.reserve(n); 

            // ==========================================
            // SMART ITERATION MECHANISM (SIME)
            // ==========================================
            for (int j = 1; j < n; ++j) {
                // Pruning A: If the j-th itemset is below min_count, all subsequent itemsets are too
                if (currentLevelData[j].support < min_count) break;

                for (int i = 0; i < j; ++i) {
                    // Pruning B: Since i < j and sorted by support, if i is below, j is definitely below
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
                        DynamicBitSet newBits;
                        int newSup = 0;

                        //if (tidSet || level == 1) {
                            // Intersection Mode (or Level 1 -> 2 transition)
                            newBits = DynamicBitSet::intersect(currentLevelData[i].bits, currentLevelData[j].bits);
                            newSup = newBits.count();
                        //} else {
                            // DiffSet Mode: Sup(AB) = Sup(A) - Count(A \ B)
                            // Note: We use diff(B, A) -> B & ~A. 
                            // Logic: transactions missing in B that were in A.
                        //    newBits = DynamicBitSet::diff(currentLevel[i].bits, currentLevel[j].bits);
                        //    newSup = currentLevel[i].support - newBits.count();
                        //}

                        if (newSup >= min_count) {
                            
                            // 1. Update Heap & Threshold
                            min_count = heap.insert(newSup);

                            // 2. Create Itemset Key
                            std::vector<int> newKey = currentLevelData[i].itemset;
                            newKey.push_back(currentLevelData[j].itemset.back());

                            // 4. Add to Next Level Candidates
                            nextLevelData.push_back({std::move(newKey), std::move(newBits), newSup});
                        }
                    }
                }
            }

            // 1. Merge nextLevelTopK into topKFI
            for (const auto& cand : nextLevelData) {
                topKFI.push_back({cand.itemset, cand.support});
            }
            
            // 2. Execute the Global Pruning & Update MinSup
            // This filters 'topKFI' AND prunes 'nextLevelData' (the parents)
            performGetTopKFI(nextLevelData);

            // Move to next level
            currentLevelData= std::move(nextLevelData);
            // Sort to enable Prefix Optimization for next pass
            std::sort(currentLevelData.begin(), currentLevelData.end()); // Maintains Rank/Support Order

            level++;

            //std::cout << "Level " << level << " Candidates: " << currentLevelData.size() << " | MinSup: " << min_count << "\n";
            
        }

        end_time = std::chrono::steady_clock::now();
        std::cout << "FI mining time: " << std::chrono::duration_cast<std::chrono::milliseconds>(end_time-bitset_time).count() / 1000.0 << " s\n";

		//Statistics
        double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end_time-start_time).count() / 1000.0;
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

private:
    std::vector<Candidate> readAndRank(const std::string& path) {

        std::cout << "Read dataset 13 Started\n";

        std::ifstream file(path);
        std::string line;
        std::unordered_map<int, std::vector<int>> vR; 
        int transIndex = 0, itemIndex = 0;


        // 1. Read File Line by Line
        while (std::getline(file, line)) {
            if (line.empty()) continue;
            // Trim CR if present (Windows/Unix compat)
            if (line.back() == '\r') line.pop_back();
            std::stringstream ss(line);
            std::string item;
            while (ss >> item) {
                if (itemToId.find(item) == itemToId.end()) {
                    itemToId[item] = itemIndex;
                    idToItem[itemIndex] = item;
                    itemIndex++;
                }
                int id = itemToId[item];

                // Add transaction ID to this item
                // Check duplicate avoidance (if same item appears twice in one line)
                if (vR[id].empty() || vR[id].back() != transIndex) {
                	vR[id].push_back(transIndex);
                }
            }
            transIndex++;
        }
        this->num_of_transactions = transIndex;
        this->num_of_items = itemIndex;

        reading_time = std::chrono::steady_clock::now();
        std::cout << "Dataset reading 13 ended: " << std::chrono::duration_cast<std::chrono::milliseconds>(reading_time - start_time).count() / 1000.0 << " s\n";

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
            omp_set_num_threads(1); // For small datasets, use single thread to avoid overhead
        }

        // std::cout << "Parallel processing Started\n";
        // auto p1 = std::chrono::high_resolution_clock::now();

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

                // This inner loop runs serially, but multiple threads 
                // are running this outer loop simultaneously for different items.
                // const std::vector<int>& tids = vR.at(rawID);
                // for (int t : tids) {
                //     bs.set(t); 
                // }

                // topKFI[i]={{(int)i}, sup};
                // l1[i]={{(int)i}, std::move(bs), sup};
            }
        }

        bitset_time = std::chrono::steady_clock::now();
        std::cout << "bitset transformation 13: " << std::chrono::duration_cast<std::chrono::milliseconds>(bitset_time - reading_time).count() / 1000.0 << " s\n";

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
        } else {
             // Less than K items found so far
             if (!topKFI.empty()) {
                 // min_count stays 0 or lowest found? 
                 // Usually min_count is 0 until we hit K items.
             }
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

    HTKMiner miner(std::stoi(argv[2]));
    miner.mine(argv[1]);
    std::cout << "Peak Memory Usage: " << std::setprecision(0) << getPeakRSS() / (1024.0 * 1024.0) << " MB" << std::endl;
    miner.saveResults("output.txt");
    return 0;
}