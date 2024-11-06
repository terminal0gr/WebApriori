package ca.pfv.spmf.gui;

import java.awt.BasicStroke;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseEvent;
import java.awt.event.MouseMotionListener;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.Arrays;

import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JSlider;
import javax.swing.Timer;
import javax.swing.ToolTipManager;

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
 * This class is for monitoring the memory usage using a JFrame window
 * 
 * @author Philippe Fournier-Viger, 2023
 */
public class MemoryViewer extends JPanel implements ActionListener, MouseMotionListener {
	/**
	 * generate serial VUID
	 */
	private static final long serialVersionUID = 278261238139167055L;

	/** The JFrame */
	static JFrame frame = null;

	/** Number of milliseconds before a refresh */
	private static final int REFRESH_RATE = 1000;

	/** The timer that updates the chart every second */
	private static Timer timer;

	/** The array that stores the memory usage values */
	private int[] memoryValues;

	/** The index of the current value in the array */
	private int position;

	/** The maximum number of values to display */
	private static final int VALUE_COUNT = 100;

	/** The maximum memory usage value to scale the chart */
	private static int maxMemoryYAxis;

	/** The font for the text elements */
	private static final Font FONT = new Font("Arial", Font.PLAIN, 12);

	/** The checkbox for toggling the grid lines */
	private JCheckBox gridCheckBox;

	/** The button for pausing and resuming the timer */
	private JButton pauseButton;

	/** The flag for indicating the timer state */
	private boolean isPaused;

	/** The constructor of the panel */
	public MemoryViewer() {
		// Initialize the array with zeros
		memoryValues = new int[VALUE_COUNT];
		Arrays.fill(memoryValues, 0);

		// Initialize the index with zero
		position = 0;

		// Set the background color of the panel
		setBackground(Color.WHITE);

		maxMemoryYAxis = (int) (Runtime.getRuntime().totalMemory() / (1024 * 1024));

		// Create and start the timer with one second delay
		timer = new Timer(REFRESH_RATE, this);
		timer.start();

		// Create the checkbox for toggling the grid lines
		gridCheckBox = new JCheckBox("Show grid lines");
		gridCheckBox.setSelected(true);
		gridCheckBox.addActionListener(this);

		// Create the button for pausing and resuming the timer
		pauseButton = new JButton("Pause");
		pauseButton.addActionListener(this);
		isPaused = false;

		// Add the checkbox and the button to the top of the panel
		this.add(gridCheckBox);
		this.add(pauseButton);

		// Add the mouse motion listener to the panel
		this.addMouseMotionListener(this);

		// Set the initial delay of the tooltip manager to zero
		ToolTipManager.sharedInstance().setInitialDelay(0);
	}

	/** The method that handles the timer and checkbox events */
	public void actionPerformed(ActionEvent e) {
		// Get the source of the event
		Object source = e.getSource();

		// If the source is the timer
		if (source == timer) {
			// Get the runtime instance of the JVM
			Runtime runtime = Runtime.getRuntime();

			// Get the total, free, and used memory of the JVM in megabytes
			int jvmMemory = (int) (runtime.totalMemory() / (1024 * 1024));
			int freeMemory = (int) (runtime.freeMemory() / (1024 * 1024));
			int usedMemory = jvmMemory - freeMemory;

			// Store the used memory value in the array
			memoryValues[position] = usedMemory;
			
			

			// Find the max value (either the JVM max value or the max value that we
			// have seen until now (because it might be bigger than the JVM max value)
			maxMemoryYAxis = jvmMemory;
			for (int i = 0; i < memoryValues.length; i++) {
				if (memoryValues[i] > maxMemoryYAxis) {
					maxMemoryYAxis = memoryValues[i];
				}
			}

			// Increment the index and wrap around if necessary
			position = (position + 1) % VALUE_COUNT;

			// Repaint the panel to update the chart and text
			repaint();
			if (isVisible() == false) {
				timer.stop();
			}
		}

		// If the source is the checkbox
		if (source == gridCheckBox) {
			// Repaint the panel to update the grid lines
			repaint();
		}

		// If the source is the button
		if (source == pauseButton) {
			// Toggle the timer state
			isPaused = !isPaused;

			// If the timer is paused
			if (isPaused) {
				// Stop the timer and change the button text to "Resume"
				timer.stop();
				pauseButton.setText("Resume");
			}
			// If the timer is resumed
			else {
				// Start the timer and change the button text to "Pause"
				timer.start();
				pauseButton.setText("Pause");
			}
		}
	}

