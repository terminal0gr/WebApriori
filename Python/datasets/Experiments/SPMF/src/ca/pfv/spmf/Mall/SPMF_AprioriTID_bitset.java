package ca.pfv.spmf.Mall;

import java.io.FileWriter;
import java.io.IOException;
import java.lang.management.ManagementFactory;
import java.lang.management.MemoryMXBean;
import ca.pfv.spmf.algorithms.frequentpatterns.aprioriTID.AlgoAprioriTID_Bitset;
import ca.pfv.spmf.input.transaction_database_list_integers.TransactionDatabase;

public class SPMF_AprioriTID_bitset {

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

    public static void main(String [] arg) throws IOException {

        String datasetName = "kosarak.dat";
        Double minSup = 0.00634443162741085; 

        if (arg.length >= 1) datasetName = arg[0];
        if (arg.length >= 2) minSup = Double.parseDouble(arg[1]);

        String noPrefix = datasetName.contains(".") ? datasetName.substring(0, datasetName.lastIndexOf('.')) : datasetName;
        String input = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\datasets\\" + datasetName;

        System.out.println("Max Heap Allowed: " + Runtime.getRuntime().maxMemory()/(1024*1024) + " MB");

        AlgoAprioriTID_Bitset algo = new AlgoAprioriTID_Bitset();
        TransactionDatabase database = new TransactionDatabase();
        try {
            database.loadFile(input);
        } catch (IOException e) {
            e.printStackTrace();
        }

        String outPutResultsfile = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + minSup + "_AprioriTID_bitset_SPMF.fim";

        // --- ΕΝΑΡΞΗ ΚΑΤΑΓΡΑΦΗΣ ---
        MemoryMonitor monitor = new MemoryMonitor();
        Thread monitorThread = new Thread(monitor);
        monitorThread.start();

        // Εκτέλεση αλγορίθμου
        algo.runAlgorithm(input, outPutResultsfile, minSup);

        // --- ΛΗΞΗ ΚΑΤΑΓΡΑΦΗΣ ---
        monitor.stop();
        try {
            monitorThread.join(); // Περιμένουμε το thread να ολοκληρώσει
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        double peakMemMB = monitor.getMaxMemoryInMB();

        System.out.println("===========================================");
        System.out.println("ΠΡΑΓΜΑΤΙΚΟ PEAK MEMORY: " + String.format("%.0f", peakMemMB) + " MB");
        System.out.println("===========================================");

        String pSN = algo.printStatsNew("AprioriTID_bitset", minSup);
        
        // Αποθήκευση JSON
        String jsonPath = "\\xampp\\htdocs\\WebApriori\\Python\\datasets\\Experiments\\output\\" + noPrefix + "_" + minSup + "_AprioriTID_bitset_SPMF.json";
        try (FileWriter file = new FileWriter(jsonPath)) {
            file.write(pSN); 
            file.flush();
        }

        System.out.println("AprioriTID_bitset finished");
    }
}