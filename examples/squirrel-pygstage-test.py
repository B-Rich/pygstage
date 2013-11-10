# Basic pygstage test using the squirrel graphics.
#
# Use arrow keys to move the squirrel around the world.

import pygame
from pygame.locals import *
import pygstage

pygame.init()
FPSCLOCK = pygame.time.Clock()
DISPLAYSURFACE = pygame.set_mode((640, 480))

GRASSCOLOR = (24, 255, 0)

world = pygstage.Stage(1000, 1000, bgcolor=GRASSCOLOR)
camera = pygstage.Camera(world, 640, 480)
squirrel = pygstage.Actor('squirrel.png')
world['squirrel'] = squirrel

camera.follow(squirrel)
camera.wander = 100

grassImages = []
for i in range(1, 5):
    grassImages.append(pygame.image.load('grass%s.png' % i))

world['grasses'] = [] # a sequence or mapping of Actors can be assigned to a world
for i in range(50):
    world['grasses'].append(pygstage.Actor(grassImages[random.randint(0, len(grassImages) - 1)],
                                           random.randint(0, 1000),
                                           random.randint(0, 1000)))

while True:
    pass # TODO - finish