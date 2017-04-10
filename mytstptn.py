# Raspberry Pi TV Test Pattern Generator Files
#
# mytstptn.py: 	change audio and image path
#				cleanup keydn event filename.jpg
#				GPIO 23,24,25 -->pin 16,18,22 =swUP,swDN.swRND
# date: 6/04/2017
# author: sarodp@yahoo.com
#---------------------------------------------------------

# wiring diagram from Raspberry Pi GPIO port 
# to pushbuttons swUP and swDN.
#
#     GPIO-23 [pin16]------[swUP]----| 
#     GPIO-24 [pin18]------[swDN]----| 
#                                    |
#     GROUND  [pin20]----------------|
#                                    |
#     GPIO-25 [pin22]------[swRND]---| 
 

#-----------------------------------------------------
# C R E D I T
#-----------------------------------------------------
# source 
# readme: http://zappy.xs4all.nl:8877/zooi/atv/
# src: http://zappy.xs4all.nl:8877/zooi/atv/tstptn.py
#
# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------
# (c) pa3bwe, pa3bwe@amsat.org
# this program maybe freely used and distributed for amateur (ham) purposes
# a qsl card is appreciated!
#---------------------------------------------------------------------------
#
# GPIO 8,7   -->pin 24,26 =swUP,swDN
#
# atv2.py	: sound added
# atv3.py	: added possibility to use switch to scroll through images
#             two switches connected to header pin 24+26 (GPIO8 + GPIO7) and gnd
# 		      see http://tinyurl.com/6wq9l86
#		      added cmd line call to amixer to increase sound level
#----------------------------------------------------------------------------------


import pygame
from pygame.locals import *
import time
import os
import sys
import random
import glob
import RPi.GPIO as GPIO

# screen size
size_h = 768
size_v = 576

#misc paths
#atv_media_path = '/home/pi/atv/images'
#snd_media_path = '/home/pi/atv/sounds'
atv_media_path = '/home/pi/myiot/mypygame/atv'
snd_media_path = '/home/pi/myiot/mypygame/atv'

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


def switchUP(channel):
	global switch_picture
	global images
	global switch_used
	switch_picture += 1 
	if switch_picture >= len(images):
		switch_picture = 0
	switch_used = True

def switchDN(channel):
	global switch_picture
	global images
	global switch_used
	switch_picture -= 1
	if switch_picture < 0:
		switch_picture = len(images) - 1
	switch_used = True

def switchRND(channel):
	global switch_used
	global randomPicture 
	randomPicture = True
	switch_used = False

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


#=======================================================================

def main():
	#00--init var's
	global callsign
	global internalPicture
	global soundOn
	global images
	global switch_used
	global randomPicture 

	#01--set mixer to max
	os.system("amixer set PCM -- 400") 

	#01a--find all pictures
	images = sorted(glob.glob( os.path.join(atv_media_path,"*.jpg" )))
	
	#02--set IO, interrupt/callback
	swUP = 16
	swDN = 18
	swRND = 22
	
	#debounce time in msec.
	msecdebounce = 300  
	
	#configure as board
	GPIO.setmode(GPIO.BOARD)                                 
	
	# pull up active, we can use ground closure
	GPIO.setup(swUP, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
	GPIO.setup(swDN, GPIO.IN, pull_up_down=GPIO.PUD_UP)        
	GPIO.setup(swRND, GPIO.IN, pull_up_down=GPIO.PUD_UP)        

	# interrupt & callback
	GPIO.add_event_detect(swUP, GPIO.FALLING, callback=switchUP, bouncetime=msecdebounce)
	GPIO.add_event_detect(swDN, GPIO.FALLING, callback=switchDN, bouncetime=msecdebounce) 
	GPIO.add_event_detect(swRND, GPIO.FALLING, callback=switchRND, bouncetime=msecdebounce) 
   
    #03a--display var's
	textOn = False
	stepX = 10
	stepY = 10

	#03--start sound (if available)
	
	#04--never start with internal picture
	internalPicture = False
	randomPicture = False
	
	#10---pygame init...
	pygame.init()
	
	pygame.mixer.init(44000, -16, 1, 1024)
	pygame.mixer.music.load(globalsound)
	pygame.mixer.music.set_volume(1.0)

	pygame.mouse.set_visible (0)

	timer1delay = 1000 #--msec delay
	pygame.time.set_timer(pygame.USEREVENT, timer1delay)

	screen = pygame.display.set_mode((size_h,size_v),pygame.FULLSCREEN)

	update_screen(screen, True)

	if soundOn:
		playsound()

	#20---pygame.loop
	FPS = 10   #--frame per sec
	clock = pygame.time.Clock()
	clock.tick(FPS)
	running = True

	while running:
		#20a--
		update_screen(screen, True)

		#20b--
		if switch_used == True:
			randomPicture = False
			switch_image()
			update_screen(screen, True)	
			switch_used = False

		#20c---
		event = pygame.event.poll()

		#20c1---
		if event.type == pygame.USEREVENT and randomPicture:
			pic = random.randint(1, 14)
			loadimage(('%02d' % pic))
			update_screen(screen, True)
		#20c2---
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
			
			if event.key == pygame.K_r:
				randomPicture = not randomPicture

			if event.key == pygame.K_HOME:
				loadimage("01")
			if event.key == pygame.K_END:
				loadimage('%02d' % len(images))

			if event.key == pygame.K_F1:
				loadimage("01")
			if event.key == pygame.K_F2:
				loadimage("02")
			if event.key == pygame.K_F3:
				loadimage("03")
			if event.key == pygame.K_F4:
				loadimage("04")
			if event.key == pygame.K_F5:
				loadimage("05")
			if event.key == pygame.K_F6:
				loadimage("06")
			if event.key == pygame.K_F7:
				loadimage("07")
			if event.key == pygame.K_F8:
				loadimage("08")
			if event.key == pygame.K_F9:
				loadimage("09")
			if event.key == pygame.K_F10:
				loadimage("10")
			if event.key == pygame.K_F11:
				loadimage("11")
			if event.key == pygame.K_F12:
				loadimage("12")

	#99---Done
	pygame.quit()
	pygame.mixer.quit()
	GPIO.cleanup()
	print '\n', exittext
	sys.exit(exitlevel)         

#1000---
if __name__ == "__main__":
	main()
