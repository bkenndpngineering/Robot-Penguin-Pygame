import pygame

class Object:
    def __init__(self, grid, surface, image, location):
        self.surface = surface
        self.grid = grid
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

    def draw(self, resize_dimensions=-1):
        if resize_dimensions == -1:
            resized_image = self.image
        else:
            resized_image = pygame.transform.scale(self.image, resize_dimensions)
        self.surface.blit(resized_image, self.grid.positionToCoordinates(self.location))