package ca.pfv.spmf.gui.viewers.product_tdb_viewer;

import javax.swing.table.AbstractTableModel;

import ca.pfv.spmf.input.product_transaction_database.ProductTransaction;
import ca.pfv.spmf.input.product_transaction_database.ProductTransactionDatabase;
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
 * A JTable model for visualizing a transaction database with profit information (as used by erasable itemset mining algorithms such as VME) in SPMF format.
 * 
 * @author Philippe Fournier-Viger, 2024
 */
public class ProductTransactionTableModel extends AbstractTableModel {

	/** The database */
	private ProductTransactionDatabase database;

	/**
	 * Constructor
	 * 
	 * @param database the database
	 */
	public ProductTransactionTableModel(ProductTransactionDatabase database) {
		this.database = database;
	}

	/**
	 * Get the number of columns
	 * 
	 * @return the number of columns
	 */
	public int getColumnCount() {
		return database.getItems().size() + 2;
	}

	/**
	 * Get the number of rows
	 * 
	 * @return the number of rows
	 */
	public int getRowCount() {
		return database.size();
	}

	/**
	 * Get the value at a given position in the table
	 * 
	 * @param row    the row number
	 * @param column the column number
	 * @return the value
	 */
	public Object getValueAt(int row, int column) {
		if (column == 0) {
			return "T" + row;
		} else if(column == database.getItems().size() +1){
			return database.getTransactions().get(row).getProfit();
		}else {
			ProductTransaction transaction = database.getTransactions().get(row);
			Integer item = database.getItems().get(column - 1);
			if (transaction.contains(item)) {
				return "Item " + item;
			} else {
				return "";
			}
		}
	}

	/**
	 * Get the name of a given column
	 * 
	 * @param column the column number
	 * @return the column name
	 */
	public String getColumnName(int column) {
		if (column == 0) {
			return "Transaction";
		} else if(column == database.getItems().size()+1){
			return "Profit";
		}else {
			return "Item " + database.getItems().get(column - 1);
		}
	}

	/**
	 * Get the database
	 * 
	 * @return the database
	 */
	public ProductTransactionDatabase getDatabase() {
		return database;
	}
}
