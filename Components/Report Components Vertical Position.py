#MenuTitle: Report Components Vertical Position
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Reports the y coordinate of all components in the selected glyphs.
"""

from Foundation import NSPoint
from GlyphsApp import Glyphs

Glyphs.clearLog()

this_font = Glyphs.font

all_positions = {}
for this_layer in this_font.selectedLayers:
	components_coords = []
	for this_component in this_layer.components:
		components_coords.append(this_component.position.y)
	all_positions[this_layer.parent.name] = tuple(components_coords)

for glyph_name, positions in all_positions.items():
	print(positions, glyph_name)

only_positions = list(all_positions.values())
if len(list(set(list(all_positions.values())))) == 1:
	print("✅ All good")
else:
	print("⚠️ Different positions:", set(only_positions))

Glyphs.showMacroWindow()
