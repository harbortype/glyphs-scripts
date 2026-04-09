# MenuTitle: Reinterpolate Sidebearings
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Reinterpolates the LSB and RSB of the selected layers directly. Unlike the Reinterpolate Metrics command, which interpolates LSB and width, this script interpolates the RSB directly. This makes it more appropriate for layers whose outlines are not linear interpolations of other masters, such as intermediate layers or manually edited masters.
"""

import sys
from GlyphsApp import Glyphs, Message

Glyphs.clearLog()

font = Glyphs.font

if not font:
    Message(title="Reinterpolate Sidebearings", message="No font is open.")
    sys.exit()


def axisTag_from_index(axis_index):
    return font.axes[axis_index].axisTag


def get_axis_values(obj):
    return {axisTag_from_index(i): obj.axes[i] for i in range(len(obj.axes))}


def find_closest_masters(master):
    """
    Returns masters that share the same position on all non-wght axes,
    sorted by ascending weight distance to the given master.
    """
    target = get_axis_values(master)
    closest = []
    for other in font.masters:
        if other == master:
            continue
        other_values = get_axis_values(other)
        if all(
            other_values[tag] == target[tag]
            for tag in target
            if tag != "wght"
        ):
            closest.append(other)
    closest.sort(key=lambda m: abs(get_axis_values(m)["wght"] - target["wght"]))
    return closest


def interpolate_value(m1_pos, m2_pos, m3_pos, m1_val, m2_val):
    if not m1_val or m1_val > 99999999999999:
        m1_val = 0
    if not m2_val or m2_val > 99999999999999:
        m2_val = 0
    delta_pos = (m3_pos - m1_pos) / (m2_pos - m1_pos)
    return round(m1_val + delta_pos * (m2_val - m1_val))


this_master = font.selectedFontMaster
this_values = get_axis_values(this_master)

if "wght" not in this_values:
    Message(
        title="Reinterpolate Sidebearings",
        message="No weight axis found in this font.",
    )
    sys.exit()

closest = find_closest_masters(this_master)

if len(closest) < 2:
    Message(
        title="Reinterpolate Sidebearings",
        message="Need at least 2 other masters on the weight axis for interpolation.",
    )
    sys.exit()

master_1, master_2 = closest[0], closest[1]
pos_1 = get_axis_values(master_1)["wght"]
pos_2 = get_axis_values(master_2)["wght"]
pos_current = this_values["wght"]

for layer in font.selectedLayers:
    glyph = layer.parent
    layer_1 = glyph.layers[master_1.id]
    layer_2 = glyph.layers[master_2.id]

    old_lsb = layer.LSB
    old_rsb = layer.RSB

    new_lsb = interpolate_value(pos_1, pos_2, pos_current, layer_1.LSB, layer_2.LSB)
    new_rsb = interpolate_value(pos_1, pos_2, pos_current, layer_1.RSB, layer_2.RSB)

    layer.beginChanges()
    layer.LSB = new_lsb
    layer.RSB = new_rsb
    layer.endChanges()

    print(f"{glyph.name}: LSB {old_lsb} → {new_lsb}, RSB {old_rsb} → {new_rsb}")
