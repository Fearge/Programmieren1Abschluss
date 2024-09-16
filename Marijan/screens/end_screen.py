import pygame

class EndScreen:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.restart_text = self.font.render("Press R to restart", True, (0, 0, 0))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            return "start"  # Transition to the start screen

    def render(self, score):
        self.screen.fill((255, 255, 255))  # White background
        self.end_text = self.font.render(f"Game Over ({score} Points)", True, (0, 0, 0))
        self.screen.blit(self.end_text, (200, 200))
        self.screen.blit(self.restart_text, (200, 300))