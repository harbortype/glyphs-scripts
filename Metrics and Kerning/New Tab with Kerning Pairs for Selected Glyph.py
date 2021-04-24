#MenuTitle: New Tab with Kerning Pairs for Selected Glyph
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens a new tab with kerning pairs for the selected glyph (minus diacritics)
"""

import GlyphsApp

# Glyphs.clearLog()

def nameForID( font, ID ):
	if ID[0] == "@": # is a group
		return ID
	else: # is a glyph
		return font.glyphForId_( ID ).name

	
font = Glyphs.font
masterID = font.selectedFontMaster.id
masterKernDict = font.kerning[ masterID ]
text = ''
exclude = [ "acute", "breve", "caron", "cedilla", "circumflex", "commaaccent", "dieresis", "dotaccent", "grave", "hungarumlaut", "macron", "ogonek", "ring", "tilde" ]

glyph = font.selectedLayers[0].parent
glyphName = glyph.name
glyphID = glyph.id

leftKey = glyph.leftKerningKey
rightKey = glyph.rightKerningKey

if leftKey[0] == '@':
	leftClass = leftKey
else:
	leftClass = font.glyphs[ glyphName ].id
	
if rightKey[0] == '@':
	rightClass = rightKey
else:
	rightClass = font.glyphs[ glyphName ].id

rightGlyphs = []
if rightClass in masterKernDict.keys():
	for rightPair in masterKernDict[ rightClass ]:
		if rightPair[0] == '@':
			for g in font.glyphs:
				if g.leftKerningKey == rightPair:
					rightGlyphs.append( g.name )
		else:
			rightGlyphs.append( nameForID( font, rightPair ) )

	filterDiacritics = lambda s: not any(x in s for x in exclude)
	rightGlyphs = filter( filterDiacritics, rightGlyphs )

	for r in rightGlyphs:
		text += "/%s/%s/space" % ( glyphName, r )
	text += "\n"

leftGlyphs = []
for leftPair, rightKernDict in masterKernDict.iteritems():
	if leftClass in rightKernDict.keys():
		if leftPair[0] == '@':
			for g in font.glyphs:
				if g.rightKerningKey == leftPair:
					leftGlyphs.append( g.name )
		else:
			leftGlyphs.append( nameForID( font, leftPair ) )

		filterDiacritics = lambda s: not any(x in s for x in exclude)
		leftGlyphs = filter( filterDiacritics, leftGlyphs )
		
for L in leftGlyphs:
	text += '/%s/%s/space' % ( L, glyphName )

# print(text)

if text:
	from PyObjCTools.AppHelper import callAfter
	callAfter( Glyphs.currentDocument.windowController().addTabWithString_, text )

