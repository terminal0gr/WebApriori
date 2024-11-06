package ca.pfv.spmf.gui.viewers.sequencedb_viewer;

import java.awt.BorderLayout;
import java.awt.Component;
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
import javax.swing.table.TableCellRenderer;
import javax.swing.table.TableColumnModel;
import javax.swing.table.TableModel;

import ca.pfv.spmf.gui.Main;
import ca.pfv.spmf.gui.MainWindow;
import ca.pfv.spmf.gui.SortableJTable;
import ca.pfv.spmf.gui.preferences.PreferencesManager;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionPanel.Order;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionWindow;
import ca.pfv.spmf.input.sequence_database_array_integers.Sequence;
import ca.pfv.spmf.input.sequence_database_array_integers.SequenceDatabase;
import ca.pfv.spmf.test.MainTestApriori_saveToFile;

/*
 * Copyright (c) 2008-2022 Philippe Fournier-Viger
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
 * A tool to visualize a sequence database in SPMF format
 * 
 * @author Philippe Fournier-Viger, 2024
 */
public class SequenceDatabaseViewer extends JFrame {

	/** The table */
	private JTable table;
	/** The scroll pane */
	private JScrollPane scrollPane;
	/** The status label */
	private JLabel statusLabel;
	/** The name label */
	private JLabel nameLabel;

	/**
	 * Constructor
	 * 
	 * @param runAsStandaloneProgram if true, this tool will be run in standalone
	 *                               mode (close the window will close the program).
	 *                               Otherwise not.
	 */
	public SequenceDatabaseViewer(boolean runAsStandaloneProgram, String filePath) {
		// Initialize the frame title
		super("SPMF Sequence Database Viewer " + Main.SPMF_VERSION);
		if (runAsStandaloneProgram) {
			// Set the default close operation
			setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		}
		// Set the layout to border layout
		setLayout(new BorderLayout());

		// Create a JTable object to display the sequence database
		table = new SortableJTable();
		// Set the auto resize mode to off
		table.setAutoResizeMode(JTable.AUTO_RESIZE_OFF);

		// Create a JScrollPane object to wrap the table
		scrollPane = new JScrollPane(table);
		// Set the horizontal and vertical scroll bar policies to always show
		scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);
		scrollPane.setVerticalScrollBarPolicy(JScrollPane.VERTICAL_SCROLLBAR_ALWAYS);

		// Add the scroll pane to the frame using the BorderLayout.CENTER position
		add(scrollPane, BorderLayout.CENTER);

		JPanel statusPanel = new JPanel();
		statusPanel.setLayout(new FlowLayout(FlowLayout.LEFT));
		statusLabel = new JLabel();
		statusPanel.add(statusLabel);

