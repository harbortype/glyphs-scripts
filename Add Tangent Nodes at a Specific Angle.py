#MenuTitle: Add Tangent Nodes at a Specific Angle
# -*- coding: utf-8 -*-
__doc__="""
Insert points on the tangents at a specific angle
"""

from Foundation import NSAffineTransform
import vanilla, math

font = Glyphs.font
Glyphs.clearLog()


class AddTangentNodesAtAngle( object ):

    def __init__( self ):

        windowWidth = 260
        windowHeight = 190
        self.w = vanilla.FloatingWindow(
            ( windowWidth, windowHeight ),
            "Add tangent nodes at angle",
            minSize = ( windowWidth, windowHeight ),
            maxSize = ( windowWidth, windowHeight ),
            autosaveName = "com.harbortype.AddTangentNodesAtAngle.mainwindow"
        )

        self.w.text_1 = vanilla.TextBox( (30, 26, 120, 17), "Angle:" )
        self.w.angle = vanilla.EditText( (100, 24, -30, 22), callback=self.SavePreferences )
        self.w.text_2 = vanilla.TextBox( (30, 56, 120, 17), "Distance:" )
        self.w.distance = vanilla.EditText( (100, 54, -30, 22), callback=self.SavePreferences )
        self.w.duplicateNodes = vanilla.CheckBox( (30, 86, -30, 22), "Duplicate nodes on tangents",
            callback=self.SavePreferences, value=True)
        self.w.button = vanilla.Button( (30, -46, -30, 20), "Add Nodes", callback=self.Main )
        
        self.w.setDefaultButton( self.w.button )

        if not self.LoadPreferences():
            print "Note: 'Add Tangent Nodes at a Specific Angle' could not load preferences. Will resort to defaults."
        
        self.w.open()
        self.w.makeKey()


    def SavePreferences( self, sender ):
        try:
            Glyphs.defaults["com.harbortype.AddTangentNodesAtAngle.angle"] = self.w.angle.get()
            Glyphs.defaults["com.harbortype.AddTangentNodesAtAngle.distance"] = self.w.distance.get()
            Glyphs.defaults["com.harbortype.AddTangentNodesAtAngle.duplicateNodes"] = self.w.distance.get()
        except:
            return False

        return True


    def LoadPreferences( self ):
        try:
            Glyphs.registerDefault("com.harbortype.AddTangentNodesAtAngle.angle", 45)
            Glyphs.registerDefault("com.harbortype.AddTangentNodesAtAngle.distance", 0)
            Glyphs.registerDefault("com.harbortype.AddTangentNodesAtAngle.duplicateNodes", False)
            self.w.angle.set( Glyphs.defaults["com.harbortype.AddTangentNodesAtAngle.angle"] )
            self.w.distance.set( Glyphs.defaults["com.harbortype.AddTangentNodesAtAngle.distance"] )
            self.w.duplicateNodes.set( Glyphs.defaults["com.harbortype.AddTangentNodesAtAngle.duplicateNodes"] )
        except:
            return False

        return True


    def RotatePath( self, path, angle ):
        """Rotates a path by an angle in degrees"""
        transform = NSAffineTransform.transform()
        transform.rotateByDegrees_( angle )
        for node in path.points:
            node.position = transform.transformPoint_(
                NSMakePoint(node.x, node.y)
                )


    def Main( self, sender ):
        font.disableUpdateInterface()
        layers = font.selectedLayers
        angle = int(self.w.angle.get())
        distance = int(self.w.distance.get())
        duplicateNodes = self.w.duplicateNodes.get()
        
        for layer in layers:
            print layer.parent


            # Find the tangent nodes
            if angle % 90: # if not a right angle

                # Move the origin of the angle to a more natural position for this task
                tangentAngle = 90 - angle

                newPaths = []
                for path in layer.paths:
                    
                    # Create an empty path
                    newPath = GSPath()

                    for segment in path.segments:
                        # Create a path from the segment and duplicate it 
                        # so we can compare with the original later on
                        originalSegment = GSPath()
                        for point in segment.points:
                            newNode = path.nodes[ point.index ].copy()
                            originalSegment.addNode_( newNode )
                        fakeSegment = originalSegment.copy()
                        # Rotate the segment and add points to the extremes
                        self.RotatePath( fakeSegment, tangentAngle )        
                        # fakeSegment.addNodesAtExtremes()
                        fakeSegment.addExtremes_( True )
                        # Get the tangent angle of the middle node
                        middleNode = fakeSegment.nodes[3]
                        middleTangent = round( 
                            fakeSegment.tangentAngleAtNode_direction_( middleNode, 5 ) 
                            )
                        # Rotate the segment back
                        self.RotatePath( fakeSegment, -tangentAngle )
                        # If the new diagonal extremes are perpendicular to our angle,
                        # restore the original segment
                        if middleTangent % 180 == 0:
                            fakeSegment = originalSegment
                        # Add the nodes to the new path, skipping the first node 
                        # because the last and first ones repeat on adjacent segments
                        for node in fakeSegment.nodes[1:]:
                            newPath.addNode_( node )
                   
                    # Close the path (if originally closed) and store it
                    newPath.closed = True if path.closed else False
                    newPaths.append( newPath )
            else: # if right angle
                newPaths = layer.paths
            

            # Duplicate the tangent nodes (for extrusion)
            if duplicateNodes:

                # Iterate the new paths, which are stored separately 
                # and were not appended to the layer yet
                for path in newPaths:

                    # Get all oncurve nodes
                    onCurveNodes = [ node for node in path.nodes if node.type != "offcurve" ]

                    # Create a list for our "diagonal extremes"
                    diagonalExtremes = []

                    # Make the angle positive
                    tangentAngle = angle
                    while tangentAngle < 0:
                        tangentAngle += 360
                    # Get the angle value from 0° to 180°
                    tangentAngle = tangentAngle % 180

                    for node in onCurveNodes:
                        errorMargin = 1.5 # in degrees
                        
                        if node.smooth == True: # smooth node
                            # For smooth nodes, check if their tangent angles match ours. 
                            # If true, adds the node to our list of diagonal extremes.
                            # An error margin is considered.
                            minTangentAngle = tangentAngle - errorMargin
                            maxTangentAngle = tangentAngle + errorMargin
                            nextNodeTan = round( path.tangentAngleAtNode_direction_( node, 1 ) )
                            if nextNodeTan < 0:
                                nextNodeTan += 180
                            if nextNodeTan > minTangentAngle and nextNodeTan < maxTangentAngle:
                                diagonalExtremes.append( node )
                        
                        else: # corner node
                            # For non-smooth angles, check if our tangent falls outside 
                            # the angle of the corner. If true, this means this particular 
                            # node will produce a line when extruded.
                            nextNodeAngle = path.tangentAngleAtNode_direction_( node, 1 )
                            prevNodeAngle = path.tangentAngleAtNode_direction_( node, -1 )
                            # Subtract the tangent angle from the angles of the corner 
                            # then uses sine to check if the angle falls below or above 
                            # the horizontal axis. Only add the node if the angle is 
                            # completely above or below the line.
                            nextNodeHorizontal = nextNodeAngle - tangentAngle
                            prevNodeHorizontal = prevNodeAngle - tangentAngle
                            if math.sin( math.radians(nextNodeHorizontal) ) < 0:
                                if math.sin( math.radians(prevNodeHorizontal) ) < 0: 
                                    diagonalExtremes.append( node ) 
                            if math.sin( math.radians(nextNodeHorizontal) ) > 0:
                                if math.sin( math.radians(prevNodeHorizontal) ) > 0:
                                    diagonalExtremes.append( node )

                    # Duplicate the diagonal extremes and returns an updated list of nodes
                    duplicateExtremes = []
                    for node in diagonalExtremes:
                        newNode = GSNode()
                        newNode.type = "line"
                        newNode.smooth = False
                        newNode.position = node.position
                        node.smooth = False
                        path.insertNode_atIndex_( newNode, node.index+1 )
                        duplicateExtremes.append( newNode )
                    allExtremes = []
                    for i in range( len(diagonalExtremes) ):
                        allExtremes.append( diagonalExtremes[i] )
                        allExtremes.append( duplicateExtremes[i] )

                    # Selects the diagonal extreme nodes
                    for node in diagonalExtremes:
                        layer.selection.append( node )


            # Move the nodes
            if distance != 0:

                # Calculate the deltaX and deltaY
                deltaX = math.cos( math.radians(angle) ) * distance
                deltaY = math.sin( math.radians(angle) ) * distance

                # Create a copy of the layer and offset all paths by 1 unit.
                fakeLayer = layer.copy()
                offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
                offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( fakeLayer, 2, 2, False, False, 0.5, None, None )
                
                for p, path in enumerate(newPaths):
                    
                    # Check if the start point should move or not
                    
                    # Get the NSBezierPath and the NSPoint for the start node
                    offsetPath = fakeLayer.paths[p].bezierPath
                    print offsetPath
                    startPoint = path.nodes[-1].position
                    fixedStartPoint = True
                    # Move the NSBezierPath by deltaX and deltaY
                    translate = NSAffineTransform.transform()
                    translate.translateXBy_yBy_( 3, 3 )
                    offsetPath.transformUsingAffineTransform_( translate )
                    
                    # On counterclockwise (filled) paths, the start node should 
                    # move if the start node falls INSIDE the transformed path
                    if path.direction == -1:
                        if not offsetPath.containsPoint_( startPoint ):
                            fixedStartPoint = False
                    # On clockwise paths, the start node should move if the 
                    # start node falls OUTSIDE the transformed path
                    elif path.direction == 1:
                        if offsetPath.containsPoint_( startPoint ):
                            fixedStartPoint = False

                    print fixedStartPoint
                    
                    # If the start point should move, we need to rearrange 
                    # the list with our diagonal extremes
                    if fixedStartPoint == False:
                        print path.nodes[-1]
                        print diagonalExtremes
                        if path.nodes[-1] not in diagonalExtremes:
                            if diagonalExtremes[-1].index > diagonalExtremes[0].index:
                                lastNode = diagonalExtremes.pop(-1)
                                diagonalExtremes.insert( 0, lastNode )

                    n = 0
                    tupleList = []
                    for i in range( len(diagonalExtremes)/2 ):
                        tupleList.append( (diagonalExtremes[n], diagonalExtremes[n+1]) )
                        n += 2

                    for pair in tupleList:
                        if pair[0].index > pair[1].index:
                            selection = path.nodes[ pair[0].index +1 : ]
                            selection.extend( path.nodes[ : pair[1].index +1 ] )
                        else:
                            selection = path.nodes[ pair[0].index +1 : pair[1].index +1 ]

                        layer.selection = selection

                        # Finaly move a node
                        for node in layer.selection:
                            pos = node.position
                            pos.x = pos.x + deltaX
                            pos.y = pos.y + deltaY
                            node.position = pos


            # Replace all paths with the new ones
            if newPaths:
                layer.paths = newPaths
                layer.roundCoordinates()

        font.enableUpdateInterface()

AddTangentNodesAtAngle()
