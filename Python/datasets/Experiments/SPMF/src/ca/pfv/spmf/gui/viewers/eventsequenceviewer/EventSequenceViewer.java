package ca.pfv.spmf.gui.viewers.eventsequenceviewer;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

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
import ca.pfv.spmf.gui.visuals.timeline.EventT;
import ca.pfv.spmf.gui.visuals.timeline.TimelineViewer;
import ca.pfv.spmf.input.event_sequence.Event;
import ca.pfv.spmf.input.event_sequence.EventSequence;
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
 * This class is an event sequence viewer tool for visualizing the content of an
 * event sequence file with timestamps.
 * 
 * @author Philippe Fournier-Viger
 */
public class EventSequenceViewer extends JFrame {

	/** The table */
	private JTable table;
	/** The scroll pane */
	private JScrollPane scrollPane;
	/** The status label */
	private JLabel statusLabel;
	/** The name label */
	private JLabel nameLabel;

	// The JPanel object that holds the timeline chart
	private JPanel timelinePanel;
	private EventSequence es;

	/**
	 * Constructor
	 * 
	 * @param runAsStandaloneProgram if true, this tool will be run in standalone
	 *                               mode (close the window will close the program).
	 *                               Otherwise not.
	 */
	public EventSequenceViewer(boolean runAsStandaloneProgram, String filePath) {
		// Initialize the frame title
		super("SPMF Event Sequence Viewer " + Main.SPMF_VERSION);
		if (runAsStandaloneProgram) {
			// Set the default close operation
			setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		}
		// Set the layout to border layout
		setLayout(new BorderLayout());

		// Create a JTable object to display the event sequence
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

//		// Create a JPanel object to hold the buttons
		JPanel buttonPanel = new JPanel();

		// Create a JButton object for the first button
		JButton button1 = new JButton("View with Timeline Viewer");
		// Add an action listener to the button
		button1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				viewAsTimeline();
			}

		});
		button1.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/timeline20b.png")));

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

		// Create a JPanel object to hold the top components
		JPanel topPanel = new JPanel();
		// Create a JLabel object to display the sequence name
		nameLabel = new JLabel();
		// Set the text of the label to show the file name of the sequence
		nameLabel.setText("Sequence: " + filePath);

		// Create a JButton object to load a sequence
		if(runAsStandaloneProgram) {
			JButton loadButton = new JButton("Load sequence");
			loadButton.setIcon(new ImageIcon(MainWindow.class.getResource("/ca/pfv/spmf/gui/icons/Open24.gif")));
			// Add an action listener to the button
			loadButton.addActionListener(new ActionListener() {
				public void actionPerformed(ActionEvent e) {
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
					int result = fc.showOpenDialog(EventSequenceViewer.this);
					// If the user approved the file selection
					if (result == JFileChooser.APPROVE_OPTION) {
						// Get the selected file
						File file = fc.getSelectedFile();
						// Get the file path
						String filepath = file.getPath();
						openSequenceFile(filepath);
					}
					// remember this folder for next time.
					if (fc.getSelectedFile() != null) {
						PreferencesManager.getInstance().setInputFilePath(fc.getSelectedFile().getParent());
					}
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
			openSequenceFile(filePath);
		}

		// Set the size and location of the frame
		setSize(800, 600);
		setLocationRelativeTo(null);
		pack();
		// Make the frame visible
		setVisible(true);
	}

	protected void viewAsTimeline() {
	    if (table.getModel() != null) {
	        EventSequence db = ((EventSequenceTableModel) table.getModel()).es;
	        Map<Integer, String> mapItemToString = db.getMapItemToStringValues();

	        // Create a list of Events
	        List<EventT> events = new ArrayList<>();
	        for (int i = 0; i < db.size(); i++) {
	            Event event = db.get(i); 
	            String name = mapItemToString.get(event.getItem());
	            long time = event.getTimestamp();
	            events.add(new EventT(name, time));
	        }

	        // Instantiate the TimelineViewer
	        TimelineViewer timelineViewer = new TimelineViewer(false, events, null);

	        // You may need to add additional code here to display the timelineViewer
	    }
	}

	private void viewItemFrequencyDistribution() {
		if (table.getModel() != null) {
			EventSequence db = ((EventSequenceTableModel) table.getModel()).es;
			Map<Integer, String> mapItemToString = db.getMapItemToStringValues();

			// Find the maximum item
			int maxItem = es.getMaxItemID();

			// Prepare the data (counts)
			int[] yValues = new int[maxItem + 1];
			for (int i = 0; i < db.size(); i++) {
				Event event = db.get(i);
				int item = event.getItem();
				yValues[item]++;
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
	 * Open a sequence in the viewer
	 * 
	 * @param filepath the file path
	 */
	private void openSequenceFile(String filepath) {
		es = new EventSequence();
		try {
			// Load the file containing the event sequence
			es.loadFile(filepath);
		} catch (Exception ex) {
			// Get the exception message and the stack trace as a string
			String errorMessage = String.format("Error loading file. Reading error: %s%n", ex.getMessage());
			// Get the exception class name as a string
			String title = ex.getClass().getName();
			// Show a JDialog with the exception message and the stack trace, and set the
			// dialog title and the message type
			JOptionPane.showMessageDialog(this, errorMessage, title, JOptionPane.ERROR_MESSAGE);
		}
		// Create a new EventSequenceTableModel object with the new sequence
		EventSequenceTableModel model = new EventSequenceTableModel(es);
		// Set the table model to the new model
		table.setModel(model);

		// Get the file object of the sequence
		File file = new File(filepath);
		// Get the file size in bytes
		long fileSize = file.length();
		// Convert the file size to megabytes
		double fileSizeMB = fileSize / (1024.0 * 1024.0);
		// Format the file size to two decimal places
		String fileSizeMBString = String.format("%.2f", fileSizeMB);

		// Get the number of events in the sequence
		int eventCount = es.size();
		// Get the number of unique events in the sequence
		int uniqueEventCount = es.getUniqueEvents().size();
		// Get the minimum and maximum timestamps in the sequence
		long minTimestamp = es.getMinTimestamp();
		long maxTimestamp = es.getMaxTimestamp();
		// Calculate the duration of the sequence by subtracting the min and max
		// timestamps
		long duration = maxTimestamp - minTimestamp;
		// Format the duration to seconds
		String durationString = String.format("%.2f", duration / 1000.0);

		// Update the status label to show the new file size, event count, unique event
		// count, and duration
		statusLabel.setText("Size: " + fileSizeMBString + " MB | Events: " + eventCount + " | Unique events: "
				+ uniqueEventCount + " | Loading time: " + durationString + " s");
		// Update the name label to show the new file name of the sequence
		nameLabel.setText("Sequence: " + filepath);
	}

	/** The table model for this tool */
	public class EventSequenceTableModel implements TableModel {

		// The EventSequence object that holds the data
		private EventSequence es;
		// The list of listeners for this table model
		private List<TableModelListener> listeners;

		// The constructor that takes an EventSequence object as a parameter
		public EventSequenceTableModel(EventSequence es) {
			// Initialize the fields
			this.es = es;
			this.listeners = new ArrayList<TableModelListener>();
		}

		// The method that returns the number of rows in the table
		public int getRowCount() {
			// Return three, since there are event type, and timestamp
			return 2;
		}

		// The method that returns the number of columns in the table
		public int getColumnCount() {
			// Return the number of events in the sequence plus one for the first column
			return es.size() + 1;
		}

		// The method that returns the name of the column at the given index
		public String getColumnName(int columnIndex) {
			// If the column index is zero, return an empty string
			if (columnIndex == 0) {
				return "";
			}
			// Otherwise, return the index of the event minus one
			return String.valueOf(columnIndex - 1);
		}

		// The method that returns the class of the values in the column at the given
		// index
		public Class<?> getColumnClass(int columnIndex) {
			// Return the class of String, since the table will display event values or null
			// values
			return String.class;
		}

		// The method that returns the value at the given row and column index
		public Object getValueAt(int rowIndex, int columnIndex) {
			// If the column index is zero, return the row name
			if (columnIndex == 0) {
				switch (rowIndex) {
				case 0:
					return "Event Type";
				case 1:
					return "Timestamp";
				default:
					return null;
				}
			}
			// Otherwise, get the event at the given column index minus one
			Event event = es.get(columnIndex - 1);
			// Return the value of the event based on the row index
			switch (rowIndex) {
			case 0:
				return getItemName(event.getItem());
			case 1:
				return Long.toString(event.getTimestamp());
			default:
				return null;
			}
		}

		// The method that returns whether the cell at the given row and column index is
		// editable
		public boolean isCellEditable(int rowIndex, int columnIndex) {
			// Return false, since the table is not editable
			return false;
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

		/**
		 * Get the item name for a given column index
		 * 
		 * @param itemID the item
		 * @return the item name
		 */
		private String getItemName(int itemID) {
			String itemName = es.getNameForItem(itemID);
			if (itemName != null) {
				return itemName;
			} else {

				return "Item " + itemID;
			}
		}
	}

	// The method that draws a timeline chart using the Graphics2D class
	public void drawTimeline(Graphics2D g2d) {
		// Get the width and height of the frame
		int width = getWidth();
		int height = getHeight();
		// Set the margin for the chart
		int margin = 50;
		// Set the font for the chart
		g2d.setFont(new Font("Arial", Font.PLAIN, 12));
		// Set the color for the chart
		g2d.setColor(Color.BLACK);
		// Draw the x-axis and the y-axis
		g2d.drawLine(margin, height - margin, width - margin, height - margin);
		g2d.drawLine(margin, margin, margin, height - margin);
		// Draw the x-axis label
		g2d.drawString("Time (s)", width / 2, height - margin / 2);
		// Draw the y-axis label
		g2d.rotate(-Math.PI / 2);
		g2d.drawString("Event Type", -height / 2, margin / 2);
		g2d.rotate(Math.PI / 2);
		// Get the minimum and maximum timestamps in the sequence
		long minTimestamp = es.getMinTimestamp();
		long maxTimestamp = es.getMaxTimestamp();
		// Calculate the scale factor for the x-axis
		double xScale = (double) (width - 2 * margin) / (maxTimestamp - minTimestamp);
		// Get the unique events in the sequence
		List<String> uniqueEvents = new ArrayList<String>();
		for (Integer elm : es.getUniqueEvents()) {
			uniqueEvents.add("" + elm);
		}
		// Calculate the scale factor for the y-axis
		double yScale = (double) (height - 2 * margin) / uniqueEvents.size();
		// Draw the x-axis ticks and labels
		for (int i = 0; i <= 10; i++) {
			// Calculate the x-coordinate of the tick
			int x = margin + (int) (i * (width - 2 * margin) / 10.0);
			// Draw the tick
			g2d.drawLine(x, height - margin - 5, x, height - margin + 5);
			// Calculate the corresponding timestamp
			long timestamp = minTimestamp + (long) (i * (maxTimestamp - minTimestamp) / 10.0);
			// Format the timestamp to seconds
			String timestampString = String.format("%.2f", timestamp / 1000.0);
			// Draw the label
			g2d.drawString(timestampString, x - 10, height - margin + 20);
		}
		// Draw the y-axis ticks and labels
		for (int i = 0; i < uniqueEvents.size(); i++) {
			// Get the event type
			String eventType = uniqueEvents.get(i);
			// Calculate the y-coordinate of the tick
			int y = margin + (int) ((i + 0.5) * yScale);
			// Draw the tick
			g2d.drawLine(margin - 5, y, margin + 5, y);
			// Draw the label
			g2d.drawString(eventType, margin - 30, y + 5);
		}
		// Draw the points and lines for the events in the sequence
		for (int i = 0; i < es.size(); i++) {
			// Get the event
			Event event = es.get(i);
			// Get the event type and the timestamp
			String eventType = "" + event.getItem();
			long timestamp = event.getTimestamp();
			// Calculate the x-coordinate and the y-coordinate of the point
			int x = margin + (int) ((timestamp - minTimestamp) * xScale);
			int y = margin + (int) ((uniqueEvents.indexOf(eventType) + 0.5) * yScale);
			// Draw the point
			g2d.fillOval(x - 3, y - 3, 6, 6);
			// If this is not the first event, draw a line to connect with the previous
			// event
			if (i > 0) {
				// Get the previous event
				Event prevEvent = es.get(i - 1);
				// Get the previous event type and the previous timestamp
				String prevEventType = "" + prevEvent.getItem();
				long prevTimestamp = prevEvent.getTimestamp();
				// Calculate the x-coordinate and the y-coordinate of the previous point
				int prevX = margin + (int) ((prevTimestamp - minTimestamp) * xScale);
				int prevY = margin + (int) ((uniqueEvents.indexOf(prevEventType) + 0.5) * yScale);
				// Draw the line
				g2d.drawLine(prevX, prevY, x, y);
			}
		}
	}

//	// The method that creates and adds the timeline panel to the frame
//	public void addTimelinePanel() {
//		// Create a new JPanel object with a preferred size
//		timelinePanel = new JPanel() {
//			@Override
//			protected void paintComponent(Graphics g) {
//				// Call the super method
//				super.paintComponent(g);
//				// Cast the Graphics object to a Graphics2D object
//				Graphics2D g2d = (Graphics2D) g;
//				// Call the drawTimeline method and pass the Graphics2D object as a parameter
//				drawTimeline(g2d);
//			}
//		};
//		timelinePanel.setPreferredSize(new Dimension(300, 600));
//		// Override the paintComponent method of the JPanel class
//		
//		// Add the timeline panel to the frame using the BorderLayout.EAST position
//		add(timelinePanel, BorderLayout.SOUTH);
//	}

//	// The method that adds a listener to the table model to repaint the timeline panel
//	public void addTableModelListener() {
//		// Get the table model
//		TableModel model = table.getModel();
//		// Add a table model listener to the model
//		model.addTableModelListener(new TableModelListener() {
//			@Override
//			public void tableChanged(TableModelEvent e) {
//				// Repaint the timeline panel
//				timelinePanel.repaint();
//			}
//		});
//	}

}
