
from base_sprite import *
from spritesheet import Animation
from attacks import PlayerAttack



class Player(Character):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.12, Animation.LOOP),
        'standing': (STANDING_FRAMES, 0.20, LOOP),
        'jumping': (JUMPING_FRAMES, 0.10, NORMAL),
        'falling': (FALLING_FRAMES, 0.10, NORMAL),
        'landing': (LANDING_FRAMES, 0.10, NORMAL)
    }
    _id_counter = 0
    def __init__(self, screen, pos, *groups):
        super().__init__(screen,pos,  groups)
        # properties
        self.jump_release = 0
        self.attack_cooldown = 0
        self.id = Player._id_counter
        Player._id_counter += 1

        # Grappling hook
        self.grappling_hook = None
        self.__is_grappling = False
        self.__pull_target_pos = vec(0, 0)
        self.__is_pulling = False

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

    def __str__(self):
        return f'Player_{self.id}'

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
        super().flip_image_on_direction()

    def attack(self):
        self.character_attack = PlayerAttack(self.screen, 10, self.__str__(), self.screen.attacks)
        self.character_attack.align(self)
        self.is_attacking = True
        print('attack')

    def is_attack_finished(self):
        return self.character_attack.attack_duration > self.character_attack.attack_length


    def handle_events(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE and self.attack_cooldown == 0:
                self.attack()
                self.attack_cooldown = PLAYER_ATT_COOLDOWN

    def update(self):
        super().update()
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

