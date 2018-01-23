import hlt
import numpy as np

class Navigator:

    # Public: Initialize the navigator.  This is intended to be used
    # for the whole game, so don't be creatin' them left and right.
    # Use #refresh_map(game_map) at the beginning of each turn.
    def __init__(self, ship_radius=hlt.constants.SHIP_RADIUS):
        self.game_map = None
        self.ship_radius = ship_radius

        # list of ship id's, corresponding to each row in ships_xy.
        self.ship_ids = []

        # ships_xy is a matrix of [ [x1,y2], [x2,y2], ...]  for each
        # ship.
        self.ships_xy = []

        # planets_xy is a matrix of [ [x1,y2], [x2,y2], ...] for each
        # planet.  planets_xy_trans is the transpose.
        self.planets_xy = []
        self.planets_xy_trans = [[], []]
        self.planet_radii = []

        # targets_xy is a matric of [ [x1,y2], [x2,y2], ...] for each
        # target.  targets_xy_trans is the transpose.
        self.targets_xy = []
        self.targets_xy_trans = [[], []]

        # Other caches
        self._target_diffs = None
        self._target_angles = None

        self.init_cache_variables()
        return

    # Private: Initialize all variables at the beginning of each turn.
    def init_cache_variables(self):
        self._ships_mat = None

        self._planets_mat = None
        self._planets_mat_trans = None

        self._targets_mat = None
        self._targets_mat_trans = None

        return

    # Public: Reread the game_map (mostly to read in all the planets).
    #
    # game_map - hlt.game_map.GameMap
    #
    # Returns nothing.
    def refresh_map(self, game_map):
        self.init_cache_variables()
        self.game_map = game_map
        for planet in game_map.all_planets():
            self.planets_xy.append([planet.x, planet.y])
            self.planets_xy_trans[0].append(planet.x)
            self.planets_xy_trans[1].append(planet.y)
            self.planet_radii.append(planet.radius + hlt.constants.SHIP_RADIUS)
        return

    # Public: Tell the navigator to direct the following ships towards
    # the target.
    #
    # ships - List of hlt.entity.Ship objects
    # target - Their target.
    #
    # Returns nothing.
    def direct_ships_to(self, ships, target):
        target_xy = [ target.x, target.y ]

        for ship in ships:
            self.ships_xy.append([ ship.x, ship.y ])
            self.targets_xy.append(target_xy[:])
            self.targets_xy_trans[0].append(target.x)
            self.targets_xy_trans[1].append(target.y)

        return

    # Public: Calculate what each ship should do.
    #
    # Returns list of [ship_id, command, vel_x, vel_y]
    def navigate(self):
        # FIXME: Implement.
        return []

    # Private: Return a numpy array of ships_xy
    #
    # Returns numpy ndarray
    def ships_mat(self):
        if self._ships_mat is None:
            self._ships_mat = np.array(self.ships_xy)
        return self._ships_mat

    # Private: Return a numpy array of planets_xy
    #
    # Returns numpy.ndarray
    def planets_mat(self):
        if self._planets_mat is None:
            self._planets_mat = np.array(self.planets_xy)
        return self._planets_mat

    # Private: Return a numpy array of planets_xy_trans
    #
    # Returns numpy.ndarray
    def planets_mat_trans(self):
        if self._planets_mat_trans is None:
            self._planets_mat_trans = np.array(self.planets_xy_trans)
        return self._planets_mat_trans

    # Private: Return a numpy array of target_xy
    #
    # Returns numpy ndarray
    def targets_mat(self):
        if self._targets_mat is None:
            self._targets_mat = np.array(self.targets_xy)
        return self._targets_mat

    # Private: Return a numpy array of target_xy_trans
    #
    # Returns numpy ndarray
    def targets_mat_trans(self):
        if self._targets_mat_trans is None:
            self._targets_mat_trans = np.array(self.targets_xy_trans)
        return self._targets_mat_trans
    
    # Public: For each ship, returns the angle to the target.
    #
    # Returns ndarray of angles for each ship.
    def target_angles(self):
        diff = self.targets_mat() - self.ships_mat()
        tan_theta = diff[:,1] / diff[:,0]
        return np.arctan(tan_theta)

    # Public: For each ship, returns the distance to the target.
    #
    # Returns ndarray of distances for each ship.
    def target_dist(self):
        return np.linalg.norm(self.targets_mat() - self.ships_mat(), axis=1)

    # Public: For each ship, returns a list of angles to each planet.
    #
    # Returns 2 ndarray of shape (len(ships), len(planets)): one of
    # angles between ships to the respective planets, the other of the
    # anglular width of the planet w/respect to the ship.
    def planet_angles(self):
        ship_ones = np.ones((self.ships_mat().shape[0], 1))
        planet_ones = np.ones((self.planets_mat().shape[0], 1))
        planet_angles_ary = []

        planet_radii = np.transpose( self.planet_radii ) * ship_ones
        ship_width_angle_diff = np.arctan(planet_radii / self.planet_dist())

        for ship_loc in self.ships_mat():
            diffs = self.planets_mat() - (ship_loc * planet_ones)
            tan_theta = diffs[:,1] / diffs[:,0]
            ship_angles = np.arctan(tan_theta)
            planet_angles_ary.append( np.transpose(ship_angles) )
        return np.array(planet_angles_ary), ship_width_angle_diff

    # Public: For each ship, returns a list of distances to each
    # planet.
    #
    # Returns ndarray of shape (len(ships), len(planets))
    def planet_dist(self):
        ones = np.ones((self.planets_mat().shape[0], 1))
        planet_dist_ary  = []
        for ship_loc in self.ships_mat():
            ship_distances = np.linalg.norm(self.planets_mat() - (ship_loc * ones), axis=1)
            planet_dist_ary.append( np.transpose(ship_distances) )
        return np.array(planet_dist_ary)

    # Public: Finds a list of planets in between the ships and their
    # targets.
    #
    # Returns ndarray of [angle, dist] pairs for the first planet in
    # the way.  pair is [0,0] if no planets in the way.
    def intersecting_planets(self):
        # FIXME: Implement.
        return
