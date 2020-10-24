#MenuTitle: Open All Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens all nodes for the selected paths (or all paths if none are selected).
"""

font = Glyphs.font
layers = font.selectedLayers

def open_nodes(path):	
	
	for segment in path.segments:
		
		try: # Glyphs 3
			countOfPoints = segment.countOfPoints()
		except: # Glyphs 2
			countOfPoints = len(segment)
		
		newPath = GSPath()
		if countOfPoints == 4:
			for n in range(countOfPoints):
				point = segment[n]
				newNode = GSNode()
				newNode.position = point.x, point.y
				if n == 0:
					newNode.type = 'line'
				elif n == 3:
					newNode.type = 'curve'
				else:
					newNode.type = 'offcurve'
				newPath.addNode_(newNode)
		else:
			for n in range(countOfPoints):
				point = segment[n]
				newNode = GSNode()
				newNode.position = point.x, point.y
				newNode.type = 'line'
				newPath.addNode_(newNode)

		newPaths.append(newPath)

for layer in layers:
	
	try:
		layer.beginChanges()
		
		selection = [ x.parent for x in layer.selection ]
		selectedPaths = []
		for item in selection:
			if item not in selectedPaths and type(item) == GSPath:
				selectedPaths.append(item)
		if len(selectedPaths) == 0:
			selectedPaths = layer.paths
		
		newPaths = []
		try: # Glyphs 3
			for i in range(len(layer.shapes)-1,-1,-1):
				shape = layer.shapes[i]
				if type(shape) == GSPath and shape in selectedPaths:
					open_nodes(shape)
					del layer.shapes[i]
			layer.shapes.extend(newPaths)
		except: # Glyphs 2
			for i in range(len(layer.paths)-1,-1,-1):
				path = layer.paths[i]
				if path in selectedPaths:
					open_nodes(path)
					del layer.paths[i]
			layer.paths.extend(newPaths)
	
	finally:
		layer.endChanges()
