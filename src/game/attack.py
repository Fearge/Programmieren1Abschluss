import pygame

from .object import GameObject
from .enemy import Enemy

class Attack(GameObject):
    def __init__(self, x, y, width, height, player):
        self.__width = width
        self.__height = height
        self.__player = player
        super().__init__(x, y, width= self.__width, height=self.__height)
        self.__cooldown = 0
        self.__attacktime = 200
        self.__start_time = 0

    @property
    def attacktime(self):
        return self.__attacktime

    def start_attack(self):
        self.__start_time = pygame.time.get_ticks()
        self.all_sprites.add(self)

    def update(self,screen):
        super().update()
        self.follow_player(self.__player)
        if pygame.time.get_ticks() - self.__start_time > self.attacktime:
            self.kill()

    def follow_player(self, player):
        self.rect.x = player.rect.x + player.rect.width
        self.rect.y = player.rect.y

    def collision_checks(self):
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy) and self.rect.colliderect(sprite.rect):
                sprite.reduce_health(10)  # Reduce health by 10 or any other value
                self.kill()  # Remove the attack from the group