import pygame

class GameObject(pygame.sprite.Sprite):
    # Create global Groups visible to all Objects
    all_collision_objects = pygame.sprite.Group()
    all_enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    def __init__(self, x, y, width, height):
        # Call init from sprite.Sprite
        super().__init__()
        # Add myself to all_sprites-Group
        self.all_sprites.add(self)
        # Create Surface to display
        self.image = pygame.Surface((width, height))
        # Create the rect-Handle for this object
        self.rect = self.image.get_rect(width=width, height=height)
        # Physics placeholder
        self.physics = None
        # Sound placeholder
        self.sound = None
        # Default speed of this object
        self.speed = 0
        # The position of this Object
        self.position = pygame.Vector2(x, y)
        # Set the initial position to (x, y) with the topleft handle of .rect
        self.rect.topleft = self.position


    # Update is called on every Frame
    def update(self):
        self.collision_checks()
        # run physics routine if defined
        if self.physics is not None:
            self.physics.update()


    # Check for collisions - do nothing per default
    def collision_checks(self):
        # overload this function in the child object
        pass


