#MenuTitle: Copy to Background and Remove Overlaps in All Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Copies all layers of the selected glyphs to the background, remove overlaps and correct path directions in all layers.
"""

import copy

def process( lyr ):
	lyr.setBackground_(lyr)
	lyr.removeOverlap()
	lyr.correctPathDirection()

thisFont = Glyphs.font # frontmost font
selectedLayers = thisFont.selectedLayers # active layers of selected glyphs
master_ids = [master.id for master in thisFont.masters] # all the master ids

# Glyphs.clearLog() # clears log in Macro window
thisFont.disableUpdateInterface() # suppresses UI updates in Font View
 
for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	print("Processing %s" % thisGlyph.name)
	thisGlyph.beginUndo() # begin undo grouping
	for layer in thisGlyph.layers:
		if layer.layerId in master_ids or layer.isSpecialLayer:
			process( layer )
	thisGlyph.endUndo()   # end undo grouping


thisFont.enableUpdateInterface() # re-enables UI updates in Font View
