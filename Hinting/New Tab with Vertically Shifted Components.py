#MenuTitle: New Tab with Vertically Shifted Components
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens a new edit tab with components that are transformed beyond mere horizontal shifts.
"""



thisFont = Glyphs.font # frontmost font
thisFontMaster = thisFont.selectedFontMaster # active master
listOfSelectedLayers = thisFont.selectedLayers # active layers of selected glyphs

def containsTransformedComponents( thisGlyph ):
    for thisLayer in thisGlyph.layers:
        if thisLayer.isMasterLayer or thisLayer.isSpecialLayer:
            for thisComponent in thisLayer.components:
                if thisComponent.transform[-1] != 0.0:
                    print("%s: component %s is shifted by %s on layer %s." % (thisGlyph.name, thisComponent.name, thisComponent.transform[-1], thisLayer.name))
                    return True
    return False 

glyphList = []

for thisGlyph in thisFont.glyphs:
    if containsTransformedComponents( thisGlyph ):
        glyphList.append(thisGlyph.name)

if glyphList:
    tabString = "/"+"/".join(glyphList)
    thisFont.newTab(tabString)
else:
    Message(
        title="No Transformed Components",
        message="No vertically shifted components found in this font.",
        OKButton="Yeah"
        )