# MenuTitle: Reorder Axes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
import vanilla
import collections
from AppKit import NSDragOperationMove
from GlyphsApp import Glyphs

__doc__ = """
Reorder axes and their values in masters, instances and special layers. Needs Vanilla.
"""

genericListPboardType = "genericListPboardType"
Glyphs.clearLog()


class ReorderAxes(object):

	thisFont = Glyphs.font  # frontmost font
	axes = collections.OrderedDict()
	for xs in thisFont.axes:
		if Glyphs.versionNumber < 3.0:
			axes[xs["Tag"]] = xs["Name"]
		else:
			axes[xs.axisTag] = xs.name

	def __init__(self):
		# Window 'self.w':
		windowWidth = 280
		windowHeight = 190
		windowWidthResize = 200  # user can resize width by this value
		windowHeightResize = 200  # user can resize height by this value
		self.w = vanilla.Window(
			(windowWidth, windowHeight),  # default window size
			"Reorder Axes",  # window title
			minSize=(windowWidth, windowHeight),  # minimum size (for resizing)
			maxSize=(windowWidth + windowWidthResize, windowHeight + windowHeightResize),  # maximum size (for resizing)
			autosaveName="com.harbortype.ReorderAxes.mainwindow"  # stores last window position and size
		)

		# UI elements:
		linePos, inset, lineHeight = 12, 15, 22
		# self.w.text_1 = vanilla.TextBox((inset-1, linePos+2, 75, 14), "inset", sizeStyle='small')
		# linePos += lineHeight
		listValues = []
		for i, (tag, name) in enumerate(self.axes.items()):
			listValues.append({"Index": i, "Name": name, "Tag": tag})
		self.w.list_1 = vanilla.List(
			(inset, linePos, -inset, -inset - 20 - inset),
			listValues,
			columnDescriptions=[
				{"title": "Index", "width": 40},
				{"title": "Tag", "width": 60},
				{"title": "Name"}],
			allowsMultipleSelection=False,
			allowsEmptySelection=True,
			dragSettings=dict(
				type=genericListPboardType,
				operation=NSDragOperationMove,
				# allowDropBetweenRows = True,
				# allowDropOnRow = False,
				callback=self.dragCallback
			),
			selfDropSettings=dict(
				type=genericListPboardType,
				operation=NSDragOperationMove,
				allowDropBetweenRows=True,
				# allowDropOnRow = False,
				callback=self.selfDropCallback
			)
		)
		linePos += lineHeight

		# Run Button:
		self.w.runButton = vanilla.Button((-80 - inset, -20 - inset, -inset, -inset), "Reorder", sizeStyle='regular', callback=self.Process)
		self.w.setDefaultButton(self.w.runButton)

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def dragCallback(self, sender, indexes):
		self.draggedItems = indexes

	def selfDropCallback(self, sender, dropInfo):
		isProposal = dropInfo["isProposal"]
		if not isProposal:
			target = dropInfo['rowIndex']
			for original in self.draggedItems:
				newList = self.w.list_1.get()
				if target > original:
					newList.insert(target - 1, newList.pop(original))
				else:
					newList.insert(target, newList.pop(original))
				self.w.list_1.set(newList)
		return True

	def Process(self, sender):
		try:
			thisFont = Glyphs.font  # frontmost font
			print("Reorder Axes Report for %s" % thisFont.familyName)
			print(thisFont.filepath)
			print()

			newOrder = [item["Index"] for item in self.w.list_1.get()]
			print("New order is:")
			for i in newOrder:
				if Glyphs.versionNumber < 3.0:
					print(" ", thisFont.axes[i]["Name"])
				else:
					print(" ", thisFont.axes[i].name)
			print()

			# Reorder the font-wide Axes custom parameter
			print("Reordering font axes parameter...")
			newAxes = [thisFont.axes[i] for i in newOrder]
			thisFont.axes = newAxes

			# Reorder the axis values in each font master
			print("Reordering the master's axes values...")
			for master in thisFont.masters:
				newMasterAxes = [master.axes[i] for i in newOrder]
				master.axes = newMasterAxes

			# Reorder the axis values in each instance
			print("Reordering the instances's axes values...")
			for instance in thisFont.instances:
				newInstanceAxes = [instance.axes[i] for i in newOrder]
				instance.axes = newInstanceAxes

			# Process special layers
			print("Reordering values in special layers...")
			for glyph in thisFont.glyphs:
				for layer in glyph.layers:
					if layer.isSpecialLayer and "{" in layer.name:
						first, values = layer.name.split("{")
						values = [x.strip() for x in values[:-1].split(",")]
						if len(values) != len(newOrder):
							print(" ERROR: count of axes in special layer of", glyph.name, "does not match number of axes in font. Skipping...")
							continue
						newValues = [values[i] for i in newOrder]
						newValues = ", ".join(newValues)
						layer.name = "%s{%s}" % (first, newValues)
						print(" ", glyph.name, "-", layer.name)

			# TODO Process delta hints ???
			# for glyph in thisFont.glyphs:
			# 	for layer in glyph.layers:
			# 		for i in reversed(range(len(layer.hints))):
			# 			hint = layer.hints[i]
			# 			if hint.type == TTDELTA:
			# 				elementDict = hint.elementDict()
			# 				if "settings" in elementDict:
			# 					settings = elementDict["settings"]
			# 					if settings:
			# 						for deltaType in ("deltaH","deltaV"):
			# 							if deltaType in settings:
			# 								newDeltas = {}
			# 								# print(len(settings[deltaType]))
			# 								# print(settings[deltaType])
			# 								for transformType in settings[deltaType]:
			# 									# print(transformType)
			# 									transformValues = transformType[1:-1] # remove { and }
			# 									transformValues = transformValues.split(", ")
			# 									newValues = [transformValues[i] for i in newOrder]
			# 									while len(newValues) < len(transformValues):
			# 										newValues.append("0")
			# 									newValues = ", ".join(newValues)
			# 									newTransformType = "{" + newValues + "}"
			# 									# print(transformType)
			# 									# print(newValues)
			# 									# Copy the existing deltas to the
			# 									deltas = settings[deltaType][transformType]
			# 									newDeltas[newTransformType] = deltas
			# 									# settings[deltaType][newTransformType] = deltas
			# 									# del settings[deltaType][transformType]
			# 									# print(deltas)
			# 								settings[deltaType] = newDeltas
			# 								print(settings[deltaType])

			print()
			print("DONE!")
			self.w.close()  # delete if you want window to stay open
		except Exception as e:
			# brings macro window to front and reports error:
			Glyphs.showMacroWindow()
			print("Reorder Axes Error: %s" % e)
			import traceback
			print(traceback.format_exc())


ReorderAxes()
