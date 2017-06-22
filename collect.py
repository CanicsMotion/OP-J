#####################################
# @Autor Janek
# keys:
#   esc Exit
######################################

#Ids
#0 Noteon
#1 Notes off
#2 Stop
#3 DSP
#4 REC

import pygame, sys
from pygame.locals import *
import os
import subprocess
import random

class PdOpener:
    DIR = "pds"
    def __init__(s,p):
        s.parent = p
    def send2Pd(s,message=''):
        os.system("echo '" + message + "' | pdsend 3000")
    def send(s,id,msg):
        s.send2Pd(str(id)+" "+str(msg)+";")

    def startSynth(s,path):
        if s.parent.DEBUG:                  #Debug
            s.pd =subprocess.Popen(["puredata" ,path,"master.pd"])
        else:
            s.pd =subprocess.Popen(["puredata" ,"-nogui",path,"master.pd"])
class Overlay:
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE  = (  0,   0, 255)
    KEYS = [97, 119, 115, 101, 100, 102, 116, 103, 122, 104, 117, 106, 107, 111, 108, 112, 246, 252, 228]
    WHITES = [True,False,True,False,True,True,False,True,False,True,False,True,True,False,True,False,True,False,True]
    def __init__(s,display,**option):
        s.DISPLAYSURF = display
        s.looping = False
        s.pd = PdOpener(s)
        s.isRec = False
        s.looping = False
        s.notes = []
        s.DEBUG = False
        if option.get("seasonId"):
            s.seasonId = int(option.get("seasonId"))
        else:
            s.seasonId = 0
        s.init() 
    def init(s):
        s.pd.startSynth("pds/net.pd")
        s.loop()
    def draw(s):
        scl = 20
        h = s.DISPLAYSURF.get_height()
        w = s.DISPLAYSURF.get_width()
        s.DISPLAYSURF.fill(s.WHITE)
        if s.isRec:
            pygame.draw.rect(s.DISPLAYSURF,(70,40,40),(0,0,w,h))
        for note in s.notes:
            if note in s.KEYS:
                index = s.KEYS.index(note)
                x = index*w/scl
                pygame.draw.rect(s.DISPLAYSURF,(12,0,0),(x,0,(w/scl),h))
                if s.DEBUG:
                    print(index)
    def loop(s):
        s.looping = True
        while s.looping:
            for event in pygame.event.get():
                s.onEvent(event)
            s.draw()
            pygame.display.update()
        print "exit"

    def onEvent(s,event):
        if event.type == QUIT:
            s.Quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                s.Quit()
            if event.key == K_F4:
                pygame.display.toggle_fullscreen()
            if event.key == K_F5:
                s.looping = False

            s.notes.append(event.key)
            if s.DEBUG:
                print(s.notes)
            if event.key in s.KEYS:
                index = s.KEYS.index(event.key)
                message = '0 ' + str(index) + ';'
                s.pd.send2Pd(message)
            if event.key == K_m:
                s.toggleRec()
                
        if event.type == KEYUP:
            for item in s.notes:
                if item == event.key:
                    s.notes.remove(item)
                    if event.key in s.KEYS:
                        index = s.KEYS.index(event.key)
                        message = '1 ' + str(index) + ';'
                        s.pd.send2Pd(message)
                    break
    def Quit(s):
        s.stopRec()
        s.pd.pd.kill()
        s.looping=False
        if __name__ == "__main__":
            pygame.quit()
            sys.exit()
    def startRec(s):
        id = s.seasonId
        s.pd.send(4,"rec/"+str(id) + ".wav")
        print "isRec = True"+ str(id)
        s.isRec = True
    def stopRec(s):
        s.pd.send(4,0)
        print "isRec = False"
        s.isRec = False
    def toggleRec(s):
        if s.isRec:
            s.stopRec()
        else:
            s.startRec()

class Keyboard(Overlay):
    def init(s):
        s.pd.startSynth("pds/net.pd")
        s.loop()
    def draw(s):
        scl = 19
        h = s.DISPLAYSURF.get_height()
        w = s.DISPLAYSURF.get_width()
        s.DISPLAYSURF.fill(s.BLACK)
        if s.isRec:
            pygame.draw.rect(s.DISPLAYSURF,s.RED,(0,0,w,h))
        for note in s.notes:
            if note in s.KEYS:
                index = s.KEYS.index(note)
                x = (index+.5)*w/(scl+1)
                y = 0
                c = (0,0,0)
                if s.WHITES[index]:
                    y = h*.6
                    c = (index*10,255,255)
                else:
                    y = h*.4
                    c = (255,index*10,255)
                
                pygame.draw.rect(s.DISPLAYSURF,c,(x,y,(w/scl)-5,h*.3),10)
                if s.DEBUG:
                    print(index)
                pygame.draw.rect(s.DISPLAYSURF,c,(20,20,w-40,h-40),3)
                pygame.draw.rect(s.DISPLAYSURF,c,(0,0,w,h),8)
class Custom(Overlay):
    def init(s):
        s.path = "pds/net.pd"
    def start(s,path):
        s.pd.startSynth(path)
        s.loop()#
class Drumrack(Overlay):
    def init(s):
        s.pd.startSynth("pds/DrumRack.pd")
        s.loop()
    def draw(s):
        scl = 19
        h = s.DISPLAYSURF.get_height()
        w = s.DISPLAYSURF.get_width()
        s.DISPLAYSURF.fill(s.BLACK)
        if s.isRec:
            pygame.draw.rect(s.DISPLAYSURF,s.RED,(0,0,w,h))
        for note in s.notes:
            if note in s.KEYS:
                index = s.KEYS.index(note)
                x = (index+.5)*w/(scl+1)
                y = 0
                c = (0,0,0)
                if s.WHITES[index]:
                    y = h*.6
                    c = (index*10,255,255)
                else:
                    y = h*.4
                    c = (255,index*10,255)
                
                pygame.draw.rect(s.DISPLAYSURF,c,(x,y,(w/scl)-5,h*.3),10)
                if s.DEBUG:
                    print(index)
                pygame.draw.rect(s.DISPLAYSURF,c,(20,20,w-40,h-40),3)
                pygame.draw.rect(s.DISPLAYSURF,c,(0,0,w,h),8)

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()
    swidth = pygame.display.Info().current_w
    sheight = pygame.display.Info().current_h
    pygame.mixer.quit()

    DISPLAYSURF = pygame.display.set_mode((400, 300), 0,32)
    pygame.display.set_caption('Drawing')
    font =pygame.font.SysFont("monospce",40)

if __name__ == "__main__":
    #c = raw_input("File in /pds/")
    #DEBUG = True
    #startSynth(os.path.join("pds",c))
    global a,DISPLAYSURF
    a = Keyboard(DISPLAYSURF)
    a.loop()
