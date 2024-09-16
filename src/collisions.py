from constants import *
def collide_with_obstacles(character, hit):
	# character's bottom and obstacle top
	if abs(hit.rect.top - character.rect.bottom) < COLLISION_TOLERANCE:
		character.vel.y = 0
		character.pos.y = hit.rect.top + 1
		character.ground_count += 1

	# character's top and obstacle bottom
	if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE:
		character.vel.y = 0
		character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)

	if character.vel.y < 0:
		if abs(hit.rect.bottom - character.rect.top) < COLLISION_TOLERANCE + 30:
			character.vel.y = 0
			character.pos.y = (hit.rect.bottom - 1) + (character.rect.bottom - character.rect.top)

	# character's left and obstacle right
	if abs(hit.rect.right - character.rect.left) < COLLISION_TOLERANCE:
		character.vel.x = 0
		character.pos.x = hit.rect.right + character.rect.width/2 + 1

	# character's right and obstacle left
	if abs(hit.rect.left - character.rect.right) < COLLISION_TOLERANCE:
		character.vel.x = 0
		character.pos.x = hit.rect.left - character.rect.width/2 - 1

def collide_with_enemies(player):
	player.kill()

