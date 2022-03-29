import sys, pygame, pathfinder, Enemy
pygame.init()

##SETTING UP THE DISPLAY
screenSize = 1600, 900 
squareSize = 50 #32x18
RUNNING = True
screen = pygame.display.set_mode(screenSize)

##COLOUR CONSTANTS 
dark_gray = 155, 155, 155
light_gray = 200,200,200
black = 0,0,0
red = 255,0,0
green = 0,255,0

##LOAD IMAGES
wall = pygame.image.load("wall.png")
wall = pygame.transform.scale(wall, (squareSize,squareSize))

##SET UP SPRITE GROUPS
enemies = pygame.sprite.Group()
enemies.add(Enemy.Arrow((0,0)))

def drawOutlines(screen, colour, squareSize, screenSize):
    for x in range(squareSize, screenSize[0], squareSize):
        pygame.draw.line(screen, colour, (x, 0), (x, screenSize[1]))
    for y in range(squareSize, screenSize[1], squareSize):
        pygame.draw.line(screen, colour, (0, y), (screenSize[0], y))

class Map:
    def __init__(self, x, y):
        self.max_X = x-1
        self.max_Y = y-1
        self.start = 0,0
        self.end = self.max_X,self.max_Y

        self.grid = [[0 for i in range(y)] for j in range(x)]
    
    def set_start(self, x, y):
        if x <= self.max_X & y <= self.max_Y & x >= 0 & y >= 0:
            self.start = x,y
        else:
            print("INVALID start set")

    def set_end(self, x, y):
        if x <= self.max_X & y <= self.max_Y:
            self.end = x,y
        else:
            print("INVALID end set")

    def place(self, x, y):
        self.grid[x][y] = 1

    def clear(self, x, y):
        self.grid[x][y] = 0

    def drawTiles(self, screen, squareSize):
        for x in range(len(self.grid)):
            for y in range(len(self.grid[x])):
                if self.grid[x][y] == 1:
                    screen.blit(wall, (x*squareSize, y*squareSize))

    def findPath(self):
        return pathfinder.astar(self.grid, self.start, self.end)

    def drawPath(self, screen, colour, squareSize):
        path = self.findPath()
        self.setPath(path)
        for i in range(len(path)-1):
            start = (path[i][0] * squareSize + squareSize/2, path[i][1] * squareSize + squareSize/2)
            end = (path[i+1][0] * squareSize + squareSize/2, path[i+1][1] * squareSize + squareSize/2)
            pygame.draw.line(screen, colour, start, end)
    
    def setPath(self, path = None):
        if path == None:
            path = self.findPath()
        Enemy.Enemy.path = path

map = Map(int(screenSize[0]/squareSize), int(screenSize[1]/squareSize))
map.setPath()

while RUNNING:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
            RUNNING = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                enemies.add(Enemy.Arrow((0,0)))

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1: #if left click
                map.place(int(event.pos[0]/squareSize), int(event.pos[1]/squareSize))
            elif event.button == 3: #if right click
                map.clear(int(event.pos[0]/squareSize), int(event.pos[1]/squareSize))

    if RUNNING: #If 'x' button not clicked
        screen.fill(dark_gray)
        for x in range(0,screenSize[0],squareSize*2):
            for y in range(0,screenSize[1],squareSize*2):
                pygame.draw.rect(screen, light_gray , (x, y, squareSize, squareSize))
        for x in range(squareSize,screenSize[0],squareSize*2):
            for y in range(squareSize,screenSize[1],squareSize*2):
                pygame.draw.rect(screen, light_gray , (x, y, squareSize, squareSize))
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(screen, red, (int(pos[0]/squareSize)*squareSize, int(pos[1]/squareSize)*squareSize, squareSize, squareSize))
        

        map.drawTiles(screen,squareSize)
        drawOutlines(screen, black, squareSize, screenSize)
        map.drawPath(screen, green, squareSize)

        enemies.update(screen)

        pygame.display.flip()