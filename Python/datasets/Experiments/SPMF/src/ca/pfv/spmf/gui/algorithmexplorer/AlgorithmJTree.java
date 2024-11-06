package ca.pfv.spmf.gui.algorithmexplorer;

import java.util.Enumeration;
import java.util.List;

import javax.swing.JLabel;
import javax.swing.JTree;
import javax.swing.event.TreeSelectionListener;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeNode;

import ca.pfv.spmf.algorithmmanager.AlgorithmManager;
import ca.pfv.spmf.algorithmmanager.DescriptionOfAlgorithm;
import ca.pfv.spmf.algorithmmanager.DescriptionOfParameter;

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
 * JTree that displays the algorithms offered in SPMF
 * 
 * @author Philippe Fournier-Viger
 */
@SuppressWarnings("serial")
public class AlgorithmJTree extends JTree {

	/** indicate if the highlight function is activated for the JTree */
	boolean activatedHighlight = false;

	public boolean isActivatedHighlight() {
		return activatedHighlight;
	}

	public void setActivatedHighlight(boolean activatedHighlight) {
		this.activatedHighlight = activatedHighlight;
		repaint();
	}

	class AlgoNode {
		final String name;
		boolean isHighlight;
		boolean isCategory;

		public boolean isHighlight() {
			return isHighlight;
		}

		public void setHighlight(boolean isHighlight) {
			this.isHighlight = isHighlight;
		}

		public boolean isCategory() {
			return isCategory;
		}

		public void setCategory(boolean isCategory) {
			this.isCategory = isCategory;
		}

		AlgoNode(String name, boolean isCategory) {
			this.name = name;
			isHighlight = false;
			this.isCategory = isCategory;
		}

		@Override
		public String toString() {
			return name;
		}

		public String getName() {
			return name;
		}
	}

	public AlgorithmJTree(boolean showTools, boolean showAlgorithms, boolean showExperimentTools) {
		// Create the tree root
		super(new DefaultMutableTreeNode("Root"));
		this.setRootVisible(false);
		DefaultMutableTreeNode rootNode = (DefaultMutableTreeNode) getModel().getRoot();

		DefaultTreeModel defaultTreeModel = new DefaultTreeModel(rootNode);
		setModel(defaultTreeModel);

		// Get the algorithm manager
		AlgorithmManager manager = null;
		try {
			manager = AlgorithmManager.getInstance();
		} catch (Exception e1) {
			e1.printStackTrace();
		}

		// -----------------------------------------------------------------------------------

		// Get the list of algorithms or categories
		List<String> algorithmList = manager.getListOfAlgorithmsAsString(showTools, showAlgorithms,
				showExperimentTools);
		DefaultMutableTreeNode categoryNode = null;

		// For each algorithm or category
		for (String algorithmOrCategoryName : algorithmList) {
			// If a new category, create a node for the category
			if (manager.getDescriptionOfAlgorithm(algorithmOrCategoryName) == null) {
				AlgoNode newNode = new AlgoNode(algorithmOrCategoryName, true);
				categoryNode = new DefaultMutableTreeNode(newNode);

				addNodeToDefaultTreeModel(defaultTreeModel, rootNode, categoryNode);
			} else {
				AlgoNode newNode = new AlgoNode(algorithmOrCategoryName, false);
				// Otherwise, create an algorithm node for the current category
				addNodeToDefaultTreeModel(defaultTreeModel, categoryNode, new DefaultMutableTreeNode(newNode));
			}
		}

//        ImageIcon imageIcon = new ImageIcon(TreeExample.class.getResource("/leaf.jpg"));
		// set the renderer for the tree so as to be able to highlight tree node
		this.setCellRenderer(new DefaultTreeCellRenderer() {
			@Override
			public java.awt.Component getTreeCellRendererComponent(JTree tree, Object value, boolean sel,
					boolean expanded, boolean leaf, int row, boolean hasFocus) {
				JLabel label = (JLabel) super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row,
						hasFocus);
				// Special case for the root
				if (((DefaultMutableTreeNode) value).getUserObject() instanceof String) {
					return label;
				}
				// The case of other nodes
				AlgoNode node = (AlgoNode) ((DefaultMutableTreeNode) value).getUserObject();
				if (activatedHighlight && node.isHighlight()) {
					label.setForeground(java.awt.Color.BLUE);
				} else {
					label.setForeground(java.awt.Color.BLACK);
				}

				return label;
			}
		});
//        renderer.setLeafIcon(imageIcon);

