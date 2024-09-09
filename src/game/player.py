import pygame
from .attack import Attack
from .object import GameObject
from ..utils import constants
class Player(GameObject):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        super().__init__(x, y, width=self.width, height=self.height)
        self.speed = 5
        self.attacks = [Attack(200, 200 , 64, 64)]
        self.draw_image = False
        self.direction = constants.NORTH


    def update(self, screen):
        super().update()


        #if keys[pygame.K_SPACE]:
         #   self.attack(self.attacks[0])

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            direction = constants.WEST
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            direction = constants.EAST
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            direction = constants.NORTH
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            direction = constants.SOUTH





    def collision_checks(self):
        if self.rect.x < 0 or self.rect.x > 800 or \
                self.rect.y < 0 or self.rect.y > 600:
            self.kill()  # Remove the player from the group
            print(f"Player died")

    def attack(self,attack):
        attack.start_attack()
        attack.follow_player(self)


