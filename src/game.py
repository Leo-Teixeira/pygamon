import pygame
import pytmx
import pyscroll

####création de la classe game permettant de lancer la fenetre du jeu avec tous les composant
from player import Player
from src.dialog import dialogBox
from src.map import MapManager


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('pygamon')

        # generer le joueur
        self.player = Player()
        self.map_manager = MapManager(self.screen, self.player)
        self.dialog_box = dialogBox()


    ##fonction qui permet de recuperer le deplacement du joueur avec les touche
    def handle_input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            self.player.move_up()
        elif pressed[pygame.K_DOWN]:
            self.player.move_down()
        elif pressed[pygame.K_LEFT]:
            self.player.move_left()
        elif pressed[pygame.K_RIGHT]:
            self.player.move_right()



    def update(self):
        self.map_manager.update()

    def run(self):

        clock = pygame.time.Clock()  ##permet de fixer le nombre de fps a chaque tour de boucle

        running = True
        while running:

            self.update()  ##update le joueur
            self.player.save_location()
            self.handle_input()
            self.map_manager.draw()
            self.dialog_box.render(self.screen)
            pygame.display.flip()  # actualise
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.dialog_box.execute()
        clock.tick(60)  ##defini le nombre de fps
        pygame.quit()
