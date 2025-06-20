 package ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth;
 
 /* This file is copyright (c) 2008-2015 Philippe Fournier-Viger
 * 
 * This file is part of the SPMF DATA MINING SOFTWARE
 * (http://www.philippe-fournier-viger.com/spmf).
 * 
 * SPMF is free software: you can redistribute it and/or modify it under the
 * terms of the GNU General Public License as published by the Free Software
 * Foundation, either version 3 of the License, or (at your option) any later
 * version.
 * 
 * SPMF is distributed in the hope that it will be useful, but WITHOUT ANY
 * WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
 * A PARTICULAR PURPOSE. See the GNU General Public License for more details.
 * You should have received a copy of the GNU General Public License along with
 * SPMF. If not, see <http://www.gnu.org/licenses/>.
 */


import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.PriorityQueue;

import org.json.JSONObject;

import java.util.Map.Entry;

import ca.pfv.spmf.patterns.itemset_array_integers_with_count.Itemset;
import ca.pfv.spmf.patterns.itemset_array_integers_with_count.Itemsets;
import ca.pfv.spmf.tools.MemoryLogger;

/** 
 * This is an implementation of the FPGROWTH algorithm (Han et al., 2004) that is modified to find the top-k  most frequent itemsets.
 * The original FPGrowth is described in this paper:
 * <br/><br/>
 * 
 * Han, J., Pei, J., & Yin, Y. (2000, May). Mining frequent patterns without candidate generation. In ACM SIGMOD Record (Vol. 29, No. 2, pp. 1-12). ACM
 * <br/><br/>
 * 
 * This is an optimized version that saves the result to a file
 * or keep it into memory if no output path is provided
 * by the user to the runAlgorithm method().
 *
 * @see FPTree
 * @see Itemset
 * @see Itemsets
 * @author Philippe Fournier-Viger
 */
public class AlgoFPGrowthTOPK {

	// for statistics
	private long startTimestamp; // start time of the latest execution
	private long endTime; // end time of the latest execution
	private int transactionCount = 0; // transaction count in the database
	
	// parameter
	public int minSupportRelative;// the relative minimum support
	
	BufferedWriter writer = null; // object to write the output file
	
	// The  patterns that are found 
	// (if the user wants to keep them into memory)
	protected Itemsets patterns = null;
		
	// This variable is used to determine the size of buffers to store itemsets.
	// A value of 50 is enough because it allows up to 2^50 patterns!
	final int BUFFERS_SIZE = 2000;
	
	// buffer for storing the current itemset that is mined when performing mining
	// the idea is to always reuse the same buffer to reduce memory usage.
	private int[] itemsetBuffer = null;
	// another buffer for storing fpnodes in a single path of the tree
	private FPNode[] fpNodeTempBuffer = null;
	
	/** maximum pattern length */
	private int maxPatternLength = 1000;
	
	/** minimum pattern length */
	private int minPatternLength = 0;
	
	// ======================================
	/** the number of patterns to find "k" */
	protected int n;

	/** priority queue to store the top-n patterns */
	PriorityQueue<Itemset> nItemsets;
	// ======================================

	/**
	 * Constructor
	 */
	public AlgoFPGrowthTOPK() {
		
	}

