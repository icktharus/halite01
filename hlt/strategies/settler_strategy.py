from .base_strategy import BaseStrategy

class SettlerStrategy(BaseStrategy):
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
