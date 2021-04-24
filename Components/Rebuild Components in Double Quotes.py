#MenuTitle: Rebuild Components in Double Quotes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Replaces components in double quotes using the single quotes in all layers. For example, if the quotedblleft is made from a rotated quotedblright, it will copy the current component to the background and rebuild it using 2 quotelefts.
"""

from Foundation import NSPoint

Glyphs.clearLog()

font = Glyphs.font

quotes = {
	"quoteleft": ["quotedblleft"],
	"quoteright": ["quotedblright"],
	"quotesinglbase": ["quotedblbase"],
}

font.disableUpdateInterface()

for quote in quotes.items():
	base_glyph = quote[0]
	compound_glyphs = quote[1]
	print(compound_glyphs)
	
	if base_glyph not in font.glyphs:
		print("🚫 {} not in font.".format(base_glyph))
		continue
	
	for layer in font.glyphs[base_glyph].layers:
		layer.decomposeComponents()
	
	for glyph in compound_glyphs:
		if glyph not in font.glyphs:
			print("🚫 {} not in font.".format(glyph))
			continue
		for layer in font.glyphs[glyph].layers:
			layer.background = layer.copyDecomposedLayer()
			for component in layer.components:
				original_bounds = component.bounds
				component.name = base_glyph
				component.rotation = 0.0
				new_bounds = component.bounds
				delta_x = original_bounds.origin.x - new_bounds.origin.x
				component.applyTransform((
					1.0, # scale x
					0.0, # skew x
					0.0, # skew y
					1.0, # scale y
					delta_x, # position x
					0.0, # position y
					))
			background_bounds = layer.background.bounds
			new_bounds = layer.bounds
			delta_y = background_bounds.origin.y - new_bounds.origin.y
			layer.applyTransform((
				1.0, # scale x
				0.0, # skew x
				0.0, # skew y
				1.0, # scale y
				0.0, # position x
				delta_y, # position y
				))
			print("✅ Replaced components in {}.".format(glyph))

font.enableUpdateInterface()

Glyphs.showMacroWindow()