	/**
	 * Method to run the FPGRowth algorithm.
	 * @param input the path to an input file containing a transaction database.
	 * @param output the output file path for saving the result (if null, the result 
	 *        will be returned by the method instead of being saved).
	 * @param k the number of patterns to find.
	 * @return the top k itemsets
	 * @throws IOException exception if error reading or writing files
	 */
	public PriorityQueue<Itemset> runAlgorithm(String input, String output, int kValue) throws FileNotFoundException, IOException {
		return runAlgorithm(input, output, kValue, " ");
	}
	public PriorityQueue<Itemset> runAlgorithm(String input, String output, int kValue, String separator) throws FileNotFoundException, IOException {
		// record start time
		startTimestamp = System.currentTimeMillis();
		
		//initialize tool to record memory usage
		MemoryLogger.getInstance().reset();
		MemoryLogger.getInstance().checkMemory();
		
		// if the user want to keep the result into memory
		if(output == null){
			writer = null;
			patterns =  new Itemsets("FREQUENT ITEMSETS");
	    }else{ // if the user want to save the result to a file
			patterns = null;
			writer = new BufferedWriter(new FileWriter(output)); 
		}
		
		// ======================================
		this.n = kValue;

		// Initialize the priority queue to store the top K patterns
		nItemsets = new PriorityQueue<>(Comparator.comparingInt(Itemset::getAbsoluteSupport));

		// Set the internal minsup value to 1
		minSupportRelative = 1;
		// ======================================
		
		// (1) PREPROCESSING: Initial database scan to determine the frequency of each item
		// The frequency is stored in a map:
		//    key: item   value: support
		final Map<Integer, Integer> mapSupport = scanDatabaseToDetermineFrequencyOfSingleItems(input); 
		// check the memory usage
		MemoryLogger.getInstance().checkMemory();
		
		
		// We add all frequent items to the set of candidate of size 1
		// ====================================== OPTIMIZATION ===========
		// Find the highest support among the single items
		if(minPatternLength <=1) {
			int itemCount = mapSupport.size();
			if (itemCount >= n) {
				int itemSupports[] = new int[mapSupport.size()];
				int index = 0;
				for (Entry<Integer, Integer> entry : mapSupport.entrySet()) {
					itemSupports[index++] = entry.getValue();
				}
				Arrays.sort(itemSupports);
//				System.out.println(Arrays.toString(itemSupports));
				minSupportRelative = itemSupports[itemSupports.length - n];
//				System.out.println(minSupportRelative);
			}
		}
		// check the memory usage
		MemoryLogger.getInstance().checkMemory();
		// ==============================================================
		
		// (2) Scan the database again to build the initial FP-Tree
		// Before inserting a transaction in the FPTree, we sort the items
		// by descending order of support.  We ignore items that
		// do not have the minimum support.
		FPTree tree = new FPTree();
		
		// read the file
		BufferedReader reader = new BufferedReader(new FileReader(input));
		String line;
		// for each line (transaction) until the end of the file
		while( ((line = reader.readLine())!= null)){ 
			// if the line is  a comment, is  empty or is a
			// kind of metadata
			if (line.isEmpty() == true ||	line.charAt(0) == '#' || line.charAt(0) == '%'
				|| line.charAt(0) == '@') {
				continue;
			}
			
			String[] lineSplited = line.split(" ");
//			Set<Integer> alreadySeen = new HashSet<Integer>();
			List<Integer> transaction = new ArrayList<Integer>();
			
			// for each item in the transaction
			for(String itemString : lineSplited){  
				Integer item = Integer.parseInt(itemString);
				// only add items that have the minimum support
				if(mapSupport.get(item) >= minSupportRelative){
					transaction.add(item);	
				}
			}
			// sort item in the transaction by descending order of support
			Collections.sort(transaction, new Comparator<Integer>(){
				public int compare(Integer item1, Integer item2){
					// compare the frequency
					int compare = mapSupport.get(item2) - mapSupport.get(item1);
					// if the same frequency, we check the lexical ordering!
					if(compare == 0){ 
						return (item1 - item2);
					}
					// otherwise, just use the frequency
					return compare;
				}
			});
			// add the sorted transaction to the fptree.
			tree.addTransaction(transaction);
		}
		// check the memory usage
		MemoryLogger.getInstance().checkMemory();
		// close the input file
		reader.close();
		
		// We create the header table for the tree using the calculated support of single items
		tree.createHeaderList(mapSupport);
		MemoryLogger.getInstance().checkMemory();
		// close the input file

		// (5) We start to mine the FP-Tree by calling the recursive method.
		// Initially, the prefix alpha is empty.
		// if at least an item is frequent
		if(tree.headerList.size() > 0) {
			// initialize the buffer for storing the current itemset
			itemsetBuffer = new int[BUFFERS_SIZE];
			// and another buffer
			fpNodeTempBuffer = new FPNode[BUFFERS_SIZE];
			// recursively generate frequent itemsets using the fp-tree
			// Note: we assume that the initial FP-Tree has more than one path
			// which should generally be the case.
			// ======================================
			Iterator<Itemset> iter = nItemsets.iterator();
			while (iter.hasNext()) {
				saveItemsetToFile(iter.next());
			}
			// ======================================
			fpgrowth(tree, itemsetBuffer, 0, transactionCount, mapSupport);
		}
		MemoryLogger.getInstance().checkMemory();
		// close the input file

		
		// close the output file if the result was saved to a file
		if(writer != null){
			// ======================================
			Iterator<Itemset> iter = nItemsets.iterator();
			while (iter.hasNext()) {
				saveItemsetToFile(iter.next());
			}
			// ======================================
			writer.close();
		}
		// record the execution end time
		endTime= System.currentTimeMillis();
		
		// check the memory usage
		MemoryLogger.getInstance().checkMemory();
		
		// return the result (if saved to memory)
		return nItemsets;
	}


	


