import pygame as pg
from pygame.examples.cursors import image

from constants import *
from src import Sprite
from src.spritesheet import Spritesheet, Animation
from os import path

vec = pg.math.Vector2


class AnimatedSprite(Sprite):
    #COLORKEY = (255,255,255)
    COLORKEY = COLORKEY
    ANIMATIONS = {}

    def __init__(self,screen, *groups):
        super().__init__(*groups)
        self.screen = screen

        # control
        self.active_anim = None
        self.elapsed_time = 0
        self.active_name = ""
        self.animation_storage = {}
        self.transitions = {}

        self.spritesheet = Spritesheet(path.join(self.screen.game.img_dir, SPRITESHEET_PATH), colorkey=self.COLORKEY)
        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()

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

    def load(self):
        for name, (frames, duration, mode) in self.ANIMATIONS.items():
            anim = self.spritesheet.get_animation(frames, duration, mode, scale=0.5)
            self.store_animation(name, anim)

    def animate(self):
        for new_state, condition in self.transitions.get(self.active_name, []):
            if condition:
                self.set_active_animation(new_state)
                break
        self.image = self.active_anim.get_frame(self.elapsed_time)
        self.rect = self.image.get_rect()


    def is_animation_finished(self):
        return self.active_anim.is_animation_finished(self.elapsed_time)

    def update(self):
        self.elapsed_time += 1/self.screen.game.ticks
        self.animate()


class Character(AnimatedSprite):
    ANIMATIONS = {
        'hit': (HIT_PARTICLES, 0.6, Animation.NORMAL),
    }
    def __init__(self, screen, pos,  *groups):
        super().__init__(screen,groups)

        # properties
        self.health = HEALTH
        self.direction = 'R'
        self.alive = True
        self.character_attack = None
        self.is_attacking = False
        self.attack_cooldown = 0
        self.sprite_type = 'character'

        #hit particles
        self.particles_duration = 0.5
        self.particles_elapsed_time = 0

        #music
        self.attack_sound = None
        self.hit_sound = None
        self.death_sound = None

        # physics
        self.ground_count = 0
        self.attack_count = 0
        self.shoot_count = 0
        self.pos = vec(pos)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        self.rect.midbottom = self.pos

    def flip_image_on_direction(self):
        if self.vel.x > 0:
            self.direction = 'R'
        elif self.vel.x < 0:
            self.direction = 'L'

    def get_hit(self, damage):
        self.health -= damage
        self.show_hit_particles()
        self.screen.game.music.play_sound(self.hit_sound)

    def show_hit_particles(self):
        particle = Particle(self.screen, self.rect.center, self.screen.particles)
        pg.transform.scale(particle.image, (self.rect.width*2, self.rect.height*2))

    def attack(self):
        self.screen.game.music.play_sound(self.attack_sound)

    def animate(self):
        super().animate()
        if self.direction == 'L':
            self.image = pg.transform.flip(self.active_anim.get_frame(self.elapsed_time),True,False)

    def move(self):
        pass

    def is_attack_finished(self):
        pass



    def update(self):
        super().update()
        # apply gravity
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
        if self.vel.y > PLAYER_MAX_FALL_SPEED:
            self.vel.y = PLAYER_MAX_FALL_SPEED
        if self.health == 0:
            self.screen.game.music.play_sound(self.death_sound)
            self.kill()
            self.alive = False


        #attack handling
        if self.is_attacking:
            if self.is_attack_finished():
                self.is_attacking = False
                self.character_attack.kill()
                self.character_attack = None
                self.screen.game.music.stop_sound(self.attack_sound)
            elif self.character_attack:
                self.character_attack.align(self) # good enough for now, mb has to be reworked for ranged attacks
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.particles_duration > self.particles_elapsed_time:
            self.particles_elapsed_time += 1/self.screen.game.ticks

        self.rect.midbottom = self.pos

class Particle(AnimatedSprite):
    ANIMATIONS = {
        'particle': (HIT_PARTICLES, 0.6, Animation.NORMAL),
    }
    def __init__(self, screen, pos, *groups):
        super().__init__(screen, groups)
        self.pos = vec(pos)
        self.sprite_type = 'particle'
        self.rect.midbottom = self.pos
        self.duration = 0.5

    def update(self):
        self.elapsed_time += 1/self.screen.game.ticks
        if self.elapsed_time >= self.duration:
            self.kill()


import pygame as pg

class BaseScreen:
    def __init__(self, game):
        self.game = game
        self.surface = game.surface
        self.clock = pg.time.Clock()

    def create_button(self, text, font, color, hover_color, rect):
        mouse_pos = pg.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pg.draw.rect(self.surface, hover_color, rect)
        else:
            pg.draw.rect(self.surface, color, rect)
        button_text = font.render(text, True, (0, 0, 0))  # Black text
        self.surface.blit(button_text, button_text.get_rect(center=rect.center))

    def draw_text(self, text, font, color, pos):
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=pos)
        self.surface.blit(text_surface, text_rect)

    def display(self):
        pg.display.flip()


