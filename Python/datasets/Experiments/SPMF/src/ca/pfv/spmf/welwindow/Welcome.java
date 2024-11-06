package ca.pfv.spmf.welwindow;

import java.awt.BorderLayout;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

import ca.pfv.spmf.gui.AboutWindow;
import ca.pfv.spmf.gui.Main;
import ca.pfv.spmf.gui.MainWindow;
import ca.pfv.spmf.gui.workflow_editor.WorkflowEditorWindow;

/*
 * Copyright (c) 2008-2019 Philippe Fournier-Viger
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

public class Welcome extends JFrame {
	public static final long serialVersionUID = 1L;
	private JButton buttonDatasetTools;
	private JButton buttonRunAlgorithm;
	private JButton buttonPlugins;
	private JButton buttonRunManyAlgorithms;
	private JButton buttonDocumentation;
//	private JButton buttonPreferences;
	private JButton buttonAboutSPMF;
	private JLabel labelWhatWouldYouLike;
	private JLabel labelLogo;
	private JPanel panelMain;

	public Welcome() {
		setTitle("SPMF v." + Main.SPMF_VERSION + " - Welcome");
		setSize(900, 175);
		setLocationRelativeTo(null);
		setResizable(false);
		setDefaultCloseOperation(EXIT_ON_CLOSE);
		initComponents();
		setVisible(true);
	}

	private void initComponents() {
	    JFrame frame = this;
	    frame.setTitle("SPMF v." + Main.SPMF_VERSION + " - Welcome");
//	    frame.setSize(900, 175);
	    frame.setLocationRelativeTo(null);
//	    frame.setResizable(false);
	    frame.setLayout(new BorderLayout()); // Set the layout manager to BorderLayout

	    // Initialize buttons and labels
	    buttonDatasetTools = new JButton("Prepare data (dataset tools)");
	    buttonRunAlgorithm = new JButton("Run a data algorithm");
	    buttonPlugins = new JButton("Add/Remove plugins");
	    buttonRunManyAlgorithms = new JButton("Run many data mining algorithm(s)");
	    buttonDocumentation = new JButton("Online documentation");
	    buttonAboutSPMF = new JButton("About SPMF");
	    labelWhatWouldYouLike = new JLabel("What would you like to do?", SwingConstants.CENTER);
	    labelLogo = new JLabel(new ImageIcon(Welcome.class.getResource("spmf.png")));

	    // Set icons for buttons
	    buttonDocumentation.setIcon(new ImageIcon(Welcome.class.getResource("/ca/pfv/spmf/gui/icons/Information24.gif")));
	    buttonAboutSPMF.setIcon(new ImageIcon(Welcome.class.getResource("/ca/pfv/spmf/gui/icons/About24.gif")));
//
	    // North panel with labelLogo and labelWhatWouldYouLike
	    JPanel northPanel = new JPanel(new BorderLayout());
	    northPanel.add(labelLogo, BorderLayout.NORTH);
	    northPanel.add(labelWhatWouldYouLike, BorderLayout.SOUTH);

	    // South panel with buttons aligned vertically
	    JPanel southPanel = new JPanel(new GridLayout(3, 1));
	    southPanel.add(buttonDatasetTools);
	    southPanel.add(buttonRunAlgorithm);
	    southPanel.add(buttonRunManyAlgorithms);

	    // East panel with buttons aligned vertically
	    JPanel eastPanel = new JPanel(new GridLayout(3, 1));
	    eastPanel.add(buttonDocumentation);
	    eastPanel.add(buttonPlugins);

	    // Adding panels to the main panel
	    panelMain = new JPanel(new BorderLayout()); // Panel using BorderLayout
	    panelMain.add(northPanel, BorderLayout.NORTH);
	    panelMain.add(southPanel, BorderLayout.CENTER);
	    panelMain.add(eastPanel, BorderLayout.EAST);


	    panelMain.validate();
	    setupButtonEvents(frame);
	    frame.setContentPane(panelMain);
	    frame.pack();
	    frame.setVisible(true);
	    frame.setDefaultCloseOperation(Welcome.EXIT_ON_CLOSE);
	}


	/** Setup the button events for a frame
	 * 
	 * @param frame the frame
	 */
	private void setupButtonEvents(JFrame frame) {
		buttonDocumentation.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				actionDocumentation(evt);
			}
		});
		
		buttonAboutSPMF.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				actionAboutSPMF(evt);
			}
		}); 
		
		buttonDatasetTools.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				try {
					actionDatasetTools(evt);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
		
		buttonRunAlgorithm.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				try {
					actionRunAlgorithm(evt);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});

		buttonPlugins.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
				actionPlugins(evt);
			}
		});
		
		buttonRunManyAlgorithms.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent e) {
//				MainWindow mainWindowTools;
				try {
					@SuppressWarnings("unused")
					WorkflowEditorWindow drawFrame = new WorkflowEditorWindow(false);
				} catch (Exception e1) {
					e1.printStackTrace();
				}
			}
		});
	}

	private void actionDatasetTools(ActionEvent evt) throws Exception {
		MainWindow mainWindowTools = new MainWindow(true, false, false);
		mainWindowTools.setDefaultCloseOperation(Welcome.HIDE_ON_CLOSE);
		mainWindowTools.setVisible(true);
	}

	private void actionRunAlgorithm(ActionEvent evt) throws Exception {
		MainWindow window = new MainWindow(false, true, false);
		window.setDefaultCloseOperation(Welcome.HIDE_ON_CLOSE);
		window.setVisible(true);
	}

	private void actionPlugins(ActionEvent evt) {
		PluginWindow mainplugin = new PluginWindow(this);
		mainplugin.setDefaultCloseOperation(Welcome.HIDE_ON_CLOSE);
	}

	private void actionDocumentation(ActionEvent evt) {

		String url = "http://www.philippe-fournier-viger.com/spmf/index.php?link=documentation.php";
		try {
			java.awt.Desktop.getDesktop().browse(java.net.URI.create(url));
		} catch (java.io.IOException e) {
			System.out.println(e.getMessage());
		}
	}

	private void actionAboutSPMF(ActionEvent evt) {
		AboutWindow about;
		try {
			about = new AboutWindow(this);
			about.setVisible(true);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		SwingUtilities.invokeLater(Welcome::new);
	}
}
