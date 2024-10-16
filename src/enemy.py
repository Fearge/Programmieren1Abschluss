from player import *
from attacks import ChargeAttack,ShootAttack
from health_bar import HealthBar
import asyncio



class Enemy(Character):
    # implement colorkey if needed, standard: (34, 177, 76)
    _id_counter = 0
    def __init__(self, screen, pos,health, *groups):
        super().__init__(screen, pos,health, *groups)
        # properties
        self.prev_pos = vec(pos)
        self.id = Enemy._id_counter # for identification of enemy instances
        Enemy._id_counter += 1

        self.health_bar = HealthBar(self.pos.x, self.pos.y, 50, 10, self.health)
        self.hit_sound = ENEMY_OUCH_SOUND_PATH
        self.death_sound = ENEMY_DEATH_SOUND_PATH

        self.range_threshold = 100
        self.is_attacking = False

        self.attack_cooldown = 0

        self.rect.midbottom = self.pos
        self.movement_tick = 0

    def __str__(self):
        return f'enemy_{self.id}'

    # idle animation
    def move(self):
        #init velocity and acceleration
        self.acc.x = self.vel.x * 0.12
        # moving left and right
        if self.direction == 'R':
            self.vel.x = ENEMY_VEL
        else: self.vel.x = -ENEMY_VEL

        #reverses direction every 100 ticks
        self.movement_tick += 1
        if self.movement_tick % 100 == 0:
            self.vel.x *= -1
        super().flip_image_on_direction()

    def handle_events(self, event):
        pass

    # returns true if player is within threshold
    def is_player_near(self, player, threshold):
        if abs(self.pos.y - player.pos.y) < 10:
            return abs(self.pos.x-player.pos.x) < threshold
        return False

    def update(self):
        super().update()
        self.prev_pos = vec(self.pos)
        if self.is_player_near(self.screen.player, self.range_threshold):
            pg.event.post(pg.event.Event(pg.USEREVENT, {f'enemy': self.id}))
        self.health_bar.rect.x = self.rect.x
        self.health_bar.rect.y = self.rect.y - 10
        self.health_bar.update(self.health)
        self.rect.midbottom = self.pos


def start_event_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

class MeleeEnemy(Enemy):
    ANIMATIONS = {
        'enemy_walking': (MELEE_ENEMY_WALKING_FRAMES, 0.6, Animation.LOOP),
    }
    def __init__(self, screen, pos, *groups):
        self.health = MELEE_ENEMY_HEALTH
        self.charge_target_pos = (0,0)
        super().__init__(screen, pos,MELEE_ENEMY_HEALTH, *groups)
        self.range_threshold = 200
        self.attack_sound = CHARGE_SOUND

    # charge attack
    def move(self):
        if not self.is_attacking:
            super().move()
        else:
            self.vel = self.calculate_charge_direction(self.charge_target_pos)
            super().flip_image_on_direction()

    def calculate_charge_direction(self, target_pos):
        direction = target_pos - self.pos
        try:
            direction = direction.normalize() # if vector is zero it cant be normalized
        except ValueError:
            return None
        return direction * ENEMY_CHARGE

    def is_attack_finished(self):
        return self.pos.distance_to(self.charge_target_pos) < 5

    def attack(self): # maybe make this async
        self.charge_target_pos = vec(self.screen.player.pos)
        self.is_attacking = True
        self.character_attack = ChargeAttack(self.screen, CHARGE_ATTACK_DAMAGE, self.__str__(), self.screen.attacks)
        self.character_attack.align(self)
        super().attack()

    def handle_events(self, event):
        if event.type == pg.USEREVENT:
            if event.dict.get('enemy') == self.id and self.attack_cooldown == 0:
                self.attack()
                self.attack_cooldown = ENEMY_CHARGE_COOLDOWN  # Cooldown period before the next attack

    def update(self):
        super().update()

class RangedEnemy(Enemy):
    ANIMATIONS = {
        'enemy_walking': (RANGED_ENEMY_WALKING_FRAMES, 0.6, Animation.LOOP),
    }
    def __init__(self, screen, pos, *groups):
        self.health = RANGED_ENEMY_HEALTH
        super().__init__(screen, pos, RANGED_ENEMY_HEALTH, *groups)
        self.range_threshold = 300
        self.attack_sound = LASER_SOUND_PATH


    def attack(self):
        direction = self.screen.player.pos - self.pos
        self.character_attack = ShootAttack(self.screen, self.rect.center, direction, RANGE_ATTACK_DAMAGE,self.__str__(), self.screen.attacks)
        super().attack()

    def move(self):
        if self.is_attacking:
            self.vel = vec(0,0)
        else: super().move()

    def is_attack_finished(self):
        return self.character_attack.pos.x == WIDTH or 0

    def handle_events(self, event):
        if event.type == pg.USEREVENT:
            if event.dict.get('enemy') == self.id and self.attack_cooldown == 0:
                print('player near')
                self.attack()
                self.attack_cooldown = RANGED_ENEMY_COOLDOWN

    def update(self):
        super().update()
