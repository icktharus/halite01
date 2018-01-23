import hlt
import math
import numpy as np
import unittest
from unittest.mock import Mock

class TestNavigator(unittest.TestCase):
    def setUp(self):
        self._player        = None
        self._ship          = None
        self._planet        = None
        self._target_planet = None
        self._subject       = None
        return

    def tearDown(self):
        return

    def game_map(self):
        game_map = Mock()
        game_map.all_planets = Mock(return_value=self.all_planets())
        return game_map

    def subject(self):
        if self._subject is None:
            self._subject = hlt.strategies.Navigator()
            self._subject.direct_ships_to([ self.ship() ], self.target_planet())
            self._subject.refresh_map(self.game_map())
        return self._subject

    def player(self):
        if self._player is None:
            player_id = 9
            self._player = hlt.game_map.Player(player_id)
        return self._player

    def planet(self):
        if self._planet is None:
            planet_id     = 60
            planet_x      = 160
            planet_y      = 220
            planet_health = 100
            planet_radius = 10
            docking_spots = 10
            current       = 0
            remaining     = 10
            owned         = False
            owner         = None
            docked_ships  = []
            self._planet = hlt.entity.Planet(planet_id,
                                             planet_x, planet_y,
                                             planet_health,
                                             planet_radius,
                                             docking_spots, current,
                                             remaining,
                                             owned, owner, docked_ships)
        return self._planet

    def target_planet(self):
        if self._target_planet is None:
            planet_id     = 60
            planet_x      = 310
            planet_y      = 410
            planet_health = 100
            planet_radius = 5
            docking_spots = 10
            current       = 0
            remaining     = 10
            owned         = False
            owner         = None
            docked_ships  = []
            self._target_planet = hlt.entity.Planet(planet_id,
                                                    planet_x, planet_y,
                                                    planet_health,
                                                    planet_radius,
                                                    docking_spots, current,
                                                    remaining,
                                                    owned, owner, docked_ships)
        return self._target_planet

    def all_planets(self):
        return [ self.planet(), self.target_planet() ]

    def ship(self):
        if self._ship is None:
            ship_id     = 11
            ship_x      = 10
            ship_y      = 10
            ship_health = hlt.constants.MAX_SHIP_HEALTH
            ship_vel_x  = 0
            ship_vel_y  = 0
            ship_status = hlt.entity.Ship.DockingStatus.UNDOCKED
            planet      = None
            progress    = 0
            cooldown    = 0
            self._ship = hlt.entity.Ship(self.player().id,
                                         ship_id, ship_x, ship_y,
                                         ship_health, ship_vel_x, ship_vel_y,
                                         ship_status, planet, progress,
                                         cooldown)
            players_dict = { self.player().id : self.player() }
            planets_dict = { self.target_planet().id : self.target_planet(),
                             self.planet().id : self.planet() }
            self._ship._link(players_dict, planets_dict)
        return self._ship
            
    def test_ships_mat(self):
        mat = self.subject().ships_mat()
        self.assertTrue(np.array_equal(mat,
                                       np.array([[ self.ship().x, self.ship().y ]])))
        pass

    def test_planets_mat(self):
        mat = self.subject().planets_mat()
        expected_mat = np.array([
                [ self.planet().x, self.planet().y ],
                [ self.target_planet().x, self.target_planet().y ]
                ])
        self.assertTrue(np.array_equal(mat, expected_mat))
                                       
        pass

    def test_planets_mat_trans(self):
        mat = self.subject().planets_mat_trans()
        expected_mat = np.transpose(np.array([
                    [ self.planet().x, self.planet().y ],
                    [ self.target_planet().x, self.target_planet().y ]
                    ]))
        self.assertTrue(np.array_equal(mat, expected_mat))
        pass

    def test_targets_mat(self):
        mat = self.subject().targets_mat()
        self.assertTrue(np.array_equal(mat,
                                       np.array([[ self.target_planet().x, self.target_planet().y ]])))
        pass

    def test_targets_mat_trans(self):
        mat = self.subject().targets_mat_trans()
        self.assertTrue(np.array_equal(mat,
                                       np.transpose(np.array([[ self.target_planet().x, self.target_planet().y ]]))))
        pass

    def test_target_angles(self):
        target_angles = self.subject().target_angles()
        expected_angles = np.array([0.927295218001612])
        self.assertTrue(np.allclose(target_angles, expected_angles))
        pass

    def test_target_dist(self):
        target_dist = self.subject().target_dist()
        expected_dist = np.array([500])
        self.assertTrue(np.array_equal(target_dist, expected_dist))
        pass

    def test_planet_angles(self):
        planet_angles, planet_widths = self.subject().planet_angles()

        expected_angles = np.array([[ 0.950546840812075,
                                      0.927295218001612 ]])
        expected_angle_widths = np.array([[ 0.040664244853507,
                                            0.010999556365541 ]])

        self.assertTrue(np.allclose(planet_angles, expected_angles))
        self.assertTrue(np.allclose(planet_widths, expected_angle_widths))
        pass

    def test_planet_dist(self):
        planet_dists = self.subject().planet_dist()
        expected_dists = np.array([[258.069758011278803, 500.0]])
        self.assertTrue(np.allclose(planet_dists, expected_dists))
        pass

