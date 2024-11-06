package ca.pfv.spmf.gui.visuals.histograms;

import java.awt.BorderLayout;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentEvent;
import java.awt.event.ComponentListener;
import java.util.List;
import java.util.Map;
import java.util.Vector;

import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextField;

import ca.pfv.spmf.gui.Main;
import ca.pfv.spmf.gui.MainWindow;
import ca.pfv.spmf.gui.visuals.histograms.HistogramDistributionPanel.Order;

/*
 * Copyright (c) 2008-2024 Philippe Fournier-Viger
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
 * A window (JFrame) that display a histogram panel for showing some frequency
 * distribution to the user.
 * 
 * @author Philippe Fournier-Viger
 */
public class HistogramDistributionWindow extends JFrame {

	/** default serial UID */
	private static final long serialVersionUID = 4751136799631193209L;

	/** The scroll pane */
	private JScrollPane scrollPane;

	/**
	 * A constructor that takes the name of the text file and creates the panel
	 * 
	 * @param fileName        the pattern file name
	 * @param runAsStandalone set to true if this window is executed by itself as a
	 *                        standalone program, otherwise false
	 * @param mapItemToString
	 * @param measure         the measure to be used to visualize the pattern
	 *                        distribution
	 * @param order           the desired sorting order for the x axis
	 */
	public HistogramDistributionWindow(boolean runAsStandalone, int[] yValues, int[] xLabels, String title,
			boolean showBarLabels, boolean showBarValues, String xAxisName, String yAxisName,
			Map<Integer, String> mapItemToString, Order order) {
		
		

		// Create a Histogram object with the values and labels arrays
		HistogramDistributionPanel histogram = new HistogramDistributionPanel(yValues, xLabels, title, showBarLabels,
				showBarValues, xAxisName, yAxisName, mapItemToString, order);

		initializeWindow(runAsStandalone, histogram, order);
	}

	public HistogramDistributionWindow(boolean runAsStandalone, Vector<List<Object>> data, int index, String title,
			String xAxisName, String yAxisName, Order order) {
		super();

		// Create a chart panel object and add it to the frame
		HistogramDistributionPanel panel = new HistogramDistributionPanel(data, 780, 550, index, title, true, true,
				xAxisName, yAxisName, order);

		initializeWindow(runAsStandalone, panel, order);
	}

	private void initializeWindow(boolean runAsStandalone, HistogramDistributionPanel histogram, Order order) {
		setIconImage(Toolkit.getDefaultToolkit()
				.getImage(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/histogram.png")));
		// Set the title of the frame
		setTitle("SPMF Histogram Viewer " + Main.SPMF_VERSION);

		// Create a JFrame with a title

		this.setLayout(new BorderLayout());
		JPanel contentPane = (JPanel) this.getContentPane();

		// Set the default close operation
		if (runAsStandalone) {
			this.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		}

		// Set the layout manager of the contentPane to a vertical BoxLayout
		contentPane.setLayout(new BoxLayout(contentPane, BoxLayout.Y_AXIS));

		scrollPane = new JScrollPane(histogram);

		// Set the horizontal scroll bar policy of the JScrollPane to always show
		scrollPane.setHorizontalScrollBarPolicy(JScrollPane.HORIZONTAL_SCROLLBAR_ALWAYS);

		// Add the JScrollPane to the contentPane instead of the histogram JPanel
		contentPane.add(scrollPane);

		// Set the size and location of the JFrame
		this.setSize(800, 400);
		this.setPreferredSize(new Dimension(800, 400));
		this.setLocationRelativeTo(null);

		// Create a new JTextField object and set its initial text to the current value
		// of the MIN_BAR_WIDTH constant
		JTextField textField = new JTextField(String.valueOf(histogram.getBarWidth()));
		textField.setColumns(3);
		textField.setSize(40, 20);

		// Create a new JLabel object and set its text to "Bar width:" or something
		// similar
		JLabel labelWidth = new JLabel("Change bar width:");

		// Create a new JPanel object and set its layout to a FlowLayout with center
		// alignment
		JPanel textPanel = new JPanel();
		textPanel.setLayout(new FlowLayout(FlowLayout.CENTER));

		// Add the JLabel and the JTextField to the JPanel
		textPanel.add(labelWidth);
		textPanel.add(textField);

		JLabel labelSortXValues = new JLabel("Sort X axis by:");
		textPanel.add(labelSortXValues);
//		String[] options = {"Ascending X values", "Descending X values", "Ascending Y values", "Descending Y values"};
		JComboBox<Order> sortComboBox = new JComboBox<Order>(Order.values());
		sortComboBox.setSelectedItem(order);
		textPanel.add(sortComboBox);
		sortComboBox.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				// Get the selected option
				Order option = (Order) sortComboBox.getSelectedItem();
				histogram.setSortOrder(option);
				// Repaint the histogram panel to reflect the changes
				repaint();
			}
		});

