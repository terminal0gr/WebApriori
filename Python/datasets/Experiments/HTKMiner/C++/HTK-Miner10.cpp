#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
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
    return (size_t)(usage.ru_maxrss * 1024); 
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

// Corresponds to entries in 'nextLevelData' (Candidates with Bitsets)
struct Candidate {
    std::vector<int> itemset; 
    DynamicBitSet bits;
    int support;

    // [PURE SUPPORT SORT]
    // Ensures SIME processes high-support items first.
    bool operator<(const Candidate& other) const {
        if (support != other.support) {
            return support > other.support; // Descending Support
        }
        return itemset < other.itemset; // Tie-breaker
    }
};

// ==========================================
// 2. HTK-MINER CLASS
// ==========================================

class HTKMiner {
private:
    std::unordered_map<std::string, int> itemToId; 
    std::unordered_map<int, std::string> idToItem; 
    std::vector<int> rankToRaw;                    
    
    // Global State
    std::vector<TopKFIM> topKFI; // The global Top-K results (matches Python 'topKFI')
    int min_count = 0;           // The dynamic threshold
    int topK;
    int num_of_transactions = 0;
    int num_of_items = 0;
    bool tidSet; 

    using ItemStat = std::pair<int, int>; 

public:
    HTKMiner(int k, bool mode = true) : topK(k), tidSet(mode) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // 1. Level 1 Generation (Read & Rank)
        // 'currentLevel' acts as the parent list for generation
        std::vector<Candidate> currentLevel = readAndRank(filepath);
        
        // Initial populate of topKFI with Level 1 results
        for(const auto& cand : currentLevel) {
            topKFI.push_back({cand.itemset, cand.support});
        }
        // Initial Pruning/Threshold update
        performGetTopKFI(currentLevel); // Update min_count and prune currentLevel

        std::cout << "Level 1 Frequent Items: " << currentLevel.size() << "\n";
        std::cout << "Initial MinSup: " << min_count << "\n";

        // 2. Main Mining Loop
        int level = 1;
        while (!currentLevel.empty()) {
            
            // 'nextLevelData' corresponds to Python's nextLevelData + nextLevelTopK
            std::vector<Candidate> nextLevelData; 
            int n = currentLevel.size();
            nextLevelData.reserve(n); 

            // ==========================================
            // SIME LOGIC (Pure Support Sort)
            // ==========================================
            for (int j = 1; j < n; ++j) {
                // [PRUNING A]: Outer Loop Break
                // Valid because list is sorted by Support Descending.
                if (currentLevel[j].support < min_count) break;

                for (int i = 0; i < j; ++i) {
                    // [PRUNING B]: Inner Loop Skip
                    if (currentLevel[i].support < min_count) continue;

                    // Prefix Check
                    bool match = true;
                    for (int k = 0; k < level - 1; ++k) {
                        if (currentLevel[i].itemset[k] != currentLevel[j].itemset[k]) {
                            match = false; 
                            break;
                        }
                    }

                    // [CORRECTION for BUG in 07]: 
                    // Due to Support Sorting, non-matching prefixes are scattered.
                    // We must CONTINUE, not BREAK.
                    if (!match) continue; 

                    // Bitset Intersection / Diff
                    DynamicBitSet newBits;
                    int newSup = 0;

                    // if (tidSet || level == 1) { // Implicit intersection for simpler logic
                        newBits = DynamicBitSet::intersect(currentLevel[i].bits, currentLevel[j].bits);
                        newSup = newBits.count();
                    // }

                    // Local Threshold Check
                    // We add to nextLevelData if it meets the *current* min_count.
                    // Stricter pruning happens in performGetTopKFI() at end of level.
                    if (newSup >= min_count) {
                        std::vector<int> newKey = currentLevel[i].itemset;
                        newKey.push_back(currentLevel[j].itemset.back());

                        nextLevelData.push_back({std::move(newKey), std::move(newBits), newSup});
                    }
                }
            }

            // ==========================================
            // PYTHON LOGIC INTEGRATION: getTopKFI()
            // ==========================================
            // 1. Merge nextLevelTopK into topKFI
            for (const auto& cand : nextLevelData) {
                topKFI.push_back({cand.itemset, cand.support});
            }

            // 2. Execute the Global Pruning & Update MinSup
            // This filters 'topKFI' AND prunes 'nextLevelData' (the parents)
            performGetTopKFI(nextLevelData);

            // 3. Move to next level
            currentLevel = std::move(nextLevelData);
            
            // 4. Sort by Support for next SIME pass
            std::sort(currentLevel.begin(), currentLevel.end());

            level++;
            // std::cout << "Level " << level << " Candidates: " << currentLevel.size() << " | MinSup: " << min_count << "\n";
        }

        auto end = std::chrono::high_resolution_clock::now();
        double elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() / 1000.0;
        
        std::cout << "Total Execution Time: " << elapsed << " s\n";
        std::cout << "FIM found: " << topKFI.size() << "\n";
        std::cout << "Absolute minSup: " << min_count << "\n";
    }

    void saveResults(const std::string& path) {
        std::ofstream out(path);
        // topKFI is already sorted and pruned by performGetTopKFI
        for (const auto& res : topKFI) {
            for (size_t i = 0; i < res.items.size(); ++i) {
                out << idToItem[rankToRaw[res.items[i]]] << (i == res.items.size()-1 ? "" : " ");
            }
            out << " #SUP: " << res.support << "\n";
        }
    }

private:
    // Matches Python: self.getTopKFI(topKFI, level+1)
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

        // Determine Initial min_count (Pre-Mine)
        if (stats.size() >= (size_t)topK) {
             // Simple K-th estimate for initial pruning
             int kSup = stats[topK - 1].first;
             // Don't set this->min_count too high yet, let performGetTopKFI handle it
             // But we can prune L1 candidates to save memory
             this->min_count = kSup; 
             // Note: performGetTopKFI will correct this precisely later
        }

        std::vector<Candidate> l1;
        for (size_t rank = 0; rank < stats.size(); ++rank) {
            // Early prune of raw items
            if (stats[rank].first < min_count && stats.size() >= (size_t)topK) break; 
            
            int rawID = stats[rank].second;
            int sup = stats[rank].first;

            rankToRaw.push_back(rawID);

            DynamicBitSet bs;
            bs.resize(num_of_transactions);
            for (int t : vR[rawID]) bs.set(t);

            l1.push_back({{(int)rank}, std::move(bs), sup});
        }
        
        // Ensure L1 is sorted by Support Descending
        std::sort(l1.begin(), l1.end());
        return l1;
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