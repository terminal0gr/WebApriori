package ca.pfv.spmf.algorithmmanager.descriptions;

import java.io.IOException;

import ca.pfv.spmf.algorithmmanager.AlgorithmType;
import ca.pfv.spmf.algorithmmanager.DescriptionOfAlgorithm;
import ca.pfv.spmf.algorithmmanager.DescriptionOfParameter;
import ca.pfv.spmf.algorithms.clustering.distanceFunctions.DistanceFunction;
/* This file is copyright (c) 2008-2016 Philippe Fournier-Viger
* 
* This file is part of the SPMF DATA MINING SOFTWARE
* (http://www.philippe-fournier-viger.com/spmf).
* 
* SPMF is free software: you can redistribute it and/or modify it under the
* terms of the GNU General Public License as published by the Free Software
* Foundation, either version 3 of the License, or (at your option) any later
* version.
* 
* SPMF is distributed in the hope that it will be useful, but WITHOUT ANY
* WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
* A PARTICULAR PURPOSE. See the GNU General Public License for more details.
* You should have received a copy of the GNU General Public License along with
* SPMF. If not, see <http://www.gnu.org/licenses/>.
*/
import ca.pfv.spmf.algorithms.clustering.kmeans.AlgoKMeans;

/**
 * This class describes the KMeans algorithm parameters. 
 * It is designed to be used by the graphical and command line interface.
 * 
 * @see AlgoKMeans
 * @author Philippe Fournier-Viger
 */
public class DescriptionAlgoKMeans extends DescriptionOfAlgorithm {

	/**
	 * Default constructor
	 */
	public DescriptionAlgoKMeans(){
	}

	@Override
	public String getName() {
		return "KMeans";
	}

	@Override
	public String getAlgorithmCategory() {
		return "CLUSTERING";
	}

	@Override
	public String getURLOfDocumentation() {
		return "http://www.philippe-fournier-viger.com/spmf/KMeans.php";
	}

	@Override
	public void runAlgorithm(String[] parameters, String inputFile, String outputFile) throws IOException {
		int k = getParamAsInteger(parameters[0]);
		String distanceFunctionName = getParamAsString(parameters[1]);
		DistanceFunction distanceFunction 
			= DistanceFunction.getDistanceFunctionByName(distanceFunctionName);
		
		String separator;
		if (parameters.length > 2 && "".equals(parameters[2]) == false) {
			separator = getParamAsString(parameters[2]);
		}else{
			separator = " ";
		}
		
		// Apply the algorithm
		AlgoKMeans algoKMeans = new AlgoKMeans();
		algoKMeans.runAlgorithm(inputFile, k, distanceFunction, separator);
		algoKMeans.printStatistics();
		algoKMeans.saveToFile(outputFile);
	}

	@Override
	public DescriptionOfParameter[] getParametersDescription() {
        
		DescriptionOfParameter[] parameters = new DescriptionOfParameter[3];
		parameters[0] = new DescriptionOfParameter("k", "(e.g. 3)", Integer.class, false);
		parameters[1] = new DescriptionOfParameter("Distance function", "(e.g. euclidian, cosine...)", String.class, false);
		parameters[2] = new DescriptionOfParameter("separator", "(default: ' ')", String.class, true);
		return parameters;
	}

	@Override
	public String getImplementationAuthorNames() {
		return "Philippe Fournier-Viger";
	}

	@Override
	public String[] getInputFileTypes() {
		return new String[]{"Database of instances", "Database of double vectors"};
	}

	@Override
	public String[] getOutputFileTypes() {
		return new String[]{"Clusters"};
	}
	@Override
	public AlgorithmType getAlgorithmType() {
		return AlgorithmType.DATA_MINING;
	}
}
