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
            # Round all nodes
            for this_path in this_layer.paths:
                for this_node in this_path.nodes:
                    x = int(this_node.position.x)
                    y = int(this_node.position.y)
                    # Glyphs will only set the position if there is
                    # a difference larger than 1/100 of a unit, so we
                    # force a larger difference of 1 unit and then
                    # set it back to the original coordinates.
                    # https://forum.glyphsapp.com/t/roundcoordinates-doesnt-round-all-coordinates/10936/4
                    this_node.position = NSPoint(x + 1, y + 1)
                    this_node.position = NSPoint(x, y)
            # Round the layer width as well
            if not this_layer.width.is_integer():
                this_layer.width = round(this_layer.width)
finally:
    this_font.enableUpdateInterface()
