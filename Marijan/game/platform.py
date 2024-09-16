from .object import GameObject

class Platform(GameObject):

    def __init__(self, x, y, width, height):
        super().__init__(x=x, y=y, width=width, height=height)
        self.image.fill((0, 255, 255))
        self.all_collision_objects.add(self)

    def update(self, screen = None):
        super().update()
