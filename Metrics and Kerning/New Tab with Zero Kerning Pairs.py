#MenuTitle: New Tab with Zero Kerning Pairs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens a new tab with missing kerning pairs (value set as zero) for each master
"""

font = Glyphs.font

# generate glyph names to display in the tabs
def listName(g):
    if "@" not in g:
        # if it's not a kerning group, it's a glyph id. iterate through the glyphs in the font to find the name.
        return "/" + font.glyphForId_(g).name
    elif "@MMK" in g:
        # if it's a group, just get the last characters in the name
        return "/" + str(g)[7:]

# iterates through the kerning dictionary of each master to find pairs with value set as zero
for master in font.masters:
    zeroList = [str(master.name), "\n"]
    for firstG in font.kerning[master.id]:
        for secondG in font.kerning[master.id][firstG]:
            value = font.kerning[master.id][firstG][secondG]
            if value == 0:
                zeroList.append(str(listName(firstG)))
                zeroList.append(str(listName(secondG)))
                zeroList.append("\n")
    font.newTab(''.join(zeroList))