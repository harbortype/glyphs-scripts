#MenuTitle: Duplicate Selected Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a copy of the selected nodes and adds them in place
"""

font = Glyphs.font
layer = font.selectedLayers[0]
newPathsArray = []

def ProcessPath( path ):
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
    return newPath
    
layer.beginChanges()

try:
    # Glyphs 3
    for i in range(len(layer.shapes)-1,-1,-1):
        shape = layer.shapes[i]
        if isinstance(shape, GSPath):
            newPath = ProcessPath(shape)
            newPathsArray.append(newPath)
        else:
            newPathsArray.append(shape)
    layer.shapes = newPathsArray
except:
    # Glyphs 2
    for pathIndex, path in enumerate( layer.paths ):
        newPath = ProcessPath(path)
        newPathsArray.append(newPath)
    layer.paths = newPathsArray
finally:
    layer.endChanges()
