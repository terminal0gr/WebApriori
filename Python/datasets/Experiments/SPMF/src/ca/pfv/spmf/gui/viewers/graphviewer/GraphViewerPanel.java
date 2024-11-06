package ca.pfv.spmf.gui.viewers.graphviewer;

import java.awt.BasicStroke;
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
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.Image;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.RenderingHints;
import java.awt.event.ComponentAdapter;
import java.awt.event.ComponentEvent;
import java.awt.event.MouseEvent;
import java.awt.geom.AffineTransform;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import javax.imageio.ImageIO;
import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.event.MouseInputListener;

import ca.pfv.spmf.gui.preferences.PreferencesManager;
import ca.pfv.spmf.gui.viewers.graphviewer.graphlayout.AbstractGraphLayout;
import ca.pfv.spmf.gui.viewers.graphviewer.graphmodel.GEdge;
import ca.pfv.spmf.gui.viewers.graphviewer.graphmodel.GNode;
import ca.pfv.spmf.test.MainTestApriori_saveToFile;

/**
 * A special type of JPanel to visualize subgraphs.
 * 
 * @author Philippe Fournier-Viger
 *
 */
public class GraphViewerPanel extends JPanel implements MouseInputListener// , Scrollable
{
	/** Serial UID */
	private static final long serialVersionUID = -9054590513003092459L;

	/** Graph layout class */
	private AbstractGraphLayout graphLayoutGenerator;

	/** The list of nodes */
	private List<GNode> nodes;

	/** The list of edges */
	private List<GEdge> edges;

	/** The node that is currently dragged by the mouse */
	private GNode currentlyDraggedNode = null;

	/** The node that the mouse is currently over */
	private GNode currentlyMouseOverNode = null;

//	/** The edge that the mouse is currently over */
//	private GEdge currentlyMouseOverEdge = null;

	/** Maximum allowed value of X for nodes */
	int maxX;

	/** Maximum allowed value of Y for nodes */
	int maxY;

	/** This indicates the level of zoom */
	double scaleLevel = 1.0;

	/** Mouse button left is pressed */
	boolean mouseLeftIsPressed = false;

	/** Mouse button right is pressed */
	boolean mouseRightIsPressed = false;

	/** width */
	int width;

	/** height */
	int height;

	/** Highlight color for nodes */
	Color NODE_HIGHLIGHT_COLOR = Color.YELLOW;

	/** Node text size */
	private static int NODE_TEXT_SIZE = 10;
	
	/** Edge text size */
	private static int EDGE_TEXT_SIZE = 10;

	/** Color for nodes */
	private Color NODE_COLOR = new Color(235, 235, 235);

	/** Color for edges */
	private Color EDGE_COLOR = Color.BLUE;

	/** Color for node labels */
	private Color NODE_LABEL_COLOR = Color.BLACK;

	/** Color for edge labels */
	private Color EDGE_LABEL_COLOR = Color.BLACK;

	/** Color for node borders */
	private Color NODE_BORDER_COLOR = Color.BLACK;

	/** Background color */
	private Color CANVAS_COLOR = Color.WHITE;

	/** Anti-aliasing is activated */
	private boolean ANTI_ALIASING_ACTIVATED = false;

	/** Show node labels */
	private boolean SHOW_NODE_IDS = true;

	/** Show edge labels */
	private boolean SHOW_EDGE_IDS = true;

	/** Show node names */
	private boolean SHOW_NODE_LABELS = true;

	/** Show edge names */
	private boolean SHOW_EDGE_LABELS = true;

	/** Mouse previous X position */
	int mouseXPosition;

	/** Mouse previous Y position */
	int mouseYPosition;

	/**
	 * Constructor
	 */
	public GraphViewerPanel(AbstractGraphLayout graphLayoutGenerator, int i, int j) {
		addComponentListener(new ComponentAdapter() {
			@Override
			public void componentResized(ComponentEvent e) {
				resized(false);
			}
		});

		width = i;
		height = j;

		nodes = new ArrayList<GNode>();
		edges = new ArrayList<GEdge>();

		this.graphLayoutGenerator = graphLayoutGenerator;

		addMouseMotionListener(this);
		addMouseListener(this);

		setBackground(CANVAS_COLOR);
		resized(false);
	}

