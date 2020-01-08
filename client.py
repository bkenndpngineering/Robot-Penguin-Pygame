import pygame
from textures import *
from grid import Grid
import math
import random
from clientPoll import gameClient
from button import Button
import time
#from Delta_Arm_Testing.deltaArm import DeltaArm

# TODO
# get movement
# remote shutdown
# client--> server status, allow for next packet

pygame.init()
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption('PENGUIN GAME CLIENT')
clock = pygame.time.Clock()

client = gameClient().run()

def end_effect(image, delay_time=35):
    image_height = 100
    image_width = 100 
    image = pygame.transform.scale(image, (image_width, image_height))
    cols = math.ceil(SCREEN_WIDTH / image_width)
    rows = math.ceil(SCREEN_HEIGHT / image_height)
    for i in range(0, cols):
        for ii in range(0, rows):
            display.blit(image, (i * image_width, ii * image_height))
            pygame.display.update()
            pygame.time.wait(delay_time)

def run_game(difficulty=1):

    # hidden escape button
    # bottom right
    button_height = 50
    button_width = 100
    button_hidden = Button("", (SCREEN_WIDTH - button_width, SCREEN_HEIGHT - button_height, button_width, button_height), inact_color=(0,0,0), act_color=(0,0,0)) # act colors must match background color to be "hidden"

    # set up game board
    grid = Grid(display, (510, 60), 100, [9, 9])
    # end goal
    grid.addGoal([8, 8]) # place goal and player at opposite ends
    # player before enemy
    grid.addPlayer([0, 0])
    grid.addBaby(grid.getUnusedCoordinates()) # randomize baby/jewel

    if difficulty > 3 or (difficulty < 0) or (difficulty == 1):
        difficulty = 1 # just in case
        # easiest setting
        # between 5 and 10 obstacles
        num_obstacles = random.randint(5, 10) # randint returns including the ends of the range
        for i in range(0, num_obstacles-1):
            grid.addObstacle(grid.getUnusedCoordinates(False)) # do not spawn obstacle on border of grid, blocks goal sometimes
    elif difficulty == 2:
        # medium difficulty
        # between 7 and 13 obstacles
        num_obstacles = random.randint(7, 13)
        for i in range(0, num_obstacles - 1):
            grid.addObstacle(grid.getUnusedCoordinates(False))
    elif difficulty == 3:
        # hardest difficulty
        # between 9 and 15 obstacles
        num_obstacles = random.randint(9, 15)
        for i in range(0, num_obstacles - 1):
            grid.addObstacle(grid.getUnusedCoordinates(False))

    # enemy after player
    grid.addEnemy(grid.getUnusedCoordinates(), difficulty)

    prog_terminate = False
    has_won = False
    while not prog_terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog_terminate = True

        button_hidden.render(display)
        if button_hidden.isPressed():
            prog_terminate = True

        # test receive instructions
        instructions = client.getInstructions()
        if client.stopped:
            prog_terminate = True

        if grid.getCollision(grid.player, grid.enemy): # player dies
            prog_terminate = True
            has_won = False

        if grid.getCollision(grid.player, grid.baby) and grid.goal.collected:
            prog_terminate = True
            has_won = True

        waitTime = .25
        # character movement, networked
        if instructions != False:
            for instruction in instructions:
                if instruction == "rotateLeft":
                    grid.player.rotateLeft()
                    grid.draw()
                    time.sleep(waitTime)
                elif instruction == "rotateRight":
                    grid.player.rotateRight()
                    grid.draw()
                    time.sleep(waitTime)
                elif instruction == "forwards":
                    grid.player.moveForward()
                    grid.draw()
                    time.sleep(waitTime)
                elif instruction == "backwards":
                    grid.player.moveBackward()
                    grid.draw()
                    time.sleep(waitTime)

            client.makeReady()


        # draw background
        display.blit(background, (0,0))
        grid.draw()

        pygame.display.update()
        clock.tick(60)

    grid.enemy.stop()
    return has_won

if __name__ == '__main__':
    # main loop 
    # get difficulty from surface tablet
    instructions = []
    while not instructions:
        instructions = client.getInstructions()
        pass
    for instruction in instructions:
        if instruction == "1":
            diff = 1
        if instruction == "2":
            diff = 2
        if instruction == "3":
            diff = 3
    client.makeReady()
    if run_game(diff) == True:  # wins the game
        end_effect(win_screen)
    else: # looses the game
        end_effect(loose_screen)

pygame.quit()
client.stop()
