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

        animations = {
            'walking': (WALKING_FRAMES, 0.12, Animation.PlayMode.LOOP),
            'standing': (STANDING_FRAMES, 0.20, Animation.PlayMode.LOOP),
            'jumping': (JUMPING_FRAMES, 0.10, Animation.PlayMode.NORMAL),
            'falling': (FALLING_FRAMES, 0.10, Animation.PlayMode.NORMAL),
            'landing': (LANDING_FRAMES, 0.10, Animation.PlayMode.NORMAL)
        }

        for name, (frames, duration, mode) in animations.items():
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
        self.has_attacked = False
        self.isPlayerNear = False


        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.vel.x = ENEMY_VEL
        self.movement_tick = 0

    def load(self):
        spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), colorkey=(34, 177, 76))

        animations = {
            'walking': (WALKING_FRAMES, 0.12, Animation.PlayMode.LOOP),
        }

        for name, (frames, duration, mode) in animations.items():
            anim = spritesheet.get_animation(frames, duration, mode, scale=1.2)
            self.store_animation(name, anim)

    def animate(self):
        if self.vel.x > 0:
            self.image = self.active_anim.get_frame(self.elapsed_time)
        else:
            self.image = pg.transform.flip(self.active_anim.get_frame(self.elapsed_time), True, False)

    # idle animation
    def move(self):
        self.movement_tick += 1
        if self.movement_tick % 100 == 0:
            self.vel.x *= -1

        self.acc.x = self.vel.x * 0.12


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

    def is_player_near(self, player, threshold):
        distance = self.pos.distance_to(player.pos)
        return distance < threshold

    def update(self, dt = 1):
        super().update(1/self.screen.game.fps)

        self.check_stuck()
        self.animate()
        self.prev_pos = vec(self.pos)

        if self.is_player_near(self.screen.player, 300):
            pg.event.post(pg.event.Event(pg.USEREVENT, {'enemy':'near_player'}))
            self.isPlayerNear = True
        else:
            self.isPlayerNear = False

        self.rect.midbottom = self.pos

class MeleeEnemy(Enemy):
    def __init__(self, screen, pos, *groups):
        super().__init__(screen, pos, groups)
        self.attacks = pg.sprite.Group()
        self.attack = Attack(screen, 10, False, self.attacks)

    def move(self):
        if self.isPlayerNear and self.attack.cooldown == 0:
            direction = self.screen.player.pos - self.pos
            if direction.length() > 0:
                direction = direction.normalize()
            self.vel.x = direction[0] * ENEMY_CHARGE
            self.vel.y += ENEMY_VEL
        else:
            super().move()
            #self.move()# Idle movement, when player's not near

    def attack_player(self):
        self.attack.align(self)

    def handle_events(self, event):
        if event.type == pg.USEREVENT:
            if event.dict.get('enemy') == 'near_player' and not self.has_attacked:
                self.attack_player()
                self.has_attacked = True

    def update(self):
        super().update()
        self.attacks.update()
        for attack in self.attacks:
            self.attack_player()

class Attack(AnimatedSprite):
    def __init__(self, screen, damage, followPlayer, *groups):
        super().__init__(groups)

        # properties
        self.screen = screen
        self.pos = vec(0, 0)
        self.damage = damage
        self.followPlayer = followPlayer

        self.attack_length = 50
        self.__attack_duration = 0
        self.cooldown = 0
        self.__cooldown_timer = 0

        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def load(self):
        spritesheet = Spritesheet(path.join(self.screen.game.img_dir, 'batman_spritesheet.png'), colorkey=(34, 177, 76))
        animations = {
            'walking': (WALKING_FRAMES, 0.12, Animation.PlayMode.LOOP)
        }
        for name, (frames, duration, mode) in animations.items():
            anim = spritesheet.get_animation(frames, duration, mode, scale=1.2)
            self.store_animation(name, anim)

    def animate(self):
        self.image = self.active_anim.get_frame(self.elapsed_time)

    def align(self, entity):
        if entity.direction == 'R':
            self.rect.center = entity.pos + (entity.rect.width, -entity.rect.height / 2)
        elif entity.direction == 'L':
            self.rect.center = entity.pos - (entity.rect.width, entity.rect.height / 2)
        self.pos = entity.pos

    def is_ready(self):
        return self.__cooldown_timer == 0

    def reset_cooldown(self):
        self.__cooldown_timer = self.cooldown

    def update(self):
        super().update(1 / self.screen.game.fps)

        self.animate()
        self.__attack_duration += 1
        if self.__attack_duration > self.attack_length:
            self.kill()
            print('killed')
        if self.__cooldown_timer > 0:
            self.__cooldown_timer -= 1

