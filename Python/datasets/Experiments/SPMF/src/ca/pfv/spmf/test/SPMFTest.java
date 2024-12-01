package ca.pfv.spmf.test;

import java.io.FileWriter;
import java.io.IOException;

import org.json.JSONObject;

import ca.pfv.spmf.algorithms.frequentpatterns.apriori.AlgoApriori;
import ca.pfv.spmf.algorithms.frequentpatterns.aprioriTID.AlgoAprioriTID_Bitset;
import ca.pfv.spmf.algorithms.frequentpatterns.dFIN.AlgoDFIN;
import ca.pfv.spmf.algorithms.frequentpatterns.eclat.AlgoDEclat;
import ca.pfv.spmf.algorithms.frequentpatterns.eclat.AlgoDEclat_Bitset;
import ca.pfv.spmf.algorithms.frequentpatterns.eclat.AlgoEclat;
import ca.pfv.spmf.algorithms.frequentpatterns.eclat.AlgoEclat_Bitset;
import ca.pfv.spmf.algorithms.frequentpatterns.fin_prepost.FIN;
import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth;
import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowthTOPK;
//import ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth_with_strings.AlgoFPGrowth_Strings;
import ca.pfv.spmf.algorithms.frequentpatterns.negFIN.AlgoNegFIN;
import ca.pfv.spmf.input.transaction_database_list_integers.TransactionDatabase;

public class SPMFTest {

	public static void main(String [] arg) throws IOException{

        //Declaration section
        String datasetName = "";
        
        datasetName="kosarak.dat";
        double minSup = 0.5; 
        Integer TopK = 10000;
        String separator = " ";
        // datasetName="1_L-0023.csv";
        // minSup=0.01;
        // separator=";";

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

        //It is used in some algorithm (e.g. Eclat)
        TransactionDatabase database;


        ////////////////////////////
        // algorithm="Apriori";
		// AlgoApriori algo = new AlgoApriori();
		// // Uncomment the following line to set the maximum pattern length (number of items per itemset)
        // //algo.setMaximumPatternLength(3);
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
		// algo.runAlgorithm(minSup, input, outPutResultsfile, separator);
		// pSN=algo.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        //System.out.println(algorithm + " finished");
        ////////////////////////////


        // ////////////////////////////
        // algorithm="Apriori_TID_bitset";
		// AlgoAprioriTID_Bitset algo1 = new AlgoAprioriTID_Bitset();
		// // Uncomment the following line to set the maximum pattern length (number of items per itemset)
        // //algo1.setMaximumPatternLength(3);
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
		// algo1.runAlgorithm(input, outPutResultsfile, minSup);
		// pSN=algo1.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        // ////////////////////////////


        ////////////////////////////
        // algorithm="Eclat";
        // AlgoEclat algoEclat = new AlgoEclat();
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
        // // Loading the transaction database
		// database = new TransactionDatabase();
		// try {
		// 	database.loadFile(input);
		// } catch (IOException e) {
		// 	e.printStackTrace();
		// } 
		// algoEclat.runAlgorithm(outPutResultsfile, database, minSup, false);
		// pSN=algoEclat.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        ////////////////////////////

        ////////////////////////////
        // algorithm="Eclat_bitset";
        // AlgoEclat_Bitset algoEclat_Bitset = new AlgoEclat_Bitset();
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
        // // Loading the transaction database
		// database = new TransactionDatabase();
		// try {
		// 	database.loadFile(input);
		// } catch (IOException e) {
		// 	e.printStackTrace();
		// } 
		// algoEclat_Bitset.runAlgorithm(outPutResultsfile, database, minSup, false);
		// pSN=algoEclat_Bitset.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        ////////////////////////////


        // ////////////////////////////diffsets
        // algorithm="DEclat";
        // AlgoEclat algoDEclat = new AlgoDEclat();
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
        // // Loading the transaction database
		// database = new TransactionDatabase();
		// try {
		// 	database.loadFile(input);
		// } catch (IOException e) {
		// 	e.printStackTrace();
		// } 
		// algoDEclat.runAlgorithm(outPutResultsfile, database, minSup, false);
		// pSN=algoDEclat.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        // ////////////////////////////

        // ////////////////////////////
        // algorithm="DEclat_bitset";
        // AlgoDEclat_Bitset algoDEclat_Bitset = new AlgoDEclat_Bitset();
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
        // // Loading the transaction database
		// database = new TransactionDatabase();
		// try {
		// 	database.loadFile(input);
		// } catch (IOException e) {
		// 	e.printStackTrace();
		// } 
		// algoDEclat_Bitset.runAlgorithm(outPutResultsfile, database, minSup, false);
		// pSN=algoDEclat_Bitset.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        // ////////////////////////////

        ////////////////////////////
        // algorithm="FPGrowth";
        // AlgoFPGrowth algoFPGrowth = new AlgoFPGrowth();
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
		// algoFPGrowth.runAlgorithm(input, outPutResultsfile, minSup);
		// pSN=algoFPGrowth.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        ////////////////////////////

        ////////////////////////////
        algorithm="FPGrowth_Top_K";
		AlgoFPGrowthTOPK algoFPGrowthTopK = new AlgoFPGrowthTOPK();
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + TopK + "_" + algorithm + "_SPMF_java.fim";
		algoFPGrowthTopK.runAlgorithm(input, outPutResultsfile, TopK);
		//pSN=algoFPGrowthTopK.printStatsNew(algorithm,minSup);
        pSN=algoFPGrowthTopK.printStatsNew(algorithm);
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + TopK + "_" + algorithm + "_SPMF_java.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN.toString(4)); // 4 is for pretty-print indentation
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }
        System.out.println(algorithm + " finished");
        ////////////////////////////


        ////////////////////////////For research in database of type 4 or with string items.
        algorithm="FPGrowth_Strings";
        //AlgoFPGrowth_Strings algo = new AlgoFPGrowth_Strings();


        ////////////////////////////
        // algorithm="FIN";
		// FIN fin = new FIN();
		// // Uncomment the following line to set the maximum pattern length (number of items per itemset)
        // //algo1.setMaximumPatternLength(3);
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
		// fin.runAlgorithm(input, minSup, outPutResultsfile);
		// pSN=fin.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        ////////////////////////////


        ////////////////////////////
        // algorithm="DFIN";
        // AlgoDFIN algoDFIN = new AlgoDFIN();
		// // Uncomment the following line to set the maximum pattern length (number of items per itemset)
        // //algo1.setMaximumPatternLength(3);
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
		// algoDFIN.runAlgorithm(input, minSup, outPutResultsfile);
		// pSN=algoDFIN.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
        // // Write the JSON object to the file
        // try (FileWriter file = new FileWriter(outPutResultsfile)) {
        //     file.write(pSN.toString(4)); // 4 is for pretty-print indentation
        //     file.flush();
        // } catch (IOException e) {
        //     e.printStackTrace();
        // }
        // System.out.println(algorithm + " finished");
        ////////////////////////////

        ////////////////////////////
        // algorithm="negFIN";
		// AlgoNegFIN algoNegFIN = new AlgoNegFIN();
		// // Uncomment the following line to set the maximum pattern length (number of items per itemset)
        // //algo1.setMaximumPatternLength(3);
        // outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.fim";
		// algoNegFIN.runAlgorithm(input, minSup, outPutResultsfile);
		// pSN=algoNegFIN.printStatsNew(algorithm,minSup);
        // outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF_java.json";
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



