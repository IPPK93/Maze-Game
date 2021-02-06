import pygame
from maze_generation import *


class Field(): # Change to clear name
    def __init__(self, field_width, field_height, cell_size, padding_size, maze_width, maze_height, cell_color = Color.PINK.value, wall_color = Color.BROWN.value):
        self.maze = Maze(maze_height, maze_width)
        self.cell_color = cell_color
        self.wall_color = wall_color
        self.cell_size = cell_size
        self.padding = padding_size
        self.surface = pygame.Surface((field_width, field_height))  
        self.surface.fill(Color.GREY.value)

    def draw_maze(self):
        color = self.cell_color
        border_color = self.wall_color

        pygame.draw.rect(self.surface, border_color, (0, 0, self.padding, self.padding))
        pygame.draw.rect(self.surface, border_color, (self.padding, 0, self.maze.width * (self.cell_size + self.padding), self.padding))
        pygame.draw.rect(self.surface, border_color, (0, self.padding, self.padding, self.maze.height * (self.cell_size + self.padding)))

        for i in range(self.maze.height):
            for j in range(self.maze.width):
                cell = self.maze.grid[i][j]
                cell_x, cell_y = self.padding + (self.padding + self.cell_size) * j, self.padding + (self.padding + self.cell_size) * i
                pygame.draw.rect(self.surface, color, (cell_x, cell_y, self.cell_size, self.cell_size))

                if Direction.RIGHT in cell:
                    border_color = color
                pygame.draw.rect(self.surface, border_color, (cell_x + self.cell_size, cell_y, self.padding, self.cell_size))
                border_color = self.wall_color

                if Direction.DOWN in cell:
                    border_color = color
                pygame.draw.rect(self.surface, border_color, (cell_x, cell_y + self.cell_size, self.cell_size, self.padding))
                border_color = self.wall_color

                pygame.draw.rect(self.surface, border_color, (cell_x + self.cell_size, cell_y + self.cell_size, self.padding, self.padding))
        

        
