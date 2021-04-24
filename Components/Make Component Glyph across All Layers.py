#MenuTitle: Make Component Glyph across All Layers
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Assembles the selected glyphs from components (the same as running the Make Component Glyph command for all layers) and removes all anchors.
"""

font = Glyphs.font
for selectedLayer in font.selectedLayers:
	glyph = selectedLayer.parent
	for layer in glyph.layers:
		layer.makeComponents()
		layer.anchors = []