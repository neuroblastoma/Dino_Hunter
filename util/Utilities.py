import pygame

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
            print('Unable to load spritesheet image: ' + filename)
            raise SystemExit(e)

        # Sticking with rows/cols for simplicity
        self.rows = rows
        self.cols = columns

    def get_images(self):
        # TODO: Error checking
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
            surface.blit(self.sheet, (0,0), rect, pygame.BLEND_RGBA_ADD)

            retSurfaces.append(surface)

        return retSurfaces

def simple_camera(camera, rect, screenWidth, screenHeight):
    left, top, _, _ = rect
    _, _, width, height = camera

    return pygame.Rect(-left + (screenWidth/2), -top + (screenHeight/2), width, height)


def complex_camera(camera, rect, screenWidth, screenHeight):
    # we want to center target_rect
    x = -rect.center[0] + screenWidth/2
    y = -rect.center[1] + screenHeight/2
    # move the camera. Let's use some vectors so we can easily substract/multiply
    camera.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera.topleft)) * 0.06
    # set max/min x/y so we don't see stuff outside the world
    camera.x = max(-(camera.width-screenWidth), min(0, camera.x))
    camera.y = max(-(camera.height-screenHeight), min(0, camera.y))

    return camera