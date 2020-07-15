from random import randint
from pygame.locals import *
import pygame as pg
import sys
import os
import ctypes
from os import listdir
from os.path import isfile, join


"""ARGUMENTS"""
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-wi', help="Screen width in blocks, min 4, default 8", type= int, default=8)
parser.add_argument('-he', help="Screen height in blocks, min 3, default 10", type= int, default= 10)
parser.add_argument('-l', help="Lives, min 1, default 3", type= int, default= 3)
print(parser.format_help())
args = parser.parse_args()
print(args)  # Namespace(bar=0, foo='pouet')
args.he = max(args.he, 3)
args.wi = max(args.wi, 4)
args.l = max(args.l, 1)
print("Height:", args.he) # pouet
print("width:", args.wi) # 0
print("Lives:", args.l) # 0

"""CONSTANTS"""
#Screen Constants
OFF = 50
SCRWIDTH = args.wi * OFF
SCRHEIGHT = args.he * OFF
SCRX = SCRWIDTH/OFF
SCRY = SCRHEIGHT/OFF
SCRRESOLUTIONWIDH = ctypes.windll.user32.GetSystemMetrics(0)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (SCRRESOLUTIONWIDH/2-SCRWIDTH/2,50)

#COLORS
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
DARKGREEN = (8,80,0)

#FONT
pg.font.init() 
myfont = pg.font.Font('PressStart2P.ttf', 12)

# #IN-GAME OBJECTS
# goF = 1 #frog
# goC = 2 #car
goW = 3 #water
# goT = 4 #turtle
goS = -1 #SAFE
goR = -2 #road
# goE = 0 #empty

# color = {goF:GREEN, goC:RED, goW:BLUE, goT: GREEN, goS:GREEN, goR:BLACK}

#SPRITES
carSprites = [f for f in os.listdir('./sprites/') if f[:3] == "car"]
for i in range(0, len(carSprites)):
    carSprites[i] = pg.image.load('./sprites/'+carSprites[i])
sprites = {
    goW: pg.image.load('./sprites/water.png'),
    goR: pg.image.load('./sprites/road.png'),
    goS: pg.image.load('./sprites/grass.png'),
    'live': pg.image.load('./sprites/heart.png')
    }


fpsClock = pg.time.Clock()
FPS = 30

DISPLAY = pg.display.set_mode((SCRWIDTH, SCRHEIGHT), 0)
pg.display.set_icon(pg.image.load('frog.png'))

def drawIntro(hiScore):
    DISPLAY.fill(DARKGREEN)
    DISPLAY.blit(myfont.render("FROGGEY GAME", False, WHITE), (10,SCRHEIGHT/2-40))
    DISPLAY.blit(myfont.render("arrows - move, space - start", False, WHITE), (10,SCRHEIGHT/2+20))
    DISPLAY.blit(myfont.render("esc - quit", False, WHITE), (10,SCRHEIGHT/2+40))
    DISPLAY.blit(myfont.render("HI-SCORE {0}".format(hiScore), False, WHITE), (10,SCRHEIGHT/2+60))


class Frog():
    """Main character class"""
    frogSprite = pg.image.load('./sprites/frog.png')
    x = 3
    y = 3
    alive = True
    lives = 0
    invisibility = False
    def move(self, key):
        if key == pg.K_UP:
            self.y = self.y - 1 if self.y - 1 >= 0 else self.y
        elif key == pg.K_RIGHT:
            self.x = self.x + 1 if self.x + 1 < SCRX else self.x
        elif key == pg.K_DOWN:
            self.y = self.y + 1 if self.y + 1 < SCRY else self.y
        elif key == pg.K_LEFT:
            self.x = self.x - 1 if self.x - 1 >= 0 else self.x
        else:
            pass
        return

    def draw(self):
        DISPLAY.blit(self.frogSprite, (self.x*OFF, self.y*OFF))
        for i in range(0, self.lives):
            DISPLAY.blit(sprites['live'], (i*40, 5))
        #draw rectangle instead of sprite
        #drawRect(self.x, self.y, DARKGREEN) 
        return

    def spawn(self):
        self.invisibility = False
        self.x = int(SCRX/2)
        self.y = SCRY-1
        #print(self.x, self.y)
        return

    def checkHit(self, x, y):
        if self.invisibility == False:
            if self.x==x and self.y == y:
                self.lives -= 1
                self.invisibility = True
                self.alive = (self.lives != 0)
        return self.x==x and self.y == y


    def checkWin(self):
        return self.y == 0 and self.x%2 == 0

    def __init__(self):
        self.spawn()
        self.lives = args.l

class Car():
    """Enemy class"""
    x = 0
    y = 0
    direction = 0
    tick = 0
    trigger = 0
    sprite = ''
    def ticked(self):
        self.tick += 1
        if self.tick == self.trigger:
            if self.direction == 0:
                self.x -= 1
                if self.x < 0:
                    self.x = SCRX
            else:
                self.x += 1
                if self.x > SCRX:
                    self.x = -1
            self.tick = 0
        return

    def draw(self):
        if self.direction == 0:
            DISPLAY.blit(self.sprite, (self.x*OFF, self.y*OFF))
        else:
            DISPLAY.blit(pg.transform.flip(self.sprite, True, False), (self.x*OFF, self.y*OFF))
        #drawRect(self.x, self.y, RED if self.y%2 else YELLOW)
        return

    def __init__(self, x, y, trigger, direction):
        self.x = x
        self.y = y
        self.trigger = trigger
        self.direction = direction
        self.sprite = carSprites[randint(0, len(carSprites)-1)]
        

class Level():
    levelNum = 1
    area = []
    enemies = []
    isNotOver = False

    def draw(self):
        for i in range(0, len(self.area)):
            for j in range(0, len(self.area[i])):
                DISPLAY.blit(sprites[self.area[i][j]], (j*OFF, i*OFF))
                #drawRect(j, i, color[self.area[i][j]])
        return
    
    def drawInfo(self, num, hi):
        score = myfont.render("HI-SCORE {0} LEVEL {1}".format(hi, num), False, WHITE)
        DISPLAY.blit(score, (SCRWIDTH-260,5))



    def __init__(self, num):
        self.isNotOver = True
        self.levelNum = num
        for i in range(int(SCRY)):
            self.area.append([])
            for j in range(int(SCRX)):
                if i == 0:
                    self.area[i].append(goS) if j%2==0 else self.area[i].append(goW)
                else:
                    self.area[i].append(goR)

        self.enemies = []
        i = 1
        while i < SCRY-1:
            direction = randint(0, 2)
            trigger = randint(5, 15)
            for j in range(1, int(SCRX/2)):

                self.enemies.append(Car(randint(0, SCRX), i, trigger, direction))
                #print( "i = {0} j = {1} dir = {2} trg = {3}".format(i, j, direction, trigger))
            i += randint(1, 3)



def drawRect(x, y, color):
    pg.draw.rect(DISPLAY, color, (x*OFF, y*OFF, OFF, OFF))

def gameQuit():
    pg.quit()
    sys.exit()

def update():
    pg.display.update()
    fpsClock.tick(FPS)