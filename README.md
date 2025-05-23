# Glyphs scripts

An assortment of scripts for the [Glyphs font editor](http://glyphsapp.com/).

## Script list

### Anchors

- **Add Caret Anchors:** Adds caret_* anchors to the selected glyphs based from the base glyphs’ widths. Applies to all layers. Does not modify existing caret anchors.
- **Copy Layer Anchors from Other Font:** Copies the anchors of the current layer from the background file.
- **Copy Selected Anchors from Other Font:** Copies the position of the selected anchors from the background file.
- **Re-interpolate Anchors:** Re-interpolates only the anchors on selected layers.

### Color Fonts

- **SVG Export and SVG Import:** Generates SVGs from inside Glyphs and reimports them for creating SVG color fonts. More information below. Needs Vanilla and Drawbot.

### Components

- **Decompose Nested Components:** Decompose nested components on selected glyphs.
- **Make Component Glyph across All Layers:** Assembles the selected glyphs from components (the same as running the Make Component Glyph command for all layers) and removes all anchors.
- **New Tab with Components in Background:** Opens a new Edit tab with glyphs containing components in their backgrounds.
- **New Tab with Nested Components:** Opens a new Edit tab with glyphs that contain components made of components.
- **Rebuild Components in Double Quotes:** Replaces components in double quotes using the single quotes in all layers. For example, if the quotedblleft is made from a rotated quotedblright, it will copy the current component to the background and rebuild it using 2 quotelefts.
- **Report Components Vertical Position:** Reports the y coordinate of all components in the selected glyphs.
- **Set Components Alignment Type 3:** Sets the automatic alignment of all components in the selected glyphs to be type 3 (the type that allows to be vertically shifted). Applies to all masters.

### Font

- **Export Fonts into Subfolder:** Exports OTF and TTF at the same time into a specified subfolder. Needs Vanilla.
- **Remove Vertical Metrics Parameters from Instances:** Removes all vertical metrics parameters from instances (typo, hhea and win).
- **Reorder Axes:** Reorder axes and their values in masters, instances and special layers. Needs Vanilla.
- **Replace in Family Name:** Finds and replaces in family name, including Variable Font Family Name and instances’ familyName custom parameters. Needs Vanilla.
- **Sort Instances:** Sorts instances by axes values. Needs Vanilla.

### Glyph Names

- **Copy Sort Names from Background Font:** Copies the custom sortNames for all glyphs from the font in the background.
- **List Glyphs in Current Tab:** Appends a line with the unique glyphs of the current tab.
- **Rename Glyphs and Update Features:** Renames glyphs and updates all classes and features. Will match either the entire glyph name or the dot suffix. Needs Vanilla.

### Hinting

- **Export Hinting Test Page (HTML):** Create a Test HTML for the current font inside the current Webfont Export folder, or for the current Glyphs Project in the project’s export path.
Based on mekkablue's Webfont Test HTML script.
- **New Tab with Rotated, Scaled or Flipped Components:** Opens a new edit tab with components that were rotated, scaled or flipped. They may cause issues on TrueType.
- **New Tab with Vertically Shifted Components:** Opens a new edit tab with components that are transformed beyond mere horizontal shifts.
- **Reverse PS Hint:** Reverses the direction of the selected PS hints.

### Interpolation

- **New Tab with Repeating Components and Paths:** Opens a new Edit tab with glyphs that contain multiple instances of the same component or path. They might be interpolating with the wrong ones!

### Layers

- **Copy Master into Sublayer:** Copies a master into a sublayer of another master for the selected glyphs. Useful for creating COLR/CPAL color fonts. Based on [@mekkablue](https://github.com/mekkablue/Glyphs-Scripts)'s Copy Layer to Layer script. Needs Vanilla.
- **Remove all layers for the current master:** Deletes all non-master layers for the current master (including bracket and brace layers) in selected glyphs.

### Metrics and Kerning

- **Copy Kerning Groups from Unsuffixed Glyphs:** Copies the kerning groups from the default (unsuffixed) glyphs to the selected ones. The selected glyphs need to have a dot suffix, otherwise they will be skipped.
- **New Tab with Kerning Exceptions:** Opens a new Edit tab containing all kerning exceptions for the current master.
- **New Tab with Kerning Pairs for Selected Glyph:** Opens a new tab with kerning pairs for the selected glyph (minus diacritics).
- **New Tab with Missing Kerning Pairs:** Compares two glyphs files and opens a new tab with missing kerning pairs for the current master.
- **New Tab with Zero Kerning Pairs:** Opens a new tab with missing kerning pairs (value set as zero) for each master.
- **Round all Kerning:** Rounds all kerning pairs of the current master (or all masters) according a multiple provided by you.

### Paths

- **Add Extremes to Selection:** Adds extreme points to selected paths.
- **Add Nodes on Selected Segments at 45°:** Adds nodes at 45° on selected segments. Interpolation may produce kinks if a node changes the angle AND proportion of its handles between masters. This is not a problem for extremes, but sometimes we need to add intermediate nodes to better control a curve. The easiest way to ensure no kinks will happen in difficult curves is to keep the handles at a constant angle, like 45°.
- **Add Point Along Segment:** Adds points along selected segments at a specific position (time). Needs Vanilla.
- **Create Centerline:** Creates a centerline between two selected paths. The paths should have opposite directions. If it doesn’t work as expected, try reversing one of the paths. Needs Vanilla.
- **Duplicate Selected Nodes:** Creates a copy of the selected nodes and adds them in place.
- **Duplicate Selected Nodes with Offcurve Points:** Creates a copy of the selected nodes, adds them in place and create zero-length offcurve points in between.
- **Interpolate Path with Itself:** Interpolates the path with itself. The fixed half will be the one with the start point. This script will be improved in the near future.
- **Make Block Shadow:** Insert points on the tangents at a specific angle and extrude the path in the same direction, creating a block shadow effect. Needs Vanilla.
- **Make Next Node First:** Moves the start point of the selected  path(s) to the next oncurve node. Specially useful if assigned to a keyboard shortcut.
- **Make Previous Node First:** Moves the start point of the selected  path(s) to the previous oncurve node. Specially useful if assigned to a keyboard shortcut.
- **New Tab with Overlaps:** Opens a new Edit tab containing all glyphs that contain overlaps.
- **Open All Nodes:** Opens all nodes for the selected paths (or all paths if none are selected).
- **Open Selected Nodes:** Opens the selected nodes.
- **Re-interpolate:** Re-interpolates selected layers. Makes it possible to assign a keyboard shortcut to this command via Preferences > Shortcuts (in Glyphs 3) or System Preferences > Keyboard > Shortcuts > App Shortcuts (in Glyphs 2).
- **Remove Overlaps and Correct Path Directions in All Masters:** Removes overlaps (if so, copies the original to the background), corrects path directions in all layers and opens a new tab with glyphs that became incompatible. Reports in Macro Window.
- **Round Coordinates for Entire Font:** Round coordinates of all paths in the entire font.

## SVG Export and Import

### SVG Export.py

1) Before running the script, define which masters should be exported and their colors in JSON files and place them alongside your .glyphs file. Let’s call the following example `acquamarine.json`:

```json
{
	"Extrude": [ 15, 54, 69 ],
	"Regular": [ 1, 187, 226 ],
	"Bevel B": {
		"startPoint": [0,0],
		"endPoint": [0,550],
		"colors": [
			[ 168, 231, 244 ],
			[ 195, 241, 249 ]
		],
		"locations": [0,1]
	}
}
```

I believe the template above is quite self-explanatory. `Extrude`, `Regular` and `Bevel B` are names masters in our .glyphs file. Extrude and Regular have a solid fill, while Bevel B has a linear gradient fill. All trio of values represent RGB colors. You may add more colors as necessary. If you do so, remember to include additional “stops” in `locations`. Zero represents the start point of the gradient and 1 is the end point.

2) Run the script and type the name of the JSON file on the window. The script will create a subfolder with the same name and place all SVGs inside it.

