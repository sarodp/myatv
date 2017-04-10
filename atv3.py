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

#colors
blackColor = pygame.Color( 0, 0, 0)
whiteColor = pygame.Color( 255, 255, 255)
greenColor = pygame.Color( 0, 255, 0)
redColor = pygame.Color( 255, 0, 0)

# some constants ---------------------
#screen size
size_h = 640
size_v = 480

#misc paths
atv_media_path = '/home/pi/atv/images'
snd_media_path = '/home/pi/atv/sounds'

images = []
i = 0
globalimage = os.path.join(atv_media_path,"image1.jpg")
globalsound = os.path.join(snd_media_path,"sound.wav")
callsign = "PA3BWE"
internalPicture = False
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
			internalPicture = False
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
			internalPicture = False
	except:
		pass
			
#random color
def randomColor():
	return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

#update screen
def update_screen(screen, update):
	global globalimage
	global callsign
	global internalPicture
	global soundOn
	
	if internalPicture:
		surface = pygame.Surface(screen.get_size())
		pygame.draw.rect(surface, blackColor, (0, 0, 640, 320))
		pygame.draw.rect(surface, whiteColor, (0, 240, 640, 320))
		for w in range(10):
			pygame.draw.rect(surface, randomColor(), (w * 64, 230, (w + 1) * 64, 20))
		
		screen.blit(surface, (0,0))
				
		font = pygame.font.Font('freesansbold.ttf', 130)
		
		fontCall = font.render(callsign, True, whiteColor)
		fontRect = fontCall.get_rect()
		fontRect.centerx = screen.get_rect().centerx
		fontRect.centery = 120
		screen.blit(fontCall, fontRect)	
		
		fontCall = font.render(callsign, True, blackColor)
		fontRect.centery = 360			
		screen.blit(fontCall, fontRect)
	else:
		picture = pygame.image.load(globalimage)
		picture = pygame.transform.scale(picture,(size_h, size_v))
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
		switch_picture = len(images) - 1
	switch_used = True

def switch26(channel):
	global switch_picture
	global switch_used
	switch_picture -= 1
	if switch_picture <= 0:
		switch_picture = 0
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
	
	#always start with internal picture
	internalPicture = True
	randomPicture = False
	
	pygame.init()
	
	pygame.mixer.init(44000, -16, 1, 1024)
	pygame.mixer.music.load(globalsound)
	pygame.mixer.music.set_volume(1.0)
	
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
			
			if event.key == pygame.K_i:
				internalPicture = True
			
			if event.key == pygame.K_r:
				randomPicture = not randomPicture
				if randomPicture:       			# do it immediate, we don't want to wait xx seconds ...
					pic = random.randint(1, 25)
					loadimage(str(pic))
							
			if event.key == pygame.K_t:
				if textOn:
					update_screen(screen, True)
				else:
					font = pygame.font.Font('freesansbold.ttf', 80)
					fontCall = font.render(callsign, True, (randomColor()))
					fontRect = fontCall.get_rect()
		
					fontRect.centerx = screen.get_rect().centerx
					fontRect.centery = screen.get_rect().centery
					screen.blit(fontCall, fontRect)	
					pygame.display.update()
					
				textOn =  not textOn
			
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
			
		if textOn:
			update_screen(screen, False)
			screen.blit(fontCall, fontRect)	
			pygame.display.update()
			fontRect.centery += stepY
			fontRect.centerx += stepX
			if fontRect.top <= 0 or fontRect.bottom >= screen.get_rect().height:
				stepY = 0 - stepY
				fontCall = font.render(callsign, True, (randomColor()))
			if fontRect.left <= 0 or fontRect.right >= screen.get_rect().width:
				stepX = 0 - stepX
				fontCall = font.render(callsign, True, (randomColor()))
		clock.tick(2)
		
		if internalPicture:
			update_screen(screen, True)
			textOn = False
			
	pygame.quit()
	pygame.mixer.quit()
	GPIO.cleanup()
	print '\n', exittext
	sys.exit(exitlevel)         
	
if __name__ == "__main__":
	main()
