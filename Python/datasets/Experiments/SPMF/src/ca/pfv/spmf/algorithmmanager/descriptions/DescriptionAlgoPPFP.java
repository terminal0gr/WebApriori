package ca.pfv.spmf.algorithmmanager.descriptions;

import java.io.IOException;
/* This file is copyright (c) 2008-2022 Philippe Fournier-Viger
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

import ca.pfv.spmf.algorithmmanager.AlgorithmType;
import ca.pfv.spmf.algorithmmanager.DescriptionOfAlgorithm;
import ca.pfv.spmf.algorithmmanager.DescriptionOfParameter;
import ca.pfv.spmf.algorithms.frequentpatterns.ppfp.AlgoPPFP;

/**
 * This class describes the PPFP algorithm parameters. It is designed to be used
 * by the graphical and command line interface.
 * 
 * @see AlgoPPFP
 * @author Vincent M. Nofong (modified from Philippe Fournier-Viger's
 *         implementation of FPGrowth)
 */
public class DescriptionAlgoPPFP extends DescriptionOfAlgorithm {

	/**
	 * Default constructor
	 */
	public DescriptionAlgoPPFP() {
	}

	@Override
	public String getName() {
		return "PPFP";
	}

	@Override
	public String getAlgorithmCategory() {
		return "PERIODIC PATTERN MINING";
	}

	@Override
	public String getURLOfDocumentation() {
		return "http://www.philippe-fournier-viger.com/spmf/PPFP_periodic_patterns.php";
	} // 22819

	@Override
	public void runAlgorithm(String[] parameters, String inputFile, String outputFile) throws IOException {
		double minsup = getParamAsDouble(parameters[0]);
		double periodicity = getParamAsDouble(parameters[1]);
		double difference = getParamAsDouble(parameters[2]);
		AlgoPPFP algorithm = new AlgoPPFP();

		if (parameters.length >= 2 && "".equals(parameters[1]) == false) {
			algorithm.setMaximumPatternLength(getParamAsInteger(parameters[1]));
		}
		if (parameters.length >= 3 && "".equals(parameters[2]) == false) {
			algorithm.setMinimumPatternLength(getParamAsInteger(parameters[2]));
		}
		algorithm.runAlgorithm(inputFile, outputFile, minsup, periodicity, difference);
		algorithm.printStats();
	}

	@Override
	public DescriptionOfParameter[] getParametersDescription() {

		DescriptionOfParameter[] parameters = new DescriptionOfParameter[5];
		parameters[0] = new DescriptionOfParameter("Minsup (%)", "(e.g. 0.4 or 40%)", Double.class, false);
		parameters[1] = new DescriptionOfParameter("Periodicity ", "(e.g. 0.4 or 40)", Double.class, false);
		parameters[2] = new DescriptionOfParameter("Difference ", "(e.g. 0.4 or 40)", Double.class, false);
		parameters[3] = new DescriptionOfParameter("Max pattern length", "(e.g. 2 items)", Integer.class, true);
		parameters[4] = new DescriptionOfParameter("Min pattern length", "(e.g. 2 items)", Integer.class, true);
		return parameters;
	}

	@Override
	public String getImplementationAuthorNames() {
		return "Vincent M. Nofong modified from Philippe Fournier-Viger";
	}

	@Override
	public String[] getInputFileTypes() {
		return new String[] { "Database of instances", "Transaction database", "Simple transaction database" };
	}

	@Override
	public String[] getOutputFileTypes() {
		return new String[] { "Periodic patterns", "Periodic frequent patterns",
				"Productive Periodic frequent itemsets" };
	}
	
	@Override
	public AlgorithmType getAlgorithmType() {
		return AlgorithmType.DATA_MINING;
	}

}
