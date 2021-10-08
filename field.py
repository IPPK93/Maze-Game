import pygame
from maze_generation import *
from colors import *
from player import *

# maze_params: (maze_width, maze_height)
# cell_params: (cell_size, cell_color, padding_size, wall_color)
# field_params: (field_width, field.height)

class Field(): # Change to clear name
    def __init__(self, field_params, cell_params, maze_params, floor_num, player):
        self.maze_width, self.maze_height = maze_params
        self.cur_maze = 0
        self.cell_size, self.cell_color, self.padding, self.wall_color = cell_params
        self.surface = pygame.Surface(field_params)
        self.floor_num = floor_num
        self.mazes = [Maze(self.maze_height, self.maze_width) for i in range(floor_num)]
        self.player = player
        self.portals = [(-1, -1) for i in range(floor_num)]

    def draw_maze(self):
        self.surface.fill(Color.GREY.value)
        color = self.cell_color
        border_color = self.wall_color

        pygame.draw.rect(self.surface, border_color, (0, 0, self.padding, self.padding))
        pygame.draw.rect(self.surface, border_color, (self.padding, 0, self.maze_width * (self.cell_size + self.padding), self.padding))
        pygame.draw.rect(self.surface, border_color, (0, self.padding, self.padding, self.maze_height * (self.cell_size + self.padding)))

        for i in range(self.maze_height):
            for j in range(self.maze_width):
                cell = self.mazes[self.cur_maze].grid[i][j]
                cell_x, cell_y = self.padding + (self.padding + self.cell_size) * j, self.padding + (self.padding + self.cell_size) * i
                pygame.draw.rect(self.surface, color, (cell_x, cell_y, self.cell_size, self.cell_size))

                if (j, i) in self.portals[self.cur_maze]:
                    pygame.draw.rect(self.surface, Color.LIGHT_BLUE.value, (cell_x, cell_y, self.cell_size, self.cell_size))
                
                if self.cur_maze != self.floor_num - 1 and (j, i) in self.portals[self.cur_maze + 1]:
                    pygame.draw.rect(self.surface, Color.DUSTY.value, (cell_x, cell_y, self.cell_size, self.cell_size))
                
                if Direction.RIGHT in cell:
                    border_color = color
                pygame.draw.rect(self.surface, border_color, (cell_x + self.cell_size, cell_y, self.padding, self.cell_size))
                border_color = self.wall_color

                if Direction.DOWN in cell:
                    border_color = color
                pygame.draw.rect(self.surface, border_color, (cell_x, cell_y + self.cell_size, self.cell_size, self.padding))
                border_color = self.wall_color

                pygame.draw.rect(self.surface, border_color, (cell_x + self.cell_size, cell_y + self.cell_size, self.padding, self.padding))
    
    
    def get_maze(self):
        return self.mazes[self.cur_maze]

    # probably need to change to bfs traversal
    def dfs(self, position, dist, cur_max, infinity):
        x_pos, y_pos = position
        if dist[y_pos][x_pos] > dist[cur_max[1]][cur_max[0]]:
            cur_max[0], cur_max[1] = position
        
        if Direction.UP in self.get_maze().grid[y_pos][x_pos] and dist[y_pos - 1][x_pos] == infinity:
            dist[y_pos - 1][x_pos] = dist[y_pos][x_pos] + 1 
            self.dfs((x_pos, y_pos - 1), dist, cur_max, infinity)
        if Direction.DOWN in self.get_maze().grid[y_pos][x_pos] and dist[y_pos + 1][x_pos] == infinity:
            dist[y_pos + 1][x_pos] = dist[y_pos][x_pos] + 1 
            self.dfs((x_pos, y_pos + 1), dist, cur_max, infinity)
        if Direction.LEFT in self.get_maze().grid[y_pos][x_pos] and dist[y_pos][x_pos - 1] == infinity:
            dist[y_pos][x_pos - 1] = dist[y_pos][x_pos] + 1 
            self.dfs((x_pos - 1, y_pos), dist, cur_max, infinity)
        if Direction.RIGHT in self.get_maze().grid[y_pos][x_pos] and dist[y_pos][x_pos + 1] == infinity:
            dist[y_pos][x_pos + 1] = dist[y_pos][x_pos] + 1 
            self.dfs((x_pos + 1, y_pos), dist, cur_max, infinity)
        

    def build_path(self, dist, s, t):
        path = [t]
        while t != s:
            x_pos, y_pos = t
            if Direction.UP in self.get_maze().grid[y_pos][x_pos] and dist[y_pos - 1][x_pos] == dist[y_pos][x_pos] - 1:
                t = (x_pos, y_pos - 1)
            if Direction.DOWN in self.get_maze().grid[y_pos][x_pos] and dist[y_pos + 1][x_pos] == dist[y_pos][x_pos] - 1:
                t = (x_pos, y_pos + 1)
            if Direction.LEFT in self.get_maze().grid[y_pos][x_pos] and dist[y_pos][x_pos - 1] == dist[y_pos][x_pos] - 1:
                t = (x_pos - 1, y_pos)
            if Direction.RIGHT in self.get_maze().grid[y_pos][x_pos] and dist[y_pos][x_pos + 1] == dist[y_pos][x_pos] - 1:
                t = (x_pos + 1, y_pos)
            
            path.append(t)
            
        path.reverse()
        return path
            
            
    
    # note: maze is basically a tree
    def find_longest_path(self, s, t = (-1, -1)):
        infinity = 1 << 31
        dist = [[infinity for i in range(self.maze_width)] for j in range(self.maze_height)]
        dist[s[1]][s[0]] = 0
        cur_max = [s[0], s[1]]
        self.dfs(s, dist, cur_max, infinity)
        return self.build_path(dist, s, tuple(cur_max) if t == (-1, -1) else t)
        
    
    def build_floor(self, s, t = (-1, -1)):
        if self.cur_maze == 0:
            longest_path = self.find_longest_path(s,t)
            t = longest_path[-1]
            self.portals[self.cur_maze] = (s, t)
            upfloor_in_point = longest_path[len(longest_path) // 3]
            upfloor_out_point = longest_path[2 * len(longest_path) // 3]
            self.cur_maze += 1
            self.build_floor(upfloor_in_point, upfloor_out_point)
            self.cur_maze -= 1
            
            
        elif self.cur_maze == self.floor_num - 1:
            self.portals[self.cur_maze] = (s, t) 
            return 

        else:
            longest_path = self.find_longest_path(s, t)
            self.portals[self.cur_maze] = (s, t)
            upfloor_in_point = longest_path[len(longest_path) // 3]
            upfloor_out_point = longest_path[2 * len(longest_path) // 3]
            self.cur_maze += 1
            self.build_floor(upfloor_in_point, upfloor_out_point)
            self.cur_maze -= 1
            
            
            
    def move_player(self, direction, cell):
        self.player.move(direction, cell)
        if self.cur_maze != 0 and (self.player.x_pos, self.player.y_pos) == self.portals[self.cur_maze][1]:
            self.cur_maze -= 1
            self.draw_maze()
        elif self.cur_maze != self.floor_num - 1 and (self.player.x_pos, self.player.y_pos) == self.portals[self.cur_maze + 1][0]:
            self.cur_maze += 1
            self.draw_maze()

            
            
            
            
    def add_player(player):
        players.append(player)
    
