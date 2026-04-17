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
	for n in range(len(thisPath.nodes)-1,-1,-1):
		thisNode = thisPath.nodes[n]
		thisSegment = [
			thisNode,
			thisNode.nextNode,
			thisNode.nextNode.nextNode,
			thisNode.nextNode.nextNode.nextNode
			]

		if not all([node.selected for node in thisSegment]):
			continue
		if thisSegment[1].type != OFFCURVE and thisSegment[2].type != OFFCURVE:
			continue

		# copy nodes
		tempPath = GSPath()
		for node in thisSegment:
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
		newListOfNodes.extend(thisPath.nodes[n + 4:])
		if len(thisPath.nodes) != len(tempPath.nodes):
			newListOfNodes = []
			if n == len(thisPath.nodes)-1:
				# first node is in segment
				newListOfNodes.extend(tempPath.nodes)
				newListOfNodes.extend(thisPath.nodes[3:-1])
			else:
				newListOfNodes.extend(thisPath.nodes[:n])
				newListOfNodes.extend(tempPath.nodes)
				newListOfNodes.extend(thisPath.nodes[n+4:])
			thisPath.nodes = newListOfNodes

if font.gridLength:
	thisLayer.roundCoordinates()
