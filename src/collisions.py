
from src.attacks import Attack
from src.base_sprite import Character, vec
from constants import *
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


def attack_collision(attack: Attack, character: Character):
    if attack.entity_id != character.__str__() and attack.has_hit == False:
        character.get_hit(attack.damage)
        attack.has_hit = True
        attack.kill()

def hook_collision(hook, screen):
    hook.vel = vec(0, 0)
    hook.is_attached = True
    screen.game.music.play_sound(GRAPPLE_CONNECT_SOUND_PATH)
