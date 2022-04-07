import pygame

class UI:
    def __init__(self):
        self.open = False
        self.open_amount = 0
        self.open_speed = 5

        openButtonImage = pygame.transform.scale(pygame.image.load("Sprites/UI/Pullout.png"), (50,100))
        openButtonHover = pygame.transform.scale(pygame.image.load("Sprites/UI/PulloutHover.png"), (50,100))
        openButtonPress = pygame.transform.scale(pygame.image.load("Sprites/UI/PulloutPush.png"), (50,100))
        openButtonPressHover = pygame.transform.scale(pygame.image.load("Sprites/UI/PulloutPushHover.png"), (50,100))
        self.openButton = Button(openButtonImage, openButtonHover, openButtonPress, openButtonPressHover, (1550,400))

        self.image = pygame.transform.scale(pygame.image.load("Sprites/UI/MenuBG.png"), (100,900))
        self.rect = self.image.get_rect()
        self.rect.topleft = (1600, 0)

    def updateClick(self, mousePos):
        onMenu = False
        if self.openButton.get_hit(mousePos):
            onMenu = True
            self.openButton.set_press(not self.openButton.pressed)
            self.open = self.openButton.pressed
        elif self.get_hit(mousePos):
            onMenu = True
        return onMenu

    def update(self, mousePos):
        if self.openButton.get_hit(mousePos):
            self.openButton.set_hover(True)
        else:
            self.openButton.set_hover(False)

        if self.open and self.open_amount < 100:
            self.move()
        elif (not self.open) and self.open_amount > 0:
            self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        self.openButton.draw(screen)

    def move(self):
        if self.open:
            self.open_amount += self.open_speed
            self.rect.x -= self.open_speed
            self.openButton.rect.x -= self.open_speed
        else:
            self.open_amount -= self.open_speed
            self.rect.x += self.open_speed
            self.openButton.rect.x += self.open_speed

    def get_hit(self, point):
        return self.rect.collidepoint(point)



class Button:
    def __init__(self, image, image_hover, image_pressed, image_press_hover, location):
        self.imageIndex = 0
        self.images = [image, image_hover, image_pressed, image_press_hover]
        self.rect = self.images[0].get_rect()
        self.rect.topleft = location
        self.hovered = False
        self.pressed = False

    def set_hover(self, value):
        self.hovered = value
        self.update_image()

    def set_press(self, value):
        self.pressed = value
        self.update_image()

    def update_image(self):
        self.imageIndex = 0
        if self.pressed:
            self.imageIndex += 2
        if self.hovered:
            self.imageIndex += 1

    def get_hit(self, point):
        return self.rect.collidepoint(point)

    def draw(self, screen):
        screen.blit(self.images[self.imageIndex], self.rect)
    