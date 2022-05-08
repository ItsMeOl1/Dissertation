import pathfinder, pygame
from enemy import Enemy

wall_images = {"top": pygame.transform.scale(pygame.image.load("Sprites/Towers/wall_top.png"), (50,50)),
               "middle": pygame.transform.scale(pygame.image.load("Sprites/Towers/wall_middle.png"), (50,50)),
               "bottom": pygame.transform.scale(pygame.image.load("Sprites/Towers/wall_bottom.png"), (50,50*1.4)),
               "alone": pygame.transform.scale(pygame.image.load("Sprites/Towers/wall_alone.png"), (50,50*1.4))}

class Map:
    def __init__(self, x, y):
        self.max_X = x-1
        self.max_Y = y-1
        self.start = 0,0  # Where enemies start
        self.end = self.max_X,self.max_Y # Where enemies end
        

        self.grid = [[0 for i in range(y)] for j in range(x)] # Create an array of 0s
        self.path = self.findPath()

        self.resource_clay_location = None
        self.resource_clay_amount = 0
    
    def set_start(self, x, y): # Where enemies start
        if x <= self.max_X & y <= self.max_Y & x >= 0 & y >= 0:
            self.start = x,y
        else:
            print("INVALID start set")

    def set_end(self, x, y): # Where enemies end
        if x <= self.max_X & y <= self.max_Y:
            self.end = x,y
        else:
            print("INVALID end set")

    def place(self, x, y, type = 1): # Place a defence in the given coordinate
        self.grid[x][y] = type

    def clear(self, x, y): # Delete a defence in the given coordinate
        self.grid[x][y] = 0
    
    def get_block(self, x, y):
        return self.grid[x][y]

    def drawTiles(self, screen, squareSize, screenSize): # Draw all defences on screen
        for x in range(len(self.grid)):         #
            for y in range(len(self.grid[x])):  # For each grid tile
                top = False
                bottom = False
                if self.grid[x][y] != 0: # If something's placed
                    if y == 0 or self.grid[x][y-1] == 0:
                        top = True
                    if y == (screenSize[1]/squareSize)-1 or self.grid[x][y+1] == 0:
                        bottom = True
                    if top and bottom:
                        screen.blit(wall_images["alone"], (x*squareSize, y*squareSize))
                    elif top:
                        screen.blit(wall_images["top"], (x*squareSize, y*squareSize))
                    elif bottom:
                        screen.blit(wall_images["bottom"], (x*squareSize, y*squareSize))
                    else:
                        screen.blit(wall_images["middle"], (x*squareSize, y*squareSize))
                    
    def findPath(self):
        self.path = pathfinder.astar(self.grid, self.start, self.end)
        if self.path is not False:
            self.setPath(self.path)
        return self.path

    def drawPath(self, screen, colour, squareSize): # Draw green line where the path is
        self.setPath(self.path)
        for i in range(len(self.path)-1):
            start = (self.path[i][0] * squareSize + squareSize/2, self.path[i][1] * squareSize + squareSize/2)
            end = (self.path[i+1][0] * squareSize + squareSize/2, self.path[i+1][1] * squareSize + squareSize/2)
            pygame.draw.line(screen, colour, start, end)
    
    def setPath(self, path = None): # Give the enemies the path
        if path == None:
            path = self.findPath()
        Enemy.path = path