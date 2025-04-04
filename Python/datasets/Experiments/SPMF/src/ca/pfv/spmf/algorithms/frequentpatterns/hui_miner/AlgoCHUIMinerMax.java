package ca.pfv.spmf.algorithms.frequentpatterns.hui_miner;



/* This file is copyright (c) 2008-2014 Philippe Fournier-Viger
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
import java.io.File;
import java.io.FileInputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;

import ca.pfv.spmf.tools.MemoryLogger;

/**
 * CHUI-Mine(Max)-EUCP is an implementation of CHUI-Mine(Max) based on
 * (Wu et al.) with some modifications to improve performance. 
 * 
 * The modifications are
 * -  this implementation does not compute the utility unit arrays for recovery of
 * all itemsets. 
 * - this implementation adds the EUCP strategy from the FHM algorithm to improve the performance
 *   of CHUI-Mine(Max). This algorithm is thus named "E-CHUI-Mine(Max).
 * 
 * @see UtilityList
 * @see Element
 * @author Philippe Fournier-Viger 2014
 */
public class AlgoCHUIMinerMax {

	/** the time the algorithm started */
	public long startTimestamp = 0;   
	/**the time the algorithm terminated */
	public long endTimestamp = 0;   

	/** the number of MHUI generated */
	public int mhuiCount = 0;  
	
	/** the number of candidates considered */
	public int candidateCount =0;
	
	/** Map to remember the TWU of each item */
	Map<Integer, Integer> mapItemToTWU;
	
	/** Writer object to write to the output file if the user choose to */
	BufferedWriter writer = null;  
	
	/** List of maximal HUI found (if the result is kept in memory) */
	List<Itemset> mhuis = null;
	
	/** The minimum utility threshold */
	int minUtility = 0;
	
	/** OPTIMIZATION SPECIFIC TO E-CHUI-MINE(max). 
     We integrate the structure used by the EUCP strategy proposed in FHM 
     (Fournier-Viger et al., 2014) for pruning candidates.
	 Key: for an item x, 
	 Value: a map of item where key is an item y and value is the TWU of {x,y} 
	 */
	Map<Integer, Map<Integer, Integer>> mapFMAP;  // PAIR OF ITEMS , item --> item, twu
	
	/** Determine if the EUCP strategy will be used */
	boolean useEUCPstrategy;
	
	
	/**
	 * Default constructor
	 */
	public AlgoCHUIMinerMax(boolean useEUCPstrategy) {
		this.useEUCPstrategy = useEUCPstrategy;
	}
	
	
	///====================== SPECIFIC TO MHUIs ============== /
	/** variable that indicate the MID that will be assigned to the next MHUI found */
	int nextMID = 0;
	
	/** map between items to their respective MID list */
	Map<Integer, List<Integer>> mapItemToMIDs = null;
	
	/**
	 * Get the mid list of an item
	 * @param item the item
	 * @return the mid list as a list of integers
	 */
	public List<Integer> getMIDList(int item){
		return mapItemToMIDs.get(item);
	}
	

	/**
	 * Add an MID to the MID list of an item
	 * @param mid the mid to be added
	 * @param item the item
	 */
	private void addMIDtoMIDListOfItem(int mid, int item) {
		getMIDList(item).add(mid);
	}

	
	/**
	 * This method intersect two MID lists to create a new MID lists
	 * @param midlist1  the first MID list
	 * @param midlist2  the second MID list
	 * @return  the intersection of the MID lists
	 */
	public List<Integer> intersectTwoMIDLists(
			List<Integer> midlist1, List<Integer> midlist2){
		// A NAIVE IMPLEMENTATION IN COMMENTS, CAN BE USED FOR CHECKING THE RESULTS
		HashSet<Integer> set = new HashSet<Integer>();
		set.addAll(midlist1);
		set.retainAll(midlist2);
		return new ArrayList<Integer>(set);
		
//		// create a new array having the smallest size between the two arrays
//		final int newArraySize = (midlist1.size() < midlist2.size() ) ? midlist1.size()  : midlist2.size();		
//		List<Integer> intersection = new ArrayList<Integer>(newArraySize);
//
//	    int pos1 = 0;
//	    int pos2 = 0;
//	    while(pos1 < midlist1.size()  && pos2 < midlist2.size() ) {
//	    	if(midlist1.get(pos1) < midlist2.get(pos2)) {
//	    		pos1++;
//	    	}else if(midlist2.get(pos2) < midlist1.get(pos1))  {
//	    		pos2++;
//	    	}else { // if they are the same
//	    		intersection.add(midlist1.get(pos1));
//	    		pos1++;
//	    		pos2++;
//	    	}
//	    }
//	    // return the new array that is full.
//	    return intersection; 
	}

	
	///======================================================= /


