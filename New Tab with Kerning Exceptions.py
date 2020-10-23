#MenuTitle: New Tab with Kerning Exceptions
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Opens a new Edit tab containing all kerning exceptions for the current master.
"""

tabText=""
currentMasterID = Font.selectedFontMaster.id
masterKerning = Font.kerning[currentMasterID]

for leftSide in masterKerning.keys():
	leftSideGlyph = leftSide[7:] if leftSide[0] == "@" else Font.glyphForId_(leftSide).name
	
	if leftSide[0] != "@" and Font.glyphs[leftSideGlyph].rightKerningGroup:
		for rightSide in masterKerning[leftSide].keys():
			rightSideGlyph = rightSide[7:] if rightSide[0] == "@" else Font.glyphForId_(rightSide).name
			tabText+="nn/%s/%s nn\n" % (leftSideGlyph, rightSideGlyph)
	
	else:
		for rightSide in masterKerning[leftSide].keys():
			rightSideGlyph = rightSide[7:] if rightSide[0] == "@" else Font.glyphForId_(rightSide).name
			if rightSide[0]!="@" and Font.glyphs[rightSideGlyph].leftKerningGroup:
				tabText+="nn/%s/%s nn\n" % (leftSideGlyph, rightSideGlyph)

Font.newTab(tabText.strip())