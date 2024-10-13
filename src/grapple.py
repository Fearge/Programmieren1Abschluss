"""from pygame.math import Vector2 as vec
from constants import *
from src.base_sprite import AnimatedSprite
from src.spritesheet import Animation


class GrapplingHook(AnimatedSprite):
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.12, Animation.LOOP),
    }
    def __init__(self, screen, pos, *groups):
        super().__init__(screen, *groups)
        self.pos = vec(pos)
        self.vel = vec(0,0)  # Adjust speed as needed
        self.is_active = False
        self.is_attached = False

    def update(self):
        if not self.is_attached:
            self.pos += self.vel
            self.rect.center = self.pos"""

