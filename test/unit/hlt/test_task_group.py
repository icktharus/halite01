import hlt
import math
import unittest

class TestTaskGroup(unittest.TestCase):

    def setUp(self):
        self._player  = None
        self._ship    = None
        self._planet  = None
        self._subject = None
        return

    def tearDown(self):
        hlt.task_group.TaskGroup.delete_all()
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

            players_dict = { self.player().id : self.player() }
            planets_dict = { self.planet().id : self.planet() }
            self._ship._link(players_dict, planets_dict)
        return self._ship

    def planet(self):
        if self._planet == None:
            planet_id     = 60
            planet_x      = 100
            planet_y      = 100
            planet_health = 100
            planet_radius = 5
            docking_spots = 10
            current       = 0
            remaining     = 10
            owned         = False
            owner         = None
            docked_ships  = []
            self._planet = hlt.entity.Planet(planet_id, planet_x, planet_y,
                                             planet_health, planet_radius,
                                             docking_spots, current, remaining,
                                             owned, owner, docked_ships)
        return self._planet

    def subject(self):
        if self._subject == None:
            self._subject = hlt.task_group.TaskGroup()
        return self._subject

    def test_add_ship(self):
        self.ship()
        self.assertEqual(hlt.entity.Ship.unassigned_ships[self.player().id],
                         { self.ship().id : self.ship() })

        self.subject().add_ship(self.ship())
        self.assertEqual(self.ship(), self.subject().ships[self.ship().id])
        self.assertEqual(self.subject().id, self.ship().task_group().id)
        self.assertEqual(hlt.entity.Ship.unassigned_ships[self.player().id], {})
        pass

    def test_delete(self):
        task_group = self.subject()
        task_group.add_ship(self.ship())

        hlt.task_group.TaskGroup.delete(task_group)

        self.assertEqual(hlt.entity.Ship.unassigned_ships[self.player().id],
                         { self.ship().id : self.ship() })
        self.assertEqual(hlt.task_group.TaskGroup.task_groups, {})
        pass

    def test_delete_all(self):
        task_group = self.subject()

        self.assertEqual(hlt.task_group.TaskGroup.task_groups,
                         { task_group.id : task_group })
        hlt.task_group.TaskGroup.delete_all()
        self.assertEqual(hlt.task_group.TaskGroup.task_groups, {})
        pass

    def test_target(self):
        task_group = self.subject()
        task_group.target(self.planet())

        self.assertEqual(task_group.targets, [self.planet()])
        task_group.clear_targets()
        self.assertEqual(task_group.targets, [])
        pass

if __name__ == '__main__':
    unittest.main()
