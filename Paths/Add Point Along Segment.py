# MenuTitle: Add Point Along Segment
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Adds points along selected segments at a specific position (time). Needs Vanilla.
"""

import vanilla
from GlyphsApp import Glyphs, GSPath


class AddPointAlongSegment(object):

    key = "com.harbortype.AddPointAlongSegment"

    def __init__(self):
        # Window 'self.w':
        windowWidth = 360
        windowHeight = 60
        windowWidthResize = 200  # user can resize width by this value
        windowHeightResize = 0   # user can resize height by this value
        self.w = vanilla.FloatingWindow(
            (windowWidth, windowHeight),  # default window size
            "Add Point Along Segment",  # window title
            minSize=(windowWidth, windowHeight),  # minimum size (for resizing)
            maxSize=(windowWidth + windowWidthResize, windowHeight + \
                     windowHeightResize),  # maximum size (for resizing)
            # stores last window position and size
            autosaveName=self.key + ".mainwindow"
        )

        # UI elements:
        linePos, inset = 12, 15
        buttonWidth = 80
        self.w.time = vanilla.Slider(
            (inset, linePos, -inset * 3 - buttonWidth - 40, 23),
            minValue=0.0,
            maxValue=1.0,
            tickMarkCount=3,
            callback=self.UpdateEditText,
            sizeStyle='regular'
        )
        self.w.edit_1 = vanilla.EditText(
            (
                -inset * 2 - buttonWidth - 40,
                linePos,
                -inset * 2 - buttonWidth,
                19
            ),
            sizeStyle='small',
            callback=self.UpdateSlider
        )

        # Run Button:
        self.w.runButton = vanilla.Button(
            (-buttonWidth - inset, linePos + 1, -inset, 17),
            "Add point",
            sizeStyle='regular',
            callback=self.Main
        )
        self.w.setDefaultButton(self.w.runButton)

        # Load Settings:
        if not self.LoadPreferences():
            print("Note: 'Add Point Along Segment' could not load \
                preferences. Will resort to defaults")

        # Open window and focus on it:
        self.w.open()
        self.w.makeKey()

    def SavePreferences(self, sender):
        try:
            Glyphs.defaults[self.domain("time")] = self.w.time.get()
            Glyphs.defaults[self.domain("edit_1")] = self.w.edit_1.get()
        except:
            return False
        return True

    def LoadPreferences(self):
        try:
            Glyphs.registerDefault(self.domain("time"), 0.5)
            Glyphs.registerDefault(self.domain("edit_1"), "0.5")
            self.w.time.set(Glyphs.defaults[self.domain("time")])
            self.w.edit_1.set(Glyphs.defaults[self.domain("edit_1")])
        except:
            return False
        return True

    def domain(self, pref_name):
        pref_name = pref_name.strip().strip(".")
        return self.key + "." + pref_name.strip()

    def UpdateEditText(self, sender):
        self.w.edit_1.set(round(self.w.time.get(), 3))

    def UpdateSlider(self, sender):
        newValue = float(self.w.edit_1.get())
        self.w.time.set(newValue)

    def AddPoint(self, pathObject, position):
        oldPath = pathObject
        oldPathNodes = len(oldPath.nodes)
        newPath = oldPath.copy()
        addedNodes = 0
        for node in pathObject.nodes:
            if node.selected and node.prevNode.selected:
                nodeIndex = node.index + addedNodes
                newPath.insertNodeWithPathTime_(nodeIndex + position)
                addedNodes = len(newPath.nodes) - oldPathNodes
        return oldPath, newPath

    def Main(self, sender):
        try:
            # update settings to the latest user input:
            if not self.SavePreferences(self):
                print("Note: 'Add Point Along Segment' could not write \
                    preferences.")

            this_font = Glyphs.font  # frontmost font
            this_layer = this_font.selectedLayers[0]
            position = self.w.time.get()

            if Glyphs.versionNumber >= 3.0:
                for i in range(len(this_layer.shapes) - 1, -1, -1):
                    shape = this_layer.shapes[i]
                    if isinstance(shape, GSPath):
                        oldPath, newPath = self.AddPoint(shape, position)
                        this_layer.removeShape_(oldPath)
                        this_layer.addShape_(newPath)
            else:
                for path in this_layer.paths:
                    oldPath, newPath = self.AddPoint(path, position)
                    this_layer.removePath_(oldPath)
                    this_layer.addPath_(newPath)

        except Exception as e:
            # brings macro window to front and reports error:
            Glyphs.showMacroWindow()
            print("Add Point Along Segment Error: %s" % e)
            import traceback
            print(traceback.format_exc())


AddPointAlongSegment()
