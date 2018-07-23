#MenuTitle: Open Selected Nodes
# -*- coding: utf-8 -*-
__doc__="""
Opens selected nodes.
"""

import GlyphsApp

Glyphs.clearLog()

font = Glyphs.font
layer = font.selectedLayers[0]

# "Call this before you do bigger changes to the Layer. This will increase performance and prevent undo problems. Always call layer.endChanges() if you are finished."
layer.beginChanges()

pathArray = [] 
delArray = []

for pathIndex, path in enumerate(layer.paths):
    
    # makes a list of selected nodes as long as they're not handles (handles can't be split open)
    selectedNodeList = []
    for node in path.nodes:
        if (node.selected == True) and (node.type != "offcurve"):
            selectedNodeList.append(node)
    print selectedNodeList
    
    if len(selectedNodeList) >= 1:
        listCounter = 0

        for selectedNode in selectedNodeList:

            # will create a new path for each node on the list and add to it copies of every node until the next selected node.
            newPath = GSPath()
            
            # if it's the last (or only) node on the list, will copy every node until the end of the path, then restart at the beginning of the path until it reaches the first node on the list. 
            if selectedNode == selectedNodeList[-1]:
                
                for newNode in path.nodes[ selectedNode.index : ]:
                    newPath.addNode_(newNode.copy())

                # if the first node of the list is also the first node of the path, only that first node will be included, no need for loops.
                if selectedNodeList[0].index == 0:
                    newPath.addNode_(path.nodes[0].copy())

                elif selectedNodeList[0].index != 0:
                    for newNode in path.nodes[ 0 : selectedNodeList[0].index + 1 ]:
                        newPath.addNode_(newNode.copy())

            else:
                for newNode in path.nodes[ selectedNode.index : selectedNodeList[listCounter + 1].index + 1 ]:
                    newPath.addNode_(newNode.copy())

            # an open path has to start with a line node
            newPath.nodes[0].type = "line"

            listCounter += 1
            pathArray.append(newPath)
        
        # will only add a path to be deleted if there are selected nodes on that path
        delArray.append(pathIndex)

# deletes original paths so there are no duplicates
for pathIndex in delArray:
    del(layer.paths[pathIndex])

# draws new open paths
for path in pathArray:
    layer.paths.append(path)

layer.endChanges()