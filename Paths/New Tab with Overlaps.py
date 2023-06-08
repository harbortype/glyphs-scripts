# MenuTitle: New Tab with Overlaps
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens a new Edit tab containing all glyphs that contain overlaps.
"""

from GlyphsApp import Glyphs
from AppKit import NSClassFromString

thisFont = Glyphs.font  # frontmost font
master_ids = [master.id for master in thisFont.masters]  # all the master ids


def check_for_overlaps(lyr):
    paths = list(lyr.paths)
    GSPathOperator = NSClassFromString("GSPathOperator")
    segments = GSPathOperator.segmentsFromPaths_(paths)
    count1 = len(segments)
    if Glyphs.versionNumber >= 3.0:
        GSPathOperator.addIntersections_(segments)
    else:
        PathOperator = GSPathOperator.new()
        PathOperator.addIntersections_(segments)
    count2 = len(segments)
    if count1 != count2:
        return True
    return False


try:
    thisFont.disableUpdateInterface()  # suppresses UI updates in Font View
    text = ""
    for thisGlyph in thisFont.glyphs:
        thisLayer = thisGlyph.layers[0]
        if not thisLayer.paths:
            continue
        if thisLayer.layerId in master_ids or thisLayer.isSpecialLayer:
            has_overlaps = check_for_overlaps(thisLayer)
            if has_overlaps:
                text += "/%s " % (thisGlyph.name)
    thisFont.newTab(text)
finally:
    thisFont.enableUpdateInterface()  # re-enables UI updates in Font View
