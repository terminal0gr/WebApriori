#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <map>
#include <chrono>
#include <bit> // For std::popcount (C++20)

// ==========================================
// 1. HIGH-PERFORMANCE BITSET
// ==========================================
struct DynamicBitSet {
    std::vector<uint64_t> data;
    size_t num_bits;

    DynamicBitSet() : num_bits(0) {}
    void resize(size_t n_bits) {
        num_bits = n_bits;
        data.assign((n_bits + 63) / 64, 0);
    }
    void set(size_t index) {
        data[index / 64] |= (1ULL << (index % 64));
    }
    size_t count() const {
        size_t c = 0;
        for (uint64_t val : data) {
            #if defined(__cpp_lib_bitops)
                c += std::popcount(val);
            #else
                c += __builtin_popcountll(val);
            #endif
        }
        return c;
    }
    static DynamicBitSet intersect(const DynamicBitSet& a, const DynamicBitSet& b) {
        DynamicBitSet res;
        res.num_bits = a.num_bits;
        res.data.resize(a.data.size());
        for (size_t i = 0; i < a.data.size(); ++i) res.data[i] = a.data[i] & b.data[i];
        return res;
    }
    static DynamicBitSet diff(const DynamicBitSet& a, const DynamicBitSet& b) {
        DynamicBitSet res;
        res.num_bits = a.num_bits;
        res.data.resize(a.data.size());
        for (size_t i = 0; i < a.data.size(); ++i) res.data[i] = b.data[i] & (~a.data[i]);
        return res;
    }
};

// ==========================================
// 2. TOP-K RESULT MANAGER (TIE-AWARE)
// ==========================================
// This replaces the QuickHeap and the final list.
// It ensures that size() is exactly K + (all items with same support as K-th).
class ResultManager {
    std::map<int, std::vector<std::vector<int>>, std::greater<int>> data;
    size_t K;
    int current_min_sup = 0;
    size_t total_count = 0;

public:
    ResultManager(size_t k) : K(k) {}

    void add(const std::vector<int>& itemset, int support) {
        if (support < current_min_sup && total_count >= K) return;

        data[support].push_back(itemset);
        total_count++;

        // Update threshold and prune if we exceed K
        if (total_count >= K) {
            size_t seen = 0;
            int new_min_sup = 0;
            for (auto const& [sup, list] : data) {
                seen += list.size();
                if (seen >= K) {
                    new_min_sup = sup;
                    break;
                }
            }

            if (new_min_sup > current_min_sup) {
                current_min_sup = new_min_sup;
                // Prune everything strictly less than new_min_sup
                auto it = data.upper_bound(current_min_sup); 
                while (it != data.end()) {
                    total_count -= it->second.size();
                    it = data.erase(it);
                }
            }
        }
    }

    int getThreshold() const { return current_min_sup; }
    size_t size() const { return total_count; }
    auto& getData() { return data; }
};

// ==========================================
// 3. CANDIDATE STRUCTURE
// ==========================================
struct Candidate {
    std::vector<int> itemset;
    DynamicBitSet bits;
    int support;

    // Sorting for Level-Generation (Lexicographical)
    bool operator<(const Candidate& other) const {
        return itemset < other.itemset;
    }
};


// ==========================================
// 1. QUICK HEAP (Sorted Array Implementation)
// ==========================================
// Matches Python's logic: A fixed-size array kept sorted Descending.
class QuickHeap {
    int K;
    std::vector<int> heapList;

public:
    QuickHeap(int k) : K(k) {
        heapList.reserve(K + 1);
    }

    // Corresponds to: self.heap.initialFill(list(item1TopK.values()))
    void initialFill(const std::vector<int>& supports) {
        heapList = supports;
        // Keep only top K (the input supports are already sorted descending from InitialTopKFI)
        if (heapList.size() > K) {
            heapList.resize(K);
        }
    }

    // Corresponds to: self.heap.insert(support)
    // Returns the new minimum support threshold (the last item in the list)
    int insert(int value) {
        if (heapList.empty()) {
            heapList.push_back(value);
            return 0; // Heap not full yet
        }

        // Optimization: Early exit if value is worse than the worst item
        if (heapList.size() >= K && value <= heapList.back()) {
            return heapList.back();
        }

        // Binary Search for insertion point (Descending Order)
        // std::upper_bound with std::greater finds the first element strictly smaller than value
        auto it = std::upper_bound(heapList.begin(), heapList.end(), value, std::greater<int>());
        heapList.insert(it, value);

        if (heapList.size() > K) {
            heapList.pop_back(); // Remove smallest
        }

        // If heap is full, return the K-th support (the pruning threshold)
        if (heapList.size() == K) return heapList.back();
        return 0;
    }

    // Helper to get current minSup from heap
    int getMinSup() const {
        if (heapList.size() < K) return 0;
        return heapList.back();
    }
};



