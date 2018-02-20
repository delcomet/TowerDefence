import pygame
import vector
import button
import box
from pygame.constants import *
from colors import *


class Game:
    def __init__(self, map_name):
        global tile_group, checkpoint_group, road_group, base_group
        pygame.init()
        fr = open(map_name, "r")
        self.map_values = fr.readlines()
        fr.close()

        self.width_map = (len(self.map_values[0]) - 1)
        self.height_map = (len(self.map_values))

        self.tile_size = 20
        self.start_tile = None
        self.end_tile = None
        self.arena_size = [self.tile_size * self.width_map, self.tile_size * self.height_map]
        self.window_size = [self.tile_size * self.width_map + 250, self.tile_size * self.height_map + 150]
        self.window = pygame.display.set_mode(self.window_size)

        tile_group = pygame.sprite.OrderedUpdates()
        checkpoint_group = pygame.sprite.Group()
        base_group = pygame.sprite.Group()
        road_group = pygame.sprite.Group()

        self.mouse = pygame.mouse.get_pos()
        self.setup_map(map_name)
        self.end_tile.image = pygame.Surface([60, 100])
        self.end_tile.pos = self.end_tile.origin
        self.end_tile.rect = self.end_tile.image.get_rect()
        self.end_tile.rect.x = self.end_tile.pos[0] - self.end_tile.image.get_width() / 2
        self.end_tile.rect.y = self.end_tile.pos[1] - self.end_tile.image.get_height() / 2
        remainder = self.end_tile.rect.x + self.end_tile.image.get_width() - self.tile_size * self.width_map
        if remainder > 0:
            self.end_tile.rect.x += -remainder

        self.end_tile.image.fill(black)

        for block in checkpoint_group:
            if block.rect.x == self.start_tile.rect.x or block.rect.y == self.start_tile.rect.y:
                a = [block.pos[0] - self.start_tile.pos[0], block.pos[1] - self.start_tile.pos[1]]
                mag = vector.mag(a)
                self.start_speed = vector.times(1 / mag, a)

        tiles_loaded = str(len(tile_group))
        window_in_tiles = str(self.width_map * self.height_map)
        if tiles_loaded != window_in_tiles:
            print("NUMBER OF TILES DOES NOT MATCH THE WINDOW SIZE!")

        self.clock = pygame.time.Clock()
        self.fps = 120

    def setup_map(self, map_name):
        x = 0
        y = 0
        index = 0
        fr = open(map_name, "r")
        self.map_values = fr.readlines()
        fr.close()

        for line in self.map_values:
            width = 0
            for digit in line:

                if digit == '0':
                    width += 1
                    grass_tile = Tile(grass, [x, y], self.tile_size)
                    grass_tile.index = index
                    tile_group.add(grass_tile)
                    x += self.tile_size
                    index += 1

                if digit == '1':
                    width += 1
                    road_tile = Tile(road, [x, y], self.tile_size)
                    road_tile.index = index
                    tile_group.add(road_tile)
                    road_group.add(road_tile)
                    x += self.tile_size
                    index += 1

                if digit == '2':
                    width += 1
                    check_tile = Tile(road, [x, y], self.tile_size)
                    check_tile.index = index
                    checkpoint_group.add(check_tile)
                    tile_group.add(check_tile)
                    x += self.tile_size
                    index += 1

                if digit == '8':
                    width += 1
                    self.start_tile = Tile(green, [x, y], self.tile_size)
                    self.start_tile.index = index
                    tile_group.add(self.start_tile)
                    base_group.add(self.start_tile)
                    x += self.tile_size
                    index += 1

                if digit == '9':
                    width += 1
                    self.end_tile = Tile(red, [x, y], self.tile_size)
                    self.end_tile.index = index
                    tile_group.add(self.end_tile)
                    base_group.add(self.end_tile)
                    x += self.tile_size
                    index += 1

            x = 0
            y += self.tile_size


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, speed, health, radius, color):
        super().__init__()
        self.color = color.copy()
        self.pos = pos
        self.radius = radius
        self.speed = vector.times(speed, game.start_speed)
        self.image = pygame.Surface([radius * 2, radius * 2])
        self.image.fill(white)
        self.image.set_colorkey(white)
        pygame.draw.circle(self.image, color, (radius, radius), radius, )
        self.origin = pos[0] + radius, pos[1] + radius
        self.rect = self.image.get_rect()
        self.crossed_checkpoints = []
        self.index = 0
        self.move_origin(pos)
        self.distance_travelled = vector.mag(vector.distance(game.start_tile.pos, self.pos))
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

    def hit_checkpoint(self):
        for a in checkpoint_group:
            distance_vector = [a.origin[0] - self.origin[0], a.origin[1] - self.origin[1]]
            if vector.mag(distance_vector) < game.tile_size:

                if self.speed[0] == 0:

                    # Moving UP
                    if self.speed[1] < 0 and a.rect.centery > self.rect.centery and a not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(a)
                        # Turning RIGHT
                        if tile_group.sprites()[a.index - 2].color == grass:
                            self.speed = [-1 * self.speed[1], self.speed[0]]
                        # Turning LEFT
                        else:
                            self.speed = [self.speed[1], self.speed[0]]
                        self.move_origin(a.origin)

                    # Moving DOWN
                    if self.speed[1] > 0 and a.rect.centery < self.rect.centery and a not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(a)
                        # Turning RIGHT
                        if tile_group.sprites()[a.index - 2].color == grass:
                            self.speed = [self.speed[1], self.speed[0]]
                        # Turning LEFT
                        else:
                            self.speed = [-1 * self.speed[1], self.speed[0]]
                        self.move_origin(a.origin)

                elif self.speed[1] == 0:

                    # Moving LEFT
                    if self.speed[0] < 0 and a.rect.centerx > self.rect.centerx and a not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(a)
                        # Turning DOWN
                        if tile_group.sprites()[a.index - 2 * game.width_map].color == grass:
                            self.speed = [self.speed[1], -1 * self.speed[0]]
                        # Turning UP
                        else:
                            self.speed = [self.speed[1], self.speed[0]]
                        self.move_origin(a.origin)

                    # Moving RIGHT
                    if self.speed[0] > 0 and a.rect.centerx < self.rect.centerx and a not in self.crossed_checkpoints:
                        self.crossed_checkpoints.append(a)
                        # Turning DOWN
                        if tile_group.sprites()[a.index - 2 * game.width_map].color == grass:
                            self.speed = [self.speed[1], self.speed[0]]
                        # Turning UP
                        else:
                            self.speed = [self.speed[1], -1 * self.speed[0]]
                        self.move_origin(a.origin)

    def hit_base(self):
        if pygame.sprite.collide_rect(self, game.end_tile):
            self.kill()

    def update(self):
        self.apply_speed()
        self.hit_checkpoint()
        self.hit_base()
        self.check_health()
        self.hit_bullet()

    def check_health(self):
        if self.health <= 0:
            self.die()

    def hit_bullet(self):
        if pygame.sprite.spritecollide(self, bullet_group, True):
            self.health += -1
            self.color[0] += 255 / self.start_health
            self.color[2] += -255 / self.start_health
            if self.color[2] < 0:
                self.die()
            else:
                self.draw_image()

    def die(self):
        self.kill()


