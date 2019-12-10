import pygame

class Grid():
    def __init__(self, surface, start_coordinates, grid_size):
        self.start_coordinates = start_coordinates
        self.grid_size = grid_size
        self.entity_list = []
        self.surface = surface

    def draw(self):
        for i in range(0, 9):
            for ii in range(0, 9):
                pygame.draw.rect(self.surface, (0, 0, 0),
                                 (self.start_coordinates[0] + self.grid_size * i, self.start_coordinates[1] + self.grid_size * ii, self.grid_size, self.grid_size), 1)