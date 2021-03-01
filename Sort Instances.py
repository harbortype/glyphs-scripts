#MenuTitle: Sort Instances
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import vanilla, collections
from AppKit import NSDragOperationCopy, NSDragOperationMove
__doc__="""
Sorts instances by axes values. Needs Vanilla.
"""

genericListPboardType = "genericListPboardType"

class SortInstances( object ):

	thisFont = Glyphs.font  # frontmost font
	axes = collections.OrderedDict()
	for axis in thisFont.axes[:]:
		try: # Glyphs 3
			axes[axis.axisTag] = axis.name
		except: # Glyphs 2
			axes[axis["Tag"]] = axis["Name"]

	def __init__( self ):
		# Window 'self.w':
		windowWidth  = 280
		windowHeight = 190
		windowWidthResize  = 200 # user can resize width by this value
		windowHeightResize = 200   # user can resize height by this value
		self.w = vanilla.Window(
			(windowWidth, windowHeight), # default window size
			"Sort Instances", # window title
			minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
			maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
			autosaveName = "com.harbortype.SortInstances.mainwindow" # stores last window position and size
		)
		
		# UI elements:
		linePos, inset, lineHeight = 12, 15, 22
		# self.w.text_1 = vanilla.TextBox( (inset-1, linePos+2, 75, 14), "inset", sizeStyle='small' )
		# linePos += lineHeight
		listValues = []
		for i, (tag, name) in enumerate(self.axes.items()):
			listValues.append({"Index": i, "Name": name, "Tag": tag})
		self.w.list_1 = vanilla.List((inset, linePos, -inset, -inset-20-inset),
			listValues,
			columnDescriptions=[
				{"title": "Index", "width": 40},
				{"title": "Tag",   "width": 60},
				{"title": "Name"}],
			allowsMultipleSelection = False,
			allowsEmptySelection = True,
			dragSettings=dict(type=genericListPboardType,
				operation = NSDragOperationMove,
				# allowDropBetweenRows = True,
				# allowDropOnRow = False,
				callback = self.dragCallback),
			selfDropSettings=dict(type=genericListPboardType,
				operation = NSDragOperationMove,
				allowDropBetweenRows = True,
				# allowDropOnRow = False,
				callback = self.selfDropCallback))
		linePos += lineHeight
		
		# Run Button:
		self.w.runButton = vanilla.Button( (-80-inset, -20-inset, -inset, -inset), "Sort", sizeStyle='regular', callback=self.Process )
		self.w.setDefaultButton( self.w.runButton )
		
		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def dragCallback( self, sender, indexes ):
		self.draggedItems = indexes
	
	def selfDropCallback(self, sender, dropInfo):
		isProposal = dropInfo["isProposal"]
		if not isProposal:
			target = dropInfo['rowIndex']
			for original in self.draggedItems:
				newList = self.w.list_1.get()
				if target > original:
					newList.insert(target-1, newList.pop(original))
				else:
					newList.insert(target, newList.pop(original))
				self.w.list_1.set(newList)
		return True
	
	def Process( self, sender ):
		try:
			thisFont = Glyphs.font # frontmost font
			print("Sort Instances Report for %s" % thisFont.familyName)
			print(thisFont.filepath)
			print()
			
			newOrder = [item["Index"] for item in self.w.list_1.get()]
			print("Sorting instances by:")
			for i in newOrder:
				try: # Glyphs 3
					print(" ", thisFont.axes[i].name, i)
				except: # Glyphs 2
					print(" ", thisFont.axes[i]["Name"], i)
			print()
			
			# Sort the instances
			allInstances = thisFont.instances
			allInstances = sorted(allInstances, key=lambda inst: tuple(inst.axes[newOrder[i]] for i in range(len(newOrder))))
			thisFont.instances = allInstances
			
			self.w.close() # delete if you want window to stay open
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print("Sort Instances Error: %s" % e)
			import traceback
			print(traceback.format_exc())

SortInstances()
