#MenuTitle: Duplicate Selected Nodes
# -*- coding: utf-8 -*-
__doc__="""
Creates a copy of the selected nodes and adds them in place
"""

font = Glyphs.font
layer = font.selectedLayers[0]

print layer.selection

for path in layer.paths:

    for node in path.nodes:

        if node.type != "offcurve" and node.selected:

            newNode = GSNode()
            newNode.type = "line"
            newNode.smooth = False
            newNode.position = node.position
            node.smooth = False
            path.insertNode_atIndex_( newNode, node.index+1 )
