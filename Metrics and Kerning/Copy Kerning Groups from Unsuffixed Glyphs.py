# MenuTitle: Copy Kerning Groups from Unsuffixed Glyphs
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Copies the kerning groups from the default (unsuffixed) glyphs to the selected ones. The selected glyphs need to have a suffix, otherwise they will be skipped.
"""

from GlyphsApp import Glyphs

Glyphs.clearLog()

font = Glyphs.font

for selected_layer in font.selectedLayers:
    this_glyph = selected_layer.parent
    glyph_name = this_glyph.name

    if "." not in glyph_name:
        print("No changes made to {} because if doesn't have a suffix".format(
            glyph_name
        ))
        continue

    default_glyph_name = glyph_name[:glyph_name.index(".")]
    if default_glyph_name not in font.glyphs:
        print("{} does not exist in this font.".format(
            default_glyph_name
        ))
        continue
    default_glyph = font.glyphs[default_glyph_name]

    this_glyph.leftKerningGroup = default_glyph.leftKerningGroup
    this_glyph.rightKerningGroup = default_glyph.rightKerningGroup
    print("Groups copied from {} to {}".format(
        default_glyph_name,
        glyph_name
    ))

Glyphs.showMacroWindow()
