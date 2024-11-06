package ca.pfv.spmf.gui.viewers.utility_cost_tdb_viewer;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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
import javax.swing.event.TableModelListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.TableModel;

import ca.pfv.spmf.gui.Main;
import ca.pfv.spmf.gui.MainWindow;
import ca.pfv.spmf.gui.SortableJTable;
import ca.pfv.spmf.gui.preferences.PreferencesManager;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionPanel.Order;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionWindow;
import ca.pfv.spmf.input.cost_utility_transaction_database.CostUtilityTransactionDatabase;
import ca.pfv.spmf.input.cost_utility_transaction_database.ItemCost;
import ca.pfv.spmf.input.cost_utility_transaction_database.TransactionCost;
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
 * A tool to visualize a utility transaction database in SPMF format.
 * 
 * @author Philippe Fournier-Viger, 2024
 */
public class CostUtilityTransactionDatabaseViewer {

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
	public CostUtilityTransactionDatabaseViewer(boolean runAsStandaloneProgram, String filePath) {
		frame = new JFrame("SPMF Cost Utility Transaction Database Viewer " + Main.SPMF_VERSION);
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

		// Create a JButton object for the second button
		JButton button2 = new JButton("View item cost distribution");
		// Add an action listener to the button
		button2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				viewItemCostDistribution();
			}
		});
		button2.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/histogram.png")));

		// Create a JButton object for the third button
		JButton button3 = new JButton("View transaction utility distribution");
		// Add an action listener to the button
		button3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				viewTransactionUtilityDistribution();
			}
		});
		button3.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/histogram.png")));

		// Add the buttons to the panel using a FlowLayout manager
		buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
		buttonPanel.add(button1);
		buttonPanel.add(button3);
		buttonPanel.add(button2);
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
		// Create a new CostUtilityTransactionDatabase object
		CostUtilityTransactionDatabase db = new CostUtilityTransactionDatabase();
		try {
			// Load the file containing the utility transaction database
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
		TransactionTableModel model = new TransactionTableModel(db);
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

		// Initialize the sum of transaction lengths and utilities to zero
		int sumLength = 0;
		int sumUtility = 0;
		// Loop through the transactions in the database
		for (TransactionCost transaction : db.getTransactions()) {
			// Add the transaction length and utility to the sums
			sumLength += transaction.size();
			sumUtility += transaction.getTransactionUtility();
		}
		// Calculate the average transaction length by dividing the sum by the number of
		// transactions
		double averageLength = (double) sumLength / db.size();
		// Format the average to two decimal places
		String averageLengthString = String.format("%.2f", averageLength);
		// Calculate the average transaction utility by dividing the sum by the number
		// of
		// transactions
		double averageUtility = (double) sumUtility / db.size();
		// Format the average to two decimal places
		String averageUtilityString = String.format("%.2f", averageUtility);

		// Update the status label to show the new number of transactions and items
		statusLabel.setText("Size: " + fileSizeMBString + " MB | Transactions: " + db.size() + " | Items: "
				+ db.getAllItems().size() + " | Average transaction length: " + averageLengthString
				+ " | Average transaction utility: " + averageUtilityString);
		// Update the name label to show the new file name of the database
		nameLabel.setText("Database: " + filepath);
	}

	private void viewItemCostDistribution() {
		if (table.getModel() != null) {
			CostUtilityTransactionDatabase db = ((TransactionTableModel) table.getModel()).db;

			Map<Integer, String> mapItemToString = db.getMapItemToStringValues();

			// Find the maximum item
			int maxItem = db.getMaxItemID();

			// Prepare the data (utilities)
			int[] yValues = new int[maxItem + 1];
			for (TransactionCost transaction : db.getTransactions()) {
				for (ItemCost item : transaction.getItems()) {
					yValues[item.item] += item.cost;
				}
			}

			// Prepare the X values data
			int[] xValues = new int[maxItem + 1];
			for (int i = 0; i < maxItem + 1; i++) {
				xValues[i] = i;
			}

			///// Remove zero values ////////////////////////////33
			// SPECIAL CASE: Check if some item did not exist in the previous array
			// and create a new array to remove them.
			// This case only occurs if the input file has item that are not
			// consecutive and starting from 1. For example: fruithut_utility.txt
			int count = db.getAllItems().size();
			if (count != maxItem) {

				// Initialize new arrays to store the non-zero pairs
				int[] newXValues = new int[count];
				int[] newYValues = new int[count];

				// Keep track of the index for the new arrays
				int index = 0;

				// Loop over the original arrays
				for (int i = 0; i < maxItem + 1; i++) {
					// If the Y value is not zero, add the pair to the new arrays
					if (yValues[i] != 0) {
						newXValues[index] = xValues[i];
						newYValues[index] = yValues[i];
						index++;
					} else {
						if (mapItemToString.get(xValues[i]) != null) {
							System.out.println(xValues[i]);
						}
					}
				}
				xValues = newXValues;
				yValues = newYValues;
			}
			//////////////////////////////////////////////

			HistogramDistributionWindow frame2 = new HistogramDistributionWindow(false, yValues, xValues,
					"Item cost distribution", true, true, "Item", "Cost", mapItemToString, Order.ASCENDING_Y);
		}
	}

	// Define a method to view the transaction utility distribution using a
	// histogram window
	private void viewTransactionUtilityDistribution() {
		if (table.getModel() != null) {
			CostUtilityTransactionDatabase db = ((TransactionTableModel) table.getModel()).db;

			// Find the maximum utility
			int maxUtility = 0;
			for (TransactionCost transaction : db.getTransactions()) {
				int utility = transaction.getTransactionUtility();
				if (utility > maxUtility) {
					maxUtility = utility;
				}
			}

			// Prepare the data (counts)
			int[] yValues = new int[maxUtility + 1];
			for (TransactionCost transaction : db.getTransactions()) {
				int utility = transaction.getTransactionUtility();
				yValues[utility]++;
			}

			// Prepare the X values data
			int[] xValues = new int[maxUtility + 1];
			for (int i = 0; i < maxUtility + 1; i++) {
				xValues[i] = i;
			}

			HistogramDistributionWindow frame2 = new HistogramDistributionWindow(false, yValues, xValues,
					"Transaction utility frequency distribution", true, true, "Utility", "Count", null,
					Order.ASCENDING_X);
		}
	}

	/**
	 * View the distribution of transaction length using a histogram window
	 */
	private void viewTransactionLengthDistribution() {
		if (table.getModel() != null) {
			CostUtilityTransactionDatabase db = ((TransactionTableModel) table.getModel()).db;

			// Find the maximum size
			int maxSize = 0;
			for (TransactionCost transaction : db.getTransactions()) {
				int size = transaction.size();
				if (size > maxSize) {
					maxSize = size;
				}
			}

			// Prepare the data (utilities)
			int[] yValues = new int[maxSize + 1];
			for (TransactionCost transaction : db.getTransactions()) {
				int size = transaction.size();
				yValues[size] += 1;
			}

			// Prepare the X values data
			int[] xValues = new int[maxSize + 1];
			for (int i = 0; i < maxSize + 1; i++) {
				xValues[i] = i;
			}

			HistogramDistributionWindow frame2 = new HistogramDistributionWindow(false, yValues, xValues,
					"Transaction length distribution", true, true, "Length", "Count", null, Order.ASCENDING_X);
		}
	}

	/**
	 * The table model to display the utility transactions
	 */
	class TransactionTableModel implements TableModel {

		/** The CostUtilityTransactionDatabase object that holds the data **/
		CostUtilityTransactionDatabase db;

		/** The list of listeners for this table model */
		private List<TableModelListener> listeners;

		/**
		 * The constructor that takes a CostUtilityTransactionDatabase object as
		 * parameter
		 * 
		 * @param db a utility transaction database object
		 */
		public TransactionTableModel(CostUtilityTransactionDatabase db) {
			// Initialize the fields
			this.db = db;
			this.listeners = new ArrayList<TableModelListener>();
		}

		/**
		 * Get the number of rows in the table
		 * 
		 * @return number of rows
		 */
		public int getRowCount() {
			// Return the number of transactions in the database plus one
			return db.size() + 1;
		}

		/**
		 * Get the number of columns in the table
		 * 
		 * @return number of columns
		 */
		public int getColumnCount() {
			// Return the number of items in the database plus two
			return db.getAllItems().size() + 2;
		}

		/**
		 * Get the name of the column at the given index
		 * 
		 * @param columnIndex the column index
		 * @return the name
		 */
		public String getColumnName(int columnIndex) {
			// If the column index is zero, return "TID"
			if (columnIndex == 0) {
				return "Transaction";
			}
			// If the column index is equal to the number of items plus one, return "TU"
			if (columnIndex == db.getAllItems().size() + 1) {
				return "Utility";
			}
			// Otherwise, return the name of the item at the given index minus one
			// Assume that the items are sorted in ascending order
//			return "Item " + columnIndex;
			return getItemName(columnIndex, true);
		}

		/**
		 * Get the item name for a given column index
		 * 
		 * @param itemID the item
		 * @return the item name
		 */
		private String getItemName(int itemID, boolean forColumnName) {
			String itemName = db.getNameForItem(itemID);
			if (itemName != null) {
				if (forColumnName) {
					return itemName + " (" + itemID + ")";
				} else {
					return itemName;
				}
			} else {

				return "Item " + itemID;
			}
		}

		/**
		 * Get the class of the values in the column at the given index.
		 * 
		 * @param columnIndex the index
		 * @return the class
		 */
		public Class<?> getColumnClass(int columnIndex) {
			// If the column index is zero, return the class of Integer, since the TID is an
			// integer
			if (columnIndex == 0) {
				return Integer.class;
			}
			// If the column index is equal to the number of items plus one, return the
			// class of Integer, since the TU is an
			// integer
			if (columnIndex == db.getAllItems().size() + 1) {
				return Integer.class;
			}
			// Otherwise, check the row index of the last row
			int rowIndex = db.size();
			// If the row index is equal to the number of transactions, return the class of
			// Integer, since the utility is an integer
			if (rowIndex == db.size()) {
				return Integer.class;
			}
			// Otherwise, return the class of String, since the table will display item
			// names and utilities
			return String.class;
		}

		/**
		 * Get the value at the given row and column index
		 * 
		 * @param rowIndex    the row
		 * @param columnIndex the column
		 * @return the object
		 */
		public Object getValueAt(int rowIndex, int columnIndex) {
			// If the row index is equal to the number of transactions, return the utility
			// for
			// the column
			if (rowIndex == db.size()) {
				// If the column index is zero, return "Total utility:"
				if (columnIndex == 0) {
					return "Total cost:";
				}
				// If the column index is equal to the number of items plus one, return the
				// total utility of the database
				if (columnIndex == db.getAllItems().size() + 1) {
					return Long.toString(db.getTotalUtility());
				}
				// Otherwise, get the item at the given column index minus one
				// Assume that the items are sorted in ascending order
				int item = columnIndex;
				// Initialize the utility to zero
				int utility = 0;
				// Loop through the transactions in the database
				for (TransactionCost transaction : db.getTransactions()) {
					// Loop through the items in the transaction
					for (ItemCost ItemCost : transaction.getItems()) {
						// If the item matches, add the utility to the sum
						if (ItemCost.item == item) {
							utility += ItemCost.cost;
						}
					}
				}
				// Return the utility as an Integer object
				return Integer.toString(utility);
			}
			// Otherwise, use the modified code
			// If the column index is zero, return the row index
			if (columnIndex == 0) {
				return Integer.toString(rowIndex);
			}
			// If the column index is equal to the number of items plus one, return the
			// transaction utility
			if (columnIndex == db.getAllItems().size() + 1) {
				return Integer.toString(db.getTransactions().get(rowIndex).getTransactionUtility());
			}
			// Otherwise, get the transaction at the given row index
			TransactionCost transaction = db.getTransactions().get(rowIndex);
			// Get the item at the given column index minus one
			// Assume that the items are sorted in ascending order
			int item = columnIndex;
			// Return the item name and utility if the transaction contains the item, empty
			// string otherwise
			for (ItemCost ItemCost : transaction.getItems()) {
				if (ItemCost.item == item) {
//					return getItemName(columnIndex, false) + " (" + ItemCost.utility + ")";
					return "Cost: " + ItemCost.cost;
				}
			}
			return "";
		}

		/**
		 * Get whether the cell at the given row and column index is editable
		 * 
		 * @param rowIndex    the row
		 * @param columnIndex the column
		 * @return a boolean indicating if the cell is editable
		 */
		public boolean isCellEditable(int rowIndex, int columnIndex) {
			// Return false, since the table is not editable
			return false;
		}

		/**
		 * Set the value at the given row and column index
		 * 
		 * @param rowIndex    the row
		 * @param columnIndex the column
		 * @param aValue      the object
		 */
		public void setValueAt(Object aValue, int rowIndex, int columnIndex) {
			// Do nothing, since the table is not editable
		}

		/**
		 * Add a listener to this table model
		 * 
		 * @param l a TableModelListener object
		 */
		public void addTableModelListener(TableModelListener l) {
			// Add the listener to the list
			listeners.add(l);
		}

		/**
		 * Remove a listener from this table model
		 * 
		 * @param l a TableModelListener object
		 */
		public void removeTableModelListener(TableModelListener l) {
			// Remove the listener from the list
			listeners.remove(l);
		}
	}

}
