package ca.pfv.spmf.algorithmmanager.descriptions;

import java.io.IOException;

import ca.pfv.spmf.algorithmmanager.AlgorithmType;
import ca.pfv.spmf.algorithmmanager.DescriptionOfAlgorithm;
import ca.pfv.spmf.algorithmmanager.DescriptionOfParameter;
import ca.pfv.spmf.algorithms.frequentpatterns.HUIM_BPSO.AlgoHUIM_BPSO;

/**
 * This class describes the HUIM-BPSO algorithm parameters. 
 * It is designed to be used by the graphical and command line interface.
 * 
 * @see AlgoHUIM_BPSO
 * @author Philippe Fournier-Viger
 */

public class DescriptionAlgoHUIM_BPSO extends DescriptionOfAlgorithm  {

	/**
	 * Default constructor
	 */
	public DescriptionAlgoHUIM_BPSO(){
	}

	@Override
	public String getName() {
		return "HUIM-BPSO";
	}

	@Override
	public String getAlgorithmCategory() {
		return "HIGH-UTILITY PATTERN MINING";
	}

	@Override
	public String getURLOfDocumentation() {
		return "http://www.philippe-fournier-viger.com/spmf/HUIM-BPSO.php";
	}

	@Override
	public void runAlgorithm(String[] parameters, String inputFile, String outputFile) throws IOException {
		int minutil = getParamAsInteger(parameters[0]);
		// Applying the algorithm
		AlgoHUIM_BPSO algo = new AlgoHUIM_BPSO();
		algo.runAlgorithm(inputFile, outputFile, minutil);
		algo.printStats();
	}

	@Override
	public DescriptionOfParameter[] getParametersDescription() {
        
		DescriptionOfParameter[] parameters = new DescriptionOfParameter[1];
		parameters[0] = new DescriptionOfParameter("Minimum utility", "(e.g. 40)", Integer.class, false);
		return parameters;
	}

	@Override
	public String getImplementationAuthorNames() {
		return "Jerry Chun-Wei Lin, Lu Yang, Philippe Fournier-Viger";
	}

	@Override
	public String[] getInputFileTypes() {
		return new String[]{"Database of instances","Transaction database", "Transaction database with utility values"};
	}

	@Override
	public String[] getOutputFileTypes() {
		return new String[]{"Patterns",  "High-utility patterns","High-utility itemsets"};
	}
	@Override
	public AlgorithmType getAlgorithmType() {
		return AlgorithmType.DATA_MINING;
	}
}
