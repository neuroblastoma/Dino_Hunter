import math
import pygame
pygame.init()

screenWidth = 1500
screenHeight = 750
win = pygame.display.set_mode((screenWidth,screenHeight))

pygame.display.set_caption("Test Game Concepts")

bg = pygame.image.load('bg.jpg')

#Player Helo Values
x = 50
y = 50
width = 25
height = 25
vel = 2

#Gun Values
xGun = x
yGun = y
gunWidth = 5
gunHeight = 5
gunVel = 10

#Ground Dino 1 Values
width1 = 30
height1 = 30
x1 = 5
y1 = screenHeight - height1
vel1 = 0.5
x1Mod = 1

#Ground Dino 2 Values
width2 = 15
height2 = 15
x2 = 500
y2 = screenHeight - height2
vel2 = 5
x2Mod = 1

#Air Dino Values
airWidth = 15
airHeight = 15
airX = 500
airY = (screenHeight - height2) / 2
airVel = 5
airXMod = 1
airYMod = +1


run = True
while run:
    pygame.time.delay(25)

    #Ground Dino 1 Movement
    x1 += vel1 * x1Mod
    if x1 == screenWidth - width1:
        x1Mod = -1
    if x1 == 0:
        x1Mod = 1

    #Ground Dino 2 Movement
    x2 += vel2 * x2Mod
    if x2 == screenWidth - width1:
        x2Mod = -1
    if x2 == 0:
        x2Mod = 1

    #Air Dino 1 Movement
    #TODO: FIX:Vary height pattern movement
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

    if keys[pygame.K_LEFT] and x > vel:
        x -= vel
    if keys[pygame.K_RIGHT] and x < (screenWidth - width):
        x += vel
    if keys[pygame.K_UP] and y > vel:
        y -= vel
    if keys[pygame.K_DOWN] and y < (screenHeight - height):
        y += vel
    if keys[pygame.K_SPACE]:
        #TODO: shoot gun
        pygame.draw.rect(win,(0,0,0),(x,y,gunWidth,gunHeight))
        pygame.display.update()


    win.fill((255, 255, 255))

    #draw player helo
    pygame.draw.rect(win,(0,0,255),(x,y,width,height))
    #draw dino1
    pygame.draw.rect(win,(255,0,0),(x1,y1,width1,height1))
    #draw dino2
    pygame.draw.rect(win,(255,165,0),(x2,y2,width2,height2))
    #draw air dino
    pygame.draw.rect(win, (255, 255, 0), (airX, airY, airWidth, airHeight))

    pygame.display.update()

pygame.quit()