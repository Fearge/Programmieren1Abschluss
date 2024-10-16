import pygame as pg
from pygame.math import Vector2 as vec
from src.constants import HIT_PARTICLES
from src.spritesheet import Animation


class GrapplingHook(pg.sprite.Sprite):
    def __init__(self, pos, *groups):
        super().__init__(groups)
        self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.is_shooting = False
        self.is_attached = False
        self.path = []
        self.sprite_type = 'grappling_hook'
        self.image = pg.Surface((10, 10))
        self.rect = pg.Rect(pos, (10, 10))  # Example size, adjust as needed
        self.rect.midbottom = self.pos

    def draw(self, surface):
        if len(self.path) > 0:
            pg.draw.lines(surface, (0, 0, 0), False, self.path, 2)  # Example color, adjust as needed

    def update(self):
        self.pos += self.vel
        if self.is_shooting and not self.is_attached:
            self.path.append(self.pos)
        self.rect.midbottom = self.pos