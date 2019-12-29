#MenuTitle: Rename Glyphs and Update Features
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Renames glyphs and updates all classes and features. Will match either the entire glyph name or the dot suffix.
"""

# from AppKit import *
import vanilla


font = Glyphs.font

class RenameGlyphs( object ):
	
	def __init__( self ):
		windowWidth = 280
		windowHeight = 115
		self.w = vanilla.Window(
			( windowWidth, windowHeight ),
			"Rename glyphs and update features",
			autosaveName = "com.harbortype.RenameGlyphs.mainwindow"
		)

		self.w.text_1 = vanilla.TextBox( 
			(15, 18+2, 120, 17), 
			"Find" 
		)
		self.w.findString = vanilla.EditText(
			(120, 18-1, -15, 22)
		)

		self.w.text_2 = vanilla.TextBox( 
			(15, 48+2, 120, 17), 
			"Replace with" 
		)
		self.w.replaceString = vanilla.EditText(
			(120, 48-1, -15, 22)
		)

		self.w.renameButton = vanilla.Button(
			(-130, -35, -15, -15),
			"Rename",
			callback=self.Rename
		)
		self.w.undoButton = vanilla.Button(
			(15, -35, 115, -15),
			"Undo",
			callback=self.Undo
		)
		self.w.setDefaultButton( self.w.renameButton )

		# Load settings
		if not self.LoadPreferences():
			print("Note: 'Rename Glyphs and Update Features' could not load preferences. Will resort to defaults.")

		self.w.open()
		self.w.makeKey()


	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.harbortype.RenameGlyphs.findString"] = self.w.findString.get()
			Glyphs.defaults["com.harbortype.RenameGlyphs.replaceString"] = self.w.replaceString.get()
		except:
			return False

		return True


	def LoadPreferences( self ):
		try:
			Glyphs.registerDefault("com.harbortype.RenameGlyphs.findString", "ss01")
			Glyphs.registerDefault("com.harbortype.RenameGlyphs.replaceString", "ss02")
			self.w.findString.set( Glyphs.defaults["com.harbortype.RenameGlyphs.findString"] )
			self.w.replaceString.set( Glyphs.defaults["com.harbortype.RenameGlyphs.replaceString"] )
		except:
			return False

		return True


	def Undo( self, sender ):

		findString = self.w.findString.get()
		replaceString = self.w.replaceString.get()

		self.w.findString.set( replaceString )
		self.w.replaceString.set( findString )

		self.Rename( sender )


	def Rename( self, sender ):

		Glyphs.clearLog()

		self.SavePreferences( sender )

		findString = self.w.findString.get()
		replaceString = self.w.replaceString.get()
		newNames = {}

		font.disableUpdateInterface()

		for glyph in font.glyphs:
		
			# Exact match
			if findString == glyph.name:
				originalName = glyph.name
				glyph.name = replaceString
				newName = glyph.name
				newNames[ originalName ] = newName
				print(originalName, ">", newName)
			
			# Substring match
			elif findString in glyph.name.split("."):
				originalName = glyph.name
				glyph.name = glyph.name.replace( findString, replaceString )
				newName = glyph.name
				newNames[ originalName ] = newName
				print(originalName, ">", newName)

		# Classes
		for otClass in font.classes:

			# Update automatic classes
			if otClass.automatic:
				otClass.update()

			# Find and replace in manual classes
			else:
				code = otClass.code
				for oldName, newName in newNames.iteritems():
					code = code.replace( oldName, newName )
				font.classes[ otClass.name ].code = code

		# Features
		for feature in font.features:
			
			if feature: # Catch an empty feature when first run
				
				# Update automatic features
				if feature.automatic:
					feature.update()

				# Find and replace in manual features
				else:
					code = feature.code
					for oldName, newName in newNames.iteritems():
						code = code.replace( oldName, newName )
					font.features[ feature.name ].code = code

		font.enableUpdateInterface()
		

RenameGlyphs()
