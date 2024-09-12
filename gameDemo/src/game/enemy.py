import random
from .object import GameObject
from ..graphics.animator import Animator

class Enemy(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__(x=x, y=y, width=width, height=height)
        self.all_enemies.add(self)
        self.image.fill((255, 0, 0))  # Red color
        self.animator = Animator(animation_filename='bullet.png',
                                 parent=self,
                                 animation_frames=6,
                                 animation_speed=120)
        self.speed = 2

    def update(self, screen):
        super().update()
        self.rect.x += self.speed #+ random.randint(-2, 3)
        #self.rect.y += self.speed #+ random.randint(-3, 3)
        # Check if the enemy is out of scope
        if self.rect.x < 0 or self.rect.x > screen.get_size()[0] or \
                self.rect.y < 0 or self.rect.y > screen.get_size()[1]:
            self.kill()  # Remove the player from the group
            print(f"{self} was killed")

