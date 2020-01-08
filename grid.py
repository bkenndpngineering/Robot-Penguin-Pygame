import pygame
from obstacle import Obstacle, Goal, Enemy, Player, Baby
from textures import *
import copy
import random
from textures import *

class Grid():
    def __init__(self, surface, start_coordinates, rect_size, grid_dimensions=[9, 9]):
        self.start_coordinates = start_coordinates
        self.rect_size = rect_size
        self.entity_list = []
        self.surface = surface
        self.grid_dimensions = grid_dimensions
        self.goal = None
        self.enemy = None
        self.player = None
        self.baby = None

    def addBaby(self, location):
        if self.baby == None:  # only add one player
            self.baby = Baby(self, location)
            self.addObject(self.baby)

    def addPlayer(self, location):
        if self.player == None: # only add one player
            self.player = Player(self, location)
            self.addObject(self.player)

    def addObject(self, object):
        self.entity_list.append(object)

    def addObstacle(self, location):
        self.addObject(Obstacle(self, location))

    def addGoal(self, location):
        if self.goal == None: # only add one goal
            self.goal = Goal(self, location)
            self.addObject(self.goal)

    def addEnemy(self, location, difficulty):
        if self.enemy == None: # only add one enemy
            self.enemy = Enemy(self, location, 2).run()
            self.addObject(self.enemy)

    def isAtGoal(self, object1):
        if self.goal != None:
            return self.getCollision(object1, self.goal)

    def isAtEnemy(self, object1):
        if self.enemy != None:
            return self.getCollision(object1, self.enemy)

    def isAtBaby(self, object1):
        if self.baby != None:
            return self.getCollision(object1, self.baby)

    def getCollision(self, object1, object2):
        if (object1.location == object2.location):
            return True
        else:
            return False

    def getAnyCollision(self, object1):
        is_collided = False
        for i in self.entity_list:
            if i == object1:
                pass
            elif self.getCollision(object1, i):
                is_collided = True
                break
        return is_collided

    def positionToCoordinates(self, position):
        # returns top left corner of rect
        # useful for drawing functions
        x_offset = self.start_coordinates[0]
        y_offset = self.start_coordinates[1]
        x_grid_location = position[0]
        y_grid_location = position[1]
        x_coordinate = x_offset + x_grid_location*self.rect_size
        y_coordinate = y_offset + y_grid_location*self.rect_size

        return (x_coordinate, y_coordinate)

    def draw(self):
        self.surface.blit(background, (0, 0))

        # draw black rectangles
        for i in range(0, self.grid_dimensions[0]):
            for ii in range(0, self.grid_dimensions[1]):
                pygame.draw.rect(self.surface, (0, 0, 0),
                                 (self.start_coordinates[0] + self.rect_size * i, self.start_coordinates[1] + self.rect_size * ii, self.rect_size, self.rect_size), 1)
        # draw objects
        for i in self.entity_list:
            i.draw()

        # draw player again so it is on top at all times
        self.player.draw()

    def getUnusedCoordinates(self, border_OK=True):
        # coordinates start at 0, go to 8, in the case of a 9x9 grid
        if border_OK:
            taken_coordinates = []
            for entity in self.entity_list:
                taken_coordinates.append(entity.location)

            x = random.randint(0, self.grid_dimensions[0]-1)
            y = random.randint(0, self.grid_dimensions[1]-1)
            while ([x, y] in taken_coordinates):
                x = random.randint(0, self.grid_dimensions[0]-1)
                y = random.randint(0, self.grid_dimensions[1]-1)

            return [x, y]

        else:
            taken_coordinates = []
            for entity in self.entity_list:
                taken_coordinates.append(entity.location)

            x = random.randint(1, self.grid_dimensions[0] - 2)
            y = random.randint(1, self.grid_dimensions[1] - 2)
            while ([x, y] in taken_coordinates):
                x = random.randint(1, self.grid_dimensions[0] - 2)
                y = random.randint(1, self.grid_dimensions[1] - 2)

            return [x, y]
