#MenuTitle: Reverse PS Hint
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__="""
Reverses the direction of the selected PS hints.
"""

this_font = Glyphs.font

for this_layer in this_font.selectedLayers:
	try:
		this_font.disableUpdateInterface()
		for this_hint in this_layer.hints:
			if this_hint.selected and this_hint.isPostScript:
				if this_hint.type != STEM:
					continue
				origin_node = this_hint.originNode
				target_node = this_hint.targetNode
				this_hint.originNode = target_node
				this_hint.targetNode = origin_node
	except Exception as e:
		raise e
	finally:
		this_font.enableUpdateInterface()
