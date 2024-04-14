import pygame
import sys
from settings import *
from character import Character
from plant import Plant
from jackInBox import JackInBox
from door import Door
from key import Key

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

    def draw_maze(self):
        # Draw the tiles for the maze
        for y, row in enumerate(WORLD_MAP):
            for x, char in enumerate(row):
                if char == "X":
                    rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    self.screen.blit(self.tile_image, rect)
                elif char == " ":
                    rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    self.screen.blit(self.floor_image, rect)
                elif char == "Y":
                    rect = pygame.Rect(x * TILESIZE, y * TILESIZE, TILESIZE, TILESIZE)
                    self.screen.blit(self.door_image, rect)

        # Draw the key if it has not been picked up
        if self.key.is_visible:
            self.key.draw(self.screen)

    def run(self):
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

            # Check if the character reaches the door
            if self.character.rect.collidepoint(*self.get_door_position()):
                print("Congratulations! You escaped!")
                pygame.quit()
                sys.exit()

            self.screen.fill((0, 0, 0))  # Clear screen
            self.draw_maze()  # Draw maze background
            self.character.draw(self.screen)  # Draw the character
            self.plant.draw(self.screen)  # Draw the plant
            self.monster.draw(self.screen)  # Draw the monster
            pygame.display.update()  # Update the display
            self.clock.tick(FPS)  # Maintain the specified frames per second

    def get_door_position(self):
        # Find the position of the door in the map
        for y, row in enumerate(WORLD_MAP):
            for x, char in enumerate(row):
                if char == "Y":
                    return x * TILESIZE, y * TILESIZE

        # If door position not found, return None
        return None


if __name__ == '__main__':
    game = Game()
    game.run()
