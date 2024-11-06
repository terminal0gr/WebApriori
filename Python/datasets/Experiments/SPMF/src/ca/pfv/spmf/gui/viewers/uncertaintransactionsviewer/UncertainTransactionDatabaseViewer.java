package ca.pfv.spmf.gui.viewers.uncertaintransactionsviewer;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.net.URL;

import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.filechooser.FileNameExtensionFilter;

import ca.pfv.spmf.algorithms.frequentpatterns.uapriori.ItemsetUApriori;
import ca.pfv.spmf.algorithms.frequentpatterns.uapriori.UncertainTransactionDatabase;
import ca.pfv.spmf.gui.Main;
import ca.pfv.spmf.gui.MainWindow;
import ca.pfv.spmf.gui.SortableJTable;
import ca.pfv.spmf.gui.preferences.PreferencesManager;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionPanel.Order;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionWindow;
import ca.pfv.spmf.test.MainTestApriori_saveToFile;

/*
 * Copyright (c) 2024 Philippe Fournier-Viger
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
 * A tool to visualize an uncertain transaction database in SPMF format.
 * 
 * @author Philippe Fournier-Viger, 2024
 */
public class UncertainTransactionDatabaseViewer {

	/** The table */
	private JTable table;
	/** The scroll pane */
	private JScrollPane scrollPane;
	/** The status label */
	private JLabel statusLabel;
	/** The name label */
	private JLabel nameLabel;
	/** The frame */
	private JFrame frame;

	/**
	 * Constructor
	 * 
	 * @param runAsStandaloneProgram if true, this tool will be run in standalone
	 *                               mode (close the window will close the program).
	 *                               Otherwise not.
	 */
	public UncertainTransactionDatabaseViewer(boolean runAsStandaloneProgram, String filePath) {
		frame = new JFrame("SPMF Uncertain Transaction Database Viewer " + Main.SPMF_VERSION);
		if (runAsStandaloneProgram) {
			// Set the default close operation
			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		}

		table = new SortableJTable();

		table.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);

		scrollPane = new JScrollPane(table);

