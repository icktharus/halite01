import hlt
import logging
import math

game = hlt.Game("Alexy")
logging.info("Starting my Alexy bot!")

class ScoredPlanet:
    def __init__(self, planet, my_ships, other_ships, max_dist):
        self.planet = planet
        self.my_ships = my_ships
        self.other_ships = other_ships
        self.max_dist = max_dist

    def score(self, ship):
        return self.size_score()

    def size_score(self):
        return (self.planet.num_docking_spots -
                len(self.planet.all_docked_ships()))

    def distance_score(self, ship):
        dist = self.planet.calculate_distance_between(ship)
        return (max_dist - dist)/max_dist

max_dist = 0
while True:
    game_map = game.update_map()
    max_dist = math.sqrt(game_map.width ** 2 + game_map.height ** 2)

    command_queue = []
    me = game_map.get_me()
    my_ships = me.all_ships()
    other_ships = []
    for player in game_map.all_players():
        if player == me:
            continue
        other_ships.append(player.all_ships())

    planets = [ ScoredPlanet(planet, my_ships, other_ships, max_dist) for planet in game_map.all_planets() ]

    for ship in my_ships:
        if ship.docking_status != ship.DockingStatus.UNDOCKED:
            continue

        for planet in sorted(planets, key=lambda planet: planet.score(ship)):
            if planet.planet.is_owned():
                continue

            if ship.can_dock(planet.planet):
                command_queue.append(ship.dock(planet.planet))
            else:
                navigate_command = ship.navigate(
                    ship.closest_point_to(planet.planet),
                    game_map,
                    speed=int(hlt.constants.MAX_SPEED/2),
                    ignore_ships=True)
                if navigate_command:
                    command_queue.append(navigate_command)
            break

    game.send_command_queue(command_queue)
    # TURN END
# GAME END
