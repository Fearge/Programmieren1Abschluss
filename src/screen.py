from itertools import chain

import pygame as pg
from os import path

from pygame import FULLSCREEN

from constants import *

from collisions import *
from map import TiledMap, Camera
from player import Obstacle, Player
from src.attacks import ChargeAttack, PlayerAttack
from src.base_sprite import BaseScreen
from src.enemy import MeleeEnemy, Enemy, RangedEnemy
from health_bar import HealthBar
from src.grapple import GrapplingHook


class Screen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.health_bar = HealthBar(10, 10, 200, 20, PLAYER_HEALTH)  # Position and size of the health bar
        self.enemies_health_bars = []
        self.load()
        self.new()



    def load(self):
        #  prepare map
        self.map = TiledMap(path.join(self.game.map_dir, 'Base Level.tmx'))
        self.map_img, self.map.rect = self.map.make_map()

    def new(self):
        # sprite groups
        self.character_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        self.hooks = pg.sprite.Group()
        self.particles = pg.sprite.Group()


        for obj in self.map.tmx_data.objects:
            obj_midbottom = vec(obj.x + obj.width/2, obj.y + obj.height)
            if obj.name == 'player':
                self.player = Player(self, obj_midbottom, self.character_sprites)
            elif obj.name == 'obstacle':
                Obstacle((obj.x, obj.y), (obj.width, obj.height), self.obstacles)
            elif obj.name == 'melee_enemy':
                rangedEnemy = RangedEnemy(self, obj_midbottom, self.enemies)
                self.character_sprites.add(rangedEnemy)
            elif obj.name == 'ranged_enemy':
                meleeEnemy = MeleeEnemy(self, obj_midbottom, self.enemies)
                self.character_sprites.add(meleeEnemy)

        self.camera = Camera(self.game, self.map.width, self.map.height)

    def handle_events(self, e):
        self.player.handle_events(e)
        for enemy in self.enemies:
            enemy.handle_events(e)



    def display(self):
        self.game.surface.blit(self.map_img, self.camera.apply(self.map))
        self.camera.draw(self.game.surface, self.character_sprites)

        for particle in self.particles:
            self.game.surface.blit(particle.image, self.camera.apply(particle))
        for attack in self.attacks:
            self.game.surface.blit(attack.image, self.camera.apply(attack))
        for hook in self.hooks:
            self.game.surface.blit(hook.image, self.camera.apply(hook))

        # health bars
        self.health_bar.draw(self.game.surface, None)  # Draw the health bar
        for enemy in self.enemies:
            enemy.health_bar.draw(self.game.surface, self.camera)

        super().display()

    def check_collisions(self):
        # PLAYER COLLISIONS
        # collision with obstacles
        hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
        if hits:
            for hit in hits:
                collide_with_obstacles(self.player, hit)
        for enemy in self.enemies:
            hits = pg.sprite.spritecollide(enemy, self.obstacles, False)
            if hits:
                for hit in hits:
                    collide_with_obstacles(enemy, hit)
        # attacks
        for attack in self.attacks:
            hits = pg.sprite.spritecollide(attack, self.character_sprites, False)
            if hits:
                for hit in hits:
                    attack_collision(attack, hit)
        # Hook
        for hook in self.hooks:
            if not hook.is_attached:
                hits = pg.sprite.spritecollide(hook, self.obstacles, False)
                if hits:
                    hook_collision(hook, self)

    def run(self):
        super().run()

    def update(self):
        #update sprites
        self.particles.update()
        self.character_sprites.update()
        self.attacks.update()
        self.hooks.update()
        self.check_collisions()
        self.camera.update(self.player)

        #health bar
        self.health_bar.update(self.player.health)
        if self.player.health <= 0 or self.player.pos.y > self.map.height + 100:
            self.game.music.play_sound(HUGO_DEATH_SOUND_PATH)
            self.game.set_screen(DeathScreen(self.game))

        #check if all enemies are dead
        if not self.enemies:
            self.game.set_screen(WinScreen(self.game))




class StartScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.start_button_rect = pg.Rect((self.surface.get_width() // 2 - 100, self.surface.get_height() // 5 * 3),(200,100))
        self.fullscreen_button_rect = pg.Rect((self.surface.get_width() // 2 - 100, self.surface.get_height() // 5 * 4),(200,100))

        self.button_color = (255, 255, 255)
        self.hover_color = (200, 200, 200)

        self.start_button_font = pg.font.Font(None, 80)
        self.fullscreen_button_font = pg.font.Font(None, 40)
        self.title_font = pg.font.Font(None, 130)

        self.background = pg.image.load(path.join(self.game.map_dir, 'HugoMapFinCut.png')).convert()
        if not self.game.music.is_music_playing:
            self.game.music.load_music(path.join(self.game.map_dir, BACKGROUNDMUSIC_PATH))
            self.game.music.play_music()


    def display(self):
        self.game.surface.blit(self.background, (0, 0))
        self.draw_text("HUGO 2", self.title_font, (255, 128, 40), (self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))
        self.create_button("Start", self.start_button_font, self.button_color, self.hover_color, self.start_button_rect)
        self.create_button("Fullscreen", self.fullscreen_button_font, self.button_color, self.hover_color, self.fullscreen_button_rect)
        super().display()

    def handle_events(self, e):
        if e.type == pg.MOUSEBUTTONDOWN and e.button == 1:
            if self.start_button_rect.collidepoint(pg.mouse.get_pos()):
                self.game.set_screen(Screen(self.game))
            elif self.fullscreen_button_rect.collidepoint(pg.mouse.get_pos()):
                self.toggle_fullscreen()
        super().handle_events(e)

    def toggle_fullscreen(self):
        if self.game.fullscreen:
            pg.display.set_mode((WIDTH, HEIGHT))
        else:
            pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        self.game.fullscreen = not self.game.fullscreen

class DeathScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.death_sound = False

        # Colors and fonts
        self.death_font = pg.font.Font(None, 150)  # Standard pygame font for "Game Over"
        self.button_font = pg.font.Font(None, 80)  # Same font size as the "Start" button

        self.game_over_color = (255, 0, 0)  # Red for "Game Over"
        self.button_color = (255, 255, 255)  # White for the button
        self.button_hover_color = (200, 200, 200)

        # Text positions
        self.game_over_text = self.death_font.render("Game Over", True, self.game_over_color)

        # Button
        self.button_rect = pg.Rect((self.surface.get_width() // 2 - 100, self.surface.get_height() // 1.5),(250,100))

    def update(self):
        if not self.death_sound:
            self.game.music.stop_music()
            self.game.music.play_sound(LOSE_SOUND_PATH)
            self.death_sound = True

    def display(self):
        # Background
        self.surface.fill((0, 0, 0))  # Black background

        # Game Over text
        self.draw_text("Game Over", self.death_font, self.game_over_color, (self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))
        # Button with hover effect
        self.create_button("Restart", self.button_font, self.button_color, self.button_hover_color, self.button_rect)

        # Update display
        super().display()

    def handle_events(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(pg.mouse.get_pos()):
                self.restart_game()
        super().handle_events(e)

    def restart_game(self):
        # Reset the screen to the game
        self.game.set_screen(StartScreen(self.game))  # Set the main game as the active screen

class WinScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.win_sound = False

        # Colors and fonts
        self.win_font = pg.font.Font(None, 150)  # Standard pygame font for "You Win"
        self.button_font = pg.font.Font(None, 60)  # Same font size as the "Restart" button

        self.win_text_color = (0, 255, 0)  # Green for "You Win"
        self.button_color = (255, 255, 255)  # White for the button
        self.button_hover_color = (200, 200, 200)

        # Text positions
        self.win_text = self.win_font.render("You Win", True, self.win_text_color)
        self.win_text_rect = self.win_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))

        # Button
        self.button_rect = pg.Rect((self.surface.get_width() // 2 - 125, self.surface.get_height() // 1.5), (250, 100))

    def update(self):
        if not self.win_sound:
            self.game.music.play_sound(WIN_SOUND_PATH)  # Plays a winning sound effect
            self.win_sound = True
    def display(self):
        # Background
        self.surface.fill((100, 100, 100))  # Black background

        # "You Win" text
        self.draw_text("You Win", self.win_font, self.win_text_color, (self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))

        # Button with hover effect
        self.create_button("Play Again", self.button_font, self.button_color, self.button_hover_color, self.button_rect)

        # Update display
        super().display()

    def handle_events(self, e):
        if e.type == pg.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(pg.mouse.get_pos()):
                self.restart_game()
        super().handle_events(e)

    def restart_game(self):
        # Reset the screen to the main game
        self.game.music.stop_music()
        self.game.set_screen(StartScreen(self.game))  # Set the main game as the active screen