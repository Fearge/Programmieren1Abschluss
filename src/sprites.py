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
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), colorkey=(34, 177, 76))

		anmations = {
			'walking': (WALKING_FRAMES, 0.12, Animation.PlayMode.LOOP),
			'standing': (STANDING_FRAMES, 0.20, Animation.PlayMode.LOOP),
			'jumping': (JUMPING_FRAMES, 0.10, Animation.PlayMode.NORMAL),
			'falling': (FALLING_FRAMES, 0.10, Animation.PlayMode.NORMAL),
			'landing': (LANDING_FRAMES, 0.10, Animation.PlayMode.NORMAL)
		}

		for name, (frames, duration, mode) in anmations.items():
			anim = spritesheet.get_animation(frames, duration, mode, scale=1.2)
			self.store_animation(name, anim)


	def animate(self):
		transitions = {
			"walking": [("standing", self.vel.x == 0), ("jumping", self.vel.y < 0)],
			"standing": [("walking", abs(self.vel.x) > 0), ("jumping", self.vel.y < 0)],
			"jumping": [("falling", self.vel.y > 0)],
			"falling": [("landing", self.ground_count > 0)],
			"landing": [("walking", self.is_animation_finished() and abs(self.vel.x) > 0),
						("standing", self.is_animation_finished() and abs(self.vel.x) == 0)]
		}
		for new_state, condition in transitions.get(self.active_name, []):
			if condition:
				self.set_active_animation(new_state)
				break

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
				attack = Attack(self.screen, 10, True, self.attacks)
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

		# update previous position
		self.prev_pos = vec(self.pos)

	def update(self, dt = 1):
		super().update(1/self.screen.game.fps)

		self.check_stuck()
		self.prev_pos = vec(self.pos)
		self.rect.midbottom = self.pos





class Attack(AnimatedSprite):
	def __init__(self, screen, damage, followPlayer, *groups):
		super().__init__(groups)

		# properties
		self.screen = screen
		self.pos = vec(0,0)
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
		spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), colorkey=(34, 177, 76))
		animations = {
			'walking': (WALKING_FRAMES, 0.12, Animation.PlayMode.LOOP)
		}

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