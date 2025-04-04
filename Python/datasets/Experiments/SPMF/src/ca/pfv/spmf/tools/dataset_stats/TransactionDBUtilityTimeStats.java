package ca.pfv.spmf.tools.dataset_stats;

import java.io.BufferedReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

/* This file is copyright (c) Cheng-Wei Wu et al.
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

/**
 * This class is used to calculate statistics about a transaction database with
 * utility and time information.
 * 
 * @author Philippe Fournier-Viger
 * 
 */

public class TransactionDBUtilityTimeStats {

	/**
	 * Constructor
	 */
	public TransactionDBUtilityTimeStats() {

	}

	/**
	 * Calculate information about a database with utility information
	 * 
	 * @param inputPath an input file path
	 * @throws IOException
	 */
	public void runAlgorithm(String inputPath) throws IOException {

		/** The total utility in this database */
		long totalUtility = 0;

		/** the number of transactions in this database */
		int databaseSize = 0;

		/** the maximum ID of items in this database */
		int maxID = 0;

		/** the sum of all transaction length for this database */
		int sumAllLength = 0;

		/** the average transaction length in this database */
		double avgLength = 0.0;

		/** the maximum length of transactions in this database */
		int maxLength = 0;

		/** the set of all items in this database */
		Set<Integer> allItem = new HashSet<Integer>();

		/** the list of utility values */
		List<Integer> utilityValues = new ArrayList<Integer>();

		BufferedReader br;
		String line = ""; // get the String by reading from BufferedReader
		String[] tokens1, tokens2; // get the result of split String

		br = new java.io.BufferedReader(new java.io.FileReader(inputPath));
		int minTime = Integer.MAX_VALUE;
		int maxTime = 0;

		while (true) {
			line = br.readLine();
			if (line == null) {
				break;
			}
			// if the line is a comment, is empty or is a
			// kind of metadata
			if (line.isEmpty() == true || line.charAt(0) == '#' || line.charAt(0) == '%' || line.charAt(0) == '@') {
				continue;
			}
			databaseSize++;
			// divide into 4 parts : 1.itemsets 2.transaction utility 3.utility of each item
			// 4. time information
			tokens1 = line.split(":");
			// divide itemsets into items
			tokens2 = tokens1[0].split(" ");
			totalUtility += Long.parseLong(tokens1[1]);
			int time = Integer.parseInt(tokens1[3]);

			if (time > maxTime) {
				maxTime = time;
			}
			if (time < minTime) {
				minTime = time;
			}

			sumAllLength += tokens2.length;
			if (maxLength < tokens2.length) {
				maxLength = tokens2.length;
			}

			for (int i = 0; i < tokens2.length; i++) {
				int num = Integer.parseInt(tokens2[i]);
				if (num > maxID) {
					maxID = num;
				}
				allItem.add(num);
			}

			// for the utility values
			String[] utilities = tokens1[2].split(" ");
			for (String utilityString : utilities) {
				int utility = Integer.parseInt(utilityString);
				utilityValues.add(utility);
			}
		}
		br.close();

		avgLength = (int) ((double) sumAllLength / databaseSize * 100) / 100.0; // accurate to the second decimal place

		// Print the calculated information to the console
		System.out.println("---------- Utility transaction database with time information----------");
		System.out.println("Number of transations : " + String.valueOf(databaseSize));
		System.out.println("Transactions time range from: " + minTime + " to " + maxTime);
		System.out.println("Total utility : " + String.valueOf(totalUtility));
		System.out.println("Number of distinct items : " + String.valueOf(allItem.size()));
		System.out.println("Maximum Id of item : " + String.valueOf(maxID));
		System.out.println("Average length of transaction : " + String.valueOf(avgLength));
		System.out.println("Maximum length of transaction : " + String.valueOf(maxLength));
		double density = (avgLength / allItem.size()) * 100d;
		System.out.println("Average utility per item: "
				+ BasicStatsFunctions.calculateMean(utilityValues) + " standard deviation: "
				+ BasicStatsFunctions.calculateStdDeviation(utilityValues) + " variance: "
				+ BasicStatsFunctions.calculateVariance(utilityValues));
		System.out.println("Database density: " + density + " %");

	}

}
