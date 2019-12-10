import pygame
from textures import *
from grid import Grid

# 9x9 grid
# Bgnew.jpg -- background
# transparent tiles in grid
# randomize obstacles, depending on difficulty
# bear chases people

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('PENGUIN GAME')
clock = pygame.time.Clock()

grid = Grid(display, (510, 60), 100)
grid.addObstacle((1,1))

prog_terminate = False
while not prog_terminate:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            prog_terminate = True

    # draw background
    display.blit(background, (0,0))
    grid.draw()

    # randomize obstacles

    pygame.display.update()
    clock.tick(60)