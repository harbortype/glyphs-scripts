#MenuTitle: Copy Layer Anchors from Other Font
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Copies the anchors of the current layer from the background file.
"""

this_font = Glyphs.font
other_font = Glyphs.fonts[1]


def CopyAnchors(origin_layer, target_layer):
	print(origin_layer, target_layer)
	target_layer.anchors = []
	for this_anchor in origin_layer.anchors:
		target_layer.anchors.append(this_anchor.copy())

try:
	this_font.disableUpdateInterface()

	master_index = this_font.masters.index(this_font.selectedFontMaster)
	for this_layer in this_font.selectedLayers:
		this_glyph = this_layer.parent
		if this_glyph.name not in other_font.glyphs:
			print(f"{this_glyph.name} does not exist in background font.")
			continue
		origin_glyph = other_font.glyphs[this_glyph.name]
		origin_layer = origin_glyph.layers[master_index]
		target_layer = this_glyph.layers[master_index]
		CopyAnchors(origin_layer, target_layer)

finally:
	this_font.enableUpdateInterface()
