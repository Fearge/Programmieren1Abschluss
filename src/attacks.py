from base_sprite import *
class Attack(AnimatedSprite):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.12, LOOP)
    }
    def __init__(self, screen, damage, follow_player, entity, length: 50, *groups):
        super().__init__(screen, groups)

        # properties
        self.pos = vec(0, 0)
        self.damage = damage
        self.followPlayer = follow_player
        self.entity = entity

        self.attack_length = length
        self.__attack_duration = 0

        self.load()
        self.image = self.active_anim.get_frame(0)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


    @property
    def attack_duration(self):
        return self.__attack_duration

    def align(self, entity):
        if entity.direction == 'R':
            self.rect.center = entity.pos + (entity.rect.width, -entity.rect.height / 2)
        elif entity.direction == 'L':
            self.rect.center = entity.pos - (entity.rect.width, entity.rect.height / 2)
        self.pos = entity.pos

    def update(self):
        super().update(1 / self.screen.game.fps)
        self.__attack_duration += 1
        if self.__attack_duration > self.attack_length:
            self.kill()
            print('killed')