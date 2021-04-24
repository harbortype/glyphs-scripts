#MenuTitle: Remove all layers for the current master
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Deletes all non-master layers for the current master (including bracket and brace layers) in selected glyphs.
"""

# Glyphs.showMacroWindow()
# Glyphs.clearLog()

font = Glyphs.font
selectedLayers = font.selectedLayers

font.disableUpdateInterface()

for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent

	thisGlyph.beginUndo()

	# Build list of layers to be deleted
	layersToBeDeleted = []
	for currentLayer in thisGlyph.layers:
		if currentLayer.associatedMasterId == thisLayer.layerId:
			if currentLayer.associatedMasterId != currentLayer.layerId:
				layersToBeDeleted.append(currentLayer.layerId)

	# Delete layers
	if len(layersToBeDeleted) > 0:
		for id in layersToBeDeleted:
			del thisGlyph.layers[id]

	thisGlyph.endUndo()

font.enableUpdateInterface()
