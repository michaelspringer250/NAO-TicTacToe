import numpy as np
import cv2
import os
import copy
import statistics

#create a 2d array to hold the gamestate
gamestate = [["-","-","-"],["-","-","-"],["-","-","-"]]

MARGIN = 5

#kernel used for noise removal
kernel =  np.ones((7,7),np.uint8)
# Load a color image

img = cv2.resize(cv2.imread("C:/Users/mspri/Desktop/OC/image.jpg"), (640, 480), interpolation = cv2.INTER_AREA)


#print(img_width, img_height)

# turn into grayscale
img_g =  cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# turn into thresholded binary
ret,thresh1 = cv2.threshold(img_g,127,255,cv2.THRESH_BINARY)
#remove noise from binary
thresh1 = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)


#find and draw contours. RETR_EXTERNAL retrieves only the extreme outer contours
contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# find largest contour (outline of whole board) and second largest contour (border of the actual game)
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
print("Second largest contour index", cv2.boundingRect(contours[secondLargestContour]))

# Crop image to inside of second largest contour
x1, y1, w1, h1 = cv2.boundingRect(contours[secondLargestContour])
bwCropped = thresh1[y1+MARGIN:y1+h1-MARGIN,x1+MARGIN:x1+w1-MARGIN]
colorCroppped = img[y1+MARGIN:y1+h1-MARGIN,x1+MARGIN:x1+w1-MARGIN]

# Find contours in cropped image
contours, hierarchy = cv2.findContours(bwCropped, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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

# Clean out extra contours
while len(contours) > 9:
	# Find the furthest width from the median and the bounding rect of that width
	contours.sort(key=getWidth)
	medianWidth = getMedianWidth(contours)	
	furthestFromMedianWidth = 0
	furthestFromMedianWidthBoundingRect = 0
	for ct in contours:
		if abs(medianWidth - cv2.boundingRect(ct)[2]) > furthestFromMedianWidth:
			furthestFromMedianWidth = abs(medianWidth - cv2.boundingRect(ct)[2])
			furthestFromMedianWidthBoundingRect = cv2.boundingRect(ct)
	# Find the furthest height from the median and the bounding rect of that height
	contours.sort(key=getHeight)
	medianHeight = getMedianHeight(contours)
	furthestFromMedianHeight = 0
	furthestFromMedianHeightBoundingRect = 0
	for ct in contours:
		if abs(medianHeight - cv2.boundingRect(ct)[3]) > furthestFromMedianHeight:
			furthestFromMedianHeight = abs(medianHeight - cv2.boundingRect(ct)[3])
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
			print("Deleting",cv2.boundingRect(ct))
			contours.pop(i)
			print("New length",len(contours))
			break
		i = i + 1

for ct in contours:
	print(cv2.boundingRect(ct))

x = 1
y = 2
for ct in contours:
	cv2.drawContours(colorCroppped, [ct], -1, (255,0+x*10,0+y*11), 15)
	x = x + 1
	y = y + 1

#cv2.drawContours(colorCroppped, contours, -1, (0,255,0), 15)
cv2.imwrite("C:/Users/mspri/Desktop/OC/post.jpg", img)

# ======================================================
# ======================================================
# BELOW HERE HAS NOT BEEN UPDATED TO USE CROPPED IMAGE
# ======================================================
# ======================================================


# get the image width and height
img_width = img.shape[1]
img_height = img.shape[0]

# tileCount = 0
# #print(len(contours))
# for cnt in contours:
	# print('iteration')
	# # ignore small contours that are not tiles
	# if cv2.contourArea(cnt) > 20000:
		# tileCount = tileCount+1
		# # use boundingrect to get coordinates of tile
		# x,y,w,h = cv2.boundingRect(cnt)
		# #print(cv2.boundingRect(cnt))
		# # create new image from binary, for further analysis. Trim off the edge that has a line
		# tile = thresh1[y+MARGIN:y+h-MARGIN*2,x+MARGIN:x+w-MARGIN*2]
		# # create new image from main image, so we can draw the contours easily
		# imgTile = img[y+MARGIN:y+h-MARGIN*2,x+MARGIN:x+w-MARGIN*2]

		# #print(x, "  ", y)
		# #determine the array indexes of the tile
		# tileX = int(round(((x+40)/img_width)*3))
		# tileY = int(round(((y+40)/img_height)*3))
		# #print(tileX, "  ", tileY)

		# if tileX >= 0 and tileX < 3 and tileY >= 0 and tileY < 3:
			# # find contours in the tile image. RETR_TREE retrieves all of the contours and reconstructs a full hierarchy of nested contours.
			# c, hierarchy = cv2.findContours(tile, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
			# for ct in c:
				# print('inner iteration')
				# # to prevent the tile finding itself as contour
				# if cv2.contourArea(ct) < cv2.contourArea(cnt) - 14000:
					# #print(cv2.boundingRect(ct))
					# cv2.drawContours(imgTile, [ct], -1, (255,0+tileX*127,0+tileY*127), 15)
					# #calculate the solitity
					# area = cv2.contourArea(ct)
					# hull = cv2.convexHull(ct)
					# hull_area = cv2.contourArea(hull)
					# if(hull_area != 0):
						# solidity = float(area)/hull_area
					# else:
						# solidity = 1

					# # fill the gamestate with the right sign
					# if(solidity > 0.7):
				
						# gamestate[tileX][tileY] = "O"
					# else:
						# gamestate[tileX][tileY] = "X"
		# # put a number in the tile
		# cv2.putText(img, str(tileCount), (x+20,y+30), cv2.FONT_HERSHEY_SIMPLEX, 5, (0,0,255), 5)
# #print the gamestate
# print("Gamestate:")
# for line in gamestate:
	# linetxt = ""
	# for cel in line:
		# linetxt = linetxt + "|" + cel
	# print(linetxt)


#res = cv2.resize(img,None,fx=0.2, fy=0.2, interpolation = cv2.INTER_CUBIC)
#print(type(img))

# wasSuccessful = cv2.imwrite("C:/Users/mspri/Desktop/OC/post.jpg", img)
# print("%r" % wasSuccessful)