# Dino_Hunter.py
#
# CS3021 Big Project
#
# Winter 2020
# Created: 31 Jan 2020
# Updated: 31 Jan 2020
#
# Matthew Gurrister
# Steven Gore
# John Lytle

import os
import math
import random
import pygame
import sys

try:
    import Utilities
except ImportError:
    from util import Utilities

from itertools import cycle
from util import FIFO
from util import Stack
from Main_Menu import *


# CLASSES ##################
class Camera(object):
    """Creates a viewport on a fixed _x-axis"""

    def __init__(self, cameraFunc, width, height):
        self.width = width
        self.height = height
        self.offsetState = pygame.Rect(self.width / 2, 1000, self.width, self.height)
        self.cameraFunc = cameraFunc

    def apply(self, target):
        """Apply camera offset to target"""
        # Bind _x coordinate
        dx = target.rect.x + self.offsetState.x
        dx = dx % self.width

        # Bind _y coordinate
        if 101 <= target.y <= self.height - target.rect.height:
            target.y = target.y
        elif target.y > self.height - target.rect.height:
            target.y = self.height - target.rect.height
        else:
            target.y = 101

        target.rect = pygame.Rect(dx, target.y, target.rect.height, target.rect.width)

        return target.rect

    def update(self, target):
        """Updates the camera coordinates to match targets. Centers screen on target"""
        self.offsetState = self.cameraFunc(self.offsetState, target, self.width)


