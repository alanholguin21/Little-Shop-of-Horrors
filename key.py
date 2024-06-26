import pygame
from settings import *

class Key:
    def __init__(self, x, y):
        self.image = pygame.image.load("key.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_visible = True  # Add is_visible attribute and initialize it as True
 
    def draw(self, surface, pos):
        if self.is_visible:
            surface.blit(self.image, pos)