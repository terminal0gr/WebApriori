package ca.pfv.spmf.gui.visuals.heatmap;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionAdapter;

import javax.swing.JPanel;
import javax.swing.JScrollPane;
/*
 * Copyright (c) 2008-2023 Philippe Fournier-Viger
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
 * A Jpanel to display a heat map.
 * 
 * @author Philippe Fournier-Viger
 */
@SuppressWarnings("serial")
public class HeatMap extends JPanel {
	private final String[] rowNames;
	private final String[] columnNames;
	private final double[][] data;
	private double min = Double.MAX_VALUE;
	private double max = Double.MIN_VALUE;
	// Flags to control the drawing of labels
	private boolean drawRowLabels = true;
	private boolean drawColumnLabels = true;
	// Flag to control the drawing of the color scale
	private boolean drawColorScale = true;
	private boolean drawColumnLabelsVertically = false; // Flag to control the orientation of column labels

	/** The fond to be used for labels */
	private Font font = new Font("Arial", Font.PLAIN, 8);
	
	private int margin = 10; // Default margin size

	private int minCellWidth = 9; // Default minimum width for the heatmap cells
	private int minCellHeight = 9; // Default minimum height for the heatmap cells

	/** Minimum horizontal gap between heatmap and color scale */
	private final int COLOR_SCALE_MIN_GAP = 5;

	private JPanel drawingPanel = null;
	private JScrollPane scrollpane = null;

	public HeatMap(double[][] data, String[] rowNames, String[] columnNames) {
		if (data.length != rowNames.length || data[0].length != columnNames.length) {
			throw new IllegalArgumentException("Mismatch between data and names dimensions");
		}
		this.data = data;
		this.rowNames = rowNames;
		this.columnNames = columnNames;
		calculateMinMaxValues();
		setLayout(new BorderLayout());
		scrollpane = new JScrollPane(createHeatMapPanel());
		add(scrollpane, BorderLayout.CENTER);

	}
	
	/**
	 * Method to change the font size and style of the text labels
	 * 
	 * @param font the font
	 */
	public void setFont(Font font) {
		this.font = font;
		repaint();
	}

	// Add setters to change the flags
	public void setDrawRowLabels(boolean drawRowLabels) {
		this.drawRowLabels = drawRowLabels;
	}

	public void setDrawColumnLabels(boolean drawColumnLabels) {
		this.drawColumnLabels = drawColumnLabels;
	}

	// Add a setter to change the flag
	public void setDrawColorScale(boolean drawColorScale) {
		this.drawColorScale = drawColorScale;
	}

	// Add a setter to change the flag
	public void setDrawColumnLabelsVertically(boolean drawColumnLabelsVertically) {
		this.drawColumnLabelsVertically = drawColumnLabelsVertically;
	}

	private void calculateMinMaxValues() {
		for (double[] row : data) {
			for (double v : row) {
				if (v < min)
					min = v;
				if (v > max)
					max = v;
			}
		}
	}

