package ca.pfv.spmf.Mall;

import java.io.FileWriter;
import java.io.IOException;

import org.json.JSONObject;

import ca.pfv.spmf.algorithms.frequentpatterns.negFIN.AlgoNegFIN;

public class SPMF_negFIN {

	public static void main(String [] arg) throws IOException{

        //Declaration section
        String datasetName = "chess.dat";
        Double minSup = 0.945244055068836; // relative support

        //Line arguments section
        if (arg.length >= 1) {
            datasetName=arg[0];
        }
        if (arg.length >= 2) {
            minSup=Double.parseDouble(arg[1]);
        }

        String outPutResultsfile, noPrefix;

        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;
        String algorithm = "";

        long heapSize = Runtime.getRuntime().totalMemory();  // Initial heap size
        long maxHeapSize = Runtime.getRuntime().maxMemory(); // Maximum heap size
        long freeMemory = Runtime.getRuntime().freeMemory(); // Free heap memory
        System.out.println("Initial Heap Size (Mbytes): " + heapSize/(1024*1024));
        System.out.println("Maximum Heap Size (bytes): " + maxHeapSize/(1024*1024));
        System.out.println("Free Heap Memory (bytes): " + freeMemory/(1024*1024));

        ////////////////////////////
        algorithm="negFIN";
        AlgoNegFIN algo = new AlgoNegFIN();
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.fim";
		algo.runAlgorithm(input, minSup, outPutResultsfile);
		//algo.printStats();
        String pSN=algo.printStatsNew(algorithm, minSup);
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            //file.write(pSN.toString(4)); // 4 is for pretty-print indentation
            file.write(pSN); // 4 is for pretty-print indentation
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }        
        System.out.println(algorithm + " finished");
        ////////////////////////////
        // algorithm="FPGrowth_Top_K";
		// AlgoFPGrowthTOPK algoFPGrowthTopK = new AlgoFPGrowthTOPK();
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + topK + "_" + algorithm + "_SPMF_java.fim";
		// algoFPGrowthTopK.runAlgorithm(input, outPutResultsfile, topK, separator);
		// algoFPGrowthTopK.printStats(algorithm);
        // pSN=algoFPGrowthTopK.printStatsNew(algorithm);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + topK + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        ////////////////////////////


	}
}

