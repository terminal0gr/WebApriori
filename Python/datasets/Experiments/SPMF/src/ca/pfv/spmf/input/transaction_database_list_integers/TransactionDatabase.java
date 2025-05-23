package ca.pfv.spmf.input.transaction_database_list_integers;

/* Copyright (c) 2008-2024 Philippe Fournier-Viger
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
* 
* You should have received a copy of the GNU General Public License along with
* SPMF. If not, see <http://www.gnu.org/licenses/>.
*/
import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * This class represents a transaction database (a.k.a. binary context),
 * implemented as a list of integers. It can read a transaction database
 * directly from a file. See the ca.pfv.spmf.test folder for some examples of
 * files that can be read.
 * 
 * @author Philipe-Fournier-Viger
 */
public class TransactionDatabase {

	/** The list of items in this database */
	private final Set<Integer> items = new HashSet<Integer>();

	/** the list of transactions */
	private final List<List<Integer>> transactions = new ArrayList<List<Integer>>();

	/** largest item id */
	private int maxItemID;

	/**
	 * A map, where an entry in the map is key = String (attribute value), value =
	 * Integer (item id)
	 */
	Map<Integer, String> mapItemIDtoStringValue = null;

	/**
	 * Method to add a new transaction to this database.
	 * 
	 * @param transaction the transaction to be added
	 */
	public void addTransaction(List<Integer> transaction) {
		transactions.add(transaction);
		items.addAll(transaction);
	}

	/**
	 * Method to load a file containing a transaction database into memory
	 * 
	 * @param path the path of the file
	 * @throws IOException exception if error reading the file
	 */
	public void loadFile(String path) throws IOException {
		loadFile(path," ");
	}

	public void loadFile(String path, String delimiter) throws IOException {
		String thisLine; // variable to read each line
		try (BufferedReader myInput = new BufferedReader(new InputStreamReader(new FileInputStream(new File(path))))) {

			maxItemID = 0;
			// for each line
			while ((thisLine = myInput.readLine()) != null) {
				// if the line is not a comment, is not empty or is not other
				// kind of metadata
				// if the line starts with a comment
				if (thisLine.isEmpty() == false) {
					if (thisLine.startsWith("@ITEM")) {
						// remove "@ITEM="
						thisLine = thisLine.substring(6);
						// get the position of the first = in the remaining string
						int index = thisLine.indexOf("=");
						int itemID = Integer.parseInt(thisLine.substring(0, index));
						String stringValue = thisLine.substring(index + 1);
//					System.out.println(itemID);
//					System.out.println(stringValue);
						if (mapItemIDtoStringValue == null) {
							mapItemIDtoStringValue = new HashMap<Integer, String>();
						}
						mapItemIDtoStringValue.put(itemID, stringValue);
					} else if (thisLine.isEmpty() == false && thisLine.charAt(0) != '#' && thisLine.charAt(0) != '%'
							&& thisLine.charAt(0) != '@') {
						// split the line according to spaces and then
						// call "addTransaction" to process this line.
						addTransaction(thisLine.split(delimiter));
					}
				}
			}
		}
	}

	/**
	 * This method process a line from a file that is read.
	 * 
	 * @param tokens the items contained in this line
	 */
	private void addTransaction(String itemsString[]) {
		// create an empty transaction
		List<Integer> itemset = new ArrayList<Integer>();
		// for each item in this line
		for (String attribute : itemsString) {
			// convert from string to int
			int item = Integer.parseInt(attribute);
			// add the item to the current transaction
			itemset.add(item);
			// add the item to the set of all items in this database
			items.add(item);

			if (item > maxItemID) {
				maxItemID = item;
			}
		}
		// add the transactions to the list of all transactions in this database.
		transactions.add(itemset);
	}

	/**
	 * Method to print the content of the transaction database to the console.
	 */
	public void printDatabase() {
		System.out.println("===================  TRANSACTION DATABASE ===================");
		int count = 0;
		// for each transaction
		for (List<Integer> itemset : transactions) { // pour chaque objet
			System.out.print(count + ":  ");
			print(itemset); // print the transaction
			count++;
		}
	}

	/**
	 * Method to print a transaction to System.out.
	 * 
	 * @param itemset a transaction
	 */
	private void print(List<Integer> itemset) {
		StringBuilder r = new StringBuilder();
		// for each item in this transaction
		for (Integer item : itemset) {
			// append the item to the StringBuilder
			r.append(item.toString());
			r.append(' ');
		}
		System.out.println(r); // print to System.out
	}

	/**
	 * Get the number of transactions in this transaction database.
	 * 
	 * @return the number of transactions.
	 */
	public int size() {
		return transactions.size();
	}

	/**
	 * Get the list of transactions in this database
	 * 
	 * @return A list of transactions (a transaction is a list of Integer).
	 */
	public List<List<Integer>> getTransactions() {
		return transactions;
	}

	/**
	 * Get the set of items contained in this database.
	 * 
	 * @return The set of items.
	 */
	public Set<Integer> getItems() {
		return items;
	}

	/**
	 * Get the name corresponding to an item id, if one is known. Otherwise returns
	 * null.
	 * 
	 * @param item the item
	 * @return a string or null
	 */
	public String getNameForItem(Integer item) {
		if (mapItemIDtoStringValue == null) {
			return null;
		}
		String name = mapItemIDtoStringValue.get(item);
		if (name == null) {
			return null;
		}
		return name;
	}

	/**
	 * Return a map to convert item names to strings (if applicable)
	 * 
	 * @return a map or null;
	 */
	public Map<Integer, String> getMapItemToStringValues() {
		return mapItemIDtoStringValue;
	}

	/**
	 * Get the maximum Item ID
	 * 
	 * @return the id
	 */
	public int getMaxItemID() {
		return maxItemID;
	}
}
