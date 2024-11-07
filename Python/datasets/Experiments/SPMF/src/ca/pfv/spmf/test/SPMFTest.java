package ca.pfv.spmf.test;

import java.io.FileWriter;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

import org.json.JSONObject;

import ca.pfv.spmf.algorithms.frequentpatterns.apriori.AlgoApriori;
import ca.pfv.spmf.algorithms.frequentpatterns.aprioriTID.AlgoAprioriTID_Bitset;
import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth;
import ca.pfv.spmf.algorithms.frequentpatterns.negFIN.AlgoNegFIN;

public class SPMFTest {

	public static void main(String [] arg) throws IOException{

        //Declaration section
        String datasetName = "chess.dat";
        double minsup = 0.8; // means a minsup of 2 transaction (we used a relative support)

        String outPutResultsfile, noPrefix;
        JSONObject pSN;

        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;




        ////////////////////////////
        String algorithm="Apriori";
		AlgoApriori algo = new AlgoApriori();
		// Uncomment the following line to set the maximum pattern length (number of items per itemset)
        //algo.setMaximumPatternLength(3);
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.fim";
		algo.runAlgorithm(minsup, input, outPutResultsfile);
		pSN=algo.printStatsNew();
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN.toString(4)); // 4 is for pretty-print indentation
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
        ////////////////////////////


        ////////////////////////////
        algorithm="prioriTID_Bitset";
		AlgoAprioriTID_Bitset algo1 = new AlgoAprioriTID_Bitset();
		// Uncomment the following line to set the maximum pattern length (number of items per itemset)
        //algo1.setMaximumPatternLength(3);
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.fim";
		algo1.runAlgorithm(input, outPutResultsfile, minsup);
		pSN=algo1.printStatsNew();
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN.toString(4)); // 4 is for pretty-print indentation
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
        ////////////////////////////




        ////////////////////////////
        algorithm="FPGrowth";
        AlgoFPGrowth algoFPGrowth = new AlgoFPGrowth();
		// Uncomment the following line to set the maximum pattern length (number of items per itemset)
        //algo1.setMaximumPatternLength(3);
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.fim";
		algoFPGrowth.runAlgorithm(input, outPutResultsfile, minsup);
		pSN=algoFPGrowth.printStatsNew();
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN.toString(4)); // 4 is for pretty-print indentation
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
        ////////////////////////////


        ////////////////////////////
        algorithm="negFIN";
		AlgoNegFIN algoNegFIN = new AlgoNegFIN();
		// Uncomment the following line to set the maximum pattern length (number of items per itemset)
        //algo1.setMaximumPatternLength(3);
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.fim";
		algoNegFIN.runAlgorithm(input, minsup, outPutResultsfile);
		pSN=algoNegFIN.printStatsNew();
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minsup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN.toString(4)); // 4 is for pretty-print indentation
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
        ////////////////////////////

	}
}

	// 
	// //Malliaridis output
	// public JSONObject printStatsNew() {
	// 	JSONObject jsonObject = new JSONObject();
    //     jsonObject.put("totalFI", itemsetCount);
    //     jsonObject.put("Runtime", (endTimestamp - startTimestamp)/1000.);
    //     jsonObject.put("Memory", MemoryLogger.getInstance().getMaxMemory());
    //     return jsonObject;
	// }

