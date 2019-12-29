#MenuTitle: Duplicate Selected Nodes with Offcurve Points
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a copy of the selected nodes, adds them in place and create zero-length offcurve points in between.
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
                
                offcurveNode1 = GSNode()
                offcurveNode1.type = "offcurve"
                offcurveNode1.position = node.position
                newPath.addNode_( offcurveNode1 )

                offcurveNode2 = GSNode()
                offcurveNode2.type = "offcurve"
                offcurveNode2.position = node.position
                newPath.addNode_( offcurveNode2 )

                newNode = GSNode()
                newNode.type = "curve"
                newNode.smooth = False
                newNode.position = node.position
                newPath.addNode_( newNode )
        
        newPath.closed = True if path.closed else False
        newPathsArray.append( newPath )

    layer.paths = newPathsArray

finally:
    layer.endChanges()
