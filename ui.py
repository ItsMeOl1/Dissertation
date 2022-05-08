import pygame


class UI:
    def __init__(self):
        self.open = False
        self.open_amount = 0
        self.open_speed = 1.3
        self.xoffset = 0
        self.selected = "wall"  # What button is pressed

        self.image = pygame.transform.scale(
            pygame.image.load("Sprites/UI/MenuBG.png"), (100, 900))
        self.rect = self.image.get_rect()
        self.rect.topleft = (1600, 0)

        openButtonImage = pygame.transform.scale(
            pygame.image.load("Sprites/UI/Pullout.png"), (50, 100))
        openButtonHover = pygame.transform.scale(
            pygame.image.load("Sprites/UI/PulloutHover.png"), (50, 100))
        openButtonPress = pygame.transform.scale(
            pygame.image.load("Sprites/UI/PulloutPush.png"), (50, 100))
        openButtonPressHover = pygame.transform.scale(
            pygame.image.load("Sprites/UI/PulloutPushHover.png"), (50, 100))

        wallButtonImage = pygame.transform.scale(
            pygame.image.load("Sprites/UI/WallButton.png"), (14*5, 15*5))
        wallButtonHover = pygame.transform.scale(pygame.image.load(
            "Sprites/UI/WallButtonHover.png"), (14*5, 15*5))
        wallButtonPress = pygame.transform.scale(
            pygame.image.load("Sprites/UI/WallButtonPush.png"), (14*5, 15*5))

        towerButtonImage = pygame.transform.scale(pygame.image.load(
            "Sprites/UI/BasicTowerButton.png"), (14*5, 15*5))
        towerButtonHover = pygame.transform.scale(pygame.image.load(
            "Sprites/UI/BasicTowerButtonHover.png"), (14*5, 15*5))
        towerButtonPress = pygame.transform.scale(pygame.image.load(
            "Sprites/UI/BasicTowerButtonPush.png"), (14*5, 15*5))

        bombButtonImage = pygame.transform.scale(
            pygame.image.load("Sprites/UI/BombButton.png"), (14*5, 15*5))
        bombButtonHover = pygame.transform.scale(pygame.image.load(
            "Sprites/UI/BombButtonHover.png"), (14*5, 15*5))
        bombButtonPress = pygame.transform.scale(
            pygame.image.load("Sprites/UI/BombButtonPush.png"), (14*5, 15*5))

        self.buttons = [Button(openButtonImage, openButtonHover, openButtonPress, openButtonPressHover, (1550, 400), -50, "open"),
                        Button(wallButtonImage, wallButtonHover, wallButtonPress,
                               wallButtonPress, (1650, 50), 15, "wall"),
                        Button(towerButtonImage, towerButtonHover, towerButtonPress,
                               towerButtonPress, (1650, 200), 15, "tower1"),
                        Button(bombButtonImage, bombButtonHover, bombButtonPress, bombButtonPress, (1650, 800), 15, "bomb")]

        self.buttons[1].set_press(True)

    def collision(self, mousePos):  # Check if a click was on the UI
        onMenu = False
        if self.buttons[0].get_hit(mousePos):  # If on open button
            onMenu = True
        elif self.get_hit(mousePos):  # If on main UI
            onMenu = True
        return onMenu

    def updateClick(self, mousePos):  # Make buttons do their effect
        for button in self.buttons:
            if button.get_hit(mousePos):  # If clicked a button
                info = button.info()
                if info[1] == "open":
                    self.open = not self.open
                    button.set_press(not button.pressed)
                else:
                    for i in self.buttons:  # Set every button to not be pressed
                        if i.info()[1] != "open":  # Except the open button
                            i.set_press(False)
                    button.set_press(True)
                    self.selected = info[1]

        return self.collision(mousePos)

    def update(self, mousePos):
        for button in self.buttons:
            if button.get_hit(mousePos):  # If hovering over button
                button.set_hover(True)
            else:
                button.set_hover(False)

        if self.open and self.open_amount < 90:  # If opening
            self.move()
        elif (not self.open) and self.open_amount > 0:  # If closing
            self.move()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for button in self.buttons:
            button.draw(screen)

    def move(self):  # Move whole UI
        if self.open:
            self.open_amount += self.open_speed
        else:
            self.open_amount -= self.open_speed

        self.rect.x = 1600 - self.open_amount
        for button in self.buttons:
            button.rect.x = 1600 - self.open_amount + button.xoffset

    def get_hit(self, point):  # If hit main UI
        return self.rect.collidepoint(point)


class Button:
    def __init__(self, image, image_hover, image_pressed, image_press_hover, location, x, name):
        self.imageIndex = 0
        self.images = [image, image_hover, image_pressed, image_press_hover]
        self.rect = self.images[0].get_rect()
        self.rect.topleft = location
        self.hovered = False
        self.pressed = False
        self.xoffset = x
        self.name = name

    def set_hover(self, value):  # Is the mouse hovering over the button
        self.hovered = value
        self.update_image()

    def set_press(self, value):  # Has the button been clicked
        self.pressed = value
        self.update_image()

    def info(self):
        return [self.pressed, self.name]

    def update_image(self):
        self.imageIndex = 0
        if self.pressed:
            self.imageIndex += 2
        if self.hovered:
            self.imageIndex += 1

    def get_hit(self, point):  # Is a point on the button
        return self.rect.collidepoint(point)

    def draw(self, screen):
        screen.blit(self.images[self.imageIndex], self.rect)
