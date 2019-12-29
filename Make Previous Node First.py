#MenuTitle: Make Previous Node First
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Moves the start point of the selected  path(s) to the previous oncurve node. Specially useful if assigned to a keyboard shortcut.
"""

thisFont = Glyphs.font
currentMaster = thisFont.selectedFontMaster

# Gets the parent object of every selected element. This return a large 
# list, with many duplicate items, so we'll need to filter it later.
allSelected = [ x.parent for x in thisFont.selectedLayers[0].selection ]

# Loops through previous list, removes all duplicate items keeping only 
# objects that are paths.
selectedPaths = []
for selectedItem in allSelected:
	if selectedItem not in selectedPaths and type(selectedItem) == GSPath:
		selectedPaths.append( selectedItem )

# For each selected path, gets a list of oncurve nodes and makes 
# the last node the first one.
for path in selectedPaths:
	onCurveNodes = [node for node in path.nodes if node.type != "offcurve"]
	onCurveNodes[-2].makeNodeFirst()