class ControlManager(object):
    """Class for tracking game states & managing event loop"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    FPS = 60

    def __init__(self, caption, screen_width=1500, screen_height=750):
        """Initialize the display and prepare game objects"""
        # Screen settings
        self._screen_width = screen_width
        self._screen_height = screen_height
        self.fps = ControlManager.FPS
        self.current_level = -1

        # Screen attributes
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self._screen_width, self._screen_height))
        self.screen_rect = self.screen.get_rect()

        # Background
        self.bg = Background(width=self._screen_width, height=screen_height)
        self.determine_layer = Utilities.determine_layer(self._screen_height)

        # Core settings
        self.clock = pygame.time.Clock()
        self.camera = Camera(Utilities.fixed_x_camera, self._screen_width, self._screen_height)
        self.run = True

        # HUD surface
        self.hud = pygame.Surface((self._screen_width, 100))
        self.hud_font = pygame.font.Font(os.path.join(os.path.abspath("images"), "PressStart2P-Regular.ttf"), 15)

        self.mob_limit = 10
        self.mob_queue = FIFO.FIFO()

        # Sprite trackers
        self.world = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Tracking HUD
        self.tracker = Stack.Stack()

        # Sprite initialization
        self.player = Player(x=self._screen_width / 2)
        self.create_enemies()

        # Add sprites to "global" tracker
        self.world.add(self.player, layer=self.player.layer)
        self.players.add(self.player)

        # Score
        self.score = 0

    @property
    def screen_width(self):
        return self._screen_width

    @screen_width.setter
    def screen_width(self, width):
        return Utilities.checkDimensions(width)

    @property
    def screen_height(self):
        return self._screen_height

    @screen_width.setter
    def screen_height(self, height):
        return Utilities.checkDimensions(height)

    def reset(self):
        self.run = True
        self.current_level = -1
        self.score = 0

        # Remove any residual sprites
        while not self.mob_queue.empty:
            self.mob_queue.remove()
        self.players.empty()
        self.world.empty()
        self.enemies.empty()

        # Re-init player and enemies
        self.player = Player(x=self._screen_width / 2)
        self.create_enemies()

        # Repopulate trackers
        self.players.add(self.player)
        self.world.add(self.player, layer=self.player.layer)

    def create_enemies(self):
        base = (2, 4, 3)
        self.current_level += 1
        if self.current_level == 0:
            self.mob_queue.add(TRex(self._screen_width, self._screen_height))
            self.mob_queue.add(Raptor(self._screen_width, self._screen_height))
            self.mob_queue.add(Ptero(self._screen_width, self._screen_height))
        else:
            for i in range(base[0] * self.current_level):
                self.mob_queue.add(TRex(self._screen_width, self._screen_height))
                self.mob_queue.add(Raptor(self._screen_width, self._screen_height))
                self.mob_queue.add(Ptero(self._screen_width, self._screen_height))

    def main_loop(self):
        """This loop represents all the actions that need to be taken during one cycle:
                1. Update world based on what user did
                2. Clear screen w/ win.fill(black)
                3. Redraw the graphics for the world
                4. Call pygame.display.update to update graphics on screen.
        """
        paused = False
        # Need to set for subsequent runs from main menu
        if not self.run:
            self.reset()

        while self.run:
            # Check events
            for event in pygame.event.get():
                # If user clicks red X, toggle run
                if event.type == pygame.QUIT:
                    self.run = False
                # Pause
                if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    paused = not paused
                    paused_txt = self.hud_font.render("-- PAUSED --", 1, (255, 0, 0))
                    self.screen.blit(paused_txt, self.screen_rect.center)
                    pygame.display.update()

            # Update key state
            key_state = pygame.key.get_pressed()
            horizontal_direction, vertical_direction, firing = self.parse_key_state(key_state)

            if not paused:
                # Mob spawn
                while len(self.enemies) <= self.mob_limit and not self.mob_queue.empty():
                    e = self.mob_queue.remove()
                    # Adjust layer depending on _y value
                    e.layer = self.determine_layer(e.y + e.height)
                    self.enemies.add(e)
                    self.world.add(e, layer=e.layer)

                # Collision detection
                self.detect_collision()

                # Movement
                self.player.vdir = vertical_direction
                self.player.hdir = horizontal_direction
                self.player.firing = firing
                self.player.move()

                # Clamp player's _x coordinate:
                self.player.x = self.player.x % self._screen_width

                # Update camera
                self.camera.update(self.player)

                # Advance to next level
                if not self.enemies and self.mob_queue.empty():
                    counter = 100
                    while counter > 0:
                        # Draw Level Complete
                        font = pygame.font.SysFont('comicsans', 100, True)
                        level_txt = font.render("LEVEL COMPLETE! " + str(counter // 10), 1, (0, 255, 0))
                        self.screen.blit(level_txt, (375, 300))
                        counter -= 1
                        self.player.rect.y = self._screen_height / 2
                        self.player.rect.x = self._screen_width / 2
                        pygame.display.update()
                        self.redraw_game_window()

                    # Reset player position
                    self.player.rect.y = self._screen_height / 2
                    self.player.rect.x = self._screen_width / 2

                    # Increase gun strength
                    self.player.gun_str += 1

                    # Spawn new enemies
                    self.create_enemies()
                    for e in self.enemies:
                        self.world.add(e)

                self.redraw_game_window()

        # Exit to main menu
        hs_event = pygame.event.Event(pygame.USEREVENT + 4, {"score": self.score})
        rs_event = pygame.event.Event(pygame.USEREVENT + 3, {"dummy": 0})
        pygame.event.post(rs_event)
        pygame.event.post(hs_event)

    def detect_collision(self):
        # Player-enemy collision detection:
        pe_collision = pygame.sprite.spritecollide(sprite=self.player.rect, group=self.enemies, dokill=False,
                                                   collided=pygame.sprite.Rect.colliderect)
        if pe_collision:
            pe_collision[0].damaged += 1
            self.player.damaged += 1
            if self.player.health <= self.player.damaged:
                self.player.lives -= 1
                self.player._x = 100
                self.player._y = 100
                self.player.gun_str = 1
                self.player.damaged = 0

            if pe_collision[0].health <= pe_collision[0].damaged:
                pe_collision[0].kill()

            if self.player.lives <= 0:
                counter = 500
                while counter > 0:
                    font = pygame.font.SysFont('comicsans', 100, True)
                    go_txt = font.render("GAME OVER!", 1, (0, 255, 0))
                    self.screen.blit(go_txt, (550, 300))
                    # score_txt = font.render("SCORE = " + str(self.player.score), 1, (0, 255, 0))
                    # self.screen.blit(score_txt, (375, 400))
                    counter -= 1
                    pygame.display.update()
                    self.redraw_game_window()

                self.player.kill()
                self.run = False

        # Projectile-enemy collision detection
        if self.bullets:
            for bullet in self.bullets:
                # bullet collision detection
                collision = pygame.sprite.spritecollide(sprite=bullet, group=self.enemies, dokill=False)
                if collision:
                    self.score += 1
                    collision[0].damaged += (self.player.gun_str)
                    if collision[0].damaged >= collision[0].health:
                        collision[0].kill()

                    self.bullets.remove(bullet)
                    self.world.remove(bullet)

                if bullet.rect.x > self._screen_width or bullet.rect.x < 0:
                    self.bullets.remove(bullet)
                    self.world.remove(bullet)

    def parse_key_state(self, key_state):
        """Parses pressed keys"""
        # Quit
        if key_state[pygame.K_ESCAPE]:
            self.run = False

        # Movement
        # If > 0: up/left else down/right
        vertical_direction = 0
        horizontal_direction = 0

        # Directional keys
        if key_state[pygame.K_w] or key_state[pygame.K_s]:
            vertical_direction = key_state[pygame.K_s] - key_state[pygame.K_w]
        elif key_state[pygame.K_UP] or key_state[pygame.K_DOWN]:
            vertical_direction = key_state[pygame.K_DOWN] - key_state[pygame.K_UP]
        if key_state[pygame.K_a] or key_state[pygame.K_d]:
            horizontal_direction = key_state[pygame.K_d] - key_state[pygame.K_a]
        elif key_state[pygame.K_LEFT] or key_state[pygame.K_RIGHT]:
            horizontal_direction = key_state[pygame.K_RIGHT] - key_state[pygame.K_LEFT]

        # Weapon-related
        firing = key_state[pygame.K_SPACE]

        return horizontal_direction, vertical_direction, firing

    def redraw_game_window(self):
        """redraw_game_window function will fill the window with the specific RGB value and then call on each
        object's .draw() method in order to populate it to the window. """

        # Update time delta
        dt = self.clock.tick(self.fps)

        # Clear screen
        self.screen.fill(ControlManager.BLACK)

        # Update background
        self.bg.move(self.camera.offsetState.x)
        self.bg.draw(self.screen)

        # Projectile spawn
        if self.player.firing:
            # Number of supported bullets on screen
            if len(self.bullets) < 5 + self.current_level:
                # Create a bullet instance
                bullet = Projectile(round(self._screen_width // 2),
                                    round(self.player.rect.center[1] + self.player.height // 4), 2,
                                    color=(255, 255, 255), facing=self.player.facing,
                                    velocity=int(3), dx=self.player.angle)

                # Adds bullet to bullets sprite group
                self.bullets.add(bullet)

            # Add all bullets to world tracker
            self.world.add(self.bullets)

        # Move select entities and draw everything to screen
        for entity in self.world:
            entity.animate(dt)

            # Player has already moved (to update camera)
            if not isinstance(entity, Player):
                entity.move()

            # Offset is not applied to projectiles
            if not isinstance(entity, Projectile):
                entity.draw(self.screen, self.camera.apply(entity))
            else:
                entity.draw(self.screen, entity)

            # Add enemies to HUD tracker
            if not isinstance(entity, Projectile):
                self.tracker.push(entity)

        self.display_hud()

        # Update the main display
        pygame.display.update()

    def display_hud(self):
        """Update HUD components"""

        # Clear HUD
        self.hud.fill(ControlManager.BLACK)

        # draw borders
        rect = self.hud.get_rect()
        pygame.draw.rect(self.hud, ControlManager.WHITE, rect, 3)

        # Left screen: lives, health bar
        left_x = self._screen_width // 32
        #   Draw Player Health
        # Custom Health bar at top left
        pygame.draw.rect(self.hud, (255, 0, 0), (left_x, 15, self.player.health, 20))
        pygame.draw.rect(self.hud, (0, 255, 0), (left_x, 15, (self.player.health - self.player.damaged), 20))

        #   Health counter
        health_txt = self.hud_font.render("Health: " + str(self.player.health - self.player.damaged), 1,
                                          ControlManager.WHITE)
        self.hud.blit(health_txt, (left_x, 40))

        #   Draw Player lives
        # text = self.hud_font.render('Lives: ' + str(self.player.lives), 1, (0, 0, 0))
        # self.hud.blit(text, (left_x, 60))
        offset = 0
        for i in range(self.player.lives):
            self.hud.blit(self.player.icon, (left_x + offset - 10, 60))
            offset += 35

        # Middle screen: Enemy tracker
        pygame.draw.rect(self.hud, ControlManager.WHITE, (rect.x + self._screen_width // 4, rect.y, 2 * rect.width // 4,
                                                          rect.height), 3)
        while not self.tracker.empty():
            e = self.tracker.pop()
            x, y = e.rect.topleft

            new_x = (x * (2 * rect.width // 4) // self._screen_width) + self._screen_width // 4
            new_y = (y * 100) / self._screen_height
            t = pygame.rect.Rect(new_x, new_y - 10, 10, 10)
            pygame.draw.rect(self.hud, e.rgb, t)

        # Right screen: score, gun strength, level
        #   Draw Player scoreboard
        right_x = (3 * self._screen_width // 4) + self._screen_width // 16
        text = self.hud_font.render("Score: " + str(self.score).zfill(6), 1, ControlManager.WHITE)
        self.hud.blit(text, (right_x, 60))
        #   Level
        lvl_txt = self.hud_font.render("Level: " + str(self.current_level), 1, ControlManager.WHITE)
        self.hud.blit(lvl_txt, (right_x, 40))
        #   Draw projectile detail
        gun_str = self.hud_font.render("Power: " + str(self.player.gun_str), 1, ControlManager.WHITE)
        self.hud.blit(gun_str, (right_x, 20))

        # Blit hud to screen
        self.screen.blit(self.hud, (0, 0))


class Background(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.mid_bg = pygame.image.load(os.path.join(os.path.abspath("images"), "retro_forest.jpg"))
        self.mid_bg = pygame.transform.scale(self.mid_bg, (self.width, self.height))
        self.mid_rect = self.mid_bg.get_rect()

    def draw(self, surface):
        surface.blit(self.mid_bg, self.mid_rect)
        surface.blit(self.mid_bg, self.mid_rect.move(self.mid_rect.width, 0))
        surface.blit(self.mid_bg, self.mid_rect.move(-self.mid_rect.width, 0))

    def move(self, offset):
        # Bind _x coordinate between 0 and _screen_width
        if self.mid_rect.left >= self.width:
            self.mid_rect.x = 0
        elif self.mid_rect.right <= 0:
            self.mid_rect.x = 0

        dx = -(self.mid_rect.x - offset)
        self.mid_rect.move_ip(dx, 0)


class Entity(pygame.sprite.Sprite):
    """This is the top-level class for any character entity that will exist on the screen in-game.
    It extends the Pygame Sprite class (https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite)
    """

    def __init__(self, health, x, y, width, height, vel):
        super().__init__()

        self.health = health
        self.damaged = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.images = None
        self.frame = None
        self.rect = None
        self.frameCycle = None
        self.facing = False
        self.timer = 0
        self.frame_duration = 0

    def animate(self, dt):
        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.frame = next(self.frameCycle)

    def draw(self, surface, target):
        # Use this to see hit boxes
        # pygame.draw.rect(surface, self.rgb, self.rect, 2)
        if self.facing:
            surface.blit(self.frame, target)
        else:
            surface.blit(pygame.transform.flip(self.frame, True, False), target)

    def move(self, **kwargs):
        return NotImplemented


class Player(Entity):
    """Creates player"""

    def __init__(self, x):
        super().__init__(health=100, x=x, y=100, width=5, height=5, vel=0)

        self.gun_str = 1

        self.lives = 3
        self.score = 0
        self.vdir = 0
        self.hdir = 0
        self.firing = 0
        self.rgb = (255, 255, 255)

        # Speed related ##################################################################
        self.max_speed = 7
        self.max_lift = 6  # 5 pixels/sec
        self.lift_speed = 0

        # Determines facing direction
        self.facing = True
        self.old_horizontalDirection = -1

        self.layer = 5

        # Animation #####################################################################
        # Load player sprite sheet
        self.sheet = Utilities.SpriteSheet(
            filename=os.path.join(os.path.abspath("images"), "MH-6J Masknell-flight.png"),
            rows=1, columns=6)

        self.timer = 0
        self.frame_duration = 33
        # Creates iterable list of images/frames
        self.frames = self.sheet.get_images()
        # Set transparency for image (white)
        for frame in self.frames:
            frame.set_colorkey((255, 255, 255))

        self.icon = pygame.transform.scale(self.frames[2], (50, 30))
        self.frameCycle = cycle(self.frames)
        self.frame = next(self.frameCycle)
        self.rect = self.frame.get_rect()
        self.angle = 0

    def move(self):
        """
        Moves player based on keyboard input and tracks facing direct. Movement is not instantaneous.
            The following cases apply to horizontal player movement
                1. If player is stationary, horizontal speed resets after slowing down
                2. If player changes direction, horizontal speed is negated
                3. If player continues in same direction, horizontal speed is increased until max
        """
        # Determine direction to face
        old_facing = self.facing
        if self.hdir != 0:
            self.facing = True if self.hdir == -1 else False
            self.old_horizontalDirection = self.hdir

            # Case 3: Increase speed until max
            self.angle = 10
            if self.vel < self.max_speed:
                self.vel += 0.25
            else:
                self.vel = self.max_speed

        # Case 1: reset horizontal speed
        else:
            self.angle = -10
            if self.vel > 0:
                self.vel -= 0.25
                self.hdir = self.old_horizontalDirection
            else:
                self.vel = 0

        # Case 2: Simulate "drag" of direction change
        if old_facing != self.facing:
            self.vel = self.vel * -0.75

        # Incremental vertical speed
        if self.vdir < 0 or self.vdir > 0:
            if self.lift_speed < self.max_lift:
                self.lift_speed += 0.45
            else:
                self.lift_speed = self.max_lift

        # Adjust (_x,_y)
        self.x += (self.hdir * self.vel)
        self.y += (self.vdir * self.lift_speed)

        # Update self.rectangle with new coords
        self.rect = pygame.Rect(self.x, self.y, 70, 90)

    def draw(self, surface, target):
        image = pygame.transform.rotate(self.frame, self.angle)

        if self.facing:
            surface.blit(image, target)
        else:
            surface.blit(pygame.transform.flip(image, True, False), target)


class Enemy(Entity):
    def __init__(self, filename, rows, cols, duration):
        super().__init__(health=100, x=0, y=0, width=0, height=0, vel=random.uniform(0.5, 1.0))
        self.end = None
        self.path = None
        self.initialize_animation(filename, rows, cols, duration)
        self.layer = 1

    def initialize_animation(self, filename, rows, cols, duration):
        # Animation #####################################################################
        # Load sprite sheet
        self.sheet = Utilities.SpriteSheet(filename=os.path.join(os.path.abspath("images"), filename), rows=rows,
                                           columns=cols)

        self.facing = False
        self.timer = 0
        self.frame_duration = duration
        self.frames = self.sheet.get_images()

        for frame in self.frames:
            frame.set_colorkey((255, 255, 255))

        self.frameCycle = cycle(self.frames)
        self.frame = next(self.frameCycle)
        self.rect = self.frame.get_rect()

    def draw(self, surface, target):
        super().draw(surface, target)

        # Floating health bar
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.center[0], self.y - 15, self.health, 10))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.center[0], self.y - 15, (self.health - self.damaged), 10))

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.facing = True
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.facing = False
                self.x += self.vel
            else:
                self.vel = self.vel * -1

        self.rect = pygame.Rect(self.x, self.y, self.height, self.width)


class TRex(Enemy):
    def __init__(self, screen_width, screen_height):
        super().__init__('trex-sheet.png', 1, 4, 175)
        self.health = 50
        self.x = random.randrange(0, screen_width - 121)
        self.y = random.randrange(screen_height - 300, screen_height - 200)
        self.width = 218
        self.height = 150
        self.vel = random.uniform(0.5, 1.0)

        self.rgb = (255, 0, 0)
        self.end = screen_width - (self.width * random.randrange(2, 4))
        self.path = [0 + (self.width * random.randrange(2, 4)), self.end]


class Raptor(Enemy):
    def __init__(self, screen_width, screen_height):
        super().__init__('Raptor-sheet.png', 1, 6, 70)
        self.health = 15
        self.x = random.randrange(0, screen_width - 61)
        self.y = random.randrange(screen_height - 200, screen_height - 100)
        self.width = 150
        self.height = 90
        self.vel = random.uniform(3, 5)

        self.rgb = (255, 165, 0)
        self.end = screen_width - (self.width * random.randrange(2, 4))
        self.path = [0 + (self.width * random.randrange(2, 4)), self.end]


class Ptero(Enemy):
    def __init__(self, screen_width, screen_height):
        super().__init__('Ptero-sheet.png', 1, 6, 175)
        self.health = 15
        self.x = random.randrange(0, screen_width - 120)
        self.y = random.randrange(60, screen_height - 60)
        self.width = 170
        self.height = 110
        self.vel = random.uniform(2, 3)

        self.rgb = (255, 255, 0)

        # _x-values
        self.end = screen_width - (self.width * random.randrange(2, 4))
        self.path = [0 + (self.width * random.randrange(2, 4)), self.end]

        # _y-values
        self.y_vel = random.uniform(-2, 2)
        self.y_end = screen_height - (self.height * random.randrange(2, 4))
        self.y_path = [0 + (self.height * random.randrange(2, 4)), self.y_end]


class Projectile(Entity):

    def __init__(self, x, y, radius, color, facing, velocity, dx):
        super().__init__(health=1, x=x, y=y, height=0, width=0, vel=velocity)
        self.x = int(x)
        self.y = int(y)
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(self.x - radius, self.y - radius, radius * 2, radius * 2)
        self.facing = facing
        self.dx = dx
        self.sheet = Utilities.SpriteSheet(filename=os.path.join(os.path.abspath("images"), 'bullets.png'), rows=1,
                                           columns=2)
        self.frames = self.sheet.get_images()
        for frame in self.frames:
            frame.set_colorkey((255, 255, 255))

        # VECTOR MATH!
        self.offset = pygame.math.Vector2(40, 0).rotate(math.radians(45))

        # Change bullet vector based on direction and forward movement
        if self.facing:
            if self.dx > 0:
                self.v = pygame.math.Vector2(self.vel, -2).rotate(0) * 9
                self.pos = pygame.math.Vector2(self.rect.x - 20, self.rect.y) + self.offset
            else:
                self.v = pygame.math.Vector2(self.vel, 0).rotate(0) * 9
                self.pos = pygame.math.Vector2(self.rect.x - 17, self.rect.y + 12) + self.offset
        else:
            if self.dx > 0:
                self.v = pygame.math.Vector2(-self.vel, -2).rotate(0) * 9
                self.pos = pygame.math.Vector2(self.rect.x - 30, self.rect.y) + self.offset
            else:
                self.v = pygame.math.Vector2(-self.vel, 0).rotate(0) * 9
                self.pos = pygame.math.Vector2(self.rect.x - 30, self.rect.y + 12) + self.offset

    def animate(self, dt):
        return NotImplemented

    def draw(self, surface, target):
        x = random.randint(0, 1)
        surface.blit(self.frames[x], self.rect.center)

    def move(self):
        self.pos -= self.v
        self.rect.center = self.pos


# MAIN ##################
def main():
    # MAIN CODE ######################################################
    pygame.init()

    # SETTINGS #######################################################
    screen_width = 1500
    screen_height = 750

    # Instantiation ##################################################
    game = ControlManager(caption="Dino Hunter", screen_width=screen_width, screen_height=screen_height)

    # Menu ###########################################################
    main_menu = MainMenu(size=(screen_width, screen_height), game_func=game.main_loop)
    main_menu.start()

    pygame.quit()


if __name__ == '__main__':
    main()
