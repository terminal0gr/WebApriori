package ca.pfv.spmf.Mall;

import java.io.UnsupportedEncodingException;
import java.net.URL;

import ca.pfv.spmf.algorithms.associationrules.TopKRules_and_TNR.AlgoETARM;
import ca.pfv.spmf.algorithms.associationrules.TopKRules_and_TNR.Database;

/**
 * Example of how to use the ETARM algorithm in source code.
 * @author Philippe Fournier-Viger (Copyright 2010)
 */
public class SPMF_ETARM {

	public static void main(String [] arg) throws Exception{
		
        //Declaration section
        String datasetName = "kosarak.dat";
		int topK = 100;  
		double minConf = 0.8; 

        //Line arguments section
        if (arg.length >= 1) {
            datasetName=arg[0];
        }
        if (arg.length >= 2) {
            topK=Integer.parseInt(arg[1]);
        }
        if (arg.length >= 3) {
            minConf=Double.parseDouble(arg[2]);
        }

		// Load database into memory
        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;
		Database database = new Database(); 
		database.loadFile(input); 

		AlgoETARM algo = new AlgoETARM();
		
//		// This optional parameter allows to specify the maximum number of items in the 
//		// left side (antecedent) of rules found:
//		algo.setMaxAntecedentSize(2);  // optional
//
//		// This optional parameter allows to specify the maximum number of items in the 
//		// right side (consequent) of rules found:
//		algo.setMaxConsequentSize(1);  // optional
		
		algo.runAlgorithm(topK, minConf, database);

		algo.printStats();
		algo.writeResultTofile(".//outputETARM.txt");   // to save results to file

	}

	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = SPMF_TopKRules.class.getResource(filename);
		 return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
}
