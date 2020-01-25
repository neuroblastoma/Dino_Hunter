import math
import pygame
pygame.init()

screenWidth = 1500
screenHeight = 750
win = pygame.display.set_mode((screenWidth,screenHeight))

pygame.display.set_caption("Test Game Concepts")

class player(object):
    ''' Player class. Defaulting attributes:
    x = 50
    y = 50
    width = 25
    height = 25
    vel = 2
    '''
    def __init__(self, x=50, y=50, width=25, height=25, vel=2):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

    def draw(self, win):
        win.fill((0, 0, 0))
        pygame.draw.rect(win, (0, 0, 255), (self.x, self.y, self.width, self.height))

class groundDino(object): #TODO: Just created groundDino class. Need to go through MAIN to update w/ OOP
    ''' Ground Dinosaur. Defaulting attributes:
    width1 = 30
    height1 = 30
    x1 = 5
    y1 = screenHeight - height1
    vel1 = 0.5
    x1Mod = 1 '''
    def __init__(self, x=5, y=screenHeight - 30, width=30, height=30, vel=0.5, rgb=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.rgb = rgb
        self.xMod = 1

    def draw(self, win):
        #win.fill((0, 0, 0))
        if self.rgb == 3:
            color = (0, 0, 255)
        elif self.rgb == 2:
            color = (0, 255, 0)
        else:
            color = (255, 0, 0)
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.height))

#Ground Dino 2 Values (raptor)
'''
width2 = 15
height2 = 15
x2 = 500
y2 = screenHeight - height2
vel2 = 5
x2Mod = 1
'''
#Air Dino Values
airWidth = 15
airHeight = 15
airX = 50
airY = screenHeight - 50
airVel = 5
airXMod = 1
airYMod = -1

def redrawGameWindow():
    win.fill((255, 255, 255))
    #draw player helo
    player1.draw(win)

    #draw dinoList
    for dino in dinoList:
        dino.draw(win)

    #draw dino1
    #tRex.draw(win)

    #draw dino2
    #raptor.draw(win)

    #draw air dino
    pygame.draw.rect(win, (255, 255, 0), (airX, airY, airWidth, airHeight))

    pygame.display.update()

#######################  MAIN  #################################
player1 = player()
tRex = groundDino()
raptor = groundDino(500,screenHeight - 15, 15, 15, 5)
dinoList = [tRex, raptor]

run = True
while run:
    pygame.time.delay(25)

    #tRex Movement
    tRex.x += tRex.vel * tRex.xMod
    if tRex.x == screenWidth - tRex.width:
        tRex.xMod = -1
    if tRex.x == 0:
        tRex.xMod = 1

    #raptor Movement
    raptor.x += raptor.vel * raptor.xMod
    if raptor.x == screenWidth - raptor.width:
        raptor.xMod = -1
    if raptor.x == 0:
        raptor.xMod = 1

    #Air Dino 1 Movement #TODO: FIX:Vary height pattern movement
    airX += airVel * airXMod
    if airX == screenWidth - airWidth:
        airXMod = -1
    if airX == 0:
        airXMod = 1
    if airY == 0:
        airYMod = 1
    if airY == screenHeight:
        airYMod = -1
    airY += (airVel * math.sin(airX)) + airYMod


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player1.x > player1.vel:
        player1.x -= player1.vel
    if keys[pygame.K_RIGHT] and player1.x < (screenWidth - player1.width):
        player1.x += player1.vel
    if keys[pygame.K_UP] and player1.y > player1.vel:
        player1.y -= player1.vel
    if keys[pygame.K_DOWN] and player1.y < (screenHeight - player1.height):
        player1.y += player1.vel
    if keys[pygame.K_SPACE]: #TODO: shoot gun
        '''
        xGun = x
        yGun = y + (height / 2)
        pygame.draw.rect(win,(0,0,0),(xGun,yGun,screenWidth,2))
        pygame.display.update()
        '''
        pass

    redrawGameWindow()

pygame.quit()