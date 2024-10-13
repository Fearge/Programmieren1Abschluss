from base_sprite import *
class Attack(AnimatedSprite):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'walking': (WALKING_FRAMES, 0.12, LOOP)
    }
    def __init__(self, screen, damage, entity_id, *groups):
        super().__init__(screen,groups)

        # properties
        self.pos = vec(0, 0)
        self.damage = damage
        self.entity_id = entity_id

        self.attack_length = 50
        self.__attack_duration = 0

        self.rect.midbottom = self.pos

    @property
    def attack_duration(self):
        return self.__attack_duration

    def align(self, entity):
        offset = vec(entity.rect.width, 0) if entity.direction == 'R' else vec(-entity.rect.width, 0)
        self.pos = entity.pos + offset
        if entity.direction == 'L':
            self.image = pg.transform.flip(self.image, True, False)

    def update(self):
        super().update()
        self.__attack_duration += 1
        self.rect.midbottom = self.pos


# for possible future development of character-specific attacks
class PlayerAttack(Attack):
    def __init__(self, screen, damage, entity_id, *groups):
        super().__init__(screen, damage, entity_id, *groups)


class ChargeAttack(Attack):
    def __init__(self, screen, damage, entity_id, *groups):
        super().__init__(screen, damage, entity_id, *groups)

