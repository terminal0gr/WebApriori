package ca.pfv.spmf.gui.texteditor;

import java.awt.Dimension;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Insets;
import java.awt.Point;
import java.awt.Rectangle;
import java.awt.geom.Rectangle2D;

import javax.swing.JPanel;
import javax.swing.JTextArea;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.text.Element;
import javax.swing.text.Utilities;

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
 * Object to add line numbers to a text area
 *
 */
public class LineNumberPane extends JPanel {

	/**
	 * serial UID
	 */
	private static final long serialVersionUID = 1076288361088590368L;

	/** Text area */
	private JTextArea textArea;

	/**
	 * Constructor
	 * 
	 * @param ta a text area
	 */
	public LineNumberPane(JTextArea ta) {
		this.textArea = ta;
		ta.getDocument().addDocumentListener(new DocumentListener() {

			@Override
			public void insertUpdate(DocumentEvent e) {
				revalidate();
				repaint();
			}

			@Override
			public void removeUpdate(DocumentEvent e) {
				revalidate();
				repaint();
			}

			@Override
			public void changedUpdate(DocumentEvent e) {
				revalidate();
				repaint();
			}
		});
	}

	@Override
	public Dimension getPreferredSize() {
		FontMetrics fm = getFontMetrics(textArea.getFont());
		int lineCount = textArea.getLineCount();
		Insets insets = getInsets();
		int min = fm.stringWidth("000");
		int width = Math.max(min, fm.stringWidth(Integer.toString(lineCount))) + insets.left + insets.right;
		int height = fm.getHeight() * lineCount;
		return new Dimension(width, height);
	}

	@Override
	protected void paintComponent(Graphics g) {
	    super.paintComponent(g);
	    g.setFont(textArea.getFont());

	    FontMetrics fm = textArea.getFontMetrics(textArea.getFont());
	    Insets insets = getInsets();

	    Rectangle clip = g.getClipBounds();
	    int rowStartOffset = textArea.viewToModel2D(new Point(0, clip.y));
	    int endOffset = textArea.viewToModel2D(new Point(0, clip.y + clip.height));

	    Element root = textArea.getDocument().getDefaultRootElement();
	    while (rowStartOffset <= endOffset) {
	        try {
	            int index = root.getElementIndex(rowStartOffset);
	            Element line = root.getElement(index);

	            String lineNumber = "";
	            if (line.getStartOffset() == rowStartOffset) {
	                lineNumber = String.valueOf(index + 1);
	            }

	            int x = insets.left;
	            // Use modelToView2D instead of modelToView
	            Rectangle2D r = textArea.modelToView2D(rowStartOffset);
	            int y = (int) (r.getY() + r.getHeight());
	            g.drawString(lineNumber, x, y - fm.getDescent());

	            // Move to the next row
	            rowStartOffset = Utilities.getRowEnd(textArea, rowStartOffset) + 1;
	        } catch (Exception e) {
	            break;
	        }
	    }
	}


}