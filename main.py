import pygame
import enemy
import buildings
import map
import ui
import rounds
pygame.init()

# DISPLAY SET UP
screenSize = 1600, 900
squareSize = 50  # 32x18 quares in 1600,900
screen = pygame.display.set_mode(screenSize)

# SET UP
RUNNING = True
clock = pygame.time.Clock()
timePassed = 0

# CONSTANTS
FPS_font = pygame.font.SysFont("Arial", 13)
mouseposSurface = pygame.Surface((squareSize, squareSize))
mouseposSurface.fill((255, 0, 0))
mouseposSurface.set_alpha(15)
background = pygame.image.load("Sprites/Floors/grass.png")
background = pygame.transform.scale(background, (1600, 900))

# SPRITE GROUPS
enemies = pygame.sprite.Group()
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
    screen.blit(background, (0, 0))


def mouseClick(mousePos):
    # Which in game block is being clicked
    xblock = int(mousePos[0]/squareSize)
    yblock = int(mousePos[1]/squareSize)
    if UI.selected == "wall":
        levelmap.place(xblock, yblock)
        if not levelmap.findPath():  # If new wall is blocking the path completely
            levelmap.clear(xblock, yblock)
            levelmap.findPath()
    elif levelmap.get_block(xblock, yblock) == 1:  # If clicked on a wall
        if UI.selected == "bomb":
            levelmap.clear(xblock, yblock)
        elif UI.selected == "tower1":
            buildings.BasicTower(
                towers, (xblock*squareSize, yblock*squareSize))
            levelmap.place(xblock, yblock, 2)
    elif levelmap.get_block(xblock, yblock) > 1:  # If clkicked on a tower
        if UI.selected == "bomb":
            for tower in towers:
                if tower.rect.collidepoint(mousePos):
                    tower.kill()
                    break
            levelmap.clear(xblock, yblock)
            levelmap.findPath()


# INITIALISING GAME OBJECTS
Round = rounds.get_next_round()
UI = ui.UI()

levelmap = map.Map(int(screenSize[0]/squareSize),
                   int(screenSize[1]/squareSize))
levelmap.setPath()

# MAIN GAME LOOP
while RUNNING:
    clock.tick()
    timePassed += clock.get_time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If 'x' button is clicked
            pygame.quit()
            RUNNING = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # If user clicked
            UI.updateClick(event.pos)

    if RUNNING:  # If 'x' button is not clicked
        keys = pygame.key.get_pressed()
        mouseButtons = pygame.mouse.get_pressed()
        mousePos = pygame.mouse.get_pos()

        # If user clicked not on UI
        if mouseButtons[0] and not UI.collision(mousePos):
            mouseClick(mousePos)

        if not enemies and not Round.enemyList:  # If round is over
            Round = rounds.get_next_round()

        drawBackground()
        levelmap.drawTiles(screen, squareSize, screenSize)
        levelmap.drawPath(screen, (0, 255, 0), squareSize)

        ticks = 0
        while timePassed >= 50:
            timePassed -= 50
            ticks += 1

        enemies.update(screen, ticks)
        towers.update(screen, bullets, enemies, ticks)
        UI.update(mousePos)
        bullets.update(screen, enemies, ticks)

        newEnemy = Round.update(ticks)  # Get if an enemy needs to be created
        if newEnemy == "1":
            enemy.Squirrel((0, 0), enemies)

        # Draw a red transparent quare over the square mouse is currently over
        screen.blit(mouseposSurface, (int(mousePos[0]/squareSize)*squareSize, int(
            mousePos[1]/squareSize)*squareSize, squareSize, squareSize))
        UI.draw(screen)

        drawFPS()
        drawRound()

        pygame.display.flip()
