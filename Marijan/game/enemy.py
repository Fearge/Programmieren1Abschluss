import pygame
from .object import GameObject

class Enemy(GameObject):
    def __init__(self, x, y, width, height, health=100):
        self.width = width
        self.height = height
        self.health = health
        super().__init__(x, y, width=self.width, height=self.height)

    def reduce_health(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.kill()  # Remove the enemy from the group
            print("Enemy died")

    def draw_health_bar(self, screen):
        # Calculate health bar dimensions
        bar_width = self.width
        bar_height = 5
        fill = (self.health / 100) * bar_width
        outline_rect = pygame.Rect(self.rect.x, self.rect.y + 10, bar_width, bar_height)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y + 10, fill, bar_height)

        # Draw health bar
        pygame.draw.rect(screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(screen, (0, 0, 0), outline_rect, 1)

    def update(self, screen):
        # Add enemy-specific update logic here
        super().update()
        self.draw_health_bar(screen)
