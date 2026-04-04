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

struct TopKFIM {
    std::vector<int> items; 
    int support;
};

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
            #elif defined(__GNUC__) || defined(__clang__)
                c += __builtin_popcountll(val);
            #else
                val = val - ((val >> 1) & 0x5555555555555555ULL);
                val = (val & 0x3333333333333333ULL) + ((val >> 2) & 0x3333333333333333ULL);
                c += (((val + (val >> 4)) & 0x0F0F0F0F0F0F0F0FULL) * 0x0101010101010101ULL) >> 56;
            #endif
        }
        return c;
    }
    static DynamicBitSet intersect(const DynamicBitSet& a, const DynamicBitSet& b) {
        DynamicBitSet res;
        res.num_bits = a.num_bits;
        res.data.resize(a.data.size());
        for (size_t i = 0; i < a.data.size(); ++i) {
        	res.data[i] = a.data[i] & b.data[i];
        }
        return res;
    }
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

struct Candidate {
    std::vector<int> itemset; 
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
// 2. QUICK HEAP
// ==========================================
class QuickHeap {
    int K;
    std::vector<int> heapList;

public:
    QuickHeap(int k) : K(k) { 
    	heapList.reserve(K + 1); 
    }

    void initialFill(const std::vector<int>& supports) {
        heapList = supports;
        std::sort(heapList.begin(), heapList.end(), std::greater<int>());
        if (heapList.size() > K) {
        	heapList.resize(K);
        }
    }

    int insert(int value) {
        if (heapList.size() >= K && value <= heapList.back()) {
        	return heapList.back();
        }
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
// 3. HTK-MINER CLASS
// ==========================================

class HTKMiner {
private:
    std::unordered_map<std::string, int> itemToId; 
    std::unordered_map<int, std::string> idToItem; 
    std::vector<int> rankToRaw;                    
    
    QuickHeap heap;
    int min_count = 0;
    int topK;
    int num_of_transactions = 0;
    int num_of_items = 0;
    bool tidSet; 
    std::vector<TopKFIM> finalTopK;

    using ItemStat = std::pair<int, int>; 

public:
    HTKMiner(int k, bool mode = true) : heap(k), topK(k), tidSet(mode) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // 1. Read & Create Level 1 (Already Sorted by Support from readAndRank)
        std::vector<Candidate> currentLevel = readAndRank(filepath);
 
        std::cout << "Level 1 Frequent Items: " << currentLevel.size() << "\n";
        std::cout << "Initial MinSup: " << min_count << "\n";

        // 2. Main Mining Loop
        int level = 1;
        while (!currentLevel.empty()) {
            std::vector<Candidate> nextLevel;
            int n = currentLevel.size();
            nextLevel.reserve(n); 

            // ==========================================
            // SIME LOGIC (Smart Iteration Mechanism)
            // ==========================================
            // Order: Support Descending (Guaranteed by std::sort at end of loop)
            // Outer J: 1 -> N
            // Inner I: 0 -> J
            
            for (int j = 1; j < n; ++j) {
                // Since sorted by Support Descending, if J is weak, J+1 is definitely weak.
                if (currentLevel[j].support < min_count) break;

                for (int i = 0; i < j; ++i) {
                    // Since sorted by Support Descending, if i is weak, i+1 is definitely weak.
                    if (currentLevel[i].support < min_count) break;

                    // Prefix Check (O(Level))
                    bool match = true;
                    for (int k = 0; k < level - 1; ++k) {
                        if (currentLevel[i].itemset[k] != currentLevel[j].itemset[k]) {
                            match = false; 
                            break;
                        }
                    }

                    // [CRITICAL BUG FIX]:
                    // Because we sort by SUPPORT, items with same prefix are NOT neighbors.
                    // If prefix doesn't match, we simply continue searching.
                    if (!match) continue; 

                    // If we are here, Prefix Matches AND Support is high enough.
                    DynamicBitSet newBits;
                    int newSup = 0;

                    //if (tidSet || level == 1) { // Removed 'if' to simplify logic as per your preference, add back if needed
                        newBits = DynamicBitSet::intersect(currentLevel[i].bits, currentLevel[j].bits);
                        newSup = newBits.count();
                    //} 

                    if (newSup >= min_count) {
                        min_count = heap.insert(newSup);

                        std::vector<int> newKey = currentLevel[i].itemset;
                        newKey.push_back(currentLevel[j].itemset.back());

                        finalTopK.push_back({newKey, newSup});
                        nextLevel.push_back({std::move(newKey), std::move(newBits), newSup});
                    }
                }
            }
            
            currentLevel = std::move(nextLevel);
            
            // [VITAL]: Sort strictly by Support Descending for the next SIME pass
            std::sort(currentLevel.begin(), currentLevel.end()); 

            level++;
            // std::cout << "Level " << level << " Candidates: " << currentLevel.size() << " | MinSup: " << min_count << "\n";
        }

        cleanupResults();
        auto end = std::chrono::high_resolution_clock::now();

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

        while (std::getline(file, line)) {
            if (line.empty()) continue;
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
                if (vR[id].empty() || vR[id].back() != transIndex) {
                	vR[id].push_back(transIndex);
                }
            }
            transIndex++;
        }
        this->num_of_transactions = transIndex;
        this->num_of_items = itemIndex;

        std::vector<ItemStat> stats;
        for (auto& [id, tids] : vR) stats.push_back({(int)tids.size(), id});
        
        std::sort(stats.begin(), stats.end(), [](const ItemStat& a, const ItemStat& b) {
            return a.first > b.first; 
        });

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
        
        // Ensure Level 1 is sorted by support
        std::sort(l1.begin(), l1.end());
        return l1;
    }

    void cleanupResults() {
        finalTopK.erase(std::remove_if(finalTopK.begin(), finalTopK.end(),
            [this](const TopKFIM& f) { return f.support < min_count; }), finalTopK.end());
    }
};

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