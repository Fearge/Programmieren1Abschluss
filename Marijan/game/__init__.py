import pygame
from pygame.examples.go_over_there import screen

from .object import GameObject
from .player import Player
from .enemy import Enemy
from .physics import PhysicsEngine
from .platform import Platform
from .camera import Camera
from .attack import Attack


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.camera = Camera(screen.get_width(), screen.get_height())
        self.enemy_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.attack_sprites = pygame.sprite.Group()
        self.init()

    def init(self):
        self.spawn_objects()
        self.spawn_enemies()
        self.spawn_player()

    def update(self):
        self.all_sprites.update(screen = self.screen)
        """self.platform_sprites.update()
        self.player_sprites.update(screen=self.screen)
        self.enemy_sprites.update(screen=self.screen)"""
        self.camera.update(self.player_sprites.sprites()[0])  # Assuming one player

        # Adjust platform positions based on player velocity
        player_velocity = self.player_sprites.sprites()[0].get_velocity()
        player_speed = self.player_sprites.sprites()[0].get_speed()
        for platform in self.platform_sprites:
            platform.rect.x -= player_velocity.x
            platform.rect.y -= player_velocity.y

        #self.logic()

    def render(self, renderer):
        renderer.render_background()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        renderer.update_display()

    def spawn_enemies(self):
        while len(self.enemy_sprites) < 10:
            enemy = Enemy(x=500, y=100, width=30, height=30)
            self.enemy_sprites.add(enemy)
            self.all_sprites.add(enemy)

    """def logic(self):
        if len(self.enemy_sprites) < 10:
            self.spawn_enemies()
        if len(self.player_sprites) < 1:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"reason": "game_over"}))
            self.reset_game()
            print("game_over")"""

    def spawn_player(self):
        player = Player(x=100, y=100, width=50, height=50)
        self.player_sprites.add(player)
        self.all_sprites.add(player)

    def spawn_objects(self):
        self.platform_sprites.add(Platform(x=-400, y=self.screen.get_height() - 20, width=self.screen.get_width() + 800, height=20))
        self.platform_sprites.add(Platform(x=40, y=self.screen.get_height() - 200, width=100, height=20))
        self.platform_sprites.add(Platform(x=80, y=self.screen.get_height() - 100, width=100, height=20))
        self.platform_sprites.add(Platform(x=120, y=self.screen.get_height() - 280, width=100, height=20))
        self.platform_sprites.add(Platform(x=320, y=self.screen.get_height() - 320, width=100, height=20))
        self.platform_sprites.add(Platform(x=520, y=self.screen.get_height() - 400, width=100, height=20))

        for platform in self.platform_sprites:
            self.all_sprites.add(platform)

    def handle_events(self, event):
        if len(self.player_sprites) < 1:
            return 'end'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player = self.player_sprites.sprites()[0]
                attack = Attack(player.rect.x, player.rect.y, 64, 64, player)
                self.all_sprites.add(attack)
                player.attack(attack)
        return None

    def render(self, renderer):
        renderer.render_background()
        renderer.render_sprites(self.all_sprites)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        renderer.update_display()
