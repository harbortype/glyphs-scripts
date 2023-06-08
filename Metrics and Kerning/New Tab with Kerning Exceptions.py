# MenuTitle: New Tab with Kerning Exceptions
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens a new Edit tab containing all kerning exceptions for the current master.
"""

from GlyphsApp import Glyphs

tabText = ""
font = Glyphs.font
currentMasterID = font.selectedFontMaster.id
masterKerning = font.kerning[currentMasterID]


def GetGlyphName(kerning_key):
    if kerning_key[0] == "@":
        return kerning_key[7:]
    else:
        return font.glyphForId_(kerning_key).name


for leftSide in masterKerning.keys():
    left_glyph = GetGlyphName(leftSide)

    if leftSide[0] != "@" and font.glyphs[left_glyph].rightKerningGroup:
        for rightSide in masterKerning[leftSide].keys():
            right_glyph = GetGlyphName(rightSide)
            tabText += "nn/%s/%s nn\n" % (left_glyph, right_glyph)
    else:
        for rightSide in masterKerning[leftSide].keys():
            right_glyph = GetGlyphName(rightSide)
            if rightSide[0] != "@" and font.glyphs[right_glyph].leftKerningGroup:
                tabText += "nn/%s/%s nn\n" % (left_glyph, right_glyph)

font.newTab(tabText.strip())