### SVG Import.py

1) On a copy of your original .glyphs file, create a master for each one of the color schemes files you exported with the previous script. For example, if you have a subfolder called “acquamarine”, create a master named “Acquamarine” and assign to it a custom axis value. The name is case-insensitive.

2) After creating all masters, create an instance for each one of them so they will be exported. To do so, got o **Font Info** > **Instances** > **+** > **Add Instance for each Master**.

3) Run the script.

In a nutshell, for each master, it will check if there is a subfolder with the same name as the master, create a layer named *svg* and import the SVG file into it.


## Installing

### Glyphs 3

1. **Install the modules:** In *Window > Plugin Manager,* click on the *Modules* tab, and make sure at least the [Python](glyphsapp3://showplugin/python) and [Vanilla](glyphsapp3://showplugin/vanilla) modules are installed. If they were not installed before, restart the app.
2. **Install the scripts:** Go to *Window > Plugin Manager* and click on the *Scripts* tab. Scroll down to [Harbortype scripts](glyphsapp3://showplugin/harbortype%20scripts%20by%20Henrique%20Beier) and click on the *Install* button next to it.

Now the scripts are available in *Script > Harbortype.* If the Harbortype scripts do not show up in the *Script* menu, hold down the Option key and choose *Script > Reload Scripts* (⌘⌥⇧Y).

### Glyphs 2

Download or clone this repository and put it into the Scripts folder. To find this folder, go to Script > Open Scripts Folder (⌘⇧Y) in Glyphs. After placing the scripts there, hold down the Option key and go to Script > Reload Scripts (⌘⌥⇧Y). The scripts will now be visible in the Script menu.

Some scripts require Tal Leming’s Vanilla. To install it, go to the menu Glyphs > Preferences > Addons > Modules and click the Install Modules button.

## License

Copyright 2018 Henrique Beier (@harbortype). Some code samples by Rainer Erich Scheichelbauer (@mekkablue) and Luisa Leitenperger.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
