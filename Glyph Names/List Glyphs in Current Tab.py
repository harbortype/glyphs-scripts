# MenuTitle: List Glyphs in Current Tab
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

__doc__ = """
Appends a line with the unique glyphs of the current tab.
"""

from GlyphsApp import Glyphs, Message

thisFont = Glyphs.font
currentTab = thisFont.currentTab

if currentTab:

	allGlyphs = [x.name for x in thisFont.glyphs]
	uniqueGlyphs = []

	for layer in currentTab.layers:
		glyph = layer.parent
		if glyph.name:
			if glyph.name in uniqueGlyphs:
				continue
			uniqueGlyphs.append(glyph.name)

	uniqueGlyphs.sort(key=lambda x: allGlyphs.index(x))

	thisFont.currentText += "\n/" + "/".join(uniqueGlyphs)

else:
	Message(
		title="List Glyphs in Current Tab",
		message="This script only works when an Edit tab is active.",
		OKButton="OK",
	)
