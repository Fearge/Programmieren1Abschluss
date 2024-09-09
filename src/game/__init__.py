import pygame

from .object import GameObject
from .player import Player
from .attack import Attack

class Game:
    def __init__(self, screen):
        self.screen = screen
        # Gruppen erstellen
        #self.enemy_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.all_sprites = GameObject.all_sprites
        self.init()

    def init(self):
        # Enemies
        #self.spawn_enemies()
        # Player
        self.spawn_player()
        #Attack
        #self.createAttacks()

    def spawn_enemies(self):
        """while len(self.enemy_sprites) < 1:
            enemy = Enemy(x=10, y=100, width=128, height=128)
            self.enemy_sprites.add(enemy)
            self.all_sprites.add(enemy)"""

    def spawn_player(self):
        player = Player(x=100, y=100, width=64, height=64)
        self.player_sprites.add(player)
        self.all_sprites.add(player)

    def update(self):
        self.all_sprites.update(self.screen)

    def render(self):
        self.screen.fill((255, 255, 255))  # White background
        self.all_sprites.draw(self.screen)