	/**
	 * Mine an FP-Tree having more than one path.
	 * @param tree  the FP-tree
	 * @param prefix  the current prefix, named "alpha"
	 * @param mapSupport the frequency of items in the FP-Tree
	 * @throws IOException  exception if error writing the output file
	 */
	private void fpgrowth(FPTree tree, int [] prefix, int prefixLength, int prefixSupport, Map<Integer, Integer> mapSupport) throws IOException {
		
		if(prefixLength == maxPatternLength){
			return;
		}
		
		
		////		======= DEBUG ========
//		System.out.print("###### Prefix: ");
//		for(int k=0; k< prefixLength; k++) {
//			System.out.print(prefix[k] + "  ");
//		}
//		System.out.println("\n");
////				========== END DEBUG =======
//		System.out.println(tree);
		
		// We will check if the FPtree contains a single path
		boolean singlePath = true;
		// This variable is used to count the number of items in the single path
		// if there is one
		int position = 0;
		// if the root has more than one child, than it is not a single path
		if(tree.root.childs.size() > 1) {
			singlePath = false;
		}else {
			
			// Otherwise,
			// if the root has exactly one child, we need to recursively check childs
			// of the child to see if they also have one child
			FPNode currentNode = tree.root.childs.get(0);
			while(true){
				// if the current child has more than one child, it is not a single path!
				if(currentNode.childs.size() > 1) {
					singlePath = false;
					break;
				}
				// otherwise, we copy the current item in the buffer and move to the child
				// the buffer will be used to store all items in the path
				fpNodeTempBuffer[position] = currentNode;
				
				position++;
				// if this node has no child, that means that this is the end of this path
				// and it is a single path, so we break
				if(currentNode.childs.size() == 0) {
					break;
				}
				currentNode = currentNode.childs.get(0);
			}
		}
		
		// Case 1: the FPtree contains a single path
		if(singlePath){	
			// We save the path, because it is a maximal itemset
			saveAllCombinationsOfPrefixPath(fpNodeTempBuffer, position, prefix, prefixLength);
		}else {
			// For each frequent item in the header table list of the tree in reverse order.
			for(int i = tree.headerList.size()-1; i>=0; i--){
				// get the item
				Integer item = tree.headerList.get(i);
				
				// get the item support
				int support = mapSupport.get(item);
	
				// Create Beta by concatening prefix Alpha by adding the current item to alpha
				prefix[prefixLength] = item;
				
				// calculate the support of the new prefix beta
				int betaSupport = (prefixSupport < support) ? prefixSupport: support;
				
				// save beta to the output file
				saveItemset(prefix, prefixLength+1, betaSupport);
				
				if(prefixLength+1 < maxPatternLength){
				
					// === (A) Construct beta's conditional pattern base ===
					// It is a subdatabase which consists of the set of prefix paths
					// in the FP-tree co-occuring with the prefix pattern.
					List<List<FPNode>> prefixPaths = new ArrayList<List<FPNode>>();
					FPNode path = tree.mapItemNodes.get(item);
					
					// Map to count the support of items in the conditional prefix tree
					// Key: item   Value: support
					Map<Integer, Integer> mapSupportBeta = new HashMap<Integer, Integer>();
					
					while(path != null){
						// if the path is not just the root node
						if(path.parent.itemID != -1){
							// create the prefixpath
							List<FPNode> prefixPath = new ArrayList<FPNode>();
							// add this node.
							prefixPath.add(path);   // NOTE: we add it just to keep its support,
							// actually it should not be part of the prefixPath
							
							// ####
							int pathCount = path.counter;
							
							//Recursively add all the parents of this node.
							FPNode parent = path.parent;
							while(parent.itemID != -1){
								prefixPath.add(parent);
								
								// FOR EACH PATTERN WE ALSO UPDATE THE ITEM SUPPORT AT THE SAME TIME
								// if the first time we see that node id
								if(mapSupportBeta.get(parent.itemID) == null){
									// just add the path count
									mapSupportBeta.put(parent.itemID, pathCount);
								}else{
									// otherwise, make the sum with the value already stored
									mapSupportBeta.put(parent.itemID, mapSupportBeta.get(parent.itemID) + pathCount);
								}
								parent = parent.parent;
							}
							// add the path to the list of prefixpaths
							prefixPaths.add(prefixPath);
						}
						// We will look for the next prefixpath
						path = path.nodeLink;
					}
	
					// (B) Construct beta's conditional FP-Tree
					// Create the tree.
					FPTree treeBeta = new FPTree();
					// Add each prefixpath in the FP-tree.
					for(List<FPNode> prefixPath : prefixPaths){
						treeBeta.addPrefixPath(prefixPath, mapSupportBeta, minSupportRelative); 
					}  
					
					// Mine recursively the Beta tree if the root has child(s)
					if(treeBeta.root.childs.size() > 0){
	
						// Create the header list.
						treeBeta.createHeaderList(mapSupportBeta); 
						// recursive call
						fpgrowth(treeBeta, prefix, prefixLength+1, betaSupport, mapSupportBeta);
					}
				}
			}
		}
		
	}


