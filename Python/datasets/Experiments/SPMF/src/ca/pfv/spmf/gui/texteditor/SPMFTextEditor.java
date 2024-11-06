package ca.pfv.spmf.gui.texteditor;

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
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.GraphicsEnvironment;
import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.ComponentEvent;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;

import javax.swing.ImageIcon;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.event.CaretEvent;
import javax.swing.event.CaretListener;
import javax.swing.event.ListSelectionEvent;
import javax.swing.event.ListSelectionListener;
import javax.swing.text.BadLocationException;
import javax.swing.text.DefaultHighlighter;
import javax.swing.text.Highlighter;

import ca.pfv.spmf.gui.preferences.PreferencesManager;

/**
 * This is a simple text editor, adapted for SPMF.
 * 
 * @author Philippe Fournier-Viger
 */

public class SPMFTextEditor implements ActionListener {
	/** The text area */
	JTextArea textAreaX;

	/** The JFrame */
	JFrame frame;

	/** A JScrollpane so as to have scrollbars */
	JScrollPane scrollPane = null;

	/** An object to highlight the current line in the text area */
	LinePainter linePainter = null;

	/** Flag indicating if the application is run as a standalone program or not */
	boolean runAsStandalone = true;

	/** If true the nightmode is activated. Otherwise not */
	boolean nightMode = false;

	/** The status bar */
	private JTextField statusBar;

	/** The search bar */
	private JTextField searchBar;

	/** The search bar panel */
	JPanel searchBarPanel;

	/** The path of the current file */
	String currentFilePath = null;

	/** The name of the current file */
	String currentFileName = "Untitled";

	/** The color used for highlighting words that we search */
	Color colorSearchHighlights = Color.ORANGE;

	/** List of current objects highlighted by the search bar */
	java.util.List<Object> currentHighlightTags = new ArrayList<Object>();

	/** current file size */
	double currentFileSize = 0;

	/** Tool to manage undo */
	UndoTool undoTool;

