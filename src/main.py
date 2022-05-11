import pygame

from game import Game

#####generation de la base du module
if __name__ == '__main__':
    pygame.init()  # lancement de la fenetre
    game = Game()  # instancie la classe game
    game.run()
