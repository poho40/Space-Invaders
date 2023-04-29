import pygame
import sys
import os
import math
import random
from pygame.locals import *
from pygame import mixer
import time
from PIL import Image

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (300, 300))

def Level_text():
    over_text = over_font.render("Level : " + str(level), True, (255, 255, 255))
    screen.blit(over_text, (300, 300))
class ScrollingBackground:

    def __init__(self, screenheight, imagefile):
        self.img = pygame.image.load(imagefile)
        self.coord = [0, 0]
        self.coord2 = [0, -screenheight]
        self.y_original = self.coord[1]
        self.y2_original = self.coord2[1]

    def Show(self, surface):
        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)

    def updateCoordinates(self, speed_y, time):
        distance_y = speed_y * time
        self.coord[1] += distance_y
        self.coord2[1] += distance_y
        if self.coord2[1] >= 0:
            self.coord[1] = self.y_original
            self.coord2[1] = self.y2_original

class HeroShip:

    def __init__(self, screenheight, screenwidth, imagefile):
        self.shape = pygame.image.load(imagefile)
        self.top = screenheight - self.shape.get_height()
        self.left = screenwidth/2 - self.shape.get_width()/2

    def Show(self, surface):
        surface.blit(self.shape, (self.left, self.top))

    def UpdateCoords(self, x, y):
        self.left = x -self.shape.get_width()/2
class Enemy:

    def __init__(self, x, y, imagefile):
        self.shape = pygame.image.load(imagefile)
        self.top = y
        self.left = x

    def Show(self, surface):
        surface.blit(self.shape, (self.left, self.top))


class Lasers :

    def __init__(self, x, imagefile):
        self.shape = pygame.image.load(imagefile)
        self.top = screenheight -self.shape.get_height()
        self.left = x

    def Show(self, surface):
        surface.blit(self.shape, (self.left, self.top))

    def UpdateCoords(self):
        self.top = self.top  - 10 
pygame.init()  # initialize pygame
score_value = 0
level = 0
font = pygame.font.Font('freesansbold.ttf', 32)
over_font = pygame.font.Font('freesansbold.ttf', 64)
pygame.display.set_caption("Home Invader")
clock = pygame.time.Clock()
screenheight, screenwidth = (666, 1000)
screen = pygame.display.set_mode((screenwidth, screenheight))
framerate = 60
bg_speed = 100
starttime = time.time()
# Load the background image here. Make sure the file exists!

bg = ScrollingBackground(screenheight, "background.jpeg")
Hero = HeroShip(screenheight, screenwidth, "basketball.png")
pygame.mouse.set_visible(0)
pygame.display.set_caption('Goofy Game')
list = []
LaserX = []
LaserY = []
EnemyLaserX = []
EnemyLaserY = []
# Enemy
enemyImg = []
num_of_enemies = 6
EnemyX = []
EnemyY = []
img = Image.open("Enemy.png")
ship = Image.open("basketball.png")
laser = Image.open("laser.jpeg")
width = img.width
height = img.height

def reset_level():
    score_value = 0
    StartingX = 0
    StartingY = 0
    for i in range(num_of_enemies):
        if(StartingX + width > screenwidth):
            StartingX = 0
            StartingY += height
        EnemyY.append(StartingY)
        EnemyX.append(StartingX)
        StartingX += width
    StartingX = 0
    StartingY = 0
# fix indentation

running = True
while running:
    time = clock.tick(framerate)/1000.0
    x, y = pygame.mouse.get_pos()
    Hero.UpdateCoords(x,y)
    if(len(EnemyX) == 0):
        level+=1
        reset_level()
    for i in range(len(EnemyX)):
        if(pygame.time.get_ticks() % 300.0 == 40.0*(i+1)):
            EnemyLaserX.append(EnemyX[i])
            EnemyLaserY.append(EnemyY[i])
    for i in range(len(LaserY)):
        LaserY[i] -= 20
    for i in range(len(EnemyLaserY)):
        EnemyLaserY[i] += 20
    if pygame.time.get_ticks() % 30.0 == 0:
        LaserX.append(x)
        LaserY.append(screenheight - ship.height)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    bg.updateCoordinates(bg_speed, time)
    bg.Show(screen)
    Hero.Show(screen)
    actualJ = 0
    for j in range(len(EnemyX))[::-1]:
        for i in range(len(LaserX)):
            if ((LaserX[i] >= EnemyX[actualJ])&(LaserX[i] <= EnemyX[actualJ]+width) & (LaserY[i] >= EnemyY[actualJ]-height) & (LaserY[i] <= EnemyY[actualJ])):
                del LaserX[i]
                del LaserY[i]
                del EnemyX[actualJ]
                del EnemyY[actualJ]
                actualJ -=1
                score_value += 1
                break
        actualJ += 1
    for i in range(len(EnemyLaserX)):
        if ((EnemyLaserX[i] >= x)&(EnemyLaserX[i] <= x+ship.width) & (EnemyLaserY[i] >= screenheight - ship.height) & (EnemyLaserY[i] <= screenheight)):
            del EnemyLaserX[i]
            del EnemyLaserY[i]
            running = False
            game_over_text()
            break
    for i in range(len(EnemyX)):
        screen.blit(pygame.image.load("Enemy.png"), (EnemyX[i], EnemyY[i]))
    for i in range(len(LaserX)):
        screen.blit(pygame.image.load("laser.jpeg"), (LaserX[i], LaserY[i]))
    for i in range(len(EnemyLaserX)):
        screen.blit(pygame.image.load("laser.jpeg"), (EnemyLaserX[i], EnemyLaserY[i]))
    show_score(screenwidth-200, screenheight-100)
    if(running):
        Level_text()
    pygame.display.update()
    if(running == False):
        pygame.time.delay(1000)