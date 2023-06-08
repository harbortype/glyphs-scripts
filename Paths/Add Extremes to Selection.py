# MenuTitle: Add Extremes to Selection
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Adds extreme points to selected paths.
"""

from GlyphsApp import Glyphs, GSPath

thisFont = Glyphs.font
thisLayer = thisFont.selectedLayers[0]

try:
    for i in range(len(thisLayer.shapes) - 1, -1, -1):
        shape = thisLayer.shapes[i]
        if isinstance(shape, GSPath):
            pathSelected = False
            for node in shape.nodes:
                if node in thisLayer.selection:
                    pathSelected = True
                    break
            if pathSelected:
                shape.addNodesAtExtremes()
                shape.selected = True
except:
    for path in thisLayer.paths:
        if path.selected:
            path.addNodesAtExtremes()
            path.selected = True
