import pygame
import sys
from settings import *

class StartPage:
    def __init__(self):
        # Initialize Pygame and create a window
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Little Shop of Horror')
        self.clock = pygame.time.Clock()

        # Load and scale start page image
        self.start_page_image = pygame.image.load("start_page.png").convert_alpha()
        self.start_page_image = pygame.transform.scale(self.start_page_image, (800, 600))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Start the game when spacebar is pressed
                        return

            self.screen.blit(self.start_page_image, (0, 0))  # Display the start page image
            pygame.display.update()
            self.clock.tick(FPS)