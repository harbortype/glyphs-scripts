#MenuTitle: New Tab with Components in Background
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Opens a new Edit tab with glyphs containing components in their backgrounds.
"""

thisFont = Glyphs.font
tabLayers = []

for thisGlyph in thisFont.glyphs:
	glyphHasComponents = False
	for thisLayer in thisGlyph.layers:
		for thisComponent in thisLayer.background.components:
			tabLayers.append(thisLayer)
			glyphHasComponents = True
			break
	if glyphHasComponents:
		tabLayers.append(GSControlLayer(10))


if tabLayers:
	thisFont.newTab()
	thisFont.tabs[-1].layers = tabLayers
else:
	Message(
		title="New Tab with Components in Background",
		message="There are no components in any glyph background.",
		OKButton="OK",
	)