	/**
	 * This method saves all combinations of a prefix path if it has enough support
	 * @param prefix the current prefix
	 * @param prefixLength the current prefix length
	 * @param prefixPath the prefix path
	 * @throws IOException if exception while writting to output file
	 */
	private void saveAllCombinationsOfPrefixPath(FPNode[] fpNodeTempBuffer, int position, 
			int[] prefix, int prefixLength) throws IOException {

		int support = 0;
		// Generate all subsets of the prefixPath except the empty set
		// and output them
		// We use bits to generate all subsets.
loop1:	for (long i = 1, max = 1 << position; i < max; i++) {
			
			// we create a new subset
			int newPrefixLength = prefixLength;
			
			// for each bit
			for (int j = 0; j < position; j++) {
				// check if the j bit is set to 1
				int isSet = (int) i & (1 << j);
				// if yes, add the bit position as an item to the new subset
				if (isSet > 0) {
					if(newPrefixLength == maxPatternLength){
						continue loop1;
					}
					
					prefix[newPrefixLength++] = fpNodeTempBuffer[j].itemID;
					// 2018-03-18: REMOVED THE FOLLOWING "IF" to fix
					// support counting error.
//					if(support == 0) {
						support = fpNodeTempBuffer[j].counter;
//					}
				}
			}
			// save the itemset
			saveItemset(prefix, newPrefixLength, support);
		}
	}
	

