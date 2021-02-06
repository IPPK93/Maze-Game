import pygame
from maze_generation import *
from player import *


MAZE_HEIGHT = 10
MAZE_WIDTH = 30

CELL_SIZE = 40
PADDING = 10

WALL_COLOR = (10, 10, 10)

WINDOW_HEIGHT = (PADDING + CELL_SIZE) * MAZE_HEIGHT + PADDING  # +PADDING for upper border
WINDOW_WIDTH = (PADDING + CELL_SIZE) * MAZE_WIDTH + PADDING    # +PADDING for left border

             
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
screen.fill(Color.GREY.value)
running = True

field = Field(WINDOW_WIDTH, WINDOW_HEIGHT, CELL_SIZE, PADDING, MAZE_WIDTH, MAZE_HEIGHT)
field.draw_maze()

player = Player("semicolon_three.png", CELL_SIZE, PADDING, PADDING, PADDING)
p_start_x, p_start_y = 0, 0

screen.blit(field.surface, (0, 0))
screen.blit(player.surf, player.rect)
pygame.display.flip()

while running:
    cur_cell = field.maze.grid[player.y_pos + p_start_y][player.x_pos + p_start_x]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.move(Direction.UP, cur_cell)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.move(Direction.DOWN, cur_cell)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.move(Direction.LEFT, cur_cell)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.move(Direction.RIGHT, cur_cell)

    screen.fill(Color.GREY.value)
    screen.blit(field.surface, (0, 0))
    screen.blit(player.surf, player.rect)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
