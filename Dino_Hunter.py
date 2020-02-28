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


# CLASSES ##################
class Entity(pygame.sprite.Sprite):
    """This is the top-level class for any character entity that will exist on the screen in-game.
    It extends the Pygame Sprite class (https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite)
    Attributes: health, width, height, x-position, y-position, and velocity.
    Behaviors: DrawToWindow, BoundToGameWindow
    Rules: ? """

    def __init__(self, health, x, y, width, height, vel):
        # TODO: Why is this the way? (https://stackoverflow.com/questions/53804098/add-argument-after-must-be-an-iterable-not-int-pygame)
        super(Entity, self).__init__()

        self.health = health
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.images = None
        self.rect = None

    def draw(self, surface, target):
        # TODO: Do we need a draw to window method in the Entity class?
        ## This is all inherited from the Sprite class..., so ?
        pass

    def update(self, dt):
        pass

    # def bound(self):
    # TODO: Do we need a bound to window method in the Entity class?


class Player(Entity):
    # Attributes: Lives, Weapons/Power-ups
    # Rules: Clipping/Sprite collision: player will lose health if collides with any other object

    # Starting position(1380, 50)
    # y collision with ground = 575?
    def __init__(self):
        # TODO: Player should enter screen from top, right
        super().__init__(health=100, x=100, y=100, width=5, height=5, vel=0)

        # TODO: Sounds, lift, gravity, etc.
        self.lives = 3

        # Speed related ##################################################################
        # TODO: This should be both vertical and horizontal speed
        # TODO: This should be it's own data structure that tracks the overall state (dict?)
        self.max_speed = 7
        self.max_lift = 3  # 5 pixels/sec
        self.lift_speed = 0

        # Determines facing direction
        self.left_facing = True
        self.old_horizontalDirection = -1

        # Animation #####################################################################
        # TODO: May want to move this to a method? This will not be the only time we need to load images in this manner
        # Entity or Utilities.SpriteSheet?

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
        self.rect = pygame.Rect(self.frame.get_rect())

    def update(self, dt):
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
        self.rect = (self.x, self.y, 70, 90)


# class AirDino(Entity):
# TODO: Air/Ground Dinosaur Class
# Attributes: ?
# Behaviors: ?
# Rules: ?


# TODO: Projectile Class subclass of entity (Matt)

class BackgroundObjects(Entity):
    def __init__(self, health, x, y, width, height, vel):
        super().__init__(health, x, y, width, height, vel)

class Camera(object):
    '''https://stackoverflow.com/questions/14354171/add-scrolling-to-a-platformer-in-pygame'''
    def __init__(self, cameraFunc, width, height):
        self.width = width
        self.height = height
        self.state = pygame.Rect(0,0, self.width, self.height)
        self.cameraFunc = cameraFunc

    def apply(self, target):
        t = pygame.Rect(target.rect)
        return t.move(self.state.topleft)

    def update(self, target):
        t = pygame.Rect(target.rect)
        self.state = self.cameraFunc(self.state, t, self.width, self.height)

    # def update(self, *args):
    #     super().update(*args)
    #     if self.target:
    #         x = -self.target.rect.center[0] + self.width / 2
    #         y = -self.target.rect.center[1] + self.height / 2
    #         self.cam += (pygame.Vector2((x, y)) - self.cam) * 0.05
    #         self.cam.x = max(-(self.state.width - self.width), min(0, self.cam.x))
    #         self.cam.y = max(-(self.state.height - self.height), min(0, self.cam.y))

    # def draw(self, target):
    #     self.state = self.update(self.state, target.rect)


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
        self.camera = Camera(Utilities.complex_camera, self.screenWidth, self.screenHeight)
        self.dt = None
        self.keyState = None
        self.run = True

        # Sprite trackers
        self.world = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.players = pygame.sprite.Group()

        # Sprite initialization
        self.player = Player()
        self.create_enemies()

        # Add sprites to "global" tracker
        self.world.add(self.player)
        self.players.add(self.player)

        for e in self.enemies:
            self.world.add(e)


    def redrawGameWindow(self):
        """redrawGameWindow function will fill the window with the specific RGB value and then call on each
        object's .draw() method in order to populate it to the window. """
        black = (0, 0, 0)

        # Clear screen
        self.screen.fill(black)

        # Draw background
        self.screen.blit(self.background, (0,0))

        # Update camera
        self.camera.update(self.player)

        for entity in self.world:
            # TODO: Should update and draw be the same thing?
            #   One updates the position/animation
            #   The other draws everything to the screen
            #   self.screen.blit()?
            entity.update(self.dt)
            entity.draw(self.screen, self.camera.apply(entity))

        # Update the main display
        pygame.display.update()

    def create_enemies(self):
        # TODO: different amount/types depending on level?

        # TODO: THIS IS A TEST
        evilPlayer = Player()

        self.enemies.add(evilPlayer)

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

            print(type(self.player))

            # Collision detection:
            if self.enemies:
                if pygame.sprite.spritecollide(self.players, self.enemies, dokill=False):
                    self.player.lives -= 1
                    # TODO: Explosion or flashing or something?

                    if self.player.lives <= 0:
                        self.player.kill()
                        # TODO: Game over screen...
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

        # Movement
        # If > 0: up/left else down/right
        verticalDirection = 0
        horizontalDirection = 0
        if self.keyState[pygame.K_w] or self.keyState[pygame.K_s]:
            verticalDirection = self.keyState[pygame.K_s] - self.keyState[pygame.K_w]
        elif self.keyState[pygame.K_UP] or self.keyState[pygame.K_DOWN]:
            verticalDirection = self.keyState[pygame.K_DOWN] - self.keyState[pygame.K_UP]
        if self.keyState[pygame.K_a] or self.keyState[pygame.K_d]:
            horizontalDirection = self.keyState[pygame.K_d] - self.keyState[pygame.K_a]
        elif self.keyState[pygame.K_LEFT] or self.keyState[pygame.K_RIGHT]:
            horizontalDirection = self.keyState[pygame.K_RIGHT] - self.keyState[pygame.K_LEFT]

        firing = self.keyState[pygame.K_SPACE]

        return horizontalDirection, verticalDirection, firing


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
