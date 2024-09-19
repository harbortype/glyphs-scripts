# MenuTitle: Re-interpolate Anchors
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

__doc__ = """
Re-interpolates only the anchors on selected layers.
"""

from GlyphsApp import Glyphs

thisFont = Glyphs.font

for thisLayer in thisFont.selectedLayers:
	# create a temporary copy of the current layer
	originalLayer = thisLayer.copy()
	# reinterpolate the layer
	thisLayer.reinterpolate()
	# put back paths and components as of before reinterpolating the layer
	try:  # Glyphs 3
		thisLayer.shapes = originalLayer.shapes
	except:  # Glyphs 2
		thisLayer.paths = originalLayer.paths
		thisLayer.components = originalLayer.components
	thisLayer.width = originalLayer.width
