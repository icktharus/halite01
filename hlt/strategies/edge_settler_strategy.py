from .base_strategy import BaseStrategy
import hlt
import logging
import math
import numpy
from .strategy_utils import *

class EdgeSettlerStrategy(BaseStrategy):

    def __init__(self, game):
        game_map = game.map

        self.me = game_map.get_me()

        map_width = game_map.width
        map_height = game_map.height

        # An edge planet is any planet whose center is within 25% of
        # the min of width and height.
        edge_dist = 0.25 * min(map_width, map_height)

        edge_planets = {}
        central_planets = {}
        for planet in game_map.all_planets():
            if ((planet.x < edge_dist or planet.x > (map_width-edge_dist)) or
                (planet.y < edge_dist or planet.y > (map_height-edge_dist))):

                edge_planets[planet.id] = True
            else:
                central_planets[planet.id] = True

        self.map_width = map_width
        self.map_height = map_height
        self.edge_planets = edge_planets
        self.central_planets = central_planets

        self.planet_task_groups = {}
        self.docked_ships = {}

        logging.info("* %d edge planets, %d central planets" % (len(edge_planets), len(central_planets)))

        return

    def average_distance(self, ships, target):
        distances = []
        for ship in ships:
            distance = ship.calculate_distance_between(target)
            distances.append(distance)
        return numpy.mean(distances)

    def next_planet(self, game_map, ships):
        edge_planets = []
        central_planets = []

        for planet in game_map.all_planets():
            if planet.id in self.edge_planets:
                edge_planets.append(planet)
            else:
                central_planets.append(planet)

        for planet_group in [ edge_planets, central_planets ]:
            closest_planet = None
            closest_dist = max(self.map_width, self.map_height)
            for planet in planet_group:
                if planet.owner != None and planet.owner.id == self.me.id:
                    continue
                avg_dist = self.average_distance(ships, planet)
                if avg_dist < closest_dist:
                    closest_planet = planet
                    closest_dist = avg_dist
            if closest_planet != None:
                return closest_planet
        return None

    def create_task_group(self, game_map, ships):
        group_ships = []
        while len(ships) > 0:
            group_ships.append(ships.pop())

        if len(group_ships) < 3:
            return None

        planet = self.next_planet(game_map, group_ships)

        task_group = None
        if planet.id in self.planet_task_groups:
            task_group_id = self.planet_task_groups[planet.id]
            task_group = hlt.task_group.TaskGroup.task_groups[task_group_id]

            for ship in group_ships:
                task_group.add_ship(ship)

            logging.info("* using existing TaskGroup(%d): %d ships, target: %d" % (task_group_id, len(task_group.ships), (0 if planet == None else planet.id)))

        else:
            task_group = hlt.task_group.TaskGroup(group_ships)
            self.planet_task_groups[planet.id] = task_group.id

            logging.info("* creating task group %d: %d ships, target: %d" % (task_group.id, len(group_ships), (0 if planet == None else planet.id)))

        if planet != None:
            task_group.target(planet)

        return task_group

    def get_commands(self, game_map, task_group):
        command_queue = []

        if len(task_group.targets) == 0:
            return command_queue

        planet = task_group.targets[0]

        leader = task_group.leader()

        if planet.owner != None and planet.owner != game_map.get_me():
            closest = None
            closest_dist = -1.0
            for enemy in planet.all_docked_ships():
                dist = leader.calculate_distance_between(enemy)
                if closest == None or dist < closest_dist:
                    closest = enemy
                    closest_dist = dist

            point = leader.closest_point_to(closest)
            for ship in task_group.available_ships():
                nav = ship.navigate(
                    point, game_map, speed=int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if nav:
                    command_queue.append(nav)

        else:
            point = leader.closest_point_to(planet)
            for ship in ships:
                if ship.can_dock(planet):
                    command_queue.append(ship.dock(planet))
                    self.docked_ships[ ship.id ] = True
                else:
                    navigate = ship.navigate(
                        point, game_map, speed=int(hlt.constants.MAX_SPEED),
                        ignore_ships=False)
                    if navigate:
                        command_queue.append(navigate)

        return command_queue

    def is_task_group_done(self, task_group):
        if len(task_group.targets) == 0:
            return True
        planet = task_group.targets[0]
        return True if planet.is_owned() else False

    def can_task_group_continue(self, task_group, game_map):
        if not super().can_task_group_continue(task_group, game_map):
            return False
        planet = task_group.targets[0]
        return False if planet.health <= 0 else True

    def is_outdated(self, game_map):
        for planet in game_map.all_planets():
            if not planet.is_owned():
                return False
        return True

