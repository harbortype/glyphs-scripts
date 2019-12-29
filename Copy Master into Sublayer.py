#MenuTitle: Copy Master into Sublayer...
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Copies a master into a sublayer of another master for the selected glyphs. Useful for creating COLR/CPAL color fonts. Based on @mekkablue's Copy Layer to Layer script.
"""

import vanilla

thisFont = Glyphs.font
currentMaster = thisFont.selectedFontMaster


class CopyMasterIntoSublayer( object ):

	def __init__( self ):
		windowWidth  = 280
		windowHeight = 150
		windowWidthResize  = 0
		windowHeightResize = 0
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ),
			"Copy master into sublayer", 
			minSize = ( windowWidth, windowHeight ), 
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), 
			autosaveName = "com.harbortype.CopyMasterIntoSublayer.mainwindow" 
		)

		self.w.text_1 = vanilla.TextBox((15, 12+2, 120, 14), "Copy paths from:", sizeStyle='small')
		self.w.masterSource = vanilla.PopUpButton((120, 12, -15, 17), self.GetMasterNames(), sizeStyle='small', callback=None)

		self.w.text_2 = vanilla.TextBox((15, 48+2, 120, 14), "into the sublayer:", sizeStyle='small')
		self.w.layerTarget = vanilla.EditText((120, 48-1, -15, 18), sizeStyle='small', callback=None)

		self.w.text_3 = vanilla.TextBox((15, 48+22, 120, 14), "of master:", sizeStyle='small')
		self.w.masterDestination = vanilla.PopUpButton((120, 48+20, -15, 17), self.GetMasterNames(), sizeStyle='small', callback=None)

		
		self.w.copybutton = vanilla.Button((-80, -30, -15, -10), "Copy", sizeStyle='small', callback=self.CopyAll )
		self.w.setDefaultButton( self.w.copybutton )

		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Copy Master into Sublayer' could not load preferences. Will resort to defaults.")

		self.w.open()
		self.w.makeKey()


	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.layerTarget"] = self.w.layerTarget.get()
		except:
			return False

		return True


	def LoadPreferences( self ):
		try:
			Glyphs.registerDefault("com.harbortype.CopyMasterIntoSublayer.layerTarget", "Color 0")
			self.w.layerTarget.set( Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.layerTarget"] )
		except:
			return False

		return True


	def GetMasterNames( self ):
		"""Collects names of masters to populate the submenu in the GUI."""
		myMasterList = []
		for masterIndex in range( len( thisFont.masters ) ):
			thisMaster = thisFont.masters[masterIndex]
			myMasterList.append( '%i: %s' % (masterIndex, thisMaster.name) )
		return myMasterList


	def CheckIfSublayerExists( self, masterId, sublayerName, glyph ):
		"""Checks if there is a sublayer of the same name. 
		If it does, clear the layer. 
		If it doesn't, create the layer."""
		for layer in glyph.layers:
			# Find a layer with the name informed by the user and associated with the current master.
			# Effectively, this will loop through all layers in all masters and return only if the layer
			# is a child of the current master (associatedMasterId)
			if layer.name == sublayerName and layer.associatedMasterId == masterId:
				return layer
		return None


	def CreateEmptySublayer( self, masterId, sublayerName, glyph ):
		"""Creates a new empty GSLayer object and appends it to the current glyph under the current master."""
		newLayer = GSLayer()
		newLayer.name = sublayerName
		newLayer.associatedMasterId = masterId
		glyph.layers.append(newLayer)


	def ClearSublayer( self, sublayer ):
		"""Clears all content from the current layer."""
		sublayer.paths = None
		sublayer.components = None
		sublayer.anchors = None
		sublayer.background = None


	def CopyAll( self, sender ):
		"""Copies all data into the sublayer."""
		sublayerName = self.w.layerTarget.get()
		indexOfMasterSource = self.w.masterSource.get()
		indexOfMasterDestination = self.w.masterDestination.get()
		masterDestinationId = thisFont.masters[ indexOfMasterDestination ].id
		# Gets the selected glyphs
		selectedGlyphs = [ x.parent for x in thisFont.selectedLayers ]

		# For each selected glyph
		for glyph in selectedGlyphs:

			# Prepare sublayer
			sublayer = self.CheckIfSublayerExists( masterDestinationId, sublayerName, glyph )
			if sublayer:
				self.ClearSublayer( sublayer )
			else:
				self.CreateEmptySublayer( masterDestinationId, sublayerName, glyph )
				sublayer = self.CheckIfSublayerExists( masterDestinationId, sublayerName, glyph )

			# Copy paths, components and anchors
			sublayer.paths = glyph.layers[ indexOfMasterSource ].paths
			sublayer.components = glyph.layers[ indexOfMasterSource ].components
			sublayer.anchors = glyph.layers[ indexOfMasterSource ].anchors


CopyMasterIntoSublayer()
