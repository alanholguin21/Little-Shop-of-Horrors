import pygame
class Camera:
    def __init__(self, camera_width, camera_height):
        self.camera_rect = pygame.Rect(0, 0, camera_width, camera_height)
        self.width = camera_width
        self.height = camera_height

    def apply(self, rect):
        # This method shifts the rect based on the camera's position
        return rect.move(self.camera_rect.topleft)

    def update(self, target_rect):
        # This method centers the target in the middle of the camera view
        x = -target_rect.centerx + self.width // 2 + 370
        y = -target_rect.centery + self.height // 2 + 300

        # Update the camera's position
        self.camera_rect = pygame.Rect(x, y, self.width, self.height)
