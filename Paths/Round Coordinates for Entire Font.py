# MenuTitle: Round Coordinates for Entire Font
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Round coordinates of all paths in the entire font.
"""

from GlyphsApp import Glyphs
from Foundation import NSPoint

this_font = Glyphs.font

try:
    this_font.disableUpdateInterface()
    for this_glyph in this_font.glyphs:
        for this_layer in this_glyph.layers:
            for this_path in this_layer.paths:
                for this_node in this_path.nodes:
                    this_node.position = NSPoint(
                        int(this_node.position.x),
                        int(this_node.position.y),
                    )
finally:
    this_font.enableUpdateInterface()
