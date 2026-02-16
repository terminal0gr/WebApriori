#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <chrono>

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

// The final result structure (Replacing ResultManager's complex map)
struct TopKFIM {
    std::vector<int> items;
    int support;
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
            res.data[i] = b.data[i] & (~a.data[i]);
        }
        return res;
    }
};

// Candidate for the Mining Loop
struct Candidate {
    std::vector<int> itemset;
    DynamicBitSet bits;
    int support;

    // Lexicographical sort for Prefix Matching
    bool operator<(const Candidate& other) const {
        return itemset < other.itemset;
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
        if (heapList.size() > K) {
            heapList.resize(K);
        }
    }

    // Matches Python: self.heap.insert(support)
    int insert(int value) {
        if (heapList.empty()) {
            heapList.push_back(value);
            return 0; 
        }

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

        if (heapList.size() == K) return heapList.back();
        return 0;
    }

    int getMinSup() const {
        if (heapList.size() < K) return 0;
        return heapList.back();
    }
};

// ==========================================
// 3. HTK-MINER
// ==========================================
class HTKMiner {
    // Core Algorithm State
    QuickHeap heap;
    int min_count = 0; // The dynamic pruning threshold
    std::vector<TopKFIM> finalTopK; // Results storage

    // Dataset Metadata
    std::unordered_map<std::string, int> itemToId;
    std::unordered_map<int, std::string> idToItem;
    int num_of_transactions = 0;
    int num_of_items = 0;
    int topK;
    
    // Configuration
    bool tidSet; // true = intersection mode, false = diffset mode
    std::string delimiter;

    // Helper Typedefs
    using VerticalDB = std::unordered_map<int, std::vector<int>>; 
    using ItemStat = std::pair<int, int>; // {Support, ItemID}

public:
    HTKMiner(int k, std::string delim = " ", bool mode = true) 
        : heap(k), topK(k), delimiter(delim), tidSet(mode) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // 1. Read, Count, Prune, and Convert to BitSets
        std::vector<Candidate> currentLevel = readDatasetFile(filepath);
        
        std::cout << "Level 1 Frequent Items: " << currentLevel.size() << "\n";
        std::cout << "Initial MinSup: " << min_count << "\n";

        // 2. Main Mining Loop
        int level = 1;
        while (!currentLevel.empty()) {
            std::vector<Candidate> nextLevel;
            // Reserve memory heuristic: next level usually smaller or similar
            int n = currentLevel.size();
            nextLevel.reserve(n); 

            //For debugging purposes
            // for (int i=0; i<n; i++ ) {
            //     std::cout << "Currentlevel " << level << " Item:"  << currentLevel[i].itemset[0] << " Sup:" << currentLevel[i].support << "\n";
            // }

            // Loop A
            for (int i = 0; i < n; ++i) {
                if (currentLevel[i].support < min_count) continue;

                // Loop B
                for (int j = i + 1; j < n; ++j) {
                    if (currentLevel[j].support < min_count) continue;

                    // Prefix Check: Match first (level-1) items
                    // Since sorted lexicographically, we can break early?
                    // No, for prefix matching we check strict equality of prefix.
                    bool match = true;
                    for (int k = 0; k < level - 1; ++k) {
                        if (currentLevel[i].itemset[k] != currentLevel[j].itemset[k]) {
                            match = false; 
                            break;
                        }
                    }

                    if (match) {
                        DynamicBitSet newBits;
                        int newSup = 0;

                        if (tidSet || level == 1) { 
                            // Intersection Mode (or Level 1 -> 2 transition)
                            newBits = DynamicBitSet::intersect(currentLevel[i].bits, currentLevel[j].bits);
                            newSup = newBits.count();
                        } else {
                            // DiffSet Mode: Sup(AB) = Sup(A) - Count(A \ B)
                            // Note: We use diff(B, A) -> B & ~A. 
                            // Logic: transactions missing in B that were in A.
                            newBits = DynamicBitSet::diff(currentLevel[i].bits, currentLevel[j].bits);
                            newSup = currentLevel[i].support - newBits.count();
                        }

                        // Check against global MinSup (Top-K threshold)
                        // Also allow filling up to K if not full yet
                        if (newSup >= min_count) {
                            
                            // 1. Update Heap & Threshold
                            min_count = heap.insert(newSup);

                            // 2. Create Itemset Key
                            std::vector<int> newKey = currentLevel[i].itemset;
                            newKey.push_back(currentLevel[j].itemset.back());

                            // 3. Store Result
                            finalTopK.push_back({newKey, newSup});

                            // 4. Add to Next Level Candidates
                            nextLevel.push_back({std::move(newKey), std::move(newBits), newSup});
                        }
                    } else {
                        // Optimization: Because list is sorted, if prefix differs, 
                        // no subsequent 'j' will match this 'i'.
                        break;
                    }
                }
            }

            // Move to next level
            currentLevel = std::move(nextLevel);
            // Sort to enable Prefix Optimization for next pass
            std::sort(currentLevel.begin(), currentLevel.end());
            level++;
            
            std::cout << "Level " << level << " Candidates: " << currentLevel.size() << " | MinSup: " << min_count << "\n";
        }

        // Final Pruning: Remove items that fell out of Top-K during the process
        // because finalTopK accumulated items that *were* frequent at the time of discovery.
        cleanupFinalResults();

        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() / 1000.0;
        
        std::cout << "Total Execution Time: " << elapsed << " s\n";
        std::cout << "FIM found: " << finalTopK.size() << "\n";
        std::cout << "Absolute minSup: " << min_count << "\n";
    }

    void saveResults(const std::string& outPath) {
        std::ofstream out(outPath);
        // Writing in Python format equivalent (Items... #SUP: X)
        for (const auto& res : finalTopK) {
            for (size_t i = 0; i < res.items.size(); ++i) {
                out << idToItem[res.items[i]] << (i == res.items.size() - 1 ? "" : " ");
            }
            out << " #SUP: " << res.support << "\n";
        }
    }

