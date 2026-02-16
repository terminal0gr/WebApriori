#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
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
// 4. HTK-MINER MAIN CLASS
// ==========================================
class HTKMiner {
    ResultManager results;
    std::unordered_map<std::string, int> itemToId;
    std::unordered_map<int, std::string> idToItem;
    int num_of_transactions = 0; 
    int itemCount = 0;
    bool tidSet; // true = intersection, false = diffset
    std::string delimiter;

public:
    HTKMiner(int k, std::string delim = " ", bool mode = true) 
        : results(k), delimiter(delim), tidSet(mode) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // Level 1
        std::vector<Candidate> currentLevel = loadAndBuildLevel1(filepath);
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
    std::vector<Candidate> loadAndBuildLevel1(const std::string& path) {
        std::ifstream file(path);
        std::string line;
        std::unordered_map<int, std::vector<int>> verticalData;
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
                    if (verticalData[id].empty() || verticalData[id].back() != transIndex) {
                        verticalData[id].push_back(transIndex);
                    }
                        
                }
            }
            transIndex++;
        }
        num_of_transactions = transIndex;
        itemCount = itemIndex;

        std::vector<Candidate> l1;
        for (auto& [id, tids] : verticalData) {
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