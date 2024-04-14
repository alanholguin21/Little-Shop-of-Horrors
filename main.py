import pygame
import sys
from settings import *
from character import Character
from plant import Plant
from jackInBox import JackInBox
from door import Door
from key import Key
from camera import Camera

class Game:
    def __init__(self):
        # Initialize Pygame and create a window
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        pygame.display.set_caption('Little Shop of Horror')
        self.clock = pygame.time.Clock()

        # Load and scale tile image for the maze and door
        self.tile_image = pygame.image.load("tile.png").convert_alpha()
        self.floor_image = pygame.image.load("floor.png").convert_alpha()
        self.tile_image = pygame.transform.scale(self.tile_image, (TILESIZE, TILESIZE))
        self.floor_image = pygame.transform.scale(self.floor_image, (TILESIZE, TILESIZE))

        self.door_image = pygame.image.load("door.png").convert_alpha()
        self.door_image = pygame.transform.scale(self.door_image, (TILESIZE, TILESIZE))

        # Initialize game entities
        self.character = Character(50, 50, WORLD_MAP)
        self.plant = Plant(300, 300, WORLD_MAP)
        self.monster = JackInBox(500, 500, WORLD_MAP)  # Adjusted for diversity in positioning
        self.key = Key(200, 200)  # Initialize the key object
        self.door = Door(700, 500)
        self.camera = Camera(32, 12)


    def draw_maze(self):
        
    
        for y, row in enumerate(WORLD_MAP):
            for x, char in enumerate(row):
                if char == "X":
                    rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    self.screen.blit(self.tile_image, self.camera.apply(rect))
                elif char == " ":
                    rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    self.screen.blit(self.floor_image, self.camera.apply(rect))
                elif char == "Y":
                    # Draw the door at the position of "Y"
                    rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    self.screen.blit(self.door_image, self.camera.apply(rect))
                    # Update door position
                    self.door.rect = rect

        # Draw the key if it has not been picked up
        if self.key.is_visible:
            self.key.draw(self.screen, self.camera.apply(self.key.rect))

    def run(self):
        caught = False  # Variable to track if the character is caught
        # Main game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.character.move_left_continuous()
                    elif event.key == pygame.K_RIGHT:
                        self.character.move_right_continuous()
                    elif event.key == pygame.K_UP:
                        self.character.move_up_continuous()
                    elif event.key == pygame.K_DOWN:
                        self.character.move_down_continuous()
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.character.stop_moving_left()
                    elif event.key == pygame.K_RIGHT:
                        self.character.stop_moving_right()
                    elif event.key == pygame.K_UP:
                        self.character.stop_moving_up()
                    elif event.key == pygame.K_DOWN:
                        self.character.stop_moving_down()

            # Update game state and redraw
            self.character.update()
            self.plant.update(self.character)
            self.monster.update(self.character)

            # Check if the character picks up the key
            if self.character.pick_up_key(self.key.rect):
                self.key.is_visible = False  # Set key visibility to False if picked up

            # Check if the character reaches the door with the key
            if not self.key.is_visible and self.character.rect.colliderect(self.door.rect):
                self.screen.fill((0, 0, 0))  # Clear screen
                ending_image = pygame.image.load("ending.png").convert_alpha()
                ending_image = pygame.transform.scale(ending_image, (ending_image.get_width() // 2, ending_image.get_height() // 2))
                self.screen.blit(ending_image, (0, 0))
                pygame.display.update()
                pygame.time.wait(9000)
                pygame.quit()
                sys.exit()

            # Check if the character collides with the monster
            if pygame.sprite.collide_rect(self.character, self.monster):
                self.screen.fill((0, 0, 0))  # Clear screen
                # Display ending image
                ending_image = pygame.image.load("death.png").convert_alpha()
                # Shrink the image to half its original size
                ending_image = pygame.transform.scale(ending_image, (ending_image.get_width() // 2, ending_image.get_height() // 2))
                self.screen.blit(ending_image, (0, 0))
                pygame.display.update()
                # Wait for a moment before closing the game
                pygame.time.wait(9000)
                pygame.quit()
                sys.exit()

            self.camera.update(self.character.rect)
            self.screen.fill((0, 0, 0))  # Clear screen
            self.draw_maze()  # Draw maze background
            self.character.draw(self.screen,  self.camera.apply(self.character.rect))  # Draw the character
            self.plant.draw(self.screen,  self.camera.apply(self.plant.rect))  # Draw the plant
            self.monster.draw(self.screen,  self.camera.apply(self.monster.rect))  # Draw the monster
            pygame.display.update()  # Update the display
            self.clock.tick(FPS)  # Maintain the specified frames per second


if __name__ == '__main__':
    game = Game()
    game.run()
