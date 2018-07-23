#MenuTitle: Open All Nodes
# -*- coding: utf-8 -*-
__doc__="""
Opens all nodes.
"""

import GlyphsApp

Glyphs.clearLog()

font = Glyphs.font
layer = font.selectedLayers[0]

layer.beginChanges()

# # access all selected nodes
# for path in layer.paths:
# 	for thisNodeIndex in range(len(path.nodes)):
# 		thisNode = path.nodes[thisNodeIndex]
# 		if thisNode.selected:
# 			newPath = GSPath()
# 			newNodeIndex = thisNodeIndex
# 			while newNodeIndex < len(path.nodes):
# 				newNode = GSNode()
# 				if newNodeIndex == thisNodeIndex:
# 					newNode.type = 'line'
# 				else:					
# 					newNode.type = path.nodes[newNodeIndex].type
# 				newNode.connection = path.nodes[newNodeIndex].connection
# 				newNode.setPosition_( path.nodes[newNodeIndex].position )
# 				newPath.addNode_( newNode )
# 				newNodeIndex += 1
# 			layer.paths.append( newPath )

pathArray = []
for path in layer.paths:
	for segment in path.segments:
		newPath = GSPath()
		nodeIndex = 0

		if len(segment) == 4:
			for point in segment:
				newNode = GSNode()
				newNode.position = point.x, point.y
				
				if nodeIndex == 0:
					newNode.type = 'line'
				elif nodeIndex == 3:
					newNode.type = 'curve'
				else:
					newNode.type = 'offcurve'

				newPath.addNode_( newNode )
				nodeIndex += 1
		else:
			for point in segment:
				newNode = GSNode()
				newNode.position = point.x, point.y
				newNode.type = 'line'
				newPath.addNode_( newNode )
		
		pathArray.append( newPath )

layer.paths = []

for path in pathArray:
	layer.paths.append( path )

layer.endChanges()
