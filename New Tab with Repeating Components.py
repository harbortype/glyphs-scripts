#MenuTitle: New Tab with Repeating Components
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Opens a new Edit tab with glyphs that contain multiple instance of the same component. They might be interpolating with the wrong ones!
"""

thisFont = Glyphs.font
txt = ""

for thisGlyph in thisFont.glyphs:
	firstLayer = thisGlyph.layers[0]
	# Check for repeating components
	thisGlyphComponents = []
	for thisComponent in firstLayer.components:
		if thisComponent.name in thisGlyphComponents:
			txt += "/{0}".format(thisGlyph.name)
			break
		thisGlyphComponents.append(thisComponent.name)
	# Check for paths with the same number of nodes in the glyph
	thisGlyphPaths = []
	for thisPath in firstLayer.paths:
		nodeOrder = tuple([node.type for node in thisPath.nodes])
		if nodeOrder in thisGlyphPaths:
			txt += "/{0}".format(thisGlyph.name)
			break
		thisGlyphPaths.append(nodeOrder)

if txt:
	Glyphs.font.newTab(txt)
else:
	Message(
		title="New Tab with Repeating Components",
		message="No glyphs with repeating components in this font.",
		OKButton="OK",
	)