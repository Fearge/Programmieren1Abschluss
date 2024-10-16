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


class Screen:
    def __init__(self, game):
        self.game = game
        self.health_bar = HealthBar(10, 10, 200, 20, HEALTH)  # Position and size of the health bar
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

        pg.display.flip()

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
        while True:
            self.game.events()
            self.update()
            self.display()
            self.game.clock.tick(self.game.ticks)

    def update(self):
        #update sprites
        self.particles.update()
        self.character_sprites.update()
        self.attacks.update()
        self.hooks.update()

        self.check_collisions()
        self.camera.update(self.player)
        self.health_bar.update(self.player.health)
        if self.player.health <= 0 or self.player.pos.y > self.map.height + 100:
            self.game.set_screen(DeathScreen(self.game))

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


    def draw(self):
        self.game.surface.blit(self.background, (0, 0))
        self.draw_text("HUGO 2", self.title_font, (255, 128, 40), (self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))
        self.create_button("Start", self.start_button_font, self.button_color, self.hover_color, self.start_button_rect)
        self.create_button("Fullscreen", self.fullscreen_button_font, self.button_color, self.hover_color, self.fullscreen_button_rect)
        self.display()

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.start_button_rect.collidepoint(pg.mouse.get_pos()):
                self.game.set_screen(Screen(self.game))
            elif self.fullscreen_button_rect.collidepoint(pg.mouse.get_pos()):
                self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.game.fullscreen:
            pg.display.set_mode((WIDTH, HEIGHT))
        else:
            pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
        self.game.fullscreen = not self.game.fullscreen

    def run(self):
        while True:
            self.game.events()
            self.draw()

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
        self.game_over_rect = self.game_over_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))

        # Button
        self.button_rect = pg.Rect((self.surface.get_width() // 2, self.surface.get_height() // 1.5),(250,100))

    def run(self):
        while True:
            if not self.death_sound:
                self.game.music.play_sound(HUGO_DEATH_SOUND_PATH)
                self.death_sound = True
            self.game.events()
            self.display()
            self.clock.tick(self.game.ticks)

    def display(self):
        # Background
        self.surface.fill((0, 0, 0))  # Black background

        # Game Over text
        self.draw_text("Game Over", self.death_font, self.game_over_color, (self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))
        # Button with hover effect
        self.create_button("Restart", self.button_font, self.button_color, self.button_hover_color, self.button_rect)

        # Update display
        super().display()

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(pg.mouse.get_pos()):
                self.restart_game()

    def restart_game(self):
        # Reset the screen to the game
        self.game.set_screen(Screen(self.game))  # Set the main game as the active screen

"""class DeathScreen(BaseScreen):
    def __init__(self, game):
        super().__init__(game)
        self.death_sound = False

        # Farben und Schriftarten
        self.font = pg.font.Font(None, 150)  # Standard pygame Schriftart für "Game Over"
        self.button_font = pg.font.Font(None, 80)  # Gleiche Schriftgröße wie der "Start"-Button
        self.game_over_color = (255, 0, 0)  # Rot für "Game Over"
        self.button_color = WHITE  # Weiß für den Button
        self.button_hover_color = (200, 200, 200)

        # Textpositionen
        self.game_over_text = self.font.render("Game Over", True, self.game_over_color)
        self.game_over_rect = self.game_over_text.get_rect(center=(self.surface.get_width() // 2, self.surface.get_height() // 5 * 2))

        # Button
        self.button_text = self.button_font.render("Restart", True, self.button_color)
        self.button_rect = pg.Rect(0, 0, 250, 100)  # Gleiche Button-Größe wie der "Start"-Button
        self.button_rect.center = (self.surface.get_width() // 2, self.surface.get_height() // 1.5)

    def run(self):
        while True:
            if not self.death_sound:
                self.game.music.play_sound(HUGO_DEATH_SOUND_PATH)
                self.death_sound = True
            self.game.events()
            self.display()
            self.clock.tick(self.game.ticks)

    def display(self):
        # Hintergrund
        self.surface.fill((0, 0, 0))  # Schwarzer Hintergrund

        # Game Over Text
        self.surface.blit(self.game_over_text, self.game_over_rect)

        # Button mit Hover Effekt
        mouse_pos = pg.mouse.get_pos()
        if self.button_rect.collidepoint(mouse_pos):
            # Button Hover
            pg.draw.rect(self.surface, self.button_hover_color, self.button_rect)  # Grauer Button bei Hover
        else:
            pg.draw.rect(self.surface, self.button_color, self.button_rect)  # Weißer Button
        button_text = self.button_font.render("Restart", True, (0, 0, 0))  # Schwarzer Text

        self.surface.blit(button_text, button_text.get_rect(center=self.button_rect.center))

        # Update
        pg.display.flip()

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.button_rect.collidepoint(pg.mouse.get_pos()):
                self.restart_game()

    def restart_game(self):
        # Hier wird der Bildschirm auf das Spiel zurückgesetzt
        self.game.set_screen(Screen(self.game))  # Setze das Hauptspiel wieder als aktiven Bildschirm
"""