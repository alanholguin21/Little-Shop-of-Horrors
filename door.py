import pygame
class Door:
    def __init__(self, x, y):
        self.image = pygame.image.load("door.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.is_open = False

    def open(self):
        self.is_open = True

    def draw(self, surface, pos):
        if not self.is_open:
            surface.blit(self.image, pos)