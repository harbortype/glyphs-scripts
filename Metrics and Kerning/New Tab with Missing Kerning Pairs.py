# MenuTitle: New Tab with Missing Kerning Pairs
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

__doc__ = """
Compares two glyphs files and opens a new tab with missing kerning pairs for the current master
"""

from GlyphsApp import Glyphs

Glyphs.clearLog()


# generate glyph names to display in the tabs
def glyphStr(f, g):
	if "@" not in g:
		# if it's not a kerning group, it's a glyph id.
		# iterate through the glyphs in the font to find the name.
		return "/" + f.glyphForId_(g).name
	elif "@MMK" in g:
		# if it's a group, just get the last characters in the name
		return "/" + str(g)[7:]


def getID(g1, g2):
	print(g1, g2)
	# print(type(font1.glyphs[g1]), type(font1.glyphs[g2]))

	# if font1.glyphs[g1] is not None:
	if font1.glyphs[g1].rightKerningKey:
		g1 = font1.glyphs[g1].rightKerningKey
# if font1.glyphs[g2] is not None:
	if font1.glyphs[g2].leftKerningKey:
		g2 = font1.glyphs[g2].leftKerningKey
	# g1 = font1.glyphs[g1].rightKerningKey
	# g2 = font1.glyphs[g2].leftKerningKey
	# if "@" not in g1:
	# 	g1 = font1.glyphs[g1].id
	# if "@" not in g2:
	# 	g2 = font1.glyphs[g2].id
	return g1, g2


font1 = Glyphs.fonts[0]
font2 = Glyphs.fonts[1]

masterID = font1.selectedFontMaster.id
print(masterID)

kerningFront = font1.kerning[masterID]
kerningBack = font2.kerning[masterID]

text = []

pairsFront = []
pairsBack = []

print(kerningFront)

for leftG in kerningFront:
	for rightG in kerningFront[leftG]:
		currentPair = [glyphStr(font1, leftG), glyphStr(font1, rightG)]
		currentPair = ''.join(currentPair)
		pairsFront.append(currentPair)

for leftG in kerningBack:
	for rightG in kerningBack[leftG]:
		currentPair = [glyphStr(font2, leftG), glyphStr(font2, rightG)]
		currentPair = ''.join(currentPair)
		pairsBack.append(currentPair)

for pair in pairsBack:
	if pair not in pairsFront:
		glyphs = pair[1:].split("/")
		leftG, rightG = getID(glyphs[0], glyphs[1])
		print(leftG, rightG)
		kernValue = font1.kerningForPair(masterID, leftG, rightG)
		if kernValue > 100000:
			text.append("/n/n" + pair + "/n/n\n")

text = ''.join(text)
font1.newTab(text)
