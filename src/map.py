import pygame as pg
from pytmx.util_pygame import load_pygame


class TiledMap:
    def __init__(self, filename):
        self.tmx_data = load_pygame(filename)
        self.width = self.tmx_data.width*self.tmx_data.tilewidth
        self.height = self.tmx_data.height*self.tmx_data.tileheight

    def render(self, surface):
        for layer in self.tmx_data.visible_layers:
            if hasattr(layer, 'data'):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile:
                        surface.blit(tile, (x*self.tmx_data.tilewidth, y*self.tmx_data.tileheight))

    def make_map(self):
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)
        return temp_surface, temp_surface.get_rect()

class Camera:
    def __init__(self, game, width, height):
        self.game = game
        self.width = width
        self.height = height
        self.camera = pg.Rect(0, 0, width, height)
        self.smoothing_factor = 0.1

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)
    
    def draw(self, surface, group):
        for sprite in group:
            surface.blit(sprite.image, self.apply(sprite))

    # interpolation for camera smoothing
    def smooth(self, start, end, factor):
        return start + factor * (end - start)

    def update(self, target):
        target_x = max(-self.width + self.game.width, min(0, int(self.game.width / 2) - target.rect.centerx))
        target_y = max(-self.height + self.game.height, min(0, int(self.game.height / 2) - target.rect.centery))

        # Smoothly interpolate the camera position
        self.camera.x = self.smooth(self.camera.x, target_x, self.smoothing_factor)
        self.camera.y = self.smooth(self.camera.y, target_y, self.smoothing_factor)
