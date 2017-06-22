import pygame, sys
from pygame.locals import *
import os
from opener import *
from collect import *
from arranger import *
  

mode = 0
#Modes:
#0 none
#1 opener
#2 synth
looping = False

SYNTH = ["Arranger","Keyboard","Drumrack","Custom"]

if __name__ == "__main__":
    pass

def scan(folder,extension):
    items = []
    for item in os.listdir(folder):
        if item.endswith(extension):
            items.append(item)
    print items
    return items
class Status():
	lastId = 0
	def __init__(s,values):
		s.lastId = int(values.get("lastId"))
	def __repr__(s):
		return '{"lastId":'+str(s.lastId)+'}'
	def getNewId(s):
		s.lastId +=1
		with open("status.json","w") as f:
			print s
			f.write(str(s))
		return s.lastId
	
with open("status.json","r") as f:
	status = json.load(f,object_hook=Status)
print status
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
		over = Keyboard(DISPLAYSURF,seasonId=status.getNewId())
	if coice == "Drumrack": 
		over = Drumrack(DISPLAYSURF,seasonId=status.getNewId())
	if coice == "Arranger":
		over = Arranger(DISPLAYSURF)
		over.loop()
	elif coice == "Custom":
		list = scan("pds",".pd")
		prompt = Promt(DISPLAYSURF,list)
		coice = prompt.loop()
		print coice
		coice = os.path.join("pds",coice)
		over = Custom(DISPLAYSURF,seasonId=status.getNewId())
		over.start(coice)
		#TODO start custom synth
	print "Finish"