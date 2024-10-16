#----------------------------
#Sprites were generously crafted by Pascal Rosen & Tatjana Schmitt (Kommunikationsdesign)
#----------------------------


from base_sprite import *
from attacks import PlayerAttack
from src import Sprite
from src.grapple import GrapplingHook


class Player(Character):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.6, Animation.LOOP),
        'standing': (STANDING_FRAMES, 0.80, LOOP),
        'jumping': (JUMPING_FRAMES, 0.80, NORMAL),
        'enemy_walking': (MELEE_ENEMY_WALKING_FRAMES, 0.6, Animation.LOOP),
        'keuling': (KEULING_FRAMES, 0.6, NORMAL),
        'swooshing': (SWOOSHING_FRAMES, 0.6, NORMAL),
    }
    _id_counter = 0
    def __init__(self, screen, pos, *groups):
        super().__init__(screen, pos, PLAYER_HEALTH, *groups)
        # properties
        self.jump_release = 0
        self.attack_cooldown = 0
        self.id = Player._id_counter
        Player._id_counter += 1

        # Grappling hook
        self.grappling_hook = None
        self.__pull_target_pos = vec(0, 0)
        self.is_pulling = False
        self.hook_cooldown = 0

        self.rect.midbottom = pos
        self.width = self.rect.right - self.rect.left
        self.height = self.rect.top - self.rect.bottom

        #sounds
        self.attack_sound = PUNCH_SOUND_PATH
        self.hit_sound = HUGO_OUCH_SOUND_PATH
        self.death_sound = HUGO_DEATH_SOUND_PATH




    def animate(self):
        self.transitions = {
            "walking": [("standing", self.vel.x == 0), ("jumping", self.vel.y != 0),("keuling", self.is_attacking)],
            "standing": [("walking", abs(self.vel.x) > 0), ("jumping", self.vel.y != 0),("keuling", self.is_attacking)],
            "jumping": [("jumping", self.vel.y != 0),("standing",self.ground_count),("keuling", self.is_attacking)],
            "keuling": [("standing", self.character_attack is None)]
        }
        super().animate()

    def __str__(self):
        return f'Player_{self.id}'

    def move(self):
        keys = pg.key.get_pressed()
        # horizontal movement
        if keys[pg.K_a]:
            self.acc.x = -PLAYER_ACC

        elif keys[pg.K_d]:
            self.acc.x = PLAYER_ACC

        # jumping
        if keys[pg.K_SPACE]:
            if self.jump_release > 0:
                if self.ground_count > 0 and not self.active_name == 'falling':
                    self.vel.y = PLAYER_JUMP
                    self.ground_count = 0
                    self.jump_release = 0
                    self.screen.game.music.play_sound(HUGO_JUMP_SOUND_PATH)

        else:
            self.jump_release += 1
        super().flip_image_on_direction()

    def attack(self):
        self.character_attack = PlayerAttack(self.screen, PLAYER_DAMAGE, self.__str__(), self.screen.attacks)
        self.character_attack.align(self)
        self.is_attacking = True
        super().attack()

    def is_attack_finished(self):
        return self.character_attack.attack_duration > self.attack_cooldown

    def shoot_hook(self,target_pos: vec):
        if self.hook_cooldown == 0:
            self.grappling_hook = GrapplingHook(self.rect.center, self.screen.hooks)
            self.grappling_hook.is_shooting = True
            self.grappling_hook.vel = (target_pos - self.grappling_hook.pos).normalize() * SHOOT_SPEED
            self.hook_cooldown = PLAYER_HOOK_COOLDOWN
            self.screen.game.music.play_sound(GRAPPLE_SHOOT_SOUND_PATH)


    def pull(self):
        if self.is_pulling and self.grappling_hook:
            direction = (self.grappling_hook.pos - self.pos).normalize()
            self.vel = direction * PULL_SPEED
            self.acc = direction * PULL_ACC

    def stop_pull(self):
        self.grappling_hook.kill()
        self.grappling_hook = None

    def handle_events(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and self.attack_cooldown == 0: #attack on left mouse click
                self.attack()
                self.attack_cooldown = PLAYER_ATT_COOLDOWN
            elif event.button == 3:
                mouse_pos = self.screen.camera.get_mouse_pos_in_world()
                self.shoot_hook(mouse_pos)
        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 3 and self.grappling_hook:
                self.stop_pull()



    def update(self):
        if self.grappling_hook:
            if self.grappling_hook.is_attached:
                self.is_pulling = True
                self.pull()
        if self.hook_cooldown > 0:
            self.hook_cooldown -= 1
        super().update()



class Obstacle(Sprite):
    def __init__(self, pos, size, *groups):
        super().__init__(groups)
        self.sprite_type = 'obstacle'

        # rect
        self.rect = pg.Rect(pos, size)

        # position
        self.x = pos[0]
        self.y = pos[1]
        self.rect.x = pos[0]
        self.rect.y = pos[1]

