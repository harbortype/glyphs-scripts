# MenuTitle: Make Block Shadow
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Insert points on the tangents at a specific angle
"""

from Foundation import NSAffineTransform
import vanilla
import math
from GlyphsApp import Glyphs, GSPath, GSNode

font = Glyphs.font
Glyphs.clearLog()


class MakeBlockShadow(object):

    def __init__(self):

        windowWidth = 220
        windowHeight = 110
        self.w = vanilla.FloatingWindow(
            (windowWidth, windowHeight),
            "Make Block Shadow",
            autosaveName="com.harbortype.MakeBlockShadow.mainwindow"
        )

        self.w.text_1 = vanilla.TextBox((30, 16, 120, 17), "Angle:")
        self.w.angle = vanilla.EditText((100, 14, -30, 22), callback=self.SavePreferences)
        self.w.text_2 = vanilla.TextBox((30, 46, 120, 17), "Distance:")
        self.w.distance = vanilla.EditText((100, 44, -30, 22), callback=self.SavePreferences)
        self.w.button = vanilla.Button((30, -34, -30, 20), "Make Shadow", callback=self.Main)

        self.w.setDefaultButton(self.w.button)

        if not self.LoadPreferences():
            print("Note: 'Make Block Shadow' could not load preferences. Will resort to defaults.")

        self.w.open()
        self.w.makeKey()

    def SavePreferences(self, sender):
        try:
            Glyphs.defaults["com.harbortype.MakeBlockShadow.angle"] = self.w.angle.get()
            Glyphs.defaults["com.harbortype.MakeBlockShadow.distance"] = self.w.distance.get()
        except:
            return False

        return True

    def LoadPreferences(self):
        try:
            Glyphs.registerDefault("com.harbortype.MakeBlockShadow.angle", -45)
            Glyphs.registerDefault("com.harbortype.MakeBlockShadow.distance", 100)
            self.w.angle.set(Glyphs.defaults["com.harbortype.MakeBlockShadow.angle"])
            self.w.distance.set(Glyphs.defaults["com.harbortype.MakeBlockShadow.distance"])
        except:
            return False

        return True

    def RotatePath(self, path, angle):
        """Rotates a path by an angle in degrees"""
        transform = NSAffineTransform.transform()
        transform.rotateByDegrees_(angle)
        for node in path.nodes:
            node.position = transform.transformPoint_(node.position)

    def Main(self, sender):
        font.disableUpdateInterface()
        try:
            layers = font.selectedLayers
            angle = int(self.w.angle.get())
            distance = int(self.w.distance.get())

            for layer in layers:

                almostExtremes = []
                # Find the tangent nodes
                if angle % 90:  # if not a right angle

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
                            if Glyphs.versionNumber < 3.0:
                                for index, point in enumerate(segment):
                                    newNode = GSNode()
                                    newNode.position = point.x, point.y
                                    if index in [1, 2] and len(segment) == 4:
                                        newNode.type = "offcurve"
                                    elif index == 1 and len(segment) == 2:
                                        newNode.type = "line"
                                    else:
                                        newNode.type = "curve"
                                    originalSegment.addNode_(newNode)
                            else:
                                for index in range(segment.count()):
                                    newNode = GSNode()
                                    point = segment.pointAtIndex_(index)
                                    newNode.position = point.x, point.y
                                    if index in [1, 2] and segment.count() == 4:
                                        newNode.type = "offcurve"
                                    elif index == 1 and segment.count() == 2:
                                        newNode.type = "line"
                                    else:
                                        newNode.type = "curve"
                                    originalSegment.addNode_(newNode)
                            fakeSegment = originalSegment.copy()
                            fakeSegment.nodes[0].type = "line"

                            # Rotate the segment and add points to the extremes
                            self.RotatePath(fakeSegment, tangentAngle)
                            if Glyphs.versionNumber < 3.0:
                                fakeSegment.addExtremes_(True)
                            else:
                                fakeSegment.addExtremes_checkSelection_(True, False)

                            closestNode = None
                            middleTangent = 1

                            # If the segment has 7 nodes, an extreme point was added
                            if len(fakeSegment) == 7:
                                # Get the tangent angle of the middle node
                                middleNode = fakeSegment.nodes[3]
                                middleTangent = round(
                                    fakeSegment.tangentAngleAtNode_direction_(middleNode, 5)
                                )

                            elif len(fakeSegment) == 4:
                                boundsLowX = fakeSegment.bounds.origin.x
                                boundsHighX = boundsLowX + fakeSegment.bounds.size.width
                                nodeList = list(fakeSegment.nodes)
                                startNode = nodeList[0]
                                endNode = nodeList[-1]
                                errorMargin = 0.01

                                if boundsLowX < startNode.position.x - errorMargin:
                                    if boundsLowX < endNode.position.x - errorMargin:
                                        if startNode.position.x < endNode.position.x:
                                            closestNode = startNode
                                        else:
                                            closestNode = endNode
                                elif boundsHighX > startNode.position.x + errorMargin:
                                    if boundsHighX > endNode.position.x + errorMargin:
                                        if startNode.position.x > endNode.position.x:
                                            closestNode = startNode
                                        else:
                                            closestNode = endNode

                            # Rotate the segment back
                            self.RotatePath(fakeSegment, -tangentAngle)

                            if closestNode:
                                almostExtremes.append(closestNode.position)

                            # If the new diagonal extremes are perpendicular to our angle,
                            # restore the original segment
                            if middleTangent % 180 == 0:  # check if horizontal
                                fakeSegment = originalSegment

                            # Add the nodes to the new path, skipping the first node
                            # because the last and first ones repeat on adjacent segments
                            for node in fakeSegment.nodes[1:]:
                                newPath.addNode_(node)

                        # Close the path (if originally closed) and store it
                        newPath.closed = True if path.closed else False
                        newPaths.append(newPath)
                else:  # if right angle
                    newPaths = layer.paths

                # Iterate the new paths, which are stored separately
                # and were not appended to the layer yet
                for path in newPaths:

                    # Duplicate the tangent nodes (for extrusion)

                    # Get all oncurve nodes
                    onCurveNodes = [node for node in path.nodes if node.type != "offcurve"]

                    # Create a list for our "diagonal extremes"
                    diagonalExtremes = []

                    # Make the angle positive
                    tangentAngle = angle
                    while tangentAngle < 0:
                        tangentAngle += 360
                    # Get the angle value from 0° to 180°
                    tangentAngle = tangentAngle % 180

                    for node in onCurveNodes:
                        errorMargin = 1.5  # in degrees

                        if node.position in almostExtremes:
                            diagonalExtremes.append(node)

                        elif node.smooth:  # smooth node
                            # For smooth nodes, check if their tangent angles match ours.
                            # If true, adds the node to our list of diagonal extremes.
                            # An error margin is considered.
                            minTangentAngle = tangentAngle - errorMargin
                            maxTangentAngle = tangentAngle + errorMargin
                            nextNodeTan = round(path.tangentAngleAtNode_direction_(node, 1))
                            if nextNodeTan < 0:
                                nextNodeTan += 180
                            if nextNodeTan > minTangentAngle and nextNodeTan < maxTangentAngle:
                                diagonalExtremes.append(node)

                        else:  # corner node
                            # For non-smooth angles, check if our tangent falls outside
                            # the angle of the corner. If true, this means this particular
                            # node will produce a line when extruded.
                            nextNodeAngle = path.tangentAngleAtNode_direction_(node, 1)
                            prevNodeAngle = path.tangentAngleAtNode_direction_(node, -1)
                            # Subtract the tangent angle from the angles of the corner
                            # then uses sine to check if the angle falls below or above
                            # the horizontal axis. Only add the node if the angle is
                            # completely above or below the line.
                            nextNodeHorizontal = nextNodeAngle - tangentAngle
                            prevNodeHorizontal = prevNodeAngle - tangentAngle
                            if math.sin(math.radians(nextNodeHorizontal)) < 0:
                                if math.sin(math.radians(prevNodeHorizontal)) < 0:
                                    diagonalExtremes.append(node)
                            if math.sin(math.radians(nextNodeHorizontal)) > 0:
                                if math.sin(math.radians(prevNodeHorizontal)) > 0:
                                    diagonalExtremes.append(node)

                    # Duplicate the diagonal extremes and returns an updated list of nodes
                    duplicateExtremes = []
                    for node in diagonalExtremes:
                        newNode = GSNode()
                        newNode.type = "line"
                        newNode.smooth = False
                        newNode.position = node.position
                        node.smooth = False
                        path.insertNode_atIndex_(newNode, node.index + 1)
                        duplicateExtremes.append(newNode)
                    allExtremes = []
                    for i in range(len(diagonalExtremes)):
                        allExtremes.append(diagonalExtremes[i])
                        allExtremes.append(duplicateExtremes[i])

                    # Selects the diagonal extreme nodes
                    for node in diagonalExtremes:
                        layer.selection.append(node)

                    # Move the nodes
                    if distance != 0:

                        # Calculate the deltaX and deltaY
                        deltaX = math.cos(math.radians(angle)) * distance
                        deltaY = math.sin(math.radians(angle)) * distance

                        # # Build a list containing all duplicate nodes
                        # allExtremes = []
                        # for node in path.nodes:
                        #     if node.position == node.nextNode.position:
                        #         allExtremes.extend([node, node.nextNode])
                        # print(allExtremes)

                        # Check if the start point should move or not
                        fixedStartPoint = True
                        startNode = path.nodes[-1]
                        # If the start node is one of the diagonal extremes, use
                        # the angle we get after subtracting the tangentAngle from
                        # the secondNodeAngle to determine if the start should be fixed
                        # or not. It should move if it sits below the horizontal axis.
                        if startNode in allExtremes:
                            secondNodeAngle = path.tangentAngleAtNode_direction_(path.nodes[0], 1)
                            secondNodeHorizontal = secondNodeAngle - tangentAngle
                            if math.sin(math.radians(secondNodeHorizontal)) < 0:
                                fixedStartPoint = False
                        # If the start node is not a diagonal extreme, duplicate the
                        # path and move it by 1 unit in the direction of the extrusion.
                        else:
                            # Get the NSBezierPath and move it
                            offsetPath = path.bezierPath
                            translate = NSAffineTransform.transform()
                            translate.translateXBy_yBy_(
                                math.copysign(1, deltaX),
                                math.copysign(1, deltaY))
                            offsetPath.transformUsingAffineTransform_(translate)

                            startPoint = startNode.position
                            # On counterclockwise (filled) paths, the start node should
                            # move if the start node falls INSIDE the transformed path
                            if path.direction == -1:
                                if offsetPath.containsPoint_(startPoint):
                                    fixedStartPoint = False
                            # On clockwise paths, the start node should move if the
                            # start node falls OUTSIDE the transformed path
                            elif path.direction == 1:
                                if not offsetPath.containsPoint_(startPoint):
                                    fixedStartPoint = False

                        # If the start point should move, rearrange
                        # the list containing the diagonal extremes
                        if not fixedStartPoint:
                            if path.nodes[-1] not in diagonalExtremes:
                                if diagonalExtremes[-1].index > diagonalExtremes[0].index:
                                    lastNode = diagonalExtremes.pop(-1)
                                    diagonalExtremes.insert(0, lastNode)

                        # Only move if the number diagonal extremes is even
                        if len(diagonalExtremes) % 2 == 0:
                            n = 0
                            tupleList = []
                            for i in range(len(diagonalExtremes) // 2):
                                tupleList.append((diagonalExtremes[n], diagonalExtremes[n + 1]))
                                n += 2

                            for pair in tupleList:
                                if pair[0].index > pair[1].index:
                                    selection = path.nodes[pair[0].index + 1:]
                                    selection.extend(path.nodes[: pair[1].index + 1])
                                else:
                                    selection = path.nodes[pair[0].index + 1:pair[1].index + 1]

                                layer.selection = selection

                                # Finaly move a node
                                for node in layer.selection:
                                    pos = node.position
                                    pos.x = pos.x + deltaX
                                    pos.y = pos.y + deltaY
                                    node.position = pos
                        else:
                            print("Could not find all extremes for glyph", layer.parent.name)

                # Replace all paths with the new ones
                if newPaths:
                    if Glyphs.versionNumber < 3.0:
                        layer.paths = newPaths
                    else:
                        layer.shapes = newPaths
                    layer.roundCoordinates()
                    layer.selection = None

        except Exception as e:
            raise e

        finally:
            font.enableUpdateInterface()


MakeBlockShadow()
