import vector
from colors import *
import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed_scalar, speed_vector, health, radius, color):
        super().__init__()

        self.color = color.copy()
        self.pos = pos
        self.radius = radius
        self.speed = vector.times(speed_scalar, speed_vector)
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.circle(self.image, color, (radius, radius), radius, )
        self.origin = pos[0] + radius, pos[1] + radius
        self.rect = self.image.get_rect()
        self.crossed_checkpoints = []
        self.index = 0
        self.move_origin(pos)
        self.distance_travelled = 0
        self.start_health = health
        self.health = health

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin = pos[0] + self.radius, pos[1] + self.radius
        self.pos = pos

    def move_origin(self, pos):
        self.origin = pos
        self.pos = [self.origin[0] - self.radius, self.origin[1] - self.radius]
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    def apply_speed(self):
        self.pos = vector.plus(self.pos, self.speed)
        self.set_position(self.pos)
        self.distance_travelled += vector.mag(self.speed)

    def draw_image(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius, )

    def hit_checkpoint(self, map):
        tile_sprites = map.tiles.sprites()
        for checkpoint in map.checkpoints:
            distance_vector = [checkpoint.origin[0] - self.origin[0], checkpoint.origin[1] - self.origin[1]]
            if vector.mag(distance_vector) < checkpoint.size:

                if self.speed[0] == 0:

                    # Moving UP
                    if self.speed[1] < 0 and checkpoint.rect.centery > self.rect.centery and checkpoint not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(checkpoint)
                        # Turning RIGHT
                        if tile_sprites[checkpoint.index - 2].color == grass:
                            self.speed = [-1 * self.speed[1], self.speed[0]]
                        # Turning LEFT
                        else:
                            self.speed = [self.speed[1], self.speed[0]]
                        self.move_origin(checkpoint.origin)

                    # Moving DOWN
                    if self.speed[1] > 0 and checkpoint.rect.centery < self.rect.centery and checkpoint not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(checkpoint)
                        # Turning RIGHT
                        if tile_sprites[checkpoint.index - 2].color == grass:
                            self.speed = [self.speed[1], self.speed[0]]
                        # Turning LEFT
                        else:
                            self.speed = [-1 * self.speed[1], self.speed[0]]
                        self.move_origin(checkpoint.origin)

                elif self.speed[1] == 0:

                    # Moving LEFT
                    if self.speed[0] < 0 and checkpoint.rect.centerx > self.rect.centerx and checkpoint not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(checkpoint)
                        # Turning DOWN
                        if tile_sprites[checkpoint.index - 2 * map.width].color == grass:
                            self.speed = [self.speed[1], -1 * self.speed[0]]
                        # Turning UP
                        else:
                            self.speed = [self.speed[1], self.speed[0]]
                        self.move_origin(checkpoint.origin)

                    # Moving RIGHT
                    if self.speed[0] > 0 and checkpoint.rect.centerx < self.rect.centerx and checkpoint not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(checkpoint)
                        # Turning DOWN
                        if tile_sprites[checkpoint.index - 2 * map.width].color == grass:
                            self.speed = [self.speed[1], self.speed[0]]
                        # Turning UP
                        else:
                            self.speed = [self.speed[1], -1 * self.speed[0]]
                        self.move_origin(checkpoint.origin)

    def hit_base(self, map):
        if pygame.sprite.collide_rect(self, map.end):
            self.kill()

    def update(self, map):
        self.apply_speed()
        self.hit_checkpoint(map)
        self.hit_base(map)
        self.check_health()
        self.hit_bullet(map)

    def check_health(self):
        if self.health <= 0:
            self.die()

    def hit_bullet(self, game):
        if pygame.sprite.spritecollide(self, game.bullet_group, True):
            self.health += -1
            self.color[0] += 255 / self.start_health
            self.color[2] += -255 / self.start_health
            if self.color[2] < 0:
                self.die()
            else:
                self.draw_image()

    def die(self):
        self.kill()

class Boss(Enemy):
    def __init__(self, map):
        pos = map.start.origin
        start_speed = map.starting_vector
        super().__init__(pos, 1, start_speed, 10, 20, blue)