	/** The method that paints the panel */
	public void paintComponent(Graphics g) {
		// Call the superclass method first
		super.paintComponent(g);

		// Cast the graphics object to Graphics2D for better rendering
		Graphics2D g2d = (Graphics2D) g;

		// Get the width and height of the panel
		int width = getWidth();
		int height = getHeight();

		// If the grid lines are enabled
		if (gridCheckBox.isSelected()) {
			// Draw the horizontal and vertical grid lines with 10 pixels gap
			g2d.setColor(new Color(230, 230, 230));
			for (int x = 0; x < width; x += 10) {
				g2d.drawLine(x, 0, x, height);
			}
			for (int y = 0; y < height; y += 10) {
				g2d.drawLine(0, y, width, y);
			}
		}

		// Draw the chart line with a stroke of 2 pixels
		g2d.setColor(Color.RED);
		g2d.setStroke(new BasicStroke(2));

		// Calculate the scaling factor for the chart based on the maximum memory value
		double scale = (double) height / maxMemoryYAxis;

		// Loop through the values array and draw a line segment for each pair of values
		for (int i = 0; i < VALUE_COUNT - 1; i++) {
			// Get the current and next values from the array
			int currentValue = memoryValues[(position + i) % VALUE_COUNT];
			int nextValue = memoryValues[(position + i + 1) % VALUE_COUNT];

			// Calculate the x and y coordinates for the current and next points on the
			// chart
			int currentX = i * width / VALUE_COUNT;
			int currentY = height - (int) (currentValue * scale);
			int nextX = (i + 1) * width / VALUE_COUNT;
			int nextY = height - (int) (nextValue * scale);

			// Draw a line segment between the current and next points on the chart
			g2d.drawLine(currentX, currentY, nextX, nextY);
		}

		// Draw the text elements with black color and Arial font
		g2d.setColor(Color.BLACK);
		g2d.setFont(FONT);

		// Draw the title of the chart at the top center of the panel
		g2d.drawString("" + memoryValues[(position + VALUE_COUNT - 1) % VALUE_COUNT] + " MB", 10, 20);

		// Draw the label of the slider at the bottom center of the panel
		g2d.drawString("Refresh rate: " + timer.getDelay() + " ms", width / 2 - 50, height - 10);
	}

	public void mouseMoved(MouseEvent e) {
		// Get the x and y coordinates of the mouse pointer
		int x = e.getX();
		int y = e.getY();

		// Get the width and height of the panel
		int width = getWidth();
		int height = getHeight();

		// Calculate the scaling factor for the chart based on the maximum memory value
		double scale = (double) height / maxMemoryYAxis;

		// Calculate the index of the value corresponding to the mouse position
		int index = x * VALUE_COUNT / width;

		// Get the value from the array
		int value = memoryValues[(position + index) % VALUE_COUNT];

		// Calculate the y coordinate of the value on the chart
		int valueY = height - (int) (value * scale);

		// If the mouse pointer is close enough to the chart line
		if (Math.abs(y - valueY) < 10) {
			// Set the tooltip text to show the memory value
			setToolTipText("" + value + " MB");
		}
		// If the mouse pointer is far from the chart line
		else {
			// Set the tooltip text to null
			setToolTipText(null);
		}
	}

	/** The main method that creates and displays the frame with the panel */
	public static void main(String[] args) {
		displayMemoryChart();
	}

	/** main method for testing **/
	public static void displayMemoryChart() {
		if (frame != null) {
			return;
		}
		// Create a new frame with the title "Memory and CPU Usage Chart"
		frame = new JFrame("SPMF Memory Viewer (JVM)");

		// Set the size and location of the frame
		frame.setSize(350, 200);
		frame.setLocationRelativeTo(null);

		// Set the default close operation of the frame
		frame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);

		// Create a new instance of the panel and add it to the frame
		MemoryViewer panel = new MemoryViewer();
		frame.add(panel);

		// =============================
		// Create a slider with horizontal orientation, range from 0 to 1000, and
		// initial value of 500
		JSlider slider = new JSlider(JSlider.HORIZONTAL, 0, 1000, 200);

		// Add a change listener to the slider that updates the timer's delay
		slider.addChangeListener(e -> {
		    if (!timer.isRunning() || timer.getDelay() != slider.getValue()) {
		        timer.setDelay(slider.getValue());
		    }
		});

		// Set some properties of the slider for better appearance and functionality
		slider.setPaintTicks(true);
		slider.setPaintLabels(true);
		slider.setMajorTickSpacing(200);
		slider.setMinorTickSpacing(50);
		slider.setSnapToTicks(true);

		// Add the slider to the bottom of the panel
		frame.getContentPane().add(slider, BorderLayout.SOUTH);
		// =============================

		frame.addWindowListener(new WindowAdapter() {
			public void windowClosing(WindowEvent e) {
				panel.setVisible(false);
				frame = null;
			}
		});

		// Make the frame visible
		frame.setVisible(true);
	}

	@Override
	public void mouseDragged(MouseEvent e) {
		// TODO Auto-generated method stub

	}
}
