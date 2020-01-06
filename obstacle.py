import pygame
from textures import *
from threading import Thread
import time
import random

class Object:
    def __init__(self, grid, image, location):
        # basic grid object, no collision detection
        self.grid = grid
        self.image = image
        self.location = location # x, y array in units of boxes in grid. specify array not tuple


    def getLocation(self):
        return self.location

    def setLocation(self, coordinates):
        self.location = coordinates

    def moveLeft(self):
        if self.location[0] != 0:
            self.location[0] -= 1

    def moveRight(self):
        if self.location[0] != self.grid.grid_dimensions[0]-1:
            self.location[0] += 1

    def moveDown(self):
        if self.location[1] != self.grid.grid_dimensions[1]-1:
            self.location[1] += 1

    def moveUp(self):
        if self.location[1] != 0:
            self.location[1] -= 1

    def draw(self):
        resized_image = pygame.transform.scale(self.image, (self.grid.rect_size, self.grid.rect_size))
        self.grid.surface.blit(resized_image, self.grid.positionToCoordinates(self.location))


class Obstacle(Object):
    def __init__(self, grid, location):
        super().__init__(grid, icon_obstacle, location)

class Goal(Object):
    def __init__(self, grid, location):
        super().__init__(grid, icon_goal, location)
        self.collected = False

    def collect(self):
        self.collected = True

    def draw(self):
        if not self.collected:
            super().draw()
        else:
            pass

class Player(Object):
    def __init__(self, grid, location):
        super().__init__(grid, icon_player_front, location)
        self.alive = True

    def moveRight(self):
        super().moveRight()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                self.grid.goal.collect()
            elif self.grid.isAtEnemy(self):
                self.alive = False
            elif self.grid.isAtBaby(self) and (self.grid.goal.collected == True): # winning game, got to child
                pass
            elif self.grid.isAtBaby(self): # if not with goal, acts as barrier
                self.location[0] -= 1
            else:
                self.location[0] -= 1

    def moveLeft(self):
        super().moveLeft()

        # check is in an obstacle, move back
        # check if in goal, win game
        # check if in enemy, end game

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                self.grid.goal.collect()
            elif self.grid.isAtEnemy(self):
                self.alive = False
            elif self.grid.isAtBaby(self) and (self.grid.goal.collected == True):  # winning game, got to child
                pass
            elif self.grid.isAtBaby(self):  # if not with goal, acts as barrier
                self.location[0] += 1
            else:  # obstacle or something
                self.location[0] += 1

    def moveUp(self):
        super().moveUp()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                self.grid.goal.collect()
            elif self.grid.isAtEnemy(self):
                self.alive = False
            elif self.grid.isAtBaby(self) and (self.grid.goal.collected == True):  # winning game, got to child
                pass
            elif self.grid.isAtBaby(self):  # if not with goal, acts as barrier
                self.location[1] += 1
            else:
                self.location[1] += 1

    def moveDown(self):
        super().moveDown()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                self.grid.goal.collect()
            elif self.grid.isAtEnemy(self):
                self.alive = False
            elif self.grid.isAtBaby(self) and (self.grid.goal.collected == True):  # winning game, got to child
                pass
            elif self.grid.isAtBaby(self):  # if not with goal, acts as barrier
                self.location[1] -= 1
            else:
                self.location[1] -= 1

    def rotateRight(self):
        if self.image == icon_player_front:
            self.image = icon_player_right
        elif self.image == icon_player_right:
            self.image = icon_player_down
        elif self.image == icon_player_down:
            self.image = icon_player_left
        elif self.image == icon_player_left:
            self.image = icon_player_front

    def rotateLeft(self):
        if self.image == icon_player_front:
            self.image = icon_player_left
        elif self.image == icon_player_right:
            self.image = icon_player_front
        elif self.image == icon_player_down:
            self.image = icon_player_right
        elif self.image == icon_player_left:
            self.image = icon_player_down

    def moveForward(self):
        if self.image == icon_player_front:
            self.moveUp()
        elif self.image == icon_player_right:
            self.moveRight()
        elif self.image == icon_player_down:
            self.moveDown()
        elif self.image == icon_player_left:
            self.moveLeft()

    def moveBackward(self):
        if self.image == icon_player_front:
            self.moveDown()
        elif self.image == icon_player_right:
            self.moveLeft()
        elif self.image == icon_player_down:
            self.moveUp()
        elif self.image == icon_player_left:
            self.moveRight()


class Enemy(Object):
    def __init__(self, grid, location, difficulty):

        super().__init__(grid, icon_seal_blue, location)
        self.player = self.grid.player
        self.is_dead = False

        # enemy AI defaults
        self.delay_time = 5 # in seconds
        self.AI_hard_mode_toggle = False
        if difficulty > 3 or (difficulty < 0) or (difficulty == 1):
            pass # keep easiest settings
        elif difficulty == 2:
            # medium difficulty
            self.delay_time = 3
        elif difficulty == 3:
            # hardest difficulty
            self.delay_time = 2
            self.AI_hard_mode_toggle = True

    def run(self):
        Thread(target=self.main, args=()).start()
        return self

    def stop(self):
        self.is_dead = True

    def main(self):
        while not self.is_dead:
            time.sleep(self.delay_time)
            self.move()

    def move(self):
        # hunt player. implement difficulty settings

        # for difficultly, change timer.
        # easiest mode will move slowest + move one axis at a time AKA X or Y
        if self.AI_hard_mode_toggle:
            # most basic AI
            if (self.location[0] > self.player.location[0]):
                self.moveLeft()
            else:
                self.moveRight()

            if (self.location[1] > self.player.location[1]):
                self.moveUp()
            else:
                self.moveDown()
        # one axis at a time version
        else:
            X_axis = bool(random.getrandbits(1))
            if (X_axis):
                if (self.location[0] > self.player.location[0]):
                    self.moveLeft()
                else:
                    self.moveRight()
            else: # move y-axis
                if (self.location[1] > self.player.location[1]):
                    self.moveUp()
                else:
                    self.moveDown()

    def moveRight(self):
        super().moveRight()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                pass  # do nothing
            else:
                self.location[0] -= 1

    def moveLeft(self):
        super().moveLeft()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                pass  # do nothing
            else:  # obstacle or something, move back
                self.location[0] += 1

    def moveUp(self):
        super().moveUp()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                pass  # do nothing
            else:
                self.location[1] += 1

    def moveDown(self):
        super().moveDown()

        if self.grid.getAnyCollision(self):
            if self.grid.isAtGoal(self):
                pass  # do nothing
            else:
                self.location[1] -= 1

class Baby(Object):
    def __init__(self, grid, location):
        super().__init__(grid, icon_jewel, location)