import pygame
class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, rect):
        # Now directly takes a pygame.Rect and adjusts it based on the camera's position
        return rect.move(-self.camera.x, -self.camera.y)

    def update(self, target):
        x = -target.rect.centerx + int(self.width / 2)
        y = -target.rect.centery + int(self.height / 2)

        # Limit scrolling to map size
        x = min(0, x)  # Left
        x = max(-(self.camera.width - self.width), x)  # Right
        y = min(0, y)  # Top
        y = max(-(self.camera.height - self.height), y)  # Bottom

        self.camera = pygame.Rect(x, y, self.camera.width, self.camera.height)