	/**
	 * Run the algorithm and save the result to file 
	 * @param input the input file path
	 * @param output the output file path
	 * @param minUtility the minimum utility threshold
	 * @param output the output file path or null if the user wants to keep result in memory
	 * @return  the set of MHUIs if the user chose to save the result to memory
	 * @throws IOException exception if error while writing the file
	 */
	public List<Itemset> runAlgorithm(String input,  int minUtility, String output) throws IOException {
		// reset maximum
		MemoryLogger.getInstance().reset();
		
		// keep the min-util threshold
		this.minUtility = minUtility;
		
		// ============================
		// Initialize the first MID that will be assigned to 0
		nextMID = 0;
		// Initialize the map for storing the mid lists of each item
		mapItemToMIDs = new HashMap<Integer, List<Integer>>();
		//============================
		
		// initialize object to write output file if the user chose to write the output
		// to file
		if(output != null) {
			writer = new BufferedWriter(new FileWriter(output));
		}else {
//			// If the user chose to save to memory, we initialize the structures
//			// for storing CHUIs into memory.
			mhuis = new ArrayList<Itemset>();
		}

		// Initialize the structure for EUCP strategy that is not included in
		// the original CHUI-Mine(max) algorithm but is included here to
		// improve performances.
		if(useEUCPstrategy) {
			mapFMAP =  new HashMap<Integer, Map<Integer, Integer>>();
		}
		
		// record the start time of the algorithm
		startTimestamp = System.currentTimeMillis();

		//  We create a  map to store the TWU of each item
		mapItemToTWU = new HashMap<Integer, Integer>();

		// We scan the database a first time to calculate the TWU of each item.
		BufferedReader myInput = null;
		String thisLine;
		try {
			// prepare the object for reading the file
			myInput = new BufferedReader(new InputStreamReader( new FileInputStream(new File(input))));
			// for each line (transaction) until the end of file
			while ((thisLine = myInput.readLine()) != null) {
				// if the line is  a comment, is  empty or is a
				// kind of metadata
				if (thisLine.isEmpty() == true ||
						thisLine.charAt(0) == '#' || thisLine.charAt(0) == '%'
								|| thisLine.charAt(0) == '@') {
					continue;
				}
				
				// split the transaction according to the : separator
				String split[] = thisLine.split(":"); 
				// the first part is the list of items
				String items[] = split[0].split(" "); 
				// the second part is the transaction utility
				int transactionUtility = Integer.parseInt(split[1]);  
				// for each item, we add the transaction utility to its TWU
				for(int i=0; i <items.length; i++){
					// convert item to integer
					Integer item = Integer.parseInt(items[i]);
					// get the current TWU of that item
					Integer twu = mapItemToTWU.get(item);
					// add the utility of the item in the current transaction to its twu
					twu = (twu == null)? 
							transactionUtility : twu + transactionUtility;
					mapItemToTWU.put(item, twu);
				}
			}
		} catch (Exception e) {
			// catches exception if error while reading the input file
			e.printStackTrace();
		}finally {
			if(myInput != null){
				myInput.close();
			}
	    }
		
		// CREATE A LIST TO STORE THE UTILITY LIST OF ITEMS WITH TWU  >= MIN_UTILITY.
		List<UtilityList> listOfUtilityLists = new ArrayList<UtilityList>();
		// CREATE A MAP TO STORE THE UTILITY LIST FOR EACH ITEM.
		// Key : item    Value :  utility list associated to that item
		Map<Integer, UtilityList> mapItemToUtilityList = new HashMap<Integer, UtilityList>();
		
		// For each item
		for(Integer item: mapItemToTWU.keySet()){
			// if the item is promising  (TWU >= minutility)
			if(mapItemToTWU.get(item) >= minUtility){
				// create an empty Utility List that we will fill later.
				UtilityList uList = new UtilityList(item);
				mapItemToUtilityList.put(item, uList);
				// add the item to the list of high TWU items
				listOfUtilityLists.add(uList); 
			}
		}
		// SORT THE LIST OF HIGH TWU ITEMS IN ASCENDING ORDER
		Collections.sort(listOfUtilityLists, new Comparator<UtilityList>(){
			public int compare(UtilityList o1, UtilityList o2) {
				// compare the TWU of the items
				return compareItems(o1.item, o2.item);
			}
			} );
		
		// SECOND DATABASE PASS TO CONSTRUCT THE UTILITY LISTS 
		// OF 1-ITEMSETS  HAVING TWU  >= minutil (promising items)
		try {
			// prepare object for reading the file
			myInput = new BufferedReader(new InputStreamReader(new FileInputStream(new File(input))));
			// variable to count the number of transaction
			int tid =0;
			// for each line (transaction) until the end of file
			while ((thisLine = myInput.readLine()) != null) {
				// if the line is  a comment, is  empty or is a
				// kind of metadata
				if (thisLine.isEmpty() == true ||
						thisLine.charAt(0) == '#' || thisLine.charAt(0) == '%'
								|| thisLine.charAt(0) == '@') {
					continue;
				}
				
				// split the line according to the separator
				String split[] = thisLine.split(":");
				// get the list of items
				String items[] = split[0].split(" ");
				// get the list of utility values corresponding to each item
				// for that transaction
				String utilityValues[] = split[2].split(" ");

				int newTU =0;
				
				// Create a list to store items
				List<PairItemUtility> revisedTransaction = new ArrayList<PairItemUtility>();
				// for each item
				for(int i=0; i <items.length; i++){
					/// convert values to integers
					PairItemUtility pair = new PairItemUtility();
					pair.item = Integer.parseInt(items[i]);
					pair.utility = Integer.parseInt(utilityValues[i]);
					// if the item has enough utility
					if(mapItemToTWU.get(pair.item) >= minUtility){
						// add it
						revisedTransaction.add(pair);
						newTU += pair.utility; // NEW OPTIMIZATION
					}
				}
				
				// sort the transaction
				Collections.sort(revisedTransaction, new Comparator<PairItemUtility>(){
					public int compare(PairItemUtility o1, PairItemUtility o2) {
						return compareItems(o1.item, o2.item);
					}});
				
				// This variable will be used to calculate the remaining utility 
				// in a transaction after the some items have been processed
				int remainingUtility = newTU;
								
				// for each item left in the transaction
				for(int i = 0; i< revisedTransaction.size(); i++){
					PairItemUtility pair =  revisedTransaction.get(i);
	
					// subtract the utility of this item from the remaining utility
					remainingUtility = remainingUtility - pair.utility;
					
					// get the utility list of this item
					UtilityList utilityListOfItem = mapItemToUtilityList.get(pair.item);
					
					// Add a new Element to the utility list of this item corresponding to this transaction
					Element element = new Element(tid, pair.utility, remainingUtility);
					
					utilityListOfItem.addElement(element);
										
					// BEGIN CODE for updating the structure used
					// BY THE EUCP STRATEGY INTRODUCED IN E-CHUI-Mine(max)
					if(useEUCPstrategy) {
						Map<Integer, Integer> mapFMAPItem = mapFMAP.get(pair.item);
						if(mapFMAPItem == null) {
							mapFMAPItem = new HashMap<Integer, Integer>();
							mapFMAP.put(pair.item, mapFMAPItem);
						}
		
						for(int j = i+1; j< revisedTransaction.size(); j++){
							PairItemUtility pairAfter = revisedTransaction.get(j);
							Integer twuSum = mapFMAPItem.get(pairAfter.item);
							if(twuSum == null) {
								mapFMAPItem.put(pairAfter.item, newTU);
							}else {
								mapFMAPItem.put(pairAfter.item, twuSum + newTU);
							}
						}
					}
					// END OF CODE FOR EUCP STRATEGY

				}
				tid++; // increase tid number for next transaction

			}
		} catch (Exception e) {
			// to catch error while reading the input file
			e.printStackTrace();
		}finally {
			if(myInput != null){
				myInput.close();
			}
	    }
		
		//============= INITIALIZE MID-LISTS OF SINGLE ITEMS ======
		for(UtilityList ulist : listOfUtilityLists) {
			mapItemToMIDs.put(ulist.item, new ArrayList<Integer>());
		}
		//=============
		
		// check the memory usage
		MemoryLogger.getInstance().checkMemory();

		// Mine the database recursively
		// (3) CALL THE recursive procedure
		chuimineMAX_eucp(true, new int[0], new ArrayList<Integer>(), null, new ArrayList<UtilityList>(), listOfUtilityLists);
		
		// check the memory usage again and close the file.
		MemoryLogger.getInstance().checkMemory();
		
		// close output file if the user chose to save output to file
		if(writer != null) {
			writer.close();
		}
		
		// record end time
		endTimestamp = System.currentTimeMillis();
		return mhuis;
	}
	
	
	/**
	 * This is the recursive method to find all high utility itemsets. It writes
	 * the itemsets to the output file.
	 * @param closedSet  This is the current prefix. Initially, it is empty.
	 * @param closedsetMIDs The mid list of the closedset itemset
	 * @param closedSetUL This is the Utility List of the prefix. Initially, it is empty.
	 * @param minUtilityRatio The minUtility threshold.
	 * @throws IOException if an error occurs while writing to file
	 * @return true if a MHUI was found. Otherwise false
	 */
	private boolean chuimineMAX_eucp(boolean firstTime, int [] closedSet, List<Integer> closedsetMIDs, UtilityList closedSetUL, 
			List<UtilityList> preset, List<UtilityList> postset)
			throws IOException {
		
		boolean foundOneMHUI = false;
		
		//L2: for all i in postset
		for(UtilityList iUL : postset){
			// L4 Calculate the tidset of the new GENERATOR "closedset U {i}"
			UtilityList newgen_TIDs;
			List<Integer> newgen_MIDs;
			// if the first time
			if(firstTime){
				// it is the tidset of it
				newgen_TIDs = iUL;
				// the midlist is the midlist of the item
				newgen_MIDs = getMIDList(iUL.item);
			}else{
				// otherwise we intersect the tidset of closedset and the
				// tidset of i
				newgen_TIDs = construct(closedSetUL, iUL);
				// and construct the midlist of newGen
				newgen_MIDs = intersectTwoMIDLists(closedsetMIDs, getMIDList(iUL.item));
			}
			// if newgen has high utility supersets
			if(isPassingHUIPruning(newgen_TIDs)){
				// L3: newgen = closedset U {i}
				// Create the itemset for newgen
				int[] newGen = appendItem(closedSet, iUL.item);	
				
				// L5:  if newgen is not a duplicate
				if(is_dup(newgen_TIDs, preset) == false){
					// L6: ClosedsetNew = newGen
					int[] closedSetNew = newGen;	

					// Initialize tidset and mist list for closedsetNew
					UtilityList closedsetNewTIDs = newgen_TIDs;
					List<Integer> closedsetNewMIDs = newgen_MIDs;
					
//					// L7 : PostsetNew = emptyset
					List<UtilityList> postsetNew = new ArrayList<UtilityList>();
					
					// for each item J in the postset
					boolean passedHUIPruning = true;
					for(UtilityList jUL : postset){
						// if J is smaller than I according to the total order on items, we skip it
						if(jUL.item == iUL.item || compareItems(jUL.item, iUL.item) < 0){
							continue;
						}
						
						// ======================== CHECK THE EUCP STRATEGY
						// ======================= WHICH WAS INTRODUCED IN FHM (Fournier-Viger et al, 2014)
						boolean shouldPrune = useEUCPstrategy && checkEUCPStrategy(iUL.item, jUL.item);
						if(shouldPrune) {
//							System.out.println("PRUNE");
							continue;
						}
						candidateCount++;
						// =========================== END OF CODE FOR EUCP STRATEGY
						
						if(containsAllTIDS(jUL, newgen_TIDs)) {
							closedSetNew = appendItem(closedSetNew, jUL.item);	
							closedsetNewTIDs = construct(closedsetNewTIDs, jUL);
							// calculate MIDlist by intersecting with mid list of item j
							closedsetNewMIDs = intersectTwoMIDLists(closedsetNewMIDs, getMIDList(jUL.item));
							
							if(isPassingHUIPruning(closedsetNewTIDs) == false) {
								passedHUIPruning = false;
								break;
							}
						}else {
							postsetNew.add(jUL);
						}
					}
					
					if(passedHUIPruning) {
						
						// CHECK IF WE CAN PRUNE THE SUCCEEDING SUPERSETS OF CLOSEDSETNEW
						// BY USING MIDLISTS
						// Let Z = ClosedSetNew U Posset(ClosedSetNew)
						// If (MIDLIST(Z) is not empty, the algorithm prune the search space
						// of ClosedSetNew and succeeding supersets of ClosedSetNew
						if(postsetNew.size() > 0) {
							List<Integer> zMIDs = intersectTwoMIDLists(closedsetNewMIDs, getMIDList(postsetNew.get(0).item));
							for(int i=1; i< postsetNew.size() && zMIDs.size() != 0; i++) {
								zMIDs = intersectTwoMIDLists(zMIDs, getMIDList(postsetNew.get(i).item));  // BUG FIX 2019
							}
							if(zMIDs.size() > 0) {
								break;
							}
						}
						
						
						// L16: recursive call
						// FIXED: we have to make a copy of preset before the recursive call
						List<UtilityList> presetNew = new ArrayList<UtilityList>(preset);
						boolean hasSupersetMHUI = chuimineMAX_eucp(false, closedSetNew, closedsetNewMIDs, closedsetNewTIDs, presetNew, postsetNew);
					
						
						// CHECK IF CLOSEDSETNEW IS A MHUI
						// - It must have no succeeding supersets that are MHUIs
						// - It must have an empty MID list
						// - It must be a HUI
						if(hasSupersetMHUI == false && 
								closedsetNewMIDs.size() == 0 &&
								closedsetNewTIDs.sumIutils >= minUtility) {
							
							//====== CLOSED SET NEW IS A MHUI =====
							foundOneMHUI = true;
							// assign a new MID for this item
							int mid = nextMID++; 
							
							// add the mid to the mid list of each item in closedsetNew
							for(int i=0; i< closedSetNew.length; i++) {
								addMIDtoMIDListOfItem(mid, closedSetNew[i]);
							}
							if(closedsetNewTIDs.elements.size() == 2) {
								System.out.println("TEST");
								
								List<Integer> mids = null;
								for(Integer item : closedSetNew) {
									System.out.println(" ITEM: " + item);
									if(mids == null){
										mids = new ArrayList<Integer>(mapItemToMIDs.get(item));
									}else{
										mids.retainAll(mapItemToMIDs.get(item));
									}

									System.out.print(" MIDS: " + mids);
								}
								System.out.println("\n CALCULATED MIDS " + mids);
							}
							
							// output th MHUI
							saveMHUI(closedSetNew, closedsetNewTIDs.sumIutils, closedsetNewTIDs.elements.size());
							// =========================
						}
						
						foundOneMHUI =  foundOneMHUI || hasSupersetMHUI;
					}
					
					// L17 : Preset = Preset U {i}
					preset.add(iUL);
				}
			}	
		}
		
		return foundOneMHUI;
	}

