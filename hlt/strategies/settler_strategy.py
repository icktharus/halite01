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

    def is_task_group_done(self, task_group):
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

