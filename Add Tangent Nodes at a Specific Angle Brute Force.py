#MenuTitle: Add Tangent Nodes at a Specific Angle by Brute Force
# -*- coding: utf-8 -*-
__doc__="""
Insert points on the tangents at a specific angle
"""

from collections import OrderedDict
import datetime

start = datetime.datetime.now()
print start

# Set the angle
angle = 135
# Calculates the opposite angle as well
secondAngle = angle + 180 if angle <= 90 else angle - 180
angles = [ angle, secondAngle ]

# Set the time step which will be used to check the tangents.
# On a path, time represents the position of a "sweep" between
# two oncurve nodes. Smaller values mean more precision,
# but also take more time to run. I get good results with 0.005.
timeStep = 0.005


font = Glyphs.font
layer = font.selectedLayers[0]

for path in layer.paths:

	# Creates a list of indexes of oncurve nodes.
	# Only oncurve nodes can be used to sweep a path using time. 
	onCurveNodes = []
	for node in path.nodes:
		if node.type != "offcurve":
			onCurveNodes.append( node.index )

	# Sweeps the whole path to find where the tangent angle matches 
	# the angles we're searching for. The points where the tangent angle 
	# match are stored in a dict. This is probably very, VERY inefficient 
	# but I don't know calculus :(
	tangentPoints = {}
	for nodeTime in onCurveNodes:
		endTime = nodeTime + 1
		while nodeTime < endTime:
			# Creates a temporary path so we don't mess with the original
			# until we find the correct point.
			tempPath = layer.paths[0].copy()
			# Creates a node in our fake path at the current time...
			nearestNode = tempPath.insertNodeWithPathTime_( nodeTime )
			# ... so we can get its tangent angle.
			tangentAngle = tempPath.tangentAngleAtNode_direction_(nearestNode, 1)
 			# If the tangent angle matches, store the current time in the dict 
 			# and skip this segment.
			if int(tangentAngle) in angles:
				tangentPoints[nodeTime] = nearestNode
				break
			nodeTime += timeStep
	
	# Now, creates an ordered dict from the results.
	# This dict is sorted by time from largest to smallest so we can 
	# simply insert the nodes, not worrying about their new indexes.
	orderedPoints = OrderedDict( sorted(tangentPoints.items(), reverse=True) )
	for time, point in orderedPoints.iteritems():
		# Insert the new nodes and profit!
		path.insertNodeWithPathTime_( time )

end = datetime.datetime.now()
print end
delta = end - start
print delta.microseconds
