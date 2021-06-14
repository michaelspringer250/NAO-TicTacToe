import numpy as np
import cv2
import os
import copy
import statistics

# Helper function to get width of bounding rect of a contour


def getWidth(val):
	return cv2.boundingRect(val)[2]

# Helper function to get height of bounding rect of a contour


def getHeight(val):
	return cv2.boundingRect(val)[3]

# Given a list of contours sorted by width, find the median width


def getMedianWidth(conts):
	length = len(conts)
	if length % 2 == 1:
		return cv2.boundingRect(conts[length//2])[2]
	else:
		return ((cv2.boundingRect(conts[length//2])[2] + cv2.boundingRect(conts[length//2 - 1])[2]) / 2)

# Given a list of contours sorted by height, find the median height


def getMedianHeight(conts):
	length = len(conts)
	if length % 2 == 1:
		return cv2.boundingRect(conts[length//2])[3]
	else:
		return ((cv2.boundingRect(conts[length//2])[3] + cv2.boundingRect(conts[length//2 - 1])[3]) / 2)


# create a 2d array to hold the gamestate
gamestate = [["-", "-", "-"], ["-", "-", "-"], ["-", "-", "-"]]

MARGIN = 5
numBoardTiles = 9

# kernel used for noise removal
kernel = np.ones((7, 7), np.uint8)
# Load a color image

IM_DIR = "C:/Users/LaneSimpson/Documents/GitHub/oc-Master/NAO-TicTacToe/behavior_1/"
IM_NAME = "image2.jpg"
img = cv2.resize(cv2.imread(IM_DIR + IM_NAME),
				 (640, 480), interpolation=cv2.INTER_AREA)


# print(img_width, img_height)

# turn into grayscale
img_g = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# turn into thresholded binary
_, thresh1 = cv2.threshold(img_g, 127, 255, cv2.THRESH_BINARY)
# remove noise from binary
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)


# find and draw contours.
# RETR_EXTERNAL retrieves only the extreme outer contours
# RETR_LIST retrieves all contours
contours, hierarchy = cv2.findContours(
	thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# find largest contour (outline of whole picture) and second largest contour (border of the actual game)
largestArea = 0
secondLargestArea = -1
largestContour = 0
secondLargestContour = 0
i = 0
for ct in contours:
	print(cv2.boundingRect(ct))
	area = cv2.contourArea(ct)
	# print("Second largest contour", secondLargestContour)
	if area > secondLargestArea:
		if area > largestArea:
			secondLargestArea = largestArea
			secondLargestContour = largestContour
			largestArea = cv2.contourArea(ct)
			largestContour = i
		else:
			secondLargestArea = cv2.contourArea(ct)
			secondLargestContour = i
	i = i + 1

print("Largest contour index", cv2.boundingRect(contours[largestContour]))
print("Second largest contour index",
	  cv2.boundingRect(contours[secondLargestContour]))

# Crop image to inside of second largest contour
x1, y1, w1, h1 = cv2.boundingRect(contours[secondLargestContour])
bwCropped = thresh1[y1+MARGIN:y1+h1-MARGIN, x1+MARGIN:x1+w1-MARGIN]
colorCroppped = img[y1+MARGIN:y1+h1-MARGIN, x1+MARGIN:x1+w1-MARGIN]

# Find contours in cropped image
contours, hierarchy = cv2.findContours(
	bwCropped, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Clean out extra contours
while len(contours) > numBoardTiles:
	# Find the furthest width from the median and the bounding rect of that width
	contours.sort(key=getWidth)
	medianWidth = getMedianWidth(contours)
	furthestFromMedianWidth = 0
	furthestFromMedianWidthBoundingRect = 0
	for ct in contours:
		tempWidth = abs(medianWidth - getWidth(ct))
		if tempWidth > furthestFromMedianWidth:
			furthestFromMedianWidth = tempWidth
			furthestFromMedianWidthBoundingRect = cv2.boundingRect(ct)
	# Find the furthest height from the median and the bounding rect of that height
	contours.sort(key=getHeight)
	medianHeight = getMedianHeight(contours)
	furthestFromMedianHeight = 0
	furthestFromMedianHeightBoundingRect = 0
	for ct in contours:
		tempHeight = abs(medianHeight - getHeight(ct))
		if tempHeight > furthestFromMedianHeight:
			furthestFromMedianHeight = tempHeight
			furthestFromMedianHeightBoundingRect = cv2.boundingRect(ct)
	# Take the larger difference between the width and height and delete the associated contour
	boundingRectToDelete = 0
	if furthestFromMedianWidth > furthestFromMedianHeight:
		boundingRectToDelete = furthestFromMedianWidthBoundingRect
	else:
		boundingRectToDelete = furthestFromMedianHeightBoundingRect
	i = 0
	for ct in contours:
		if cv2.boundingRect(ct) == boundingRectToDelete:
			print("Deleting", cv2.boundingRect(ct))
			contours.pop(i)
			print("New length", len(contours))
		else:
			i = i + 1

for ct in contours:
	print(cv2.boundingRect(ct))

x = 1
y = 2
for ct in contours:
	cv2.drawContours(colorCroppped, [ct], -1, (255, 0+x*10, 0+y*11), 15)
	x = x + 1
	y = y + 1

cv2.imwrite(IM_DIR + "outers.jpg", img)

# ======================================================
# ======================================================
# BELOW HERE HAS NOT BEEN UPDATED TO USE CROPPED IMAGE
# ======================================================
# ======================================================


# get the image width and height
img_width = colorCroppped.shape[1]
img_height = colorCroppped.shape[0]
imgCopy = cv2.resize(cv2.imread(IM_DIR + IM_NAME),
				 (640, 480), interpolation=cv2.INTER_AREA)
imgCopyCropped = imgCopy[y1+MARGIN:y1+h1-MARGIN, x1+MARGIN:x1+w1-MARGIN]

tileCount = 0
print("finding symbols in tiles")
for cnt in contours:
	print('iteration')
	tileCount = tileCount+1
	# use boundingrect to get coordinates of tile
	x,y,w,h = cv2.boundingRect(cnt)
	tileArea = cv2.contourArea(cnt)
	# create new image from binary, for further analysis. Trim off the edge that has a line
	tile = bwCropped[y+MARGIN:y+h-MARGIN,x+MARGIN:x+w-MARGIN]
	# create new image from main image, so we can draw the contours easily
	imgTile = colorCroppped[y+MARGIN:y+h-MARGIN,x+MARGIN:x+w-MARGIN]

	#determine the array indexes of the tile
	tileX = int(round(((x+40)/img_width)*3))
	tileY = int(round(((y+40)/img_height)*3))
	# print(x, "  ", y)
	# print(tileX, "  ", tileY)

	if tileX >= 0 and tileX < 3 and tileY >= 0 and tileY < 3:
		# find contours in the tile image. RETR_TREE retrieves all of the contours and reconstructs a full hierarchy of nested contours.
		c, hierarchy = cv2.findContours(tile, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
		for ct in c:
			# to prevent the tile finding itself as contour
			if cv2.contourArea(ct) < tileArea * 0.90:
				imgCopyTile = imgCopyCropped[y+MARGIN:y+h-MARGIN,x+MARGIN:x+w-MARGIN]
				number_of_white_pix = np.sum(tile == 255)
				number_of_black_pix = np.sum(tile == 0)
				print(tileX, tileY)
				print('Number of white pixels:', number_of_white_pix)
				print('Number of black pixels:', number_of_black_pix)
				# the area needs to be at least 5% black in order to be legit
				if (number_of_black_pix/number_of_white_pix > 0.05):
					cv2.drawContours(imgCopyTile, [ct], -1, (255,0+tileX*127,0+tileY*127), 15)
					#calculate the solitity
					area = cv2.contourArea(ct)
					hull = cv2.convexHull(ct)
					hull_area = cv2.contourArea(hull)
					if(hull_area != 0):
						solidity = float(area)/hull_area
					else:
						solidity = 1

					# fill the gamestate with the right sign
					if(solidity > 0.7):

						gamestate[tileX][tileY] = "O"
					else:
						gamestate[tileX][tileY] = "X"
	else:
		print("tile out of bounds:", tileX, tileY)
#print the gamestate
print("Gamestate:")
for line in gamestate:
	linetxt = ""
	for cel in line:
		linetxt = linetxt + "|" + cel
	print(linetxt)

cv2.imwrite(IM_DIR + "inners.jpg", imgCopy)
