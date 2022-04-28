import cv2
import numpy as np

# Read and process image
file_name = "grid_image.png"
img = cv2.imread("grid_image.png")
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
output = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, method=cv2.HOUGH_GRADIENT, dp=1.2, minDist=1000, minRadius=0, maxRadius=1000)
# ensure at least some circles were found
if circles is not None:
	# convert the (x, y) coordinates and radius of the circles to integers
	circles = np.round(circles[0, :]).astype("int")
	# loop over the (x, y) coordinates and radius of the circles
	for (x, y, r) in circles:
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	# show the output image
	cv2.imshow("output", np.hstack([img, output]))
	cv2.waitKey(0)