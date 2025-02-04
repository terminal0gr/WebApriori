package ca.pfv.spmf.algorithmmanager.descriptions;

import java.io.IOException;

import ca.pfv.spmf.algorithmmanager.AlgorithmType;
import ca.pfv.spmf.algorithmmanager.DescriptionOfAlgorithm;
import ca.pfv.spmf.algorithmmanager.DescriptionOfParameter;
import ca.pfv.spmf.algorithms.sequentialpatterns.uhuspm.AlgoUHUSPM;
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
/* This file is part of the SPMF DATA MINING SOFTWARE
* (http://www.philippe-fournier-viger.com/spmf).
*
* SPMF is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
*
* SPMF is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
*
* You should have received a copy of the GNU General Public License
* along with SPMF.  If not, see <http://www.gnu.org/licenses/>.
*/
/**
 * This class describes the UHUSPM algorithm parameters. It is designed to be used by the graphical and command line interface.
 * 
 * @see AlgoUHUSPM
 * @author Philippe Fournier-Viger
 */
public class DescriptionAlgoUHUSPM extends DescriptionOfAlgorithm {

	/**
	 * Default constructor
	 */
	public DescriptionAlgoUHUSPM(){
	}

	@Override
	public String getName() {
		return "UHUSPM";
	}

	@Override
	public String getAlgorithmCategory() {
		return "HIGH-UTILITY PATTERN MINING";
	}

	@Override
	public String getURLOfDocumentation() {
		return "http://www.philippe-fournier-viger.com/spmf/UHUSPM.php";
	}

	@Override
	public void runAlgorithm(String[] parameters, String inputFile, String outputFile) throws IOException, ClassNotFoundException {
		// Run the algorithm
		AlgoUHUSPM algorithm = new AlgoUHUSPM();
		algorithm.runAlgorithm(inputFile, outputFile, getParamAsInteger(parameters[0]), getParamAsFloat(parameters[1]));
		algorithm.printStats();
	}

	@Override
	public DescriptionOfParameter[] getParametersDescription() {
        
		DescriptionOfParameter[] parameters = new DescriptionOfParameter[2];
		parameters[0] = new DescriptionOfParameter("Minimum utility", "(e.g. 20)", Integer.class, false);
		parameters[1] = new DescriptionOfParameter("Minimum probability", "(e.g. 1.4)", Float.class, false);
		return parameters;
	}

	@Override
	public String getImplementationAuthorNames() {
		return "Ting Li et al.";
	}

	@Override
	public String[] getInputFileTypes() {
		return new String[]{"Database of instances","Sequence database", "Sequence database with utility and probability values"};
	}

	@Override
	public String[] getOutputFileTypes() {
		return new String[]{"Patterns", "High-utility patterns","Sequential patterns", "High-utility patterns", "High-utility probability sequential patterns"};
	}
	
	@Override
	public AlgorithmType getAlgorithmType() {
		return AlgorithmType.DATA_MINING;
	}

	
}
