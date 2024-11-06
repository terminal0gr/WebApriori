package ca.pfv.spmf.gui.viewers.arffviewer;

import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

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
import ca.pfv.spmf.input.arff.ARFFDatabase;
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
 * A tool to visualize an ARFF file. This tool is quite basic and do not provide much features.
 * It is designed to visualize simple ARFF files.
 * 
 * @author Philippe Fournier-Viger, 2024
 */
public class ARFFViewer {

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
	public ARFFViewer(boolean runAsStandaloneProgram, String filePath) {
		frame = new JFrame("SPMF ARFF Viewer " + Main.SPMF_VERSION);
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

		JPanel bottomPanel = new JPanel();
		bottomPanel.setLayout(new BoxLayout(bottomPanel, BoxLayout.Y_AXIS));
		frame.add(bottomPanel, BorderLayout.SOUTH);
		bottomPanel.add(statusPanel);

		JPanel topPanel = new JPanel();
		nameLabel = new JLabel();
		// Set the text of the label to show the file name of the database
		nameLabel.setText("Database: " + filePath);

		// Create a JButton object to load a database
		if(runAsStandaloneProgram) {
			JButton loadButton = new JButton("Load database");
			loadButton.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/Open24.gif")));
			// Add an action listener to the button
			loadButton.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
					chooseAFile();
				}
			});
			// Add the button to the frame using the BorderLayout.EAST position<
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
		// Set the file filter to accept only ARFF files
		fc.setFileFilter(new FileNameExtensionFilter("ARFF Files", "arff"));

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
		// Create a new ARFFDatabase object
		ARFFDatabase db = new ARFFDatabase();
		try {
			// Load the file containing the ARFF database
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
		// Create a new ARFFTableModel object with the new database
		ARFFTableModel model = new ARFFTableModel(db);
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

		// Update the status label to show the new number of transactions and items
		statusLabel.setText(
				"Size: " + fileSizeMBString + " MB | Records: " + db.size() + " | Attribute count: " + db.getAttributeNames().size());
		// Update the name label to show the new file name of the database
		nameLabel.setText("Database: " + filepath);
	}

	/**
	 * The table model to display the transactions
	 */
	class ARFFTableModel implements TableModel {

		/** The ARFFDatabase object that holds the data **/
		ARFFDatabase db;

		/** The list of listeners for this table model */
		private List<TableModelListener> listeners;

		/**
		 * The constructor that takes a ARFFDatabase object as parameter
		 * 
		 * @param db a ARFF database object
		 */
		public ARFFTableModel(ARFFDatabase db) {
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
			// Return the number of records in the database
			return db.size();
		}
		
		/**
		 * Get the number of columns in the table
		 * 
		 * @return number of columns
		 */
		public int getColumnCount() {
			// Return the number of items in the database plus one
			return db.getAttributeNames().size();
		}

		/**
		 * Get the name of the column at the given index
		 * 
		 * @param columnIndex the column index
		 * @return the name
		 */
		public String getColumnName(int columnIndex) {
//	
			return db.getAttributeNames().get(columnIndex);
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
			// Otherwise, check the row index of the last row
			int rowIndex = db.size();
			// If the row index is equal to the number of transactions, return the class of
			// Integer, since the count is an integer
			if (rowIndex == db.size()) {
				return Integer.class;
			}
			// Otherwise, return the class of String, since the table will display string
			// values
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
//			System.out.println(db.getRecords().get(rowIndex));
			return db.getRecords().get(rowIndex).get(columnIndex);
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
