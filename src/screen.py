import pygame as pg
from os import path

from collisions import *
from map import TiledMap, Camera
from sprites import Obstacle, Player
from src.sprites import Enemy

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

		for obj in self.map.tmx_data.objects:
			obj_midbottom = vec(obj.x + obj.width/2, obj.y + obj.height)
			if obj.name == 'player':
				self.player = Player(self, obj_midbottom, self.all_sprites)
			elif obj.name == 'obstacle':
				Obstacle((obj.x, obj.y), (obj.width, obj.height), self.obstacles)
			elif obj.name == 'melee_enemy':
				enemy = Enemy(self, obj_midbottom, self.enemies)
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

		for attack in self.player.attacks:
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