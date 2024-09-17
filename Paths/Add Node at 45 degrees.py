# MenuTitle: Add Nodes at 45° on Selected Segments
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

__doc__ = """
Adds nodes at 45° on selected segments. Interpolation may produce kinks if a node changes the angle AND proportion of its handles between masters. This is not a problem for extremes, but sometimes we need to add intermediate nodes to better control a curve. The easiest way to ensure no kinks will happen in difficult curves is to keep the handles at a constant angle, like 45°.
"""

from Foundation import NSAffineTransform, NSMakePoint
from GlyphsApp import Glyphs, GSPath, GSNode, OFFCURVE

Glyphs.clearLog()
font = Glyphs.font


def RotatePath(path, angle):
	"""Rotates a path by an angle in degrees"""
	transform = NSAffineTransform.transform()
	transform.rotateByDegrees_(angle)
	for node in path.nodes:
		node.position = transform.transformPoint_(
			NSMakePoint(node.x, node.y)
		)


thisLayer = font.selectedLayers[0]
for p, thisPath in enumerate(thisLayer.paths):
	for n, thisNode in enumerate(thisPath.nodes):
		if not thisNode.selected:
			continue
		nextNode = thisNode.nextNode
		if nextNode.type != OFFCURVE:
			continue

		# copy nodes
		tempPath = GSPath()
		for node in thisPath.nodes[n:n + 4]:
			newNode = GSNode()
			newNode.type = node.type
			newNode.smooth = node.smooth
			newNode.position = node.position
			tempPath.addNode_(newNode)
		tempPath.setClosePath_(0)

		RotatePath(tempPath, 45)
		tempPath.addNodesAtExtremes()
		RotatePath(tempPath, -45)

		newListOfNodes = []
		newListOfNodes.extend(thisPath.nodes[:n])
		newListOfNodes.extend(tempPath.nodes)
		newListOfNodes.extend(thisPath.nodes[n + 4:])

		thisPath.nodes = newListOfNodes
