# MenuTitle: Create Centerline
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a centerline between two selected paths. The paths should have opposite directions. If it doesn’t work as expected, try reversing one of the paths.
"""

from GlyphsApp import Glyphs, GSPath, GSNode, Message, pointOnLine


def interpolatePaths():
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

    newPath = GSPath()
    thisPath = selectedPaths[0]
    selectedPaths[1].reverse()
    for thisNodeIndex in range(len(thisPath.nodes)):
        thisNode = thisPath.nodes[thisNodeIndex]
        foregroundPosition = thisNode.position
        backgroundPosition = selectedPaths[1].nodes[thisNodeIndex].position
        newNode = GSNode()
        newNode.type = thisNode.type
        newNode.connection = thisNode.connection
        newNode.setPosition_(pointOnLine(
            foregroundPosition, backgroundPosition, factor))
        newPath.addNode_(newNode)
    if thisPath.closed:
        newPath.setClosePath_(1)
    layer.paths.append(newPath)
    layer.roundCoordinates()


interpolatePaths()
