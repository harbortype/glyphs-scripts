#MenuTitle: Replace in Family Name
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Finds and replaces in family name, including Variable Font Family Name and instances’ familyName custom parameters. Needs Vanilla.
"""

import vanilla

class ReplaceInFamilyName( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 250
		windowHeight = 145
		windowWidthResize  = 100 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.Window(
			( windowWidth, windowHeight ), # default window size
			"Replace in Family Name", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.harbortype.ReplaceInFamilyName.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		linePos, inset, lineHeight = 22, 25, 25
		self.w.text_1 = vanilla.TextBox( (inset-1, linePos+2, 75, 14), "Find:", sizeStyle='small' )
		self.w.find = vanilla.EditText( (inset+80, linePos, -inset, 19), "", sizeStyle='small', callback=self.SavePreferences)
		linePos += lineHeight
		self.w.text_2 = vanilla.TextBox( (inset-1, linePos+2, 75, 14), "Replace with:", sizeStyle='small' )
		self.w.replace = vanilla.EditText( (inset+80, linePos, -inset, 19), "", sizeStyle='small', callback=self.SavePreferences)
		linePos += lineHeight
		
		# Run Button:
		self.w.runButton = vanilla.Button( (-80-inset, -20-inset, -inset, -inset), "Run", sizeStyle='regular', callback=self.ReplaceInFamilyNameMain )
		self.w.setDefaultButton( self.w.runButton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Replace in Family Name' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.harbortype.ReplaceInFamilyName.find"] = self.w.find.get()
			Glyphs.defaults["com.harbortype.ReplaceInFamilyName.replace"] = self.w.replace.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			Glyphs.registerDefault("com.harbortype.ReplaceInFamilyName.find", "")
			Glyphs.registerDefault("com.harbortype.ReplaceInFamilyName.replace", "")
			self.w.find.set( Glyphs.defaults["com.harbortype.ReplaceInFamilyName.find"] )
			self.w.replace.set( Glyphs.defaults["com.harbortype.ReplaceInFamilyName.replace"] )
		except:
			return False
			
		return True

	def ReplaceInFamilyNameMain( self, sender ):
		try:
			# update settings to the latest user input:
			if not self.SavePreferences( self ):
				print("Note: 'Replace in Family Name' could not write preferences.")
			
			thisFont = Glyphs.font # frontmost font
			print("Replace in Family Name Report for %s" % thisFont.familyName)
			print(thisFont.filepath)
			print()
			
			findString = self.w.find.get()
			replaceString = self.w.replace.get()

			if not findString:
				raise Exception("The find string cannot be empty.")

			thisFont.disableUpdateInterface()

			# Replace in family name
			if findString in thisFont.familyName:
				oldFamilyName = thisFont.familyName
				newFamilyName = oldFamilyName.replace(findString, replaceString)
				thisFont.familyName = newFamilyName
				if oldFamilyName != newFamilyName:
					print("Font family name renamed from %s to %s" % (oldFamilyName, newFamilyName))

			# Replace in variable font name
			if thisFont.customParameters["Variable Font Family Name"]:
				oldFamilyName = thisFont.customParameters["Variable Font Family Name"]
				newFamilyName = oldFamilyName.replace(findString, replaceString)
				thisFont.customParameters["Variable Font Family Name"] = newFamilyName
				if oldFamilyName != newFamilyName:
					print("Variable Font Family Name renamed from %s to %s" % (oldFamilyName, newFamilyName))

			# Replace in custom parameters in instances
			for thisInstance in thisFont.instances:
				if thisInstance.customParameters["familyName"]:
					oldFamilyName = thisInstance.customParameters["familyName"]
					newFamilyName = oldFamilyName.replace(findString, replaceString)
					thisInstance.customParameters["familyName"] = newFamilyName
					if oldFamilyName != newFamilyName:
						print("Instance %s familyName renamed from %s to %s" % (thisInstance.name, oldFamilyName, newFamilyName))
			
			
			self.w.close() # delete if you want window to stay open
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print("Replace in Family Name Error: %s" % e)
			import traceback
			print(traceback.format_exc())
		
		finally:
			thisFont.enableUpdateInterface()

ReplaceInFamilyName()