		this.setShowsRootHandles(true);

//        setLayout(new BorderLayout());

		this.setVisible(true);
	}

	public void addTreeSelectionListener(TreeSelectionListener listener) {
		addTreeSelectionListener(listener);
	}

	private static void addNodeToDefaultTreeModel(DefaultTreeModel treeModel, DefaultMutableTreeNode parentNode,
			DefaultMutableTreeNode node) {

		treeModel.insertNodeInto(node, parentNode, parentNode.getChildCount());

		if (parentNode == treeModel.getRoot()) {
			treeModel.nodeStructureChanged((TreeNode) treeModel.getRoot());
		}
	}

	public void highlightSimilarAlgorithmsToSelection(boolean withParameters) {
		DefaultMutableTreeNode selectedNode = (DefaultMutableTreeNode) this.getLastSelectedPathComponent();
		String algoName = selectedNode.getUserObject().toString();
		// Get the algorithm manager
		AlgorithmManager manager = null;
		try {
			manager = AlgorithmManager.getInstance();
		} catch (Exception e1) {
			e1.printStackTrace();
		}
		DescriptionOfAlgorithm descriptionSelected = manager.getDescriptionOfAlgorithm(algoName);

		Enumeration<TreeNode> e = ((DefaultMutableTreeNode) getModel().getRoot()).depthFirstEnumeration();
		while (e.hasMoreElements()) {
			DefaultMutableTreeNode node = (DefaultMutableTreeNode) e.nextElement();
			if (node != getModel().getRoot()) {
				AlgoNode algonode = (AlgoNode) node.getUserObject();
				algonode.setHighlight(false);

				if (algonode.isCategory() == false) {
					DescriptionOfAlgorithm descriptionCurrent = manager.getDescriptionOfAlgorithm(algonode.getName());
					boolean sameInput = same(descriptionCurrent.getInputFileTypes(),
							descriptionSelected.getInputFileTypes());
					boolean sameOutput = same(descriptionCurrent.getOutputFileTypes(),
							descriptionSelected.getOutputFileTypes());

					if (sameInput && sameOutput) {
						if (withParameters == false) {
							algonode.setHighlight(true);
						} else {
							boolean sameParameters = sameMandatoryParameter(
									descriptionCurrent.getParametersDescription(),
									descriptionSelected.getParametersDescription(),
									descriptionCurrent.getNumberOfMandatoryParameters(),
									descriptionSelected.getNumberOfMandatoryParameters());
							if (sameParameters) {
								algonode.setHighlight(true);
							}
						}
					}

				}
//				System.out.println(algonode.getName());
			}
		}
		setActivatedHighlight(true);
	}

	private boolean sameMandatoryParameter(DescriptionOfParameter[] parametersDescription,
			DescriptionOfParameter[] parametersDescription2, int numberMandatoryParameters,
			int numberMandatoryParameters2) {
		if (numberMandatoryParameters != numberMandatoryParameters2) {
			return false;
		}
		for (int i = 0; i < numberMandatoryParameters; i++) {
			if (parametersDescription[i].getName().equals(parametersDescription2[i].getName()) == false) {
				return false;
			}
		}

		return true;
	}

	private boolean same(String[] outputFileTypes, String[] outputFileTypes2) {
		if (outputFileTypes == null && outputFileTypes2 == null) {
			return true;
		}
		if (outputFileTypes == null) {
			return false;
		}
		if (outputFileTypes2 == null) {
			return false;
		}
		if (outputFileTypes.length != outputFileTypes2.length) {
			return false;
		}
		for (int i = 0; i < outputFileTypes.length; i++) {
			if (outputFileTypes[i].equals(outputFileTypes2[i]) == false) {
				return false;
			}
		}

		return true;
	}

}