// ==========================================
// 4. HTK-MINER MAIN CLASS
// ==========================================
class HTKMiner {
    ResultManager results;
    QuickHeap heap{1}; // Placeholder, will be initialized properly in readDatasetFile
    int minCount = 0; //Absolute minimum support count (not percentage)
    double minSup=0; // Relative minimum support threshold as percentage

    // Bidirectional dictionary implementation. Mappings for Item <-> ID
    std::unordered_map<std::string, int> itemToId;
    std::unordered_map<int, std::string> idToItem;

    int topK;
    int num_of_transactions = 0; 
    int itemCount = 0;

    //Program parameters for the BS, BSN, DBS, DBSN modes
    bool bitSet=true; // true = use bitsets, false = use tid sets
    bool tidSet; // true = intersection, false = diffset


    std::string delimiter;

public:
    HTKMiner(int k, std::string delim = " ", bool mode = true) 
        : results(k), delimiter(delim), tidSet(mode), topK(k) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // Level 1
        std::vector<Candidate> currentLevel = readDatasetFile(filepath);
        std::cout << "Level 1 items: " << currentLevel.size() << "\n";

        int level = 1;
        while (!currentLevel.empty()) {
            std::vector<Candidate> nextLevel;
            int n = currentLevel.size();
            int minSup = results.getThreshold();

            for (int i = 0; i < n; ++i) {
                if (currentLevel[i].support < minSup) continue;

                for (int j = i + 1; j < n; ++j) {
                    if (currentLevel[j].support < minSup) continue;

                    // Prefix Check (Length - 1 match)
                    bool match = true;
                    for (int k = 0; k < level - 1; ++k) {
                        if (currentLevel[i].itemset[k] != currentLevel[j].itemset[k]) {
                            match = false; break;
                        }
                    }

                    if (match) {
                        DynamicBitSet newBits;
                        int newSup = 0;

                        if (tidSet || level == 1) { // L1 to L2 is always intersection
                            newBits = DynamicBitSet::intersect(currentLevel[i].bits, currentLevel[j].bits);
                            newSup = newBits.count();
                        } else {
                            // DiffSet: Sup(New) = Sup(A) - Count(A \ B)
                            newBits = DynamicBitSet::diff(currentLevel[i].bits, currentLevel[j].bits);
                            newSup = currentLevel[i].support - newBits.count();
                        }

                        if (newSup >= results.getThreshold() || results.size() < 10) { // logic for early K
                            std::vector<int> newKey = currentLevel[i].itemset;
                            newKey.push_back(currentLevel[j].itemset.back());
                            
                            results.add(newKey, newSup);
                            nextLevel.push_back({newKey, std::move(newBits), newSup});
                            minSup = results.getThreshold(); // Update local minSup
                        }
                    } else {
                        // Optimization: Since sorted, if prefix doesn't match, 
                        // no further J will match this I.
                        break;
                    }
                }
            }
            currentLevel = std::move(nextLevel);
            // Re-sort current level to ensure prefix-matching works for the next level
            std::sort(currentLevel.begin(), currentLevel.end());
            level++;
            std::cout << "Moving to Level " << level << " (Candidates: " << currentLevel.size() << ")\n";
        }

        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() / 1000.0;
        std::cout << "\nFound " << results.size() << " itemsets in " << elapsed << "s\n";
    }

    void saveResults(const std::string& outPath) {
        std::ofstream out(outPath);
        for (auto const& [sup, list] : results.getData()) {
            for (auto const& itemset : list) {
                for (size_t i = 0; i < itemset.size(); ++i) {
                    out << idToItem[itemset[i]] << (i == itemset.size() - 1 ? "" : " ");
                }
                out << " #SUP: " << sup << "\n";
            }
        }
    }

