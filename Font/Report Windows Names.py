# MenuTitle: Report Windows Names
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

__doc__ = """
Checks for the length of nameID 1 and 4, which can cause issues in Word for Windows and Word for Mac respectively.
"""

from GlyphsApp import Glyphs

Glyphs.clearLog()  # clears macro window log

thisFont = Glyphs.font

for thisInstance in thisFont.instances:
	nameLength = len(thisInstance.windowsFamily)
	flag = "🆗"
	delta = ""
	if nameLength > 31:
		flag = "⛔️"
		delta = "({})".format(31 - nameLength)
	elif nameLength == 31:
		flag = "⚠️"
	print("1 {} [{}] {} {}".format(flag, nameLength, thisInstance.windowsFamily, delta))

	nameLength = len(thisInstance.fullName)
	flag = "🆗"
	delta = ""
	if nameLength > 31:
		flag = "⛔️"
		delta = "({})".format(31 - nameLength)
	elif nameLength == 31:
		flag = "⚠️"
	print("4 {} [{}] {} {}".format(flag, nameLength, thisInstance.fullName, delta))

	nameLength = len(thisInstance.fontName)
	flag = "🆗"
	delta = ""
	if nameLength > 31:
		flag = "⛔️"
		delta = "({})".format(31 - nameLength)
	elif nameLength == 31:
		flag = "⚠️"
	print("6 {} [{}] {} {}".format(flag, nameLength, thisInstance.fontName, delta))
	print("")

Glyphs.showMacroWindow()
