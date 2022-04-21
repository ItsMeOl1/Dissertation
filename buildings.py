from pygame import sprite, transform
from pygame import image as pyimage
from math import atan, degrees, sqrt

class Tower(sprite.Sprite):
    image = pyimage.load("Sprites/Towers/tower.png")
    image = transform.scale(image, (50,50))
    def __init__(self, towerGroup, pos):
        super().__init__()
        self.add(towerGroup)
        self.rect = self.image.get_rect()
        self.type = "invalid"
        self.range = 0
        self.attack_damage = 0
        self.attack_speed = 0 #minimum 3!
        self.attack_cd = 100
        self.next_attack = 0
        self.rect.topleft = pos

    def update(self, screen, bulletGroup, enemyGroup):
        self.draw(screen)
        self.next_attack -= 1
        if self.next_attack < 1:
            for i in enemyGroup:
                dx = i.rect.centerx - self.rect.centerx
                dy = i.rect.centery - self.rect.centery
                dist = sqrt(dx**2 + dy**2)
                if dist < self.range:
                    self.next_attack = self.attack_cd
                    self.shoot(dy, dx, bulletGroup)
                    return

    def shoot(self, dy, dx, bulletGroup):
        Bullet (self.rect.center, self.attack_damage, self.attack_speed, dy, dx, bulletGroup)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Bullet(sprite.Sprite):
    image = pyimage.load("Sprites/bullet.png")
    def __init__(self, pos, damage, speed, dy, dx, bulletGroup):
        super().__init__()
        self.rect = self.image.get_rect()
        self.add(bulletGroup)
        self.damage = damage
        self.speed = speed
        self.rect.center = pos
        self.realCenter = list(pos)

        length = sqrt(self.speed ** 2 + dx ** 2)
        ratio = self.speed / length
        dy *= ratio
        dx *= ratio

        self.movement = (dx, dy)

    def update(self, screen, enemyGroup, ticks):
        while ticks > 0:
            self.move(enemyGroup)
            ticks -= 1
        if self.rect.centerx < -50 or self.rect.centerx > 1650: #hardcoded!!! TODO
                self.kill()
        elif self.rect.centery < -50 or self.rect.centery > 950: #hardcoded!!! TODO
                self.kill()
        if self.alive():
            self.draw(screen)


    def move(self, enemyGroup):
        for i in range(0, self.speed):
            self.realCenter[0] += self.movement[0]/self.speed
            self.realCenter[1] += self.movement[1]/self.speed
            self.rect.center = self.realCenter
            for enemy in enemyGroup:
                if enemy.rect.colliderect(self.rect):
                    self.kill()
                    enemy.kill()
                    return enemy

    def kill(self):
        sprite.Sprite.kill(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class BasicTower(Tower):
    image = pyimage.load("Sprites/Towers/tower.png")
    towerTurret = pyimage.load("Sprites/Towers/towerGun.png")
    image = transform.scale(image, (50,50))
    towerTurret = transform.scale(towerTurret, (60,60))
    def __init__(self, towerGroup, pos):
        Tower.__init__(self, towerGroup, pos)
        self.type = "Basic"
        self.range = 1000
        self.attack_damage = 1
        self.attack_speed = 15
        self.attack_cd = 50
        self.towerGunImage = self.towerTurret
        self.towerGunRect = self.towerGunImage.get_rect()
        self.towerGunRect.center = self.rect.center
        self.angle = 0

    def update(self, screen, bulletGroup, enemyGroup, ticks):
        self.draw(screen)
        self.next_attack -= ticks
        targetted = False
        for i in enemyGroup:
            dx = i.rect.centerx - self.rect.centerx
            dy = i.rect.centery - self.rect.centery
            dist = sqrt(dx**2 + dy**2)
            if dist < self.range:
                targetted = True
                while self.next_attack <= 0:
                    self.next_attack += self.attack_cd
                    self.shoot(dy, dx, bulletGroup)
                if dy == 0:
                    dy = 0.001
                self.angle = degrees(atan(dx/dy))
                if dy > 0 and dx > -0.001: #below and to right (needs to include dx = 0 ie straight down)
                    self.angle = 180 - self.angle
                    self.angle *= -1
                elif dy > 0 and dx < 0: #below and to right
                    self.angle -= 180
                self.towerGunImage = transform.rotate(self.towerTurret, self.angle)
                self.towerGunRect = self.towerGunImage.get_rect()
                self.towerGunRect.center = self.rect.center
                screen.blit(self.towerGunImage, self.towerGunRect.topleft)
                break
        if not targetted:
            screen.blit(self.towerGunImage, self.towerGunRect.topleft)
        

