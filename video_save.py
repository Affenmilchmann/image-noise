import cv2
import numpy as np
import glob
import os

def SaveVideo(output_file_name):
	img_array = []

	i = 0
	
	print("Collecting photos...")
	while (os.path.isfile("frames/" + str(i + 1) + ".png")):
		img = cv2.imread("frames/" + str(i) + ".png")
		height, width, layers = img.shape
		size = (width,height)
		img_array.append(img)
		i += 1

	print("Building video...")
	out = cv2.VideoWriter(output_file_name,cv2.VideoWriter_fourcc(*'DIVX'), 30, size)

	for i in range(len(img_array)):
		print(int(100 * i / len(img_array)))
		out.write(img_array[i])
	out.release()
	print("Ready")