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
	'''
	f = wave.open(path)
	frames = f.getnframes()
	rate = f.getframerate()
	duration = frames / float(rate)
	l = frames / scale
	for i in range(int(l)):
		f.setpos(i*scale)
		a =	f.readframes(int(10))
		c = a.encode("hex")
		d = byteToInt(c)
		tmp.append(avrg(d))
	'''
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
		s.delta = .02
		s.files = scan("rec",".wav")
		s.scale = 1.0
		s.cam = Camera(1.0,(0,0)) 
		print s.files
		s.cursor = Cursor(s)
	def loop(s):
		s.RETURN = 0
		while True:
			
			s.delta = time.time()-s.lastTime
			s.lastTime = time.time()
			if s.state == "play":
				s.playhead += s.delta*s.pixelPerSec
			for event in pygame.event.get(): 
				if event.type == QUIT:
					s.Quit()
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:
						s.Quit()
				s.handle(event)
			if K_LEFT in s.keys:
				s.cursor.move((-s.delta*(100000/s.pixelPerSec),0))
			if K_RIGHT in s.keys:
				s.cursor.move((s.delta*(100000/s.pixelPerSec),0))
			if K_b in s.keys:
				if s.selected:
					s.selected.pos = s.cursor.pos[0] + s.div[0],s.cursor.pos[1] + s.div[1]
			else:
				for clip in s.clips:
					if clip.pos[1] == s.cursor.pos[1] and clip.pos[0]<s.cursor.pos[0] and clip.length+clip.pos[0]>s.cursor.pos[0]:
						s.selected = clip
						break
					else:
						s.selected = False
			s.cam.pos = s.cursor.pos[0],s.cursor.pos[0]
			s.DISPLAYSURF.fill(s.BLACK)
			s.draw()
			pygame.display.update()
			if s.RETURN != 0:
				print s.RETURN
				s.looping = False
				return s.RETURN
	def Quit(s):
		if __name__ == "__main__":
			pygame.quit()
			sys.exit()
		s.RETURN = 1
			
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
			if event.key == K_DELETE:
				s.delete()
			if event.key == K_SPACE:
				if s.state == "play":
					s.pause()
				elif s.state == "stop":
					s.play()
			if event.key == K_v:
				s.saveQlist()
				
			if event.key == K_1:
				s.pixelPerSec*=1.2
				print s.pixelPerSec
			if event.key == K_2:
				s.pixelPerSec*=.81
				print s.pixelPerSec

			if event.key == K_3:
				pass
			if event.key == K_4:
				pass
			if event.key == K_x:
				s.showAddMenu()

		if event.type == KEYUP:
			if event.key in s.keys:
				s.keys.remove(event.key)
	def draw(s):
		localScale = int(s.pixelPerSec)
		while localScale<20:
			localScale*=10
			localScale+=1
		for i in  range(400/localScale +1):
			pygame.draw.line(s.DISPLAYSURF, (20,20,20), (i*localScale, 0), (i*localScale, 300), 1)
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
		#print clip.length
		c.pos = c.pos[0]+c.length,c.pos[1]
		c.path = clip.path
		s.clips.append(c)
	def delete(s):
		s.clips.remove(s.selected)
		s.selected = False

	def saveQlist(s):
		sort = sorted(s.clips,key=lambda Clip: Clip.pos[0])
		print sort
		with  open("qlist/qlist.txt","w") as f:
			f.seek(0)
			prev = 0
			for clip in sort:
				strg = str(clip.path).strip(".wav")
				strg  = strg.strip("rec/")
				f.write(str(int(clip.pos[0])-prev)+ " c" + str(clip.pos[1]) + " " + strg + ";\n")
				prev = int(clip.pos[0])
			#print f.read()
	def showAddMenu(s):
		prompt = Promt(s.DISPLAYSURF,["add sound","save","exit"])
		coice = prompt.loop()
		if coice == "exit":
			pygame.quit()
			sys.exit()
		elif coice == "add sound":
			prompt = Promt(s.DISPLAYSURF,scan("rec",".wav"))
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
		s.pathId = 0
		s.parent = parent
		s.path = os.path.join("rec",str(s.pathId))+".wav"
		s.waveForm = []
		#s.getWavForm()
	def draw(s,display):
		pygame.draw.rect(display,Arranger.WHITE,(s.getPixel(s.pos[0]),Arranger.CHANNELHEIGHT*s.pos[1],s.getPixelLength(),Arranger.CHANNELHEIGHT))
		
	#	for i,line in enumerate(s.waveForm):
	#		i*s.parent.pixelPerSec
	#		pygame.draw.line(display,Arranger.RED,(i+s.pos[0],Arranger.CHANNELHEIGHT*s.pos[1]+Arranger.CHANNELHEIGHT*.5-line/8),(i+s.pos[0],Arranger.CHANNELHEIGHT*s.pos[1]+Arranger.CHANNELHEIGHT*.5+line/8))
	def drawSelect(s,display):
		pygame.draw.rect(display,Arranger.RED,(s.getPixel(s.pos[0]),Arranger.CHANNELHEIGHT*s.pos[1],s.getPixelLength(),Arranger.CHANNELHEIGHT),4)
		font =pygame.font.SysFont("monospce",19)
		label = font.render(str(s.pos),1,Arranger.RED)
		display.blit(label,(s.getPixel(s.pos[0]),s.pos[1]*Arranger.CHANNELHEIGHT))
		label = font.render(str(s.length),1,Arranger.BLUE)
		display.blit(label,(s.getPixel(s.pos[0]),s.pos[1]*Arranger.CHANNELHEIGHT+Arranger.CHANNELHEIGHT/2))
	def getPixelLength(s):
		return s.length * s.parent.pixelPerSec/1000
	def getPixel(s,argument):
		return argument * s.parent.pixelPerSec/1000
	def getWavForm(s):
		amps = getAmps(s.path,s.parent.scale)
		s.waveForm  = amps
class Cursor(object):
	def __init__(s,parent):
		s._pos = (0,0)
		s.parent = parent
	def draw(s,display):
		pygame.draw.line(display, Arranger.BLUE, (s.getPixel(s.pos[0]), 0), (s.getPixel(s.pos[0]), 300), 4)
		pygame.draw.rect(display, Arranger.BLUE, (s.getPixel(s.pos[0])-5, s.pos[1]*Arranger.CHANNELHEIGHT, 11, Arranger.CHANNELHEIGHT),2)
	def move(s,add):
		s.pos = (s.pos[0]+add[0],s.pos[1]+add[1])
	def getPixel(s,argument):
		return argument * s.parent.pixelPerSec/1000
	@property
	def pos(s):
		return int(s._pos[0]),int(s._pos[1])
	@pos.setter
	def pos(s,value):
		s._pos = value
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
