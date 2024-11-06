package ca.pfv.spmf.gui.visuals.heatmap;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import ca.pfv.spmf.algorithms.clustering.distanceFunctions.DistanceEuclidian;
import ca.pfv.spmf.algorithms.clustering.distanceFunctions.DistanceFunction;
import ca.pfv.spmf.patterns.cluster.Cluster;
import ca.pfv.spmf.patterns.cluster.DoubleArray;

public class AlgoViewClusterHeatmap {

	public void runAlgorithm(List<Cluster> clusters, DistanceFunction function) {
	    List<DoubleArray> allInstances = new ArrayList<DoubleArray>();
	    for(Cluster cluster : clusters) {
	        allInstances.addAll(cluster.getVectors());
	    }
	    
	    int instanceCount = allInstances.size();
	    double[][] data = new double[instanceCount][instanceCount];
	    String[] rowNames = new String[instanceCount];
	    String[] columnNames = new String[instanceCount];

	    // Initialize row and column names
	    for (int i = 0; i < instanceCount; i++) {
	        rowNames[i] = "Inst. " + i;
	        columnNames[i] = "Inst." + i;
	    }

	    // Calculate distances between all pairs of instances
	    double max =0;
	    for (int i = 0; i < instanceCount; i++) {
	        for (int j = 0; j < instanceCount; j++) {
	            data[i][j] = function.calculateDistance(allInstances.get(i), allInstances.get(j));
	            if(data[i][j] > max) {
	            	max = data[i][j];
	            }
	        }
	    }
	    
	    // normalize
	    for (int i = 0; i < instanceCount; i++) {
	        for (int j = 0; j < instanceCount; j++) {
	            data[i][j] /= max;
	        }
	    }
	    

	    // Display the heatmap
	    new HeatMapViewer(true, data, rowNames, columnNames, true, true, true, true);
	}

	public static void main(String[] args) {
		List<Cluster> clusters = new ArrayList<>();

		// Example: Creating 3 clusters with random data for demonstration
		int numberOfClusters = 3;
		int numberOfInstances = 50; // Assuming each cluster will have 50 instances

		Random random = new Random();
		for (int i = 0; i < numberOfClusters; i++) {
			Cluster cluster = new Cluster();
			for (int j = 0; j < numberOfInstances; j++) {
				double[] instanceData = new double[1]; // Assuming 1D data for simplicity
				instanceData[0] = random.nextDouble(); // Random membership score
				DoubleArray instance = new DoubleArray(instanceData);
				cluster.addVector(instance);
			}
			clusters.add(cluster);
		}

		AlgoViewClusterHeatmap algoView = new AlgoViewClusterHeatmap();
		algoView.runAlgorithm(clusters, new DistanceEuclidian());
	}

}