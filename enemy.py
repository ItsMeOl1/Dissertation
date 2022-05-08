from pygame import sprite, transform
from pygame import image as pyimage


class Enemy(sprite.Sprite):
    path = []

    def __init__(self, startPos, enemyGroup):
        super().__init__()
        enemyGroup.add(self)
        self.pos = startPos
        self.realpos = list(startPos)
        self.nextDestination = 0  # Index of self.path this instace is heading towards
        self.speed = 1
        self.direction = 3  # 8-direction with 1 being up

    def move(self):
        if self.atDestination():
            self.nextDestination += 1
            if self.nextDestination >= len(self.path):
                self.atEnd()
            else:
                self.getDirection()
        else:
            if self.direction in [2, 4, 6, 8]:
                self.go(self.speed * 0.7)
            else:
                self.go(self.speed)

    def atEnd(self):
        # Player taking damage goes here
        self.kill()

    def go(self, distance):
        if self.direction in [2, 3, 4]:  # if going right
            self.realpos[0] += distance
        elif self.direction in [6, 7, 8]:  # if going left
            self.realpos[0] -= distance
        if self.direction in [1, 2, 8]:  # if going up
            self.realpos[1] -= distance
        elif self.direction in [4, 5, 6]:  # if going down
            self.realpos[1] += distance
        self.rect.center = self.realpos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    # Get which direction the enemy needs to go to reach next point in path
    def getDirection(self):
        direction = [0, 0]
        if self.path[self.nextDestination-1][0] < self.path[self.nextDestination][0]:
            direction[0] = 1
        elif self.path[self.nextDestination-1][0] > self.path[self.nextDestination][0]:
            direction[0] = -1
        if self.path[self.nextDestination-1][1] < self.path[self.nextDestination][1]:
            direction[1] = -1
        elif self.path[self.nextDestination-1][1] > self.path[self.nextDestination][1]:
            direction[1] = 1
        self.direction = {"[0, 1]": 1, "[1, 1]": 2, "[1, 0]": 3, "[1, -1]": 4,
                          "[0, -1]": 5, "[-1, 1]": 6, "[-1, 0]": 7, "[-1, -1]": 8}[str(direction)]
        self.getImage()

    def getImage(self):  # To be overwritten by children
        pass

    def setDirection(self, direction):
        self.direction = direction
        self.getImage()

    def atDestination(self):
        if self.direction in [2, 3, 4]:  # if going right
            if self.rect.centerx >= self.path[self.nextDestination][0]*50 + 25:
                return True
        elif self.direction in [6, 7, 8]:  # if going left
            if self.rect.centerx <= self.path[self.nextDestination][0]*50 + 25:
                return True
        if self.direction in [1, 2, 8]:  # if going up
            if self.rect.centery <= self.path[self.nextDestination][1]*50 + 25:
                return True
        elif self.direction in [4, 5, 6]:  # if going down
            if self.rect.centery >= self.path[self.nextDestination][1]*50 + 25:
                return True
        return False


class Arrow(Enemy):  # Test class now unused
    # facing right by default
    oimage = pyimage.load("Sprites/Enemies/arrow.png")
    oimage = transform.scale(oimage, (30, 30))

    def __init__(self, startPos, enemyGroup):
        super().__init__(startPos, enemyGroup)
        self.image = self.oimage
        self.rect = self.image.get_rect()
        self.rect.x = startPos[0] * 50 - 50
        self.rect.y = startPos[1] * 50 + 25
        self.realpos = list(self.rect.topleft)
        self.setDirection(3)

    def getImage(self):
        self.image = transform.rotate(
            self.oimage, (self.direction-1) * -45)  # Rotate to face right


class Squirrel(Enemy):
    images = {7: [transform.scale(pyimage.load("Sprites/Enemies/Squirrel/squirrel_left1.png"), (36, 36)),
                  # only 2 frames for side animation
                  transform.scale(pyimage.load(
                      "Sprites/Enemies/Squirrel/squirrel_left2.png"), (36, 36)),
                  transform.scale(pyimage.load("Sprites/Enemies/Squirrel/squirrel_left1.png"), (36, 36))],  # hence the repeat here
              1:   [transform.scale(pyimage.load("Sprites/Enemies/Squirrel/squirrel_up1.png"), (36, 36)),
                    transform.scale(pyimage.load(
                        "Sprites/Enemies/Squirrel/squirrel_up15.png"), (36, 36)),
                    transform.scale(pyimage.load("Sprites/Enemies/Squirrel/squirrel_up2.png"), (36, 36))],
              5: [transform.scale(pyimage.load("Sprites/Enemies/Squirrel/squirrel_down1.png"), (36, 36)),
                  transform.scale(pyimage.load(
                      "Sprites/Enemies/Squirrel/squirrel_down15.png"), (36, 36)),
                  transform.scale(pyimage.load("Sprites/Enemies/Squirrel/squirrel_down2.png"), (36, 36))]
              }
    images[3] = [transform.flip(images[7][0], True, False),  # 3 (left) is just 7 (right) flipped
                 transform.flip(images[7][1], True, False),
                 transform.flip(images[7][2], True, False)]
    shadow = transform.scale(pyimage.load(
        "Sprites/Enemies/Squirrel/shadow.png"), (36, 40))

    def __init__(self, startPos, enemyGroup):
        super().__init__(startPos, enemyGroup)
        self.image = self.images[7][0]
        self.rect = self.image.get_rect()
        self.rect.x = startPos[0] * 50 - 50
        self.rect.y = startPos[1] * 50 + 25
        self.realpos = list(self.rect.topleft)
        self.animationCD = 5
        self.nextFrame = self.animationCD
        self.frameOrder = [0, 1, 2, 1]
        self.frame = 0
        self.speed = 3
        self.setDirection(3)

    def getImage(self):
        self.image = self.images[self.direction][self.frameOrder[self.frame]]

    def update(self, screen, ticks):
        while ticks > 0:
            self.move()
            ticks -= 1
            self.nextFrame -= 1

        while self.nextFrame < 1:
            self.nextFrame += self.animationCD
            self.frame += 1
            if self.frame >= len(self.frameOrder):
                self.frame = 0
            self.getImage()

        self.draw(screen)

    def draw(self, screen):
        screen.blit(self.shadow, self.rect.topleft)
        super().draw(screen)
