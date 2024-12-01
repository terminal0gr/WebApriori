package ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth;

/**
 * Example of how to use FPGrowth(top-k version) from the source code and save
 * the resutls to a file.
 * @author Philippe Fournier-Viger (Copyright 2008)
 */
public class MainTestFPGrowthTOPK_saveToFile {

	public static void main(String [] arg) throws FileNotFoundException, IOException{

        //Declaration section
        String datasetName = "kosarak.dat";
        Integer k = 1000; 
        String separator = " ";
        String algorithm = "";

        String outPutResultsfile, noPrefix;

		// the file paths
        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;


		//String input = fileToPath("contextPasquier99.txt");  // the database
		//String output = ".//output.txt";  // the path for saving the frequent itemsets found
		String output ="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + k + "_" + algorithm + "_SPMF_java.fim";

		
		// Applying the FPGROWTH algorithmMainTestFPGrowth.java
		AlgoFPGrowthTOPK algo = new AlgoFPGrowthTOPK();
		
		// Uncomment the following line to set the maximum pattern length (number of items per itemset, e.g. 3 )
//		algo.setMaximumPatternLength(3);
		
		// Uncomment the following line to set the minimum pattern length (number of items per itemset, e.g. 2 )
//		algo.setMinimumPatternLength(2);
		
		algo.runAlgorithm(input, output, k);
		algo.printStats();
	}
	
	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTestFPGrowthTOPK_saveToFile.class.getResource(filename);
		 return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}
