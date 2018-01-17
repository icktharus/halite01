import hlt
import logging
import math

class TaskGroup:
    """
    TaskGroups are groups of ships which have the same task, whether
    that task is to dock with a planet, or protect a planet, or
    destroy enemy ships via some strategy.

    :ivar id: TaskGroup ID (int)
    :ivar ships: List of Ship objects assigned to this TaskGroup.
    :ivar targets: Targets (list of Entity objects)
    """

    max_id = 0
    task_groups = {}

    # Public: Creates a new TaskGroup.
    #
    # ships - list of Ship objects (defaults to [])
    #
    # Returns new TaskGroup
    def __init__(self, ships=[]):
        TaskGroup.max_id  += 1
        self.id = TaskGroup.max_id

        self.ships = {}
        for ship in ships:
            self.add_ship(ship)

        self.targets = []

        self.leader_id = None
        self._leader = None
        self._followers = []

        self._available_ships = None

        TaskGroup.task_groups[self.id] = self
        return

    # Private: Pick a leader and set followers.
    #
    # Returns nothing.
    def _set_up_leader(self):
        if self.leader_id != None:
            for ship in self.all_ships():
                if ship.id == self.leader_id:
                    self._leader = ship
                else:
                    self._followers.append(ship)
        else:
            sorted_ships = sorted(self.all_ships(), key=lambda s: s.id)
            self._leader = sorted_ships[0]
            self.leader_id = self._leader.id
            self._followers = sorted_ships[1:]
        return

    # Public: Return the task_group's lead ship.
    #
    # Returns lead ship.
    def leader(self):
        if self._leader == None:
            self._set_up_leader()
        return self._leader

    # Public: Return the task_group's followers.
    def followers(self):
        if self._leader == None:
            self._set_up_leader()
        return self._followers

    # Public: Return all ships.
    def all_ships(self):
        return self.ships.values()

    # Public: Return undocked ships.
    def available_ships(self):
        if self._available_ships == None:
            self._available_ships = {}
            for ship in self.all_ships():
                if ship.docking_status != hlt.entity.Ship.DockingStatus.DOCKED:
                    self._available_ships[ship.id] = ship
            return self._available_ships.values()
        elif len(self._available_ships) == 0:
            return []
        else:
            return self._available_ships.values()

    # public: Adds a ship to this task group.
    #
    # ship - Ship object
    #
    # Returns nothing
    def add_ship(self, ship):
        ship.set_task_group(self)
        self.ships[ship.id] = ship
        return ship

    # Public: Destroys this task group, freeing up the ships for other
    # duties.
    #
    # Returns ships.
    @classmethod
    def delete(cls, task_group):
        for ship in task_group.all_ships():
            ship.set_task_group(None)
        del TaskGroup.task_groups[task_group.id]
        return task_group.all_ships()

    # Public: Destroys all task groups.  Mostly for testing.
    #
    # Returns nothing.
    @classmethod
    def delete_all(cls):
        for task_group in list(TaskGroup.task_groups.values()):
            cls.delete(task_group)
        return

    # Public: Assigns a target for this task group.
    #
    # target - an Entity to target
    #
    # Returns target.
    def target(self, target_entity):
        self.targets = [ target_entity ]
        return target_entity

    # Public: Clears the targets, presumably because they've been
    # destroyed.
    #
    # Returns nothing.
    def clear_targets(self):
        self.targets = []
        return