	/**
	 * Check the HUI pruning condition of HUI-Miner for the utilitylist of an itemset
	 * @param utilitylist the utility list of an itemset
	 * @return true if it passes the pruning condition. Otherwise false.
	 */
	private boolean isPassingHUIPruning(UtilityList utilitylist) {
		return utilitylist.sumIutils +  utilitylist.sumRutils >= minUtility;
	}

	/**
	 * Check if a utility list contains all tids from another utility list
	 * @param ul1 the first utility list
	 * @param ul2 the second utility list
	 * @return  true if it contains all tids, otherwise false.
 	 */
	private boolean containsAllTIDS(UtilityList ul1, UtilityList ul2) {
		// for each integer j in preset
		for(Element elmX : ul2.elements){
			// do a binary search to find element ey in py with tid = ex.tid
			Element elmE = findElementWithTID(ul1, elmX.tid);
			if(elmE == null){
				return false;
			}
		}
		return true;
	}

	/**
	 * This method performs the EUCP pruning from the FHM algorithm (see FHM paper at ISMIS 2014)
	 * @param itemX  an item X
	 * @param itemY an item Y
	 * @return true if  TWU({x,y} < minutil.  Otherwise return false
	 */
	private boolean checkEUCPStrategy(int itemX, int itemY) {
		Map<Integer, Integer> mapTWUF = mapFMAP.get(itemX);
		if(mapTWUF != null) {
			Integer twuF = mapTWUF.get(itemY);
			if(twuF != null && twuF < minUtility) {
				return true;
			}
		}
		return false;
	}
	
