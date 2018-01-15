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