class Tower(pygame.sprite.Sprite):
    def __init__(self, width, height, image_file):
        super().__init__()
        self.width = width * game.tile_size
        self.height = height * game.tile_size
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(grass)
        self.image.set_colorkey(grass)
        self.rect = self.image.get_rect()
        self.pos = game.mouse
        self.rect.x, self.rect.y = self.pos
        self.origin = [self.pos[0] + self.width / 2, self.pos[1] + self.height / 2]

        self.barrel_axis = None
        self.range = 0
        self.bullet_speed = 0
        self.cooldown = 0
        self.timer = 0
        self.active_state = 1

        self.original_cannon_image = pygame.image.load(image_file).convert_alpha()
        self.original_cannon_image = pygame.transform.scale(self.original_cannon_image, [self.width, self.height])
        self.original_cannon_image_rect = self.original_cannon_image.get_rect()
        self.rotated_cannon = self.original_cannon_image

        self.range_image = pygame.Surface([self.range * 2, self.range * 2])
        self.range_image_rect = self.range_image.get_rect()
        self.range_color = red.copy()
        self.range_image.fill(grass)
        self.range_image.set_colorkey(grass)
        self.range_image.set_alpha(100)

    def setup_turret(self, fire_range, bullet_speed, cooldown, barrel_axis):
        self.range = fire_range
        self.bullet_speed = bullet_speed
        self.cooldown = cooldown
        self.timer = cooldown
        self.barrel_axis = barrel_axis

        self.range_image = pygame.Surface([self.range * 2, self.range * 2])
        self.range_image_rect = self.range_image.get_rect()
        self.range_color = red.copy()
        transparent = (123, 123, 123)
        self.range_image.fill(transparent)
        self.range_image.set_colorkey(transparent)
        self.range_image.set_alpha(100)

    def set_position(self, pos):
        self.pos = pos
        self.origin = [pos[0] + self.width / 2, pos[1] + self.height / 2]
        self.rect.x, self.rect.y = pos

    def active(self, state=1):
        self.active_state = state

    def update(self):
        if event is not None:
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if len(moving_tower_group) > 0:
                        if moving_tower_group.sprites()[0].rect.collidepoint(game.mouse):
                            if moving_tower_group.sprites()[0].range_color == white:
                                static_tower_group.add(moving_tower_group.sprites()[0])
                                moving_tower_group.empty()
                        else:
                            moving_tower_group.sprites()[0].kill()

                    if self.rect.collidepoint(game.mouse):
                        self.active_state = not self.active_state
                    else:
                        self.active_state = 0

        if static_tower_group.has(self):
            self.enemy_detection()
        if moving_tower_group.has(self):
            self.active_state = 1

        if len(moving_tower_group.sprites()) > 0:
            for tile in tile_group:
                if tile.rect.collidepoint(game.mouse[0] - self.width / 4, game.mouse[1] - self.height / 4):
                    moving_tower_group.sprites()[0].set_position([tile.rect.x, tile.rect.y])
                    if pygame.sprite.spritecollide(self, road_group, False):
                        self.range_color = red
                    elif pygame.sprite.spritecollide(self, static_tower_group, False):
                        self.range_color = red
                    elif pygame.sprite.spritecollide(self, base_group, False):
                        self.range_color = red
                    else:
                        self.range_color = white

        for sprite in static_tower_group:
            sprite.range_color = white

        remainder_x = self.rect.x + self.rect.width - game.arena_size[0]
        remainder_y = self.rect.y + self.rect.height - game.arena_size[1]
        if remainder_x > 0:
            self.set_position([self.pos[0] - remainder_x, self.pos[1]])
        if remainder_y > 0:
            self.set_position([self.pos[0], self.pos[1] - remainder_y])

    def draw_images(self):
        self.image.fill(grass)
        self.image.blit(self.rotated_cannon, [0, 0])
        if self.active_state == 1:
            pygame.draw.circle(self.range_image, self.range_color,
                               [self.range_image_rect.centerx, self.range_image_rect.centery], self.range)
            game.window.blit(self.range_image, [self.origin[0] - self.range, self.origin[1] - self.range])

    def enemy_detection(self):
        self.timer += 1 / game.fps
        on_range = []
        distance_travelled_list = []

        for enemy in enemy_group:
            distance_vector = vector.distance(enemy.origin, self.origin)
            mag = vector.mag(distance_vector)
            if mag < self.range + enemy.radius:
                on_range.append(enemy)
        if len(on_range) == 0:
            return
        for on_range_enemy in on_range:
            distance_travelled_list.append(on_range_enemy.distance_travelled)
        for on_range_enemy in on_range:
            if on_range_enemy.distance_travelled == max(distance_travelled_list):
                self.aim(on_range_enemy)
                self.rotate_cannon(on_range_enemy)

    def rotate_cannon(self, enemy):
        distance_vector = vector.distance(enemy.origin, self.origin)
        angle = vector.angle(self.barrel_axis, distance_vector)
        if distance_vector[0] > 0:
            angle *= -1
        rot_image = pygame.transform.rotate(self.original_cannon_image, angle)
        rot_rect = self.original_cannon_image_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        self.rotated_cannon = rot_image
        return rot_image

    def aim(self, enemy):
        distance_vector = vector.distance(enemy.origin, self.origin)
        mag = vector.mag(distance_vector)
        unit_vector = vector.times(1 / mag, distance_vector)
        speed_vector = vector.times(self.bullet_speed, unit_vector)
        if self.cooldown < self.timer:
            self.fire(speed_vector)
            self.timer = 0

    def fire(self, speed_vector):
        bullet = Bullet(self.origin, speed_vector)
        bullet_group.add(bullet)


