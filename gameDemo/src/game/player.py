import pygame
from .object import GameObject
class Player(GameObject):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        super().__init__(x, y, width=self.width, height=self.height)
        self.speed = 5

    def update(self, screen):
        super().update()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            screen.blit(self.image, (100,200) )
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed


    def collision_checks(self):
        if self.rect.x < 0 or self.rect.x > 800 or \
                self.rect.y < 0 or self.rect.y > 600:
            self.kill()  # Remove the player from the group
            print(f"Player died")