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
import sys

# CLASSES ##################
class Entity(object):
    """This is the top-level class for any character entity that will exist on the screen.
    Attributes: health, width, height, x-position, y-position, and velocity.
    Behaviors: DrawToWindow, BoundToGameWindow
    Rules: ? """

    def __init__(self, health, x, y, width, height, vel):
        self.health = health
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

    def draw(self, win):
        # TODO: Do we need a draw to window method in the Entity class?
        pass

    # def bound(self):
        # TODO: Do we need a bound to window method in the Entity class?


class Player(Entity):
    # TODO: Player (sub)Class
    # Attributes: Lives, Weapons/Power-ups
    # Rules: Clipping/Sprite collision: player will lose health if collides with any other object
    def __init__(self):
        super().__init__(health=100, x=0, y=0, width=5, height=5, vel=0)

        #self.image or spritesheet
        #self.rect


        self.lives = 3

    # def draw(self, win):
    #     """Blit the player to the window"""
    #     win.blit(self.image, self.rect)

    # def check_collision(self):
    #     return NotImplentedError

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

def redrawGameWindow(win):
    """redrawGameWindow function will fill the window with the specific RGB value and then call on each
    object's .draw() method in order to populate it to the window. """
    win.fill((255, 255, 255))


def main():
    # MAIN CODE ################################################################################################
    
    # May want to consider moving this to its own DinoGame class (2/6: Lytle)
    pygame.init()

    screenWidth = 1500
    screenHeight = 750
    win = pygame.display.set_mode((screenWidth, screenHeight))
    pygame.display.set_caption("Dino Hunter")



    # instantiate player
    # instantiate dinosaurs

    run = True
    while run:
        pygame.time.delay(25)

        # main game code

        # check events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


        redrawGameWindow(win)

    pygame.quit()


if __name__ == '__main__':
    main()