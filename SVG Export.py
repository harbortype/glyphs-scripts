#MenuTitle: SVG Export
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Export SVG files to a subfolder defined by the user. The script takes a JSON file as input. In the JSON file, define the layers which will be exported (from the bottom up) and its colors.
"""

from drawBot import *
import vanilla
import os
import re
import subprocess
import json
from collections import OrderedDict


class ExportSVG(object):


    def __init__(self):
        winWidth = 240
        winHeight = 110
        self.w = vanilla.Window(
            # Define the window size, title, min size, max size, 
            # and last position and size
            (winWidth,winHeight),
            "Export SVG",  # window title
            minSize = (winWidth,winHeight),
            maxSize = (winWidth,winHeight),
            autosaveName = "com.harbortype.ExportSvg.mainwindow"
            )
        self.w.text_1 = vanilla.TextBox(
            (15, 20, 100, 17),
            "Layer name:",
            sizeStyle = 'regular'
            )
        self.w.exportName = vanilla.EditText(
            (100, 18, 120, 22),
            "svg",
            sizeStyle = 'regular'
            )
        self.w.runButton = vanilla.Button(
            (-100, -35, -20, -15),
            "Export",
            sizeStyle = "regular",
            callback = self.main
            )
        self.w.setDefaultButton(self.w.runButton)
        
        # Load Settings:
        if not self.loadPreferences():
            print("Note: 'Export SVG' could not load preferences. Will resort to defaults")
        
        # Open window and focus on it:
        self.w.open()
        self.w.makeKey()


    def savePreferences(self, sender):
        try:
            Glyphs.defaults["com.harbortype.ExportSVG.exportName"] = self.w.exportName.get()
        except:
            return False
            
        return True


    def loadPreferences(self):
        try:
            NSUserDefaults.standardUserDefaults().registerDefaults_(
                {
                    "com.harbortype.ExportSVG.unicode": "svg"
                }
            )
            self.w.exportName.set(
                Glyphs.defaults["com.harbortype.ExportSVG.exportName"]
                )
        except:
            return False
            
        return True


    def readJSON(self, jsonFile):
        """    
        Reads an JSON file and return its contents as an OrderedDict
        
        Arguments:
            jsonFile {str} -- complete path for .json file
        Returns:
            OrderedDict
        """ 
        # jsonFile = os.path.join(filePath, fileName, '.json')
        try:
            with open(jsonFile) as data_file:    
                jsonData = json.load(data_file, object_pairs_hook=OrderedDict)
            return jsonData
        except:
            Glyphs.showMacroWindow()
            print('No JSON file exists at %s' % (jsonFile))


    def setColors(self, layerColors):
        """
        Gets a list or OrderedDict of colors, converts them to floatpoint 
        notation (from 0.0 to 1.0 instead of 0 to 255), and then declares the 
        fill or linearGradient funcions
        
        Arguments:
            layerColors {list or OrderedDict} -- coming from a JSON file
        """
        if type(layerColors) is list:
            # If layerColors is a list, it means it is a solid fill
            for i, value in enumerate(layerColors):
                # Convert each rgb value from 0-255 to 0.0-1.0 formats
                if type(value) is int and i <= 2:
                    # Only process if it hasn't already been processed 
                    # (not int) and is one of the first 3 values (rgb) 
                    layerColors[i] = value / 255
            # Convert the processed values into a tuple, 
            # then unpack it and set it as fill color
            fillColor = tuple(layerColors)
            fill(*fillColor)

        elif type(layerColors) is OrderedDict:
            # If layerColors is an OrderedDict, it means it is a gradient
            for i, stop in enumerate(layerColors['colors']):
                # For each color stop in the gradient
                for v, value in enumerate(stop):
                    # For each color value in the color stop
                    if type(value) is int and v <= 2:
                        # Only process if it hasn't already been processed 
                        # (not int) and is one of the first 3 values (rgb) 
                        layerColors['colors'][i][v] = value / 255
            # Convert the processed values into a list, then use them to 
            # define a linearGradient. We are explicitly declaring the 
            # arguments because Python 2 only allows to unpack the last 
            # tuple in an argument list.
            colors = list(layerColors['colors'])
            locations = layerColors['locations']
            linearGradient( 
                startPoint=layerColors['startPoint'],
                endPoint=layerColors['endPoint'],
                locations=locations,
                colors=colors
                )


    def regexSvg(self, svgPath):
        """
        Perform some color substitutions on the SVG file to make it 
        compatible with Adobe software, as they don't support rgba notation
        
        Arguments:
            svgPath {str} -- path of the SVG file
        """

        # Lê o conteúdo do arquivo svg e guarda em uma variável
        with open(svgPath) as f:
            svgFile = f.read()

        # Substitui rgba(000,000,000,1.0)
        # por       rgb(000,000,000)
        svgFile = re.sub(
            r'rgba\((\d{1,3}),(\d{1,3}),(\d{1,3}),1\.0\)', 
            r'rgb(\1,\2,\3)', 
            svgFile)
        
        # Substitui stop-color="rgba(000,000,000,0.0)"
        # por       stop-color="rgb(000,000,000)" stop-opacity="0.0"
        svgFile = re.sub(
            r'stop-color="rgba\((\d{1,3}),(\d{1,3}),(\d{1,3}),(0?\.\d+)\)"', 
            r'stop-color="rgb(\1,\2,\3)" stop-opacity="\4"', 
            svgFile)
        
        # Substitui fill="rgba(000,000,000,0.0)"
        # por       fill="rgb(000,000,000)" fill-opacity="0.0"
        svgFile = re.sub(
            r'fill="rgba\((\d{1,3}),(\d{1,3}),(\d{1,3}),(0?\.\d+)\)"',
            r'fill="rgb(\1,\2,\3)" fill-opacity="\4"', 
            svgFile)
        
        with open(svgPath, 'w') as f:
            f.write(svgFile)


    def main(self, sender):
        try:
            # Basic variables
            myFont = Glyphs.font
            upm = myFont.upm
            fontPath = os.path.dirname(myFont.filepath)
            exportName = self.w.exportName.get()
            outputFolderPath = os.path.join( fontPath, exportName )
            outputSubfolderPath = '_other'

            # Calls the readJSON function using the jsonPath and returns the 
            # jsonData as an OrderedDict. The JSON files contain the layer 
            # names and their colors.
            jsonPath = os.path.join(fontPath, exportName + '.json')
            jsonData = self.readJSON(jsonPath)
            # Gets the jsonData keys (the layer names) which will be used 
            # later on for iteration
            layerNames = list(jsonData.keys())
            
            # Creates an empty list and populates it with all glyph names.
            allGlyphNames = []
            for glyph in myFont.glyphs:
                allGlyphNames.append(glyph.name)
            # Creates an empty set and populates it with unique glyph names 
            # (case insensitive). Glyphs with duplicate names are then stored 
            # on a separate list, which will later be used to decide if any 
            # glyph should be stored at root or in a subfolder
            uniqueNames = set()
            glyphsToSubfolder = []
            for glyphName in allGlyphNames:
                # Checks if the glyph name is already in the uniqueNames set.
                # If positive, stores the glyph name on the other list
                if glyphName.lower() in uniqueNames:
                    glyphsToSubfolder.append(glyphName)
                # Stores the glyph name in the uniqueNames set
                uniqueNames.add(glyphName.lower())

            # Checks if there are glyph that should be stored on a subfolder. 
            # If true, checks if the subfolder exists or creates it.
            if len(glyphsToSubfolder) > 0 :
                nestDir = os.path.join(outputFolderPath, outputSubfolderPath)
                if not os.path.exists(nestDir):
                    os.makedirs(nestDir)

            # MAIN LOOP
            for glyph in myFont.glyphs:

                # Defines where the SVG will be stored
                if glyph.name in glyphsToSubfolder:
                    outputPath = nestDir
                else:
                    outputPath = outputFolderPath

                newDrawing()
                newPage(upm,upm)

                glyphName = glyph.name

                for i, layerName in enumerate(layerNames):
                    
                    for master in myFont.masters:
                        if master.name == layerName:
                            masterId = master.id
                            break
                    
                    layerColors = jsonData[layerName]
                    self.setColors(layerColors)
                    drawPath( glyph.layers[masterId].completeBezierPath )

                svgPath = os.path.join( outputPath, glyphName+'.svg' )
                saveImage(svgPath)
                self.regexSvg(svgPath)
            
            if not self.savePreferences(self):
                print("Note: 'Export SVG' could not write preferences.")

            self.w.close()

            print('Done!')

        except Exception as e:
            # brings macro window to front and reports error:
            Glyphs.showMacroWindow()
            print("Export SVG Error:\n%s" % e)

ExportSVG()