private:
    std::vector<Candidate> readDatasetFile(const std::string& path) {
        std::ifstream file(path);
        std::string line;
        
        // Temp storage: ID -> List[TIDs]
        // Using vector<int> for TIDs initially is faster than BitSet for sparse data
        VerticalDB vR;
        
        int transIndex = 0;
        int itemIndex = 0;

        // 1. Read File Line by Line
        while (std::getline(file, line)) {
            if (line.empty()) continue;
            // Trim CR if present (Windows/Unix compat)
            if (line.back() == '\r') line.pop_back();

            std::stringstream ss(line);
            std::string item;
            while (std::getline(ss, item, ' ')) { // explicit delimiter split
                 if (item.empty()) continue;
                 
                 int id;
                 if (itemToId.find(item) == itemToId.end()) {
                     itemIndex++;
                     itemToId[item] = itemIndex;
                     idToItem[itemIndex] = item;
                     id = itemIndex;
                 } else {
                     id = itemToId[item];
                 }

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

        // 2. InitialTopKFI Logic
        // Calculate supports and find the initial Top-K cutoff
        int cutoff_support = 0;
        auto [item1TopK, calculated_min_count] = InitialTopKFI(vR);
        
        // Update Global Minimum support threshold
        this->min_count = calculated_min_count;

        // 3. Initialize Heap
        std::vector<int> supports;
        supports.reserve(item1TopK.size());
        for (const auto& p : item1TopK) supports.push_back(p.first);
        heap.initialFill(supports);

        // 4. Pruning vR (The "filter" step)
        // KeepSet for O(1) lookup
        std::unordered_set<int> keepSet;
        for (const auto& p : item1TopK) keepSet.insert(p.second);

        // Remove infrequent items from vR
        for (auto it = vR.begin(); it != vR.end(); ) {
            if (keepSet.find(it->first) == keepSet.end()) {
                it = vR.erase(it);
            } else {
                ++it;
            }
        }

        // 5. Convert to BitSets (Candidates)
        std::vector<Candidate> level1TopK;
        level1TopK.reserve(vR.size());

        for (auto& [id, tids] : vR) {
            DynamicBitSet bs;
            bs.resize(num_of_transactions);
            for (int t : tids) bs.set(t);
            
            int sup = tids.size();
            
            // Add to Final Results (Level 1 items are frequent)
            finalTopK.push_back({{id}, sup});
            
            // Add to Candidates for Level 2 generation
            level1TopK.push_back({{id}, std::move(bs), sup});
        }

        // Sort Lexicographically for the mining loop
        std::sort(level1TopK.begin(), level1TopK.end());
        return level1TopK;
    }

    // Matches Python: InitialTopKFI
    // Returns {Vector of (Support, ID), MinCount}
    std::pair<std::vector<ItemStat>, int> InitialTopKFI(const VerticalDB& vR) {

        // 1. Collect all supports from the Vertical Database
        std::vector<ItemStat> stats;
        stats.reserve(vR.size());
        for (const auto& [item, tids] : vR) {
            stats.push_back({(int)tids.size(), item});
        }

        // 2. Sort Descending by Support (Value), then by ItemID (Key)
        std::sort(stats.begin(), stats.end(), [](const ItemStat& a, const ItemStat& b) {
            if (a.first != b.first) return a.first > b.first;
            return a.second > b.second; // Secondary sort by ID desc (optional match)
        });

        int minSup = 0;

        // 3. Handle case where database has fewer items than K
        if (stats.size() < topK) {
            return {stats, 0};
        }

        // 4. Find K-th item logic tie handling: We want to include all items that have the same support as the K-th item
        // with two for loops in order to avoid the memory allocation issue of the std::vector which works similarly, 
        //but every time it runs out of space, it must:
        // 1) Allocate a new, larger block of memory.
        // 2) Copy all existing elements to the new block.
        // 3) Delete the old block.
        int mS = -1;
        size_t cutoffIndex = 0;
        for (size_t i = 0; i < stats.size(); ++i) {
            if (i >= topK - 1) {
                if (mS == -1) mS = stats[i].first;
                else if (stats[i].first != mS) break;
            }
            cutoffIndex++;
        }
        std::vector<ItemStat> item1TopK;
        item1TopK.reserve(cutoffIndex);
        for (size_t i = 0; i < cutoffIndex; ++i) {
            item1TopK.push_back(stats[i]);
        }

        minSup = (mS == -1) ? 0 : mS;
        return {item1TopK, minSup};
    }

    void cleanupFinalResults() {
        // Remove any results that are less than the FINAL min_count
        // This handles cases where items were added when min_count was low,
        // but the bar was raised later.
        finalTopK.erase(
            std::remove_if(finalTopK.begin(), finalTopK.end(),
                [this](const TopKFIM& item) { return item.support < min_count; }),
            finalTopK.end()
        );
    }
};

// ==========================================
// 4. MAIN ENTRY POINT
// ==========================================
int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "Usage: ./htkminer <dataset_path> <K> [bitset_mode 1/0]\n";
        return 1;
    }

    std::string path = argv[1];
    int k = std::stoi(argv[2]);
    bool mode = (argc > 3) ? (std::stoi(argv[3]) == 1) : true;

    HTKMiner miner(k, " ", mode);
    miner.mine(path);
    
    std::cout << "Peak Memory Usage: " << getPeakRSS() / (1024.0 * 1024.0) << " MB" << std::endl;

    miner.saveResults("output.txt");

    return 0;
}