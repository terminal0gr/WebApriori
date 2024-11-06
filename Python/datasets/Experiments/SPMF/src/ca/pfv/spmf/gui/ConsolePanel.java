package ca.pfv.spmf.gui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintStream;
import java.io.PrintWriter;

import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JMenu;
import javax.swing.JMenuItem;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollPane;
import javax.swing.JTextPane;
import javax.swing.SwingUtilities;
import javax.swing.text.BadLocationException;
import javax.swing.text.SimpleAttributeSet;
import javax.swing.text.StyleConstants;
import javax.swing.text.StyledDocument;

import ca.pfv.spmf.gui.preferences.PreferencesManager;

/*
 * Copyright (c) 2008-2015 Philippe Fournier-Viger
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
 * This is a console panel as used by the GUI of SPMF.
 * 
 * @author Philippe Fournier-Viger
 */
public class ConsolePanel extends JPanel {
	/**
	 * serial UID
	 */
	private static final long serialVersionUID = 8344817215180749939L;
	/** Color for status messages */
	private static final Color STATUS_MESSAGE_COLOR = Color.GRAY;
	/** Color for regular messages */
	private static final Color REGULAR_MESSAGE_COLOR = Color.BLACK;
	/** Text pane to show text */
	private static  JTextPane textPaneConsoleOutput;
	/** StyleDocument object */
	private StyledDocument doc;
	/** The clear button */
	private JButton clearButton;
	/** The scrollPane */
	private JScrollPane scrollPane;
	
	/** line separator */
	String newline = System.getProperty("line.separator");

	/**
	 * Constructs a new ConsolePanel, initializes components, sets up the layout and
	 * actions, and redirects system streams to the text pane.
	 */
	public ConsolePanel(boolean showClearButton) {
		initializeComponents();
		setupLayout(showClearButton);
		setupActions();

		redirectOutputStream();
	}

	public void redirectOutputStream() {
		// Redirects the standard output streams to the text pane console output.
		System.setOut(new PrintStream(new TextPaneOutputStream(textPaneConsoleOutput)));
	}

	/**
	 * Initializes the components of the console panel.
	 */
	private void initializeComponents() {
		textPaneConsoleOutput = new JTextPane();
		textPaneConsoleOutput.setEditable(false);
		textPaneConsoleOutput.setBackground(Color.WHITE);

		Integer fontSize = PreferencesManager.getInstance().getConsoleFontSize();
		if (fontSize != null) {
			java.awt.Font newFont = textPaneConsoleOutput.getFont().deriveFont((float) fontSize);
			textPaneConsoleOutput.setFont(newFont);
		}

		doc = textPaneConsoleOutput.getStyledDocument();
	}

	/**
	 * Sets up the layout of the console panel with a scrollable text pane and a
	 * clear button.
	 * 
	 * @param showClearButton if true, add a clear console button
	 */
	private void setupLayout(boolean showClearButton) {
		setLayout(new BorderLayout());
		scrollPane = new JScrollPane(textPaneConsoleOutput);
		add(scrollPane, BorderLayout.CENTER);
		if (showClearButton) {
			add(createClearButton(), BorderLayout.SOUTH);
		}
		this.validate();
	}

	/**
	 * Creates and returns a JButton that clears the console when clicked.
	 * 
	 * @return JButton to clear the console
	 */
	private JButton createClearButton() {
		clearButton = new JButton("Clear Console");
		clearButton.addActionListener(e -> clearConsole());
		return clearButton;
	}

	/**
	 * Sets up actions for the console panel, specifically the context menu for the
	 * text pane.
	 */
	private void setupActions() {
		JPopupMenu contextMenu = createContextMenu();
		textPaneConsoleOutput.setComponentPopupMenu(contextMenu);
	}

	/**
	 * Creates and returns a JPopupMenu for the text pane with a clear console
	 * option.
	 * 
	 * @return JPopupMenu with options for the console
	 */
	private JPopupMenu createContextMenu() {
		JPopupMenu contextMenu = new JPopupMenu();

		JMenuItem clearItem = new JMenuItem("Clear");
		clearItem.addActionListener(e -> clearConsole());
		contextMenu.add(clearItem);

//		JMenuItem copyItem = new JMenuItem("Copy");
//		copyItem.addActionListener(e -> copyText());
//		contextMenu.add(copyItem);

		JMenuItem saveLogItem = new JMenuItem("Save Log to File");
		saveLogItem.addActionListener(e -> saveLog());
		contextMenu.add(saveLogItem);

		contextMenu.addSeparator();

		JMenu fontSizeMenu = createFontSizeMenu();
		contextMenu.add(fontSizeMenu);

//		JMenuItem changeBgColorItem = new JMenuItem("Change Background Color");
//		changeBgColorItem.addActionListener(e -> changeBackgroundColor());
//		contextMenu.add(changeBgColorItem);

		return contextMenu;
	}