class Tile(pygame.sprite.Sprite):
    def __init__(self, color, pos, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.color = color.copy()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.origin = [pos[0] + size / 2, pos[1] + size / 2]
        self.index = 0
        if self.color == grass:
            pygame.draw.line(self.image, darkgreen, [0, 0], [0, size], 1)
            pygame.draw.line(self.image, darkgreen, [0, 0], [size, 0], 1)
            pygame.draw.line(self.image, darkgreen, [0, size - 1], [size, size - 1], 1)
            pygame.draw.line(self.image, darkgreen, [size - 1, 0], [size - 1, size], 1)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_pos, speed):
        super().__init__()
        self.image = pygame.Surface([5, 5])
        self.image.fill(black)
        self.rect = self.image.get_rect()
        self.speed = speed
        self.pos = start_pos
        self.set_position(self.pos)

    def set_position(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos

    def apply_speed(self):
        self.pos = vector.plus(self.pos, self.speed)
        self.set_position(self.pos)

    def check_borders(self):
        if self.pos[0] < self.rect.width or self.pos[1] < self.rect.height or self.pos[0] > game.arena_size[0] or \
                        self.pos[1] > game.arena_size[1]:
            self.kill()

    def update(self):
        self.apply_speed()
        self.check_borders()


# Child Classes


class Boss(Enemy):
    def __init__(self):
        Enemy.__init__(self, start, 1, 10, 20, blue)


class CannonTower(Tower):
    def __init__(self):
        Tower.__init__(self, 2, 2, 'cannon.png')
        self.setup_turret(100, 10, 0.1, [0, -1])


class ButtonCannon(button.Button):
    def __init__(self):
        super().__init__(white, 60, 60, [game.arena_size[0] + 25, 10])
        self.set_icon_image('cannon.png', 40, 40)

    def function(self):
        added_tower = CannonTower()
        moving_tower_group.add(added_tower)


class ArtilleryTower(Tower):
    def __init__(self):
        Tower.__init__(self, 3, 3, 'artillery.png')
        self.setup_turret(200, 30, 1, [0, -1])


class ButtonArtillery(button.Button):
    def __init__(self):
        super().__init__(white, 60, 60, [game.arena_size[0] + 25 + 60 + 10, 10])
        self.set_icon_image('artillery.png', 55, 55)

    def function(self):
        added_tower = ArtilleryTower()
        moving_tower_group.add(added_tower)


# Static functions

def draw_everything():
    game.window.fill(backround)
    tile_group.draw(game.window)
    base_group.draw(game.window)
    enemy_group.draw(game.window)
    bullet_group.draw(game.window)
    static_tower_group.draw(game.window)
    moving_tower_group.draw(game.window)

    button_group.draw(game.window)
    box_group.draw(game.window)

    moving_towers = moving_tower_group.sprites()
    if len(moving_towers) != 0:
        moving_towers[0].draw_images()
    for tower in static_tower_group:
        tower.draw_images()


def get_active(group):
    for active_sprite in group:
        if active_sprite.active_state == 1:
            return active_sprite
    empty_sprite = pygame.sprite.Sprite()
    empty_sprite.active_state = 0
    return empty_sprite


if __name__ == "__main__":
    game = Game("map1.txt")
    button_cannon = ButtonCannon()
    button_artillery = ButtonArtillery()

    info_box = box.Box(200, 400, [game.arena_size[0] + 25, 100], white, 150)
    info_box.add_text([100, 10], "this is awesome", 20, black, 'center')

    start = game.start_tile.origin
    static_tower_group = pygame.sprite.Group()
    box_group = pygame.sprite.Group(info_box)
    button_group = pygame.sprite.Group(button_cannon, button_artillery)
    moving_tower_group = pygame.sprite.GroupSingle()
    enemy_group = pygame.sprite.Group()
    bullet_group = pygame.sprite.Group()

    while True:

        game.mouse = pygame.mouse.get_pos()
        event = None

        for event in pygame.event.get():
            button_group.update(event)
            if event.type == QUIT:
                pygame.quit()
                quit()

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    added_enemy = Boss()
                    enemy_group.add(added_enemy)
                if event.key == K_r:
                    static_tower_group.empty()
                    enemy_group.empty()
                if event.key == K_DELETE:
                    get_active(static_tower_group).kill()

        # Logic testing:

        # Update functions:
        enemy_group.update()
        bullet_group.update()
        static_tower_group.update()
        moving_tower_group.update()

        # Draw everything:
        draw_everything()

        # Delay framerate and update display:
        game.clock.tick(game.fps)
        pygame.display.flip()
