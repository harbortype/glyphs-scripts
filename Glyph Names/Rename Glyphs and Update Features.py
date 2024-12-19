# MenuTitle: Rename Glyphs and Update Features
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

__doc__ = """
Renames glyphs and updates all classes and features. Will match either the entire glyph name or the dot suffix.
"""

import vanilla
import copy
from GlyphsApp import Glyphs, GSClass, GSFeature

font = Glyphs.font


class RenameGlyphs(object):

	def __init__(self):
		windowWidth = 280
		windowHeight = 115
		self.w = vanilla.FloatingWindow(
			(windowWidth, windowHeight),
			"Rename glyphs and update features",
			autosaveName="com.harbortype.RenameGlyphs.mainwindow"
		)

		self.w.text_1 = vanilla.TextBox(
			(15, 18 + 2, 120, 17),
			"Find"
		)
		self.w.findString = vanilla.EditText(
			(120, 18 - 1, -15, 22)
		)

		self.w.text_2 = vanilla.TextBox(
			(15, 48 + 2, 120, 17),
			"Replace with"
		)
		self.w.replaceString = vanilla.EditText(
			(120, 48 - 1, -15, 22)
		)

		self.w.renameButton = vanilla.Button(
			(-130, -35, -15, -15),
			"Rename",
			callback=self.Main
		)
		self.w.undoButton = vanilla.Button(
			(15, -35, 115, -15),
			"Undo",
			callback=self.Undo
		)
		self.w.undoButton.enable(False)
		self.w.setDefaultButton(self.w.renameButton)

		# Load settings
		if not self.LoadPreferences():
			print("Note: 'Rename Glyphs and Update Features' could not load preferences. Will resort to defaults.")

		self.w.open()
		self.w.makeKey()

		self.changedGlyphs = []
		self.classesBackup = []
		self.featuresBackup = []

	def SavePreferences(self, sender):
		try:
			Glyphs.defaults["com.harbortype.RenameGlyphs.findString"] = self.w.findString.get()
			Glyphs.defaults["com.harbortype.RenameGlyphs.replaceString"] = self.w.replaceString.get()
		except:
			return False

		return True

	def LoadPreferences(self):
		try:
			Glyphs.registerDefault("com.harbortype.RenameGlyphs.findString", "ss01")
			Glyphs.registerDefault("com.harbortype.RenameGlyphs.replaceString", "ss02")
			self.w.findString.set(Glyphs.defaults["com.harbortype.RenameGlyphs.findString"])
			self.w.replaceString.set(Glyphs.defaults["com.harbortype.RenameGlyphs.replaceString"])
		except:
			return False

		return True

	def Undo(self, sender):
		font.disableUpdateInterface()
		oldNames = [glyphNames["old"] for glyphNames in self.changedGlyphs]
		newNames = [glyphNames["new"] for glyphNames in self.changedGlyphs]
		for i in range(len(newNames)):
			font.glyphs[newNames[i]].name = oldNames[i]
		# Restore the classes and features backup
		font.classes = self.classesBackup
		font.features = self.featuresBackup
		# Empty the changed glyphs list
		self.changedGlyphs = []
		self.w.undoButton.enable(False)
		font.enableUpdateInterface()

	def ReplaceInCode(self, oldNames, newNames, code):
		for i in range(len(oldNames)):
			code = code.replace(oldNames[i], newNames[i])
		return code

	def RenameFeatures(self, oldNames, newNames):
		# Stitch together classes and features in a single loop
		for classes_and_features in [font.classes, font.features]:
			# Loop through classes and features in reverse order
			# because it might delete some automatic features
			for f in range(len(classes_and_features) - 1, -1, -1):
				class_or_feature = classes_and_features[f]
				if isinstance(class_or_feature, GSClass):
					objType = "class"
				else:
					objType = "feature"
				# Catch an empty feature when first run
				if not class_or_feature:
					continue
				# Trigger update if automatic
				if class_or_feature.automatic:
					# Only update if glyphname appears in the class/feature
					if any(glyphName in class_or_feature.code for glyphName in oldNames):
						class_or_feature.update()
						print("Updated %s %s" % (objType, class_or_feature.name))
				# Find and replace in manual features
				else:
					code = self.ReplaceInCode(oldNames, newNames, class_or_feature.code)
					if isinstance(class_or_feature, GSClass):
						font.classes[class_or_feature.name].code = code
					elif isinstance(class_or_feature, GSFeature):
						font.features[class_or_feature.name].code = code
					print("Replaced in %s %s" % (objType, class_or_feature.name))

	def Main(self, sender):

		Glyphs.clearLog()
		self.SavePreferences(sender)
		font.disableUpdateInterface()

		print("Rename Glyphs and Update Features for %s" % font.familyName)
		print(font.filepath)
		print()

		findString = self.w.findString.get()
		replaceString = self.w.replaceString.get()
		namesDict = {}

		# Store classes and features for undo
		self.classesBackup = copy.copy(font.classes)
		self.featuresBackup = copy.copy(font.features)
		self.w.undoButton.enable(True)

		for glyph in font.glyphs:

			# Exact match
			if findString == glyph.name:
				glyph.beginUndo()
				originalName = glyph.name
				glyph.name = replaceString
				newName = glyph.name
				namesDict[originalName] = newName
				glyph.endUndo()
				self.changedGlyphs.append({
					"old": originalName,
					"new": newName
				})
				print(originalName, ">", newName)

			# Substring match
			elif findString in glyph.name.split("."):
				glyph.beginUndo()
				originalName = glyph.name
				glyph.name = glyph.name.replace(findString, replaceString)
				newName = glyph.name
				namesDict[originalName] = newName
				glyph.endUndo()
				self.changedGlyphs.append({
					"old": originalName,
					"new": newName
				})
				print(originalName, ">", newName)

		oldNames = [glyphNames["old"] for glyphNames in self.changedGlyphs]
		newNames = [glyphNames["new"] for glyphNames in self.changedGlyphs]
		self.RenameFeatures(oldNames, newNames)

		font.enableUpdateInterface()


RenameGlyphs()