	/**
	 * Append an item to an itemset
	 * @param itemset an itemset represented as an array of integers
	 * @param item the item to be appended
	 * @return the resulting itemset as an array of integers
	 */
	private int[] appendItem(int[] itemset, int item) {
		int [] newgen = new int[itemset.length+1];
		System.arraycopy(itemset, 0, newgen, 0, itemset.length);
		newgen[itemset.length] = item;
		return newgen;
	}
	
	/**
	 * The method "is_dup" as described in the paper.
	 * @param newgenTIDs  the tidset of newgen
	 * @param preset      the itemset "preset"
	 */
	private boolean is_dup(UtilityList newgenTIDs, List<UtilityList> preset) {
		// L25
		// for each integer j in preset
		for(UtilityList j : preset){
			
			// for each element in the utility list of pX
			boolean containsAll = true;
			for(Element elmX : newgenTIDs.elements){
				// do a binary search to find element ey in py with tid = ex.tid
				Element elmE = findElementWithTID(j, elmX.tid);
				if(elmE == null){
					containsAll = false;
					break;
				}
			}
			
			// L26 :  
			// If tidset of newgen is included in tids of j, return true
			if(containsAll){
				// IMPORTANT
				// NOTE THAT IN ORIGINAL PAPER THEY WROTE FALSE, BUT IT SHOULD BE TRUE
				return true; 
			}
		}
		return false;  // NOTE THAT IN ORIGINAL PAPER THEY WROTE TRUE, BUT IT SHOULD BE FALSE
	}
	
