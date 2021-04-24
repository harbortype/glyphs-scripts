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

	windowWidth = 400
	windowHeight = 320
	margin = 25
	line = 22
	currentLine = 0
	column = (windowWidth - margin*4) / 2

	attributes = { 
			NSForegroundColorAttributeName: NSColor.colorWithCalibratedRed_green_blue_alpha_(0, 0, 0, .3),
		}

	def __init__(self):
		
		self.w = vanilla.Window(
			(self.windowWidth, self.windowHeight),
			"Export OTF and TTF into Subfolder",
			minSize = (self.windowWidth, self.windowHeight),
			maxSize = (self.windowWidth, self.windowHeight),
			autosaveName = "com.harbortype.exportOtfTtf.mainwindow"
		)

		fontName = NSAttributedString.alloc().initWithString_attributes_(
			"File: " + os.path.basename(Glyphs.font.filepath),
			self.attributes
		)
		self.w.currentFont = vanilla.TextBox(
			(self.margin, self.margin-10, -self.margin, self.line),
			fontName,
			alignment = "right"
		)
		self.currentLine += self.line


		self.w.subfolder_title = vanilla.TextBox(
			(self.margin, self.margin+self.currentLine, 80, self.line),
			"Subfolder: "
		)
		self.w.subfolder = vanilla.EditText(
			(self.margin+80, self.margin+self.currentLine-3, -self.margin, self.line),
		)
		self.currentLine += self.line+13
		
		self.w.allOpenFonts = vanilla.CheckBox(
			(self.margin, self.margin+self.currentLine, self.column, self.line),
			"All open fonts",
			callback=self.savePreferences
		)

		self.currentLine += self.line+13

		self.w.line = vanilla.VerticalLine(
			(self.windowWidth/2, self.margin+self.currentLine, 1, self.line*3)
		)

		self.w.otf = vanilla.CheckBox(
			(self.margin, self.margin+self.currentLine, self.column, self.line),
			"Export OTF",
			callback=self.savePreferences
		)
		self.currentLine += self.line
		self.w.otfRemoveOverlaps = vanilla.CheckBox(
			(self.margin*2, self.margin+self.currentLine, self.column, self.line),
			"Remove overlaps",
			callback=self.savePreferences
		)
		self.currentLine += self.line
		self.w.otfAutohint = vanilla.CheckBox(
			(self.margin*2, self.margin+self.currentLine, self.column, self.line),
			"Autohint",
			callback=self.savePreferences
		)
		self.currentLine -= self.line*2

		self.w.ttf = vanilla.CheckBox(
			(self.margin*3+self.column, self.margin+self.currentLine, self.column, self.line),
			"Export TTF",
			callback=self.savePreferences
		)
		self.currentLine += self.line
		self.w.ttfRemoveOverlaps = vanilla.CheckBox(
			(self.margin*4+self.column, self.margin+self.currentLine, self.column, self.line),
			"Remove overlaps",
			callback=self.savePreferences
		)
		self.currentLine += self.line
		self.w.ttfAutohint = vanilla.CheckBox(
			(self.margin*4+self.column, self.margin+self.currentLine, self.column, self.line),
			"Autohint",
			callback=self.savePreferences
		)
		self.currentLine += self.line*1.5

		self.w.progress = vanilla.ProgressBar(
			(self.margin, self.margin+self.currentLine, self.windowWidth-self.margin*2, 16),
		)
		self.w.progress.set(0) # set progress indicator to zero

		self.w.closeButton = vanilla.Button(
			(self.margin, -self.margin-self.line, self.windowWidth-self.margin*2, self.line),
			"Cancel",
			callback = self.closeWindow
		)
		self.w.runButton = vanilla.Button(
			(self.margin, -self.margin-self.line*2-8, self.windowWidth-self.margin*2, self.line),
			"Export fonts",
			callback = self.export
		)

		if not self.loadPreferences():
			print("Note: Could not load preferences. Will resort to defaults.")

		self.w.setDefaultButton(self.w.runButton)
		try:
			# Python 3
			self.w.closeButton.bind(chr(27), [])
		except:
			# Python 2
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
		
		if self.w.allOpenFonts.get():
			fonts = Glyphs.fonts
		else:
			fonts = [ Glyphs.fonts[0] ]

		# Configure the progress bar
		formatsCount = 0
		for ext in formats:
			if formats[ext]["export"] == True:
				formatsCount += 1
		totalCount = 0
		for font in fonts:
			totalCount += len(font.instances)
		totalCount = formatsCount * totalCount

		for f, font in enumerate(fonts):

			fontName = NSAttributedString.alloc().initWithString_attributes_(
				"[%s/%s] " % (f+1, len(fonts)) + os.path.basename(Glyphs.font.filepath),
				self.attributes
			)
			self.w.currentFont.set(fontName)

			# # Configure the progress bar
			# formatsCount = 0
			# for ext in formats:
			# 	if formats[ext]["export"] == True:
			# 		formatsCount += 1
			# totalCount = formatsCount * len(font.instances)

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
