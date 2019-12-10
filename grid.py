import pygame
from obstacle import Object

class Grid():
    def __init__(self, surface, start_coordinates, rect_size, grid_dimensions=[9, 9]):
        self.start_coordinates = start_coordinates
        self.rect_size = rect_size
        self.entity_list = []
        self.surface = surface
        self.grid_dimensions = grid_dimensions

    def addObject(self, image, location):
        self.entity_list.append(Object(self, self.surface, image, location))

    def positionToCoordinates(self, position):
        # returns top left corner of rect
        # useful for drawing functions
        x_offset = self.start_coordinates[0]
        y_offset = self.start_coordinates[1]
        x_grid_location = position[0]
        y_grid_location = position[1]
        x_coordinate = x_offset + x_grid_location*self.rect_size
        y_coordinate = y_offset - y_grid_location*self.rect_size

        return (x_coordinate, y_coordinate)

    def draw(self):
        # draw black rectangles
        for i in range(0, self.grid_dimensions[0]):
            for ii in range(0, self.grid_dimensions[1]):
                pygame.draw.rect(self.surface, (0, 0, 0),
                                 (self.start_coordinates[0] + self.rect_size * i, self.start_coordinates[1] + self.rect_size * ii, self.rect_size, self.rect_size), 1)
        # draw objects
        for i in self.entity_list:
            i.draw((self.rect_size, self.rect_size))