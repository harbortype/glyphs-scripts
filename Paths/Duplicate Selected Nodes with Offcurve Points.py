# MenuTitle: Duplicate Selected Nodes with Offcurve Points
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a copy of the selected nodes, adds them in place and create zero-length offcurve points in between.
"""

from GlyphsApp import Glyphs, GSPath, GSNode

font = Glyphs.font
layer = font.selectedLayers[0]
newPathsArray = []


def ProcessPath(path):
    newPath = GSPath()
    for node in path.nodes:
        newPath.addNode_(node.copy())
        if node.type != "offcurve" and node.selected:
            newPath.nodes[len(newPath.nodes) - 1].smooth = False
            offcurveNode1 = GSNode()
            offcurveNode1.type = "offcurve"
            offcurveNode1.position = node.position
            newPath.addNode_(offcurveNode1)
            offcurveNode2 = GSNode()
            offcurveNode2.type = "offcurve"
            offcurveNode2.position = node.position
            newPath.addNode_(offcurveNode2)
            newNode = GSNode()
            newNode.type = "curve"
            newNode.smooth = False
            newNode.position = node.position
            newPath.addNode_(newNode)
    newPath.closed = True if path.closed else False
    return newPath


layer.beginChanges()

try:
    # Glyphs 3
    for i in range(len(layer.shapes) - 1, -1, -1):
        shape = layer.shapes[i]
        if isinstance(shape, GSPath):
            newPath = ProcessPath(shape)
            newPathsArray.append(newPath)
        else:
            newPathsArray.append(shape)
    layer.shapes = newPathsArray
except:
    # Glyphs 2
    for pathIndex, path in enumerate(layer.paths):
        newPath = ProcessPath(path)
        newPathsArray.append(newPath)
    layer.paths = newPathsArray
finally:
    layer.endChanges()
