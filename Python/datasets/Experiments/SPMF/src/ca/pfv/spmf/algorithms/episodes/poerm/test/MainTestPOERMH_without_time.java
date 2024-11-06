package ca.pfv.spmf.algorithms.episodes.poerm.test;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;

import ca.pfv.spmf.algorithms.episodes.poerm.AlgoPOERMHeadFrequency;


/**
 * Example of how to use the POERMH algorithm from the source code
 * @author Chen YangMing, Philippe Fournier-Viger
 * @see AlgoPOERMHeadFrequency
 */
public class MainTestPOERMH_without_time {

	public static void main(String[] args) throws IOException {
		// the min support of POERMH algorithm
		int minSupport = 2;
		
		// the XSpan of POERMH algorithm
		int xSpan = 4;
		
		// the YSpan of POERMH algorithm
		int ySpan = 2;
		
		// the min confidence of POERMH algorithm
		double minConfidence = 0.3;
		
		// the winlen of POERM algorithm
		int winlen = xSpan + ySpan + 1;
		
		// Input file 
		String inputFile = fileToPath("DB_POERM.dat");
		
		// Output file 
		String outputFile = "output.txt";
		
		// If the input file does not contain timestamps, then set this variable to true
        // to automatically assign timestamps as 1,2,3...
		boolean selfIncrement = true;
		
		AlgoPOERMHeadFrequency poerm = new AlgoPOERMHeadFrequency();
		poerm.runAlgorithm(inputFile, minSupport, xSpan, ySpan, minConfidence, winlen, selfIncrement);
		poerm.writeRule2File(outputFile);
		poerm.printStats();
	}
	
	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTestPOERMH_without_time.class.getResource(filename);
		return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}

}