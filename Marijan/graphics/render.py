import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen

    def render_background(self):
        self.screen.fill((100, 200, 255))  # White background

    def render_sprites(self, sprite_group):
        sprite_group.draw(self.screen)

    def update_display(self):
        pygame.display.flip()
