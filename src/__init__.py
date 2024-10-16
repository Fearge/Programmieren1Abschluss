import pygame as pg
class Sprite(pg.sprite.Sprite):
    def __init__(self,*groups):
        super().__init__(*groups)
        pg.sprite_type = ''