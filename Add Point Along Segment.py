#MenuTitle: Add Point Along Segment
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Adds points along selected segments at a specific position (time). Needs Vanilla.
"""

import vanilla

class AddPointAlongSegment( object ):
	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 360
		windowHeight = 60
		windowWidthResize  = 200 # user can resize width by this value
		windowHeightResize = 0   # user can resize height by this value
		self.w = vanilla.FloatingWindow(
			( windowWidth, windowHeight ), # default window size
			"Add Point Along Segment", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.harbortype.AddPointAlongSegment.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		linePos, inset, lineHeight = 12, 15, 22
		buttonWidth = 80
		self.w.time = vanilla.Slider( 
			(inset, linePos, -inset*3-buttonWidth-40, 23), 
			minValue = 0.0,
			maxValue = 1.0,
			tickMarkCount = 3,
			callback=self.UpdateEditText, 
			sizeStyle='regular'
			)
		self.w.edit_1 = vanilla.EditText( 
			(-inset*2-buttonWidth-40, linePos, -inset*2-buttonWidth, 19), 
			"insert text here", 
			sizeStyle='small', 
			callback=self.UpdateSlider
			)
		# linePos += lineHeight
		
		# Run Button:
		self.w.runButton = vanilla.Button( (-buttonWidth-inset, linePos+1, -inset, 17), "Add point", sizeStyle='regular', callback=self.Main )
		self.w.setDefaultButton( self.w.runButton )
		
		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Add Point Along Segment' could not load preferences. Will resort to defaults")
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()
		
	def SavePreferences( self, sender ):
		try:
			Glyphs.defaults["com.harbortype.AddPointAlongSegment.time"] = self.w.time.get()
			Glyphs.defaults["com.harbortype.AddPointAlongSegment.edit_1"] = self.w.edit_1.get()
		except:
			return False
			
		return True

	def LoadPreferences( self ):
		try:
			Glyphs.registerDefault("com.harbortype.AddPointAlongSegment.time", 0.5)
			Glyphs.registerDefault("com.harbortype.AddPointAlongSegment.edit_1", "0.5")
			self.w.time.set( Glyphs.defaults["com.harbortype.AddPointAlongSegment.time"] )
			self.w.edit_1.set( Glyphs.defaults["com.harbortype.AddPointAlongSegment.edit_1"] )
		except:
			return False
			
		return True
	
	def UpdateEditText( self, sender ):
		self.w.edit_1.set(round(self.w.time.get(), 3))

	def UpdateSlider( self, sender ):
		newValue = float(self.w.edit_1.get())
		self.w.time.set(newValue)
	
	def AddPoint( self, pathObject, position ):
		oldPath = pathObject
		oldPathNodes = len(oldPath.nodes)
		newPath = oldPath.copy()
		addedNodes = 0
		for node in pathObject.nodes:
			if node.selected == True:
				nodeIndex = node.index + addedNodes
				if node.prevNode.selected != False:
					newPath.insertNodeWithPathTime_(nodeIndex + position)
					addedNodes = len(newPath.nodes) - oldPathNodes
		return oldPath, newPath

	def Main( self, sender ):
		try:
			# update settings to the latest user input:
			if not self.SavePreferences( self ):
				print("Note: 'Add Point Along Segment' could not write preferences.")
						
			thisFont = Glyphs.font # frontmost font
			thisLayer = Glyphs.font.selectedLayers[0]
			selection = thisLayer.selection
			position = self.w.time.get()

			try:
				# Glyphs 3
				for i in range(len(Layer.shapes)-1, -1, -1):
					shape = Layer.shapes[i]
					if type(shape) == GSPath:
						oldPath, newPath = self.AddPoint(shape, position)
						thisLayer.removeShape_(oldPath)
						thisLayer.addShape_(newPath)
			except:
				# Glyphs 2
				for path in thisLayer.paths:
					oldPath, newPath = self.AddPoint(path, position)
					thisLayer.removePath_(oldPath)
					thisLayer.addPath_(newPath)
			
			
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print("Add Point Along Segment Error: %s" % e)
			import traceback
			print(traceback.format_exc())

AddPointAlongSegment()
