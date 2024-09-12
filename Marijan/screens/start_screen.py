# screens/start_screen.py
import pygame

class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.title_text = self.font.render("Programmieren GameDemo WS23", True, (0, 0, 0))
        self.start_text = self.font.render("Press SPACE to start", True, (0, 0, 0))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            return "game"  # Transition to the game screen

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        self.screen.blit(self.title_text, (200, 200))
        self.screen.blit(self.start_text, (200, 300))
