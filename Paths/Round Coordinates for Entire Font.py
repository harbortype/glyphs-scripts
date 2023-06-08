# MenuTitle: Round Coordinates for Entire Font
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Round coordinates of all paths in the entire font.
"""

from GlyphsApp import Glyphs

this_font = Glyphs.font

for this_glyph in this_font.glyphs:
    for this_layer in this_glyph.layers:
        this_layer.roundCoordinates()
