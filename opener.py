import os
import pygame, sys
from pygame.locals import *


class Promt:
    # set up the colors
    BLACK = (  0,   0,   0)
    WHITE = (255, 255, 255)
    RED   = (255,   0,   0)
    GREEN = (  0, 255,   0)
    BLUE  = (  0,   0, 255)
    GRAY = (30,30,30)
    DARK = (10,10,10)
    LIGHT = (200,200,200)
    DIR = "pds"
    def __init__(s,display,list):
        s.DISPLAYSURF = display
        s.list = list
        s.selected = 0
        s.cam = 0
        s.RETURN = 0
        s.font =pygame.font.SysFont("monospce",40)
    def drawText(s,x,y,string):
        label = s.font.render(string,1,s.RED)
        s.DISPLAYSURF.blit(label,(x,y))
        '''
    def openPd(s,string):
        path = os.path.join(DIR,string)
        print "OPENING:"
        print path
        RETURN = path
        '''

    def loop(s):
        #s.item = s.list
        s.RETURN = 0
        s.looping = True
        while s.looping:
            for event in pygame.event.get(): 
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                s.handle(event)
            s.DISPLAYSURF.fill(s.BLACK)
            s.drawList()
            pygame.display.update()
            if s.RETURN != 0:
                print s.RETURN
                s.looping = False
                return s.RETURN
    def drawList(s):
        h = 30
        for i,item in enumerate(s.list):
            x = 100
            y = 35*i
            pygame.draw.rect(s.DISPLAYSURF, s.GRAY, (x, y, 200, h))
            pygame.draw.rect(s.DISPLAYSURF, s.GREEN, (x, y, 200, h),2)
            s.drawText(x,y,item)
        pygame.draw.rect(s.DISPLAYSURF, s.BLUE, (x, 35*s.selected, 200, h),3)
    def handle(s,event):
        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                s.selected += 1
            if event.key == K_SPACE:
                #s.openPd(s.list[s.selected])
                s.RETURN = s.list[s.selected]
            if event.key == K_UP:
                s.selected -= 1
        if s.selected >= len(s.list):
            s.selected = 0
        if s.selected <0:
            s.selected = len(s.list)-1
            


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.quit()

    # set up the window
    DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
    pygame.display.set_caption('Drawing')

    pygame.display.set_caption('Drawing')
    font =pygame.font.SysFont("monospce",40)
    global a
    a = Promt(DISPLAYSURF,["Janek","Maggi","Jochen"])
'''
def scan():
    global items
    items = []
    for item in os.listdir(DIR):
        if item.endswith(".pd"):
            items.append(item)
    print items
'''
# run the game loop
