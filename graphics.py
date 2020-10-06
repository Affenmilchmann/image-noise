from noise import pnoise1, pnoise2, pnoise3
from threading import Thread
from math import ceil

from my_math import RayCastingPoint

import pygame

pygame.init()

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
	def __init__(self, width, height, scale = 1.0, noiseScale = 0.02, depth = 10000, step = 0.5, octaves = 1, distance = 100, out_frames = 0, image_path = "naadia.jpg"):
		self.image = pygame.image.load(image_path)
		print("Image size:", self.image.get_rect().size)
		
		self.width = self.image.get_rect().size[0]
		self.height = self.image.get_rect().size[0]
		self.scale = scale
		
		self.screen = pygame.display.set_mode((max(int(self.width * self.scale * 2), self.width), int(self.height * self.scale + self.height)))
		self.isGoing = True
		
		self.noise_scale = noiseScale
		self.depth = depth
		self.step = step
		self.dist = distance
		self.octaves = octaves
		
		self.z = 0
		self.frame_id = 0
		self.out_frames = out_frames
		
	def Events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				print("############################")
				print("Programm was closed by user.")
				print("############################")
				pygame.display.quit()
				self.isGoing = False
				
		if (self.out_frames != 0 and self.frame_id >= self.out_frames):
			self.isGoing = False
	
	def DisplayInfo(self):
		if self.out_frames > 0:
			pygame.image.save(self.screen, "frames/" + str(self.frame_id) + ".png")
			self.frame_id += 1;
	
	def ThreadDraw(self, thrAmount):
		self.screen.fill((10, 0, 50))

		#thrs = []
		#for i in range(thrAmount):
		#	thrs.append(Thread(target=self.Draw, args=(self.z, int(self.scale * self.width * i / thrAmount), int(self.scale * self.width * (i + 1) / thrAmount))))

		#for i in range(thrAmount):
		#	thrs[i].start()
		#	thrs[i].join()
		
		self.Draw(self.z, int(self.width * self.scale), int(self.height * self.scale))
			
		pygame.display.flip()
		
		self.DisplayInfo()
		
		self.z = ((self.z + self.step) <= self.depth) * (self.z + self.step)

	def Draw(self, z, W, H):
		self.screen.blit(self.image, ((0, int(self.height * self.scale)),(self.width, self.height)))

		for i_x in range(W):
			for i_y in range(H):
				#rescaling currend curved image point to the actual image size
				x = round(i_x / self.scale)
				y = round(i_y / self.scale)
				
				value = GetNoise(x, y, z, self.noise_scale, self.width, self.height, self.depth, self.octaves)

				normalised_height = float(float(value + 1) / 2.0)

				poly = [[x, 	y - 1, GetNoise(x, 	   y - 1, z, self.noise_scale, self.width, self.height, self.depth, self.octaves)], 
						[x + 1, y + 1, GetNoise(x + 1, y + 1, z, self.noise_scale, self.width, self.height, self.depth, self.octaves)], 
						[x - 1, y + 1, GetNoise(x - 1, y + 1, z, self.noise_scale, self.width, self.height, self.depth, self.octaves)]]

				coords = [x, 
						  y, 
						  normalised_height]


				#	DRAWING CURVED IMAGE
				image_point = RayCastingPoint(poly, coords, screen_height = self.dist)

				if (image_point[0] < 0 or image_point[1] < 0 or image_point[0] >= int(self.width) or image_point[1] >= int(self.height)):
					pygame.draw.rect(
						self.screen,
						(0, 0, 0),
						(
							(x * self.scale, y * self.scale),
							(ceil(self.scale), ceil(self.scale))
						)
					)
				else:					
					pygame.draw.rect(
						self.screen,
						self.screen.get_at((image_point[0], image_point[1] + int(self.height * self.scale))),
						(
							(round(x * self.scale), round(y * self.scale)),
							(round(self.scale), round(self.scale))
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
						(ceil((x + self.width) * self.scale), ceil(y * self.scale)),
						(ceil(self.scale), ceil(self.scale))
					)

				)