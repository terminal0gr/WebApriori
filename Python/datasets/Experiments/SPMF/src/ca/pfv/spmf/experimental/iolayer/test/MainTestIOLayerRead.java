package ca.pfv.spmf.experimental.iolayer.test;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

/**
 * Example of how to use HMine from the source code.
 * 
 * @author Philippe Fournier-Viger, 2011.
 */
public class MainTestIOLayerRead {

	public static void main(String[] arg) throws IOException {

		String input = fileToPath("contextPasquier99.txt"); // the database
		String output = ".//output.txt"; // the path for saving the frequent itemsets found

		double minsup = 0.4; // 40% means a minsup of 2 transaction (we used a relative support)

		// Applying the algorithm
		AlgoHMineIOLayerTest algorithm = new AlgoHMineIOLayerTest();

		// Uncomment the following line to set the maximum pattern length (number of
		// items per itemset)
		algorithm.setMaximumPatternLength(4);

		algorithm.runAlgorithm(input, output, minsup);
		algorithm.printStats();
	}

	public static String fileToPath(String filename) throws UnsupportedEncodingException {
		URL url = MainTestIOLayerRead.class.getResource(filename);
		return java.net.URLDecoder.decode(url.getPath(), "UTF-8");
	}
}
