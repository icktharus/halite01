from abc import ABCMeta
from . import constants
import logging
import math
import random

class ScoredPlanet:
    def __init__(self, planet, my_ships, other_ships, max_dist):
        self.planet = planet
        self.my_ships = my_ships
        self.other_ships = other_ships
        self.max_dist = max_dist

    def size_score(self):
        return (self.planet.num_docking_spots -
                len(self.planet.all_docked_ships()))

    def distance_score(self, ship):
        dist = self.planet.calculate_distance_between(ship)
        return (max_dist - dist)/max_dist

class StrategyFactory:
    """
    Get new Strategies
    """

    STRATEGIES = [
        [ SettlerStrategy, 10 ]
        ]

    def __init__(self):
        return

    def get_strategy(self, game):
        rand_num = random.randint(0,99)
        current = 0
        last_strategy = None
        for strategy_entry in STRATEGIES:
            strategy_class, percent = strategy_entry
            if rand_num > current:
                return last_strategy(game)
            current += percent
            last_strategy = strategy_class
        # If we got here, there's only one entry.
        return last_strategy(game)


class Strategy:
    __metaclass__ = ABCMeta

    # Public: Takes the list of unassigned ships, and creates a task
    # group out of them.  Note: the ships list is modified.
    #
    # game_map - current game_map
    # ships - list of unassigned ships
    #
    # Returns (TaskGroup)task_group
    @abstractmethod
    def create_task_group(self, game_map, ships)

    # Public: Determines the best way to achieve the target.
    #
    # game_map - current game_map
    # task_group - TaskGroup
    #
    # Returns list of commands.
    @abstractmethod
    def get_commands(self, game_map, task_group)

    # Public: Ask this Strategy if we need to get a new one.
    #
    # game_map - current game_map
    #
    # Returns true or false.
    @abstractmethod
    def is_outdated(self, game_map)


class SettlerStrategy:
    def __init__(self):
        return

    def create_task_group(self, game_map, ships):
        ship = ships.pop()
        task_group = TaskGroup([ship])
        for planet in game_map.all_planets():
            if planet.is_owned():
                continue
            task_group.target(planet)
            break
        return task_group

    def get_commands(self, game_map, task_group):
        command_queue = []

        planet = task_group.targets[0]
        for ship in task_group.ships:
            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
            else:
                navigate = ship.navigate(
                    ship.closest_point_to(planet),
                    game_map,
                    speed = int(constants.MAX_SPEED/2),
                    ignore_ships=False)
                if navigate:
                    command_queue.append(navigate)
            break
        return command_queue

class StrategyX:
    """
    Here's the theory:

    For each turn, execute the following:
    * clear all TaskGroups whose targets are conquered (freeing Ships)
    * assign all unassigned Ships to new TaskGroups
    * for each TaskGroup without a target, assign a target
    * for each TaskGroup, move Ships towards the target
    """

    def __init__(self, game):
        self.board_width = game.map.width
        self.board_height = game.map.height
        self.max_dist = math.sqrt(game.map.width ** 2 + game.map.height ** 2)
        self.me = game.map.get_me()

    def sorted_planets(self, planets, my_ships, other_ships):
        scored = [ ScoredPlanet(planet, my_ships, other_ships, self.max_dist) for planet in planets ]
        return sorted(scored, key=lambda planet: planet.size_score())

    def get_commands(self, game_map):
        commands = []

        my_ships = self.me.all_ships()
        other_ships = []
        for player in game_map.all_players():
            if player == self.me:
                continue
            other_ships.append(player.all_ships())

        scored_planets = self.sorted_planets(game_map.all_planets(), my_ships, other_ships)
        
        for ship in my_ships:
            if ship.docking_status != ship.DockingStatus.UNDOCKED:
                continue

            for scored_planet in scored_planets:
                planet = scored_planet.planet
                if planet.is_full():
                    continue

                planet_is_mine = False
                if planet.is_owned() and planet.all_docked_ships()[0].owner == self.me.id:
                    planet_is_mine = True

                if False and planet.is_owned() and planet_is_mine == False:
                    # Attack!
                    logging.info("--> Attacking")
                    closest_ship = None
                    closest_dist = None
                    for enemy_ship in planet.all_docked_ships():
                        dist = ship.calculate_distance_between(enemy_ship)
                        if closest_dist == None or closest_dist > dist:
                            closest_dist = dist
                            closest_ship = enemy_ship
                    navigate_command = ship.navigate(
                        ship.closest_point_to(closest_ship),
                        game_map,
                        speed=int(constants.MAX_SPEED),
                        ignore_ships=False)
                    if navigate_command:
                        commands.append(navigate_command)
                elif ship.can_dock(planet):
                    logging.info("--> Docking")
                    commands.append(ship.dock(planet))
                else:
                    logging.info("--> Navigating to " +
                                 ship.closest_point_to(planet).str() +
                                 " w/speed " + str(constants.MAX_SPEED) +
                                 " (game_map: " +
                                 ("Good" if game_map == None else "None") +
                                 ")")
                    navigate_command = ship.navigate(
                        ship.closest_point_to(planet),
                        game_map,
                        speed=int(constants.MAX_SPEED),
                        ignore_ships=False)
                    if navigate_command:
                        logging.info("    ... just keep swimming...")
                        commands.append(navigate_command)
                break
        return commands
