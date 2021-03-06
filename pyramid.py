"""
Helper functions to construct image pyramids
"""

import cv2
import numpy as np


# Function to downsample an intensity (grayscale) image
def downsampleGray(img):
	"""
	The downsampling strategy eventually chosen is a naive block averaging method.
	That is, for each pixel in the target image, we choose a block comprising 4 neighbors
	in the source image, and simply average their intensities. For each target image point 
	(y, x), where x indexes the width and y indexes the height dimensions, we consider the 
	following four neighbors: (2*y,2*x), (2*y+1,2*x), (2*y,2*x+1), (2*y+1,2*x+1).
	NOTE: The image must be float, to begin with.
	"""

	# Perform block-averaging
	img_new = (img[0::2,0::2] + img[0::2,1::2] + img[1::2,0::2] + img[1::2,1::2]) / 4.

	return img_new


# Function to downsample a depth image
def downsampleDepth(img):
	"""
	For depth images, the downsampling strategy is very similar to that for intensity images, 
	with a minor mod: we do not average all pixels; rather, we average only pixels with non-zero 
	depth values.
	"""

	# Perform block-averaging, but not across depth boundaries. (i.e., compute average only 
	# over non-zero elements)
	img_ = np.stack([img[0::2,0::2], img[0::2,1::2], img[1::2,0::2], img[1::2,1::2]], axis=2)
	num_nonzero = np.count_nonzero(img_, axis=2)
	num_nonzero[np.where(num_nonzero == 0)] = 1
	img_new = np.sum(img_, axis=2) / num_nonzero

	return img_new.astype(np.uint8)


# Function to construct a pyramid of intensity and depth images with a specified number of levels
def buildPyramid(gray, depth, num_levels, focal_length, cx, cy):

	# Lists to store each level of a pyramid
	pyramid_gray = []
	pyramid_depth = []
	pyramid_intrinsics = []

	current_gray = gray
	current_depth = depth
	current_f = focal_length
	current_cx = cx
	current_cy = cy

	# Build levels of the pyramid
	for level in range(num_levels):
		pyramid_gray.append(current_gray)
		pyramid_depth.append(current_depth)
		K_cur = dict()
		K_cur['f'] = current_f
		K_cur['cx'] = current_cx
		K_cur['cy'] = current_cy
		pyramid_intrinsics.append(K_cur)
		if level < num_levels-1:
			current_gray = downsampleGray(current_gray)
			current_depth = downsampleDepth(current_depth)

	return pyramid_gray, pyramid_depth, pyramid_intrinsics