		// Create a JPanel object to hold the buttons
		JPanel buttonPanel = new JPanel();
		// Create a JButton object for the first button
		JButton button1 = new JButton("View sequence length distribution");
		// Add an action listener to the button
		button1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				viewSequenceLengthDistribution();
			}
		});
		button1.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/histogram.png")));

		// Create a JButton object for the second button
		JButton button2 = new JButton("View item frequency distribution");
		// Add an action listener to the button
		button2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				viewItemFrequencyDistribution();
			}
		});
		button2.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/histogram.png")));

		// Add the buttons to the panel using a FlowLayout manager
		buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
		buttonPanel.add(button1);
		buttonPanel.add(button2);
		// Add the panel to the frame using the BorderLayout.SOUTH position
		add(buttonPanel, BorderLayout.SOUTH);

		JPanel bottomPanel = new JPanel();
		bottomPanel.setLayout(new BoxLayout(bottomPanel, BoxLayout.Y_AXIS));
		add(bottomPanel, BorderLayout.SOUTH);
		bottomPanel.add(statusPanel);
		bottomPanel.add(buttonPanel);

		// Create a JPanel object to hold the top components
		JPanel topPanel = new JPanel();
		// Create a JLabel object to display the database name
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
			// Add the button to the panel
			topPanel.add(loadButton);
		}
		// Add the name label to the panel
		topPanel.add(nameLabel);
		// Add the panel to the frame using the BorderLayout.NORTH position
		add(topPanel, BorderLayout.NORTH);

		if (filePath != null) {
			openDatabaseFile(filePath);
		}

		// Set the size and location of the frame
		setSize(800, 600);
		setLocationRelativeTo(null);
		pack();
		// Make the frame visible
		setVisible(true);
	}

	/**
	 * View the distribution of item frequency using a histogram window
	 */
	private void viewItemFrequencyDistribution() {
		if (table.getModel() != null) {
			SequenceDatabase db = ((SequenceTableModel) table.getModel()).db;
			Map<Integer, String> mapItemToString = db.getMapItemToStringValues();

			// Find the maximum size
			int maxItem = db.getMaxItemID();

			// Prepare the data (counts)
			int[] yValues = new int[maxItem + 1];
			for (Sequence sequence : db.getSequences()) {
				for (Integer[] itemset : sequence.getItemsets()) {
					for (int item : itemset) {
						yValues[item]++;
					}
				}
			}

			// Prepare the X values data
			int[] xValues = new int[maxItem + 1];
			for (int i = 0; i < maxItem + 1; i++) {
				xValues[i] = i;
			}

			HistogramDistributionWindow frame2 = new HistogramDistributionWindow(false, yValues, xValues,
					"Item frequency distribution", true, true, "Item", "Count", mapItemToString, Order.ASCENDING_Y);
		}
	}

	/**
	 * View the distribution of sequence length using a histogram window
	 */
	private void viewSequenceLengthDistribution() {
		if (table.getModel() != null) {
			SequenceDatabase db = ((SequenceTableModel) table.getModel()).db;

			// Find the maximum size
			int maxSize = 0;
			for (Sequence sequence : db.getSequences()) {
				int size = sequence.size();
				if (size > maxSize) {
					maxSize = size;
				}
			}

			// Prepare the data (counts)
			int[] yValues = new int[maxSize + 1];
			for (Sequence sequence : db.getSequences()) {
				int size = sequence.size();
				yValues[size]++;
			}

			// Prepare the X values data
			int[] xValues = new int[maxSize + 1];
			for (int i = 0; i < maxSize + 1; i++) {
				xValues[i] = i;
			}

			HistogramDistributionWindow frame2 = new HistogramDistributionWindow(false, yValues, xValues,
					"Sequence length frequency distribution", true, true, "Length", "Count", null, Order.ASCENDING_X);
		}

	}

	/**
	 * Resize columns of the JTable
	 * 
	 * @param table the table
	 */
	public void resizeColumnWidth(JTable table) {
		final TableColumnModel columnModel = table.getColumnModel();
		for (int column = 0; column < table.getColumnCount(); column++) {
			int width = 60; // Min width
			for (int row = 0; row < table.getRowCount(); row++) {
				TableCellRenderer renderer = table.getCellRenderer(row, column);
				Component comp = table.prepareRenderer(renderer, row, column);
				width = Math.max(comp.getPreferredSize().width + 1, width);
			}
			if (width > 300)
				width = 300;
			columnModel.getColumn(column).setPreferredWidth(width);
		}
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
		int result = fc.showOpenDialog(SequenceDatabaseViewer.this);
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
		// Create a new SequenceDatabase object
		SequenceDatabase db = new SequenceDatabase();
		try {
			// Load the file containing the sequence database
			db.loadFile(filepath);
		} catch (Exception ex) {
			// Get the exception message and the stack trace as a string
			String errorMessage = String.format("Error loading file. Reading error: %s%n", ex.getMessage());
			// Get the exception class name as a string
			String title = ex.getClass().getName();
			// Show a JDialog with the exception message and the stack trace, and set the
			// dialog title and the message type
			JOptionPane.showMessageDialog(this, errorMessage, title, JOptionPane.ERROR_MESSAGE);
		}
		// Create a new SequenceTableModel object with the new database
		SequenceTableModel model = new SequenceTableModel(db);
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

		// Initialize the sum of sequence lengths to zero
		int sum = 0;
		// Loop through the sequences in the database
		for (Sequence sequence : db.getSequences()) {
			// Add the sequence length to the sum
			sum += sequence.size();
		}
		// Calculate the average sequence length by dividing the sum by the number of
		// sequences
		double average = (double) sum / db.size();
		// Format the average to two decimal places
		String averageString = String.format("%.2f", average);

		// Update the status label to show the new number of sequences, the min and max
		// items, and the average sequence length
		statusLabel.setText("Size: " + fileSizeMBString + " MB | Sequences: " + db.size() + " | Min item: " + db.minItem
				+ " | Max item: " + db.maxItem + " | Average itemset count per sequence: " + averageString);
		// Update the name label to show the new file name of the database
		nameLabel.setText("Database: " + filepath);

		resizeColumnWidth(table);
	}

	/** The table model for this tool */
	public class SequenceTableModel implements TableModel {

		// The SequenceDatabase object that holds the data
		private SequenceDatabase db;
		// The list of listeners for this table model
		private List<TableModelListener> listeners;
		// The maximum number of itemsets in the database
		private int maxItemsets;

		// The constructor that takes a SequenceDatabase object as a parameter
		public SequenceTableModel(SequenceDatabase db) {
			// Initialize the fields
			this.db = db;
			this.listeners = new ArrayList<TableModelListener>();
			// Find the maximum number of itemsets in the database
			maxItemsets = 0;
			for (Sequence sequence : db.getSequences()) {
				if (sequence.size() > maxItemsets) {
					maxItemsets = sequence.size();
				}
			}
		}

		// The method that returns the number of rows in the table
		public int getRowCount() {
			// Return the number of sequences in the database
			return db.size();
		}

		// The method that returns the number of columns in the table
		public int getColumnCount() {
			// Return the maximum number of itemsets in the database plus one
			return maxItemsets + 1;
		}

		// The method that returns the name of the column at the given index
		public String getColumnName(int columnIndex) {
			// If the column index is zero, return "SID"
			if (columnIndex == 0) {
				return "Sequence ID";
			}
			// Otherwise, return the name of the itemset at the given index minus one
			return "Itemset " + (columnIndex - 1);
		}

		// The method that returns the class of the values in the column at the given
		// index
		public Class<?> getColumnClass(int columnIndex) {
			// If the column index is zero, return the class of Integer, since the SID is an
			// integer
			if (columnIndex == 0) {
				return Integer.class;
			}
			// Otherwise, return the class of String, since the table will display itemset
			// values or null values
			return String.class;
		}

		// The method that returns the value at the given row and column index
		public Object getValueAt(int rowIndex, int columnIndex) {
			// If the column index is zero, return the row index
			if (columnIndex == 0) {
				return rowIndex;
			}
			// Otherwise, get the sequence at the given row index
			Sequence sequence = db.getSequences().get(rowIndex);
			// Check if the sequence has an itemset at the given column index minus one
			if (columnIndex <= sequence.size()) {
				// If yes, get the itemset at the given column index minus one
				Integer[] itemset = sequence.get(columnIndex - 1);
				// Return the itemset as a string
				return asString(itemset);
			} else {
				// If no, return null
				return null;
			}
		}

		/**
		 * Get a string representation of an itemset
		 * 
		 * @param itemset an itemset
		 * @return the String
		 */
		private String asString(Integer[] itemset) {
			StringBuilder builder = new StringBuilder();
//			builder.append('{');
			for (int i = 0; i < itemset.length; i++) {
				String itemName = getItemName(itemset[i]);
				builder.append(itemName);
				if (i != itemset.length - 1) {
					builder.append(", ");
				}
			}
//			builder.append('}');
			return builder.toString();
		}

		// The method that returns whether the cell at the given row and column index is
		// editable
		public boolean isCellEditable(int rowIndex, int columnIndex) {
			// Return false, since the table is not editable
			return false;
		}

		/**
		 * Get the item name for a given column index
		 * 
		 * @param itemID the item
		 * @return the item name
		 */
		private String getItemName(int itemID) {
			String itemName = db.getNameForItem(itemID);
			if (itemName != null) {
				return itemName;
			} else {

				return "Item " + itemID;
			}
		}

		// The method that sets the value at the given row and column index
		public void setValueAt(Object aValue, int rowIndex, int columnIndex) {
			// Do nothing, since the table is not editable
		}

		// The method that adds a listener to this table model
		public void addTableModelListener(TableModelListener l) {
			// Add the listener to the list
			listeners.add(l);
		}

		// The method that removes a listener from this table model
		public void removeTableModelListener(TableModelListener l) {
			// Remove the listener from the list
			listeners.remove(l);
		}
	}

}
