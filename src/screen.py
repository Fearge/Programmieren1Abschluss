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
		#self.attacks.update()
		self.check_collisions()
		self.camera.update(self.player)

	def display(self):
		self.game.surface.blit(self.map_img, self.camera.apply(self.map))
		self.camera.draw(self.game.surface, self.all_sprites)

		for attack in self.attacks:
			self.game.surface.blit(attack.image, self.camera.apply(attack))

		pg.display.flip()

	def check_collisions(self):
		# PLAYER COLLISIONS
		# collision with obstacles
		hits = pg.sprite.spritecollide(self.player, self.obstacles, False)
		if hits:
			for hit in hits:
				collide_with_obstacles(self.player, hit)

		#collisions with enemies
		hits = pg.sprite.spritecollide(self.player, self.enemies, False)
		if hits:
			collide_with_enemies(self.player)




		for enemy in self.enemies:
			hits = pg.sprite.spritecollide(enemy, self.obstacles, False)
			if hits:
				for hit in hits:
					collide_with_obstacles(enemy, hit)

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.Font(None, 74)  # Verwende eine Standard-Schriftart
        self.button_font = pg.font.Font(None, 48)
        self.button_color = (255, 255, 255)  # Weiß
        self.hover_color = (200, 200, 200)  # Hellgrau
        self.start_button_rect = pg.Rect((WIDTH // 2 - 75, HEIGHT // 2), (150, 50))  # Button-Rechteck

    def draw(self):
        # Hintergrundeinstellung (z. B. schwarz)
        self.game.surface.fill((0, 0, 0))

        # Titeltext zeichnen
        title_surface = self.font.render("Programmieren 1", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
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