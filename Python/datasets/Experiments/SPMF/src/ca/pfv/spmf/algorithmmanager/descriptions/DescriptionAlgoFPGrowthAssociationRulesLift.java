package ca.pfv.spmf.algorithmmanager.descriptions;

import java.io.IOException;

import ca.pfv.spmf.algorithmmanager.AlgorithmType;
import ca.pfv.spmf.algorithmmanager.DescriptionOfAlgorithm;
import ca.pfv.spmf.algorithmmanager.DescriptionOfParameter;
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

/**
 * This class describes parameters of the algorithm for generating association rules 
 * with the FPGrowth algorithm with the lift measure. 
 * It is designed to be used by the graphical and command line interface.
 * 
 * @see AlgoFPGrowth, AlgoAgrawalFaster94
 * @author Philippe Fournier-Viger
 */
public class DescriptionAlgoFPGrowthAssociationRulesLift extends DescriptionOfAlgorithm {

	/**
	 * Default constructor
	 */
	public DescriptionAlgoFPGrowthAssociationRulesLift(){
	}

	@Override
	public String getName() {
		return "FPGrowth_association_rules_with_lift";
	}

	@Override
	public String getAlgorithmCategory() {
		return "ASSOCIATION RULE MINING";
	}

	@Override
	public String getURLOfDocumentation() {
		return "http://www.philippe-fournier-viger.com/spmf/AssociationRulesWithLift.php";
	}

	@Override
	public void runAlgorithm(String[] parameters, String inputFile, String outputFile) throws IOException {
		double minsup = getParamAsDouble(parameters[0]);
		double minconf = getParamAsDouble(parameters[1]);
		double minlift = getParamAsDouble(parameters[2]);
		
		int maxAntecedentLength = 400; 
		int maxConsequentLength = 400; 
		if (parameters.length >=4 && "".equals(parameters[3]) == false) {
			maxAntecedentLength= getParamAsInteger(parameters[3]);
		}
		if (parameters.length >=5 && "".equals(parameters[4]) == false) {
			maxConsequentLength= getParamAsInteger(parameters[4]);
		}

		ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth fpgrowth = new ca.pfv.spmf.algorithms.frequentpatterns.fpgrowth.AlgoFPGrowth();
		fpgrowth.setMaximumPatternLength(maxAntecedentLength + maxConsequentLength); 
		ca.pfv.spmf.patterns.itemset_array_integers_with_count.Itemsets patterns = fpgrowth
				.runAlgorithm(inputFile, null, minsup);
		fpgrowth.printStats();
		int databaseSize = fpgrowth.getDatabaseSize();

		// STEP 2: Generating all rules from the set of frequent itemsets
		// (based on Agrawal & Srikant, 94)
		ca.pfv.spmf.algorithms.associationrules.agrawal94_association_rules.AlgoAgrawalFaster94 algoAgrawal = new ca.pfv.spmf.algorithms.associationrules.agrawal94_association_rules.AlgoAgrawalFaster94();
		algoAgrawal.setMaxAntecedentLength(maxAntecedentLength);
		algoAgrawal.setMaxConsequentLength(maxConsequentLength);
		algoAgrawal.runAlgorithm(patterns, outputFile, databaseSize,
				minconf, minlift);
		algoAgrawal.printStats();
	}

	@Override
	public DescriptionOfParameter[] getParametersDescription() {
        
		DescriptionOfParameter[] parameters = new DescriptionOfParameter[5];
		parameters[0] = new DescriptionOfParameter("Minimum support (%)", "(e.g. 0.5 or 50%)", Double.class, false);
		parameters[1] = new DescriptionOfParameter("Minimum confidence (%)", "(e.g. 0.9 or 90%)", Double.class, false);
		parameters[2] = new DescriptionOfParameter("Minimum lift ", "(e.g. 1.0)", Double.class, false);
		parameters[3] = new DescriptionOfParameter("Max antecedent length", "(e.g. 2 items)", Integer.class, true);
		parameters[4] = new DescriptionOfParameter("Max consequent length", "(e.g. 2 items)", Integer.class, true);
		return parameters;
	}

	@Override
	public String getImplementationAuthorNames() {
		return "Philippe Fournier-Viger";
	}

	@Override
	public String[] getInputFileTypes() {
		return new String[]{"Database of instances","Transaction database", "Simple transaction database"};
	}

	@Override
	public String[] getOutputFileTypes() {
		return new String[]{"Patterns", "Association rules", "Association rules with lift"};
	}

	@Override
	public AlgorithmType getAlgorithmType() {
		return AlgorithmType.DATA_MINING;
	}
}
