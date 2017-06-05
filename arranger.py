import wave
import contextlib
import os
import pygame, sys
from pygame.locals import *
import time
import json
from opener import *

def scan(folder,extension):
    items = []
    for item in os.listdir(folder):
        if item.endswith(extension):
            items.append(item)
    print items
    return items
def byteToInt(bytearray):
	tmp = []
	for i,x in enumerate(bytearray):
		if i %2 == 0:
			tmp.append( int(bytearray[i]+bytearray[i+1],16))
	return tmp
def avrg(arr):
	return sum(arr)/len(arr)
def getAmps(path,scale):
	tmp = []
	f = wave.open(path)
	frames = f.getnframes()
	rate = f.getframerate()
	duration = frames / float(rate)
	l = frames / scale
	for i in range(int(l)):
		f.setpos(i*scale)
		a =	f.readframes(10)
		c = a.encode("hex")
		d = byteToInt(c)
		tmp.append(avrg(d))
	return tmp

class Arranger():
	BLACK = (  0,   0,   0)
	WHITE = (255, 255, 255)
	RED   = (255,   0,   0)
	GREEN = (  0, 255,   0)
	BLUE  = (  0,   0, 255)
	CHANNELHEIGHT = 60
	def __init__(s,display):
		s.DISPLAYSURF = display
		s.RETURN = 0
		s.clips = []
		s.pixelPerSec = 80
		#1s = 80
		#1000ms = 80
		#1ms = .08
		s.keys = []
		s.state = "stop"
		s.selected = False
		s.div = (0,0)
		s.playhead = 0.0
		s.lastTime = time.time()
		s.files = scan("rec",".wav")
		#s.scale = 1.0
		s.cam = Camera(1.0,(0,0)) 
		print s.files
		s.cursor = Cursor()
	def loop(s):
		s.RETURN = 0
		while True:
			
			delta = time.time()-s.lastTime
			s.lastTime = time.time()
			if s.state == "play":
				s.playhead += delta*s.pixelPerSec
			for event in pygame.event.get(): 
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						pygame.quit()
						sys.exit()
				s.handle(event)
			if K_LEFT in s.keys:
				s.cursor.move((-1,0))
			if K_RIGHT in s.keys:
				s.cursor.move((1,0))
			if K_b in s.keys:
				if s.selected:
					s.selected.pos = s.cursor.pos[0] + s.div[0],s.cursor.pos[1] + s.div[1]
			else:
				for clip in s.clips:
					if clip.pos[1] == s.cursor.pos[1] and clip.pos[0]<s.cursor.pos[0] and clip.getPixelLength()+clip.pos[0]>s.cursor.pos[0]:
						s.selected = clip
						break
					else:
						s.selected = False
			s.DISPLAYSURF.fill(s.BLACK)
			s.draw()
			pygame.display.update()
			if s.RETURN != 0:
				print s.RETURN
				s.looping = False
				return s.RETURN
			
	def play(s):
		s.state = "play"
	def pause(s):
		s.state = "stop"
	def stop(s):
		s.state = "stop"
		s.playhead = 0
	def handle(s,event):
		if event.type == KEYDOWN:
			s.keys.append(event.key)
			if event.key == K_UP:
				s.cursor.move((0,-1))
			if event.key == K_DOWN:
				s.cursor.move((0,1))
			if event.key == K_b and s.selected:
				s.div = s.selected.pos[0]-s.cursor.pos[0],s.selected.pos[1]-s.cursor.pos[1]
			if event.key == K_n and s.selected:
				s.dublicate(s.selected)
			if event.key == K_SPACE:
				if s.state == "play":
					s.pause()
				elif s.state == "stop":
					s.play()
			if event.key == K_v:
				s.saveQlist()
				'''
			if event.key == K_1:
				s.scale+=100
			if event.key == K_2:
				s.scale-=100
				print s.scale
'''
			if event.key == K_3:
				
			if event.key == K_4:
				
			if event.key == K_x:
				s.showAddMenu()

		if event.type == KEYUP:
			if event.key in s.keys:
				s.keys.remove(event.key)
	def draw(s):
	 	for clip in s.clips:
	 		clip.draw(s.DISPLAYSURF)
	 	s.cursor.draw(s.DISPLAYSURF)
	 	pygame.draw.line(s.DISPLAYSURF, s.GREEN, (s.playhead, 0), (s.playhead, 300), 1)
	 	if s.selected:
	 		s.selected.drawSelect(s.DISPLAYSURF)
	def getLength(s,path):
		fname = path
		with contextlib.closing(wave.open(fname,'r')) as f:
		    frames = f.getnframes()
		    rate = f.getframerate()
		    duration = frames / float(rate)
		    return int(duration*1000)
	def dublicate(s,clip):
		c = Clip(clip.pos,s)
		c.length = clip.length
		print clip.length
		c.pos = c.pos[0]+c.getPixelLength(),c.pos[1]
		s.clips.append(c)

	def saveQlist(s):
		f = open("qlist/qlist.txt","r+")
		for clip in s.clips:
			strg = str(clip.path).strip(".wav")
			strg  = strg.strip("rec/")
			f.write(str(int(clip.pos[0]*10))+ " c" + str(clip.pos[1]) + " " + strg + ";\n")
		print f.read()
		f.close()
	def showAddMenu(s):
		prompt = Promt(DISPLAYSURF,["add sound","save","exit"])
		coice = prompt.loop()
		if coice == "exit":
			pygame.quit()
			sys.exit()
		elif coice == "add sound":
			prompt = Promt(DISPLAYSURF,scan("rec",".wav"))
			coice = prompt.loop()
			clip = Clip(s.cursor.pos,s)
			clip.path = "rec/" + coice
			clip.getWavForm()
			clip.length = s.getLength(clip.path)
			s.clips.append(clip)

