from base_sprite import *
class Attack(AnimatedSprite):
    # implement colorkey if needed, standard: (34, 177, 76)
    ANIMATIONS = {
        'Swooshing': (SWOOSHING_FRAMES, 0.6, NORMAL)
    }
    def __init__(self, screen, damage, entity_id, *groups):
        super().__init__(screen,groups)

        # properties
        self.pos = vec(0, 0)
        self.damage = damage
        self.entity_id = entity_id
        self.__attack_duration = 0
        self.has_hit = False
        self.sprite_type = 'attack'
        self.direction = 'R'

        self.rect.midbottom = self.pos

    @property
    def attack_duration(self):
        return self.__attack_duration

    def align(self, entity: Character):
        self.direction = entity.direction
        offset = vec(entity.rect.width/2, -entity.rect.height/2) if entity.direction == 'R' else vec(-entity.rect.width/2, -entity.rect.height/2)
        self.pos = entity.pos + offset


    def update(self):
        super().update()
        self.__attack_duration += 1
        self.rect.midbottom = self.pos
        if self.direction == 'L':
            self.image = pg.transform.flip(self.image, True, False)





# for possible future development of character-specific attacks
class PlayerAttack(Attack):
    def __init__(self, screen, damage, entity_id, *groups):
        super().__init__(screen, damage, entity_id, *groups)

class ChargeAttack(Attack):
    def __init__(self, screen, damage, entity_id, *groups):
        super().__init__(screen, damage, entity_id, *groups)

class ShootAttack(Attack):
    def __init__(self, screen,pos, direction, damage, entity_id, *groups):
        super().__init__(screen, damage, entity_id, *groups)
        self.image = pg.Surface((10,10))
        self.image.fill(pg.Color('red'))
        self.pos = pos
        self.rect = self.image.get_rect(center=self.pos)
        self.direction = direction.normalize()
        self.damage = damage

    def animate(self):
        pass

    def align(self, entity: Character):# no need do do alignment
        pass

    def update(self):
        self.pos += self.direction * ENEMY_BULLET_SPEED
        self.rect.center = self.pos
        super().update()

