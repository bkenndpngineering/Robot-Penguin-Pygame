import pygame

class Object:
    def __init__(self, surface, image, location):
        self.surface = surface
        self.image = image
        self.location = location # x, y array in units of boxes in grid

    def getLocation(self):
        return self.location

    def setLocation(self, coordinates):
        self.location = coordinates

    def moveLeft(self):
        if self.location[0] != 0:
            self.location[0] -= 1

    def moveRight(self):
        if self.location[0] != 9:
            self.location[0] += 1

    def moveUp(self):
        if self.location[1] != 9:
            self.location[1] += 1

    def moveDown(self):
        if self.location[1] != 0:
            self.location[0] -= 1

    def draw(self, ):
        self.surface.blit(self.image, ())