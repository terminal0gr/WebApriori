package ca.pfv.spmf.Mall;

import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;

import ca.pfv.spmf.algorithms.frequentpatterns.negFIN.AlgoNegFIN;

public class SPMF_negFIN {

    // --- memory monitor running on other thread (Inner Class) ---
    static class MemoryMonitor implements Runnable {
        private long maxMemoryUsed = 0;
        private volatile boolean running = true;
        private final MemoryMXBean memoryBean = ManagementFactory.getMemoryMXBean();

        @Override
        public void run() {
            while (running) {
                long currentUsedMemory = memoryBean.getHeapMemoryUsage().getUsed();
                if (currentUsedMemory > maxMemoryUsed) {
                    maxMemoryUsed = currentUsedMemory;
                }
                try {
                    Thread.sleep(100); // check every 100ms for accuracy
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
            }
        }

        public void stop() { running = false; }
        public double getMaxMemoryInMB() { return maxMemoryUsed / (1024.0 * 1024.0); }
    }

	public static void main(String [] arg) throws IOException{

        //Declaration section
        String datasetName = "chess.dat";
        Double minSup = 0.945244055068836; // relative support
        String separator = " ";

        //Line arguments section
        if (arg.length >= 1) { 
            datasetName=arg[0];
        }
        if (arg.length >= 2) {
            minSup=Double.parseDouble(arg[1]);
        }
        if (arg.length >= 3) {
            separator=arg[2];
        }

        String outPutResultsfile, noPrefix;

        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;
        String algorithm = "";

        long heapSize = Runtime.getRuntime().totalMemory();  // Initial heap size
        long maxHeapSize = Runtime.getRuntime().maxMemory(); // Maximum heap size
        long freeMemory = Runtime.getRuntime().freeMemory(); // Free heap memory
        System.out.println("Initial Heap Size (Mbytes): " + heapSize/(1024*1024));
        System.out.println("Maximum Heap Size (bytes): " + maxHeapSize/(1024*1024));
        System.out.println("Free Heap Memory (bytes): " + freeMemory/(1024*1024));

        ////////////////////////////
        algorithm="negFIN";
        AlgoNegFIN algo = new AlgoNegFIN();
        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.fim";
        algo.separator=separator;


        // --- Start a new thread for monitoring ---
        MemoryMonitor monitor = new MemoryMonitor();
        Thread monitorThread = new Thread(monitor);
        // Stage 1: Declare Daemon so not hang the JVM if Main crashes
        monitorThread.setDaemon(true); 
        monitorThread.start();
        try {        
		    algo.runAlgorithm(input, minSup, outPutResultsfile);
        } catch (OutOfMemoryError oom) {
            System.err.println("Error: out of memory while executing the algorithm " + algorithm);
        } finally {
            // Stage 2: In every case stop the monitoring thread
            monitor.stop();
            try {
                monitorThread.join(1000); 
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            double peakMemMB = monitor.getMaxMemoryInMB();
            System.out.println("===========================================");
            System.out.println("Real peak memory: " + String.format("%.0f", peakMemMB) + " MB");
            System.out.println("===========================================");
        }



		//algo.printStats();
        String pSN=algo.printStatsNew(algorithm, minSup);
        outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.json";
        // Write the JSON object to the file
        try (FileWriter file = new FileWriter(outPutResultsfile)) {
            file.write(pSN); 
            file.flush();
        } catch (IOException e) {
            e.printStackTrace();
        }        
        System.out.println(algorithm + " finished");

	}
}

