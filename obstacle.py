import pygame
from textures import *

class Object:
    def __init__(self, grid, image, location):
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

class Player(Object):
    def __init__(self, grid, location):
        super().__init__(grid, icon_jewel, location)