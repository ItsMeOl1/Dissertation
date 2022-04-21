import pygame, enemy, buildings, map, ui, rounds
pygame.init()

##DISPLAY SET UP
screenSize = 1600, 900 
squareSize = 50 #32x18
screen = pygame.display.set_mode(screenSize)

##SET UP
RUNNING = True
clock = pygame.time.Clock()
timePassed = 0

##CONSTANTS 
FPS_font = pygame.font.SysFont("Arial", 13)
mouseposSurface = pygame.Surface((squareSize, squareSize))
mouseposSurface.fill((255,0,0))
mouseposSurface.set_alpha(15)
background = pygame.image.load("Sprites/Floors/grass.png")
background = pygame.transform.scale(background, (1600,900))

##SPRITE GROUPS
enemies = pygame.sprite.Group()
enemy.Squirrel((0,0), enemies) #remove later

towers = pygame.sprite.Group()
bullets = pygame.sprite.Group()

def drawFPS():
    text = str(int(clock.get_fps()))
    fps = FPS_font.render(text, 0, pygame.Color("white"))
    screen.blit(fps, (0, 0))

def drawRound():
    text = Round.name
    text = FPS_font.render(text, 0, pygame.Color("white"))
    rect = text.get_rect()
    roundText = pygame.transform.scale(text, (rect.w * 5, rect.h * 5))
    screen.blit(roundText, (100, -10))

def drawBackground():
    #screen.fill(dark_gray)
    #for x in range(0,screenSize[0],squareSize*2):
    #    for y in range(0,screenSize[1],squareSize*2):
    #        pygame.draw.rect(screen, light_gray , (x, y, squareSize, squareSize))
    #for x in range(squareSize,screenSize[0],squareSize*2):
    #    for y in range(squareSize,screenSize[1],squareSize*2):
    #        pygame.draw.rect(screen, light_gray , (x, y, squareSize, squareSize))

    screen.blit(background, (0,0))

def mouseClick(mousePos):
    xblock = int(mousePos[0]/squareSize)
    yblock = int(mousePos[1]/squareSize)
    if UI.selected == "wall":
        levelmap.place(xblock, yblock)
        if not levelmap.findPath():
            levelmap.clear(xblock, yblock)
            levelmap.findPath()
    elif levelmap.get_block(xblock, yblock) == 1: ##if clicked on a wall
        if UI.selected == "bomb":
            levelmap.clear(xblock, yblock)
        elif UI.selected == "tower1":
            buildings.BasicTower(towers, (xblock*squareSize, yblock*squareSize))
            levelmap.place(xblock, yblock, 2)
    elif levelmap.get_block(xblock, yblock) > 1:
        if UI.selected == "bomb":
            for tower in towers:
                if tower.rect.collidepoint(mousePos):
                    tower.kill()
                    break
            levelmap.clear(xblock, yblock)

Round = rounds.get_next_round()

UI = ui.UI()

levelmap = map.Map(int(screenSize[0]/squareSize), int(screenSize[1]/squareSize))
levelmap.setPath()

while RUNNING:
    clock.tick()
    timePassed += clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            RUNNING = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
             UI.updateClick(event.pos)

    if RUNNING: #If 'x' button not clicked
        keys = pygame.key.get_pressed()
        mouseButtons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()

        if mouseButtons[0] and not UI.collision(mousePos):
                if UI.selected is not None: 
                    mouseClick(mousePos)

        if not enemies and not Round.enemyList:
            Round = rounds.get_next_round()

        drawBackground()
        levelmap.drawTiles(screen,squareSize, screenSize)
        levelmap.drawPath(screen, (0,255,0), squareSize)

        ticks = 0
        while timePassed >= 50:
            timePassed -= 50
            ticks += 1

        enemies.update(screen, ticks)
        towers.update(screen, bullets, enemies, ticks)
        UI.update(mousePos)
        bullets.update(screen, enemies, ticks)
        newEnemy = Round.update(ticks)
        if newEnemy == "1":
            enemy.Squirrel((0,0), enemies)

        screen.blit(mouseposSurface, (int(mousePos[0]/squareSize)*squareSize, int(mousePos[1]/squareSize)*squareSize, squareSize, squareSize))
        UI.draw(screen)

        drawFPS()
        drawRound()

        pygame.display.flip()