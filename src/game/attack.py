import pygame

from .object import GameObject
from .enemy import Enemy

class Attack(GameObject):
    def __init__(self, x, y, width, height):
        self.__width = width
        self.__height = height
        super().__init__(x, y, width= self.__width, height=self.__height)
        self.__cooldown = 0
        self.__cooldown = 0
        self.__attacktime = 200
        self.__start_time = 0
        self.draw_image = False


    @property
    def  cooldown(self):
        return self.__cooldown

    @property
    def attacktime(self):
        return self.__attacktime

    @attacktime.setter
    def attacktime(self, value):
        self.attacktime = value

    def start_attack(self):
        self.__start_time = pygame.time.get_ticks()
        self.all_sprites.add(self)

    def update(self,screen):
        super().update()
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