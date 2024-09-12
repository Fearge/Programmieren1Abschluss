import pygame

class SoundManager:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = None
        self.death_sound = None

    def load_sound(self, filename):
        self.background_music = pygame.mixer.Sound(filename)

    def play_background_music(self):
        self.background_music.play(-1)  # -1 means looping indefinitely

    def play_death_sound(self):
        self.death_sound.play()