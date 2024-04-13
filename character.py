import pygame
from settings import *

class Character:
    def __init__(self, x, y, world_map):
        self.image = pygame.image.load("character.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.world_map = world_map
        self.move_delay = 0
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False
        self.inventory = []

    # Methods for continuous movement
    def move_left_continuous(self):
        self.moving_left = True

    def move_right_continuous(self):
        self.moving_right = True

    def move_up_continuous(self):
        self.moving_up = True

    def move_down_continuous(self):
        self.moving_down = True

    def stop_moving_left(self):
        self.moving_left = False

    def stop_moving_right(self):
        self.moving_right = False

    def stop_moving_up(self):
        self.moving_up = False

    def stop_moving_down(self):
        self.moving_down = False

    def update(self):
        # Update movement delay
        if self.move_delay > 0:
            self.move_delay -= 1

        # Continuous movement
        if self.move_delay <= 0:
            if self.moving_left:
                self.move_left()
                self.move_delay = MOVE_DELAY
            elif self.moving_right:
                self.move_right()
                self.move_delay = MOVE_DELAY
            elif self.moving_up:
                self.move_up()
                self.move_delay = MOVE_DELAY
            elif self.moving_down:
                self.move_down()
                self.move_delay = MOVE_DELAY

        # Check for key press to pick things up
        keys = pygame.key.get_pressed()
        if keys[pygame.K_z]:
            self.pick_up()

    def move_left(self):
        new_x = self.rect.x - TILESIZE
        if self.can_move_to(new_x, self.rect.y):
            self.rect.x = new_x

    def move_right(self):
        new_x = self.rect.x + TILESIZE
        if self.can_move_to(new_x, self.rect.y):
            self.rect.x = new_x

    def move_up(self):
        new_y = self.rect.y - TILESIZE
        if self.can_move_to(self.rect.x, new_y):
            self.rect.y = new_y

    def move_down(self):
        new_y = self.rect.y + TILESIZE
        if self.can_move_to(self.rect.x, new_y):
            self.rect.y = new_y

    def can_move_to(self, x, y):
        if 0 <= x < len(self.world_map[0]) * TILESIZE and 0 <= y < len(self.world_map) * TILESIZE:
            map_x = x // TILESIZE
            map_y = y // TILESIZE
            return self.world_map[map_y][map_x] != "X"
        return False
    
    def pick_up_key(self, key_rect):
        if self.rect.colliderect(key_rect):
            self.image = pygame.image.load("character_with_key.png").convert_alpha()
            return True
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
