package ca.pfv.spmf.gui.visuals.heatmap;

import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics2D;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.image.BufferedImage;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import javax.imageio.ImageIO;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JFileChooser;
//HeatMapViewer.java
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;

import ca.pfv.spmf.gui.MainWindow;

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
 * A JFrame that display at HeatMap.
 * 
 * @author Philippe Fournier-Viger
 */
@SuppressWarnings("serial")
public class HeatMapViewer extends JFrame {
	private HeatMap heatMap;

	public HeatMapViewer(boolean runAsStandaloneProgram, double[][] data, String[] rowNames, String[] columnNames,  boolean drawColumnLabels, boolean drawRowLabels, boolean drawColorScale, boolean drawColumnLabelsVertically) {
		super("SPMF HeatMap Viewer");
		setIconImage(Toolkit.getDefaultToolkit().getImage(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/heatmap20.png")));
		this.heatMap  = new HeatMap(data, rowNames, columnNames);
		heatMap.setPreferredSize(new Dimension(800, 600));
		heatMap.setDrawColumnLabels(drawColumnLabels);
		heatMap.setDrawRowLabels(drawRowLabels);
		heatMap.setDrawColorScale(drawColorScale);
		heatMap.setDrawColumnLabelsVertically(drawColumnLabelsVertically);
		setPreferredSize(new Dimension(800, 600));
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		add(heatMap);
		createMenu();
		pack();
		setVisible(true);
	}

	private void createMenu() {
		JMenuBar menuBar = new JMenuBar();
		JMenu optionsMenu = new JMenu("Options");

		// Toggle Row Labels
		JCheckBoxMenuItem toggleRowLabels = new JCheckBoxMenuItem("Show Row Labels", heatMap.isDrawRowLabels());
		toggleRowLabels.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				heatMap.setDrawRowLabels(toggleRowLabels.isSelected());
				heatMap.repaint();
			}
		});

		// Toggle Column Labels
		JCheckBoxMenuItem toggleColumnLabels = new JCheckBoxMenuItem("Show Column Labels",
				heatMap.isDrawColumnLabels());
		toggleColumnLabels.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				heatMap.setDrawColumnLabels(toggleColumnLabels.isSelected());
				heatMap.repaint();
			}
		});

		// Toggle Color Scale
		JCheckBoxMenuItem toggleColorScale = new JCheckBoxMenuItem("Show Color Scale", heatMap.isDrawColorScale());
		toggleColorScale.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				heatMap.setDrawColorScale(toggleColorScale.isSelected());
				heatMap.repaint();
			}
		});

		// Toggle Column Labels Orientation
		JCheckBoxMenuItem toggleColumnLabelsOrientation = new JCheckBoxMenuItem("Draw Column Labels Vertically",
				heatMap.isDrawColumnLabelsVertically());
		toggleColumnLabelsOrientation.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				heatMap.setDrawColumnLabelsVertically(toggleColumnLabelsOrientation.isSelected());
				heatMap.repaint();
			}
		});

		// Menu item to set minimum cell width
		JMenuItem setMinCellWidthItem = new JMenuItem("Set Minimum Cell Width");
		setMinCellWidthItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String input = JOptionPane.showInputDialog(HeatMapViewer.this, "Enter minimum cell width:",
						"Set Minimum Cell Width", JOptionPane.PLAIN_MESSAGE);
				if (input != null && !input.isEmpty()) {
					try {
						int minCellWidth = Integer.parseInt(input);
						heatMap.setMinCellWidth(minCellWidth);
						heatMap.repaint();
					} catch (NumberFormatException ex) {
						JOptionPane.showMessageDialog(HeatMapViewer.this, "Invalid number format", "Error",
								JOptionPane.ERROR_MESSAGE);
					}
				}
			}
		});

		// Menu item to set minimum cell height
		JMenuItem setMinCellHeightItem = new JMenuItem("Set Minimum Cell Height");
		setMinCellHeightItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String input = JOptionPane.showInputDialog(HeatMapViewer.this, "Enter minimum cell height:",
						"Set Minimum Cell Height", JOptionPane.PLAIN_MESSAGE);
				if (input != null && !input.isEmpty()) {
					try {
						int minCellHeight = Integer.parseInt(input);
						heatMap.setMinCellHeight(minCellHeight);
						heatMap.repaint();
					} catch (NumberFormatException ex) {
						JOptionPane.showMessageDialog(HeatMapViewer.this, "Invalid number format", "Error",
								JOptionPane.ERROR_MESSAGE);
					}
				}
			}
		});

		JMenuItem setCanvasSizeItem = new JMenuItem("Set Canvas Size");
		setCanvasSizeItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String widthInput = JOptionPane.showInputDialog(HeatMapViewer.this, "Enter canvas width:",
						"Set Canvas Width", JOptionPane.PLAIN_MESSAGE);
				String heightInput = JOptionPane.showInputDialog(HeatMapViewer.this, "Enter canvas height:",
						"Set Canvas Height", JOptionPane.PLAIN_MESSAGE);
				if (widthInput != null && !widthInput.isEmpty() && heightInput != null && !heightInput.isEmpty()) {
					try {
						int width = Integer.parseInt(widthInput);
						int height = Integer.parseInt(heightInput);
						heatMap.setCanvasSize(width, height);
						HeatMapViewer.this.pack(); // Resize the frame to fit the new heatmap size
					} catch (NumberFormatException ex) {
						JOptionPane.showMessageDialog(HeatMapViewer.this, "Invalid number format", "Error",
								JOptionPane.ERROR_MESSAGE);
					}
				}
			}
		});

		// Menu item to set margin size
		JMenuItem setMarginSizeItem = new JMenuItem("Set Margin Size");
		setMarginSizeItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				String input = JOptionPane.showInputDialog(HeatMapViewer.this, "Enter margin size:", "Set Margin Size",
						JOptionPane.PLAIN_MESSAGE);
				if (input != null && !input.isEmpty()) {
					try {
						int marginSize = Integer.parseInt(input);
						heatMap.setMargin(marginSize);
					} catch (NumberFormatException ex) {
						JOptionPane.showMessageDialog(HeatMapViewer.this, "Invalid number format", "Error",
								JOptionPane.ERROR_MESSAGE);
					}
				}
			}
		});

		optionsMenu.addSeparator();
		optionsMenu.add(toggleRowLabels);
		optionsMenu.add(toggleColumnLabels);
		optionsMenu.add(toggleColorScale);
		optionsMenu.add(toggleColumnLabelsOrientation);
		optionsMenu.addSeparator();
		optionsMenu.add(setMarginSizeItem);
		optionsMenu.add(setMinCellWidthItem);
		optionsMenu.add(setMinCellHeightItem);
		optionsMenu.addSeparator();
		optionsMenu.add(setCanvasSizeItem);

		// Export Menu
		JMenu exportMenu = new JMenu("Export");
		JMenuItem exportImageItem = new JMenuItem("Export as Image");
