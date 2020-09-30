import pygame

from time import sleep, time

from my_time import *
from graphics import Session
from video_save import SaveVideo

WIDTH, HEIGHT = 200, 200
out_scale = 1.2
out_noiseScale = 0.02
out_step = 0.5
out_depth = 150
out_distance = 200
out_out_frames = 300
out_octaves = 10


def startSession():
	#Session(self,    width, height, scale, 	  noiseScale = 1,    depth = 10000, step = 0.5, distance = 100, out_frames = 0):
	session = Session(WIDTH, 
					  HEIGHT, 
					  scale = out_scale, 
					  noiseScale = out_noiseScale, 
					  depth = out_depth, 
					  step = out_step, 
					  distance = out_distance, 
					  octaves = out_octaves,
					  out_frames = out_out_frames)

	z = 0
	time_spent = 0

	while session.isGoing:
		timer = time()

		session.Events()
		session.ThreadDraw(1)

		time_spent += time() - timer

		print("Frame took ", round(time() - timer, 2), "s")
		if (session.out_frames > 0):
			time_left = TimeLeft(session.out_frames, session.frame_id, time_spent)
			print(str(round(100 * session.frame_id / session.out_frames, 2)) + "% Time left: " + HoursLeft(time_left) + MinutesLeft(time_left) + Seconds(time_left))
		print(". . .")

		
is_app_open = True
inp = ""

def Settings():
	print("************")
	print("**settings**")
	print("************")
	print("noiseScale: ", out_noiseScale)
	print("step: ", out_step)
	print("depth: ", out_depth)
	print("distance: ", out_distance)
	print("octaves: ", out_octaves)
	print("out_frames: ", out_out_frames)
	print("************")
	
def Help():
	print("Use following commands:")
	print(" 'start' - to start the programm")
	print(" 'saveVideo' - to save generated while 'start' photos in a video")
	print(" 'help(start)'")
	print(" 'settings' - to see current settings")
	print(" 'q' - to quit the programm")
	print(" 'help' - to show this text again")
	print("---------------------------")
	print("Use these ones for editing settings:")
	print(" 'noiseScale' - bigger value -> further zoom is")
	print(" 'step' - step in the 3rd demension in noise")
	print(" 'depth' - when noise will repeat along 3rd demension")
	print(" 'distance' - distance between lense and image. In other words bigger value = stronger effect")
	print(" 'octaves' - octaves of noise")
	print(" 'out_frames' - number of generated frames. They will be saved in 'frames' folder. Leave 0 if you dont want them to save")


print("********")
print("Welcome!")
print("********")
Help()

while is_app_open:
	print("--------")
	inp = input()
	
	if (inp == "q"):
		is_app_open = False
		print("Bye!")
	elif (inp == "noiseScale"):
		print("Current value is: ", out_noiseScale, " Type new value:")
		try:
			out_noiseScale = float(input())
		except ValueError:
			print("Not a float")
			
		print("New value is: ", out_noiseScale)
		
	elif (inp == "step"):
		print("Current value is: ", out_step, " Type new value:")
		try:
			out_step = float(input())
		except ValueError:
			print("Not a float")
			
		print("New value is: ", out_step)
		
	elif (inp == "depth"):
		print("Current value is: ", out_depth, " Type new value:")
		try:
			out_depth = int(input())
		except ValueError:
			print("Not a int")
			
		print("New value is: ", out_depth)
		
	elif (inp == "distance"):
		print("Current value is: ", out_distance, " Type new value:")
		try:
			out_distance = int(input())
		except ValueError:
			print("Not a int")
			
		print("New value is: ", out_distance)
		
	elif (inp == "octaves"):
		print("Current value is: ", out_octaves, " Type new value:")
		try:
			out_octaves = int(input())
		except ValueError:
			print("Not a int")
			
		print("New value is: ", out_octaves)
		
	elif (inp == "out_frames"):
		print("Current value is: ", out_out_frames, " Type new value:")
		try:
			out_out_frames = int(input())
		except ValueError:
			print("Not a int")
			
		print("New value is: ", out_out_frames)
		
	elif (inp == "help"):
		Help()
		
	elif (inp == "settings"):
		Settings()
		
	elif (inp == "start"):
		startSession()
		
	elif (inp == "saveVideo"):
		print("Input a file name:")
		fileName = input()
		SaveVideo(fileName)
		
	else:
		print("Nonexisting command!")