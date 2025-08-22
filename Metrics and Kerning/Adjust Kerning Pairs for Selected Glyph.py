#MenuTitle: Adjust Kerning Pairs for Selected Glyph
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Adjust all kerning pairs of the selected glyph for the current master or all masters. Requires vanilla.
"""

import vanilla
from GlyphsApp.UI import *
from Foundation import NSNumberFormatter

Glyphs.clearLog()

font = Glyphs.font
current_master = font.selectedFontMaster.id
current_glyph = font.selectedLayers[0].parent


class AdjustKerningPairsForSelection(object):
	key = "com.harbortype.AdjustKerningPairsForSelection"
	windowWidth = 480
	windowHeight = 100
	padding = (10, 10, 12)
	buttonHeight = 20
	sizeStyle = 'regular'
	textHeight = 17
	masterOptions = (
		"on currently selected master only",
		"on all masters",
		)


	def __init__(self):

		x, y, p = self.padding

		self.w = vanilla.FloatingWindow(
			(self.windowWidth, self.windowHeight),
			"Adjust Kerning Pairs for Selected Glyphs",
			minSize = (self.windowWidth, self.windowHeight),
			maxSize = (self.windowWidth+200, self.windowHeight+200),
			)

		y += 8

		# UI elements:
		self.w.text_1 = vanilla.TextBox("auto", "Adjust kerning for selected glyphs by:", sizeStyle=self.sizeStyle)

		# Glyph view
		self.w.glyphs = vanilla.Group("auto")
		self.w.glyphs.selectedGlyph = GlyphView("auto", layer=font.selectedLayers[0])
		self.w.glyphs.onLeftSide = vanilla.EditText("auto", "10", sizeStyle=self.sizeStyle, callback=self.SavePreferences)
		self.w.glyphs.centerGlyph = GlyphView("auto", layer=font.glyphs["o"].layers[current_master])
		self.w.glyphs.onRightSide = vanilla.EditText("auto", "10", sizeStyle=self.sizeStyle, callback=self.SavePreferences)
		self.w.glyphs.selectedGlyph2 = GlyphView("auto", layer=font.selectedLayers[0])

		# Which masters
		self.w.whichMasters = vanilla.RadioGroup(
			"auto",
			self.masterOptions,
			sizeStyle=self.sizeStyle,
			callback=self.SavePreferences,
			)
		self.w.whichMasters.getNSMatrix().setToolTip_("Choose which font masters shall be affected.")

		# Don’t invert kerning sign
		self.w.invertSign = vanilla.CheckBox("auto", "Allow turning negative kerning into positive kerning and vice-versa", sizeStyle=self.sizeStyle, callback=self.SavePreferences)

		self.w.flex1 = vanilla.Group("auto")
		self.w.flex2 = vanilla.Group("auto")
		self.w.flex3 = vanilla.Group("auto")

		glyphs_rules = [
			# Horizontal
			"H:|[selectedGlyph]-[onLeftSide(==40)]-[centerGlyph(==selectedGlyph)]-[onRightSide(==onLeftSide)]-[selectedGlyph2(==selectedGlyph)]|",
			# Vertical
			"V:|[selectedGlyph(>=80)]|",
			"V:|-39-[onLeftSide(==22)]-39-|",
			"V:|[centerGlyph(==selectedGlyph)]|",
			"V:|-39-[onRightSide(==onLeftSide)]-39-|",
			"V:|[selectedGlyph2(==selectedGlyph)]|",
		]

		# Run Button:
		self.w.runButton = vanilla.Button("auto", "Adjust kerning", sizeStyle='regular', callback=self.AdjustKerningPairsForSelectionMain)
		self.w.setDefaultButton(self.w.runButton)

		rules = [
			# Horizontal
			"H:|-border-[text_1]-border-|",
			"H:|-border-[glyphs]-border-|",
			"H:|-border-[whichMasters]-border-|",
			"H:|-border-[invertSign]-border-|",
			"H:|-border-[flex1(>=space)]-[runButton]-border-|",
			# Vertical
			"V:|-border-[text_1]-space-[glyphs]-space-[whichMasters]-space-[invertSign]-space-[runButton]-border-|",
		]
		metrics = {
			"border" : 20,
			"space" : 16,
		}
		self.w.glyphs.addAutoPosSizeRules(glyphs_rules, metrics)
		self.w.addAutoPosSizeRules(rules, metrics)


		# Load Settings:
		if not self.LoadPreferences():
			print("Note: 'Round All Kerning' could not load preferences. Will resort to defaults")

		# Open window and focus on it:
		self.w.open()
		self.w.makeKey()

	def SavePreferences(self, sender):
		try:
			Glyphs.defaults["com.harbortype.AdjustKerningPairsForSelection.onLeftSide"] = self.w.glyphs.onLeftSide.get()
			Glyphs.defaults["com.harbortype.AdjustKerningPairsForSelection.onRightSide"] = self.w.glyphs.onRightSide.get()
			# Glyphs.defaults["com.harbortype.AdjustKerningPairsForSelection.whichMasters"] = self.w.whichMasters.get()
		except:
			return False

		return True

	def LoadPreferences(self):
		try:
			Glyphs.registerDefault("com.harbortype.AdjustKerningPairsForSelection.onLeftSide", "10")
			Glyphs.registerDefault("com.harbortype.AdjustKerningPairsForSelection.onRightSide", "10")
			Glyphs.registerDefault("com.harbortype.AdjustKerningPairsForSelection.whichMasters", 0)

			self.w.glyphs.onLeftSide.set(Glyphs.defaults["com.harbortype.AdjustKerningPairsForSelection.onLeftSide"])
			self.w.glyphs.onRightSide.set(Glyphs.defaults["com.harbortype.AdjustKerningPairsForSelection.onRightSide"])
			self.w.whichMasters.set(bool(Glyphs.defaults["com.harbortype.AdjustKerningPairsForSelection.whichMasters"]))
		except:
			return False

		return True


	def CalculateKerningValue(self, current_value, adjust_by):
		if self.invertSign:
			return current_value + adjust_by
		else:
			# Prevent switching number sign
			if (current_value < 0 and adjust_by > 0) or (current_value > 0 and adjust_by < 0):
				if abs(current_value) <= abs(adjust_by):
					return 0
			return current_value + adjust_by


	def AdjustKerningPair(self, master_id, left_key, right_key, current_value, adjust_by):
		if not adjust_by:
			return
		adjusted_kerning = self.CalculateKerningValue(current_value, adjust_by)
		if current_value != adjusted_kerning:
			font.setKerningForPair(master_id, left_key, right_key, adjusted_kerning)
			print("Changed kerning between {} and {} from {} to {}".format(
				left_key,
				right_key,
				current_value,
				adjusted_kerning
				))



	def GetKey(self, glyph_key):
		if glyph_key.startswith("@"):
			return glyph_key
		return font.glyphForId_(glyph_key).name


	def ProcessMaster(self, master_id):
		print("\n=== MASTER {} ===".format(font.masters[master_id].name))
		kerning_dict = font.kerning[master_id]
		for left_glyph, right_glyphs in kerning_dict.items():
			left_key = self.GetKey(left_glyph)
			for right_glyph, kerning_value in right_glyphs.items():
				right_key = self.GetKey(right_glyph)
				if left_key == current_glyph.rightKerningKey:
					self.AdjustKerningPair(master_id, left_key, right_key, kerning_value, self.onLeftSide)
				if right_key == current_glyph.leftKerningKey:
					self.AdjustKerningPair(master_id, left_key, right_key, kerning_value, self.onRightSide)


	def AdjustKerningPairsForSelectionMain(self, sender):
		onLeftSide = self.w.glyphs.onLeftSide.get()
		self.onLeftSide = int(onLeftSide) if onLeftSide else 0
		onRightSide = self.w.glyphs.onRightSide.get()
		self.onRightSide = int(onRightSide) if onRightSide else 0
		self.whichMasters = self.w.whichMasters.get()
		self.invertSign = self.w.invertSign.get()

		if self.whichMasters == 1: # all masters
			for this_master in font.masters:
				self.ProcessMaster(this_master.id)
		else:
			self.ProcessMaster(font.selectedFontMaster.id)

		self.w.close()


AdjustKerningPairsForSelection()
