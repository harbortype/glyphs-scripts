# MenuTitle: Duplicate Selected Nodes with Offcurve Points
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a copy of the selected nodes, adds them in place and create zero-length offcurve points in between.
"""

from GlyphsApp import Glyphs, GSNode

font = Glyphs.font
layer = font.selectedLayers[0]


def ProcessPath(path):
    selectedIndexes = [i for i, node in enumerate(path.nodes) if node.type != "offcurve" and node.selected]
    # Insert from the end, so the indexes of earlier nodes do not change
    for i in reversed(selectedIndexes):
        node = path.nodes[i]
        node.smooth = False
        offcurveNode1 = GSNode()
        offcurveNode1.type = "offcurve"
        offcurveNode1.position = node.position
        offcurveNode2 = GSNode()
        offcurveNode2.type = "offcurve"
        offcurveNode2.position = node.position
        newNode = GSNode()
        newNode.type = "curve"
        newNode.smooth = False
        newNode.position = node.position
        path.nodes.insert(i + 1, offcurveNode1)
        path.nodes.insert(i + 2, offcurveNode2)
        path.nodes.insert(i + 3, newNode)


layer.beginChanges()
try:
    for path in layer.paths:
        ProcessPath(path)
finally:
    layer.endChanges()
