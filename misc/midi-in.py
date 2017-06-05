import pygame, sys
import pygame.midi
from pygame.locals import *

pygame.init()

DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN, 32)
pygame.display.set_caption('Drawing')

pygame.midi.init()
while pygame.midi.get_count() < 3:
    print("no dev")
    pygame.midi.quit()
    pygame.midi.init()
i = pygame.midi.Input(3)
#[[[144, 60, 1, 0], 251523], [[128, 60, 0, 0], 252309]]

notes = []

# set up the colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

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

def update():
    global i
    if i.poll():
        info = i.read(1024)
        for index in info:
            cmd = index[0][0]
            nht = index[0][1]
            vel = index[0][2]
            if cmd == 144:
                Note(nht,vel)
            if cmd == 128:
                for item in notes:
                    item.remove(nht)
            print index[0]

while True:
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
    DISPLAYSURF.fill(WHITE)
    update()
    draw()
    pygame.display.update()
