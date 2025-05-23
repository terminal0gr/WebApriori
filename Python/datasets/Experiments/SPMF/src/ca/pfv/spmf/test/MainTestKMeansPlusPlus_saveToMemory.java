package ca.pfv.spmf.test;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URL;
import java.util.List;

import ca.pfv.spmf.algorithms.clustering.distanceFunctions.DistanceEuclidian;
import ca.pfv.spmf.algorithms.clustering.distanceFunctions.DistanceFunction;
import ca.pfv.spmf.algorithms.clustering.kmeans.AlgoKMeanPlusPlus;
import ca.pfv.spmf.patterns.cluster.ClusterWithMean;
import ca.pfv.spmf.patterns.cluster.DoubleArray;

/**
 *  Example of how to use the KMeans++ algorithm, in source code.
 */
public class MainTestKMeansPlusPlus_saveToMemory {
	
	public static void main(String []args) throws NumberFormatException, IOException{
		
		String input = fileToPath("inputDBScan2.txt");
		// we request 3 clusters
		int k=3;	
		
		// We specify that in the input file, double values on each line are separated by spaces
		String separator = " ";
		
		// Here we specify that we want to use the euclidian distance
		DistanceFunction distanceFunction = new DistanceEuclidian(); 
		// Alternative distance functions are also available such as:
//		DistanceFunction distanceFunction = new DistanceManathan(); 
//		DistanceFunction distanceFunction = new DistanceCosine(); 
//		DistanceFunction distanceFunction = new DistanceCorrelation(); 
//		DistanceFunction distanceFunction = new DistanceJaccard(); 
		
		// Apply the algorithm
		AlgoKMeanPlusPlus algoKMeans = new AlgoKMeanPlusPlus();  
		List<ClusterWithMean> clusters = algoKMeans.runAlgorithm(input, k, distanceFunction, separator);
		algoKMeans.printStatistics();
		
		// Print the clusters found by the algorithm
		// For each cluster:
		int i=0;
		for(ClusterWithMean cluster : clusters) {
			System.out.println("Cluster " + i++);
			// For each data point:
			for(DoubleArray dataPoint : cluster.getVectors()) {
				System.out.println("   " + dataPoint);
			}
		}
	}
	
	public static String fileToPath(String filename) throws UnsupportedEncodingException{
		URL url = MainTestKMeansPlusPlus_saveToMemory.class.getResource(filename);
		 return java.net.URLDecoder.decode(url.getPath(),"UTF-8");
	}
	
	
}
