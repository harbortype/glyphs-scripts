#MenuTitle: Export Fonts into Subfolder
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Exports OTF and TTF at the same time into a specified subfolder. Needs Vanilla.
"""

import os
import errno
import re
import datetime
import vanilla
from AppKit import NSAttributedString, NSColor, NSForegroundColorAttributeName

Glyphs.clearLog()

class exportOtfTtf(object):

	def __init__(self):
		windowWidth = 400
		windowHeight = 285
		margin = 25
		line = 22
		currentLine = 0
		column = (windowWidth - margin*4) / 2
		
		self.w = vanilla.Window(
			(windowWidth, windowHeight),
			"Export OTF and TTF into Subfolder",
			minSize = (windowWidth, windowHeight),
			maxSize = (windowWidth, windowHeight),
			autosaveName = "com.harbortype.exportOtfTtf.mainwindow"
		)

		attributes = { 
			NSForegroundColorAttributeName: NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, .3),
		}
		fontName = NSAttributedString.alloc().initWithString_attributes_(
			"File: " + os.path.basename(Glyphs.font.filepath),
			attributes
		)
		self.w.currentFont = vanilla.TextBox(
			(margin, margin-10, -margin, line),
			fontName,
			alignment = "right"
		)
		currentLine += line


		self.w.subfolder_title = vanilla.TextBox(
			(margin, margin+currentLine, 80, line),
			"Subfolder: "
		)
		self.w.subfolder = vanilla.EditText(
			(margin+80, margin+currentLine-3, -margin, line),
		)
		currentLine += line+13

		self.w.line = vanilla.VerticalLine(
			(windowWidth/2, margin+currentLine, 1, line*3)
		)

		self.w.otf = vanilla.CheckBox(
			(margin, margin+currentLine, column, line),
			"Export OTF",
			callback=self.savePreferences
		)
		currentLine += line
		self.w.otfRemoveOverlaps = vanilla.CheckBox(
			(margin*2, margin+currentLine, column, line),
			"Remove overlaps",
			callback=self.savePreferences
		)
		currentLine += line
		self.w.otfAutohint = vanilla.CheckBox(
			(margin*2, margin+currentLine, column, line),
			"Autohint",
			callback=self.savePreferences
		)
		currentLine -= line*2

		self.w.ttf = vanilla.CheckBox(
			(margin*3+column, margin+currentLine, column, line),
			"Export TTF",
			callback=self.savePreferences
		)
		currentLine += line
		self.w.ttfRemoveOverlaps = vanilla.CheckBox(
			(margin*4+column, margin+currentLine, column, line),
			"Remove overlaps",
			callback=self.savePreferences
		)
		currentLine += line
		self.w.ttfAutohint = vanilla.CheckBox(
			(margin*4+column, margin+currentLine, column, line),
			"Autohint",
			callback=self.savePreferences
		)
		currentLine += line*1.5

		self.w.progress = vanilla.ProgressBar(
			(margin, margin+currentLine, windowWidth-margin*2, 16),
		)
		self.w.progress.set(0) # set progress indicator to zero

		self.w.closeButton = vanilla.Button(
			(margin, -margin-line, windowWidth-margin*2, line),
			"Cancel",
			callback = self.closeWindow
		)
		self.w.runButton = vanilla.Button(
			(margin, -margin-line*2-8, windowWidth-margin*2, line),
			"Export fonts",
			callback = self.export
		)

		if not self.loadPreferences():
			print("Note: Could not load preferences. Will resort to defaults.")

		self.w.setDefaultButton(self.w.runButton)
		self.w.closeButton.bind(unichr(27), [])
		self.w.open()
		self.w.makeKey()

	
	def closeWindow(self, sender):
		self.w.close()
		

	def savePreferences(self, sender):
		try:
			Glyphs.defaults["com.harbortype.exportOtfTtf.subfolder"] = self.w.subfolder.get()
			Glyphs.defaults["com.harbortype.exportOtfTtf.otf"] = self.w.otf.get()
			Glyphs.defaults["com.harbortype.exportOtfTtf.otfRemoveOverlaps"] = self.w.otfRemoveOverlaps.get()
			Glyphs.defaults["com.harbortype.exportOtfTtf.otfAutohint"] = self.w.otfAutohint.get()
			Glyphs.defaults["com.harbortype.exportOtfTtf.ttf"] = self.w.ttf.get()
			Glyphs.defaults["com.harbortype.exportOtfTtf.ttfRemoveOverlaps"] = self.w.ttfRemoveOverlaps.get()
			Glyphs.defaults["com.harbortype.exportOtfTtf.ttfAutohint"] = self.w.ttfAutohint.get()
		except:
			return False

		return True


	def loadPreferences(self):
		try:
			NSUserDefaults.standardUserDefaults().registerDefaults_(
				{
					"com.harbortype.exportOtfTtf.subfolder": "fonts",
					"com.harbortype.exportOtfTtf.otf": 1,
					"com.harbortype.exportOtfTtf.otfRemoveOverlaps": 1,
					"com.harbortype.exportOtfTtf.otfAutohint": 1,
					"com.harbortype.exportOtfTtf.ttf": 1,
					"com.harbortype.exportOtfTtf.ttfRemoveOverlaps": 1,
					"com.harbortype.exportOtfTtf.ttfAutohint": 0,
				}
			)
			self.w.subfolder.set( Glyphs.defaults["com.harbortype.exportOtfTtf.subfolder"] )
			self.w.otf.set( Glyphs.defaults["com.harbortype.exportOtfTtf.otf"] )
			self.w.otfRemoveOverlaps.set( Glyphs.defaults["com.harbortype.exportOtfTtf.otfRemoveOverlaps"] )
			self.w.otfAutohint.set( Glyphs.defaults["com.harbortype.exportOtfTtf.otfAutohint"] )
			self.w.ttf.set( Glyphs.defaults["com.harbortype.exportOtfTtf.ttf"] )
			self.w.ttfRemoveOverlaps.set( Glyphs.defaults["com.harbortype.exportOtfTtf.ttfRemoveOverlaps"] )
			self.w.ttfAutohint.set( Glyphs.defaults["com.harbortype.exportOtfTtf.ttfAutohint"] )
		except:
			return False

		return True


	def export(self, sender):
		self.savePreferences(sender)
		otfExport = bool(self.w.otf.get())
		otfRemoveOverlaps = bool(self.w.otfRemoveOverlaps.get())
		otfAutohint = bool(self.w.otfAutohint.get())
		ttfExport = bool(self.w.ttf.get())
		ttfRemoveOverlaps = bool(self.w.ttfRemoveOverlaps.get())
		ttfAutohint = bool(self.w.ttfAutohint.get())
		
		formats = {
			"otf": {
				"export": otfExport,
				"removeOverlaps": otfRemoveOverlaps,
				"autohint": otfAutohint
			},
			"ttf": {
				"export": ttfExport,
				"removeOverlaps": ttfRemoveOverlaps,
				"autohint": ttfAutohint
			},
		}

		shouldExport = False
		for key in formats.keys():
			if formats[key]["export"] == True:
				shouldExport = True
				break

		# Quit if no formats are set to export
		if shouldExport == False:
			print("No files to export!")
			Glyphs.showMacroWindow()
			quit()
		
		font = Glyphs.font

		# Configure the progress bar
		formatsCount = 0
		for ext in formats:
			if formats[ext]["export"] == True:
				formatsCount += 1
		totalCount = formatsCount * len(font.instances)

		# Set install folder
		subfolder = self.w.subfolder.get()
		currentFolder = os.path.dirname(font.filepath)
		installFolder = os.path.join(currentFolder, subfolder)
		try:
			os.makedirs(installFolder)
		except OSError as exc:  # Python >2.5
		        if exc.errno == errno.EEXIST and os.path.isdir(installFolder):
		            pass
		        else:
		            raise
		
		currentCount = 0
		count = {
			"otf": 0,
			"ttf": 0
		}
		
		for ext in formats:
			if formats[ext]["export"] == True:
				for instance in font.instances:
					try:
						if instance.active:
							fileName = "%s.%s" % (instance.fontName, ext)
							print("Exporting %s" % fileName)
							exportStatus = instance.generate(
								Format = ext.upper(),
								FontPath = installFolder + "/" + fileName,
								AutoHint = formats[ext]["autohint"],
								RemoveOverlap = formats[ext]["removeOverlaps"]
								)
							if exportStatus == True:
								count[ext] += 1
							if exportStatus != True:
								print(exportStatus)
								Glyphs.showMacroWindow()
					except Exception as e:
						print(e)
					currentCount += 1
					self.w.progress.set(100/totalCount*currentCount)

		print("Exported %s" % (font.familyName))
		print("%s otf files" % (count["otf"]))
		print("%s ttf files" % (count["ttf"]))
		Glyphs.showNotification("Exported %s" % (os.path.basename(font.filepath)), "%s otf files\n%s ttf files" % (count["otf"], count["otf"]))
		self.w.close()


exportOtfTtf()
