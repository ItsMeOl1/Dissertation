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
health = 10
money = 10
GAMEOVER = False

# CONSTANTS
FPS_font = pygame.font.SysFont("Arial", 13)
mouseposSurface = pygame.Surface((squareSize, squareSize))
mouseposSurface.fill((255, 0, 0))
mouseposSurface.set_alpha(15)
background = pygame.image.load("Sprites/Floors/grass.png")
heart = pygame.image.load("Sprites/heart.png")
coin = pygame.image.load("Sprites/coin.png")
background = pygame.transform.scale(background, (1600, 900))
heart = pygame.transform.scale(heart, (50, 50))
coin = pygame.transform.scale(coin, (50, 50))

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

def drawHealth():
    text = FPS_font.render(str(health), 0, pygame.Color("white"))
    rect = text.get_rect()
    healthText = pygame.transform.scale(text, (rect.w * 5, rect.h * 5))
    screen.blit(healthText, (500, -10))
    screen.blit(heart, (450, 10))

def drawMoney():
    text = FPS_font.render(str(money), 0, pygame.Color("white"))
    rect = text.get_rect()
    moneyText = pygame.transform.scale(text, (rect.w * 5, rect.h * 5))
    screen.blit(moneyText, (900, -10))
    screen.blit(coin, (850, 10))


def drawGameOver():
    text = "Game Over"
    text = FPS_font.render(text, 0, pygame.Color("white"))
    rect = text.get_rect()
    overText = pygame.transform.scale(text, (rect.w * 20, rect.h * 20))
    rect = overText.get_rect()
    rect.centerx = 800
    rect.centery = 450

    screen.blit(overText, rect)

def drawBackground():
    screen.blit(background, (0, 0))


def mouseClick(mousePos, money):
    # Which in game block is being clicked
    xblock = int(mousePos[0]/squareSize)
    yblock = int(mousePos[1]/squareSize)
    if UI.selected == "wall":
        if money > 0:
            if levelmap.get_block(xblock,yblock) == 0:
                levelmap.place(xblock, yblock)
                money -= 1
                if not levelmap.findPath():  # If new wall is blocking the path completely
                    levelmap.clear(xblock, yblock)
                    levelmap.setPath()
    elif levelmap.get_block(xblock, yblock) == 1:  # If clicked on a wall
        if UI.selected == "bomb":
            levelmap.clear(xblock, yblock)
            levelmap.setPath()
        elif UI.selected == "tower1":
            if money > 1 and levelmap.get_block(xblock, yblock) != 2:
                buildings.BasicTower(
                    towers, (xblock*squareSize, yblock*squareSize))
                levelmap.place(xblock, yblock, 2)
                money -= 2
    elif levelmap.get_block(xblock, yblock) > 1:  # If clicked on a tower
        if UI.selected == "bomb":
            for tower in towers:
                if tower.rect.collidepoint(mousePos):
                    tower.kill()
                    break
            levelmap.clear(xblock, yblock)
            levelmap.setPath()
    return money


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
        if GAMEOVER:
            drawGameOver()
            pygame.display.flip()
        else:
            keys = pygame.key.get_pressed()
            mouseButtons = pygame.mouse.get_pressed()
            mousePos = pygame.mouse.get_pos()

            # If user clicked not on UI
            if mouseButtons[0] and not UI.collision(mousePos):
                money = mouseClick(mousePos, money)

            if not enemies and not Round.enemyList:  # If round is over
                Round = rounds.get_next_round()

            drawBackground()
            levelmap.drawTiles(screen, squareSize, screenSize)
            levelmap.drawPath(screen, (0, 255, 0), squareSize)

            ticks = 0
            while timePassed >= 20:
                timePassed -= 20
                ticks += 1

            for e in enemies:
                if e.update(screen, ticks):
                    health -= 1
            
            if health < 1:
                GAMEOVER = True
            
            towers.update(screen, bullets, enemies, ticks)
            UI.update(mousePos)
            
            for b in bullets:
                if b.update(screen, enemies, ticks) == True: 
                    money += 1

            newEnemy = Round.update(ticks)  # Get if an enemy needs to be created
            if newEnemy == "1":
                enemy.Squirrel((0, 0), enemies)

            # Draw a red transparent quare over the square mouse is currently over
            screen.blit(mouseposSurface, (int(mousePos[0]/squareSize)*squareSize, int(
                mousePos[1]/squareSize)*squareSize, squareSize, squareSize))
            UI.draw(screen)

            drawFPS()
            drawRound()
            drawHealth()
            drawMoney()

            pygame.display.flip()
