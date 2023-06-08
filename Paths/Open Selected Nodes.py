# MenuTitle: Open Selected Nodes
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals
__doc__ = """
Opens the selected nodes. Originally written by Luisa Leitenperger.
"""

from GlyphsApp import Glyphs, GSPath, OFFCURVE

font = Glyphs.font
layer = font.selectedLayers[0]

try:
    layer.beginChanges()

    pathArray = []
    delArray = []

    for pathIndex, path in enumerate(layer.paths):

        # Make a list of selected nodes as long as they're not handles
        # (handles can't be split open)
        selectedNodes = []
        for node in path.nodes:
            if node.selected and node.type != OFFCURVE:
                selectedNodes.append(node)

        if len(selectedNodes) > 0:

            for nodeIndex, node in enumerate(selectedNodes):

                # Create a new path for each node on the list and
                # add copies of every node until the next selected node.
                newPath = GSPath()

                # IF PATH IS CLOSED
                if path.closed:

                    # If it's the last (or only) node on the list,
                    # copy every node until the end of the path then restart
                    # at the beginning of the path until it reaches the first
                    # node on the list.
                    if node == selectedNodes[-1]:

                        for newNode in path.nodes[node.index:]:
                            newPath.addNode_(newNode.copy())

                        # If the first node of the list is also the first node
                        # of the path, only that first node will be included,
                        # no need for loops.
                        if selectedNodes[0].index == 0:
                            newPath.addNode_(path.nodes[0].copy())

                        else:
                            for newNode in path.nodes[0:selectedNodes[0].index + 1]:
                                newPath.addNode_(newNode.copy())

                    else:
                        for newNode in path.nodes[node.index:selectedNodes[nodeIndex + 1].index + 1]:
                            newPath.addNode_(newNode.copy())

                # IF PATH IS OPEN
                else:

                    # Create a path for the first nodes
                    if nodeIndex == 0 and path.nodes[node.index].index > 0:
                        secondPath = GSPath()
                        for newNode in path.nodes[: node.index + 1]:
                            secondPath.addNode_(newNode.copy())
                        pathArray.append(secondPath)

                    # If the node is the last one selected,
                    # add all nodes until the end of the path
                    if node == selectedNodes[-1]:
                        for newNode in path.nodes[node.index:]:
                            newPath.addNode_(newNode.copy())

                    # Otherwise, add nodes until the next selected one
                    else:
                        for newNode in path.nodes[node.index:selectedNodes[nodeIndex + 1].index + 1]:
                            newPath.addNode_(newNode.copy())

                # An open path has to start with a line node
                newPath.nodes[0].type = "line"

                pathArray.append(newPath)

            # Flag path to be deleted if there are selected nodes on that path
            delArray.append(pathIndex)

    # Delete original paths so there are no duplicates
    for pathIndex in reversed(delArray):
        try:  # Glyphs 3
            del(layer.shapes[pathIndex])
        except:  # Glyphs 2
            del(layer.paths[pathIndex])

    # Append the open paths
    for path in pathArray:
        try:  # Glyphs 3
            layer.shapes.append(path)
        except:  # Glyphs 2
            layer.paths.append(path)

finally:
    layer.endChanges()
