#MenuTitle: Add Extremes to Selection
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Adds extreme points to selected paths.
"""

thisFont = Glyphs.font
thisLayer = thisFont.selectedLayers[0]

for path in thisLayer.paths:
	if path.selected:
		path.addNodesAtExtremes()
		path.selected = True