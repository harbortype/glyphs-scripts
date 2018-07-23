#MenuTitle: Copy Master into Sublayer...
# -*- coding: utf-8 -*-
__doc__="""
Copies a specific master into a sublayer for the current master. Useful for creating COLR/CPAL color fonts.
"""

# ! Clean up vanilla interface

import vanilla

Glyphs.clearLog()
thisFont = Glyphs.font
currentMaster = thisFont.selectedFontMaster

class CopyMasterIntoSublayer( object ):

    def __init__( self ):
        # Set the default size for the window
        windowWidth  = 280
        windowHeight = 220
        windowWidthResize  = 120 # user can resize width by this value
        windowHeightResize = 0   # user can resize height by this value
        self.w = vanilla.FloatingWindow(
            ( windowWidth, windowHeight ), # default window size
            "Copy master into submaster", # window title
            minSize = ( windowWidth, windowHeight ), # minimum size (for resizing)
            maxSize = ( windowWidth + windowWidthResize, windowHeight + windowHeightResize ), # maximum size (for resizing)
            autosaveName = "com.harbortype.CopyMasterIntoSublayer.mainwindow" # stores last window position and size
        )

        self.w.text_1 = vanilla.TextBox((15, 12+2, 120, 14), "Copy paths from", sizeStyle='small')
        self.w.masterSource = vanilla.PopUpButton((120, 12+20, -15, 17), self.GetMasterNames(), sizeStyle='small', callback=None)

        self.w.text_2 = vanilla.TextBox((15, 56+2, 120, 14), "into this sublayer of selected master", sizeStyle='small')
        self.w.layerTarget = vanilla.EditText((120, 56+20, -15, 17), sizeStyle='small', callback=None)

        self.w.includePaths = vanilla.CheckBox((15+150+15, 100+2, 160, 20), "Include paths", sizeStyle='small', callback=self.SavePreferences, value=True)
        self.w.includeComponents = vanilla.CheckBox((15, 100+2, 160, 20), "Include components", sizeStyle='small', callback=self.SavePreferences, value=True)
        self.w.includeAnchors = vanilla.CheckBox((15, 100+20, -100, 20), "Include anchors", sizeStyle='small', callback=self.SavePreferences, value=True)
        
        self.w.copybutton = vanilla.Button((-80, -30, -15, -10), "Copy", sizeStyle='small', callback=self.CopyAll )
        self.w.setDefaultButton( self.w.copybutton )

        # Load Settings:
        if not self.LoadPreferences():
            print "Note: 'Copy Master into Sublayer' could not load preferences. Will resort to defaults."

        self.w.open()
        self.w.makeKey()

    def SavePreferences( self, sender ):
        try:
            Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.layerTarget"] = self.w.layerTarget.get()
            Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.includeComponents"] = self.w.includeComponents.get()
            Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.includeAnchors"] = self.w.includeAnchors.get()
        except:
            return False

        return True

    def LoadPreferences( self ):
        try:
            Glyphs.registerDefault("com.harbortype.CopyMasterIntoSublayer.includePaths", True)
            Glyphs.registerDefault("com.harbortype.CopyMasterIntoSublayer.includeComponents", True)
            Glyphs.registerDefault("com.harbortype.CopyMasterIntoSublayer.includeAnchors", True)
            self.w.includePaths.set( Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.includePaths"] )
            self.w.includeComponents.set( Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.includeComponents"] )
            self.w.includeAnchors.set( Glyphs.defaults["com.harbortype.CopyMasterIntoSublayer.includeAnchors"] )
        except:
            return False

        return True

    def GetMasterNames( self ):
        """Collects names of masters to populate the submenu in the GUI."""
        myMasterList = []
        for masterIndex in range( len( thisFont.masters ) ):
            thisMaster = thisFont.masters[masterIndex]
            myMasterList.append( '%i: %s' % (masterIndex, thisMaster.name) )
        return myMasterList

    def CheckIfSublayerExists( self, glyph, sublayer ):
        """Checks if there is a sublayer of the same name. 
        If it does, clear the layer. 
        If it doesn't, create the layer."""
        for layer in glyph.layers:
            # Find a layer with the name informed by the user and associated with the current master.
            # Effectively, this will loop through all layers in all masters and return only if the layer
            # is a child of the current master (associatedMasterId)
            if layer.name == sublayer and layer.associatedMasterId == currentMaster.id:
                print "Layer exists."
                return layer
        print sublayer, "does not exist."
        return None

    def ClearSublayer( self, sublayer ):
        """Clears all content from the current layer."""
        sublayer.paths = None
        sublayer.components = None
        sublayer.anchors = None
        sublayer.background = None

    def CreateEmptySublayer( self, sublayerName, glyph ):
        """Creates a new empty GSLayer object and appends it to the current glyph under the current master."""
        newLayer = GSLayer()
        newLayer.name = sublayerName
        newLayer.associatedMasterId = currentMaster.id
        glyph.layers.append(newLayer)

    def CopyAll( self, sender ):
        """Copies all data into the sublayer."""
        sublayerName = self.w.layerTarget.get()
        indexOfMasterSource = self.w.masterSource.get()
        # Gets the selected glyphs
        selectedGlyphs = [ x.parent for x in thisFont.selectedLayers ]
        print selectedGlyphs[0].layers[ indexOfMasterSource ]
        # For each selected glyph
        for glyph in selectedGlyphs:
            # Prepare sublayer
            sublayer = self.CheckIfSublayerExists( glyph, sublayerName )
            if sublayer:
                self.ClearSublayer( sublayer )
            else:
                self.CreateEmptySublayer( sublayerName, glyph )
                # Run the check again to select the newly created layer
                sublayer = self.CheckIfSublayerExists( glyph, sublayerName )
            # Copy paths and components
            sublayer.paths = glyph.layers[ indexOfMasterSource ].paths
            sublayer.components = glyph.layers[ indexOfMasterSource ].components
            # Copy anchors ?

CopyMasterIntoSublayer()
