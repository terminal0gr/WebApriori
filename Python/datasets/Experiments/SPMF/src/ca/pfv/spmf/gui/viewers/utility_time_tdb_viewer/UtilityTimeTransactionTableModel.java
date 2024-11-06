package ca.pfv.spmf.gui.viewers.utility_time_tdb_viewer;

import java.util.ArrayList;
import java.util.List;

import javax.swing.event.TableModelListener;
import javax.swing.table.TableModel;

import ca.pfv.spmf.input.utility_transaction_database.ItemUtility;
import ca.pfv.spmf.input.utility_transaction_database_with_time.TransactionTimeUtility;
import ca.pfv.spmf.input.utility_transaction_database_with_time.UtilityTimeTransactionDatabase;

/**
	 * The table model to display the utility transactions
	 */
	class UtilityTimeTransactionTableModel implements TableModel {

		/** The UtilityTimeTransactionDatabase object that holds the data **/
		UtilityTimeTransactionDatabase db;

		/** The list of listeners for this table model */
		private List<TableModelListener> listeners;

		/**
		 * Type of temporal information used in the input file (timestamps or period
		 * information)
		 */
		TypeOfTime typeOfTime;

		/**
		 * The constructor that takes a UtilityTimeTransactionDatabase object as
		 * parameter
		 * 
		 * @param db a utility transaction database object
		 */
		public UtilityTimeTransactionTableModel(UtilityTimeTransactionDatabase db, TypeOfTime typeOfTime) {
			// Initialize the fields
			this.db = db;
			this.listeners = new ArrayList<TableModelListener>();
			this.typeOfTime = typeOfTime;
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
			return db.getAllItems().size() + 3;
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
			if (columnIndex == 1) {
				if (TypeOfTime.TIMESTAMP.equals(typeOfTime)) {
					return "Timestamp";
				} else {
					return "Period";
				}
			}
			// If the column index is equal to the number of items plus one, return "TU"
			if (columnIndex == db.getAllItems().size() + 2) {
				return "Sum (TU)";
			}

			// Otherwise, return the name of the item at the given index minus one
			// Assume that the items are sorted in ascending order
//			return "Item " + columnIndex;
			return getItemName(columnIndex - 1, true);
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
					return "Total utility:";
				}
				// If the column index is 1, return the timestamp
				if (columnIndex == 1) {
					return "";
				}
				// If the column index is equal to the number of items plus one, return the
				// total utility of the database
				if (columnIndex == db.getAllItems().size() + 2) {
					return Long.toString(db.getTotalUtility());
				}
				// Otherwise, get the item at the given column index minus one
				// Assume that the items are sorted in ascending order
				int item = columnIndex - 1;
				// Initialize the utility to zero
				int utility = 0;
				// Loop through the transactions in the database
				for (TransactionTimeUtility transaction : db.getTransactions()) {
					// Loop through the items in the transaction
					for (ItemUtility itemUtility : transaction.getItems()) {
						// If the item matches, add the utility to the sum
						if (itemUtility.item == item) {
							utility += itemUtility.utility;
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
			if (columnIndex == 1) {
				return Integer.toString(db.getTransactions().get(rowIndex).getTimeStamp());
			}

			// If the column index is equal to the number of items plus one, return the
			// transaction utility
			if (columnIndex == db.getAllItems().size() + 2) {
				return Integer.toString(db.getTransactions().get(rowIndex).getTransactionUtility());
			}
			// Otherwise, get the transaction at the given row index
			TransactionTimeUtility transaction = db.getTransactions().get(rowIndex);
			// Get the item at the given column index minus one
			// Assume that the items are sorted in ascending order
			int item = columnIndex - 1;
			// Return the item name and utility if the transaction contains the item, empty
			// string otherwise
			for (ItemUtility itemUtility : transaction.getItems()) {
				if (itemUtility.item == item) {
//					return getItemName(columnIndex, false) + " (" + itemUtility.utility + ")";
					return "Utility: " + itemUtility.utility;
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