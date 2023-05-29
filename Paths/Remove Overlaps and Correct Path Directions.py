#MenuTitle: Remove Overlaps and Correct Path Directions in All Masters
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Removes overlaps (if so, copies the original to the background), corrects path directions in all layers and opens a new tab with glyphs that became incompatible. Applies to the selected glyphs only. Reports in Macro Window.
"""

def checkForOverlaps( lyr ):
	if not lyr.paths:
		return False
	paths = list(lyr.paths)
	GSPathOperator = NSClassFromString("GSPathOperator")
	segments = GSPathOperator.segmentsFromPaths_(paths)
	count1 = len(segments)
	try: # Glyphs 3
		GSPathOperator.addIntersections_(segments)		
	except: # Glyphs 2
		PathOperator = GSPathOperator.new()
		PathOperator.addIntersections_(segments)
	count2 = len(segments)
	if count1 != count2:
		return True
	return False

def process( lyr ):
	lyr.setBackground_(lyr)
	lyr.removeOverlap()
	lyr.correctPathDirection()

thisFont = Glyphs.font # frontmost font
selectedLayers = thisFont.selectedLayers # active layers of selected glyphs
master_ids = [master.id for master in thisFont.masters] # all the master ids

# Glyphs.clearLog() # clears log in Macro window
thisFont.disableUpdateInterface() # suppresses UI updates in Font View
 
for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	if not thisGlyph.name:
		continue
	thisGlyph.beginUndo() # begin undo grouping
	if checkForOverlaps(thisGlyph.layers[0]):
		for layer in thisGlyph.layers:
			if layer.layerId in master_ids or layer.isSpecialLayer:
				print("Processing %s : %s" % (thisGlyph.name, layer.name))
				process( layer )
	else:
		for layer in thisGlyph.layers:
			if layer.layerId in master_ids or layer.isSpecialLayer:
				print("Correcting path directions for %s : %s" % (thisGlyph.name, layer.name))
				layer.correctPathDirection()
	thisGlyph.endUndo()   # end undo grouping

text = ""
for thisLayer in selectedLayers:
	thisGlyph = thisLayer.parent
	if thisGlyph.mastersCompatible:
		continue
	else:
		if "/%s " % (thisGlyph.name) not in text:
			text += "/%s " % (thisGlyph.name)

if text:
	thisFont.newTab(text)

thisFont.enableUpdateInterface() # re-enables UI updates in Font View
