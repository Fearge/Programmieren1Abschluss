from os import path
import pygame as pg
from constants import *


class Music:
    def __init__(self):

        self.dir = path.dirname(__file__)
        pg.mixer.init()


    def load_music(self, music_file):
        """Load the mus file."""
        try:
            pg.mixer.music.load(music_file)
        except pg.error as e:
            print(f"Cannot load mus file: {e}")

    def load_sound(self, sound_file):
        """Load a sound file."""
        try:
            return pg.mixer.Sound(sound_file)
        except pg.error as e:
            print(f"Cannot load sound file: {e}")
            return None

    def play_music(self, loops=0, start=0.0):
        """Play the mus file."""
        pg.mixer.music.play(loops, start)

    def play_sound(self, sound):
        self.load_sound(path.join(self.dir, 'assets', 'mus', sound)).play()

    def stop_sound(self, sound):
        self.load_sound(path.join(self.dir, 'assets', 'mus', sound)).stop()