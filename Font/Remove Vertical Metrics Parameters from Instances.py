# MenuTitle: Remove Vertical Metrics Parameters from Instances
# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

__doc__ = """
Removes all vertical metrics parameters from instances (typo, hhea and win).
"""

from GlyphsApp import Glyphs

Glyphs.clearLog()  # clears macro window log
font = Glyphs.font

verticalParameters = [
	"typoAscender",
	"typoDescender",
	"typoLineGap",
	"winAscent",
	"winDescent",
	"hheaAscender",
	"hheaDescender"
]
count = 0

for i, instance in enumerate(font.instances):
	for p in reversed(range(len(instance.customParameters))):
		if instance.customParameters[p].name in verticalParameters:
			parameterName = instance.customParameters[p].name
			del instance.customParameters[p]
			print(instance.name, ": removed %s parameter." % (parameterName))
			count += 1

if count == 0:
	print("No vertical metrics parameters were found in instances. Nothing was removed.")

Glyphs.showMacroWindow()
