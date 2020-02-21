import math
import pygame
pygame.init()

screenWidth = 1500
screenHeight = 750
win = pygame.display.set_mode((screenWidth, screenHeight))

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

class groundDino(object):
    ''' Ground Dinosaur. Defaulting attributes:
    width1 = 30
    height1 = 30
    x1 = 5
    y1 = screenHeight - height1
    vel1 = 0.5
    x1Mod = 1 '''

    def __init__(self, x=5, y=screenHeight - 30, width=30, height=30, vel=0.5, rgb=(255,0,0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel
        self.rgb = rgb
        self.xMod = 1

    def draw(self, win):
        #win.fill((0, 0, 0))
        pygame.draw.rect(win, self.rgb, (self.x, self.y, self.width, self.height))

    # Ground Dino 2 Values (raptor)
    # width2 = 15
    # height2 = 15
    # x2 = 500
    # y2 = screenHeight - height2
    # vel2 = 5
    # x2Mod = 1



class airDino(object):
    ''' Air Dinosaur. Default attributes:
    airWidth = 15
    airHeight = 15
    airX = 50
    airY = screenHeight - 50
    airVel = 5
    airXMod = 1
    airYMod = -1 '''

    def __init__(self, x=50, y=(screenHeight - 20), width=15, height=15, vel=5, rgb=(255,255,0)):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.vel = vel
        self.rgb = rgb
        self.xMod = 1
        self.yMod = -0.5

    def draw(self, win):
        pygame.draw.rect(win, self.rgb, (self.x, self.y, self.width, self.height))

class projectile(object):
    def __init__(self,x,y,radius,color,facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 #*self.facing
    # TODO: finish projectile tutorial 04:07
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x,self.y), self.radius)
        #we could use a different shape and color for weapon upgrades


def redrawGameWindow():
    win.fill((255, 255, 255))
    #draw player helo
    player1.draw(win)

    #draw dinoList
    for dino in dinoList:
        dino.draw(win)

    #bullet list
    for bullet in bullets:
        bullet.draw(win)
    #draw air dino
    #pygame.draw.rect(win, (255, 255, 0), (airX, airY, airWidth, airHeight))

    pygame.display.update()

#######################  MAIN  #################################
player1 = player()
tRex = groundDino()
raptor = groundDino(500,screenHeight - 15, 15, 15, 5, rgb=(255,165,0))
ptero = airDino()

dinoList = [tRex, raptor, ptero]

spawnList = [1]
spawnNum = 1
bullets = []
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

    #Air Dino 1 Movement #TODO: FIX:Vary height pattern movement and 'perimeter rebound'
    ptero.x += ptero.vel * ptero.xMod
    if ptero.x == screenWidth - ptero.width:
        ptero.xMod = -1
    if ptero.x == 0:
        ptero.xMod = 1
    if ptero.y == 0:
        ptero.yMod = 1
    if ptero.y == screenHeight:
        ptero.yMod = -1
    ptero.y += (ptero.vel * math.sin(ptero.x)) + ptero.yMod


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    #projectile movement
    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))
            
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and player1.x > player1.vel:
        player1.x -= player1.vel
    if keys[pygame.K_RIGHT] and player1.x < (screenWidth - player1.width):
        player1.x += player1.vel
    if keys[pygame.K_UP] and player1.y > player1.vel:
        player1.y -= player1.vel
    if keys[pygame.K_DOWN] and player1.y < (screenHeight - player1.height):
        player1.y += player1.vel
    if keys[pygame.K_SPACE]: #TODO: experiment with spawning
        spawn = str(spawnNum)
        spawn = airDino()
        spawnNum += 1
        dinoList.append(spawn)
        print(spawn)
        

    # TODO: shoot gun
        
    if keys[pygame.K_SPACE]: 
        
        #xGun = x
        #yGun = y + (height / 2)
        #pygame.draw.rect(win,(0,0,0),(xGun,yGun,screenWidth,2))
        #pygame.display.update()
        
        if len(bullets) < 2:                                                                                     #radius, color(black)               
            bullets.append(projectile(round(player1.x + player1.width //2), round(player1.y + player1.height //2), 6, (0,0,0)''', facing'''))
        pass
    

    redrawGameWindow()

pygame.quit()
