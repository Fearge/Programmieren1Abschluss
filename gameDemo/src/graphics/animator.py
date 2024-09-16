import pygame
import os
class Animator:
    def __init__(self,
                 parent=None,
                 rotation: int = 0,
                 animation_filename: str = "",
                 animation_speed: int = 60,
                 animation_frames: int = 6,
                 animation_frame_height: int = 0,
                 animation_frame_width: int = 0):
        self._changed_filename = True
        self._animation_filename = animation_filename
        self._parent = parent
        self._rotation = rotation
        self._animation_step = 0
        self.animation_speed = animation_speed
        self.animation_frames = animation_frames
        if animation_frame_height > 0:
            self._animation_frame_height = animation_frame_height
        else:
            self._animation_frame_height = self._parent.height
        if animation_frame_width > 0:
            self._animation_frame_width = animation_frame_width
        else:
            self._animation_frame_width = self._parent.width

        self._animation_last = 0

        # load the sprite image
        self.set_filename(self._animation_filename)
        self.load_image()

        # get the .rect
        #self.rect = self._parent.image.get_rect()


    def update(self):
        if self._changed_filename:
            self.load_image()
        st = pygame.time.get_ticks()
        # check if we should animate
        if self._animation_speed < st - self._animation_last:
            self._animation_last = st
            self._animation_step -= 1
            # get next frame index
            frame = self._animation_step % self._animation_frames
            # blackout the image
            self._parent.image.fill((0, 0, 0))
            if self._rotation == 0 or self._rotation == 180:
                x1 = self._animation_frame_width * frame
                y1 = 0
                x2 = self._animation_frame_width * (frame + 1)
                y2 = self._animation_frame_height
            elif self._rotation == 90 or self._rotation == 270:
                x1 = 0
                y1 = self._animation_frame_height * frame
                x2 = self._animation_frame_width * frame
                y2 = self._animation_frame_height * (frame + 1)
            # draw new frame
            self._parent.image.blit(self._sprite_sheet,
                            (0, 0),
                            area=(x1, y1, x2, y2))

    def set_filename(self, filename: str, animation_frames: int = 0) -> None:
        if self._animation_filename != filename:
            if animation_frames != 0:
                self.animation_frames = animation_frames
            self._animation_filename = filename
            self._changed_filename = True


    def load_image(self):
        self._sprite_sheet = pygame.image.load(os.path.join('assets', 'images', self._animation_filename))
        # set the animation frame size to framesize and framesize * animation_frames
        self._sprite_sheet = pygame.transform.scale(self._sprite_sheet,
                                                    (self._animation_frame_width * self._animation_frames,
                                                     self._animation_frame_height))
        # the image needs rotation
        self._sprite_sheet = pygame.transform.rotate(self._sprite_sheet, self._rotation)
        # create a surface to render the animation
        self._parent.image = pygame.Surface((self._animation_frame_width, self._animation_frame_height)).convert()
        # blackout surface
        self._parent.image.fill((0, 0, 0))
        # set alpha to black
        self._parent.image.set_colorkey((0, 0, 0))
        self._changed_filename = False

    @property
    def animation_frames(self) -> int:
        return self._animation_frames
    @animation_frames.setter
    def animation_frames(self, value: int = 1) -> None:
        self._animation_frames = value

    @property
    def animation_speed(self) -> int:
        return self._animation_speed
    @animation_speed.setter
    def animation_speed(self, value: int = 1) -> None:
        self._animation_speed = value