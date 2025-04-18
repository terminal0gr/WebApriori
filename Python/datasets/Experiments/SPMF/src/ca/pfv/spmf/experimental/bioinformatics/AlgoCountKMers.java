package ca.pfv.spmf.experimental.bioinformatics;

import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.Map.Entry;

import ca.pfv.spmf.tools.MemoryLogger;

/* Copyright (c) 2008-2024 Philippe Fournier-Viger
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
* 
* You should have received a copy of the GNU General Public License along with
* SPMF. If not, see <http://www.gnu.org/licenses/>.
*/
/**
 * Simple algorithm for counting the kmers in a Fasta dataset using a hashmap
* 
 * @author Philipe-Fournier-Viger
 **/
public class AlgoCountKMers {
	/** Number of kmers */
	int kmersCount = 0;
	
	/** object to write the output file (if the user wants to write to a file) */
	BufferedWriter writer = null;
	
	/** Runtime */
	protected long runtime; 

	/**  start time of last execution */
	protected double memoryUsage; 
	
	
	/**
	 * Run the algorithm
	 * @param dataset a FASTA dataset
	 * @param k the parameter k
	 * @param output the output file path
	 * @throws IOException if file error occurs
	 */
	public void runAlgorithm(FastaDataset dataset, int k, String output) throws IOException {
		
		runtime = System.currentTimeMillis();
		MemoryLogger.getInstance().reset();
		
		writer = new BufferedWriter(new FileWriter(output)); 
		
		// Do the counting
        Map<String, Integer> kmerFrequency = new HashMap<>();
        for (FastaSequenceEntry entry : dataset.getSequenceEntries()) {
            String sequence = entry.getSequence();
            for (int i = 0; i <= sequence.length() - k; i++) {
                String kmer = sequence.substring(i, i + k);
                kmerFrequency.put(kmer, kmerFrequency.getOrDefault(kmer, 0) + 1);
            }
        }
        MemoryLogger.getInstance().checkMemory();

        // Write to file
		for(Entry<String, Integer> kmerCountPair : kmerFrequency.entrySet()) {
			writer.write(kmerCountPair.getKey() + " #SUP: " + kmerCountPair.getValue());
			writer.newLine();
		}
        writer.close();
        MemoryLogger.getInstance().checkMemory();
        
        memoryUsage = MemoryLogger.getInstance().getMaxMemory();
        kmersCount = kmerFrequency.size();
        runtime = System.currentTimeMillis() - runtime;
	}

	/**
	 * Print statistics about the algorithm execution to System.out.
	 */
	public void printStats() {
		System.out.println("=============  BasicKmersCounter - STATS =============");
		System.out.println(" Kmers count : " + kmersCount);
		System.out.println(" Maximum memory usage : " + memoryUsage + " mb");
		System.out.println(" Total time ~ " + runtime + " ms");
		System.out.println("===================================================");
	}
}