	/**
	 * Constructor
	 * 
	 * @param runAsStandalone true if run as a standalone program, otherwise false
	 */
	public SPMFTextEditor(boolean runAsStandalone) {

		// ============== Load preferences from registry ======================
		boolean nightMode = PreferencesManager.getInstance().getNightMode();
		int fontsize = PreferencesManager.getInstance().getTextEditorFontSize();

		boolean lineWrap = PreferencesManager.getInstance().getTextEditorLineWrap();
		boolean wordWrap = PreferencesManager.getInstance().getTextEditorWordWrap();
		String fontFamilly = PreferencesManager.getInstance().getFontFamilly();

		int windowwidth = PreferencesManager.getInstance().getTextEditorWidth();
		int windowheight = PreferencesManager.getInstance().getTextEditorHeight();

		int textareawidth = PreferencesManager.getInstance().getTextEditorAreaWidth();
		int textareaheight = PreferencesManager.getInstance().getTextEditorAreaHeight();

		// Get the previous position of the window
		int texteditorXposition = PreferencesManager.getInstance().getTextEditorX();
		int texteditorYposition = PreferencesManager.getInstance().getTextEditorY();

		// Get the effective screen area
		java.awt.Rectangle screenArea = getEffectiveScreenArea();

		// Adjust the window position to make sure it is not outside the effective
		// screen area
		int minX = screenArea.x;
		int maxX = screenArea.width - windowwidth;
		texteditorXposition = Math.max(minX, texteditorXposition);
		texteditorXposition = Math.min(maxX, texteditorXposition);

		int minY = screenArea.y;
		int maxY = screenArea.height - windowheight;
		texteditorYposition = Math.max(minY, texteditorYposition);
		texteditorYposition = Math.min(maxY, texteditorYposition);
		// ========================================================

		// Set decoration for this window
//		JFrame.setDefaultLookAndFeelDecorated(true);

		// Create a new Jframe
		frame = new JFrame("SPMF Text Editor - " + currentFileName);
		frame.setIconImage(Toolkit.getDefaultToolkit()
				.getImage(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/History24.gif")));

		// Set the position and size of the JFrame
		frame.setSize(windowwidth, windowheight);

		// Set the window in the center of the screen
		frame.setLocationRelativeTo(null);

		/// ===== CODE TO DETECT IF THE WINDOW IS RESIZED ======
		frame.addComponentListener(new java.awt.event.ComponentListener() {

			@Override
			public void componentResized(ComponentEvent e) {
				// If the window is resize, we remember the size so that
				// next time we start the application we can use it again
				PreferencesManager.getInstance().setTextEditorAreaHeight(scrollPane.getHeight());
				PreferencesManager.getInstance().setTextEditorAreaWidth(scrollPane.getWidth());
				PreferencesManager.getInstance().setTextEditorHeight(frame.getHeight());
				PreferencesManager.getInstance().setTextEditorWidth(frame.getWidth());
			}

			@Override
			public void componentMoved(ComponentEvent e) {
				// if the window is moved, we remember the position so that
				// next time we start the application we can use the same position
				PreferencesManager.getInstance().setTextEditorX(frame.getX());
				PreferencesManager.getInstance().setTextEditorY(frame.getY());
			}

			@Override
			public void componentShown(ComponentEvent e) {
			}

			@Override
			public void componentHidden(ComponentEvent e) {
			}

		});
		// ========================================================

		// Save the preferences if the user want to run as a standalone application or
		// not
		this.runAsStandalone = runAsStandalone;

		// Set the close operation when the user click to close the window
		if (runAsStandalone) {
			frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		} else {
			frame.setDefaultCloseOperation(JFrame.HIDE_ON_CLOSE);
		}

		// Create a text component for showing the text of the text editor
		textAreaX = new JTextArea();

		// When the user move the caret in the text area, we will update the status bar
		textAreaX.addCaretListener(new CaretListener() {
			public void caretUpdate(CaretEvent e) {
				// call function to update the status bar
				updateStatusBar();
			}
		});

		// Set whether line wrap and word wrap features should be activated
		textAreaX.setLineWrap(lineWrap);
		textAreaX.setWrapStyleWord(wordWrap);

		// Read font size preference
		setFontSize(fontsize);
		setFontFamilly(fontFamilly);

		// Create a menubar
		JMenuBar mb = new JMenuBar();

		// ================ FILE MENU ======================
		JMenu menuFile = new JMenu("File");

		JMenuItem menuFileNew = new JMenuItem("New");
		menuFileNew.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/New24.gif")));
		menuFileNew.addActionListener(this);
		menuFile.add(menuFileNew);

		JMenuItem menuFileOpen = new JMenuItem("Open");
		menuFileOpen.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/open.gif")));
		menuFileOpen.addActionListener(this);
		menuFile.add(menuFileOpen);

		JMenuItem menuFileSave = new JMenuItem("Save");
		menuFileSave.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/save.gif")));
		menuFileSave.addActionListener(this);
		menuFile.add(menuFileSave);

		JMenuItem menuFileSaveAs = new JMenuItem("Save as...");
		menuFileSaveAs.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/SaveAs24.gif")));
		menuFileSaveAs.addActionListener(this);
		menuFile.add(menuFileSaveAs);

		menuFile.addSeparator();

		JMenuItem menuFilePrint = new JMenuItem("Print");
		menuFilePrint.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/print.gif")));
		menuFilePrint.addActionListener(this);
		menuFile.add(menuFilePrint);

		if (runAsStandalone) {
			menuFile.addSeparator();
			JMenuItem menuFileQuit = new JMenuItem("Quit");
			menuFileQuit.addActionListener(this);
			menuFile.add(menuFileQuit);
		}

		mb.add(menuFile);

		// ================ EDIT MENU ======================
		JMenu menuEdit = new JMenu("Edit");

		// Create menu items
		JMenuItem menuItemUndo = new JMenuItem("Undo");
		menuItemUndo.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/Undo24.gif")));
		menuItemUndo.addActionListener(this);
		menuEdit.add(menuItemUndo);

		JMenuItem menuItemRedo = new JMenuItem("Redo");
		menuItemRedo.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/Redo24.gif")));
		menuItemRedo.addActionListener(this);
		menuEdit.add(menuItemRedo);

		menuEdit.addSeparator();

		JMenuItem menuEditCut = new JMenuItem("Cut");
		menuEditCut.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/Cut24.gif")));
		menuEditCut.addActionListener(this);
		menuEdit.add(menuEditCut);

		JMenuItem menuEditCopy = new JMenuItem("Copy");
		menuEditCopy.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/Copy24.gif")));
		menuEditCopy.addActionListener(this);
		menuEdit.add(menuEditCopy);

		JMenuItem menuEditPaste = new JMenuItem("Paste");
		menuEditPaste.setIcon(new ImageIcon(SPMFTextEditor.class.getResource("/ca/pfv/spmf/gui/icons/Paste24.gif")));
		menuEditPaste.addActionListener(this);
		menuEdit.add(menuEditPaste);

		menuEdit.addSeparator();

		JMenuItem menuSelectAll = new JMenuItem("Select all");
		menuSelectAll.addActionListener(this);
		menuEdit.add(menuSelectAll);

		mb.add(menuEdit);

		// ================ VIEW MENU ======================
		JMenu menuView = new JMenu("View");

		JCheckBoxMenuItem menuLineWrap = new JCheckBoxMenuItem("Line wrap");
		JCheckBoxMenuItem menuWordWrap = new JCheckBoxMenuItem("Word wrap");

		menuLineWrap.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setLineWrap(menuLineWrap.isSelected());
				if (menuLineWrap.isSelected() == false) {
					menuWordWrap.setSelected(false);
					setWordWrap(false);
				}
			}
		});
		menuLineWrap.setSelected(lineWrap);
		menuView.add(menuLineWrap);

