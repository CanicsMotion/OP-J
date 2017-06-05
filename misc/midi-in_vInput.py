import pygame, sys
import pygame.midi
from pygame.locals import *
import uinput
import os

def send2Pd(message=''):
    os.system("echo '" + message + "' | pdsend 3000")

def on(vl):
    message = '0 ' + str(vl) + ';'
    send2Pd(message)


# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

looping = True

device = uinput.Device([uinput.BTN_LEFT,uinput.BTN_RIGHT,uinput.ABS_X,uinput.ABS_Y])

pygame.init()
pygame.font.init()
swidth = pygame.display.Info().current_w
sheight = pygame.display.Info().current_h

DISPLAYSURF = pygame.display.set_mode((400, 300), 0,32)#pygame.FULLSCREEN, 32)
pygame.display.set_caption('Drawing')
font =pygame.font.SysFont("monospce",40)
pygame.midi.init()
while pygame.midi.get_count() < 3:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

    
    print("no dev")
    DISPLAYSURF.fill(WHITE)
    #pygame.draw
    label = font.render("No Device Connected",1,(255,255,0))
    DISPLAYSURF.blit(label,(100,100))

    pygame.display.update()
    pygame.midi.quit()
    pygame.midi.init()
i = pygame.midi.Input(3)
#[[[144, 60, 1, 0], 251523], [[128, 60, 0, 0], 252309]]

notes = []
knops = [0]*127

scale = 9


class Note(object):
    def __init__(self,value,vel):
        self.value = value
        self.vel = vel
        notes.append(self)
    def __eq__(self,other):
        return self.value==other.value
    def remove(self,val):
        if self.value == val:
            notes.remove(self)


def draw():
    #48 - 72 Notes = 24
    global DISPLAYSURF
    scl = 24
    global notes
    h = DISPLAYSURF.get_height()
    w = DISPLAYSURF.get_width()
    for note in notes:
        x = float(note.value-48)*(w/scl)
        pygame.draw.rect(DISPLAYSURF,(note.vel*2,note.vel*2,note.vel*2),(x,0,(w/scl),h))
    for index,knop in enumerate(knops):
        pygame.draw.rect(DISPLAYSURF,(255,0,255,64),(index*(w/scale),h,(w/scale),(float(-knop)/127.0)*h))

def update():
    global i ,scale
    if i.poll():
        info = i.read(1024)
        for index in info:
            cmd = index[0][0]
            nht = index[0][1]
            vel = index[0][2]
            if cmd == 144:
                Note(nht,vel)
                if nht == 50:
                    device.emit(uinput.BTN_LEFT,True)
                if nht == 51:
                    device.emit(uinput.BTN_RIGHT,True)
            if cmd == 128:
                for item in notes:
                    item.remove(nht)
                if nht == 50:
                    device.emit(uinput.BTN_LEFT,False)
                if nht == 51:
                    device.emit(uinput.BTN_RIGHT,False)
            if cmd == 176:
                knops[nht] = vel
                if nht == 1:
                    scale = vel+1
                if nht == 2:
                    device.emit(uinput.ABS_X, vel*swidth/127)
                if nht == 3:
                    info = pygame.display.Info()
                    device.emit(uinput.ABS_Y, vel*sheight/127)
                if nht == 4:
                    on(vel)
                
            #print index[0]

while looping:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == K_F4:
                pygame.display.toggle_fullscreen()
            if event.key == K_F5:
                looping = False
    DISPLAYSURF.fill(WHITE)
    update()
    draw()
    pygame.display.update()