	/**
	 * This method scans the input database to calculate the support of single items
	 * @param input the path of the input file
	 * @throws IOException  exception if error while writing the file
	 * @return a map for storing the support of each item (key: item, value: support)
	 */
	private  Map<Integer, Integer> scanDatabaseToDetermineFrequencyOfSingleItems(String input) throws FileNotFoundException, IOException
	{
		return scanDatabaseToDetermineFrequencyOfSingleItems(input," ");
	}
	private  Map<Integer, Integer> scanDatabaseToDetermineFrequencyOfSingleItems(String input, String separator)
			throws FileNotFoundException, IOException {
		// a map for storing the support of each item (key: item, value: support)
		 Map<Integer, Integer> mapSupport = new HashMap<Integer, Integer>();
		//Create object for reading the input file
		BufferedReader reader = new BufferedReader(new FileReader(input));
		String line;
		// for each line (transaction) until the end of file
		while( ((line = reader.readLine())!= null)){ 
			// if the line is  a comment, is  empty or is a
			// kind of metadata
			if (line.isEmpty() == true ||  line.charAt(0) == '#' || line.charAt(0) == '%' 	|| line.charAt(0) == '@') {
				continue;
			}
			
			// split the line into items
			String[] lineSplited = line.split(" ");
			// for each item
			for(String itemString : lineSplited){  
				// increase the support count of the item
				Integer item = Integer.parseInt(itemString);
				// increase the support count of the item
				Integer count = mapSupport.get(item);
				if(count == null){
					mapSupport.put(item, 1);
				}else{
					mapSupport.put(item, ++count);
				}
			}
			// increase the transaction count
			transactionCount++;
		}
		// close the input file
		reader.close();
		
		return mapSupport;
	}


	/**
//	 * Write a frequent itemset that is found to the output file or
//	 * keep into memory if the user prefer that the result be saved into memory.
//	 */
//	private void saveItemset(int [] itemset, int itemsetLength, int support) throws IOException {
//		if(itemsetLength < minPatternLength) {
//			return;
//		}
//		
//		// increase the number of itemsets found for statistics purpose
//		itemsetCount++;
//		
//		// if the result should be saved to a file
//		if(writer != null){
//			// copy the itemset in the output buffer and sort items
//			System.arraycopy(itemset, 0, itemsetOutputBuffer, 0, itemsetLength);
//			Arrays.sort(itemsetOutputBuffer, 0, itemsetLength);
//			
//			// Create a string buffer
//			StringBuilder buffer = new StringBuilder();
//			// write the items of the itemset
//			for(int i=0; i< itemsetLength; i++){
//				buffer.append(itemsetOutputBuffer[i]);
//				if(i != itemsetLength-1){
//					buffer.append(' ');
//				}
//			}
//			// Then, write the support
//			buffer.append(" #SUP: ");
//			buffer.append(support);
//			// write to file and create a new line
//			writer.write(buffer.toString());
//			writer.newLine();
//			
//		}// otherwise the result is kept into memory
//		else{
//			// create an object Itemset and add it to the set of patterns 
//			// found.
//			int[] itemsetArray = new int[itemsetLength];
//			System.arraycopy(itemset, 0, itemsetArray, 0, itemsetLength);
//			
//			// sort the itemset so that it is sorted according to lexical ordering before we show it to the user
//			Arrays.sort(itemsetArray);
//			
//			Itemset itemsetObj = new Itemset(itemsetArray);
//			itemsetObj.setAbsoluteSupport(support);
//			patterns.addItemset(itemsetObj, itemsetLength);
//		}
//	}
	
	
	// ======================================
	// ======================================
	/**
	 * Method to save an itemset to the queue of top-n patterns
	 * 
	 * @param itemset an itemset
	 * @param support the support of the itemset
	 */
	private void saveItemset(int [] itemset, int itemsetLength, int support) {
		if(itemsetLength < minPatternLength) {
			return;
		}
		
		// create an object Itemset and add it to the set of patterns 
		// found.
		int[] itemsetArray = new int[itemsetLength];
		System.arraycopy(itemset, 0, itemsetArray, 0, itemsetLength);
		
		// sort the itemset so that it is sorted according to lexical ordering before we show it to the user
		Arrays.sort(itemsetArray);
		
		Itemset itemsetObj = new Itemset(itemsetArray);
		itemsetObj.setAbsoluteSupport(support);
		
		nItemsets.add(itemsetObj);
		if (nItemsets.size() > n) {
			if (support > this.minSupportRelative) {
				Itemset lower;
				do {
					lower = nItemsets.peek();
					if (lower == null) {
						break; // / IMPORTANT
					}
					nItemsets.remove(lower);
				} while (nItemsets.size() > n);
				this.minSupportRelative = nItemsets.peek().getAbsoluteSupport();
//				System.out.println(nItemsets);
//				System.out.println(minsupRelative);
			}
		}
	}

	
	private void saveItemsetToFile(Itemset itemset) throws IOException {
		// if the result should be saved to a file
		if (writer != null) {
			writer.write(itemset.toString() + " #SUP: " + itemset.getAbsoluteSupport());
			writer.newLine();
		} // otherwise the result is kept into memory
		else {
			patterns.addItemset(itemset, itemset.size());
		}
	}

