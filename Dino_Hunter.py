#Dino_Hunter.py
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

    def draw(self, surface):
        # TODO: Do we need a draw to window method in the Entity class?
        ## This is all inherited from the Sprite class..., so ?
        pass

    def update(self, dt):
        pass

    # def bound(self):
        # TODO: Do we need a bound to window method in the Entity class?



class Player(Entity):
    # TODO: Player (sub)Class
    # Attributes: Lives, Weapons/Power-ups
    # Rules: Clipping/Sprite collision: player will lose health if collides with any other object
    def __init__(self):
        # TODO: This should be calling Entity?
        super().__init__(health=100, x=100, y=100, width=5, height=5, vel=8)

        #TODO: Sounds, lift, gravity, etc.
        self.lives = 3
        #TODO: This should be both vertical and horizontal speed
        self.lift_speed = 8 # 50 pixels/sec
        self.fall_speed = 5
        self.facing = True

        # Animation #####################################################################
        # Load player sprite sheet
        self.sheet = Utilities.SpriteSheet(filename='MH-6J Masknell-flight.png', rows=1, columns=6)

        #TODO: Need to do the proper math for frame_duration
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

    def update(self, dt):
        self.timer += dt
        while self.timer >= self.frame_duration:
            self.timer -= self.frame_duration
            self.frame = next(self.frameCycle)

    def draw(self, surface):
        """Blit the player to the window"""
        if self.facing:
            surface.blit(self.frame, self.rect)
        else:
            surface.blit(pygame.transform.flip(self.frame, True, False), self.rect)
    def move(self, vdir, hdir):
        """Moves player based on keyboard input"""


        if (hdir != 0 or vdir != 0):
            #TODO: hard cap on speed if we do variable speed?
            self.facing = True if hdir == -1 else False
            self.x += (hdir * self.vel) #+ prevSpeed
            self.y += (vdir * self.vel) #
            #self.rect.move_ip(self.x, self.y)
            self.rect = (self.x, self.y, 70, 90)

        #TODO: Need to bound this to the screen limits


    def check_collision(self):
        return NotImplementedError

# class AirDino(Entity):
    # TODO: Air/Ground Dinosaur Class
    # Attributes: ?
    # Behaviors: ?
    # Rules: ?


# TODO: Projectile Class outside of Entity class?


# class ControlManager(object):
    # """Class for tracking game states & managing event loop
    #     https://github.com/Mekire/pygame-samples/blob/master/platforming/moving_platforms.py
    # """
#     def __init__(self):
#         """Initialize the diplay and prepare game objects"""
#         self.screen = pygame.display.get_surface()
#         self.screen_rect = self.screen.get_rect()
#         self.clock = pygame.time.Clock()
#         self.fps = 60
#         self.keys = pygame.key.get_pressed()
#         self.done = False
#         self.player = Player()
#         self.viewport = self.screen.get_rect()


#     def update_viewport(self):
#         """The viewport stays centered on player 
#         unless the player is at the edge of the screen."""
#         self.viewport.center = self.player.rect.center
#         self.viewport.clamp_ip(self.level_rect)

def redrawGameWindow(win, world, dt):
    """redrawGameWindow function will fill the window with the specific RGB value and then call on each
    object's .draw() method in order to populate it to the window. """
    black = (0,0,0)
    white = (255,255,255)

    win.fill(black)

    for entity in world:

        #TODO: Should update and draw be the same thing?
        #   One updates the position/animation
        #   The other draws everything to the screen
        entity.update(dt)
        entity.draw(win)

    #Update the main display
    pygame.display.update()


def main():
    # MAIN CODE ################################################################################################
    #TODO: Think about "world" state == a way to track all entities in game.
    # Pygame uses groups to categorize different things, may be worth looking into
    # May want to consider moving this to its own DinoGame class (2/6: Lytle)
    pygame.init()

    # SETTINGS ##################################
    #TODO: move all of this to ControlManager or Settings?
    fps = 60
    screenWidth = 1500
    screenHeight = 750

    win = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Dino Hunter")
    clock = pygame.time.Clock()

    # Instantiation ##################################
    # Initialize game groups
    # groundDinos = pygame.sprite.Group()
    # all = pygame.sprite.RenderUpdates()

    # Something, something containers?
    # TODO: containers may be the same as the world list below... more research needed

    # instantiate player
    player = Player()
    # instantiate dinosaurs

    # Create world list (i.e., entity tracker)
    # TODO: Is this our missing data structure in the making?
    world = [player]

    # GAME LOOP ##################################
    """This loop represents all the actions that need to be taken during one cycle:
            1. Update world based on what user did
            2. Clear screen w/ win.fill(black)
            3. Redraw the graphics for the world
            4. Call pygame.display.update to update graphics on screen.
    """
    run = True
    while run:
        #pygame.time.delay(33)
        dt = clock.tick(fps)

        # check events
        for event in pygame.event.get():
            # If user clicks red X, toggle run
            if event.type == pygame.QUIT:
                run = False

        #Retrieve all keys being pressed (key bitmap)
        keystate = pygame.key.get_pressed()

        # Parse keystate
        # If > 0: up/left else down/right
        verticalDirection = keystate[pygame.K_s] - keystate[pygame.K_w]
        horizontalDirection = keystate[pygame.K_d] - keystate[pygame.K_a]
        firing = keystate[pygame.K_SPACE]

        # Move
        player.move(verticalDirection, horizontalDirection)

        # Insert checks for collisions here

        #TODO: Should really consider scenes... Ugh. Why so complicated?

        # Insert music here

        redrawGameWindow(win, world, dt)

        # Check to see if player is out of lives?
        if player.lives <= 0:
            run = False


    pygame.quit()


if __name__ == '__main__':
    main()