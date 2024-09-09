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

    def update(self, screen):
        super().update()
        # Add enemy-specific update logic here