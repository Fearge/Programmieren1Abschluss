from pygame import Vector2
class PhysicsEngine:
    def __init__(self, parent=None):
        # Define any physics-related constants or variables here
        # needed parent to change the position of the physics-owner
        self.parent = parent
        self.gravity = Vector2(0, 0.5)
        self.velocity = Vector2(0, 0)
        self.mass = 1
        # flag if parent-object has contact to a collision object
        self._grounded = False


    def update_position(self):
        # update the parent position
        self.parent.position += self.velocity
        self.parent.rect.topleft = self.parent.position

    def apply_gravity(self):
        # apply the physics
        self.velocity += self.gravity

    def update(self):
        # apply gravity if not _grounded
        if not self._grounded:
            self.apply_gravity()
            self.update_position()
        else:
            pass


    def reset_velocity(self):
        self.velocity = Vector2(0, 0)

    def is_grounded(self):
        return self._grounded

    def set_grounded(self, grounded):
        if grounded:
            # reset velocity if grounded
            self.reset_velocity()
        self._grounded = grounded
