package ca.pfv.spmf.test;

import java.io.FileWriter;
import java.io.IOException;

import org.json.JSONObject;

import ca.pfv.spmf.algorithms.frequentpatterns.apriori.AlgoAprioriTopK;
import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowthTOPK;

public class SPMFTestTopN {

	public static void main(String [] arg) throws IOException{

        //Declaration section
        String datasetName = "kosarak.dat";
        int topK = 100; // means a minSup of 2 transaction (we used a relative support)

        String outPutResultsfile, noPrefix;
        JSONObject pSN;

        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;
        String algorithm = "";


        ////////////////////////////
        // algorithm="FPGrowth_topN";
		// AlgoFPGrowthTOPK algoFPGrowthTOPK = new AlgoFPGrowthTOPK();
		// // Uncomment the following line to set the maximum pattern length (number of items per itemset)
        // //algo.setMaximumPatternLength(3);
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Integer.toString(topK) + "_" + algorithm + "_SPMF.fim";
		// algoFPGrowthTOPK.runAlgorithm(input, outPutResultsfile, topK);
		// pSN=algoFPGrowthTOPK.printStatsNew(algorithm);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Integer.toString(topK) + "_" + algorithm + "_SPMF.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        ////////////////////////////
        algorithm="Apriori_topN";
        AlgoAprioriTopK algoAprioriTOPK = new AlgoAprioriTopK();
		// Uncomment the following line to set the maximum pattern length (number of items per itemset)
        //algo.setMaximumPatternLength(3);
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Integer.toString(topK) + "_" + algorithm + "_SPMF.fim";
		algoAprioriTOPK.runAlgorithm(topK, input, outPutResultsfile);
		pSN=algoAprioriTOPK.printStatsNew(algorithm);
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Integer.toString(topK) + "_" + algorithm + "_SPMF.json";
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

