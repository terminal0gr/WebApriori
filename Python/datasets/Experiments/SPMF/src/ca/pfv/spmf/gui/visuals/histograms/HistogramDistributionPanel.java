package ca.pfv.spmf.gui.visuals.histograms;

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
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.PrintWriter;
import java.net.URL;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import javax.imageio.ImageIO;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

import ca.pfv.spmf.gui.preferences.PreferencesManager;
import ca.pfv.spmf.test.MainTestApriori_saveToFile;

/**
 * A panel displaying a frequency histogram
 * 
 * @author Philippe Fournier-Viger, 2024
 */
public class HistogramDistributionPanel extends JPanel {

	/** The minimum bar width to display labels */
	private static final int MINIMUM_BAR_WIDTH__TO_DISPLAY_LABELS = 15;

	/** default serial UID */
	private static final long serialVersionUID = 1L;

	/** The x axis name */
	private String xAxisName = "Length";

	/** The y axis name */
	private String yAxisName = "Count";

	/** The values for the y axis */
	private int[] yValues;

	/** The values for the x axis */
	private int[] xLabels;

	/** The maximum value on the X axis */
	private int maxX;

	/** The maximum value on the Y axis */
	private int maxY;

	/** The scaling factor */
	private double scaleFactor;
	
	/** Selected order */
	private Order selectedOrder = null;

	/**
	 * A boolean that indicate if labels for each bar should be displayed on the X
	 * axis
	 */
	private boolean showBarLabels;

	/**
	 * A boolean that indicate if values for each bar should be displayed above them
	 */
	private boolean showBarValues;

	/** The default margin around the chart */
	final int MARGIN = 50;

	/** The title of the histogram */
	private String title;

	/** The bar width for this histogram **/
	private int barWidth = 2;
	
	/** The different possible orders for displaying values of the X axis*/
	public enum Order {ASCENDING_Y, DESCENDING_Y, ASCENDING_X, DESCENDING_X;
	}

	/**
	 * A map that assign strings to values on the x axis. It can be set to null if
	 * no strings are provided
	 */
	private Map<Integer, String> mapXValuesToString;

	/**
	 * Constructor
	 * 
	 * @param yValues         the values for the Y axis
	 * @param xLabels         the corresponding values for the X axis
	 * @param title           the title of the chart
	 * @param showBarLabels   A boolean that indicate if labels for each bar should
	 *                        be displayed on the X axis
	 * @param showBarValues   A boolean that indicate if values for each bar should
	 *                        be displayed above them
	 * @param xAxisName       The x axis name
	 * @param yAxisName       The y axis name
	 * @param mapItemToString A map that associate String to values on the X axis
	 * @param order			The order to be used for sorting values of the X axis.
	 */
	public HistogramDistributionPanel(int[] yValues, int[] xLabels, String title, boolean showBarLabels,
			boolean showBarValues, String xAxisName, String yAxisName, Map<Integer, String> mapXValuesToString, Order order) {
		this.mapXValuesToString = mapXValuesToString;
		initializeHistogram(yValues, xLabels, title, showBarLabels, showBarValues, xAxisName, yAxisName, order);
	}

	/**
	 * Initialize the histogram panel
	 * 
	 * @param yValues       the values for the Y axis
	 * @param xLabels       the corresponding values for the X axis
	 * @param title         the title of the chart
	 * @param showBarLabels A boolean that indicate if labels for each bar should be
	 *                      displayed on the X axis
	 * @param showBarValues A boolean that indicate if values for each bar should be
	 *                      displayed above them
	 * @param xAxisName     The x axis name
	 * @param yAxisName     The y axis name
	 * @param order			The order to be used for sorting values of the X axis.
	 */
	private void initializeHistogram(int[] yValues, int[] xLabels, String title, boolean showBarLabels,
			boolean showBarValues, String xAxisName, String yAxisName, Order order) {
		// Initialize the values, labels, and title
		this.yValues = yValues;
		this.xLabels = xLabels;
		this.title = title;
		this.showBarLabels = showBarLabels;
		this.showBarValues = showBarValues;
		this.xAxisName = xAxisName;
		this.yAxisName = yAxisName;

		// Find the maximum value in the X and Y arrays
		maxY = max(yValues);
		setSortOrder(order);
		maxX = max(xLabels);

		setBackground(Color.WHITE);

		// Set the bar width automatically
		if (xLabels.length < 600) {
			barWidth = (int) (600d / xLabels.length);
		}

		setToolTipText("");

		this.setPreferredSize(new Dimension(600, 50));
	}

