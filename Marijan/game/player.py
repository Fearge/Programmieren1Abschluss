import pygame
from .object import GameObject
from .physics import PhysicsEngine
from .attack import Attack

class Player(GameObject):
    def __init__(self, x, y, width, height):
        # Call the GameObject.__init__
        super().__init__(x=x, y=y, width=width, height=height)
        # Set the style
        self.image.fill((0, 0, 255))  # Blue
        # Add physics to this object
        self.physics = PhysicsEngine(parent=self)
        # Set default speed
        self.speed = 2
        # Add a Score
        self.score = 0

    def update(self, screen):
        # Call all .update() logic from GameObject - Important!
        super().update()
        # Define the Movement of this Object
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.physics.velocity.x = -4 * self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
            self.physics.velocity.x = 4 * self.speed
        if keys[pygame.K_w] and self.physics.is_grounded():
            # Object can only jump if it has contact to the floor
            self.physics.velocity.y += -4*self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        # Set the new position of this object
        self.position = (self.rect.x, self.rect.y)

    def collision_checks(self):
        # define the collision behavior
        if len(pygame.sprite.spritecollide(self, self.all_enemies, True)) > 0:
            print("Enemy Collision")
            # Fire an event to react anywhere
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"reason": "enemy_killed"}))
        # get platform collision
        platforms = pygame.sprite.spritecollide(self, self.all_collision_objects, False)
        if len(platforms) > 0:
            # pick the first one
            platform = platforms[0]
            # set the object position on top of this platform
            self.rect.bottom = platform.rect.top
            # check if the object falls too hard on this object
            if self.physics.velocity.y > 20:
                print("Outch")
                color = self.image.get_at((0, 0))
                if color.r + 100 < 255 and color.b - 100 > 0:
                    color.r += 100
                    color.b -= 100
                    self.image = pygame.transform.scale(self.image, (self.rect.width//2, self.rect.height//2))
                    self.rect.width = self.image.get_width()
                    self.rect.height = self.image.get_height()
                    self.image.fill(color)
                else:
                    self.player_died()
            # set the physics._grounded to True
            self.physics.set_grounded(True)
        else:
            # object is in the air (not _grounded)
            self.physics.set_grounded(False)

    def get_velocity(self):
        return self.physics.velocity

    def get_speed(self):
        return self.speed

    def player_died(self):
        # destroy this object
        self.kill()
        # fire event
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"reason": "player_died"}))

    def attack(self,attack):
        attack.start_attack()
       # attack.follow_player(self)