private:
    std::vector<Candidate> readDatasetFile(const std::string& path) {
        std::ifstream file(path);
        std::string line;
        std::unordered_map<int, std::vector<int>> vR;
        int transIndex = 0;
        int itemIndex = 0;
        int id;

        while (std::getline(file, line)) {
            std::stringstream ss(line);
            std::string item;
            while (ss >> item) {
                if (itemToId.find(item) == itemToId.end()) {
                    itemIndex++;
                    itemToId[item] = id = itemIndex;
                    idToItem[itemIndex] = item;
                } else {
                    id = itemToId[item];
                    if (vR[id].empty() || vR[id].back() != transIndex) {
                        vR[id].push_back(transIndex);
                    }
                        
                }
            }
            transIndex++;
        }
        num_of_transactions = transIndex;
        itemCount = itemIndex;


        // Context: 
        // 'vR' is your VerticalDB (std::unordered_map<int, std::vector<int>>) filled from readDataset.
        // 'heap' is an instance of QuickHeap.
        // 'topK' is your K value.

        // --- LINE 1: item1TopK, self.min_count = self.InitialTopKFI(vR) ---
        int min_count = 0;
        auto result_pair = InitialTopKFI(vR, topK, min_count);
        std::vector<ItemStat> item1TopK = result_pair.first;
        // Note: item1TopK is vector<pair<Support, ItemID>>, sorted by Support Descending.

        // --- LINE 2: self.heap.initialFill(list(item1TopK.values())) ---
        // We extract just the supports from item1TopK for the heap
        std::vector<int> initialSupports;
        initialSupports.reserve(item1TopK.size());
        for (const auto& p : item1TopK) {
            initialSupports.push_back(p.first);
        }
        heap.initialFill(initialSupports);

        // --- LINE 3: vR = {key: vR[key] for key in item1TopK if key in vR} ---
        // In C++, we prune 'vR' in place to save memory.
        // We create a "Keep List" (Set) for O(1) lookup, or just iterate vR.
        // Since we want to KEEP only what is in item1TopK, it's faster to rebuild vR or erase from it.

        // Optimization: Mark valid IDs
        std::unordered_set<int> keepSet;
        for (const auto& p : item1TopK) {
            keepSet.insert(p.second); 
        }

        // Pruning vR
        // Erase non-frequent items from vR
        for (auto it = vR.begin(); it != vR.end(); ) {
            if (keepSet.find(it->first) == keepSet.end()) { // If NOT in our keepSet
                it = vR.erase(it); // Efficiently remove and get next iterator
            } else {
                ++it;
            }
        }
        // keepSet can be cleared here if memory is a concern
        //keepSet.clear();

        // Now 'vR' contains ONLY the Top-K items + Ties.
        // NOW you can proceed to convert 'vR' to BitSets if needed.

        std::vector<Candidate> l1;
        for (auto& [id, tids] : vR) {
            DynamicBitSet bs;
            bs.resize(num_of_transactions);
            for (int t : tids) bs.set(t);
            int sup = tids.size();
            
            results.add({id}, sup);
            l1.push_back({{id}, std::move(bs), sup});
        }
        std::sort(l1.begin(), l1.end());
        return l1;
    }




    // Type aliases for cleaner code
    // ItemID -> List of Transaction IDs
    using VerticalDB = std::unordered_map<int, std::vector<int>>; 
    // Support, ItemID pair (Value, Key)
    using ItemStat = std::pair<int, int>; 

    // ==========================================
    // 2. InitialTopKFI Implementation
    // ==========================================
    // Returns: 
    // 1. A vector of {ItemID, Support} pairs (The "item1TopK" dict)
    // 2. The calculated min_count
    std::pair<std::vector<ItemStat>, int> InitialTopKFI(const VerticalDB& vR, int topK, int& min_count_out) {
        
        // 1. Collect all supports
        std::vector<ItemStat> stats;
        stats.reserve(vR.size());
        for (const auto& [item, tids] : vR) {
            stats.push_back({(int)tids.size(), item});
        }

        // 2. Sort Descending by Support
        // Logic: Sort by Support Descending. If supports equal, sort by ItemID Descending (to match Python tuple sort)
        std::sort(stats.begin(), stats.end(), [](const ItemStat& a, const ItemStat& b) {
            if (a.first != b.first) return a.first > b.first;
            return a.second > b.second;
        });

        // 3. Handle "Not enough items" case
        if (stats.size() < topK) {
            min_count_out = 0;
            return {stats, 0};
        }

        // 4. Find the cutoff point (K-th item logic with ties)
        int mS = -1;
        size_t cutoffIndex = 0;

        for (size_t i = 0; i < stats.size(); ++i) {
            // Python: if index >= self.topK-1:
            if (i >= topK - 1) {
                if (mS == -1) {
                    mS = stats[i].first; // This is the support of the K-th item
                } else if (stats[i].first != mS) {
                    // We found a support different from the K-th item's support. Stop.
                    break;
                }
            }
            cutoffIndex++;
        }

        // 5. Create the result "Dictionary" (Vector of survivors)
        // We only keep items up to cutoffIndex
        std::vector<ItemStat> item1TopK;
        item1TopK.reserve(cutoffIndex);
        for (size_t i = 0; i < cutoffIndex; ++i) {
            item1TopK.push_back(stats[i]); // Pushing (Support, ID)
        }

        min_count_out = (mS == -1) ? 0 : mS;
        return {item1TopK, min_count_out};
    }



};





int main(int argc, char** argv) {
    if (argc < 3) {
        std::cout << "Usage: ./htk <file> <K> [mode 1=intersect/0=diff]\n";
        return 1;
    }
    HTKMiner miner(std::stoi(argv[2]), " ", (argc > 3 ? std::stoi(argv[3]) == 1 : true));
    miner.mine(argv[1]);
    miner.saveResults("output.txt");
    return 0;
}