#MenuTitle: Copy Selected Anchors from Other Font
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Copies the position of the selected anchors from the background file.
"""

this_font = Glyphs.font
other_font = Glyphs.fonts[1]

font_master = this_font.selectedFontMaster
master_index = this_font.masters.index(font_master)

for this_layer in this_font.selectedLayers:
	this_glyph = this_layer.parent
	other_glyph = other_font.glyphs[this_glyph.name]
	other_layer = other_glyph.layers[master_index]
	for this_anchor in this_layer.anchors:
		if this_anchor in this_layer.selection:
			other_anchor = other_layer.anchors[this_anchor.name]
			this_anchor.position = other_anchor.position
