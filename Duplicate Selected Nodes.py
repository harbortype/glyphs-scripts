#MenuTitle: Duplicate Selected Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a copy of the selected nodes and adds them in place
"""

font = Glyphs.font
layer = font.selectedLayers[0]
newPathsArray = []

layer.beginChanges()

try:
    for pathIndex, path in enumerate( layer.paths ):
        newPath = GSPath()
        
        for node in path.nodes:
            newPath.addNode_( node.copy() )
            
            if node.type != "offcurve" and node.selected:
                newPath.nodes[len(newPath.nodes)-1].smooth = False

                newNode = GSNode()
                newNode.type = "line"
                newNode.smooth = False
                newNode.position = node.position
                newPath.addNode_( newNode )
        
        newPath.closed = True if path.closed else False
        newPathsArray.append( newPath )

    layer.paths = newPathsArray

finally:
    layer.endChanges()
