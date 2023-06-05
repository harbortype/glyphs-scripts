# MenuTitle: Set Components Alignment Type 3
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Sets the automatic alignment of all components in the selected glyphs to be type 3 (the type that allows to be vertically shifted). Applies to all masters.
"""

from GlyphsApp import Glyphs, GSShapeTypeComponent

this_font = Glyphs.font

for this_layer in this_font.selectedLayers:
    this_glyph = this_layer.parent
    for glyph_layer in this_glyph.layers:
        for this_shape in glyph_layer.shapes:
            if this_shape.shapeType != GSShapeTypeComponent:
                continue
            this_shape.alignment = 3
