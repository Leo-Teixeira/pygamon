import pygame


class AnimateSprite(pygame.sprite.Sprite):

    def __init__(self, name):
        super().__init__()
        self.sprite_sheet = pygame.image.load(f'../image/{name}.png')  ##declare l'image
        self.animation_index = 0
        ## definition des differentes images du joueur quand il avance
        self.images = {'down': self.get_images(0),
                       'left': self.get_images(32),
                       'right': self.get_images(64),
                       'up': self.get_images(96)}
        self.speed = 0.1 ##declare la vitesse du joueur
        self.clock = 0

    def change_animation(self, name):
        self.image = self.images[name][self.animation_index]
        self.image.set_colorkey([0, 0, 0])
        self.clock += self.speed * 8

        if self.clock >= 100:
            self.animation_index += 1

            if self.animation_index >= len(self.images[name]):
                self.animation_index = 0
            self.clock = 0

    def get_images(self, y):
        images = []

        for i in range(0, 3):
            x = i * 32
            image = self.getImage(x, y)
            images.append(image)
        return images

    ##permettre de recuperer l'image souhaiter
    def getImage(self, x, y):
        image = pygame.Surface([32, 32])  ##recupere la surface de l'image
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))  ## extrait morceau du spreet sheet
        return image