	/**
	 * Copy text from the console
	 */
	public void copyText() {
		String text = textPaneConsoleOutput.getSelectedText();
		if (text != null) {
			StringSelection stringSelection = new StringSelection(text);
			Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
			clipboard.setContents(stringSelection, null);
		}
	}

	/**
	 * Save text from the console to a file
	 */
	private void saveLog() {
		JFileChooser fileChooser = new JFileChooser();
		if (fileChooser.showSaveDialog(this) == JFileChooser.APPROVE_OPTION) {
			File file = fileChooser.getSelectedFile();
			try (PrintWriter out = new PrintWriter(new FileWriter(file))) {
				out.println(textPaneConsoleOutput.getText());
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}

//	/**
//	 * Change the background color
//	 */
//	private void changeBackgroundColor() {
//		Color newColor = JColorChooser.showDialog(this, "Choose Background Color",
//				textPaneConsoleOutput.getBackground());
//		if (newColor != null) {
//			textPaneConsoleOutput.setBackground(newColor);
//		}
//	}

	/**
	 * Create font size menu
	 */
	private JMenu createFontSizeMenu() {
		JMenu fontSizeMenu = new JMenu("Font Size");
		JMenuItem increaseFontSize = new JMenuItem("Increase");
		increaseFontSize.addActionListener(e -> changeFontSize(1));
		fontSizeMenu.add(increaseFontSize);

		JMenuItem decreaseFontSize = new JMenuItem("Decrease");
		decreaseFontSize.addActionListener(e -> changeFontSize(-1));
		fontSizeMenu.add(decreaseFontSize);

		return fontSizeMenu;
	}

	/**
	 * Change the font size
	 * 
	 * @param delta by how much points the font size should be increased or reduced
	 */
	private void changeFontSize(int delta) {
		Font currentFont = textPaneConsoleOutput.getFont();
		float newSize = currentFont.getSize() + delta;
		textPaneConsoleOutput.setFont(currentFont.deriveFont(newSize));

//		System.out.println(PreferencesManager.getInstance().getConsoleFontSize());
		PreferencesManager.getInstance().setConsoleFontSize((int) newSize);
//		Systsem.out.println(PreferencesManager.getInstance().getConsoleFontSize());
	}

	/**
	 * An OutputStream that writes to a JTextPane.
	 */
	public void postStatusMessage(String message) {
		SwingUtilities.invokeLater(() -> {
			try {
				SimpleAttributeSet keyWord = new SimpleAttributeSet();
				StyleConstants.setForeground(keyWord, STATUS_MESSAGE_COLOR);
				doc.insertString(doc.getLength(), message + "\n", keyWord);
			} catch (BadLocationException e) {
				e.printStackTrace();
			}
		});
	}

	/**
	 * Clears the text from the console output.
	 */
	public void clearConsole() {
		SwingUtilities.invokeLater(() -> textPaneConsoleOutput.setText(""));
	}

	/**
	 * An OutputStream that writes to a JTextPane.
	 */
	private class TextPaneOutputStream extends OutputStream {
//		private final JTextPane textPane;

		/**
		 * Constructs a new TextPaneOutputStream that writes to the given JTextPane.
		 * 
		 * @param textPane The JTextPane to write to
		 */
		public TextPaneOutputStream(JTextPane textPane) {
//			this.textPane = textPane;
		}

		@Override
		/**
		 * Writes the specified byte to the text pane console output.
		 * 
		 * @param b The byte to be written
		 */
		public void write(int b) {
			SwingUtilities.invokeLater(() -> {
				try {
					SimpleAttributeSet attributes = new SimpleAttributeSet();
					StyleConstants.setForeground(attributes, REGULAR_MESSAGE_COLOR);
					doc.insertString(doc.getLength(), String.valueOf((char) b), attributes);
				} catch (BadLocationException e) {
					e.printStackTrace();
				}
			});
		}
	}

	/**
	 * Test method
	 */
	public static void main(String[] args) {
		SwingUtilities.invokeLater(() -> {
			JFrame frame = new JFrame("ConsolePanel Test");
			ConsolePanel consolePanel = new ConsolePanel(true);

			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
			frame.setLayout(new BorderLayout());
			frame.add(consolePanel, BorderLayout.CENTER);
			frame.setSize(600, 400);
			frame.setVisible(true);

			// Example usage of postStatusMessage
			consolePanel.postStatusMessage("Algorithm is running...");
			System.out.println("test");
			consolePanel.postStatusMessage("Algorithm stopped.");

			System.out.println("test");
		});
	}

	public void appendLine(String line) {
		textPaneConsoleOutput.setText(textPaneConsoleOutput.getText() + newline + line);
	}

//	public void appendLine(String line) {
//		textPaneConsoleOutput.prin
//	}
}