//		exportImageItem.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/save.gif")));
		exportImageItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				exportHeatMapAsImage();
			}
		});
		exportMenu.add(exportImageItem);

		JMenuItem exportCSVItem = new JMenuItem("Export as CSV");
//		exportCSVItem.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/save.gif")));
		exportCSVItem.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				exportHeatMapDataAsCSV();
			}
		});
		exportMenu.add(exportCSVItem);

		menuBar.add(optionsMenu);
		menuBar.add(exportMenu);
		setJMenuBar(menuBar);
	}

	private void exportHeatMapAsImage() {
		JFileChooser fileChooser = new JFileChooser();
		fileChooser.setDialogTitle("Specify a file to save");
		int userSelection = fileChooser.showSaveDialog(this);

		if (userSelection == JFileChooser.APPROVE_OPTION) {
			File fileToSave = fileChooser.getSelectedFile();
			// Ensure the file has the correct extension
			if (!fileToSave.getName().toLowerCase().endsWith(".png")) {
				fileToSave = new File(fileToSave.getParentFile(), fileToSave.getName() + ".png");
			}
			saveComponentAsImage(heatMap, fileToSave);
		}
	}

	private void saveDataAsCSV(double[][] data, String[] rowNames, String[] columnNames, File file) {
		try (BufferedWriter writer = new BufferedWriter(new FileWriter(file))) {
			// Write column names
			writer.write(",");
			for (String columnName : columnNames) {
				writer.write(columnName + ",");
			}
			writer.newLine();

			// Write data with row names
			for (int i = 0; i < data.length; i++) {
				writer.write(rowNames[i] + ",");
				for (int j = 0; j < data[i].length; j++) {
					writer.write(data[i][j] + (j < data[i].length - 1 ? "," : ""));
				}
				writer.newLine();
			}
			JOptionPane.showMessageDialog(this, "HeatMap data saved successfully as CSV with row and column names!",
					"Data Export", JOptionPane.INFORMATION_MESSAGE);
		} catch (IOException ex) {
			ex.printStackTrace();
			JOptionPane.showMessageDialog(this, "Error saving data: " + ex.getMessage(), "Export Error",
					JOptionPane.ERROR_MESSAGE);
		}
	}

	private void exportHeatMapDataAsCSV() {
		JFileChooser fileChooser = new JFileChooser();
		fileChooser.setDialogTitle("Specify a file to save");
		int userSelection = fileChooser.showSaveDialog(this);

		if (userSelection == JFileChooser.APPROVE_OPTION) {
			File fileToSave = fileChooser.getSelectedFile();
			// Ensure the file has the correct extension
			if (!fileToSave.getName().toLowerCase().endsWith(".csv")) {
				fileToSave = new File(fileToSave.getParentFile(), fileToSave.getName() + ".csv");
			}
			saveDataAsCSV(heatMap.getData(), heatMap.getRowNames(), heatMap.getColumnNames(), fileToSave);
		}
	}

	private void saveComponentAsImage(Component comp, File file) {
		BufferedImage image = new BufferedImage(comp.getWidth(), comp.getHeight(), BufferedImage.TYPE_INT_RGB);
		Graphics2D g2d = image.createGraphics();
		comp.paint(g2d);
		g2d.dispose();
		try {
			ImageIO.write(image, "png", file);
			JOptionPane.showMessageDialog(this, "HeatMap image saved successfully!", "Image Export",
					JOptionPane.INFORMATION_MESSAGE);
		} catch (IOException ex) {
			ex.printStackTrace();
			JOptionPane.showMessageDialog(this, "Error saving image: " + ex.getMessage(), "Export Error",
					JOptionPane.ERROR_MESSAGE);
		}
	}
}