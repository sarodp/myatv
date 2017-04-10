# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# (c) pa3bwe, pa3bwe@amsat.org
# this program maybe freely used and distributed for amateur (ham) purposes
# a qsl card is appreciated!
#-------------------------------------------------------------------------------
#atv2.py	: sound added
#atv3.py	: added possibility to use switch to scroll through images
#             two switches connected to header pin 24+26 (GPIO8 + GPIO7) and gnd
# 		      see http://tinyurl.com/6wq9l86
#		      added cmd line call to amixer to increase sound level

import pygame
from pygame.locals import *
import time
import os
import sys
import random
import glob
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

# screen size
size_h = 768
size_v = 576

#misc paths
atv_media_path = '/home/pi/atv/images'
snd_media_path = '/home/pi/atv/sounds'

images = []
i = 0
globalimage = os.path.join(atv_media_path,"image01.jpg")
globalsound = os.path.join(snd_media_path,"sound.wav")
soundOn = True			# if available
switch_used = False		# external switch not used ...
switch_picture = 0		# first picture in images[]

#load image
def loadimage(s):
	global globalimage
	global internalPicture
	
	testimage = os.path.join(atv_media_path,"image" + s + ".jpg")
	try:
		with open(testimage) as f:
			globalimage = testimage
	except:
		pass

#load image
def switch_image():
	global images
	global internalPicture
	global switch_picture
	global globalimage
	
	testimage = images[switch_picture]
	try:
		with open(testimage) as f:
			globalimage = testimage
	except:
		pass
			
#update screen
def update_screen(screen, update):
	global globalimage
	global callsign
	global internalPicture
	global soundOn
	
	picture = pygame.image.load(globalimage)
	screen.blit(picture, (0,0))
		
	if update:
		pygame.display.update()

def playsound():
	pygame.mixer.music.play(-1)

#return total number of jpg files	
def numjpgfiles(filepath):
	return len([f for f in os.listdir(filepath) if f.endswith('.jpg')])

def switch24(channel):
	global switch_picture
	global images
	global switch_used
	switch_picture += 1 
	if switch_picture >= len(images):
		switch_picture = 0
	switch_used = True

def switch26(channel):
	global switch_picture
	global switch_used
	switch_picture -= 1
	if switch_picture < 0:
		switch_picture = len(images) - 1
	switch_used = True
	
		
def main():
	global callsign
	global internalPicture
	global soundOn
	global images
	global switch_used
	os.system("amixer set PCM -- 400")   						 #set mixer to max"
	#find all pictures
	images = sorted(glob.glob( os.path.join(atv_media_path,"*.jpg" )))
	
	#set IO
	GPIO.setmode(GPIO.BOARD)                                 #configure as board
	GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)        # pull up active, we can use ground closure
	GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)        # pull up active, we can use ground closure
	GPIO.add_event_detect(24, GPIO.FALLING, callback=switch24, bouncetime=200)
	GPIO.add_event_detect(26, GPIO.FALLING, callback=switch26, bouncetime=200) 
   
	textOn = False
	stepX = 10
	stepY = 10
	#start sound (if available)
	
	# never start with internal picture
	internalPicture = False
	randomPicture = False
	
	pygame.init()
	
	pygame.mixer.init(44000, -16, 1, 1024)
	pygame.mixer.music.load(globalsound)
	pygame.mixer.music.set_volume(1.0)

        pygame.mouse.set_visible (0)
	
	pygame.time.set_timer(pygame.USEREVENT, 15000)
				
	screen = pygame.display.set_mode((size_h,size_v),pygame.FULLSCREEN)
	
	update_screen(screen, True)
	running = True
	clock = pygame.time.Clock()

	if soundOn:
		playsound()
		
	while running:
 		
 		if switch_used == True:
			switch_image()
			update_screen(screen, True)	
 			switch_used = False
 			
		event = pygame.event.poll()
		
		if event.type == pygame.USEREVENT and randomPicture:
			pic = random.randint(1, 25)
			loadimage(str(pic))
			update_screen(screen, True)
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
				running = False
				exittext = "Program terminated normally."
				exitlevel = 0
			
			
			if event.key == pygame.K_s:
				soundOn = not soundOn
				if soundOn:	
					playsound()
						
				if not soundOn:
					if pygame.mixer.music.get_busy():
						pygame.mixer.music.stop()
			
			if event.key == pygame.K_F1:
				loadimage("1")
			if event.key == pygame.K_F2:
				loadimage("2")	
			if event.key == pygame.K_F3:
				loadimage("3")
			if event.key == pygame.K_F4:
				loadimage("4")	
			if event.key == pygame.K_F5:
				loadimage("5")
			if event.key == pygame.K_F6:
				loadimage("6")	
			if event.key == pygame.K_F7:
				loadimage("7")
			if event.key == pygame.K_F8:
				loadimage("8")	
			if event.key == pygame.K_F9:
				loadimage("9")
			if event.key == pygame.K_F10:
				loadimage("10")	
			if event.key == pygame.K_F11:
				loadimage("11")
			if event.key == pygame.K_F12:
				loadimage("12")		
			update_screen(screen, True)				
			
		clock.tick(2)
		
			
	pygame.quit()
	pygame.mixer.quit()
	GPIO.cleanup()
	print '\n', exittext
	sys.exit(exitlevel)         
	
if __name__ == "__main__":
	main()
