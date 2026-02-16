#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <unordered_map>
#include <map>
#include <queue>
#include <chrono>
#include <cmath>
#include <bit> // C++20 for popcount
#include <omp.h> // For parallel execution (optional, can be removed if strictly single core)

// ==========================================
// 1. HIGH-PERFORMANCE BITSET STRUCTURE
// ==========================================
// Replaces Python's large integers for transaction tracking.
// Uses vector<uint64_t> to perform 64 operations per cycle.
struct DynamicBitSet {
    std::vector<uint64_t> data;
    size_t num_bits;

    DynamicBitSet() : num_bits(0) {}
    
    // Initialize with specific bit count (transaction count)
    void resize(size_t n_bits) {
        num_bits = n_bits;
        data.resize((n_bits + 63) / 64, 0);
    }

    // Set a specific bit (Transaction ID) to 1
    void set(size_t index) {
        data[index / 64] |= (1ULL << (index % 64));
    }

    // Population count (Support counting)
    // Uses C++20 std::popcount or compiler intrinsic
    size_t count() const {
        size_t c = 0;
        for (uint64_t val : data) {
            #if defined(__cpp_lib_bitops)
                c += std::popcount(val);
            #elif defined(__GNUC__) || defined(__clang__)
                c += __builtin_popcountll(val);
            #else
                // Fallback for older compilers
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

    // Difference: B & (~A)  (Items in B that are NOT in A)
    // Python Logic: data[classB] & (data[classB] ^ data[classA])
    static DynamicBitSet diff(const DynamicBitSet& a, const DynamicBitSet& b) {
        DynamicBitSet res;
        res.num_bits = a.num_bits;
        res.data.resize(a.data.size());
        for (size_t i = 0; i < a.data.size(); ++i) {
            // "b" is the superset candidate (classB), "a" is classA
            // In python code: transactions = self.data[classB] & (self.data[classB] ^ self.data[classA])
            // This is mathematically equivalent to: B & ~A
            res.data[i] = b.data[i] & (~a.data[i]);
        }
        return res;
    }
};

// ==========================================
// 2. CANDIDATE STRUCTURE
// ==========================================
// Holds the Itemset key, its support, and its vertical data (BitSet)
struct Candidate {
    std::vector<int> itemset; // The key (e.g., [1, 5, 9])
    DynamicBitSet bits;       // Vertical representation
    int support;              // Cached support value

    // For sorting candidates by Support Descending (primary) then Itemset (secondary)
    bool operator>(const Candidate& other) const {
        if (support != other.support)
            return support > other.support;
        return itemset > other.itemset;
    }
};

// ==========================================
// 3. TOP-K PRIORITY QUEUE
// ==========================================
// Replaces 'QuickHeap'. Uses a Min-Heap to track the K-th largest support.
class TopKBuffer {
    // Min-heap stores supports. The top() is the smallest support in the Top-K.
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
    size_t k;

public:
    TopKBuffer(size_t top_k) : k(top_k) {}

    // Returns the current minimum support required to enter the Top-K
    int get_min_support() const {
        if (min_heap.size() < k) return 0;
        return min_heap.top();
    }

    // Tries to insert a support value. Returns the new min_threshold.
    int insert(int support) {
        if (min_heap.size() < k) {
            min_heap.push(support);
            return (min_heap.size() == k) ? min_heap.top() : 0;
        }
        
        if (support > min_heap.top()) {
            min_heap.pop();
            min_heap.push(support);
        }
        
        return min_heap.top();
    }
    
    size_t size() const { return min_heap.size(); }
};

// ==========================================
// 4. MAIN MINER CLASS
// ==========================================
class HTKMinerCPP {
    int topK;
    bool bitSetMode; 
    bool tidSet; // True = Intersection, False = DiffSet
    std::string delimiter;
    
    // Internal State
    std::unordered_map<std::string, int> itemToId;
    std::unordered_map<int, std::string> idToItem;
    int num_transactions = 0;
    int num_items = 0;
    
    // The "Heap" logic
    TopKBuffer topKBuffer;
    int globalMinSup = 0;

    // Final Results
    std::vector<Candidate> finalTopK;

public:
    HTKMinerCPP(int k, std::string delim = " ", bool useBitSet = true, bool intersectMode = true)
        : topK(k), delimiter(delim), bitSetMode(useBitSet), tidSet(intersectMode), topKBuffer(k) {}

    void mine(const std::string& filepath) {
        auto start = std::chrono::high_resolution_clock::now();

        // 1. Read Dataset
        std::vector<Candidate> currentLevel = readDataset(filepath);
        
        auto readEnd = std::chrono::high_resolution_clock::now();
        std::cout << "Read Time: " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(readEnd - start).count() / 1000.0 
                  << " s\n";

        // 2. Mine Levels
        if (bitSetMode) {
             // Dispatch to appropriate logic
             if (tidSet) mineLevelBitSet(currentLevel, true); // Intersection
             else        mineLevelBitSet(currentLevel, false); // DiffSet
        } else {
             std::cout << "TID-list (vector<int>) mode not implemented in this snippet (BitSet is superior).\n";
        }

        auto end = std::chrono::high_resolution_clock::now();
        std::cout << "Total Execution Time: " 
                  << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() / 1000.0 
                  << " s\n";
        
        std::cout << "FIM found: " << finalTopK.size() << "\n";
        std::cout << "Absolute minSup: " << globalMinSup << "\n";
    }

    void writeResults(const std::string& filename) {
        std::ofstream out(filename);
        out << "{\n";
        for (size_t i = 0; i < finalTopK.size(); ++i) {
            out << "  \"";
            const auto& itemset = finalTopK[i].itemset;
            for (size_t j = 0; j < itemset.size(); ++j) {
                out << idToItem[itemset[j]] << (j == itemset.size() - 1 ? "" : ", ");
            }
            out << "\": " << finalTopK[i].support;
            if (i != finalTopK.size() - 1) out << ",";
            out << "\n";
        }
        out << "}\n";
    }

private:
    std::vector<Candidate> readDataset(const std::string& filepath) {
        std::ifstream file(filepath);
        std::string line;
        
        // Temp storage for vertical conversion
        std::unordered_map<int, std::vector<int>> tempVertical;
        
        int transIdx = 0;
        int nextItemId = 1;

        while (std::getline(file, line)) {
            // Trim (basic)
            if (!line.empty() && line.back() == '\r') line.pop_back();
            if (line.empty()) continue;

            // Split
            size_t pos = 0;
            std::string token;
            // Simple split logic
            while ((pos = line.find(delimiter)) != std::string::npos) {
                token = line.substr(0, pos);
                processItem(token, transIdx, nextItemId, tempVertical);
                line.erase(0, pos + delimiter.length());
            }
            processItem(line, transIdx, nextItemId, tempVertical); // Last item
            transIdx++;
        }
        num_transactions = transIdx;
        num_items = nextItemId - 1;

        // Convert to BitSets and Candidates (Level 1)
        std::vector<Candidate> candidates;
        candidates.reserve(tempVertical.size());

        // Fill BitSets (Can be parallelized with OpenMP)
        // #pragma omp parallel for 
        for (auto const& [id, tids] : tempVertical) {
            DynamicBitSet bs;
            bs.resize(num_transactions);
            for (int t : tids) bs.set(t);
            
            int sup = tids.size();
            candidates.push_back({ {id}, bs, sup });
        }

        // Initial Top-K Pruning for Level 1
        return getTopK(candidates, 1);
    }

    void processItem(const std::string& item, int transIdx, int& nextId, std::unordered_map<int, std::vector<int>>& acc) {
        if (item.empty()) return;
        if (itemToId.find(item) == itemToId.end()) {
            itemToId[item] = nextId;
            idToItem[nextId] = item;
            nextId++;
        }
        int id = itemToId[item];
        // Ensure uniqueness per transaction handled by bitset logic later, 
        // but explicit check helps if input has duplicates in one line
        if (acc[id].empty() || acc[id].back() != transIdx) {
            acc[id].push_back(transIdx);
        }
    }

    // Core Logic: Replaces mineNextLevelIntersectionBitSet and DiffSet
    void mineLevelBitSet(std::vector<Candidate>& currentLevel, bool intersectionMode) {
        int level = 1;

        while (!currentLevel.empty()) {
            std::vector<Candidate> nextLevel;
            // Reserve memory to prevent reallocations
            // Heuristic: next level rarely exceeds current level squared, usually much smaller
            // nextLevel.reserve(currentLevel.size()); 

            int n = currentLevel.size();
            
            // Double loop (iA, iB)
            // Uses indices instead of iterators for cache friendliness
            for (int iB = 1; iB < n; ++iB) {
                if (currentLevel[iB].support < globalMinSup) continue; // Prune

                for (int iA = 0; iA < iB; ++iA) {
                    if (currentLevel[iA].support < globalMinSup) continue; // Prune

                    // Prefix Check: Check if first (K-1) items match
                    // Since items are integers, we can check quickly.
                    // Optimisation: We only need to check the range [0, level-1)
                    bool prefixMatch = true;
                    for (int k = 0; k < level - 1; ++k) {
                        if (currentLevel[iA].itemset[k] != currentLevel[iB].itemset[k]) {
                            prefixMatch = false;
                            break;
                        }
                    }

                    if (prefixMatch) {
                        DynamicBitSet newBits;
                        int newSupport = 0;

                        if (level == 1 && !intersectionMode) {
                             // Special case: Level 1 DiffSet is weird because previous level didn't have diffsets.
                             // Usually Level 1 -> Level 2 is always Intersection, then switch to Diffset.
                             // But following Python code logic: 
                             // Level 1 logic in DiffSet mode: transactions = A & (A ^ B)
                             newBits = DynamicBitSet::diff(currentLevel[iA].bits, currentLevel[iB].bits); // B & ~A
                             // Wait, Python L1 Diffset: transactions = set(A) - set(B) => A & ~B
                             // The Python code is slightly confusing in L1 diffset. 
                             // Standard Diffset starts at L2. Let's assume Intersection for L1->L2 always or strict translation.
                             // Strict Translation of Python:
                             // if level==1: transactions = data[A] & (data[A] ^ data[B]) -> A & ~B
                             // else: transactions = data[B] & (data[B] ^ data[A]) -> B & ~A
                             newBits = DynamicBitSet::diff(currentLevel[iB].bits, currentLevel[iA].bits); // A & ~B
                             newSupport = currentLevel[iA].support - newBits.count();
                        }
                        else if (intersectionMode) {
                            newBits = DynamicBitSet::intersect(currentLevel[iA].bits, currentLevel[iB].bits);
                            newSupport = newBits.count();
                        } else {
                            // DiffSet Mode (Level > 1)
                            // Support = Support(A) - |Diff(B, A)|
                            newBits = DynamicBitSet::diff(currentLevel[iA].bits, currentLevel[iB].bits);
                            newSupport = currentLevel[iA].support - newBits.count();
                        }

                        if (newSupport >= globalMinSup) {
                            // Update Global MinSup via Heap
                            globalMinSup = topKBuffer.insert(newSupport);

                            // Create New Key: Prefix + A.last + B.last
                            std::vector<int> newKey = currentLevel[iA].itemset;
                            newKey.push_back(currentLevel[iB].itemset.back());

                            Candidate cand;
                            cand.itemset = newKey;
                            cand.bits = std::move(newBits);
                            cand.support = newSupport;
                            
                            nextLevel.push_back(std::move(cand));
                        }
                    }
                }
            }

            // Prepare for next iteration
            currentLevel = getTopK(nextLevel, level + 1);
            level++;
            
            // Safety break or timeout check could go here
            if (currentLevel.empty()) break;
        }
    }

    // Filters and Sorts Candidates based on TopK
    std::vector<Candidate> getTopK(std::vector<Candidate>& rawCandidates, int level) {
        // Sort by Support Descending, then by Itemset (Keys)
        std::sort(rawCandidates.begin(), rawCandidates.end(), std::greater<Candidate>());

        // Collect valid candidates for next level
        std::vector<Candidate> nextGen;
        // nextGen.reserve(rawCandidates.size()); // Optional optimization

        // logic: iterate, add to final results, keep going until topK condition met
        // The python logic is complex here: it adds ALL candidates to final results, 
        // but only returns the top K candidates to the NEXT recursion level.

        int count = 0;
        int thresholdSupport = -1;

        for (auto& cand : rawCandidates) {
            // Logic to determine cut-off for NEXT level
            bool includeInNextLevel = false;

            if (count < topK) {
                includeInNextLevel = true;
                if (count == topK - 1) thresholdSupport = cand.support;
            } else {
                // Handle ties
                if (cand.support == thresholdSupport && thresholdSupport != -1) {
                    includeInNextLevel = true;
                }
            }

            // Always add to final results if valid
            // Note: In Python code, finalTopK accumulates everything valid.
            finalTopK.push_back(cand); // Copy to results (expensive, but necessary to keep data)
            
            if (includeInNextLevel) {
                // In C++, we can move the bits to the next level since we don't need them in 'finalTopK' 
                // (finalTopK only needs support and name, typically, but we stored the bits).
                // To save RAM, we should COPY for finalTopK and MOVE for nextGen.
                // However, 'finalTopK' in Python stores the simple support value.
                // Let's rely on the struct copy. 
                // Optimization: Don't store 'bits' in finalTopK if not needed. 
                // (requires separate struct or clearing bits).
                
                nextGen.push_back(cand); // Copy
                count++;
            }
        }
        
        // Clear bits from the "finalTopK" version of these candidates to save RAM?
        // Left as todo.

        // Update global minSup if we ran out of candidates
        if (count < topK) globalMinSup = 0;
        else globalMinSup = thresholdSupport;
        
        // Sync heap (Optional, but good for consistency)
        // In C++, the heap is self-managing.

        return nextGen;
    }
};

int main(int argc, char* argv[]) {
    // Example usage
    if (argc < 2) {
        std::cout << "Usage: ./htkminer <dataset_path> [topK] [bitset_mode 1/0]\n";
        return 1;
    }

    std::string path = argv[1];
    int k = (argc > 2) ? std::stoi(argv[2]) : 10;
    bool bitset = (argc > 3) ? (std::stoi(argv[3]) != 0) : true;

    HTKMinerCPP miner(k, " ", bitset, true); // defaulting to intersection
    miner.mine(path);
    miner.writeResults("output.json");

    return 0;
}