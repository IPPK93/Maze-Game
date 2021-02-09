import pygame
from maze_generation import *
from player import *
from colors import *
from field import *


MAZE_H = 10
MAZE_W = 30

CELL_SIZE = 40
PADDING = 10

WALL_COLOR = (10, 10, 10)

WIN_H = (PADDING + CELL_SIZE) * MAZE_H + PADDING  # +PADDING for upper border
WIN_W = (PADDING + CELL_SIZE) * MAZE_W + PADDING    # +PADDING for left border

FLOOR_NUM = 3
             
pygame.init()
screen = pygame.display.set_mode((WIN_W, WIN_H))
screen.fill(Color.GREY.value)
running = True


player = Player("semicolon_three.png", CELL_SIZE, PADDING, (PADDING, PADDING), (0, 0))
field = Field((WIN_W, WIN_H), (CELL_SIZE, Color.PINK.value, PADDING, Color.BLACK.value), (MAZE_W, MAZE_H), FLOOR_NUM, player)
field.build_floor((field.player.x_pos, field.player.y_pos))
print("BUILT")
field.draw_maze()


screen.blit(field.surface, (0, 0))
screen.blit(field.player.surf, field.player.rect)
pygame.display.flip()

while running:
    cur_cell = field.get_maze().grid[player.y_pos][player.x_pos]
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                field.move_player(Direction.UP, cur_cell)
            elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                field.move_player(Direction.DOWN, cur_cell)
            elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                field.move_player(Direction.LEFT, cur_cell)
            elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                field.move_player(Direction.RIGHT, cur_cell)

    screen.fill(Color.GREY.value)
    screen.blit(field.surface, (0, 0))
    screen.blit(field.player.surf, field.player.rect)
    pygame.display.flip()

pygame.display.quit()
pygame.quit()