	/**
	 * Find the maximum value in an array ot integers
	 * 
	 * @param array the array
	 * @return the maximum value
	 */
	private int max(int[] array) {
		int max = array[0];
		for (int i = 1; i < array.length; i++) {
			if (array[i] > max) {
				max = array[i];
			}
		}
		return max;
	}

	/**
	 * Method that draw the histogram
	 * 
	 * @param g the graphic object for drawing.
	 */
	@Override
	public void paintComponent(Graphics g) {
		// Call the superclass method
		super.paintComponent(g);

		// Calculate the scale factor based on the maximum value and the panel height
		scaleFactor = (double) (getHeight() - (MARGIN * 2)) / maxY;

		// Set the font and color
		g.setFont(new Font("Arial", Font.PLAIN, 10));
		g.setColor(Color.BLACK);

		// Calculate the total width of the histogram based on the number of bars and
		// the minimum bar width
		int histogramWidth = yValues.length * getBarWidth();

		// Draw the x-axis and the y-axis

		// Use the histogram width instead of the panel width when drawing the X axis
		// line
		g.drawLine(50, getHeight() - MARGIN, 50 + histogramWidth, getHeight() - MARGIN);
		g.drawLine(50, MARGIN, 50, getHeight() - MARGIN);

		// Draw the bars and the labels
		for (int i = 0; i < yValues.length; i++) {
			// Calculate the bar height
			int barHeight = (int) (yValues[i] * scaleFactor);

			// Draw the bar with a different color for each value
			g.setColor(new Color((i * 50) % 256, (i * 100) % 256, (i * 150) % 256));
			g.fillRect(50 + i * getBarWidth(), getHeight() - MARGIN - barHeight, getBarWidth(), barHeight);

			g.setColor(Color.BLACK);
			// Draw the label below the bar
			boolean showBarsLabelsEffective = (showBarLabels && barWidth >= MINIMUM_BAR_WIDTH__TO_DISPLAY_LABELS);
//			System.out.println(showBarLabels + " " + showBarsLabelsEffective);
			if (showBarsLabelsEffective) {
				String text = getXValueAsString(i);
				g.drawString(text, 50 + i * getBarWidth() + getBarWidth() / 2 - 5, getHeight() - MARGIN + 10);
			}

			// Draw the value above the bar
			boolean showBarsValuesIsEffective = (showBarValues && barWidth >= MINIMUM_BAR_WIDTH__TO_DISPLAY_LABELS);
			if (showBarsValuesIsEffective) { // && yValues[i] > 0)
				g.drawString(String.valueOf(yValues[i]), 50 + i * getBarWidth() + getBarWidth() / 2 - 5,
						getHeight() - MARGIN - barHeight);
			}
		}

		g.setFont(new Font("Arial", Font.BOLD, 12));
		// Draw the maximum value at the end of the X axis and the Y axis
		g.drawString(String.valueOf(maxY), 40, MARGIN);
		g.drawString(yAxisName, 40, MARGIN - 12);
		
		if(Order.DESCENDING_X.equals(selectedOrder) ||  Order.ASCENDING_X.equals(selectedOrder)) {
			g.drawString(String.valueOf(maxX), (MARGIN) + histogramWidth - 5, getHeight() - MARGIN + 10);
			g.drawString(xAxisName, MARGIN + histogramWidth - 30, getHeight() - MARGIN + 22);
		}

		// Draw the value 0 at the intersection of both axes
		g.drawString("0", 40, getHeight() - MARGIN + 10);

		// Draw the title of the histogram
		// Get the font metrics of the current font
		FontMetrics fm = g.getFontMetrics();
		// Get the width of the title string
		int titleWidth = fm.stringWidth(title);
		// Calculate the x coordinate of the title string
		int titleX = getWidth() / 2 - titleWidth / 2;
		g.setFont(new Font("Arial", Font.BOLD, 16));
		g.drawString(title, titleX, 20);
	}

