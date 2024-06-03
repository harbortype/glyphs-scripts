# MenuTitle: Create Centerline
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a centerline between two selected paths. The paths should have opposite directions. If it doesn’t work as expected, try reversing one of the paths.
"""

from GlyphsApp import Glyphs, GSPath, GSNode, Message
from AppKit import NSPoint

def pointOnLine(P0, P1, t):
    return NSMakePoint(P0.x + ((P1.x - P0.x) * t), P0.y + ((P1.y - P0.y) * t))

def makeCenterline():
    font = Glyphs.font
    layer = font.selectedLayers[0]
    factor = 0.5

    if not layer.selectedObjects():
        Message(
            title="Create Centerline",
            message="Please select 2 paths."
        )
        return
    if Glyphs.versionNumber >= 3.0:
        selectedPaths = [shape for shape in layer.selectedObjects(
        )["shapes"] if isinstance(shape, GSPath)]
    else:
        selectedPaths = layer.selectedObjects()["paths"]

    # interpolate paths only if 2 paths are selected:
    if (len(selectedPaths) != 2):
        Message(
            title="Create Centerline",
            message="Please select 2 paths."
        )
        return

    # check if paths are compatible
    if (len(selectedPaths[0].nodes) != len(selectedPaths[1].nodes)):
        thisGlyph = layer.parent
        Message(
            title="Create Centerline",
            message="%s: selected paths are not compatible ('%s')." % (
                thisGlyph.name, layer.name
            )
        )
        return

    firstPath = selectedPaths[0]
    otherPath = selectedPaths[1].copy()

    newPath = interpolatePaths(firstPath, otherPath, factor)
    layer.paths.append(newPath)


def interpolatePaths(firstPath, otherPath, factor):
    otherPath.reverse()
    newPath = GSPath()
    for nodeIndex in range(len(firstPath.nodes)):
        thisNode = firstPath.nodes[nodeIndex]
        otherNode = otherPath.nodes[nodeIndex]
        thisPosition = thisNode.position
        otherPosition = otherNode.position
        interpolatesPosition = pointOnLine(
            thisPosition, otherPosition, factor
        )
        newNode = GSNode(interpolatesPosition, thisNode.type)
        newNode.connection = thisNode.connection
        newNode.roundToGrid_(1)
        newPath.nodes.append(newNode)
    if firstPath.closed:
        newPath.setClosePath_(1)
    return newPath


makeCenterline()
