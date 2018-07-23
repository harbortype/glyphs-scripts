#MenuTitle: Make Next Node First
# -*- coding: utf-8 -*-
__doc__="""
Moves the first node of the path to the next one
"""

thisFont = Glyphs.font

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
# the secondmost node the first one.
for path in selectedPaths:
    onCurveNodes = [node for node in path.nodes if node.type != "offcurve"]
    onCurveNodes[0].makeNodeFirst()