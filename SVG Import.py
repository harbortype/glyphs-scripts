#MenuTitle: SVG Import
# -*- coding: utf-8 -*-
__doc__="""
Import SVG files to the 'svg' layer on each glyph. Place the SVG files in a subfolder with the name of your master. If more than one master is present, it will search for each one of them.
"""

import GlyphsApp, os

# Glyphs.clearLog()
Glyphs.showMacroWindow()

# Basic variables
myFont = Glyphs.font
upm = myFont.upm

# Default folder is the current folder
currentDir = os.path.dirname( myFont.filepath )


def findFolder(currentMaster):
    """
    Reads the name of the current master and checks if there is a subfolder 
    with the same name (relative to the frontmost .glyphs file). 
    The comparison is case insensitive.
    
    Arguments:
        currentMaster {str} -- GSMaster object

    Returns: valid subfolder path
    """
    masterName = currentMaster.name
    potentialSubfolder = os.path.join( currentDir, masterName )

    if os.path.isdir( potentialSubfolder ):
        return potentialSubfolder
    else:
        return None


def findSvgLayer(layers,masterId):
    """
    Finds the 'svg' layer associated with a specific master ID
    
    Arguments:
        layers {arr} -- array of GSLayers of a glyph
        masterId {str} -- unique ID of master

    Returns: layer object
    """
    for layer in layers:
        # Find the svg layer associated with the current master
        if layer.name == 'svg' and layer.associatedMasterId == masterId:
            return layer
    return None


myFont.disableUpdateInterface()

for master in myFont.masters:
    # Start main loop
    # For each master, assign the findFolder result to the svgFolder variable
    # and store its ID on masterId
    svgFolder = findFolder(master)
    masterId = master.id

    if svgFolder:
        # If path exists, creates an empty dictionary which will be used to
        # store glyph names and svg paths
        glyphNamesDict = {}

        for root, dirs, files in os.walk( svgFolder ):
            # Filter the files list, keeping svg files only
            files = [ fi for fi in files if fi.endswith(".svg") ]

            for fileName in files:
                # For each file in dir, store the glyph name and the 
                # complete svg path in the dictionaty
                glyphName = fileName[:-4]
                glyphNamesDict[glyphName] = os.path.join( root.lower(), fileName )

        # The dictionary is complete now.
        # Let's start adding the svg files to the font

        for glyphName, svgPath in glyphNamesDict.iteritems():
            # We iterate svg files instead of glyphs in the font 
            # because it is more likely to exist fewer svgs than glyphs
            g = myFont.glyphs[glyphName]

            if g:
                # If a glyph exists with the same name as the svg,
                # reset the svgLayer variable
                svgLayer = None
                svgLayer = findSvgLayer( g.layers, masterId )
                if svgLayer:
                    # Clears the svg layer if it exists and is a
                    # child of the current master
                    svgLayer.backgroundImage = None
                    svgLayer.paths = None
                    svgLayer.anchors = None
                else:
                    # If the svg layer does not exists, create it
                    newLayer = GSLayer()
                    newLayer.name = 'svg'
                    newLayer.associatedMasterId = masterId
                    g.layers.append(newLayer)
                    # Run the function to find the svg layer again so we can 
                    # select the freshly created layer
                    svgLayer = findSvgLayer( g.layers, masterId )

                # Add the image to the svg layer
                newImage = GSBackgroundImage.alloc().initWithPath_(svgPath)
                svgLayer.setBackgroundImage_( newImage )

myFont.enableUpdateInterface()
