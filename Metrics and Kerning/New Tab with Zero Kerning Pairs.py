# MenuTitle: New Tab with Zero Kerning Pairs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Opens a new tab with missing kerning pairs (value set as zero) for each master
"""

from GlyphsApp import Glyphs

font = Glyphs.font


# generate glyph names to display in the tabs
def list_name(kerning_key):
    if "@MMK" in kerning_key:
        # if it's a group, just get the last characters in the name
        return "/" + str(kerning_key)[7:]
    if "@" not in kerning_key:
        # if it's not a kerning group, it's a glyph id.
        # iterate through the glyphs in the font to find the name.
        return "/" + str(font.glyphForId_(kerning_key).name)
    # if everything fails, returns an empty string
    return ""


# iterate through the kerning dictionary of each master
# to find pairs with value set as zero
for master in font.masters:
    zeroList = [str(master.name), "\n"]
    for firstG in font.kerning[master.id]:
        for secondG in font.kerning[master.id][firstG]:
            value = font.kerning[master.id][firstG][secondG]
            if value == 0:
                zeroList.append(str(list_name(firstG)))
                zeroList.append(str(list_name(secondG)))
                zeroList.append("\n")
    font.newTab("".join(zeroList))
