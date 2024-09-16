from logging import currentframe
from shutil import posix

import pygame as pg
from os import path


from base_sprite import *
from spritesheet import Spritesheet, Animation

class Player(Character):
	def __init__(self, screen, pos, *groups):
		super().__init__(pos, PLAYER_DAMAGE, groups)
		self.screen = screen
		self.pos = pos
		self.jump_release = 0
		self.attacks = pg.sprite.Group()


		# image
		self.load()
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.midbottom = pos

		self.width = self.rect.right - self.rect.left
		self.height = self.rect.top - self.rect.bottom

	def load(self):
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), bg=(34, 177, 76))

		# MOVEMENT ANIMATIONS
		# walking animation
		walking_frames = [[22, 346, 62, 55], [88, 348, 65, 49], [160, 345, 65, 54], [238, 344, 53, 56], \
			[296, 338, 60, 57], [365, 342, 63, 51], [433, 343, 65, 52], [503, 343, 58, 55]]
		walking_anim = spritesheet.get_animation(walking_frames, 0.12, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('walking', walking_anim)

		# standing animation
		standing_frames = [(28, 247, 34, 63), (73, 248, 34, 62), (115, 248, 35, 61)]
		standing_animation = spritesheet.get_animation(standing_frames, 0.20, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('standing', standing_animation)

		# jumping animation
		jumping_frames = [(609, 343, 43, 51), (664, 337, 48, 64), (720, 338, 48, 64)]
		jumping_animation = spritesheet.get_animation(jumping_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('jumping', jumping_animation)

		# falling animation
		falling_frames = [(773, 344, 60, 50), (839, 323, 44, 80), (897, 326, 46, 77)]
		falling_animation = spritesheet.get_animation(falling_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('falling', falling_animation)

		# landing animation
		landing_frames = [(960, 336, 47, 69), (1023, 362, 47, 43), (1081, 352, 42, 52)]
		landing_animation = spritesheet.get_animation(landing_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('landing', landing_animation)

		# batarang throw
		batarang_throw_frames = [(20, 1004, 46, 54), (81, 997, 53, 61), (149, 1004, 82, 54), (239, 1004, 72, 54), (326, 1003, 67, 55)]
		batarang_throw_animation = spritesheet.get_animation(batarang_throw_frames, 0.10, Animation.PlayMode.NORMAL, scale=1.2)
		self.store_animation('batarang_throw', batarang_throw_animation)

	def animate(self):
		if self.active_name == "walking":
			if self.vel.x == 0:
				self.set_active_animation("standing")

			if self.vel.y < 0:
				self.set_active_animation("jumping")

		if self.active_name == "standing":
			if abs(self.vel.x) > 0:
				self.set_active_animation("walking")

			if self.vel.y < 0:
				self.set_active_animation("jumping")

		if self.active_name == "jumping":
			if self.vel.y > 0:
				self.set_active_animation("falling")

		if self.active_name == "falling":
			if self.ground_count > 0:
				self.set_active_animation("landing")

		if self.active_name == "landing":
			if self.is_animation_finished():
				if abs(self.vel.x) > 0:
					self.set_active_animation("walking")
				else:
					self.set_active_animation("standing")
			else:
				self.vel.x = 0

			if self.is_animation_finished():
				self.set_active_animation("standing")
				self.shoot_count = 0

		bottom = self.rect.bottom
		self.image = self.active_anim.get_frame(self.elapsed_time)
		
		# flip image if necessary
		if self.direction == 'L':
			self.image = pg.transform.flip(self.image, True, False)

		self.rect = self.image.get_rect()
		self.rect.bottom = bottom

	def move(self):
		keys = pg.key.get_pressed()

		# horizontal movement
		if keys[pg.K_a]:
			self.direction = 'L'
			if not self.attack_count > 0:
				self.acc.x = -PLAYER_ACC
		
		elif keys[pg.K_d]:
			self.direction = 'R'
			if not self.attack_count > 0:
				self.acc.x = PLAYER_ACC

		# jumping
		if keys[pg.K_w]:
			if self.jump_release > 0:
				if self.ground_count > 0 and not self.active_name == 'falling':
					self.vel.y = PLAYER_JUMP
					self.ground_count = 0
					self.jump_release = 0

		else:
			self.jump_release += 1


	def handle_events(self, event):
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_SPACE:
				attack = Attack(self.screen, self.rect.midright, 10, True, self.attacks)
				attack.align(self)
				print('attack')

	def update(self):
		super().update(1/self.screen.game.fps)
		self.attacks.update()
		self.animate()
		for attack in self.attacks:
			if attack.followPlayer:
				attack.align(self)



		# update properties
		#self.width = self.rect.right - self.rect.left
		#self.height = self.rect.top - self.rect.bottom

		self.rect.midbottom = self.pos


class Obstacle(pg.sprite.Sprite):
	def __init__(self, pos, size, *groups):
		super().__init__(groups)

		# rect
		self.rect = pg.Rect(pos, size)
		
		# position
		self.x = pos[0]
		self.y = pos[1]
		self.rect.x = pos[0]
		self.rect.y = pos[1]

class Enemy(Character):
	def __init__(self, screen, pos, *groups):
		super().__init__(pos, 10 ,groups)
		# properties
		self.screen = screen
		self.pos = pos
		self.prev_pos = vec(pos)
		self.stuck_count = 0
		self.stuck_threshold = 10

		self.load()
		#self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.vel.x = ENEMY_VEL
		self.movement_tick = 0

	def load(self):
		self.image = pg.image.load(path.join('assets','img','title_bg.jpg')).convert_alpha()
		self.image = pg.transform.scale(self.image, (100, 100))

	def move(self):
		self.movement_tick += 1
		if self.movement_tick % 100 == 0:
			self.reverse_direction()

		self.acc.x = self.vel.x * 0.12

	def reverse_direction(self):
		self.vel.x *= -1

	def check_stuck(self):
		if self.pos == self.prev_pos:
			self.stuck_count += 1
		else:
			self.stuck_count = 0

		if self.stuck_count > self.stuck_threshold:
			self.vel.x = -ENEMY_VEL
			self.movement_tick = 0
			self.stuck_count = 0


	def update(self, dt = 1):
		super().update(1/self.screen.game.fps)

		self.check_stuck()
		print(f'pos{self.pos} prev pos{self.prev_pos}')

		self.prev_pos = vec(self.pos)
		self.rect.midbottom = self.pos





class Attack(AnimatedSprite):
	def __init__(self, screen, pos, damage, followPlayer, *groups):
		super().__init__(groups)

		# properties
		self.screen = screen
		self.pos = vec(pos)
		self.damage = damage
		self.followPlayer = followPlayer
		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.attack_duration = 0
		self.cooldown = 0


		self.load()
		self.image = self.active_anim.get_frame(0)
		self.rect = self.image.get_rect()
		self.rect.center = self.pos

	def load(self):
		#self.image = pg.image.load(path.join('assets','img','title_bg.jpg')).convert_alpha()
		#self.image = pg.transform.scale(self.image, (100, 100))
		#spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), bg=(34, 177, 76))

		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), bg=(34, 177, 76))

		walking_frames = [[22, 346, 62, 55], [88, 348, 65, 49], [160, 345, 65, 54], [238, 344, 53, 56], \
						  [296, 338, 60, 57], [365, 342, 63, 51], [433, 343, 65, 52], [503, 343, 58, 55]]
		walking_anim = spritesheet.get_animation(walking_frames, 0.12, Animation.PlayMode.LOOP, scale=1.2)
		self.store_animation('walking', walking_anim)

	def animate(self):
		self.image = self.active_anim.get_frame(self.elapsed_time)

	def align(self, player):
		if player.direction == 'R':
			self.rect.center = player.pos + (player.rect.width, -player.rect.height/2)
		elif player.direction == 'L':
			self.rect.center = player.pos - (player.rect.width, player.rect.height/2)
		self.pos = player.pos

	def update(self):
		super().update(1/self.screen.game.fps)
		if self.alive():
			self.animate()
			self.attack_duration += 1
			if self.attack_duration > 100:
				self.kill()
				print('killed')
		pass