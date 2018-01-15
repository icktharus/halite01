from abc import ABCMeta, abstractmethod

class BaseStrategy:
    __metaclass__ = ABCMeta

    # Public: Takes the list of unassigned ships, and creates a task
    # group out of them.  Note: the ships list is modified.
    #
    # game_map - current game_map
    # ships - list of unassigned ships
    #
    # Returns (TaskGroup)task_group
    @abstractmethod
    def create_task_group(self, game_map, ships):
        return

    # Public: Determines the best way to achieve the target.
    #
    # game_map - current game_map
    # task_group - TaskGroup
    #
    # Returns list of commands.
    @abstractmethod
    def get_commands(self, game_map, task_group):
        return

    # Public: Ask this Strategy if we need to get a new one.
    #
    # game_map - current game_map
    #
    # Returns true or false.
    @abstractmethod
    def is_outdated(self, game_map):
        return
