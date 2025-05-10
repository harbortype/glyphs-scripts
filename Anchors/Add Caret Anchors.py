# MenuTitle: Add Caret Anchors
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Adds caret_* anchors to the selected glyphs based from the base glyphs’ widths. Applies to all layers. Does not modify existing caret anchors.
"""

from AppKit import NSPoint
from math import tan, radians
from GlyphsApp import Glyphs, GSAnchor

Glyphs.clearLog()

this_font = Glyphs.font

glyph_components = {}
selected_glyphs = [lyr.parent for lyr in this_font.selectedLayers]


def get_spacing_components(this_layer):
    """Get a list of the spacing components."""
    spacing_components = []
    for this_component in this_layer.components:
        parent_glyph = this_component.component
        if parent_glyph.subCategory == "Nonspacing":
            continue
        spacing_components.append(this_component)
    return spacing_components


for this_glyph in selected_glyphs:

    # Figure out if the glyph has a dot suffix for ligatures
    suffix = None
    possible_suffixes = [".liga", ".dlig", ".rlig"]
    for sufx in possible_suffixes:
        if sufx in this_glyph.name:
            suffix = sufx
            break

    for this_layer in this_glyph.layers:

        layer_id = this_layer.layerId
        x_height = this_font.masters[layer_id].xHeight
        italic_angle = this_font.masters[layer_id].italicAngle
        italic_offset = tan(radians(italic_angle)) * (x_height / 2)

        layer_components = get_spacing_components(this_layer)
        layer_anchors = [anchor.name for anchor in this_layer.anchors]

        if layer_components and not this_layer.paths:
            for i, this_component in enumerate(layer_components):
                if i == 0:
                    continue  # Skip the first component
                offset = this_component.position.x
                new_anchor_name = "caret_" + str(i)
                if new_anchor_name not in layer_anchors:
                    new_anchor = GSAnchor(
                        new_anchor_name,
                        NSPoint(round(offset - italic_offset), 0)
                    )
                    this_layer.anchors.append(new_anchor)
