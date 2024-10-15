import pygame as pg
import sys


from os import path

from src.constants import TICKS
from src.screen import PauseScreen


class Game:
    def __init__(self, title, dim):
        # initialize pygame
        pg.init()
        pg.mixer.init()
        pg.display.set_caption(title)

        self.width = dim[0]
        self.height = dim[1]

        # set screen
        self.screen = None
        self.surface = pg.display.set_mode(dim)
        #self.surface = pg.display.set_mode(dim, pg.FULLSCREEN)
        self.clock = pg.time.Clock()

        # current directory
        self.dir = path.dirname(__file__)

    def set_screen(self, scr):
        # delete existing
        if self.screen is not None:
            del self.screen
            self.screen = None

        self.screen = scr

        # show new screen
        if self.screen is not None:
            self.screen.run()

    def save_state(self):
        self.saved_state = {
            'player': {
                'pos': self.screen.player.pos,
                'vel': self.screen.player.vel,
                'health': self.screen.player.health,
            },
            'enemies': [
                {
                    'pos': enemy.pos,
                    'vel': enemy.vel,
                    'health': enemy.health,
                } for enemy in self.screen.enemies
            ],
            # Add other game state attributes as needed
        }

    def load_state(self):
        if hasattr(self, 'saved_state'):
            self.screen.player.pos = self.saved_state['player']['pos']
            self.screen.player.vel = self.saved_state['player']['vel']
            self.screen.player.health = self.saved_state['player']['health']
            for enemy, state in zip(self.screen.enemies, self.saved_state['enemies']):
                enemy.pos = state['pos']
                enemy.vel = state['vel']
                enemy.health = state['health']

    def quit(self):
        # exit
        pg.quit()
        sys.exit()

    def events(self):
        # handle events in game loop
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit()

            self.screen.handle_events(e)
            """self.screen.player.handle_events(e)
            for enemy in self.screen.enemies:
                enemy.handle_events(e)"""