		// Set the horizontal scroll bar policy of the scroll pane to always show
		scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);

		// Add the scroll pane to the frame
		frame.add(scrollPane, BorderLayout.CENTER);

		JPanel statusPanel = new JPanel();
		statusPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
		statusLabel = new JLabel();
		statusPanel.add(statusLabel);

		// Create a JPanel object to hold the buttons
		JPanel buttonPanel = new JPanel();
		// Create a JButton object for the first button
		JButton button1 = new JButton("View transaction length distribution");
		// Add an action listener to the button
		button1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				viewTransactionLengthDistribution();
			}
		});
		button1.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/histogram.png")));

		// Add the buttons to the panel using a FlowLayout manager
		buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
		buttonPanel.add(button1);
		// Add the panel to the frame using the BorderLayout.SOUTH position
		frame.add(buttonPanel, BorderLayout.SOUTH);

		JPanel bottomPanel = new JPanel();
		bottomPanel.setLayout(new BoxLayout(bottomPanel, BoxLayout.Y_AXIS));
		frame.add(bottomPanel, BorderLayout.SOUTH);
		bottomPanel.add(statusPanel);
		bottomPanel.add(buttonPanel);

		JPanel topPanel = new JPanel();
		nameLabel = new JLabel();
		// Set the text of the label to show the file name of the database
		nameLabel.setText("Database: " + filePath);

		// Create a JButton object to load a database
		if (runAsStandaloneProgram) {
			JButton loadButton = new JButton("Load database");
			loadButton.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/Open24.gif")));

			// Add an action listener to the button
			loadButton.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					chooseAFile();
				}
			});
			// Add the button to the frame using the BorderLayout.EAST position
			topPanel.add(loadButton, BorderLayout.EAST);
		}
		topPanel.add(nameLabel);
		frame.add(topPanel, BorderLayout.NORTH);

		if (filePath != null) {
			openDatabaseFile(filePath);
		}

		// Set the size and location of the frame
		frame.setSize(800, 600);
		frame.setLocationRelativeTo(null);
		frame.pack();
		// Make the frame visible
		frame.setVisible(true);
	}

	/**
	 * Ask the user to choose a file.
	 */
	private void chooseAFile() {
		File path;
		// Get the last path used by the user, if there is one
		String previousPath = PreferencesManager.getInstance().getInputFilePath();
		if (previousPath == null) {
			// If there is no previous path (first time user),
			// show the files in the "examples" package of
			// the spmf distribution.
			URL main = MainTestApriori_saveToFile.class.getResource("MainTestApriori_saveToFile.class");
			if (!"file".equalsIgnoreCase(main.getProtocol())) {
				path = null;
			} else {
				path = new File(main.getPath());
			}
		} else {
			// Otherwise, the user used SPMF before, so
			// we show the last path that he used.
			path = new File(previousPath);
		}
		// Create a JFileChooser object to select a file
		JFileChooser fc = new JFileChooser(path);
		// Set the file filter to accept only text files
		fc.setFileFilter(new FileNameExtensionFilter("Text Files", "txt"));

		// Show the file chooser dialog and get the result
		int result = fc.showOpenDialog(frame);
		// If the user approved the file selection
		if (result == JFileChooser.APPROVE_OPTION) {
			// Get the selected file
			File file = fc.getSelectedFile();
			// Get the file path
			String filepath = file.getPath();
			openDatabaseFile(filepath);
		}
		// remember this folder for next time.
		if (fc.getSelectedFile() != null) {
			PreferencesManager.getInstance().setInputFilePath(fc.getSelectedFile().getParent());
		}
	}

	/**
	 * Open a database in the viewer
	 * 
	 * @param filepath the file path
	 */
	private void openDatabaseFile(String filepath) {
		// Create a new UncertainTransactionDatabase object
		UncertainTransactionDatabase db = new UncertainTransactionDatabase();
		try {
			// Load the file containing the uncertain transaction database
			db.loadFile(filepath);
		} catch (Exception ex) {
			// Get the exception message and the stack trace as a string
			String errorMessage = String.format("Error loading file. Reading error: %s%n", ex.getMessage());
			// Get the exception class name as a string
			String title = ex.getClass().getName();
			// Show a JDialog with the exception message and the stack trace, and set the
			// dialog title and the message type
			JOptionPane.showMessageDialog(frame, errorMessage, title, JOptionPane.ERROR_MESSAGE);
		}
		// Create a new TransactionTableModel object with the new database
		UncertainTransactionTableModel model = new UncertainTransactionTableModel(db);
		// Set the table model to the new model
		table.setModel(model);

		// Get the file object of the database
		File file = new File(filepath);
		// Get the file size in bytes
		long fileSize = file.length();
		// Convert the file size to megabytes
		double fileSizeMB = fileSize / (1024.0 * 1024.0);
		// Format the file size to two decimal places
		String fileSizeMBString = String.format("%.2f", fileSizeMB);

		// Initialize the sum of transaction lengths and probabilities to zero
		int sumLength = 0;
		// Loop through the transactions in the database
		for (ItemsetUApriori transaction : db.getTransactions()) {
			// Add the transaction length and probability to the sums
			sumLength += transaction.size();
		}
		// Calculate the average transaction length by dividing the sum by the number of
		// transactions
		double averageLength = (double) sumLength / db.size();
		// Format the average to two decimal places
		String averageLengthString = String.format("%.2f", averageLength);

		// Update the status label to show the new number of transactions and items
		statusLabel.setText("Size: " + fileSizeMBString + " MB | Transactions: " + db.size() + " | Items: "
				+ db.getAllItems().size() + " | Average transaction length: " + averageLengthString);
		// Update the name label to show the new file name of the database
		nameLabel.setText("Database: " + filepath);
	}

	/**
	 * A method to view the transaction length distribution using a histogram
	 * window.
	 */
	private void viewTransactionLengthDistribution() {
		if (table.getModel() != null) {
			UncertainTransactionDatabase db = ((UncertainTransactionTableModel) table.getModel()).db;

			// Find the maximum size
			int maxSize = 0;
			for (ItemsetUApriori transaction : db.getTransactions()) {
				int size = transaction.size();
				if (size > maxSize) {
					maxSize = size;
				}
			}

			// Prepare the data (probabilities)
			int[] yValues = new int[maxSize + 1];
			for (ItemsetUApriori transaction : db.getTransactions()) {
				int size = transaction.size();
				yValues[size] += 1;
			}

			// Prepare the X values data
			int[] xValues = new int[maxSize + 1];
			for (int i = 0; i < maxSize + 1; i++) {
				xValues[i] = i;
			}

			HistogramDistributionWindow frame2 = new HistogramDistributionWindow(false, yValues, xValues,
					"Transaction length distribution", true, true, "Length", "Probability", null, Order.ASCENDING_X);
		}
	}

}
