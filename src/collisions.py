from src.attacks import Attack
from src.base_sprite import Character, vec
import pygame as pg
from constants import *

class Quadtree:
    def __init__(self, level, bounds):
        self.level = level
        self.bounds = bounds
        self.objects = []
        self.nodes = []

    def clear(self):
        self.objects = []
        self.nodes = []

    def split(self):
        sub_width = self.bounds.width / 2
        sub_height = self.bounds.height / 2
        x = self.bounds.x
        y = self.bounds.y

        self.nodes = [
            Quadtree(self.level + 1, pg.Rect(x + sub_width, y, sub_width, sub_height)),
            Quadtree(self.level + 1, pg.Rect(x, y, sub_width, sub_height)),
            Quadtree(self.level + 1, pg.Rect(x, y + sub_height, sub_width, sub_height)),
            Quadtree(self.level + 1, pg.Rect(x + sub_width, y + sub_height, sub_width, sub_height))
        ]

    def get_index(self, rect):
        index = -1
        vertical_midpoint = self.bounds.x + (self.bounds.width / 2)
        horizontal_midpoint = self.bounds.y + (self.bounds.height / 2)

        top_quadrant = rect.y < horizontal_midpoint and rect.y + rect.height < horizontal_midpoint
        bottom_quadrant = rect.y > horizontal_midpoint

        if rect.x < vertical_midpoint and rect.x + rect.width < vertical_midpoint:
            if top_quadrant:
                index = 1
            elif bottom_quadrant:
                index = 2
        elif rect.x > vertical_midpoint:
            if top_quadrant:
                index = 0
            elif bottom_quadrant:
                index = 3

        return index

    def insert(self, obj):
        if self.nodes:
            index = self.get_index(obj.rect)
            if index != -1:
                self.nodes[index].insert(obj)
                return

        self.objects.append(obj)

        if len(self.objects) > 10 and self.level < 5:
            if not self.nodes:
                self.split()

            i = 0
            while i < len(self.objects):
                index = self.get_index(self.objects[i].rect)
                if index != -1:
                    self.nodes[index].insert(self.objects.pop(i))
                else:
                    i += 1

    def retrieve(self, return_objects, rect):
        index = self.get_index(rect)
        if index != -1 and self.nodes:
            self.nodes[index].retrieve(return_objects, rect)

        return_objects.extend(self.objects)
        return return_objects


def collide_with_obstacles(character, hit):
    # character's bottom and obstacle top
    if abs(hit.rect.top - character.rect.bottom) < COLLISION_TOLERANCE:
        character.vel.y = 0
        character.pos.y = hit.rect.top + 1
        character.ground_count += 1
        return

    # character's top and obstacle bottom
    if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE:
        character.vel.y = 0
        character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)
        return


    # character's left and obstacle right
    if abs(hit.rect.right - character.rect.left) < COLLISION_TOLERANCE:
        character.vel.x = 0
        character.pos.x = hit.rect.right + character.rect.width/2 + 1
        return


    # character's right and obstacle left
    if abs(hit.rect.left - character.rect.right) < COLLISION_TOLERANCE:
        character.vel.x = 0
        character.pos.x = hit.rect.left - character.rect.width/2 - 1
        return


def attack_collision(attack: Attack, hit: Character):
    if attack.entity_id != hit.__str__() and attack.has_hit == False:
        print(hit.health)
        hit.health -= attack.damage
        print(hit.health)
        attack.has_hit = True

def hook_collision(hook):
    hook.vel = vec(0, 0)
    hook.is_attached = True
