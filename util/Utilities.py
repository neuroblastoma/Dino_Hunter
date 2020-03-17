import pygame
import math
from util import LinkedList
import json
import os


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


def fixed_x_camera(camera_rect, entity, screen_width):
    """Tracks the position of the given entity and locks screen to their x position"""

    # Create x,y based on entity's position
    x = -entity.rect.center[0] + screen_width / 2
    y = entity.rect.y

    # Move the camera
    camera_rect.topleft += (pygame.Vector2((x, y)) - pygame.Vector2(camera_rect.topleft))  # * 0.06

    return camera_rect


def determine_layer(height):
    return lambda x: math.floor((height + x) / 10)


def retrieve_highscore(filename="high_score.data"):
    abs_filename = os.path.join(os.path.abspath("util"), filename)

    if os.path.exists(abs_filename):
        # Read filename
        try:
            with open(abs_filename, 'rb') as f:
                scores = json.load(f)
        except OSError:
            raise OSError("Unable to open {}".format(filename))
    else:
        scores = {
            "1": {
                "name": "BJC",
                "score": "644725"
            }
        }

    return scores


def determine_highscore(player_score, set_function, filename="high_score.data"):
    pscore = str(player_score).split(':')[1].split('}')[0]
    scores = retrieve_highscore(filename)

    score_list = LinkedList.LinkedList()
    set_score = False
    position = 0

    # Read dict into LL
    for item in scores.items():
        score_list.append(dataItem=item)

    i = 0
    while score_list.read(i):
        item = score_list.read(i)
        if int(item[1]['score']) < int(pscore):
            set_score = True
            # One based index
            position = int(item[0])
            break
        i += 1

    # Set score
    if set_score:
        set_function(score_list, pscore, position)

    return


def set_highscore(score_list, player_score, position, name):
    abs_filename = os.path.join(os.path.abspath("util"), "high_score.data")

    score_list.insertAtIndex(position - 1, (str(position), {'name': str(name), 'score': str(player_score.strip(' ').zfill(6))}))

    # Only write top eight entries
    scores = {}
    i = 0
    while score_list.read(i) and i < 7:
        scores[str(i + 1)] = score_list.read(i)[1]
        i += 1

    try:
        with open(abs_filename, 'w') as f:
            json.dump(scores, f)
    except OSError:
        raise OSError("Unable to open {}".format(abs_filename))
