# use this to create subset datasets based on crack type
# from the street and sidewalk dataset 
# (https://www.kaggle.com/datasets/augustineheng/pavement-image-datasets).

# Looks at the train set and the train set's labels for each image.

# Types of Cracks (0 - 6):
# alligator_crack : 0
# block_crack : 1
# longitudinal_crack : 2
# pothole : 3
# sealed_longitudinal_crack : 4
# sealed_transverse_crack : 5
# transverse_crack : 6

# IMAGE LABEL .txt file EXAMPLE:
'''
005_png.rf.c1d49e5779519d7a351ec618fd1c3c85.txt (label file name)

6 0.31293750000000004 0.2638888888888889 0.325640625 0.17592592592592593
6 0.3193645833333333 0.8032407407407407 0.5491927083333333 0.23148148148148148
2 0.7255468749999999 0.6053240740740741 0.48655208333333333 0.7893518518518519
2 0.8407447916666667 0.35532407407407407 0.31851041666666663 0.3449074074074074
'''
# This means 005_png.rf.c1d49e5779519d7a351ec618fd1c3c85.jpg in the train dataset
# has 4 cracks identified. 2 of them are transverse cracks and 2 of them are
# longitudinal cracks.
# their 

'''
6 0.49963541666666667 0.3229166666666667 0.9357708333333333 0.12268518518518519
	Float vals relative to width and height of image

6 is crack type
0.49963541666666667 is x coordinate value at the center of rectangle
0.9357708333333333 is y coordinate value at the center of rectangle
0.9357708333333333 is width of rect, rel to width of whole image
0.12268518518518519 is height of rect, rel to height of whole image
'''


import cv2 # opencv-python
		   # pip3 install opencv-python
import os
import shutil # allow recursively delete old sub-datasets
			  # will add append later
import random as r



# test1.jpg
# 005_png.rf.c1d49e5779519d7a351ec618fd1c3c85.jpg
# 005_png.rf.c1d49e5779519d7a351ec618fd1c3c85.jpg

def main():
	crackTypes = {
		0 : "alligator_crack",
		1 : "block_crack",
		2 : "longitudinal_crack",
		3 : "pothole",
		4 : "sealed_longitudinal_crack",
		5 : "sealed_transverse_crack",
		6 : "transverse_crack"
	}


	trainImagesPath = "streetDataset/train/images"
	# make directories for each type of crack
	for i in range(0, 7):
		path = "streetDataset/train/" + crackTypes[i] + "s_dataset"
		if os.path.exists(path): # remove old crackType datasets (so no dup imgs)
			shutil.rmtree(path)
		os.makedirs(path)

	crackTypeCounter = [0, 0, 0, 0, 0, 0, 0]

	# buffers
	widthBuffer = input("Enter width buffer (0 if none): ")
	heightBuffer = input("Enter height buffer (0 if none): ")
	

	'''
	widthBuffer = r.randint(0, 250)
	heightBuffer = r.randint(0, 250)
	'''


	# for each image
	for imgFileName in os.listdir(trainImagesPath):
		print(f"imgFileName: {imgFileName}")
		img = cv2.imread(trainImagesPath + "/" + imgFileName)
		cv2.imshow(imgFileName, img)
		cv2.moveWindow(imgFileName, 400, 0)
		imgHeight, imgWidth, _ = img.shape

		labelFilePath = "streetDataset/train/labels/" + imgFileName[:-3] + "txt" # replace last 3 chars with txt
		file = open(labelFilePath, 'r')

		# for each line in this img's label file
		for line in file:
			# 6 0.49963541666666667 0.3229166666666667 0.9357708333333333 0.12268518518518519
			split = line.split()
			crackType, x_center, y_center, w, h = int(split[0]), float(split[1]), \
									float(split[2]), float(split[3]), float(split[4])

			
			x_center = round(x_center * imgWidth)
			y_center = round(y_center * imgHeight)
			w = round(w * imgWidth) + int(widthBuffer)
			h = round(h * imgHeight) + int(heightBuffer)
			x = x_center - w / 2
			y = y_center - h / 2

			# check if x or y is negative, due to the buffer
			if x < 0:
				x = 0

			if y < 0:
				y = 0

			x = round(x)
			y = round(y)

			imgCrop = img[y:y + h, x:x + w]

			#cv2.imshow(crackTypes[crackType], imgCrop)

			# save cropped image to the correct crack type dataset
			saveCropPath = "streetDataset/train/" + crackTypes[crackType] + \
								"s_dataset/" +  str(crackTypeCounter[crackType]) + ".jpg"
			cv2.imwrite(saveCropPath, imgCrop)
			crackTypeCounter[crackType] += 1

			#cv2.waitKey(500)
			#cv2.destroyWindow(crackTypes[crackType])
		#cv2.destroyAllWindows()



if __name__ == '__main__':
	main()
















