from pygame import sprite
from pygame import image as pyimage

class Enemy(sprite.Sprite):
    path = []
    def __init__(self, startPos, enemyGroup):
        sprite.Sprite.__init__(self)
        enemyGroup.add(self)
        self.pos = startPos
        self.nextDestination = 0
        self.speed = 1
        self.direction = 3 #8-direction with 1 being up


    def update(self, screen):
        self.move()
        self.draw(screen)

    def move(self):
        if self.atDestination():
            self.nextDestination += 1
            if self.nextDestination >= len(self.path):
                self.kill()
            else:
                self.getDirection()
        else:
            if self.direction in [2,4,6,8]:
                self.go(self.speed* 0.7)
            else:
                self.go(self.speed)

    def go(self, distance):
        if self.direction in [2,3,4]: #if going right
            self.rect.x += distance
        elif self.direction in [6,7,8]: #if going left
            self.rect.x -= distance
        if self.direction in [1,2,8]: #if going up
            self.rect.y -= distance
        elif self.direction in [4,5,6]: #if going down
            self.rect.y += distance
    
    def kill(self):
        sprite.Sprite.kill(self)
        #do health stuff here

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        

    def getDirection(self):
        direction = [0,0]
        if self.path[self.nextDestination-1][0] < self.path[self.nextDestination][0]: 
            direction[0] = 1
        elif self.path[self.nextDestination-1][0] > self.path[self.nextDestination][0]:
            direction[0] = -1
        if self.path[self.nextDestination-1][1] < self.path[self.nextDestination][1]:
            direction[1] = -1
        elif self.path[self.nextDestination-1][1] > self.path[self.nextDestination][1]:
            direction[1] = 1
        self.direction = {"[0, 1]": 1, "[1, 1]": 2, "[1, 0]": 3, "[1, -1]": 4, "[0, -1]": 5, "[-1, 1]": 6, "[-1, 0]": 7, "[-1, -1]": 8}[str(direction)]
        
    def atDestination(self):
        if self.direction in [2,3,4]: #if going right
            if self.rect.x >= self.path[self.nextDestination][0]*50 + 25:
                return True
        elif self.direction in [6,7,8]: #if going left
            if self.rect.x <= self.path[self.nextDestination][0]*50 + 25:
                return True
        if self.direction in [1,2,8]: #if going up
            if self.rect.y <= self.path[self.nextDestination][1]*50 + 25:
                return True
        elif self.direction in [4,5,6]: #if going down
            if self.rect.y >= self.path[self.nextDestination][1]*50 + 25:
                return True
        return False

class Arrow(Enemy):
    image = pyimage.load("Enemy.png") #facing right by default
    def __init__(self,startPos, enemyGroup):
        Enemy.__init__(self, startPos, enemyGroup)
        self.rect = self.image.get_rect()
        self.rect.x = startPos[0] * 50
        self.rect.y = startPos[1] * 50
    