	private JPanel createHeatMapPanel() {
		// Constants for margins
		// Determine the space required for labels and color scale
		int labelWidth = drawRowLabels ? 50 : 0; // Space for row names if drawn
		int labelHeight = drawColumnLabels ? 30 : 0; // Space for column names if drawn
		int colorScaleSpace = drawColorScale ? 50 : 0; // Space for color scale if drawn


		drawingPanel = new JPanel() {
			{
				// Add a MouseMotionListener to update the tooltip with the value under the
				// mouse
				addMouseMotionListener(new MouseMotionAdapter() {
					@Override
					public void mouseMoved(MouseEvent e) {
						int colWidth = (getWidth() - colorScaleSpace - margin * 3 - labelWidth) / data[0].length;
						int rowHeight = (getHeight() - margin * 3 - labelHeight) / data.length;

						int col = (e.getX() - labelWidth - margin * 2) / colWidth;
						int row = (e.getY() - labelHeight - margin * 2) / rowHeight;

						if (col >= 0 && col < data[0].length && row >= 0 && row < data.length) {

							setToolTipText("<html>Row: " + rowNames[row] + "<br>Column: " + columnNames[col]
									+ "<br>Value: " + data[row][col] + "</html>");
						} else {
							setToolTipText(null); // Clear the tooltip when not over a cell
						}
					}
				});
			}

			@Override

			protected void paintComponent(Graphics g) {
				super.paintComponent(g);
				
				((Graphics2D) g).setBackground(Color.WHITE);
				

				// Set the font for the text labels
				g.setFont(font);

				// Calculate the available width and height for the heatmap dynamically
				int availableWidth = getWidth() - colorScaleSpace - margin * 3 - labelWidth;
				int availableHeight = getHeight() - margin * 3 - labelHeight;

				// Calculate the size of each cell dynamically, based on the current panel size
				int rowHeight = Math.max(minCellHeight, availableHeight / data.length); // Use the maximum of the
																						// minimum height or the dynamic
																						// height
				int colWidth = Math.max(minCellWidth, availableWidth / data[0].length); // Use the maximum of the
																						// minimum width or the dynamic
																						// width

				// Adjust the size of the panel based on the new cell sizes and the number of
				// cells
				Dimension newSize = new Dimension(colWidth * data[0].length + colorScaleSpace + margin * 3 + labelWidth,
						rowHeight * data.length + margin * 3 + labelHeight);
				setPreferredSize(newSize);
				revalidate(); // This will tell the layout manager to recalculate the layout based on the new
								// preferred size

				// Draw the heatmap cells
				for (int row = 0; row < data.length; row++) {
					for (int col = 0; col < data[row].length; col++) {
						g.setColor(calculateColor(data[row][col]));
						g.fillRect(labelWidth + (margin * 2) + (col * colWidth),
								labelHeight + margin * 2 + row * rowHeight, colWidth, rowHeight);
					}
				}

				// Draw the row names if enabled
				if (drawRowLabels) {
					g.setColor(Color.BLACK);
					for (int row = 0; row < rowNames.length; row++) {
						g.drawString(rowNames[row], margin, labelHeight + margin * 2 + row * rowHeight + rowHeight / 2);
					}
				}

				// Draw the column names if enabled
				if (drawColumnLabels) {
					if (drawColumnLabelsVertically) {
						Graphics2D g2d = (Graphics2D) g.create();
						FontMetrics metrics = g.getFontMetrics();
						for (int col = 0; col < columnNames.length; col++) {
							int stringWidth = metrics.stringWidth(columnNames[col]);
							
							// Calculate the x and y positions for the translation
							int x = labelWidth + (margin * 2) + (col * colWidth) + (colWidth / 2);
							int y = margin + stringWidth;

							drawRotate(g2d, x, y, -90, columnNames[col]);
						}
						g2d.dispose();
					} else {
						// Draw the column labels horizontally
						for (int col = 0; col < columnNames.length; col++) {
							g.drawString(columnNames[col], labelWidth + margin * 2 + col * colWidth + colWidth / 2,
									margin + labelHeight);
						}
					}
				}

				// Draw the color scale if enabled
				if (drawColorScale) {
					// Draw the color scale on the right
					int scaleHeight = availableHeight - labelHeight; // Leave space for the min text
					int cellHeight = scaleHeight / 256;
					int remainder = scaleHeight % 256; // Calculate the remainder
					for (int i = 0; i < 256; i++) {
						double value = max - (max - min) * i / 255.0; // Calculate the value for this point on the
																		// scale, starting from max
						g.setColor(calculateColor(value)); // Use the calculateColor method
						int cellHeightToUse = cellHeight;
						if (i == 255) {
							cellHeightToUse += remainder; // Add the remainder to the last cell's height
						}
						g.fillRect(COLOR_SCALE_MIN_GAP + getWidth() - colorScaleSpace - margin,
								labelHeight + margin * 3 + i * cellHeight, 
								colorScaleSpace - COLOR_SCALE_MIN_GAP,
								cellHeightToUse);
					}

					// Draw the min and max labels for the color scale
					g.setColor(calculateColor(min));
					g.drawString("Min: " + min, getWidth() - colorScaleSpace - margin,
							labelHeight + margin * 2 + scaleHeight + labelHeight);
					g.setColor(calculateColor(max));
					g.drawString("Max: " + max, getWidth() - colorScaleSpace - margin, labelHeight + margin * 3);
				}
			}
		};
		return drawingPanel;
	}

