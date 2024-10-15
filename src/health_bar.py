import pygame as pg
class HealthBar:
    def __init__(self, x, y, width, height, max_health):
        self.rect = pg.Rect(x, y, width, height)
        self.max_health = max_health
        self.current_health = 0

    def update(self, current_health):
        self.current_health = current_health

    def draw(self, surface, camera):
        # Calculate the width of the health bar based on current health
        health_ratio = self.current_health / self.max_health
        health_width = self.rect.width * health_ratio

        # Adjust the position of the health bar based on the camera
        if camera:
            self.rect.x += camera.rect.x
            self.rect.y += camera.rect.y

        # Draw the background of the health bar
        pg.draw.rect(surface, (255, 0, 0), self.rect)  # Red background
        # Draw the current health
        pg.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y, health_width, self.rect.height))  # Green health

