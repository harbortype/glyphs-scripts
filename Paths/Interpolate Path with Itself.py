#MenuTitle: Interpolate Path with Itself
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Interpolates the path with itself. The fixed half will be the one with the start point.
"""

Glyphs.clearLog()

# TODO Glyphs 3 compatibility
thisFont = Glyphs.font
allSelected = [ x.parent for x in thisFont.selectedLayers[0].selection ]
selectedPaths = []
for selectedItem in allSelected:
    if selectedItem not in selectedPaths and type( selectedItem ) == GSPath:
        selectedPaths.append( selectedItem )

def interpolateNode( firstNode, secondNode, factor ):
    interpolatedX = ( secondNode.x - firstNode.x ) * factor + firstNode.x
    interpolatedY = ( secondNode.y - firstNode.y ) * factor + firstNode.y
    interpolatedPosition = [ round(interpolatedX), round(interpolatedY) ]
    return interpolatedPosition

for path in selectedPaths:
    if not path.closed:
        print("Path is not closed")
    else:
        # checks if path has an even number of nodes
        nodeCount = len( path.nodes )
        if nodeCount % 2 == 0:
            nodes = path.nodes
            # creates node pairs that will be interpolated
            nodePairsIndex = []
            for i in range( nodeCount//2 ):
                nodePairsIndex.append([ i-1, nodeCount-2-i ])
            # performs the interpolation
            for pair in nodePairsIndex:
                newPosition = interpolateNode( nodes[pair[0]], nodes[pair[1]], 0.5 )
                nodes[pair[1]].x = newPosition[0]
                nodes[pair[1]].y = newPosition[1]