	/**
	 * This method constructs the utility list of Xe
	 * @param uX : the utility list of X
	 * @param uE : the utility list of e
	 */
	private UtilityList construct(UtilityList uX, UtilityList uE) {
		
		// create an empy utility list for pXY
		UtilityList uXE = new UtilityList(uE.item);

		// for each element in the utility list of pX
		for(Element elmX : uX.elements){
			// do a binary search to find element ey in py with tid = ex.tid
			Element elmE = findElementWithTID(uE, elmX.tid);
			if(elmE == null){
				continue;
			}
			// Create the new element
			//     IMPORTANT :  TRICKY PART :  WE NEED TO SUBTRACT  ELMX.RUTIL - ELME.iutil
			// THIS IS BECAUSE DCI  DOES NOT ADD ITEMS TO AN ITEMSET ACCORDING TO THE TOTAL ORDER
			Element elmXe = new Element(elmX.tid, elmX.iutils + elmE.iutils, elmX.rutils - elmE.iutils);
			// add the new element to the utility list of pXY
			uXE.addElement(elmXe);
		}
		// return the utility list of Xe.
		return uXE;
	}
	/**
	 * Do a binary search to find the element with a given tid in a utility list
	 * @param ulist the utility list
	 * @param tid  the tid
	 * @return  the element or null if none has the tid.
	 */
	private Element findElementWithTID(UtilityList ulist, int tid){
		List<Element> list = ulist.elements;
		
		// perform a binary search to check if  the subset appears in  level k-1.
        int first = 0;
        int last = list.size() - 1;
       
        // the binary search
        while( first <= last )
        {
        	int middle = ( first + last ) >>> 1; // divide by 2

            if(list.get(middle).tid < tid){
            	first = middle + 1;  //  the itemset compared is larger than the subset according to the lexical order
            }
            else if(list.get(middle).tid > tid){
            	last = middle - 1; //  the itemset compared is smaller than the subset  is smaller according to the lexical order
            }
            else{
            	return list.get(middle);
            }
        }
		return null;
	}

