import asyncio

from sprites import *
from attacks import ChargeAttack
class Enemy(Character):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
            'enemy_walking': (ENEMY_WALKING_FRAMES, 0.6, Animation.LOOP),
        }
    _id_counter = 0
    def __init__(self, screen, pos, *groups):
        super().__init__(screen, pos,groups)
        # properties
        self.prev_pos = vec(pos)
        self.id = Enemy._id_counter # for identification of enemy instances
        Enemy._id_counter += 1

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
        if self.health == 0:
            self.kill()
            self.alive = False
        self.rect.midbottom = self.pos


class MeleeEnemy(Enemy):
    def __init__(self, screen, pos, *groups):
        self.charge_target_pos = (0,0)
        super().__init__(screen, pos, groups)
        self.range_threshold = 200

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
            return vec(0,0)
        return direction * ENEMY_CHARGE

    def is_attack_finished(self):
        return self.pos.distance_to(self.charge_target_pos) < 5


    def attack_player(self): # maybe make this async
        self.charge_target_pos = vec(self.screen.player.pos)
        self.is_attacking = True
        self.character_attack = ChargeAttack(self.screen, 10, self.__str__(), self.screen.attacks)
        self.character_attack.align(self)

    def handle_events(self, event):
        if event.type == pg.USEREVENT:
            if event.dict.get('enemy') == self.id and self.attack_cooldown == 0:
                print('player near')
                self.attack_player()
                self.is_attacking = True
                self.attack_cooldown = ENEMY_CHARGE_COOLDOWN  # Cooldown period before the next attack

    def update(self):
        super().update()


"""class Boss(Enemy):
    def __init__(self, screen, pos, *groups):
        super().__init__(screen, pos, groups)
        self.range_threshold = 300
        
    def attack1(self):
        pass
    
    def attack2(self):
        pass

    """