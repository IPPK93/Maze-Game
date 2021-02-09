from maze_generation import *
import pygame

# field_pos = (field_x_pos, field_y_pos) - start position in field
# maze_pos = (maze_x_pos, maze_y_pos) - start position in maze

class Player(pygame.sprite.Sprite):
    def __init__(self, image, size, padding, field_pos, maze_pos):
        super(Player, self).__init__()
        self.surf = pygame.image.load(image).convert()
        self.surf = pygame.transform.scale(self.surf, (size, size))
        self.rect = self.surf.get_rect()
        self.rect = self.rect.move(*field_pos)
        self.step_len = size + padding
        self.x_pos, self.y_pos = maze_pos
        

    def move(self, direction, cell):
        if direction in cell:
            if direction == Direction.UP:
                self.rect = self.rect.move(0, -self.step_len)
                self.y_pos -= 1
            elif direction == Direction.DOWN:
                self.rect = self.rect.move(0, self.step_len)
                self.y_pos += 1
            elif direction == Direction.RIGHT:
                self.rect = self.rect.move(self.step_len, 0)
                self.x_pos += 1
            else:  # direction == Direction.LEFT
                self.rect = self.rect.move(-self.step_len, 0)
                self.x_pos -= 1
    
