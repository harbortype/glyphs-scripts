# MenuTitle: Copy Sort Names from Background Font
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Copies the custom sortNames for all glyphs from the font in the background.
"""

from GlyphsApp import Glyphs, Message

Glyphs.clearLog()

this_font = Glyphs.font

if len(Glyphs.fonts) > 1:
	other_font = Glyphs.fonts[1]
	glyphs_to_process = []

	for this_glyph in this_font.glyphs:
		if this_glyph.name not in other_font.glyphs:
			continue
		other_glyph = other_font.glyphs[this_glyph.name]
		this_sortName = this_glyph.sortName
		other_sortName = other_glyph.sortName
		if this_sortName != other_sortName:
			glyphs_to_process.append((this_glyph.name, other_sortName))

	for glyphname, sortName in glyphs_to_process:
		this_glyph = this_font.glyphs[glyphname]
		this_glyph.sortName = sortName
		print(glyphname, this_glyph.sortName)

else:
	Message(
		title="Copy Sort Names from Background Font",
		message="Only 1 file is open. Please open another Glyphs file.",
	)
