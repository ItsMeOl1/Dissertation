from pygame import sprite, transform
from pygame import image as pyimage
from math import sin, atan, radians, sqrt

class Tower(sprite.Sprite):
    image = pyimage.load("Sprites/Towers/tower.png")
    image = transform.scale(image, (50,50))
    def __init__(self, towerGroup, pos):
        sprite.Sprite.__init__(self)
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
            angle = None
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
        sprite.Sprite.__init__(self)
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

    def update(self, screen, enemyGroup):
        self.move(enemyGroup)
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
    def __init__(self, towerGroup, pos):
        Tower.__init__(self, towerGroup, pos)
        self.type = "Basic"
        self.range = 1000
        self.attack_damage = 1
        self.attack_speed = 5 #minimum 3!
        self.attack_cd = 50
        