		menuWordWrap.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setWordWrap(menuWordWrap.isSelected());
				if (menuWordWrap.isSelected()) {
					menuLineWrap.setSelected(true);
					setLineWrap(true);
				}

			}
		});
		menuWordWrap.setSelected(wordWrap);
		menuView.add(menuWordWrap);

		menuView.addSeparator();

		JCheckBoxMenuItem menuNightMode = new JCheckBoxMenuItem("Night mode");
		menuNightMode.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setNightMode(menuNightMode.isSelected());
			}
		});

		// Set the night mode to false
		menuNightMode.setSelected(nightMode);

		menuView.add(menuNightMode);

		menuView.addSeparator();

		JCheckBoxMenuItem menuSearchBar = new JCheckBoxMenuItem("Search bar");
		menuSearchBar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setSearchBar(menuSearchBar.isSelected());
			}
		});
		menuSearchBar.setSelected(true);
		menuView.add(menuSearchBar);

		JCheckBoxMenuItem menuStatusBar = new JCheckBoxMenuItem("Status bar");
		menuStatusBar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				setStatusBar(menuStatusBar.isSelected());
			}
		});
		menuStatusBar.setSelected(true);
		menuView.add(menuStatusBar);

		menuView.addSeparator();

		JMenuItem menuFontFamilly = new JMenuItem("Font familly");
		menuFontFamilly.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				chooseFontFamilly();
			}
		});
		menuView.add(menuFontFamilly);

		JMenuItem menuSetFontSize = new JMenuItem("Font size");
		menuSetFontSize.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				int fontSize = PreferencesManager.getInstance().getTextEditorFontSize();

				String result = JOptionPane.showInputDialog("Enter font size:", fontSize);

				if (result != null) {
					try {
						int fontsize = Integer.parseInt(result);
						if (fontsize > 0) {
							setFontSize(fontsize);
						} else {
							JOptionPane.showInternalMessageDialog(null, "Font size must be a positive number.");
						}
					} catch (Exception exception) {
						JOptionPane.showInternalMessageDialog(null, "Font size must be a positive number.");
					}
				}
			}
		});
		menuView.add(menuSetFontSize);

		mb.add(menuView);
		// ===============================================
		// Add the menubar
		frame.setJMenuBar(mb);
		frame.getContentPane().setLayout(new BorderLayout(1, 0));

		// Put the text area in a scroll pane
		scrollPane = new JScrollPane(textAreaX);
		scrollPane.setPreferredSize(new Dimension(textareawidth, textareaheight));
		frame.getContentPane().add(scrollPane, BorderLayout.CENTER);

