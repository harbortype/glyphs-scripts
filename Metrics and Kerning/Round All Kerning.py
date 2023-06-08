# MenuTitle: Round All Kerning
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Rounds all kerning pairs of the current master (or all masters) according a multiple provided. Requires vanilla.
"""

import vanilla
from Foundation import NSNumberFormatter
from GlyphsApp import Glyphs

font = Glyphs.font
currentMaster = font.selectedFontMaster.id


class RoundAllKerning(object):
    key = "com.harbortype.RoundAllKerning"
    windowHeight = 126
    padding = (10, 10, 12)
    buttonHeight = 20
    textHeight = 14
    sizeStyle = 'small'
    masterOptions = (
        "on currently selected master only",
        "on all masters",
    )

    def __init__(self):

        x, y, p = self.padding

        self.w = vanilla.FloatingWindow(
            (280, self.windowHeight),
            "Round All Kerning"
        )

        y += 8

        # UI elements:
        self.w.text_1 = vanilla.TextBox(
            (x, y, 216, self.textHeight),
            "Round all kerning pairs to multiples of",
            sizeStyle=self.sizeStyle
        )
        # y += self.textHeight

        # Multiple
        formatter = NSNumberFormatter.new()
        self.w.multiple = vanilla.EditText(
            (216, y - 3, -p, 19),
            "10",
            sizeStyle=self.sizeStyle,
            formatter=formatter,
            callback=self.SavePreferences
        )
        y += self.textHeight + p - 4

        # Which masters
        self.w.whichMasters = vanilla.RadioGroup(
            (x * 1.5, y, -p, self.buttonHeight * len(self.masterOptions)),
            self.masterOptions,
            sizeStyle=self.sizeStyle,
            callback=self.SavePreferences,
        )
        self.w.whichMasters.getNSMatrix().setToolTip_(
            "Choose which font masters shall be affected.")

        y += self.buttonHeight * len(self.masterOptions)

        # Run Button:
        self.w.runButton = vanilla.Button(
            (80, -20 - 15, -80, -15),
            "Round kerning",
            sizeStyle='regular',
            callback=self.RoundAllKerningMain
        )
        self.w.setDefaultButton(self.w.runButton)

        # Load Settings:
        if not self.LoadPreferences():
            print(
                "Note: 'Round All Kerning' could not load preferences.\
                Will resort to defaults"
            )

        # Open window and focus on it:
        self.w.open()
        self.w.makeKey()

    def SavePreferences(self, sender):
        try:
            Glyphs.defaults[self.key + ".multiple"] = self.w.multiple.get()
        except:
            return False

        return True

    def LoadPreferences(self):
        try:
            Glyphs.registerDefault(self.key + ".multiple", "10")
            Glyphs.registerDefault(self.key + ".whichMasters", 0)

            self.w.multiple.set(Glyphs.defaults[self.key + ".multiple"])
            self.w.whichMasters.set(
                bool(Glyphs.defaults[self.key + ".whichMasters"])
            )
        except:
            return False

        return True

    def RoundKerningValue(self, kerningValue, base=10):
        return int(base * round(float(kerningValue) / base))

    def GetKey(self, glyph_key):
        if glyph_key.startswith("@"):
            return glyph_key
        return font.glyphForId_(glyph_key).name

    def ProcessMaster(self, master_id):
        kerning_dict = font.kerning[master_id]
        for left_glyph, right_glyphs in kerning_dict.items():
            left_key = self.GetKey(left_glyph)
            for right_glyph, kerning_value in right_glyphs.items():
                right_key = self.GetKey(right_glyph)
                rounded_kerning = self.RoundKerningValue(
                    kerning_value, self.multiple)
                if kerning_value != rounded_kerning:
                    font.setKerningForPair(
                        master_id, left_key, right_key, rounded_kerning)

    def RoundAllKerningMain(self, sender):
        self.multiple = int(self.w.multiple.get())
        self.whichMasters = self.w.whichMasters.get()

        try:
            font.disableUpdateInterface()
            if self.whichMasters == 1:  # all masters
                for this_master in font.masters:
                    self.ProcessMaster(this_master.id)
            else:
                self.ProcessMaster(font.selectedFontMaster.id)
        finally:
            font.enableUpdateInterface()


RoundAllKerning()
