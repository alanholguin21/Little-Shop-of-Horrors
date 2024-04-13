# hopping_monster.py
import pygame
from collections import deque
from settings import *

class JackInBox:
    def __init__(self, x, y, world_map):
        self.image = pygame.image.load("monster.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.world_map = world_map
        self.move_delay = MONSTER_DELAY - 2

    def update(self, target):
        if self.move_delay > 0:
            self.move_delay -= 1
        else:
            self.hop_towards_target(target)
            self.move_delay = MONSTER_DELAY - 2

    def hop_towards_target(self, target):
        target_pos = (target.rect.x // TILESIZE, target.rect.y // TILESIZE)
        start_pos = (self.rect.x // TILESIZE, self.rect.y // TILESIZE)

        path = self.bfs(start_pos, target_pos)
        if path:
            next_pos = path[1]  # Get the next position from the path
            self.rect.x = next_pos[0] * TILESIZE
            self.rect.y = next_pos[1] * TILESIZE

    def bfs(self, start, target):
        queue = deque([start])
        paths = {start: [start]}
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            current = queue.popleft()
            if current == target:
                return paths[current]

            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if self.can_move_to(neighbor[0] * TILESIZE, neighbor[1] * TILESIZE) and neighbor not in paths:
                    paths[neighbor] = paths[current] + [neighbor]
                    queue.append(neighbor)

        return []

    def can_move_to(self, x, y):
        if 0 <= x < len(self.world_map[0]) * TILESIZE and 0 <= y < len(self.world_map) * TILESIZE:
            map_x = x // TILESIZE
            map_y = y // TILESIZE
            return self.world_map[map_y][map_x] != "X"
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
