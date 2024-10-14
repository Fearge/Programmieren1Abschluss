import pygame as pg
from os import path

from collisions import *
from map import TiledMap, Camera
from sprites import Obstacle, Player
from src.enemy import MeleeEnemy

vec = pg.math.Vector2

class Screen:
    def __init__(self, game):
        self.game = game

        self.load()
        self.new()

    def load(self):
        #  prepare map
        self.map = TiledMap(path.join(self.game.map_dir, 'Base Level.tmx'))
        self.map_img, self.map.rect = self.map.make_map()

    def new(self):
        # sprite groups
        self.all_sprites = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.attacks = pg.sprite.Group()
        self.hooks = pg.sprite.Group()


        for obj in self.map.tmx_data.objects:
            obj_midbottom = vec(obj.x + obj.width/2, obj.y + obj.height)
            if obj.name == 'player':
                self.player = Player(self, obj_midbottom, self.all_sprites)
            elif obj.name == 'obstacle':
                Obstacle((obj.x, obj.y), (obj.width, obj.height), self.obstacles)
            elif obj.name == 'melee_enemy':
                enemy = MeleeEnemy(self, obj_midbottom, self.enemies)
                self.all_sprites.add(enemy)

        self.camera = Camera(self.game, self.map.width, self.map.height)

    def run(self):
        while True:
            self.game.clock.tick(self.game.fps)
            self.game.events()
            self.update()
            self.display()

    def update(self):
        self.all_sprites.update()
        self.check_collisions()
        self.camera.update(self.player)

    def display(self):
        self.game.surface.blit(self.map_img, self.camera.apply(self.map))
        self.camera.draw(self.game.surface, self.all_sprites)

        for attack in self.attacks:
            self.game.surface.blit(attack.image, self.camera.apply(attack))
        for hook in self.hooks:
            self.game.surface.blit(hook.image, self.camera.apply(hook))
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

        #collisions with enemies
        hits = pg.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            collide_with_enemies(self.player)
            if self.player.health == 0:
                self.game.set_screen(DeathScreen(self.game))

        for hook in self.hooks:
            if not hook.is_attached:
                hits = pg.sprite.spritecollide(hook, self.obstacles, False)
                if hits:
                    hook_collision(hook)








class StartScreen:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 100)  # Verwende eine Standard-Schriftart
        self.button_font = pg.font.Font(None, 80)
        self.button_color = (255, 255, 255)  # Weiß
        self.hover_color = (200, 200, 200)  # Hellgrau
        self.start_button_rect = pg.Rect((WIDTH // 2 - 100, HEIGHT // 2), (200, 100))  # Button-Rechteck

    def draw(self):
        # Hintergrundeinstellung (z. B. schwarz)
        self.game.surface.fill((50, 50, 50))

        # Titeltext zeichnen
        title_surface = self.font.render("Programmieren 1", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        self.game.surface.blit(title_surface, title_rect)

        # Startbutton zeichnen
        button_color = self.hover_color if self.start_button_rect.collidepoint(pg.mouse.get_pos()) else self.button_color
        pg.draw.rect(self.game.surface, button_color, self.start_button_rect)

        button_text_surface = self.button_font.render("Start", True, (0, 0, 0))  # Textfarbe schwarz
        button_text_rect = button_text_surface.get_rect(center=self.start_button_rect.center)
        self.game.surface.blit(button_text_surface, button_text_rect)

        pg.display.flip()  # Aktualisiere den Bildschirm

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:  # Linke Maustaste
                if self.start_button_rect.collidepoint(pg.mouse.get_pos()):  # Überprüfen, ob der Button geklickt wurde
                    self.game.set_screen(Screen(self.game))  # Zum Hauptspiel wechseln

    def run(self):
        while True:
            self.handle_events()
            self.draw()

import pygame as pg

class DeathScreen:
    def __init__(self, game):
        self.game = game
        self.surface = game.surface
        self.clock = pg.time.Clock()

        # Farben und Schriftarten
        self.font = pg.font.Font(None, 180)  # Standard pygame Schriftart für "Game Over"
        self.button_font = pg.font.Font(None, 80)  # Gleiche Schriftgröße wie der "Start"-Button
        self.game_over_color = (255, 0, 0)  # Rot für "Game Over"
        self.button_color = (255, 255, 255)  # Weiß für den Button
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
            self.handle_events()
            self.display()
            self.clock.tick(60)

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
            button_text = self.button_font.render("Restart", True, (0, 0, 0))  # Schwarzer Text bei Hover
        else:
            pg.draw.rect(self.surface, self.button_color, self.button_rect)  # Weißer Button
            button_text = self.button_font.render("Restart", True, (0, 0, 0))  # Schwarzer Text

        self.surface.blit(button_text, button_text.get_rect(center=self.button_rect.center))

        # Update
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(pg.mouse.get_pos()):
                    self.restart_game()

    def restart_game(self):
        # Hier wird der Bildschirm auf das Spiel zurückgesetzt
        self.game.set_screen(Screen(self.game))  # Setze das Hauptspiel wieder als aktiven Bildschirm
