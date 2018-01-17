import hlt

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

class ShipUtils:
    @staticmethod
    def follow(ships, leader, game_map):
        command_queue = []

        next_x = leader.x + leader.vel_x
        next_y = leader.y + leader.vel_y
        next_position = hlt.entity.Position(next_x, next_y)

        for ship in ships:
            # Only move if we're far enough to move.
            if ship.calculate_distance_between(next_position) > leader.radius:
                nav = ship.navigate(next_position, game_map,
                                    speed = int(leader.velocity()),
                                    ignore_ships=False)

                if nav:
                    command_queue.append(nav)

        return command_queue
