from logging import currentframe
from shutil import posix

import pygame as pg
from os import path


from base_sprite import *
from spritesheet import Spritesheet, Animation

class Player(Character):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.12, Animation.LOOP),
        'standing': (STANDING_FRAMES, 0.20, LOOP),
        'jumping': (JUMPING_FRAMES, 0.10, NORMAL),
        'falling': (FALLING_FRAMES, 0.10, NORMAL),
        'landing': (LANDING_FRAMES, 0.10, NORMAL)
    }
    def __init__(self, screen, pos, *groups):
        super().__init__(pos, PLAYER_DAMAGE, groups)
        self.screen = screen
        self.pos = pos
        self.jump_release = 0
        self.attacks = pg.sprite.Group()
        self.attack_cooldown = 0


        # image
        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos

        self.width = self.rect.right - self.rect.left
        self.height = self.rect.top - self.rect.bottom

    def animate(self):
        self.transitions = {
            "walking": [("standing", self.vel.x == 0), ("jumping", self.vel.y < 0)],
            "standing": [("walking", abs(self.vel.x) > 0), ("jumping", self.vel.y < 0)],
            "jumping": [("falling", self.vel.y > 0)],
            "falling": [("landing", self.ground_count > 0)],
            "landing": [("walking", self.is_animation_finished() and abs(self.vel.x) > 0),
                        ("standing", self.is_animation_finished() and abs(self.vel.x) == 0)]
        }
        super().animate()

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
        super().move()

    def attack(self):
        attack = Attack(self.screen, 10, True, self.attacks)
        attack.align(self)
        print('attack')

    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and self.attack_cooldown == 0:
                self.attack()
                self.attack_cooldown = PLAYER_ATT_COOLDOWN


    def update(self):
        super().update(1/self.screen.game.fps)
        self.attacks.update()
        #self.animate()
        for attack in self.attacks:
            if attack.followPlayer:
                attack.align(self)

        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

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

class Attack(AnimatedSprite):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.12, LOOP)
    }
    def __init__(self, screen, damage, followPlayer, *groups):
        super().__init__(groups)

        # properties
        self.screen = screen
        self.pos = vec(0, 0)
        self.damage = damage
        self.followPlayer = followPlayer

        self.attack_length = 50
        self.__attack_duration = 0

        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def align(self, entity):
        if entity.direction == 'R':
            self.rect.center = entity.pos + (entity.rect.width/2, -entity.rect.height / 2)
        elif entity.direction == 'L':
            self.rect.center = entity.pos - (entity.rect.width, entity.rect.height / 2)
        self.pos = entity.pos

    def update(self):
        super().update(1 / self.screen.game.fps)

        self.animate()
        self.__attack_duration += 1
        if self.__attack_duration > self.attack_length:
            self.kill()
            print('killed')

