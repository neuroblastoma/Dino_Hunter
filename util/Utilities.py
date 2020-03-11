import pygame
import math


class SpriteSheet(object):
    '''
    Create individual surfaces from a single image source (i.e., sprite sheet)
    Based on code from:
        https://www.pygame.org/wiki/Spritesheet
        https://github.com/taylorjohn/Spritesheet/blob/master/python3_4/spritesheet.py

    Parameters: filename, rows, columns
    '''

    def __init__(self, filename, rows, columns):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            # print('Unable to load spritesheet image: ' + filename)
            raise SystemExit(e)

        # Sticking with rows/cols for simplicity
        self.rows = rows
        self.cols = columns

    def get_images(self):
        rects = []
        spriteWidth = self.sheet.get_width() // self.cols
        spriteHeight = self.sheet.get_height() // self.rows

        # Parse sprite sheet until upper bounds are met
        for y in range(0, self.sheet.get_height(), spriteHeight):
            if y + spriteHeight > self.sheet.get_height():
                continue
            for x in range(0, self.sheet.get_width(), spriteWidth):
                if x + spriteWidth > self.sheet.get_width():
                    continue

                # Append sprite dimensions to a list of rectangles
                rects.append((x, y, spriteWidth, spriteHeight))

        # Create a list of Pygame Surface objects
        retSurfaces = []
        for rect in rects:
            surface = pygame.Surface((rect[2], rect[3]), 0, self.sheet)
            surface.blit(self.sheet, (0, 0), rect, pygame.BLEND_RGBA_ADD)

            retSurfaces.append(surface)

        return retSurfaces


def complex_camera(camera_rect, entity, screenWidth, screenHeight):
    """Tracks the position of the given entity and locks screen to their x position"""

    # Create x,y based on entity's position
    x = -entity.rect.center[0] + screenWidth / 2
    y = entity.rect.y

    # Move the camera
    camera_rect.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera_rect.topleft))  # * 0.06

    return camera_rect


def determine_layer(height):
    return lambda x: math.floor((height + x) / 10)
