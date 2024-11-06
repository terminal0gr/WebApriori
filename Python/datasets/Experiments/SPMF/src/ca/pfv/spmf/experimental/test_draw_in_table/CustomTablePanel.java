package ca.pfv.spmf.experimental.test_draw_in_table;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.Dimension;
import java.awt.Graphics;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableCellRenderer;

public class CustomTablePanel extends JPanel {
	/**
	 * serial uid
	 */
	private static final long serialVersionUID = 4987997933960254190L;
	private JTable table;

	public CustomTablePanel() {
		super(new BorderLayout());

		// Create sample data for the table
		String[] columnNames = { "First Name", "Last Name", "Sport" };
		Object[][] data = { { "John", "Doe", "Tennis" }, { "Jane", "Smith", "Swimming" },
				// Add more rows as needed
		};

		// Create the JTable
		table = new JTable(data, columnNames);
		table.setPreferredScrollableViewportSize(new Dimension(300, 150));

		// Set custom renderer for table cells
		table.setDefaultRenderer(Object.class, new DefaultTableCellRenderer() {
			/**
			 * serial UID
			 */
			private static final long serialVersionUID = -2217750414158979166L;

			@Override
			public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected,
					boolean hasFocus, int row, int column) {
				Component c = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);
				if (row == 0 && column == 0) {
					c.setBackground(Color.RED);
				} else {
					// Set default background color for other cells
					c.setBackground(Color.WHITE);
				}
				return c;
			}
		});

		// Add the table to the panel
		JScrollPane scrollPane = new JScrollPane(table);
		add(scrollPane, BorderLayout.CENTER);
	}

	@Override
	protected void paintComponent(Graphics g) {
		super.paintComponent(g);

		// Set the background color to light blue
		g.setColor(new Color(173, 216, 230)); // RGB values for light blue
		g.fillRect(0, 0, getWidth(), getHeight());
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(() -> {
			JFrame frame = new JFrame("Custom Table Example");
			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			frame.add(new CustomTablePanel());
			frame.pack();
			frame.setVisible(true);
		});
	}
}