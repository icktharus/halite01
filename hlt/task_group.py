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
    task_groups = []

    # Public: Creates a new TaskGroup.
    #
    # ships - list of Ship objects (defaults to [])
    #
    # Returns new TaskGroup
    def __init__(self, ships=[]):
        max_id     += 1
        self.id    = max_id

        self.ships = []
        for ship in ships:
            self.add_ship(ship)

        self.targets = []

        task_groups.append(self)
        return self

    # Public: Adds a ship to this task group.
    #
    # ship - Ship object
    #
    # Returns nothing
    def add_ship(self, ship):
        ship.set_task_group(self)
        self.ships.append(ship)
        return ship

    # Public: Destroys this task group, freeing up the ships for other
    # duties.
    #
    # Returns ships.
    def __del__(self):
        for ship in self.ships:
            ship.set_task_group(None)
        task_groups.remove(self)
        return self.ships

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

