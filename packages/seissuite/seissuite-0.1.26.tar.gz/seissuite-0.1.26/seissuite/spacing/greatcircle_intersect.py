# -*- coding: utf-8 -*-
"""
Created on Tues Jun 23 16:32:27 2015

@author: boland

help for interesections function came from:
http://stackoverflow.com/questions/29465468\
python-intersection-point-of-two-great-circles-lat-long

CODE DESCRIPTION:
The following python script takes a set of four lat-lon coordinates and
returns which two points intersect the two great-circle lines between these
two stations. Note that two points are given as output, NOT the closest 
intersection to both stations. This could be determined in future. 
"""

import numpy as np
import math

# Define points in great circle 1
#p1_lat1 = 32.498520
#p1_long1 = -106.816846
#p1_lat2 = 38.199999
#p1_long2 = -102.371389

# Define points in great circle 2
#p2_lat1 = 34.086771
#p2_long1 = -107.313379
#p2_lat2 = 34.910553
#p2_long2 = -98.711786


def intersect_paths(coord1, coord2, coord3, coord4):
	"""
	Function that returns the two possible intersection
	lat-lon points between two great circle paths given
	there four initial coordinates!
	"""

	# Define points in great circle 1
	p1_long1 = coord1[0]
	p1_lat1 = coord1[1]
	p1_long2 = coord2[0]
	p1_lat2 = coord2[1]

	# Define points in great circle 2
	p2_long1 = coord3[0]
	p2_lat1 = coord3[1]
	p2_long2 = coord4[0]
	p2_lat2 = coord4[1]

	# Convert points in great circle 1, degrees to radians
	p1_lat1_rad = ((math.pi * p1_lat1) / 180.0)
	p1_long1_rad = ((math.pi * p1_long1) / 180.0)
	p1_lat2_rad = ((math.pi * p1_lat2) / 180.0)
	p1_long2_rad = ((math.pi * p1_long2) / 180.0)

	# Convert points in great circle 2, degrees to radians
	p2_lat1_rad = ((math.pi * p2_lat1) / 180.0)
	p2_long1_rad = ((math.pi * p2_long1) / 180.0)
	p2_lat2_rad = ((math.pi * p2_lat2) / 180.0)
	p2_long2_rad = ((math.pi * p2_long2) / 180.0)

	# Put in polar coordinates
	x1 = math.cos(p1_lat1_rad) * math.cos(p1_long1_rad)
	y1 = math.cos(p1_lat1_rad) * math.sin(p1_long1_rad)
	z1 = math.sin(p1_lat1_rad)
	x2 = math.cos(p1_lat2_rad) * math.cos(p1_long2_rad)
	y2 = math.cos(p1_lat2_rad) * math.sin(p1_long2_rad)
	z2 = math.sin(p1_lat2_rad)
	cx1 = math.cos(p2_lat1_rad) * math.cos(p2_long1_rad)
	cy1 = math.cos(p2_lat1_rad) * math.sin(p2_long1_rad)
	cz1 = math.sin(p2_lat1_rad)
	cx2 = math.cos(p2_lat2_rad) * math.cos(p2_long2_rad)
	cy2 = math.cos(p2_lat2_rad) * math.sin(p2_long2_rad)
	cz2 = math.sin(p2_lat2_rad)

	# Get normal to planes containing great circles
	# np.cross product of vector to each point from the origin
	N1 = np.cross([x1, y1, z1], [x2, y2, z2])
	N2 = np.cross([cx1, cy1, cz1], [cx2, cy2, cz2])

	# Find line of intersection between two planes
	L = np.cross(N1, N2)

	# Find two intersection points
	X1 = L / np.sqrt(L[0]**2 + L[1]**2 + L[2]**2)
	X2 = -X1
	i_lat1 = math.asin(X1[2]) * 180./np.pi
	i_long1 = math.atan2(X1[1], X1[0]) * 180./np.pi
	i_lat2 = math.asin(X2[2]) * 180./np.pi
	i_long2 = math.atan2(X2[1], X2[0]) * 180./np.pi
	
	int_coord1 = [i_lat1, i_long1]; int_coord2 = [i_lat2, i_long2]
	# Print results
	return [int_coord1, int_coord2]




