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
pygame.init()

screenWidth = 1500
screenHeight = 750
win = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("Dino Hunter")

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

    # def draw(self, win):
        # TODO: Do we need a draw to window method in the Entity class?

    # def bound(self):
        # TODO: Do we need a bound to window method in the Entity class?

    # TODO: Player (sub)Class
    # Attributes: Lives, Weapons/Power-ups
    # Rules: Clipping/Sprite collision: player will lose health if collides with any other object

    # TODO: Air/Ground Dinosaur Class
    # Attributes: ?
    # Behaviors: ?
    # Rules: ?

# TODO: Projectile Class outside of Entity class?


def redrawGameWindow():
    """redrawGameWindow function will fill the window with the specific RGB value and then call on each
    object's .draw() method in order to populate it to the window. """
    win.fill((255, 255, 255))

# MAIN CODE ################################################################################################
# instantiate player
# instantiate dinosaurs

run = True
while run:
    pygame.time.delay(25)

    # main game code

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()

pygame.quit()