	public int getWidth() {
		return width;
	}

	public int getHeight() {
		return height;
	}

	/**
	 * Change the graph layout generator for this panel
	 * 
	 * @param graphLayoutGenerator a new graph layout generator
	 */
	public void setGraphLayoutGenerator(AbstractGraphLayout graphLayoutGenerator) {
		this.graphLayoutGenerator = graphLayoutGenerator;
	}

	/**
	 * Method that is called when the JPanel is resized to recalculate some values
	 * that depends on the size.
	 * 
	 * @param doAutoLayout
	 */
	protected void resized(boolean doAutoLayout) {
		maxX = getWidth() - GNode.getRadius();
		maxY = getHeight() - GNode.getRadius();

		// Make sure that all nodes remains inside the canvas
		for (GNode node : nodes) {
			boolean nodeIsOutsideCanvasX = (node.getCenterX() >= maxX);
			boolean nodeIsOutsideCanvasY = (node.getCenterY() >= maxY);

			if (nodeIsOutsideCanvasX || nodeIsOutsideCanvasY) {
				int x = nodeIsOutsideCanvasX ? maxX : node.getCenterX();
				int y = nodeIsOutsideCanvasY ? maxY : node.getCenterY();
				node.updatePosition(x, y);
			}
		}

		repaint();

		setPreferredSize(new Dimension(width, height));

		revalidate();

		if (doAutoLayout) {
			autoLayout();
		}
//		repaint();

	}

	/**
	 * Add an edge
	 * 
	 * @param newEdge a new edge
	 */
	public void addEdge(GEdge newEdge) {
		edges.add(newEdge);
	}

	/**
	 * Add a node
	 * 
	 * @param newNode a new node
	 */
	public void addNode(GNode newNode) {
		nodes.add(newNode);
	}

	@Override
	protected void paintComponent(Graphics g) {

		super.paintComponent(g);

		Graphics2D g2 = (Graphics2D) g; // cast g to Graphics2D

		// Draw the plot
		Image image = drawTheVisual();
		g2.drawImage(image, 0, 0, this);
	}

