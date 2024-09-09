from lib2to3.pgen2.tokenize import group

import pygame
from game import *  # Assuming you have a Game class in the 'game' module

def main():
    # Initialize Pygame
    pygame.init()

    # Set up the game window
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Your Pygame Title')

    # Create an instance of the Game class
    game = Game(screen)

    # Main game loop
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player = game.player_sprites.sprites()[0]
                    player.attack(player.attacks[0])

        # Update game state
        game.update()

        # Render the game
        game.render()

        # Update the display
        pygame.display.flip()

        # Control the frame rate (optional)
        pygame.time.Clock().tick(60)  # Adjust the argument to set the desired frames per second

    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
