import pygame
from textures import *
from grid import Grid
from obstacle import Player

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

# set up game board
grid = Grid(display, (510, 60), 100)
grid.addObstacle([1,1])
grid.addObstacle([6,8])
grid.addGoal([5,5])

# create player outside of grid b/c need manual control
player = Player(grid, [0,0])
grid.addObject(player)

prog_terminate = False
while not prog_terminate:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            prog_terminate = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player.moveLeft()
            if event.key == pygame.K_RIGHT:
                player.moveRight()
            if event.key == pygame.K_DOWN:
                player.moveDown()
            if event.key == pygame.K_UP:
                player.moveUp()

    # draw background
    display.blit(background, (0,0))
    grid.draw()

    # randomize obstacles

    pygame.display.update()
    clock.tick(60)