	public static void drawRotate(Graphics2D g2d, double x, double y, int angle, String text) {
		g2d.translate((float) x, (float) y);
		g2d.rotate(Math.toRadians(angle));
		g2d.drawString(text, 0, 0);
		g2d.rotate(-Math.toRadians(angle));
		g2d.translate(-(float) x, -(float) y);
	}

	protected Color calculateColor(double value) {
	    // Normalize the value to be between 0 and 1
	    double normalizedValue = (value - min) / (max - min);

	    // Define the colors for the start, middle, and end of the gradient
	    Color startColor = Color.RED; // Color for the minimum value
	    Color middleColor = Color.GREEN; // Color for the middle value
	    Color endColor = Color.BLUE; // Color for the maximum value

	    // Calculate the color based on the normalized value
	    int r, g, b;
	    if (normalizedValue < 0.5) {
	        // Interpolate between startColor and middleColor
	        double ratio = normalizedValue * 2;
	        r = (int) (startColor.getRed() * (1 - ratio) + middleColor.getRed() * ratio);
	        g = (int) (startColor.getGreen() * (1 - ratio) + middleColor.getGreen() * ratio);
	        b = (int) (startColor.getBlue() * (1 - ratio) + middleColor.getBlue() * ratio);
	    } else {
	        // Interpolate between middleColor and endColor
	        double ratio = (normalizedValue - 0.5) * 2;
	        r = (int) (middleColor.getRed() * (1 - ratio) + endColor.getRed() * ratio);
	        g = (int) (middleColor.getGreen() * (1 - ratio) + endColor.getGreen() * ratio);
	        b = (int) (middleColor.getBlue() * (1 - ratio) + endColor.getBlue() * ratio);
	    }

	    return new Color(r, g, b);
	}


	public boolean isDrawRowLabels() {
		return drawRowLabels;
	}

	public boolean isDrawColumnLabels() {
		return drawColumnLabels;
	}

	public boolean isDrawColorScale() {
		return drawColorScale;
	}

	public boolean isDrawColumnLabelsVertically() {
		return drawColumnLabelsVertically;
	}

	public double[][] getData() {
		return data;
	}

	public String[] getRowNames() {
		return rowNames;
	}

	public String[] getColumnNames() {
		return columnNames;
	}

	// Getter for minimum cell width
	public int getMinCellWidth() {
		return minCellWidth;
	}

	// Setter for minimum cell width
	public void setMinCellWidth(int minCellWidth) {
		this.minCellWidth = Math.max(minCellWidth, 1); // Ensure the minimum width is at least 1
	}

	// Getter for minimum cell height
	public int getMinCellHeight() {
		return minCellHeight;
	}

	// Setter for minimum cell height
	public void setMinCellHeight(int minCellHeight) {
		this.minCellHeight = Math.max(minCellHeight, 1); // Ensure the minimum height is at least 1
	}

	public void setCanvasSize(int width, int height) {
		// Set the preferred size of the heatmap panel
		drawingPanel.setPreferredSize(new Dimension(width, height));

		// Assuming 'scrollPane' is the variable name for the JScrollPane
		// If 'scrollPane' is not directly accessible, you may need to get it from the
		// parent or by other means
		JScrollPane scrollPane = (JScrollPane) drawingPanel.getParent().getParent();
		scrollPane.revalidate();
		scrollPane.repaint();
	}

	// Getter for margin size
	public int getMargin() {
	    return margin;
	}

	// Setter for margin size
	public void setMargin(int margin) {
	    this.margin = Math.max(margin, 0); // Ensure the margin is not negative
	    revalidate();
	    repaint();
	}
}
