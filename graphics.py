from noise import pnoise1, pnoise2, pnoise3
from threading import Thread
from math import ceil

from my_math import RayCastingPoint

import pygame

pygame.init()
naadia_image = pygame.image.load('naadia.jpg')

def GetNoise(x, y, z, scale, w, h, d, oc):
	return pnoise3(x * scale, 
				   y * scale, 
				   z * scale, 
				  
				  repeatx = int(w  * scale), 
				  repeaty = int(h * scale), 
				  repeatz = int(d  * scale), 
				  
				  octaves = oc, 
				  base = 1)

class Session:
	def __init__(self, width, height, scale = 1.0, noiseScale = 0.02, depth = 10000, step = 0.5, octaves = 1, distance = 100, out_frames = 0):
		self.screen = pygame.display.set_mode((int(width * scale * 2) + 50, int(height * scale * 2) + 50))
		self.isGoing = True
		
		self.WIDTH = width
		self.HEIGHT = height
		self.SCALE = scale
		self.NOISE_SCALE = noiseScale
		self.DEPTH = depth
		self.STEP = step
		self.DIST = distance
		self.OCTAVES = octaves
		
		self.z = 0
		self.frame_id = 0
		self.out_frames = out_frames
		
	def Events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("############################")
				print("Programm was closed by user.")
				print("############################")
				self.isGoing = False
				
		if (self.out_frames != 0 and self.frame_id >= self.out_frames):
			self.isGoing = False
	
	def DisplayInfo(self):
		if self.out_frames > 0:
			pygame.image.save(self.screen, "frames/" + str(self.frame_id) + ".png")
			self.frame_id += 1;
	
	def ThreadDraw(self, thrAmount):
		self.screen.fill((10, 0, 50))

		thrs = []
		for i in range(thrAmount):
			thrs.append(Thread(target=self.Draw, args=(self.z, self.WIDTH * int(i / thrAmount), self.WIDTH * int((i + 1) / thrAmount))))

		for i in range(thrAmount):
			thrs[i].start()
			thrs[i].join()

		pygame.display.flip()
		
		self.DisplayInfo()
		
		self.z = ((self.z + self.STEP) <= self.DEPTH) * (self.z + self.STEP)

	def Draw(self, z, W_begin, W_end):
		self.screen.blit(naadia_image, ((0, int(self.HEIGHT * self.SCALE)),(self.WIDTH, self.HEIGHT)))

		for x in range(W_begin, W_end):
			for y in range(self.HEIGHT):
				value = GetNoise(x, y, z, self.NOISE_SCALE, self.WIDTH, self.HEIGHT, self.DEPTH, self.OCTAVES)

				normalised_height = float(float(value + 1) / 2.0)

				poly = [[x, 	y - 1, GetNoise(x, 	   y - 1, z, self.NOISE_SCALE, self.WIDTH, self.HEIGHT, self.DEPTH, self.OCTAVES)], 
						[x + 1, y + 1, GetNoise(x + 1, y + 1, z, self.NOISE_SCALE, self.WIDTH, self.HEIGHT, self.DEPTH, self.OCTAVES)], 
						[x - 1, y + 1, GetNoise(x - 1, y + 1, z, self.NOISE_SCALE, self.WIDTH, self.HEIGHT, self.DEPTH, self.OCTAVES)]]

				coords = [x, 
						  y, 
						  normalised_height]


				#	DRAWING CURVED IMAGE
				image_point = RayCastingPoint(poly, coords, screen_height = self.DIST)

				if (image_point[0] < 0 or image_point[1] < 0 or image_point[0] >= int(self.WIDTH * self.SCALE) or image_point[1] >= int(self.HEIGHT * self.SCALE)):
					pygame.draw.rect(
						self.screen,
						(0, 0, 0),
						(
							(x, y),
							(ceil(self.SCALE), ceil(self.SCALE))
						)
					)
				else:
					pygame.draw.rect(
						self.screen,
						self.screen.get_at((image_point[0], image_point[1] + int(self.HEIGHT * self.SCALE))),
						(
							(ceil(x * self.SCALE), ceil(y * self.SCALE)),
							(ceil(self.SCALE), ceil(self.SCALE))
						)
					)

				#	DRAWING PERLIN
				pygame.draw.rect(
					self.screen, 
					(
						int(255 * normalised_height), 
						int(255 * normalised_height), 
						int(255 * normalised_height)
					),
					(
						(ceil((x + self.WIDTH) * self.SCALE), ceil(y * self.SCALE)),
						(ceil(self.SCALE), ceil(self.SCALE))
					)

				)