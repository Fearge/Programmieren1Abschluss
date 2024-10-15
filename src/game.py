import pygame as pg
import sys


from os import path

from src.constants import *
from src.music import Music


class Game:
    def __init__(self, title, dim):
        # initialize pygame
        pg.init()
        pg.display.set_caption(title)

        self.width = dim[0]
        self.height = dim[1]

        # set screen
        self.screen = None
        self.fullscreen = False
        self.surface = pg.display.set_mode(dim)
        self.clock = pg.time.Clock()
        self.paused = False

        # current directory
        self.dir = path.dirname(__file__)

        # load and play Music
        self.music = Music()
        self.music.load_music(path.join(self.dir, 'assets', 'mus', BACKGROUNDMUSIC_PATH))
        self.music.play_music()


    def set_screen(self, scr):
        # delete existing
        if self.screen is not None:
            del self.screen
            self.screen = None

        self.screen = scr

        # show new screen
        if self.screen is not None:
            self.screen.run()

    def quit(self):
        # exit
        pg.quit()
        sys.exit()

    def events(self):
        # handle events in game loop
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.quit()
            elif e.type == pg.KEYDOWN:
                if e.key == pg.K_ESCAPE:
                    self.quit()

            self.screen.handle_events(e)




