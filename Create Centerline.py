#MenuTitle: Create Centerline
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Creates a centerline between two selected paths. The paths should have opposite directions. If it doesn’t work as expected, try reversing one of the paths.
"""

import GlyphsApp, vanilla
from AppKit import NSPoint

class CreateCenterline( object ):

	def __init__( self ):
		self.w = vanilla.FloatingWindow( (180, 66 ), "", autosaveName="com.harbortype.CreateCenterline.mainwindow" )
		self.w.runButton = vanilla.Button((25, 20, 130, 20), "Create centerline!", sizeStyle='regular', callback=self.interpolatePaths )
		self.w.setDefaultButton( self.w.runButton )
		# self.w.runButton.bind('`', [])
		self.w.open()

		# self.w.makeKey()

	def interpolatedPosition( self, foregroundPosition, backgroundPosition, factor ):
		interpolatedX = foregroundPosition.x * factor + backgroundPosition.x * factor
		interpolatedY = foregroundPosition.y * factor + backgroundPosition.y * factor
		interpolatedPosition = NSPoint( interpolatedX, interpolatedY )
		return interpolatedPosition

	def interpolatePaths( self, sender ):
		font = Glyphs.font
		layer = font.selectedLayers[0]
		selectedPaths = layer.selectedObjects()["paths"]
		factor = 0.5
		# interpolate paths only if 2 paths are selected:
		if ( len(selectedPaths) == 2 ) and ( len(selectedPaths[0]) == len(selectedPaths[1]) ):
			newPath = GSPath()
			thisPath = selectedPaths[0]
			selectedPaths[1].reverse()
			for thisNodeIndex in range(len(thisPath.nodes)):
				thisNode = thisPath.nodes[thisNodeIndex]
				foregroundPosition = thisNode.position
				backgroundPosition = selectedPaths[1].nodes[thisNodeIndex].position
				newNode = GSNode()
				newNode.type = thisNode.type
				newNode.connection = thisNode.connection
				newNode.setPosition_( self.interpolatedPosition( foregroundPosition, backgroundPosition, factor ) )
				newPath.addNode_( newNode )
			if thisPath.closed == True:
				newPath.setClosePath_(1)
			layer.paths.append( newPath )
			layer.roundCoordinates()
		else:
			thisGlyph = layer.parent
			print("%s: incompatible paths in ('%s')." % ( thisGlyph.name, layer.name ))


CreateCenterline()