	/**
	 * Draw the image for this panel
	 * 
	 * @return an Image object
	 */
	private Image drawTheVisual() {
		int width = getWidth();
		int height = getHeight();
		Image image = createImage(width, height);
		Graphics2D g2 = (Graphics2D) image.getGraphics();

		if (ANTI_ALIASING_ACTIVATED) {
			java.awt.RenderingHints rh1 = new java.awt.RenderingHints(java.awt.RenderingHints.KEY_TEXT_ANTIALIASING,
					RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
			java.awt.RenderingHints rh2 = new java.awt.RenderingHints(java.awt.RenderingHints.KEY_ANTIALIASING,
					RenderingHints.VALUE_ANTIALIAS_ON);
			g2.setRenderingHints(rh1);
			g2.setRenderingHints(rh2);
		}

		g2.setColor(CANVAS_COLOR);
		g2.fillRect(0, 0, width, height);

		// Draw edges
		if (SHOW_EDGE_IDS || SHOW_EDGE_LABELS) {
			java.awt.Font newFont = g2.getFont().deriveFont((float) EDGE_TEXT_SIZE);
			g2.setFont(newFont);
		}
		g2.setColor(getEdgeColor());
		for (GEdge edge : edges) {
			drawEdge(g2, edge.getFromNode().getCenterX(), edge.getFromNode().getCenterY(),
					edge.getToNode().getCenterX(), edge.getToNode().getCenterY(), edge.isDirected(), edge);
		}

		// Draw nodes

		if (SHOW_NODE_IDS || SHOW_NODE_LABELS) {
			java.awt.Font newFont = g2.getFont().deriveFont((float) NODE_TEXT_SIZE);
			g2.setFont(newFont);
		}
		for (GNode node : nodes) {
			drawNode(g2, node);
		}

		return image;
	}

	/**
	 * Draw a node
	 * 
	 * @param g    the Graphics object
	 * @param node a node
	 */
	private void drawNode(Graphics g, GNode node) {

		if (node == currentlyMouseOverNode) {
			g.setColor(NODE_HIGHLIGHT_COLOR);
		} else {
			g.setColor(getNodeColor());
		}

		// Draw selection rectangle
//		g.drawRect(node.topLeftX, node.topLeftY, GNode.DIAMETER, GNode.DIAMETER);

		// Draw the vertex shape
		g.fillOval(node.getTopLeftX(), node.getTopLeftY(), GNode.getDIAMETER(), GNode.getDIAMETER());
		g.setColor(NODE_BORDER_COLOR);
		g.drawOval(node.getTopLeftX(), node.getTopLeftY(), GNode.getDIAMETER(), GNode.getDIAMETER());

		// Draw the vertex name
		/** Font metrics */
		if (SHOW_NODE_IDS || SHOW_NODE_LABELS) {
//			java.awt.Font newFont = g2.getFont().deriveFont((float) NODE_TEXT_SIZE);
//			g.setFont(newFont);
			
			String text = node.getIdAndNameAsString(SHOW_NODE_IDS, SHOW_NODE_LABELS);

			int stringWidth = g.getFontMetrics().stringWidth(text);
			int stringHeight = g.getFontMetrics().getHeight();

			int xlabel = node.getCenterX() - stringWidth / 2;
			int ylabel = node.getCenterY() + stringHeight / 2;
			// if(node.isHighlighted()) {
			// g.setColor(Color.YELLOW);
			// }else {
			// g.setColor(new Color(235, 235, 235));
			// }
			// g.fillRect(xlabel, ylabel - stringHeight, stringWidth, stringHeight);

			g.setColor(NODE_LABEL_COLOR);
			g.drawString(text, xlabel, ylabel);
		}

	}

	/**
	 * Draw an edge
	 * 
	 * @param g          Graphics2D object
	 * @param x1         position x where arrow starts
	 * @param y1         position y where arrow starts
	 * @param x2         position x where arrow ends
	 * @param y2         position y where arrow ends
	 * @param isDirected boolean indicating if the graph is directed
	 * @param edge       the edge
	 */
	private void drawEdge(Graphics2D g, final int x1, final int y1, final int x2, final int y2, boolean isDirected,
			GEdge edge) {

		// Get the current transform
		java.awt.geom.AffineTransform currentTransform = g.getTransform();

		// We prepare a transform to draw the arrow head
		double distanceX = x2 - x1;
		double distanceY = y2 - y1;

		double newAngle = Math.atan2(distanceY, distanceX);

		AffineTransform newTransform = AffineTransform.getTranslateInstance(x1, y1);
		newTransform.concatenate(AffineTransform.getRotateInstance(newAngle));

		// Do the transformation
		g.transform(newTransform);

		g.setColor(getEdgeColor());

		// Draw the line
		int arrowLength = (int) Math.sqrt(distanceX * distanceX + distanceY * distanceY) - (GNode.getRadius());
		g.setStroke(new BasicStroke(GEdge.getEdgeThickness()));
		g.drawLine(0 + GNode.getRadius(), 0, (int) arrowLength, 0);
		g.setStroke(new BasicStroke(1));

		// Draw the arrow from position (0, 0)
		if (isDirected) {
			g.fillPolygon(
					new int[] { arrowLength, arrowLength - GEdge.getArrowHeadSize(),
							arrowLength - GEdge.getArrowHeadSize(), arrowLength },
					new int[] { 0, -GEdge.getArrowHeadSize(), GEdge.getArrowHeadSize(), 0 }, 4);
		}

		// We finished drawing the arrow to we restore the previous transform
		g.setTransform(currentTransform);

		// Draw the edge label
		if (SHOW_EDGE_IDS || SHOW_EDGE_LABELS) {
			String text = edge.getIdAndNameAsString(SHOW_EDGE_IDS, SHOW_EDGE_LABELS);
//			g.setColor(Color.RED);
			int stringWidth = g.getFontMetrics().stringWidth(text);
			int xlabel = (x1 + x2) / 2 - stringWidth / 2;
			int ylabel = (y1 + y2) / 2 + g.getFontMetrics().getHeight() / 2;
			g.setColor(CANVAS_COLOR);
			g.fillRect(xlabel, ylabel - (g.getFontMetrics().getHeight()), stringWidth, g.getFontMetrics().getHeight());
			g.setColor(EDGE_LABEL_COLOR);
			g.drawString(text, xlabel, ylabel);
		}

	}

	@Override
	public void mouseClicked(MouseEvent e) {

	}

	@Override
	public void mousePressed(MouseEvent event) {
		mouseXPosition = event.getX();
		mouseYPosition = event.getY();

		if (event.getButton() == MouseEvent.BUTTON1) {
			mouseLeftIsPressed = true;
		}

		if (event.getButton() == MouseEvent.BUTTON3) {
			mouseRightIsPressed = true;
		}

		Point mousePosition = this.getMousePosition();
		if (mousePosition != null) {
			// find the node that is contained
			for (int i = nodes.size() - 1; i >= 0; i--) {
				GNode node = nodes.get(i);
				if (node.contains(mousePosition.x, mousePosition.y)) {
					currentlyDraggedNode = node;
					currentlyMouseOverNode = node;
//					currentlyDraggedEdge = null;

					updateMouseCursor();
					return;
				}
			}

//			// find the edge that is contained
//			for (int i = edges.size() - 1; i >= 0; i--) {
//				GEdge edge = edges.get(i);
//				if (edge.contains(mousePosition.x, mousePosition.y)) {
////					currentlyDraggedEdge = edge;
//					currentlyMouseOverEdge = edge;
//					currentlyDraggedNode = null;
//					return;
//				}
//			}
		}
		currentlyDraggedNode = null;

		updateMouseCursor();
//		currentlyDraggedEdge = null;

	}

	@Override
	public void mouseReleased(MouseEvent e) {
		currentlyDraggedNode = null;
//		currentlyDraggedEdge = null;
		mouseLeftIsPressed = false;
		mouseRightIsPressed = false;
		updateMouseCursor();
	}

	@Override
	public void mouseEntered(MouseEvent e) {
		// TODO Auto-generated method stub

	}

	@Override
	public void mouseExited(MouseEvent e) {
		// TODO Auto-generated method stub

	}

//    public void mouseDragged(MouseEvent e) {
//
//    }
	@Override
	public void mouseDragged(MouseEvent e) {

		// The user is dragging us, so scroll!
		Rectangle r = new Rectangle(e.getX(), e.getY(), 1, 1);
		scrollRectToVisible(r);

		Point mousePosition = this.getMousePosition();
		if (mousePosition != null && mouseLeftIsPressed && currentlyDraggedNode != null) {
			int newX = mousePosition.x;
			if (newX < GNode.getRadius()) {
				newX = GNode.getRadius();
			} else if (newX > maxX) {
				newX = maxX;
			}

			int newY = mousePosition.y;
			if (newY < GNode.getRadius()) {
				newY = GNode.getRadius();
			} else if (newY > maxY) {
				newY = maxY;
			}
			currentlyDraggedNode.updatePosition(newX, newY);
		}
//		if (mousePosition != null && currentlyDraggedEdge != null) {
//			int newX = mousePosition.x;
//			if (newX < GNode.RADIUS) {
//				newX = GNode.RADIUS;
//			} else if (newX > maxX) {
//				newX = maxX;
//			}
//
//			int newY = mousePosition.y;
//			if (newY < GNode.RADIUS) {
//				newY = GNode.RADIUS;
//			} else if (newY > maxY) {
//				newY = maxY;
//			}
//			currentlyDraggedEdge.updatePosition(newX, newY);
//		}

		updateMouseCursor();
		repaint();

		mouseXPosition = e.getX();
		mouseYPosition = e.getY();
	}

	@Override
	public void mouseMoved(MouseEvent e) {
		Point mousePosition = this.getMousePosition();
		if (mousePosition == null) {
			return;
		}

		findNodeThatCursorIsOver(mousePosition);

//		if (currentlyMouseOverNode == null) {
//			findEdgeThatCursorIsOver(mousePosition);
//		}

		updateMouseCursor();

		GraphViewerPanel.this.repaint();
	}

	private void findNodeThatCursorIsOver(Point mousePosition) {
		// Find the node that the cursor is over it
		for (int i = nodes.size() - 1; i >= 0; i--) {
			GNode node = nodes.get(i);
			if (node.contains(mousePosition.x, mousePosition.y)) {
				currentlyMouseOverNode = node;
				return;
			}
		}
		currentlyMouseOverNode = null;
	}

//	private void findEdgeThatCursorIsOver(Point mousePosition) {
//		// Find the edge that the cursor is over it
//		for (int i = edges.size() - 1; i >= 0; i--) {
//			GEdge edge = edges.get(i);
//			if (edge.contains(mousePosition.x, mousePosition.y)) {
//				currentlyMouseOverEdge = edge;
//				return;
//			}
//		}
//		currentlyMouseOverEdge = null;
//	}

	/**
	 * Perform automatic layout of graph nodes.
	 */
	public void autoLayout() {
		if (nodes.size() == 0) {
			return;
		}
		graphLayoutGenerator.autoLayout(edges, nodes, getWidth(), getHeight());
	}

	/**
	 * Get edge count
	 * 
	 * @return the count
	 */
	public int getEdgeCount() {
		return edges.size();
	}

	/**
	 * Get node count
	 * 
	 * @return the count
	 */
	public int getNodeCount() {
		return nodes.size();
	}

	@Override
	public void update(Graphics g) {
		super.update(g);

		paintComponent(g);
	}

	/**
	 * Remove all edges and nodes.
	 */
	public void clear() {
		edges.clear();
		nodes.clear();
	}

//	@Override
	public Dimension getPreferredSize() {
		if (width == 0) {
			return super.getPreferredSize();
		} else {
			return new Dimension(width, height);
		}
	}

	/**
	 * Update the size of this panel
	 * 
	 * @param newWidth     the new width
	 * @param newHeight    the new height
	 * @param doAutoLayout do auto layout
	 */
	public void updateSize(int newWidth, int newHeight, boolean doAutoLayout) {
		width = newWidth;
		height = newHeight;
		resized(doAutoLayout);
	}

	/**
	 * Update the node size
	 * 
	 * @param newRadius the new radius
	 */
	public void updateNodeSize(int newRadius) {
		GNode.changeRadiusSize(newRadius);
		maxX = getWidth() - GNode.getRadius();
		maxY = getHeight() - GNode.getRadius();

		for (GNode node : nodes) {
			node.updatePosition(node.getCenterX(), node.getCenterY());
		}
//		revalidate();
		repaint();
	}

	/**
	 * Update the node text size
	 * 
	 * @param newTextSize the new size
	 */
	public void updateNodeTextSize(int newTextSize) {
		NODE_TEXT_SIZE = newTextSize;

		for (GNode node : nodes) {
			node.updatePosition(node.getCenterX(), node.getCenterY());
		}

//		revalidate();
		repaint();
	}
	
	/**
	 * Update the edge text size
	 * 
	 * @param newTextSize the new size
	 */
	public void updateEdgeTextSize(int newTextSize) {
		EDGE_TEXT_SIZE = newTextSize;

//		revalidate();
		repaint();
	}

	/**
	 * Update edge thickness
	 * 
	 * @param newThickness the new thickness
	 */
	public void updateEdgeThickness(int newThickness) {
		GEdge.changeThickness(newThickness);

//		revalidate();
		repaint();
	}

	/**
	 * This method is called when the user click on the button to export the current
	 * plot to a file
	 * 
	 * @throws IOException if an error occurs
	 */
	protected void exportAsPNG() {

		// ask the user to choose the filename and path
		String outputFilePath = null;
		try {
			File path;
			// Get the last path used by the user, if there is one
			String previousPath = PreferencesManager.getInstance().getOutputFilePath();
			// If there is no previous path (first time user),
			// show the files in the "examples" package of
			// the spmf distribution.
			if (previousPath == null) {
				URL main = MainTestApriori_saveToFile.class.getResource("MainTestApriori_saveToFile.class");
				if (!"file".equalsIgnoreCase(main.getProtocol())) {
					path = null;
				} else {
					path = new File(main.getPath());
				}
			} else {
				// Otherwise, use the last path used by the user.
				path = new File(previousPath);
			}

			// ASK THE USER TO CHOOSE A FILE
			final JFileChooser fc;
			if (path != null) {
				fc = new JFileChooser(path.getAbsolutePath());
			} else {
				fc = new JFileChooser();
			}
			int returnVal = fc.showSaveDialog(GraphViewerPanel.this);

			// If the user chose a file
			if (returnVal == JFileChooser.APPROVE_OPTION) {
				File file = fc.getSelectedFile();
				outputFilePath = file.getPath(); // save the file path
				// save the path of this folder for next time.
				if (fc.getSelectedFile() != null) {
					PreferencesManager.getInstance().setOutputFilePath(fc.getSelectedFile().getParent());
				}
			} else {
				// the user did not choose so we return
				return;
			}

		} catch (Exception e) {
			JOptionPane.showMessageDialog(null,
					"An error occured while opening the save plot dialog. ERROR MESSAGE = " + e.toString(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}

		try {

			// add the .png extension
			if (outputFilePath.endsWith("png") == false) {
				outputFilePath = outputFilePath + ".png";
			}
			File outputFile = new File(outputFilePath);
			BufferedImage image = (BufferedImage) drawTheVisual();
			ImageIO.write(image, "png", outputFile);

		} catch (Exception e) {
			JOptionPane.showMessageDialog(null,
					"An error occured while attempting to save the plot. ERROR MESSAGE = " + e.toString(), "Error",
					JOptionPane.ERROR_MESSAGE);
		}
	}

	protected void updateMouseCursor() {
		// || currentlyMouseOverEdge != null)
		if (currentlyMouseOverNode != null) {
			if (mouseLeftIsPressed) {
				setCursor(Cursor.getPredefinedCursor(Cursor.MOVE_CURSOR));
			} else {
				setCursor(Cursor.getPredefinedCursor(Cursor.MOVE_CURSOR));
			}
		} else {
			setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
		}
	}

	public Color getNodeColor() {
		return NODE_COLOR;
	}

	public void setNodeColor(Color color) {
		NODE_COLOR = color;
		repaint();
	}

	public void setNodeTextColor(Color color) {
		NODE_LABEL_COLOR = color;
		repaint();
	}

	public Color getNodeTextColor() {
		return NODE_LABEL_COLOR;
	}

	public Color getEdgeTextColor() {
		return EDGE_LABEL_COLOR;
	}

	public void setEdgeTextColor(Color color) {
		EDGE_LABEL_COLOR = color;
		repaint();
	}

	public Color getEdgeColor() {
		return EDGE_COLOR;
	}

	public void setEdgeColor(Color color) {
		EDGE_COLOR = color;
		repaint();
	}

	public Color getCanvasColor() {
		return CANVAS_COLOR;
	}

	public void setCanvasColor(Color cANVAS_COLOR) {
		CANVAS_COLOR = cANVAS_COLOR;
		repaint();
	}

	public Color getNodeBorderColor() {
		return NODE_BORDER_COLOR;
	}

	public void setNodeBorderColor(Color color) {
		NODE_BORDER_COLOR = color;
	}

	public void setAntiAliasing(boolean selected) {
		ANTI_ALIASING_ACTIVATED = selected;
		repaint();
	}

	public static int getNodeTextSize() {
		return NODE_TEXT_SIZE;
	}
	
	public static int getEdgeTextSize() {
		return EDGE_TEXT_SIZE;
	}

	public void showEdgeIDs(boolean selected) {
		SHOW_EDGE_IDS = selected;
	}

	public void showNodeIDs(boolean selected) {
		SHOW_NODE_IDS = selected;
	}

	public void showEdgeLabels(boolean selected) {
		SHOW_EDGE_LABELS = selected;
	}

	public void showNodeLabels(boolean selected) {
		SHOW_NODE_LABELS = selected;
	}

}