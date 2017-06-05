import pygame, sys
from pygame.locals import *
import os
from opener import *
from collect import *


mode = 0
#Modes:
#0 none
#1 opener
#2 synth
looping = False

SYNTH = ["Keyboard","Drumrack","Custom"]

if __name__ == "__main__":
    pass

def scan(folder,extension):
    items = []
    for item in os.listdir(folder):
        if item.endswith(extension):
            items.append(item)
    print items
    return items


pygame.init()
pygame.font.init()
swidth = pygame.display.Info().current_w
sheight = pygame.display.Info().current_h
pygame.mixer.quit()

DISPLAYSURF = pygame.display.set_mode((400, 300), 0,32)
pygame.display.set_caption('Drawing')
font =pygame.font.SysFont("monospce",40)
while True:
	mode = 1
	prompt = Promt(DISPLAYSURF,SYNTH)
	coice = prompt.loop()
	mode = 2
	if coice == "Keyboard":
		over = Keyboard(DISPLAYSURF)
	if coice == "Drumrack":
		over = Drumrack(DISPLAYSURF)
	elif coice == "Custom":
		list = scan("pds",".pd")
		prompt = Promt(DISPLAYSURF,list)
		coice = prompt.loop()
		print coice
		coice = os.path.join("pds",coice)
		custom = Custom(DISPLAYSURF)
		custom.start(coice)
		#TODO start custom synth
	print "Finish"