	/**
	 * Method to save a MHUI.
	 * @param the prefix to be writent o the output file
	 * @param an item to be appended to the prefix
	 * @param utility the utility of the prefix concatenated with the item
	 */
	private void saveMHUI(int[] itemset, long utility, int support) throws IOException {
		mhuiCount++; // increase the number of high utility itemsets found

//		// if the user chose to save to memory
		if(writer == null) {
			mhuis.add(new Itemset(itemset, utility, support));
		}
		else{
			// If the user decide to save to file
			//Create a string buffer
			StringBuilder buffer = new StringBuilder();
			// append the prefix
			for (int i = 0; i < itemset.length; i++) {
				buffer.append(itemset[i]);
				buffer.append(' ');
			}
	
			// append the support value
			buffer.append(" #SUP: ");
			buffer.append(support);
			// append the utility value
			buffer.append(" #UTIL: ");
			buffer.append(utility);
			// write to file
			writer.write(buffer.toString());
			writer.newLine();
		}
	}

	
	/**
	 * Print statistics about the latest execution to System.out.
	 * @throws IOException 
	 */
	public void printStats() throws IOException {
		
		if(useEUCPstrategy) {
			System.out.println("=============  CHUIMine(max)_EUCP ALGORITHM - STATS =============");
		}else {
			System.out.println("=============  CHUIMine(max) ALGORITHM - STATS =============");
		}		
		System.out.println(" Total time ~ "                  + (endTimestamp - startTimestamp) + " ms");
		System.out.println(" Memory ~ "                      + MemoryLogger.getInstance().getMaxMemory() + " MB");
		System.out.println(" MHUI count : " + mhuiCount); 
		System.out.println(" Candidate count : "             + candidateCount);
		System.out.println("=====================================================");
	}

    
	/**
	 * Method to compare items by their TWU
	 * @param item1 an item
	 * @param item2 another item
	 * @return 0 if the same item, >0 if item1 is larger than item2,  <0 otherwise
	 */
	private int compareItems(int item1, int item2) {
		int compare = mapItemToTWU.get(item1) - mapItemToTWU.get(item2);
		// if the same, use the lexical order otherwise use the TWU
		return (compare == 0)? item1 - item2 :  compare;
	}
}