	/**
	 * Print statistics about the algorithm execution to System.out.
	 */
	public void printStats() {
		printStats("SPMF_FPGrowth_TopK");
	}

	// 2025-06-16 Malliaridis: New stats procedure to fit with other experiments	
	public void printStats(String algorithm) {
		System.out.println("=============  FP-GROWTH (top-k version) 2.61 - STATS =============");
		long time = endTime - startTimestamp;
		System.out.println("Transactions count from database: " + transactionCount);
		System.out.print("Max memory usage: " + MemoryLogger.getInstance().getMaxMemory() + " mb \n");
		System.out.println("Frequent itemsets count: " + nItemsets.size()); 
		System.out.println("Total time: " + time/1000. + " s");
		System.out.println("Language: java");
		System.out.println("library: SPMF");
        System.out.println("Algorithm" + algorithm);
		System.out.println("minSup:" + nItemsets.peek().getRelativeSupport(transactionCount));
        System.out.println("minSup Absolute" + nItemsets.peek().getAbsoluteSupport());
        System.out.println("totalFI: " + nItemsets.size());
		System.out.println("===================================================");
	}

	// 2025-06-16 Malliaridis: New stats procedure to fit with other experiments	
	public JSONObject printStatsNew(String algorithm) {
		JSONObject jsonObject = new JSONObject();
        jsonObject.put("Language", "java");
        jsonObject.put("library", "SPMF");
        jsonObject.put("Algorithm", algorithm);
		jsonObject.put("minSup", nItemsets.peek().getRelativeSupport(transactionCount));
        jsonObject.put("minSup Absolute", nItemsets.peek().getAbsoluteSupport());
        jsonObject.put("totalFI", nItemsets.size());
        jsonObject.put("Runtime", (endTime - startTimestamp)/1000.);
        jsonObject.put("Memory", MemoryLogger.getInstance().getMaxMemory());
        return jsonObject;
	}

	/**
	 * Get the number of transactions in the last transaction database read.
	 * @return the number of transactions.
	 */
	public int getDatabaseSize() {
		return transactionCount;
	}

	/** 
	 * Set the maximum pattern length
	 * @param length the maximum length
	 */
	public void setMaximumPatternLength(int length) {
		maxPatternLength = length;
	}
	
	/** 
	 * Set the minimum pattern length
	 * @param length the minimum length
	 */
	public void setMinimumPatternLength(int minPatternLength) {
		this.minPatternLength = minPatternLength;
	}

}
