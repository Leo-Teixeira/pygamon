import pygame

##element graphique qui peut interagir avec d'autre sprite qui sont non static
from src.animation import AnimateSprite


class Entity(AnimateSprite):

    def __init__(self, name, x, y):
        super().__init__(name)
        self.image = self.getImage(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect() ## attribue une position a l'image
        self.position = [x, y]
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 12) ## defini ou sont les pied du joueur
        self.oldPosition = self.position.copy() ## copie la derniere position du joueur

    def save_location(self):
        self.oldPosition = self.position.copy()

    ##fonction qui permette de faire bouger le joueur
    def move_right(self):
        self.change_animation('right')
        self.position[0] += self.speed

    def move_left(self):
        self.change_animation('left')
        self.position[0] -= self.speed

    def move_up(self):
        self.change_animation('up')
        self.position[1] -= self.speed

    def move_down(self):
        self.change_animation('down')
        self.position[1] += self.speed

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom ## recupere la position de ses pieds

    def move_back(self):
        self.position = self.oldPosition
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

class Player(Entity):

    def __init__(self):
        super().__init__("playerMain", 0, 0)

class Pnj(Entity):

    def __init__(self, name, nb_point):
        super().__init__(name, 0, 0)
        self.nb_point = nb_point
        self.points = []
        self.name = name
        self.speed = 1
        self.current_point = 0

    def move_pnj(self):
        current_point = self.current_point
        target_point = self.current_point + 1

        if target_point >= self.nb_point:
            target_point = 0

        current_rect = self.points[current_point]
        target_rect = self.points[target_point]

        if current_rect.y < target_rect.y and abs(current_rect.x - target_rect.x) < 5:
            self.move_down()
        elif current_rect.y > target_rect.y and abs(current_rect.x - target_rect.x) < 5:
            self.move_up()
        elif current_rect.x > target_rect.x and abs(current_rect.y - target_rect.y) < 5:
            self.move_left()
        elif current_rect.x < target_rect.x and abs(current_rect.y - target_rect.y) < 5:
            self.move_right()

        if self.rect.colliderect(target_rect):
            self.current_point = target_point

    def teleport_spawn(self):
        location = self.points[self.current_point]
        self.position[0] = location.x
        self.position[1] = location.y
        self.save_location()

    def load_point(self, tmx_data):
        for num in range(1, self.nb_point + 1):
            point = tmx_data.get_object_by_name(f"{self.name}_path{num}")
            rect = pygame.Rect(point.x, point.y, point.width, point.height)
            self.points.append(rect)