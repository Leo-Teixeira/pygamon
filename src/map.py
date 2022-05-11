from dataclasses import dataclass
import pygame, pytmx, pyscroll

from src.player import Pnj


@dataclass()
class Portail:
    from_world: str
    origin_point: str
    target_world: str
    teleport_point: str

@dataclass()
class Map:
    name: str
    walls: list[pygame.Rect]
    group: pyscroll.PyscrollGroup
    tmx_data: pytmx.TiledMap
    portals: list[Portail]
    pnj: list[Pnj]


class MapManager:

    def __init__(self, screen, player, origin_point=None):
        ##dictionnaire qui va permettre de stocker caracteristique des map
        self.maps = dict()
        self.screen = screen
        self.player = player
        self.current_map = "world"

        self.register_map("world", portals=[Portail(from_world="world", origin_point="enter_house", target_world="house", teleport_point="spawn_house"), Portail(from_world="world", origin_point="enter_beach", target_world="mer", teleport_point="spawn_beach")], pnj=[Pnj("paul", nb_point=4)])
        self.register_map("house", portals=[Portail(from_world="house", origin_point="exit_house", target_world="world", teleport_point="enter_house_exit")])
        self.register_map("mer", portals=[Portail(from_world="mer", origin_point="exit_beach", target_world="world", teleport_point="enter_beach_exit")])

        self.teleport_player("player")
        self.teleport_pnj()

    def register_map(self, name, portals=[], pnj=[]):

        # charger la carte
        tmx_data = pytmx.util_pygame.load_pygame(
            f'../card/{name}.tmx')  # on specifie le fichier de la carte pour le stocker
        map_data = pyscroll.data.TiledMapData(tmx_data)  # recuperation de la carte
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data,
                                                           self.screen.get_size())  # met tout les calques sur la fenetre defini

        ## definition des collision
        walls = []  ## liste vide

        ## pour tous les objet de la carte
        for obj in tmx_data.objects:
            ##si objet a pour nom collision
            if obj.type == 'collision':
                walls.append(
                    pygame.Rect(obj.x, obj.y, obj.width, obj.height))  ## on apprend a la liste l'objet

            # dessiner groupe de calque
            group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=5)  # regroupe tous les calques
            group.add(self.player)

            for pnjs in pnj:
                group.add(pnjs)

            self.maps[name] = Map(name, walls, group, tmx_data, portals, pnj)

    def teleport_player(self, name):
        point = self.get_object(name)
        self.player.position[0] = point.x
        self.player.position[1] = point.y
        self.player.save_location()

    def check_collisions(self):

        for portals in self.get_map().portals:
            if portals.from_world == self.current_map:
                point = self.get_object(portals.origin_point)
                rect = pygame.Rect(point.x, point.y, point.width, point.height)

                if self.player.feet.colliderect(rect):
                    copy_portal = portals
                    self.current_map = portals.target_world
                    self.teleport_player(copy_portal.teleport_point)

        for sprite in self.get_group().sprites():

            if type(sprite) is Pnj:
                if sprite.feet.colliderect(self.player.rect):
                    sprite.speed = 0
                else:
                    sprite.speed = 0.1

            if sprite.feet.collidelist(self.get_walls()) > -1:
                sprite.move_back()

    def get_map(self):
        return self.maps[self.current_map]

    def get_group(self):
        return self.get_map().group

    def get_walls(self):
        return self.get_map().walls

    def get_object(self, name): return self.get_map().tmx_data.get_object_by_name(name)

    def teleport_pnj(self):
        for map in self.maps:
            map_data = self.maps[map]
            pnj = map_data.pnj

            for pnjs in pnj:
                pnjs.load_point(map_data.tmx_data)
                pnjs.teleport_spawn()

    def draw(self):
        self.get_group().draw(self.screen)
        self.get_group().center(self.player.rect.center)

    def update(self):
        self.get_group().update()
        self.check_collisions()

        for pnjs in self.get_map().pnj:
            pnjs.move_pnj()
