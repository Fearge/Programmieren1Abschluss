from game import *
from graphics.render import Renderer
from screens.start_screen import StartScreen
from screens.end_screen import EndScreen

def main():
    # Global Settings
    FPS = 60
    WIDTH, HEIGHT = 800, 600

    clock = pygame.time.Clock()
    # Initialize Pygame
    pygame.init()

    # Fonts
    font = pygame.font.Font(None, 36)

    # Game variables
    score = 0

    # Set up the game window
    screen_width, screen_height = WIDTH, HEIGHT
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Programmieren GameDemo')

    renderer = Renderer(screen)
    # Create an instance of the Game class
    start_screen = StartScreen(screen)
    end_screen = EndScreen(screen)
    game = Game(screen)

    current_screen = "start"  # Initial screen

    # Main game loop
    running = True
    while running:
        # Check for pygame.EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Check for game.STATE
            elif current_screen == "start":
                result = start_screen.handle_events(event)
                if result == "game":
                    current_screen = "game"
            elif current_screen == "game":
                result = game.handle_events(event)
                if result == "end":
                    current_screen = "end"
            elif current_screen == "end":
                result = end_screen.handle_events(event)
                if result == "start":
                    current_screen = "start"

        # Check which screen to render
        if current_screen == "start":
            start_screen.render()
        elif current_screen == "game":
            game.update()
            game.render(renderer)
        elif current_screen == "end":
            end_screen.render(score)
        # Show all changes (Flip the page)
        pygame.display.flip()
        # Set Framerate
        clock.tick(FPS)


    # Quit Pygame
    pygame.quit()

if __name__ == "__main__":
    main()
