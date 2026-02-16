#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <unordered_set>
#include <chrono>
#include <bit> // For std::popcount (C++20)

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
    std::vector<int> items; // Stores Rank IDs
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

    // Lexicographical sort on Ranks synchronized with Support in Descending order
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
    
    QuickHeap heap;
    int min_count = 0;
    int topK;
    int num_of_transactions = 0;
    int num_of_items = 0;
    bool tidSet; // true = intersection mode, false = diffset mode
    std::vector<TopKFIM> finalTopK;

    using ItemStat = std::pair<int, int>; // {Support, RawID}

public:
    HTKMiner(int k, bool mode = true) : heap(k), topK(k), tidSet(mode) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // Step 1: Read, Rank and bitset conversion
        std::vector<Candidate> currentLevel = readAndRank(filepath);
 
        std::cout << "Level 1 Frequent Items: " << currentLevel.size() << "\n";
        std::cout << "Initial MinSup: " << min_count << "\n";

        // 2. Main Mining Loop
        int level = 1;
        while (!currentLevel.empty()) {
            std::vector<Candidate> nextLevel;
            int n = currentLevel.size();
            // Reserve memory heuristic: next level usually smaller or similar
            nextLevel.reserve(n); 

            //For debugging purposes
            // for (int i=0; i<n; i++ ) {
            //     std::cout << "Currentlevel " << level << " Item:"  << currentLevel[i].itemset[0] << " Sup:" << currentLevel[i].support << "\n";
            // }

            // ==========================================
            // SMART ITERATION MECHANISM (SIME)
            // ==========================================
            for (int j = 1; j < n; ++j) {
                // Pruning A: If the j-th itemset is below min_count, all subsequent itemsets are too
                if (currentLevel[j].support < min_count) continue;

                for (int i = 0; i < j; ++i) {
                    // Pruning B: Since i < j and sorted by support, if i is below, j is definitely below
                    if (currentLevel[i].support < min_count) continue;

                    // Pruning C: Prefix Matching 
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

                        //if (tidSet || level == 1) {
                            // Intersection Mode (or Level 1 -> 2 transition)
                            newBits = DynamicBitSet::intersect(currentLevel[i].bits, currentLevel[j].bits);
                            newSup = newBits.count();
                        //} else {
                            // DiffSet Mode: Sup(AB) = Sup(A) - Count(A \ B)
                            // Note: We use diff(B, A) -> B & ~A. 
                            // Logic: transactions missing in B that were in A.
                        //    newBits = DynamicBitSet::diff(currentLevel[i].bits, currentLevel[j].bits);
                        //    newSup = currentLevel[i].support - newBits.count();
                        //}

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
                    	//TODO Experiment if we have gain with this here...
                        // Optimization: Because list is sorted, if prefix differs, 
                        // no subsequent 'j' will match this 'i'.
                        //break;
                    }
                }
            }
            // Move to next level
            currentLevel = std::move(nextLevel);
            // Sort to enable Prefix Optimization for next pass
            std::sort(currentLevel.begin(), currentLevel.end()); // Maintains Rank/Support Order

            level++;

            std::cout << "Level " << level << " Candidates: " << currentLevel.size() << " | MinSup: " << min_count << "\n";

            
        }

        cleanupResults();
        auto end = std::chrono::high_resolution_clock::now();

		//Statistics
        double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() / 1000.0;
        std::cout << "Total Execution Time: " << elapsed << " s\n";
        std::cout << "FIM found: " << finalTopK.size() << "\n";
        std::cout << "Absolute minSup: " << min_count << "\n";
    }

    void saveResults(const std::string& path) {
        std::ofstream out(path);
        for (const auto& res : finalTopK) {
            for (size_t i = 0; i < res.items.size(); ++i) {
                out << idToItem[rankToRaw[res.items[i]]] << (i == res.items.size()-1 ? "" : " ");
            }
            out << " #SUP: " << res.support << "\n";
        }
    }

private:
    std::vector<Candidate> readAndRank(const std::string& path) {
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

        // Rank items by support
        std::vector<ItemStat> stats;
        for (auto& [id, tids] : vR) stats.push_back({(int)tids.size(), id});
        
        std::sort(stats.begin(), stats.end(), [](const ItemStat& a, const ItemStat& b) {
            return a.first > b.first; 
        });

        // Determine Initial min_count and Cutoff
        int mS = (stats.size() >= topK) ? stats[topK-1].first : 0;
        this->min_count = mS;

        std::vector<int> heapInit;
        std::vector<Candidate> l1;
        for (size_t rank = 0; rank < stats.size(); ++rank) {
            if (stats[rank].first < min_count) break;
            
            int rawID = stats[rank].second;
            int sup = stats[rank].first;

            rankToRaw.push_back(rawID);
            heapInit.push_back(sup);

            DynamicBitSet bs;
            bs.resize(num_of_transactions);
            for (int t : vR[rawID]) bs.set(t);

            finalTopK.push_back({{(int)rank}, sup});
            l1.push_back({{(int)rank}, std::move(bs), sup});
        }
        heap.initialFill(heapInit);
        std::sort(l1.begin(), l1.end());
        return l1;
    }

    void cleanupResults() {
        finalTopK.erase(std::remove_if(finalTopK.begin(), finalTopK.end(),
            [this](const TopKFIM& f) { return f.support < min_count; }), finalTopK.end());
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

    HTKMiner miner(std::stoi(argv[2]));
    miner.mine(argv[1]);
    std::cout << "Peak Memory Usage: " << getPeakRSS() / (1024.0 * 1024.0) << " MB" << std::endl;
    miner.saveResults("output.txt");
    return 0;
}