class Clip(object):
	def __init__(s,pos,parent,**options):
		s.pos = pos
		s.length = 0
		s.pathId = 0000
		s.parent = parent
		s.path = os.path.join("rec",str(s.pathId))+".wav"
		s.waveForm = []
		#s.getWavForm()
	def draw(s,display):
		pygame.draw.rect(display,Arranger.WHITE,(s.pos[0],Arranger.CHANNELHEIGHT*s.pos[1],s.getPixelLength(),Arranger.CHANNELHEIGHT))
	#	for i,line in enumerate(s.waveForm):
	#		i*s.parent.pixelPerSec
	#		pygame.draw.line(display,Arranger.RED,(i+s.pos[0],Arranger.CHANNELHEIGHT*s.pos[1]+Arranger.CHANNELHEIGHT*.5-line/8),(i+s.pos[0],Arranger.CHANNELHEIGHT*s.pos[1]+Arranger.CHANNELHEIGHT*.5+line/8))
	def drawSelect(s,display):
		pygame.draw.rect(display,Arranger.RED,(s.pos[0],Arranger.CHANNELHEIGHT*s.pos[1],s.getPixelLength(),Arranger.CHANNELHEIGHT),4)
	def getPixelLength(s):
		return s.length * s.parent.pixelPerSec/1000
	def getWavForm(s):
		amps = getAmps(s.path,s.parent.scale)
		s.waveForm  = amps
class Cursor(object):
	def __init__(s):
		s.pos = (0,0)
	def draw(s,display):
		pygame.draw.line(display, Arranger.BLUE, (s.pos[0], 0), (s.pos[0], 300), 4)
		pygame.draw.rect(display, Arranger.BLUE, (s.pos[0]-5, s.pos[1]*Arranger.CHANNELHEIGHT, 11, Arranger.CHANNELHEIGHT),2)
	def move(s,add):
		s.pos = (s.pos[0]+add[0],s.pos[1]+add[1])
class Camera:
	def __init__(s,scale,pos):
		s.scale = scale
		s.pos = pos
if __name__ == "__main__":
	pygame.init()
	pygame.font.init()
	swidth = pygame.display.Info().current_w
	sheight = pygame.display.Info().current_h
	pygame.mixer.quit()

	DISPLAYSURF = pygame.display.set_mode((400, 300), 0,32)
	pygame.display.set_caption('Drawing')
	font =pygame.font.SysFont("monospce",40)

	a = Arranger(DISPLAYSURF)
	'''
	c = Clip((5,1),a)
	c.length = 2
	a.clips.append(c)
	b = a.getLength("rec/0.wav")
	print b
	'''
	a.loop()
