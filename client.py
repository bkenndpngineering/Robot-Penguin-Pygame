import pygame
from textures import *
from grid import Grid
import math
import random
from clientPoll import gameClient
from button import Button
import time
from Delta_Testing_Testing.deltaArm import DeltaArm

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
    has_won = 2 # bool --> enum, 1,2,3
    # seperate has won, and prog_terminate
    # make enums -- win, loose, exit

    while not prog_terminate:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                prog_terminate = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    prog_terminate = True

        button_hidden.render(display)
        if button_hidden.isPressed():
            prog_terminate = True

        # test receive instructions
        instructions = client.getInstructions()
        if client.stopped:
            prog_terminate = True
            has_won = 3

        if grid.getCollision(grid.player, grid.enemy): # player dies # redundant. use player.isAlive ??
            prog_terminate = True
            has_won = 2

        if grid.getCollision(grid.player, grid.baby) and grid.goal.collected:
            prog_terminate = True
            has_won = 1

        waitTime = .25
        # character movement, networked
        if instructions != False:
            for instruction in instructions:
                if instruction == "rotateLeft":
                    grid.player.rotateLeft()
                    grid.draw()
                    pygame.display.update()

                    player_coord = grid.player.getLocation()  # top left corner
                    print(player_coord)

                    time.sleep(waitTime)  # replace with blocking move functions
                    if grid.player.won: break
                elif instruction == "rotateRight":
                    grid.player.rotateRight()
                    grid.draw()
                    pygame.display.update()

                    player_coord = grid.player.getLocation()  # top left corner
                    print(player_coord)

                    time.sleep(waitTime)
                    if grid.player.won: break
                elif instruction == "forwards":
                    grid.player.moveForward()
                    grid.draw()
                    pygame.display.update()

                    player_coord = grid.player.getLocation()  # top left corner
                    print(player_coord)

                    if grid.player.image == icon_player_front:
                        arm.moveToRelativeCoordinates((-14, -27, 0))
                    if grid.player.image == icon_player_down:
                        arm.moveToRelativeCoordinates((14, 27, 0))
                    if grid.player.image == icon_player_left:
                        arm.moveToRelativeCoordinates((27, -15, 0))
                    if grid.player.image == icon_player_right:
                        arm.moveToRelativeCoordinates((-27, 15, 0))

                    time.sleep(waitTime)
                    if grid.player.won: break
                elif instruction == "backwards":
                    grid.player.moveBackward()
                    grid.draw()
                    pygame.display.update()

                    player_coord = grid.player.getLocation()  # top left corner
                    print(player_coord)

                    time.sleep(waitTime)  # replace with blocking arm move function
                    if grid.player.won: break

            if not grid.player.won:
                client.makeReady()
            else:
                client.reset = True
                client.makeReady()

        if grid.player.won:
            prog_terminate = True
            has_won = 1

        # draw background
        display.blit(background, (0,0))
        grid.draw()

        pygame.display.update()
        clock.tick(60)

    grid.enemy.stop()
    return has_won


arm = DeltaArm()

## Grid coordinates
## (71, -183, -269.63) # TOP LEFT
## (-177, -44.5, -272.5) # TOP RIGHT
## (-32, 198, -272.69) # BOTTOM RIGHT
## (198, 61, -270.1) # BOTTOM LEFT
## num boxes height 9,
## box height = TLeft - BLeft = 244/9 = 27
## num boxes width 9
## width box = TLeft - TRight = 248/9 = 27.5
## 27 = BOX DIMENSIONS
## table height around 270
'''
Movement:
1 space right = +(-27, 15, 0)
1 space left = +(27, -15, 0)
1 space up = +(-14, -27, 0)
1 space down = +(14 27, 0)
'''


# if X, Y does not work
# got to coordinates then lower Z from a larger height

if __name__ == '__main__':
    # main loop 
    # get difficulty from surface tablet

    if arm.initialize():
        ready = True
    else:
        ready = False

    # move into idle position
    #arm.moveToCoordinates(71, -183, -240)
    x_val = 71
    y_val = -183
    for i in range(0,9):
        prex = x_val
        prey = y_val
        print(str(i))
        for l in range(0,9):
            arm.moveToCoordinates(x_val, y_val, -240)
            x_val -= 27
            y_val += 15
        x_val = prex + 14
        y_val = prey + 27
        

    while 1:
        instructions = []
        while not instructions:
            instructions = client.getInstructions()

        for instruction in instructions:
            if instruction == "1":
                diff = 1
            elif instruction == "2":
                diff = 2
            elif instruction == "3":
                diff = 3
            else:
                diff = 1
        client.makeReady()
        state = run_game(diff)
        if state == 1:  # wins the game
            # send reset signal to server -- > go to start screen
            end_effect(win_screen)
            client.restart = True
            client.makeReady()
        elif state == 2:  # looses the game
            # send reset signal to server -- > go to start screen
            end_effect(loose_screen)
            client.restart = True
            client.makeReady()
        elif state == 3:
            # kill the whole thang
            break

# still needs to be able to exit
# server/client
# send reset command from client --> server
# server --> start screen
# client reset, wait for difficulty

pygame.quit()
client.stop()

arm.shutdown()
