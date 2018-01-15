import hlt
import math
import unittest

class TaskGroupTest(unittest.TestCase):

    def setUp(self):
        self._player = None
        self._ship = None
        self._subject = None
        return

    def player(self):
        if self._player == None:
            player_id = 9
            self._player = hlt.game_map.Player(player_id)
        return self._player

    def ship(self):
        if self._ship == None:
            ship_id     = 11
            ship_x      = 50
            ship_y      = 100
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
        return self._ship

    def subject(self):
        if self._subject == None:
            self._subject = hlt.task_group.TaskGroup()
        return self._subject

    def test_add_ship(self):
        self.assertEqual(hlt.entity.Ship.unassigned_ships, [self.ship()])

        self.subject().add_ship(self.ship())
        self.assertEqual(self.ship().id, self.subject().ships[0].id)
        self.assertEqual(self.subject().id, self.ship().task_group().id)
        self.assertEqual(hlt.entity.Ship.unassigned_ships, [])
        pass

if __name__ == '__main__':
    unittest.main()
