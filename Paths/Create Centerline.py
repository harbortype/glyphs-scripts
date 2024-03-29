# MenuTitle: Create Centerline
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a centerline between two selected paths. The paths should have opposite directions. If it doesn’t work as expected, try reversing one of the paths.
"""

import vanilla
from GlyphsApp import Glyphs, GSPath, GSNode, Message
from AppKit import NSPoint


class CreateCenterline(object):

    key = "com.harbortype.CreateCenterline"

    def __init__(self):
        self.w = vanilla.FloatingWindow(
            (180, 66), "", autosaveName=self.key + ".mainwindow")
        self.w.runButton = vanilla.Button(
            (25, 20, 130, 20),
            "Create centerline!",
            sizeStyle='regular',
            callback=self.interpolatePaths
        )
        self.w.setDefaultButton(self.w.runButton)
        # self.w.runButton.bind('`', [])
        self.w.open()

        # self.w.makeKey()

    def interpolatedPosition(self, foregroundPos, backgroundPos, factor):
        interpolatedX = foregroundPos.x * factor + backgroundPos.x * factor
        interpolatedY = foregroundPos.y * factor + backgroundPos.y * factor
        interpolatedPosition = NSPoint(interpolatedX, interpolatedY)
        return interpolatedPosition

    def interpolatePaths(self, sender):
        font = Glyphs.font
        layer = font.selectedLayers[0]
        factor = 0.5

        if not layer.selectedObjects():
            Message(
                title="Create Centerline",
                message="Please select 2 paths.",
                OKButton="OK",
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
                message="Please select 2 paths.",
                OKButton="OK",
            )
            return

        # check if paths are compatible
        if (len(selectedPaths[0]) != len(selectedPaths[1])):
            thisGlyph = layer.parent
            Message(
                title="Create Centerline",
                message="%s: selected paths are not compatible ('%s')." % (
                    thisGlyph.name, layer.name),
                OKButton="OK",
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
            newNode.setPosition_(self.interpolatedPosition(
                foregroundPosition, backgroundPosition, factor))
            newPath.addNode_(newNode)
        if thisPath.closed:
            newPath.setClosePath_(1)
        layer.paths.append(newPath)
        layer.roundCoordinates()


CreateCenterline()
