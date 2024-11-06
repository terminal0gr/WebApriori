package ca.pfv.spmf.gui.developerswindow;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.UnsupportedLookAndFeelException;

import ca.pfv.spmf.gui.Main;
import ca.pfv.spmf.gui.MainWindow;
import ca.pfv.spmf.gui.algorithmexplorer.AlgorithmExplorer;
import ca.pfv.spmf.gui.preferences.PreferencesViewer;
import ca.pfv.spmf.gui.web.WebpageAlgorithmDocViewer;
/*
 * Copyright (c) 2022 Philippe Fournier-Viger
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
 * JFrame to provide tools for developers.
 * 
 * @author Philippe Fournier-Viger
 *
 */
public class DevelopersToolsWindow extends JFrame implements ActionListener {

	/** serial UID */
	private static final long serialVersionUID = 6003542342904279422L;
	/** The JPanel */
	private JPanel panel;
	/** The buttons */
	private JButton preferencesButton, findDocButton, simpleAlgorithmButton, webpageAlgorithmButton,
			algorithmExplorerButton, outputInputAlgorithmButton, authorCountButton, categoryCountButton, typeCountButton, 
			algorithmByInputButton, systemInfoButton, downloadDocumentation;

	/**
	 * Constructor
	 * 
	 * @throws UnsupportedLookAndFeelException
	 * @throws IllegalAccessException
	 * @throws InstantiationException
	 * @throws ClassNotFoundException
	 */
	public DevelopersToolsWindow(boolean runAsStandalone) throws ClassNotFoundException, InstantiationException,
			IllegalAccessException, UnsupportedLookAndFeelException {
		setTitle("SPMF Developers Tools " + Main.SPMF_VERSION);
		setDefaultCloseOperation(runAsStandalone ? JFrame.EXIT_ON_CLOSE : JFrame.DISPOSE_ON_CLOSE);
		panel = new JPanel(new GridLayout(5, 2, 5, 5));
		initializeButtons();
		addComponentsToPanel();
		getContentPane().add(panel, BorderLayout.CENTER);
		setSize(800, 400);
		setLocationRelativeTo(null);
		setVisible(true);
	}

	/** Initialize the buttons
	 * 
	 */
	private void initializeButtons() {
		preferencesButton = createButton("View user preferences in registry");
		findDocButton = createButton("Find broken URLs in SPMF documentation");
		algorithmExplorerButton = createButton("Algorithm Manager");
		simpleAlgorithmButton = createButton("View and export list of algorithms");
		webpageAlgorithmButton = createButton("View documentation via internal browser");
		outputInputAlgorithmButton = createButton("All Input/Output Types");
		authorCountButton = createButton("Algorithm count by authors");
		categoryCountButton = createButton("Algorithm count by category");
		typeCountButton = createButton("Algorithm count by internal type");
		algorithmByInputButton = createButton("Algorithms by input type");
		systemInfoButton = createButton("System information");
		downloadDocumentation = createButton("Download offline documentation to /doc/ folder");
	}

	/**
	 * Create a button
	 * @param text the name
	 * @return the button
	 */
	private JButton createButton(String text) {
		JButton button = new JButton(text);
		button.addActionListener(this);
		return button;
	}

	/** Add components to the panel */
	private void addComponentsToPanel() {
		JLabel labelSPMF = new JLabel(new ImageIcon(MainWindow.class.getResource("spmf.png")));
		panel.add(labelSPMF);
		panel.add(simpleAlgorithmButton);
		panel.add(outputInputAlgorithmButton);
		panel.add(algorithmByInputButton);
//		panel.add(algorithmExplorerButton);
		panel.add(authorCountButton);
		panel.add(categoryCountButton);
		panel.add(typeCountButton);
		panel.add(findDocButton);
		panel.add(preferencesButton);
//		panel.add(webpageAlgorithmButton);
		panel.add(systemInfoButton);
		panel.add(downloadDocumentation);
	}

	@Override
	public void actionPerformed(ActionEvent e) {
		Object source = e.getSource();
		try {
			if (source == preferencesButton) {
				new PreferencesViewer().setVisible(true);
			} else if (source == findDocButton) {
				new FindDocBrokenURLsViewer();
			} else if (source == simpleAlgorithmButton) {
				new AlgorithmListExporterWindow(false);
			} else if (source == webpageAlgorithmButton) {
				new WebpageAlgorithmDocViewer();
			} else if (source == algorithmExplorerButton) {
				new AlgorithmExplorer(false);
			} else if (source == outputInputAlgorithmButton) {
				new InputOutputTypeListWindow(false);
			} else if (source == authorCountButton) {
				new AuthorAlgorithmCountWindow(false);
			} else if (source == algorithmByInputButton) {
				new InputTypeListWindow(false);
			}else if (source == systemInfoButton) {
				new SystemInfoDisplay(false);
			}else if (source == categoryCountButton) {
				new CategoryAlgorithmCountWindow(false);
			}else if (source == typeCountButton) {
				new TypeAlgorithmCountWindow(false);
			}else if (source == downloadDocumentation) {
				DocumentationDownloaderWindow window = new DocumentationDownloaderWindow();
				window.createAndShowGUI();
			}
		} catch (Exception e1) {
			e1.printStackTrace();
		}
	}

	/**
	 * Main method
	 */
	public static void main(String[] args) throws ClassNotFoundException, InstantiationException,
			IllegalAccessException, UnsupportedLookAndFeelException {
		new DevelopersToolsWindow(true);
	}

}
