# MenuTitle: Duplicate Selected Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a copy of the selected nodes and adds them in place
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
        newNode = GSNode()
        newNode.type = "line"
        newNode.smooth = False
        newNode.position = node.position
        path.nodes.insert(i + 1, newNode)


layer.beginChanges()
try:
    for path in layer.paths:
        ProcessPath(path)
finally:
    layer.endChanges()
