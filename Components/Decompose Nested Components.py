#MenuTitle: Decompose Nested Components
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Decompose nested components on selected glyphs.
"""
from Foundation import NSPoint

thisFont = Glyphs.font
decomposed = []

def hasExportingComponents(glyph):
	for comp in glyph.layers[0].components:
		if comp.component.export:
			return True
	return False

for layer in thisFont.selectedLayers:
	thisGlyph = layer.parent
	for thisLayer in thisGlyph.layers:
		toDecompose = []
		for i in range(len(thisLayer.components)-1,-1,-1):
			thisComponent = thisLayer.components[i]
			thisComponentPosition = thisComponent.position
			otherGlyph = thisFont.glyphs[thisComponent.name]
			if otherGlyph.layers[0].components:
				if hasExportingComponents(otherGlyph):
					otherGlyphPosition = otherGlyph.layers[thisLayer.layerId].components[0].position
					if thisGlyph.name not in decomposed:
						decomposed.append(thisGlyph.name)
					thisComponent.decompose(doAnchors = False)
					# Reposition component
					newComponent = thisLayer.components[i]
					if newComponent.position.y:
						newComponent.automaticAlignment = False
					newComponent.position.x = NSPoint(
						thisComponentPosition.x + otherGlyphPosition.x,
						thisComponentPosition.y + otherGlyphPosition.y
						)



if len(decomposed):
	Glyphs.font.newTab("/" + "/".join(decomposed))
else:
	Message(
		title="Decompose Nested Components",
		message="There are no components of components in the selected glyphs.",
	)