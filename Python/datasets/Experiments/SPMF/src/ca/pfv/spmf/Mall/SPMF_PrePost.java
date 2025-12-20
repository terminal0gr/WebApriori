package ca.pfv.spmf.Mall;

import java.io.FileWriter;
import java.io.IOException;

import ca.pfv.spmf.algorithms.frequentpatterns.fin_prepost.PrePost;

public class SPMF_PrePost {

	public static void main(String [] arg) throws IOException{

        //Declaration section
        String datasetName = "chess.dat";
        Double minSup = 0.945244055068836; // relative support
        // String datasetName = "kosarak.dat";
        // Double minSup = 0.0226928834487203; // relative support
        Boolean usePrePostPlus = false;

        //Line arguments section
        if (arg.length >= 1) {
            datasetName=arg[0];
        }
        if (arg.length >= 2) {
            minSup=Double.parseDouble(arg[1]);
        }
        if (arg.length >= 3) {
            usePrePostPlus=Boolean.parseBoolean(arg[2]);
        }

        String algorithm = "";
        if (usePrePostPlus) {
            algorithm="PrePost+";
        } else {
            algorithm="PrePost";
        }

        String outPutResultsfile, noPrefix;

        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;

        long heapSize = Runtime.getRuntime().totalMemory();  // Initial heap size
        long maxHeapSize = Runtime.getRuntime().maxMemory(); // Maximum heap size
        long freeMemory = Runtime.getRuntime().freeMemory(); // Free heap memory
        System.out.println("Initial Heap Size (Mbytes): " + heapSize/(1024*1024));
        System.out.println("Maximum Heap Size (bytes): " + maxHeapSize/(1024*1024));
        System.out.println("Free Heap Memory (bytes): " + freeMemory/(1024*1024));

        ////////////////////////////
        PrePost algo = new PrePost();
        algo.usePrePostPlus=usePrePostPlus;
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.fim";
		algo.runAlgorithm(input, minSup, outPutResultsfile);
		//algo.printStats();
        String pSN=algo.printStatsNew(algorithm, minSup);
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN); 
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }        
        System.out.println(algorithm + " finished");

	}
}

