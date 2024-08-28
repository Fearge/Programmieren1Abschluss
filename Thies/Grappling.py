import pygame
import math

# Konstante für die Fenstergröße
WIDTH, HEIGHT = 800, 600

# Farben (RGB)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Farbe für Plattformen
BROWN = (139, 69, 19)  # Farbe für den Boden

# Schwerkraft-Konstante
GRAVITY = 1
HOOK_SPEED = 20  # Geschwindigkeit des Enterhakens
HOOK_PULL_SPEED = 10 # Geschwindigkeit, mit der der Charakter zum Enterhaken gezogen wird

class GameObject:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 0, 255), self.rect)


class Player(GameObject):
    def __init__(self, x, y, width, height, speed, image_path):
        super().__init__(x, y, width, height)
        self.speed = speed
        self.velocity_y = 0
        self.is_jumping = False
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.is_using_hook = False
        self.hook = None
        self.platforms = []
        self.ceiling = None
        self.ground = None

    def move(self):
        keys = pygame.key.get_pressed()
        if not self.is_using_hook:
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed

            # Sprunglogik
            if not self.is_jumping and keys[pygame.K_SPACE]:
                self.is_jumping = True
                self.velocity_y = -15  # Initiale Aufwärtsgeschwindigkeit beim Springen

            # Schwerkraft anwenden
            self.velocity_y += GRAVITY
            self.rect.y += self.velocity_y

            # Kollision mit dem Boden oder Plattformen
            self.check_collisions()

        else:
            # Bewegung mit Enterhaken
            self.hook_movement()

    def check_collisions(self):
        if self.ground and self.rect.colliderect(self.ground.rect):
            if self.velocity_y > 0:
                self.rect.bottom = self.ground.rect.top
                self.is_jumping = False
                self.velocity_y = 0

        for platform in self.platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.rect.top
                    self.is_jumping = False
                    self.velocity_y = 0
                elif self.velocity_y < 0:
                    self.rect.top = platform.rect.bottom
                    self.velocity_y = 0

    def hook_movement(self):
        if self.hook:
            hook_x, hook_y, start_x, start_y = self.hook
            direction_x = hook_x - start_x
            direction_y = hook_y - start_y
            distance = math.hypot(direction_x, direction_y)

            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                start_x += direction_x * HOOK_SPEED
                start_y += direction_y * HOOK_SPEED

                # Erstelle ein Rechteck für den Enterhaken
                hook_rect = pygame.Rect(start_x, start_y, 10, 10)

                if hook_rect.colliderect(self.ceiling.rect) or \
                   any(hook_rect.colliderect(platform.rect) for platform in self.platforms) or \
                   hook_rect.colliderect(self.ground.rect):
                    self.velocity_y = 0  # Schwerkraft zurücksetzen
                    self.pull_to_hook(start_x, start_y)
                elif (start_x < 0 or start_x > WIDTH or start_y < 0 or start_y > HEIGHT):
                    # Wenn der Enterhaken den Bildschirm verlässt, wird er abgebrochen
                    self.hook = None
                    self.is_using_hook = False
                else:
                    self.hook = (hook_x, hook_y, start_x, start_y)

    def pull_to_hook(self, hook_x, hook_y):
        direction_x = hook_x - self.rect.centerx
        direction_y = hook_y - self.rect.centery
        distance = math.hypot(direction_x, direction_y)

        if distance > 0:
            direction_x /= distance
            direction_y /= distance
            self.rect.x += direction_x * HOOK_PULL_SPEED
            self.rect.y += direction_y * HOOK_PULL_SPEED

            if distance < HOOK_PULL_SPEED:
                self.rect.centerx = hook_x
                self.rect.centery = hook_y
                self.is_using_hook = False

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.is_using_hook:
            start_x, start_y = self.hook[2], self.hook[3]
            pygame.draw.line(surface, BLACK, self.rect.midtop, (start_x, start_y), 2)


class Ceiling(GameObject):
    def __init__(self, x, y, width, height, color=GRAY):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Platform(GameObject):
    def __init__(self, x, y, width, height, color=GREEN):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Ground(GameObject):
    def __init__(self, x, y, width, height, color=BROWN):
        super().__init__(x, y, width, height)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pygame mit Enterhaken")
        self.clock = pygame.time.Clock()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(WHITE)
        self.player = Player(100, HEIGHT - 100, 50, 50, 5, 'Hugo.jpg')  # Bildpfad anpassen
        self.ceiling = Ceiling(0, 0, WIDTH, 100)  # Breitere Decke
        self.ground = Ground(0, HEIGHT - 50, WIDTH, 50)  # Boden hinzufügen
        self.platforms = [
            Platform(100, HEIGHT - 150, 200, 20),  # Plattform 1
            Platform(400, HEIGHT - 300, 200, 20),  # Plattform 2
            Platform(200, HEIGHT - 450, 200, 20)   # Plattform 3
        ]
        self.player.ceiling = self.ceiling  # Decke dem Spieler zuweisen
        self.player.platforms = self.platforms  # Plattformen dem Spieler zuweisen
        self.player.ground = self.ground  # Boden dem Spieler zuweisen
        self.running = True

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_e:  # Enterhaken aktivieren
                        if not self.player.is_using_hook:  # Nur starten, wenn der Enterhaken nicht schon in Benutzung ist
                            self.player.is_using_hook = True
                            start_pos = self.player.rect.midtop  # Startposition des Enterhakens anpassen
                            mouse_pos = pygame.mouse.get_pos()
                            direction_x = mouse_pos[0] - start_pos[0]
                            direction_y = mouse_pos[1] - start_pos[1]
                            magnitude = math.hypot(direction_x, direction_y)
                            if magnitude > 0:
                                # Erweitere den Mauszeiger über die Mausposition hinaus
                                extended_mouse_pos = (start_pos[0] + direction_x * 1000, start_pos[1] + direction_y * 1000)
                                self.player.hook = (extended_mouse_pos[0], extended_mouse_pos[1], start_pos[0], start_pos[1])
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_e:  # Enterhaken deaktivieren
                        self.player.is_using_hook = False
                        self.player.hook = None

            self.player.move()
            self.screen.blit(self.background, (0, 0))
            self.ceiling.draw(self.screen)  # Decke zeichnen
            self.ground.draw(self.screen)   # Boden zeichnen
            for platform in self.platforms:
                platform.draw(self.screen)  # Plattformen zeichnen
            self.player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
