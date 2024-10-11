import pygame as pg
from constants import *
from src.spritesheet import Spritesheet
from os import path

vec = pg.math.Vector2


class AnimatedSprite(pg.sprite.Sprite):
    COLORKEY = (255,255,255)
    #COLORKEY = (34, 177, 76)
    ANIMATIONS = {}

    def __init__(self,screen, *groups):
        super().__init__(groups)
        self.screen = screen
        # control
        self.active_anim = None
        self.elapsed_time = 0
        self.active_name = ""
        self.animation_storage = {}
        self.transitions = {}

        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()

    def load(self):
        spritesheet = Spritesheet(path.join(self.screen.game.img_dir, SPRITESHEET_PATH), colorkey=self.COLORKEY)
        for name, (frames, duration, mode) in self.ANIMATIONS.items():
            anim = spritesheet.get_animation(frames, duration, mode, scale=1.2)
            self.store_animation(name, anim)

    def animate(self):
        for new_state, condition in self.transitions.get(self.active_name, []):
            if condition:
                self.set_active_animation(new_state)
                break
        self.image = self.active_anim.get_frame(self.elapsed_time)
        if hasattr(self, 'direction') and self.direction == 'L':
            self.image = pg.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()

    def handle_transition(self, transitions):
        pass

    def store_animation(self, name, anim):
        self.animation_storage[name] = anim

        # if no animation playing, start this one
        if self.active_name == "":
            self.set_active_animation(name)

    def set_active_animation(self, name):
        # check if animation with name exist
        if name not in self.animation_storage.keys():
            print(f'No animation: {name}')
            return

        # check if this animation is already running
        if name == self.active_name:
            return

        self.active_name = name
        self.active_anim = self.animation_storage[name]
        self.elapsed_time = 0

    def is_animation_finished(self):
        return self.active_anim.is_animation_finished(self.elapsed_time)

    def update(self, dt):
        self.elapsed_time += dt
        self.animate()


class Character(AnimatedSprite):

    def __init__(self, screen, pos, damage, *groups):
        super().__init__(screen,groups)

        # properties
        self.health = HEALTH
        self.direction = 'R'
        self.alive = True

        # physics
        self.ground_count = 0
        self.attack_count = 0
        self.shoot_count = 0
        self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.rect.midbottom = self.pos

    def reverse_direction(self):
        self.direction = 'L' if self.direction == 'R' else 'R'

    def move(self):
        if self.vel.x > 0:
            self.direction = 'R'
        elif self.vel.x < 0:
            self.direction = 'L'

    def get_hit(self, damage):
        self.health -= damage

    def update(self, dt):
        super().update(dt)

        # apply gravity
        # self.acc = vec(0, 0)
        self.acc = vec(0, GRAVITY)

        # movement
        self.move()

        # apply friction
        self.acc.x += self.vel.x * FRICTION

        # eqns of motions
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if abs(self.vel.x) < 0.5:
            self.vel.x = 0

        if self.vel.y > 10:
            self.vel.y = 10


