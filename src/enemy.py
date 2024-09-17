from sprites import *
class Enemy(Character):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
            'walking': (WALKING_FRAMES, 0.12, Animation.LOOP),
        }
    _id_counter = 0
    def __init__(self, screen, pos, *groups):
        super().__init__(pos, 10 ,groups)
        # properties
        self.screen = screen
        self.prev_pos = vec(pos)
        self.id = Enemy._id_counter
        Enemy._id_counter += 1

        self.stuck_count = 0
        self.stuck_threshold = 10
        self.range_threshold = 100
        self.isPlayerNear = False

        self.attacks = pg.sprite.Group()
        self.attack_cooldown = 0

        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.movement_tick = 0


    # idle animation
    def move(self):
         #init velocity
        if self.vel.x == 0:
            self.vel.x = ENEMY_VEL
        #moving left and right
        self.movement_tick += 1
        if self.movement_tick % 100 == 0:
            self.vel.x *= -1
        #reverse friction
        self.acc.x = self.vel.x * 0.12
        super().move()

    def handle_events(self, event):
        pass

    def stop(self):
        self.vel = vec(0,0)

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
        if abs(self.pos.y - player.pos.y) < 10:
            return abs(self.pos.x-player.pos.x) < threshold
        return False

    def update(self, dt = 1):
        super().update(1/self.screen.game.fps)

        self.check_stuck()
        #self.animate()
        self.prev_pos = vec(self.pos)

        if self.is_player_near(self.screen.player, self.range_threshold):
            pg.event.post(pg.event.Event(pg.USEREVENT, {f'enemy': self.id}))
            self.isPlayerNear = True
        else:
            self.isPlayerNear = False

        self.rect.midbottom = self.pos

class MeleeEnemy(Enemy):
    def __init__(self, screen, pos, *groups):

        self.isCharging = False
        self.playerPos = vec(0,0)
        super().__init__(screen, pos, groups)
        self.range_threshold = 500

    def charge(self, pos):
        direction = pos - self.pos
        if direction.length() > 0:
            direction = direction.normalize()
        self.vel.x = direction[0] * ENEMY_CHARGE

    def attack_player(self):
        attack = Attack(self.screen, 10, True, self.attacks)
        attack.align(self)

    def handle_events(self, event):
        if event.type == pg.USEREVENT:
            if event.dict.get('enemy') == self.id and self.attack_cooldown == 0:
                print('player near')
                self.attack_player()
                self.isCharging = True
                self.playerPos = self.screen.player.pos

    def update(self):
        super().update()
        self.attacks.update()

        for attack in self.attacks:
            if attack.followPlayer:
                attack.align(self)
            self.attack_cooldown = 100
            self.charge(self.playerPos)
            if self.isCharging and self.pos.distance_to(self.playerPos) == 0:
                self.stop()
                self.isCharging = False


        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

        """if self.isCharging and self.pos.distance_to(self.playerPos) == 0:
            self.stop()
            self.isCharging = False"""




class RangedEnemy(Enemy):
    def __init__(self, screen, pos, *groups):
        self.attacks = pg.sprite.Group()
        super().__init__(screen, pos, groups)
        super.range_threshold = 300

    """def attack_player(self):
        if self.attack_cooldown == 0:
            projectile = Projectile(self.screen, self.pos, self.screen.player.pos, self.attacks)
            self.attack_cooldown = 100  # Cooldown period before the next attack
"""
    def handle_events(self, event):
        if event.type == pg.USEREVENT:
            if event.dict.get('enemy') == self.id and self.attack_cooldown == 0:
                pass

    def update(self):
        super().update()
        self.attacks.update()
        if self.isPlayerNear:
            self.attack_player()