////*******************************
//		TextLineNumber tln = new TextLineNumber(textAreaX, scrollPane, 3);
		scrollPane.setRowHeaderView(new LineNumberPane(textAreaX));

		// *********************************************/

		// Create the status bar
		statusBar = new JTextField();
		statusBar.setText("test");
		statusBar.setEditable(false);
		statusBar.setEnabled(true);
		statusBar.setColumns(10);
		frame.getContentPane().add(statusBar, BorderLayout.SOUTH);

		// Create the search bar and put it in a search panel
		searchBar = new JTextField();
		searchBar.addCaretListener(new CaretListener() {
			public void caretUpdate(CaretEvent e) {
				find();
			}
		});
		searchBar.setText("");
		searchBar.setEditable(true);
		searchBar.setEnabled(true);
		searchBar.setColumns(10);
		searchBarPanel = new JPanel(new BorderLayout(1, 0));
		JLabel searchBarLabel = new JLabel();
		searchBarLabel.setIcon(null);
		searchBarLabel.setText("Search: ");
		searchBarPanel.add(searchBarLabel, BorderLayout.WEST);
		searchBarPanel.add(searchBar, BorderLayout.CENTER);
		frame.getContentPane().add(searchBarPanel, BorderLayout.NORTH);

		/// *************************** USE THE TOOL TO HIGHLIGHT THE CURRENT LINE
		linePainter = new LinePainter(textAreaX);
		// ****************************************************

		/*** Add the undo tool **/
		undoTool = new UndoTool(textAreaX);

		setNightMode(nightMode);

		// Update the status bar
		updateStatusBar();

		// Show the frame
		frame.pack();
		frame.setVisible(true);
	}

	private java.awt.Rectangle getEffectiveScreenArea() {
		int minX = 0, minY = 0, maxX = 0, maxY = 0;
		GraphicsEnvironment environment = GraphicsEnvironment.getLocalGraphicsEnvironment();
		int screenDevices = environment.getScreenDevices().length;
		for (java.awt.GraphicsDevice device : environment.getScreenDevices()) {
			java.awt.Rectangle bounds = device.getDefaultConfiguration().getBounds();
			minX = Math.min(minX, bounds.x);
			minY = Math.min(minY, bounds.y);
			maxX = Math.max(maxX, bounds.x + bounds.width);
			maxY = Math.max(maxY, bounds.y + bounds.height);
		}
		return new java.awt.Rectangle(minX, minY, (maxX - minX) / screenDevices, (maxY - minY) / screenDevices);
	}

	protected void chooseFontFamilly() {
		// Get current font
		java.awt.Font currentFont = textAreaX.getFont();
		String currentFontFamilly = currentFont.getFamily();

		GraphicsEnvironment ge = GraphicsEnvironment.getLocalGraphicsEnvironment();
		String fontNames[] = ge.getAvailableFontFamilyNames();
		int selectedIndex = 0;
		for (int i = 0; i < fontNames.length; i++) {
			if (fontNames[i].equals(currentFontFamilly)) {
				selectedIndex = i;
				break;
			}
		}

		JPanel panel = new JPanel(new BorderLayout(1, 0));
		JLabel label = new JLabel("This is an example");
		label.setFont(textAreaX.getFont());
		JList<String> jlist = new JList<String>(fontNames);
		jlist.setSelectedIndex(selectedIndex);
//		jlist.setSize(new Dimension(500,500));C
		jlist.addListSelectionListener(new ListSelectionListener() {
			public void valueChanged(ListSelectionEvent e) {
				String fontFamilly = (String) jlist.getSelectedValue();
				java.awt.Font currentFont = label.getFont();
				java.awt.Font newFont = new java.awt.Font(fontFamilly, currentFont.getStyle(), currentFont.getSize());
				label.setFont(newFont);
			}
		});
		JScrollPane scrollPane = new JScrollPane(jlist);
//		scrollPane.setMinimumSize(new Dimension(500,500));
		panel.add(scrollPane, BorderLayout.CENTER);
		panel.add(label, BorderLayout.SOUTH);
		JOptionPane.showMessageDialog(null, panel, "Choose font familly:", JOptionPane.QUESTION_MESSAGE);
//		System.out.println(comboBox.getSelectedIndex());

		// If the user selected a different font
		if (selectedIndex != jlist.getSelectedIndex()) {
			String fontFamilly = (String) jlist.getSelectedValue();
			setFontFamilly(fontFamilly);
		}
	}

	private void setFontFamilly(String fontFamilly) {
		java.awt.Font currentFont = textAreaX.getFont();
		java.awt.Font newFont = new java.awt.Font(fontFamilly, currentFont.getStyle(), currentFont.getSize());
		textAreaX.setFont(newFont);
		PreferencesManager.getInstance().setFontFamilly(fontFamilly);
		
		frame.revalidate();
		frame.repaint();
	}

	/**
	 * Show or hide the search bar
	 * 
	 * @param selected if true, show. if false, hide
	 */
	protected void setSearchBar(boolean selected) {
		searchBarPanel.setVisible(selected);
		frame.getContentPane().revalidate();
		frame.getContentPane().repaint();
	}

	/**
	 * Activate or deactivate WordWrap
	 * 
	 * @param selected True = activate, False = deactivate
	 */
	protected void setWordWrap(boolean selected) {
		textAreaX.setWrapStyleWord(selected);

		PreferencesManager.getInstance().setTextEditorWordWrap(selected);
	}

	/**
	 * Show or hide the status bar
	 * 
	 * @param selected if true, show. if false, hide
	 */
	protected void setStatusBar(boolean selected) {
		statusBar.setVisible(selected);
		frame.getContentPane().revalidate();
		frame.getContentPane().repaint();
	}

	/**
	 * Find the word in the search bar and highlight all its occurrences
	 */
	protected void find() {
		// Remove previous higlights
		for (Object tag : currentHighlightTags) {
			textAreaX.getHighlighter().removeHighlight(tag);
		}

		// Get the search term
		String query = searchBar.getText();

		// If no search term or text is empty, return
		if (query.isEmpty() || (textAreaX.getText().isEmpty())) {
			return;
		}

		int theOffset = textAreaX.getText().indexOf(query);
		int charCount = query.length();

		Highlighter.HighlightPainter paint = new DefaultHighlighter.DefaultHighlightPainter(colorSearchHighlights);

		while (theOffset != -1) {
			try {
				Object highlightTag = textAreaX.getHighlighter().addHighlight(theOffset, charCount + theOffset, paint);
				int newOffset = theOffset + 1;
				theOffset = textAreaX.getText().indexOf(query, newOffset);

				currentHighlightTags.add(highlightTag);

			} catch (BadLocationException ex) {
				System.err.print(ex.getStackTrace());
			}
		}
	}

	/**
	 * Activate or deactivate the night mode
	 * 
	 * @param selected true = activate, otherwise deactivate
	 */
	protected void setNightMode(boolean selected) {
		// If night mode
		if (selected) {
			textAreaX.setBackground(Color.BLACK);
			textAreaX.setForeground(Color.WHITE);
			if (linePainter != null) {
				linePainter.setColor(Color.GRAY);
			}
			colorSearchHighlights = Color.RED;
			find();
		} else {
			// Otherwise
			textAreaX.setBackground(Color.WHITE);
			textAreaX.setForeground(Color.BLACK);
			if (linePainter != null) {
				linePainter.setLighter(Color.LIGHT_GRAY);
			}
			colorSearchHighlights = Color.ORANGE;
			find();
		}

		PreferencesManager.getInstance().setNightMode(selected);
	}

	/**
	 * Set font size
	 * 
	 * @param fontsize the font size
	 */
	/**
	 * Increase the font size by 2
	 */
	protected void setFontSize(int fontsize) {
		java.awt.Font newFont = textAreaX.getFont().deriveFont((float) fontsize);
		textAreaX.setFont(newFont);

		PreferencesManager.getInstance().setTextEditorFontSize(fontsize);
		
		frame.revalidate();
		frame.repaint();
	}

	/**
	 * Update the status bar
	 */
	protected void updateStatusBar() {
		int caretPosition = textAreaX.getCaretPosition();
		int columnPosition = 1;
		int linePosition = 1;
		try {
			linePosition = textAreaX.getLineOfOffset(caretPosition);
			columnPosition = caretPosition - textAreaX.getLineStartOffset(linePosition);
			linePosition = linePosition + 1;
			statusBar.setText("Line: " + linePosition + "\tColumn: " + columnPosition + "\t Line count: "
					+ textAreaX.getLineCount());
		} catch (Exception exception) {
			System.err.println(exception.getStackTrace());
			statusBar.setText(" ");
		}
	}

	/**
	 * Activate or deactivate the line wrap function
	 * 
	 * @param selected if true, activate, otherwise, deactivate
	 */
	protected void setLineWrap(boolean selected) {
		textAreaX.setLineWrap(selected);

		PreferencesManager.getInstance().setTextEditorLineWrap(selected);
	}

	// If a button is pressed
	public void actionPerformed(ActionEvent actionEvent) {
		String actionCommand = actionEvent.getActionCommand();

		if (actionCommand.equals("Cut")) {
			textAreaX.cut();
		} else if (actionCommand.equals("Copy")) {
			textAreaX.copy();
		} else if (actionCommand.equals("Paste")) {
			textAreaX.paste();
		} else if (actionCommand.equals("Undo")) {
			undoTool.undo();
		} else if (actionCommand.equals("Redo")) {
			undoTool.redo();
		} else if (actionCommand.equals("Quit")) {
			if (runAsStandalone) {
				System.exit(0);
			} else {
				frame.setVisible(false);
			}
		} else if (actionCommand.equals("Save")) {
			save();
		} else if (actionCommand.equals("Save as...")) {
			saveAs();
		} else if (actionCommand.equals("Select all")) {
			textAreaX.select(0, textAreaX.getText().length());
		} else if (actionCommand.equals("Print")) {
			try {
				textAreaX.print();
			} catch (Exception exception) {
				// If error
				JOptionPane.showMessageDialog(frame, exception.getMessage());
			}
		} else if (actionCommand.equals("Open")) {
			// Ask user to select a file using file chooser
			JFileChooser fileChooser = new JFileChooser();
			int resultCode = fileChooser.showOpenDialog(null);

			// If the user selected a file
			if (JFileChooser.APPROVE_OPTION == resultCode) {
				File file = new File(fileChooser.getSelectedFile().getAbsolutePath());

				openAFile(file);
			}
		} else if (actionCommand.equals("New")) {
			setCurrentFile(null, "untitled");
			textAreaX.setText("");
		}
	}

	/**
	 * Load a file
	 * 
	 * @param file the file
	 */
	public void openAFile(File file) {
		currentFileSize = file.length() / 1024d / 1024d;

		// Remember the file name and path.
		String absolutePath = file.getAbsolutePath();
		String filename = file.getName();
		setCurrentFile(absolutePath, filename);

		try {
			// Create reader object
//			BufferedReader reader = new BufferedReader(new FileReader(file));	

			// The text content
//			String content = reader.readLine();
//			String line = "";
//			
//			// Take the input from the file
//			while ((line = reader.readLine()) != null) {
//				content = content + System.lineSeparator() + line;
//			}
			String content = new String(Files.readAllBytes(Paths.get(absolutePath)));

			// Set the text
			textAreaX.setText(content);
			// update the status bar
			updateStatusBar();
		} catch (Exception exception) {
			// Show error if there is one
			JOptionPane.showMessageDialog(frame, exception.getMessage());
		}
	}

	/**
	 * Save to file
	 */
	private void save() {
		// If no file was open before
		if (currentFilePath == null) {
			// We open the SaveAs function
			saveAs();
		} else {
			// Otherwise, we will save in the same location as the currently opened file
			try {
				String text = textAreaX.getText();
				File file = new File(currentFilePath);
				BufferedWriter w = new BufferedWriter(new FileWriter(file, false));
				w.write(text);
				w.flush();
				w.close();
				currentFileSize = file.length() / 1024d / 1024d;
			} catch (Exception event) {
				// If error, then show a message
				JOptionPane.showMessageDialog(frame, event.getMessage());
			}
		}
	}

	/**
	 * Save the currently opened file as.
	 */
	private void saveAs() {
		// Use a Jfilechooser to ask the user to select the location
		JFileChooser fileChooser = new JFileChooser();
		int resultCode = fileChooser.showSaveDialog(null);

		// If the user has selected a location
		if (JFileChooser.APPROVE_OPTION == resultCode) {
			// Remember the file name and path.
			String absolutePath = fileChooser.getSelectedFile().getAbsolutePath();
			String filename = fileChooser.getSelectedFile().getName();
			setCurrentFile(absolutePath, filename);
			try {
				// Open the file
				File file = new File(absolutePath);
				BufferedWriter writer = new BufferedWriter(new FileWriter(file, false));
				writer.write(textAreaX.getText());
				writer.flush();
				writer.close();
				currentFileSize = file.length() / 1024d / 1024d;
			} catch (Exception event) {
				// If some problem occurs... show a message
				JOptionPane.showMessageDialog(frame, event.getMessage());
			}
		}
	}

	/**
	 * Set information about the currently opened file
	 * 
	 * @param currentFilePath the file path
	 * @param currentFileName the file name
	 */
	void setCurrentFile(String currentFilePath, String currentFileName) {
		this.currentFilePath = currentFilePath;
		this.currentFileName = currentFileName;
		if (currentFilePath != null) {
			String fileSize = String.format("%.4f", currentFileSize);
			frame.setTitle("SPMF Text Editor  -  " + currentFileName + "   (" + fileSize + " MB)");
		} else {
			currentFileSize = 0;
			frame.setTitle("SPMF Text Editor  -  " + currentFileName);
		}
	}

}