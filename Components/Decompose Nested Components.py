#MenuTitle: Decompose Nested Components
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Decompose nested components on selected glyphs.
"""

thisFont = Glyphs.font
decomposed = []

for layer in thisFont.selectedLayers:
	thisGlyph = layer.parent
	for thisLayer in thisGlyph.layers:
		toDecompose = []
		for i in range(len(thisLayer.components)-1,-1,-1):
			thisComponent = thisLayer.components[i]
			otherGlyph = thisFont.glyphs[thisComponent.name]
			if otherGlyph.layers[0].components:
				if thisGlyph.name not in decomposed:
					decomposed.append(thisGlyph.name)
				thisComponent.decompose(doAnchors = False)


if len(decomposed):
	Glyphs.font.newTab("/" + "/".join(decomposed))
else:
	Message(
		title="Decompose Nested Components",
		message="There are no components of components in this font.",
	)