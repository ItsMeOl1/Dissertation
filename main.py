import pygame, enemy, buildings, map, ui
pygame.init()

##SETTING UP THE DISPLAY
screenSize = 1600, 900 
squareSize = 50 #32x18
RUNNING = True
screen = pygame.display.set_mode(screenSize)
clock = pygame.time.Clock()

##COLOUR CONSTANTS 
red = 255,0,0
green = 0,255,0
FPS_font = pygame.font.SysFont("Arial", 10)
mouseposSurface = pygame.Surface((squareSize, squareSize))
mouseposSurface.fill(red)
mouseposSurface.set_alpha(15)
background = pygame.image.load("Sprites/Floors/grass.png")
background = pygame.transform.scale(background, (1600,900))

##SET UP SPRITE GROUPS
enemies = pygame.sprite.Group()
enemy.Squirrel((0,0), enemies)

towers = pygame.sprite.Group()
bullets = pygame.sprite.Group()

def drawOutlines(screen, colour, squareSize, screenSize):
    for x in range(squareSize, screenSize[0], squareSize):
        pygame.draw.line(screen, colour, (x, 0), (x, screenSize[1]))
    for y in range(squareSize, screenSize[1], squareSize):
        pygame.draw.line(screen, colour, (0, y), (screenSize[0], y))

def drawFPS():
    text = str(int(clock.get_fps()))
    fps = FPS_font.render(text, 0, pygame.Color("white"))
    screen.blit(fps, (0, 0))

def drawBackground():
    #screen.fill(dark_gray)
    #for x in range(0,screenSize[0],squareSize*2):
    #    for y in range(0,screenSize[1],squareSize*2):
    #        pygame.draw.rect(screen, light_gray , (x, y, squareSize, squareSize))
    #for x in range(squareSize,screenSize[0],squareSize*2):
    #    for y in range(squareSize,screenSize[1],squareSize*2):
    #        pygame.draw.rect(screen, light_gray , (x, y, squareSize, squareSize))

    screen.blit(background, (0,0))

UI = ui.UI()

levelmap = map.Map(int(screenSize[0]/squareSize), int(screenSize[1]/squareSize))
levelmap.setPath()

while RUNNING:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            RUNNING = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                enemy.Squirrel((0,0), enemies)
            elif event.key == pygame.K_t:
                buildings.BasicTower(towers, (int(pos[0]/squareSize)*squareSize, int(pos[1]/squareSize)*squareSize))
                pos = pygame.mouse.get_pos()
                levelmap.place(int(pos[0]/squareSize), int(pos[1]/squareSize))
                levelmap.findPath()


        elif event.type == pygame.MOUSEBUTTONUP:
            if not UI.updateClick(event.pos): #if not clicking on UI
                if event.button == 1: #if left click
                    levelmap.place(int(event.pos[0]/squareSize), int(event.pos[1]/squareSize))
                    levelmap.findPath()
                elif event.button == 3: #if right click
                    levelmap.clear(int(event.pos[0]/squareSize), int(event.pos[1]/squareSize))
                    levelmap.findPath()

    if RUNNING: #If 'x' button not clicked
        
        drawBackground()
        levelmap.drawTiles(screen,squareSize, screenSize)
        #drawOutlines(screen, (0,0,0) , squareSize, screenSize)
        levelmap.drawPath(screen, green, squareSize)
        pos = pygame.mouse.get_pos()
        

        enemies.update(screen)
        towers.update(screen, bullets, enemies)
        screen.blit(mouseposSurface, (int(pos[0]/squareSize)*squareSize, int(pos[1]/squareSize)*squareSize, squareSize, squareSize))

        bullets.update(screen, enemies)

        UI.update(pos)
        UI.draw(screen)

        drawFPS()

        pygame.display.flip()