		// Add an ActionListener to the JTextField that will update the value of the
		// MIN_BAR_WIDTH constant and repaint the histogram JPanel when the user presses
		// the Enter key
		textField.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				// Get the text from the JTextField and parse it as an integer
				String text = textField.getText();
				int newWidth = Integer.parseInt(text);

				// Update the value of the MIN_BAR_WIDTH constant
				histogram.setBarWidth(newWidth);
//				repainHistogram(histogram);

				// Repaint the histogram JPanel
				histogram.repaint();

				histogram.validate();

//				// Update the view component of the scroll pane
				scrollPane.setViewportView(histogram);

			}

		});

		JButton buttonExport = new JButton("Save as PNG");
		buttonExport.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/save.gif")));
		buttonExport.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent arg0) {

				histogram.exportAsImage("histogram.png");
			}
		});

		// Create a new button for saving the histogram as a file
		JButton buttonSave = new JButton("Save as CSV");
		buttonSave.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/save.gif")));
		buttonSave.addActionListener(new ActionListener() {

			public void actionPerformed(ActionEvent arg0) {

				histogram.exportAsCSV("histogram.txt");
			}
		});

		JPanel saveOptionsPanel = new JPanel();
		saveOptionsPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
		saveOptionsPanel.add(buttonSave);
		saveOptionsPanel.add(buttonExport);// Set the maximum size of the buttonPanel to match its preferred size

		// Create a new panel for holding the buttons
		JPanel bottomPanel = new JPanel();
		bottomPanel.setLayout(new BoxLayout(bottomPanel, BoxLayout.Y_AXIS));
//		bottomPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
		// Add the JPanel to the contentPane, using the BorderLayout.NORTH constraint
		bottomPanel.add(textPanel);
		bottomPanel.add(Box.createVerticalGlue());
		// Add the buttons to the buttonPanel
		bottomPanel.add(saveOptionsPanel);

		// Set the alignment of the buttonPanel to the center of the contentPane
		bottomPanel.setAlignmentX(Component.CENTER_ALIGNMENT);
		//

		// Add the buttonPanel to the contentPane, using the BorderLayout.SOUTH
		// constraint
		contentPane.add(bottomPanel);

//		// Set the maximum size of the buttonPanel to match its preferred size
		saveOptionsPanel.setMaximumSize(saveOptionsPanel.getPreferredSize());
		textPanel.setMaximumSize(textPanel.getPreferredSize());
		bottomPanel.setMaximumSize(bottomPanel.getPreferredSize());

		// Add a ComponentListener to the histogram JPanel
		histogram.addComponentListener(new ComponentListener() {

			// Override the componentResized method
			@Override
			public void componentResized(ComponentEvent e) {
				// Get the new width and height of the frame
				int newWidth = e.getComponent().getWidth();
				int newHeight = e.getComponent().getHeight();

				// Call the setPreferredSize method on the histogram JPanel with the new width
				// and height
				histogram.setPreferredSize(new Dimension(newWidth, newHeight));

				// Call the revalidate method on the histogram JPanel after setting its
				// preferred size
				histogram.revalidate();

				// Update the view component of the scroll pane
				scrollPane.setViewportView(histogram);
			}

			// Ignore the other methods
			@Override
			public void componentMoved(ComponentEvent e) {
			}

			@Override
			public void componentShown(ComponentEvent e) {
			}

			@Override
			public void componentHidden(ComponentEvent e) {
			}
		});

		// Call the revalidate method on the histogram JPanel after setting its
		// preferred size
		histogram.revalidate();

		// Call the pack method on the JFrame after adding all the components
		pack();

		// Make the frame visible
		setVisible(true);
	}

}