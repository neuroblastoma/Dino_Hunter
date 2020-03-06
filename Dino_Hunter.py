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

import pygame
import os
from itertools import cycle
from util import Utilities
import random


# CLASSES ##################
class Camera(object):
    '''https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame'''
    def __init__(self, cameraFunc, width, height):
        self.width = width
        self.height = height
        self.offsetState = pygame.Rect(0, 0, self.width, self.height)
        self.cameraFunc = cameraFunc

    def apply(self, target):
        return target.rect.move(self.offsetState.topleft)

    def update(self, target):
        self.offsetState = self.cameraFunc(self.offsetState, target.rect, self.width, self.height)

class ControlManager(object):
    """Class for tracking game states & managing event loop
        https://github.com/Mekire/pygame-samples/blob/master/platforming/moving_platforms.py
    """

    def __init__(self, caption, screenWidth=1500, screenHeight=750):
        """Initialize the display and prepare game objects"""
        # Screen settings
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.fps = 60

        # Screen attributes
        pygame.display.set_caption(caption)
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        self.screen_rect = self.screen.get_rect()
        self.viewport = self.screen.get_rect()

        # TODO: what does this do? Is it only used for text???
        self.level = pygame.Surface((1000, 1000)).convert()
        self.level_rect = self.level.get_rect()

        # TODO: How do we handle level transitions?
        self.background = pygame.image.load(os.path.join("images", "retro_forest.jpg"))
        self.background = pygame.transform.scale(self.background, (self.screenWidth, self.screenHeight))

        # Core settings
        self.clock = pygame.time.Clock()
        self.camera = Camera(Utilities.simple_camera, self.screenWidth, self.screenHeight)
        self.dt = None
        self.keyState = None
        self.run = True

        # Sprite trackers
        self.world = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()

        # Sprite initialization
        self.player = Player()
        self.create_enemies()

        # Add sprites to "global" tracker
        self.world.add(self.player)
        self.players.add(self.player)

        for e in self.enemies:
            self.world.add(e)

    def create_enemies(self):
        # TODO: different amount/types depending on level?
        # TODO: THIS IS A TEST
        tRex1 = tRex(self.screenWidth, self.screenHeight)
        self.enemies.add(tRex1)

        raptor1 = raptor(self.screenWidth, self.screenHeight)
        self.enemies.add(raptor1)

    def make_text(self, message):
        """Renders text object to the screen"""
        font = pygame.font.Font(None, 100)
        text = font.render(message, True, (100, 100, 175))
        rect = text.get_rect(centerx=self.level_rect.centerx, y=100)

        return text, rect

    def main_loop(self):
        """This loop represents all the actions that need to be taken during one cycle:
                1. Update world based on what user did
                2. Clear screen w/ win.fill(black)
                3. Redraw the graphics for the world
                4. Call pygame.display.update to update graphics on screen.
        """
        while self.run:
            # check events
            for event in pygame.event.get():
                # If user clicks red X, toggle run
                if event.type == pygame.QUIT:
                    self.run = False
                #elif event.type == pygame.ADDENEMY:

            # Update time delta
            self.dt = self.clock.tick(self.fps)

            # Update key state
            self.keyState = pygame.key.get_pressed()

            horizontalDirection, verticalDirection, firing = self.parse_keyState()

            # Movement
            self.player.move(verticalDirection, horizontalDirection)

            # Projectile spawn
            if firing:
                # Number of supported bullets on screen
                if len(self.bullets) < 15:
                    # Adds bullet to bullets sprite group
                    self.bullets.add(Projectile(round(self.player.x + 20 + self.player.width // 2), round(self.player.y + 55 + self.player.height // 4), 2, color=(0,0,0), facing=self.player.left_facing, velocity=int(50)))

                self.world.add(self.bullets)

            # Collision detection:
            # if self.enemies:
            #     if pygame.sprite.spritecollide(sprite=self.player, group=self.enemies, dokill=False):
            #         self.player.lives -= 1
            #         # TODO: Explosion or flashing or something?
            #
            #         if self.player.lives <= 0:
            #             self.player.kill()
            #             # TODO: Game over screen...

            elif self.bullets:
                for bullet in self.bullets:
                    print(bullet.x)
                    if bullet.x > self.screenWidth or bullet.x < 0:
                        self.bullets.remove(bullet)
                        self.world.remove(bullet)

                    if pygame.sprite.spritecollide(sprite=bullet, group=self.enemies, dokill=True):
                        #TODO: Remove enemies and bullets from respective trackers and self.world
                        continue
            else:
                # TODO: Display success and move to next level
                pass


            # TODO: Should really consider scenes... Ugh. Why so complicated?

            # Insert music here


            self.redrawGameWindow()

            # Check to see if player is out of lives?
            if self.player.lives <= 0 or self.keyState[pygame.K_ESCAPE]:
                self.run = False

    def parse_keyState(self):
        '''Parses pressed keys'''
        # Quit
        if self.keyState[pygame.K_ESCAPE]:
            self.run = False

        # Movement
        # If > 0: up/left else down/right
        verticalDirection = 0
        horizontalDirection = 0

        # Directional keys
        if self.keyState[pygame.K_w] or self.keyState[pygame.K_s]:
            verticalDirection = self.keyState[pygame.K_s] - self.keyState[pygame.K_w]
        elif self.keyState[pygame.K_UP] or self.keyState[pygame.K_DOWN]:
            verticalDirection = self.keyState[pygame.K_DOWN] - self.keyState[pygame.K_UP]
        if self.keyState[pygame.K_a] or self.keyState[pygame.K_d]:
            horizontalDirection = self.keyState[pygame.K_d] - self.keyState[pygame.K_a]
        elif self.keyState[pygame.K_LEFT] or self.keyState[pygame.K_RIGHT]:
            horizontalDirection = self.keyState[pygame.K_RIGHT] - self.keyState[pygame.K_LEFT]

        # Weapon-related
        firing = self.keyState[pygame.K_SPACE]

        return horizontalDirection, verticalDirection, firing

    def redrawGameWindow(self):
        """redrawGameWindow function will fill the window with the specific RGB value and then call on each
        object's .draw() method in order to populate it to the window. """
        black = (0, 0, 0)

        # Clear screen
        self.screen.fill(black)

        # Draw background
        self.screen.blit(self.background, (0,0))

        # Update camera
        self.player.animate(self.dt)
        self.player.draw(self.screen, self.player)
        self.camera.update(self.player)

        for entity in self.world:
            if not isinstance(entity, Player):
                entity.move()
                entity.draw(self.screen, self.camera.apply(entity))

        # Update the main display
        pygame.display.update()

class Entity(pygame.sprite.Sprite):
    """This is the top-level class for any character entity that will exist on the screen in-game.
    It extends the Pygame Sprite class (https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite)
    Attributes: health, width, height, x-position, y-position, and velocity.
    Behaviors: DrawToWindow, BoundToGameWindow
    Rules: ? """

    def __init__(self, health, x, y, width, height, vel):
        super().__init__()

        self.health = health
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.images = None
        self.rect = None

    def draw(self, **kwargs):
        return NotImplemented

    def move(self, **kwargs):
        return NotImplemented


class Player(Entity):
    # Attributes: Lives, Weapons/Power-ups
    # Rules: Clipping/Sprite collision: player will lose health if collides with any other object

    # Starting position(1380, 50)
    # y collision with ground = 575?
    def __init__(self):
        # TODO: Player should enter screen from top, right
        super().__init__(health=100, x=100, y=100, width=5, height=5, vel=0)

        # TODO: Sounds
        self.lives = 3

        # Speed related ##################################################################
        # TODO: This should be both vertical and horizontal speed
        self.max_speed = 7
        self.max_lift = 3  # 5 pixels/sec
        self.lift_speed = 0

        # Determines facing direction
        self.left_facing = True
        self.old_horizontalDirection = -1

        # Animation #####################################################################
        # Load player sprite sheet
        self.sheet = Utilities.SpriteSheet(filename=os.path.join("images", "MH-6J Masknell-flight.png"), rows=1, columns=6)

        # TODO: Need to do the proper math for frame_duration
        self.timer = 0
        self.frame_duration = 33
        # Creates iterable list of images/frames
        self.frames = self.sheet.get_images()

        # Set transparency for image (white)
        for frame in self.frames:
            frame.set_colorkey((255, 255, 255))

        self.frameCycle = cycle(self.frames)
        self.frame = next(self.frameCycle)
        self.rect = self.frame.get_rect()

    def animate(self, dt):
        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.frame = next(self.frameCycle)

    def draw(self, surface, target):
        """Blit the player to the window"""

        # TODO: Add animation that triggers when facing changes
        # TODO: Remember: target was self.rect

        if self.left_facing:
            surface.blit(self.frame, target)
        else:
            surface.blit(pygame.transform.flip(self.frame, True, False), target)

    def move(self, vdir, hdir):
        """Moves player based on keyboard input and tracks facing direct. Movement is not instantaneous.
            The following cases apply to horizontal player movement
                1. If player is stationary, horizontal speed resets after slowing down
                2. If player changes direction, horizontal speed is negated
                3. If player continues in same direction, horizontal speed is increased until max
        """
        # TODO: Need to bound this to the screen limits

        # Determine direction to face
        old_facing = self.left_facing
        if hdir != 0:
            self.left_facing = True if hdir == -1 else False
            self.old_horizontalDirection = hdir

            # Case 3: Increase speed until max
            if self.vel < self.max_speed:
                self.vel += 0.25
            else:
                self.vel = self.max_speed

        # Case 1: reset horizontal speed
        else:
            if self.vel > 0:
                self.vel -= 0.25
                hdir = self.old_horizontalDirection
            else:
                self.vel = 0

        # Case 2: Simulate "drag" of direction change
        if old_facing != self.left_facing:
            self.vel = self.vel * -0.75

        # Incremental vertical speed
        if vdir < 0 or vdir > 0:
            if self.lift_speed < self.max_lift:
                self.lift_speed += 0.25
            else:
                self.lift_speed = self.max_lift

        # Adjust (x,y)
        self.x += (hdir * self.vel)
        self.y += (vdir * self.lift_speed)

        # Update self.rectangle with new coords
        self.rect = pygame.Rect(self.x, self.y, 70, 90)


class tRex(Entity):
    # TODO: STEVE: create tRex Dino Class
    def __init__(self, screenWidth, screenHeight):
        super().__init__(health=50, x=random.randrange(0,screenWidth - 121), y=screenHeight - 30, width=30, height=30, vel=random.uniform(0.5, 1.0))
        self.rgb = (255, 0, 0)
        self.end = screenWidth - (self.width * random.randrange(2, 4))
        self.path = [0 + (self.width * random.randrange(2, 4)), self.end]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win, R):
        self.move()
        pygame.draw.rect(win, self.rgb, self.rect)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

        self.rect = pygame.Rect(self.x, self.y, 30, 30)


class raptor(Entity):
    def __init__(self, screenWidth, screenHeight):
        super().__init__(health=25, x=random.randrange(0,screenWidth-61), y=screenHeight - 15, width=15, height=15, vel=random.uniform(4,6))
        self.rgb = (255, 255, 255)
        self.end = screenWidth - (self.width * random.randrange(2,4))
        self.path = [0 + (self.width * random.randrange(2,4)), self.end]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, win, R):
        self.move()
        pygame.draw.rect(win, self.rgb, self.rect)

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1

        self.rect = pygame.Rect(self.x, self.y, 15, 15)


class Projectile(Entity):

    def __init__(self, x, y, radius, color, facing, velocity):
        super().__init__(health=1, x=x, y=y, height=0, width=0, vel=velocity) # TODO: xVel and yVel for shooting down at dinos?
        self.x = int(x)
        self.y = int(y)
        self.radius = radius
        self.color = color
        self.rect = pygame.Rect(self.x - radius, self.y - radius, radius*2, radius*2)
        self.facing = facing

    def draw(self, surface, target):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

    def move(self):
        if self.facing:
            self.x -= self.vel
        else:
            self.x += self.vel

class BackgroundObjects(Entity):
    def __init__(self, health, x, y, width, height, vel):
        super().__init__(health, x, y, width, height, vel)

    def draw(self):
        return NotImplemented

    def move(self):
        return NotImplemented

# MAIN ##################
def main():
    # MAIN CODE ######################################################
    pygame.init()

    # SETTINGS #######################################################
    # screenWidth = 1500
    # screenHeight = 750

    # Instantiation ##################################################
    game = ControlManager(caption="Dino Hunter")

    # Something, something containers?
    # TODO: containers may be the same as the world list below... more research needed

    # GAME LOOP ######################################################
    game.main_loop()
    pygame.quit()


if __name__ == '__main__':
    main()