	/**
	 * Get a string representation of a given X value
	 * @param i the position of the X values in the array of X values
	 * @return the string representation
	 */
	private String getXValueAsString(int i) {
		int value = xLabels[i];
		if (mapXValuesToString == null) {
			return Integer.toString(value);
		}
		String name = mapXValuesToString.get(value);
		if (name != null) {
			return name;
		}
		return Integer.toString(value);
	}

	/**
	 * The method that sets the preferred size of the histogram JPanel
	 * 
	 * @param preferredSize a Dimension object indicating the preferred size
	 */
	@Override
	public void setPreferredSize(Dimension preferredSize) {
		// Calculate the total width of the histogram based on the number of bars and
		// the minimum bar width
		int histogramWidth = yValues.length * getBarWidth();

		// Set the preferred size of the histogram JPanel to the calculated width and
		// the same height as before
		super.setPreferredSize(new Dimension(histogramWidth + MARGIN * 2, getHeight()));
	}

	/**
	 * Exports the histogram as an image file (PNG)
	 * 
	 * @param fileName the file path for the image file
	 */
	public void exportAsImage(String fileName) {

		// ask the user to choose the filename and path
		String outputFilePath = null;
		try {
			File path;
			// Get the last path used by the user, if there is one
			String previousPath = PreferencesManager.getInstance().getOutputFilePath();
			// If there is no previous path (first time user),
			// show the files in the "examples" package of
			// the spmf distribution.
			if (previousPath == null) {
				URL main = MainTestApriori_saveToFile.class.getResource("MainTestApriori_saveToFile.class");
				if (!"file".equalsIgnoreCase(main.getProtocol())) {
					path = null;
				} else {
					path = new File(main.getPath());
				}
			} else {
				// Otherwise, use the last path used by the user.
				path = new File(previousPath);
			}

			// ASK THE USER TO CHOOSE A FILE
			final JFileChooser fc;
			if (path != null) {
				fc = new JFileChooser(path.getAbsolutePath());
			} else {
				fc = new JFileChooser();
			}
			int returnVal = fc.showSaveDialog(this);

			// If the user chose a file
			if (returnVal == JFileChooser.APPROVE_OPTION) {
				File file = fc.getSelectedFile();
				outputFilePath = file.getPath(); // save the file path
				// save the path of this folder for next time.
				if (fc.getSelectedFile() != null) {
					PreferencesManager.getInstance().setOutputFilePath(fc.getSelectedFile().getParent());
				}
			} else {
				// the user did not choose so we return
				return;
			}

		} catch (Exception e) {
			JOptionPane.showMessageDialog(null,
					"An error occured while opening the save plot dialog. ERROR MESSAGE = " + e.toString(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}

		try {
			// add the .png extension
			if (outputFilePath.endsWith("png") == false) {
				outputFilePath = outputFilePath + ".png";
			}
			// Create a BufferedImage object with the same size as the panel
			BufferedImage image = new BufferedImage(getWidth(), getHeight(), BufferedImage.TYPE_INT_RGB);

			// Get the Graphics object from the image
			Graphics g = image.getGraphics();
			// Paint the histogram on the image
			paint(g);

			// Create a File object with the given file name
			File file = new File(outputFilePath);

			// Write the image to the file as PNG format
			ImageIO.write(image, "png", file);

		} catch (Exception e) {
			JOptionPane.showMessageDialog(null,
					"An error occured while attempting to save the plot. ERROR MESSAGE = " + e.toString(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}
	}

	/**
	 * The method that exports the histogram as a CSV file
	 * 
	 * @param fileName the file path for the CSV file
	 */
	public void exportAsCSV(String fileName) {

		// ask the user to choose the filename and path
		String outputFilePath = null;
		try {
			File path;
			// Get the last path used by the user, if there is one
			String previousPath = PreferencesManager.getInstance().getOutputFilePath();
			// If there is no previous path (first time user),
			// show the files in the "examples" package of
			// the spmf distribution.
			if (previousPath == null) {
				URL main = MainTestApriori_saveToFile.class.getResource("MainTestApriori_saveToFile.class");
				if (!"file".equalsIgnoreCase(main.getProtocol())) {
					path = null;
				} else {
					path = new File(main.getPath());
				}
			} else {
				// Otherwise, use the last path used by the user.
				path = new File(previousPath);
			}

			// ASK THE USER TO CHOOSE A FILE
			final JFileChooser fc;
			if (path != null) {
				fc = new JFileChooser(path.getAbsolutePath());
			} else {
				fc = new JFileChooser();
			}
			int returnVal = fc.showSaveDialog(this);

			// If the user chose a file
			if (returnVal == JFileChooser.APPROVE_OPTION) {
				File file = fc.getSelectedFile();
				outputFilePath = file.getPath(); // save the file path
				// save the path of this folder for next time.
				if (fc.getSelectedFile() != null) {
					PreferencesManager.getInstance().setOutputFilePath(fc.getSelectedFile().getParent());
				}
			} else {
				// the user did not choose so we return
				return;
			}

		} catch (Exception e) {
			JOptionPane.showMessageDialog(null,
					"An error occured while opening the save plot dialog. ERROR MESSAGE = " + e.toString(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}

		try {
			// add the .csv extension
			if (outputFilePath.endsWith("csv") == false) {
				outputFilePath = outputFilePath + ".csv";
			}
			// Create a File object with the given file name
			File file = new File(outputFilePath);

			// Create a PrintWriter object to write to the file
			PrintWriter pw = new PrintWriter(file);

			// Write the title of the histogram as the first line of the file, followed by a
			// newline character
			pw.println(title + "\n");

			// Write the labels and values of the histogram as comma-separated values, one
			// pair per line, followed by a newline character
			for (int i = 0; i < yValues.length; i++) {
				pw.println(xLabels[i] + "," + yValues[i]);
			}
			// Close the PrintWriter object
			pw.close();

		} catch (Exception e) {
			JOptionPane.showMessageDialog(null,
					"An error occured while attempting to save the plot. ERROR MESSAGE = " + e.toString(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}
	}

	/**
	 * A constructor that takes data records and an index i
	 * 
	 * @param data          a list of data records
	 * @param width         the width of the panel
	 * @param height        the height of the panel
	 * @param index         the attribute of interest in the list of data records
	 * @param title         the title of the histogram * @param showBarLabels A
	 *                      boolean that indicate if labels for each bar should be
	 *                      displayed on the X axis
	 * @param showBarValues A boolean that indicate if values for each bar should be
	 *                      displayed above them
	 * @param xAxisName     The x axis name
	 * @param yAxisName     The y axis name
	 * @param order			The order to be used for sorting values of the X axis.
	 */
	public HistogramDistributionPanel(Vector<List<Object>> data, int width, int height, int index, String title,
			boolean showBarLabels, boolean showBarValues, String xAxisName, String yAxisName, Order order) {
		super();

		// The maximum count of patterns for any support value
		int maxLabel = 0;
		for (List<Object> record : data) {
			Object value = record.get(index);

//			System.out.println(value + " " + value.getClass());
			double valueAsDouble = -1;
			if (value instanceof Integer) {
				valueAsDouble = (Integer) value;
			} else if (value instanceof Double) {
				valueAsDouble = (Double) value;
			} else if (value instanceof Float) {
				valueAsDouble = (Float) value;
			} else if (value instanceof Boolean) {
				valueAsDouble = ((Boolean) value) ? 1d : 0d;
			} else if (value instanceof Short) {
				valueAsDouble = ((Short) value);
			}
			if (valueAsDouble > maxLabel) {
				maxLabel = (int) valueAsDouble;
			}
		}

		int[] valuesArray = new int[maxLabel + 1];
		int[] labelsArray = new int[maxLabel + 1];

		for (int i = 0; i < maxLabel + 1; i++) {
			labelsArray[i] = i;
		}

		for (List<Object> record : data) {
			Object value = record.get(index);

//			System.out.println(value + " " + value.getClass());
			double valueAsDouble = -1;
			if (value instanceof Integer) {
				valueAsDouble = (Integer) value;
			} else if (value instanceof Double) {
				valueAsDouble = (Double) value;
			} else if (value instanceof Float) {
				valueAsDouble = (Float) value;
			} else if (value instanceof Boolean) {
				valueAsDouble = ((Boolean) value) ? 1d : 0d;
			} else if (value instanceof Short) {
				valueAsDouble = ((Short) value);
			}
			int position = (int) valueAsDouble;
			valuesArray[position]++;
		}
		initializeHistogram(valuesArray, labelsArray, title, showBarLabels, showBarValues, xAxisName, yAxisName, order);
	}

	/**
	 * Get the width of bars
	 * 
	 * @return the width (integer)
	 */
	int getBarWidth() {
		return barWidth;
	}

	/**
	 * Set the width to be used for bars
	 * 
	 * @param width the width
	 */
	void setBarWidth(int width) {
		barWidth = width;
		int histogramWidth = yValues.length * getBarWidth();
		setPreferredSize(new Dimension(histogramWidth + MARGIN * 2, getHeight()));
	}
	
	/**
	 * Set the sort order for displaying the x axis values.
	 * @param order the order
	 */
	public void setSortOrder(Order order) {
		switch (order) {
        case Order.ASCENDING_Y:
            // Sort the xLabels and yValues arrays in ascending order of yValues
            sortArrays(yValues, xLabels, true);
            break;
        case Order.DESCENDING_Y:
            // Sort the xLabels and yValues arrays in descending order of yValues
            sortArrays(yValues, xLabels, false);
            break;
        case Order.ASCENDING_X:
            // Sort the xLabels and yValues arrays in ascending order of xLabels
            sortArrays(xLabels, yValues, true);
            break;
        case Order.DESCENDING_X:
            // Sort the xLabels and yValues arrays in descending order of xLabels
            sortArrays(xLabels, yValues, false);
            break;
		}

		selectedOrder = order;
		maxX = xLabels[xLabels.length-1];
    }

	/** A helper method that will sort two arrays based on the values of one array
	 * The boolean parameter ascending determines the order of sorting
	 * @param array1 an array
	 * @param array2 another array
	 * @param ascending if true, sort by ascending order. otherwise, descending order
	 */
	private void sortArrays(int[] array1, int[] array2, boolean ascending) {
		// Use a simple bubble sort algorithm
		for (int i = 0; i < array1.length - 1; i++) {
			for (int j = i + 1; j < array1.length; j++) {
				// Compare the values at index i and j
				// If ascending is true, swap them if values[i] > values[j]
				// If ascending is false, swap them if values[i] < values[j]
				if ((ascending && array1[i] > array1[j]) || (!ascending && array1[i] < array1[j])) {
					// Swap the values
					int temp = array1[i];
					array1[i] = array1[j];
					array1[j] = temp;
					// Swap the corresponding labels
					temp = array2[i];
					array2[i] = array2[j];
					array2[j] = temp;
				}
			}
		}
	}

}
