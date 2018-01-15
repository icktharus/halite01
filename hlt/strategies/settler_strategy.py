from .base_strategy import BaseStrategy
import hlt
import logging

class SettlerStrategy(BaseStrategy):

    def create_task_group(self, game_map, ships):
        ship = ships.pop()

        logging.info("--> creating new task group with ship %d", ship.id)
        task_group = hlt.task_group.TaskGroup([ship])
        for planet in game_map.all_planets():
            if planet.is_owned():
                continue
            task_group.target(planet)
            break
        return task_group

    def get_commands(self, game_map, task_group):
        command_queue = []

        planet = task_group.targets[0]
        for ship in task_group.ships.values():
            if ship.can_dock(planet):
                command_queue.append(ship.dock(planet))
            else:
                point = ship.closest_point_to(planet)
                logging.info("* Ship(%d) navigating to Planet(%d): ship: %s, point: %s, planet: %s" % (ship.id, planet.id, str(ship), str(point), str(planet)))
                navigate = ship.navigate(
                    point,
                    game_map,
                    speed = int(hlt.constants.MAX_SPEED),
                    ignore_ships=False)
                if navigate:
                    command_queue.append(navigate)
        return command_queue

    def is_task_group_done(self, task_group):
        planet = task_group.targets[0]
        if planet.is_owned():
            logging.info("* TaskGroup(%d) is done because planet is owned." % task_group.id)
        return True if planet.is_owned() else False

    def can_task_group_continue(self, task_group, game_map):
        if not super().can_task_group_continue(task_group, game_map):
            logging.info("* TaskGroup(%d) can't continue because super.can_continue is false." % task_group.id)
            return False
        planet = task_group.targets[0]
        if planet.health <= 0:
            logging.info("* TaskGroup(%d) can't continue because planet is dead." % task_group.id)
        return False if planet.health <= 0 else True

    def is_outdated(self, game_map):
        for planet in game_map.all_planets():
            if not planet.is_owned():
                return False
        return True

