from pygame import sprite, transform
from pygame import image as pyimage
from math import cos, radians, sqrt

class Tower(sprite.Sprite):
    image = pyimage.load("tower.png")
    image = transform.scale(image, (50,50))
    def __init__(self, towerGroup, pos):
        sprite.Sprite.__init__(self)
        self.add(towerGroup)
        self.rect = self.image.get_rect()
        self.type = "invalid"
        self.range = 0
        self.attack_damage = 0
        self.attack_speed = 0
        self.attack_cd = 100
        self.next_attack = 0
        self.rect.topleft = pos

    def update(self, screen, bulletGroup):
        #add targeting
        self.draw(screen)
        if self.next_attack < 1:
            self.shoot(90, bulletGroup)
            self.next_attack = self.attack_cd

    def shoot(self, angle, bulletGroup):
        Bullet (self.rect.center, self.attack_damage, self.attack_speed, angle, bulletGroup)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class Bullet(sprite.Sprite):
    image = pyimage.load("bullet.png")
    def __init__(self, pos, damage, speed, angle, bulletGroup):
        sprite.Sprite.__init__(self)
        self.rect = self.image.get_rect()
        self.add(bulletGroup)
        self.damage = damage
        self.speed = speed
        self.rect.center = pos
        dx = cos((radians(angle)))
        dy = sqrt(self.speed ** 2 - dx ** 2)
        self.movement = (dx, dy)

    def update(self, screen, enemyGroup):
        self.move(enemyGroup)
        if self.alive():
            self.draw(screen)


    def move(self, enemyGroup):
        for i in range(0, self.speed):
            self.rect.centerx += self.movement[0]/self.speed*i
            self.rect.centery += self.movement[1]/self.speed*i
            for enemy in enemyGroup:
                if enemy.rect.colliderect(self.rect):
                    self.kill()
                    return enemy

    def kill(self):
        sprite.Sprite.kill(self)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

class BasicTower(Tower):
    def __init__(self, towerGroup, pos):
        Tower.__init__(self, towerGroup, pos)
        self.type = "Basic"
        self.range = 300
        self.attack_damage = 1
        self.attack_speed = 10
        

