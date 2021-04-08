#MenuTitle: Re-interpolate
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Re-interpolates selected layers. Makes it possible to assign a keyboard shortcut to this command via Preferences > Shortcuts (in Glyphs 3) or System Preferences > Keyboard > Shortcuts > App Shortcuts (in Glyphs 2).
"""

thisFont = Glyphs.font

for thisLayer in thisFont.selectedLayers:
	thisLayer.reinterpolate()