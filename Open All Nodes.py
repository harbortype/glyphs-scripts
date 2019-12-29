#MenuTitle: Open All Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens all nodes for the selected paths (or all paths if none are selected).
"""

font = Glyphs.font
layers = font.selectedLayers

for layer in layers:
	
	layer.beginChanges()
	allSelected = [ x.parent for x in layer.selection ]
	
	selectedPaths = []
	for item in allSelected:
		if item not in selectedPaths and type(item) == GSPath:
			selectedPaths.append( item )

	if len( selectedPaths ) == 0:
		selectedPaths = layer.paths

	newPaths = []
	for path in layer.paths:
		for segment in path.segments:
			newPath = GSPath()

			if len(segment) == 4:
				for nodeIndex, point in enumerate( segment ):
					newNode = GSNode()
					newNode.position = point.x, point.y
					if nodeIndex == 0:
						newNode.type = 'line'
					elif nodeIndex == 3:
						newNode.type = 'curve'
					else:
						newNode.type = 'offcurve'
					newPath.addNode_( newNode )
			else:
				for point in segment:
					newNode = GSNode()
					newNode.position = point.x, point.y
					newNode.type = 'line'
					newPath.addNode_( newNode )

			newPaths.append( newPath )

	layer.paths = newPaths
	layer.endChanges()
