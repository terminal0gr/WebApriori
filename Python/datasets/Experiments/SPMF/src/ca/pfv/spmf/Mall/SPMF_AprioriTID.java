package ca.pfv.spmf.Mall;

import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;

import ca.pfv.spmf.algorithms.frequentpatterns.aprioriTID.AlgoAprioriTID;
import ca.pfv.spmf.input.transaction_database_list_integers.TransactionDatabase;

public class SPMF_AprioriTID {

    // --- Ο ΠΑΡΑΤΗΡΗΤΗΣ ΜΝΗΜΗΣ (Inner Class) ---
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
                    Thread.sleep(50); // Συχνός έλεγχος κάθε 50ms για ακρίβεια
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
        //String datasetName = "kosarak.dat";
        //Double minSup = 0.0226928834487203; // relative support
        //Double minSup = 0.00634443162741085; // relative support
        // 

        //Line arguments section
        if (arg.length >= 1) {
            datasetName=arg[0];
        }
        if (arg.length >= 2) {
            minSup=Double.parseDouble(arg[1]);
        }

        String outPutResultsfile, noPrefix;

        int lastDotIndex = datasetName.lastIndexOf('.');
        if (lastDotIndex != -1) { //found
            noPrefix = datasetName.substring(0, lastDotIndex); // Removes everything after the last '.'
        } else {
            noPrefix=datasetName;
        }

        String input =  "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;

        long heapSize = Runtime.getRuntime().totalMemory();  // Initial heap size
        long maxHeapSize = Runtime.getRuntime().maxMemory(); // Maximum heap size
        long freeMemory = Runtime.getRuntime().freeMemory(); // Free heap memory
        System.out.println("Initial Heap Size (Mbytes): " + heapSize/(1024*1024));
        System.out.println("Maximum Heap Size (bytes): " + maxHeapSize/(1024*1024));
        System.out.println("Free Heap Memory (bytes): " + freeMemory/(1024*1024));

        ////////////////////////////
        String algorithm="AprioriTID";
        AlgoAprioriTID algo = new AlgoAprioriTID();

        TransactionDatabase database = new TransactionDatabase();
		try {
			database.loadFile(input);
		} catch (IOException e) {
			e.printStackTrace();
		}


        outPutResultsfile="\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + Double.toString(minSup) + "_" + algorithm + "_SPMF.fim";

        // --- ΕΝΑΡΞΗ ΚΑΤΑΓΡΑΦΗΣ ---
        MemoryMonitor monitor = new MemoryMonitor();
        Thread monitorThread = new Thread(monitor);
        // ΚΙΝΗΣΗ 1: Ορισμός ως Daemon ώστε να μην "κρεμάει" το JVM αν σκάσει η Main
        monitorThread.setDaemon(true); 
        monitorThread.start();
        try {
            // Εκτέλεση αλγορίθμου
            algo.runAlgorithm(input, outPutResultsfile, minSup);
        } catch (OutOfMemoryError oom) {
            System.err.println("Σφάλμα: Η μνήμη εξαντλήθηκε κατά την εκτέλεση του αλγορίθμου!");
        } finally {
            // ΚΙΝΗΣΗ 2: Το finally εκτελείται ΠΑΝΤΑ, ακόμα και μετά από κρασάρισμα
            monitor.stop();
            // Χρησιμοποιούμε join με timeout (π.χ. 1 δευτερόλεπτο) για ασφάλεια
            try {
                monitorThread.join(1000); 
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
            double peakMemMB = monitor.getMaxMemoryInMB();
            System.out.println("===========================================");
            System.out.println("ΠΡΑΓΜΑΤΙΚΟ PEAK MEMORY: " + String.format("%.0f", peakMemMB) + " MB");
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

