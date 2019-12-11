import pygame
from obstacle import Obstacle, Goal, Enemy, Player
import copy

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
        # draw black rectangles
        for i in range(0, self.grid_dimensions[0]):
            for ii in range(0, self.grid_dimensions[1]):
                pygame.draw.rect(self.surface, (0, 0, 0),
                                 (self.start_coordinates[0] + self.rect_size * i, self.start_coordinates[1] + self.rect_size * ii, self.rect_size, self.rect_size), 1)
        # draw objects
        for i in self.entity_list:
            i.draw()