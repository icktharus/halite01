from abc import ABCMeta, abstractmethod
import logging

class BaseStrategy:
    __metaclass__ = ABCMeta

    def __init__(self, game):
        return

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
        return []

    # Public: Ask this Strategy if we need to get a new one.
    #
    # game_map - current game_map
    #
    # Returns true if this strategy is outdated and another needs to
    # be used.
    @abstractmethod
    def is_outdated(self, game_map):
        return False

    # Public: Ask if the specified TaskGroup has completed its task.
    #
    # task_group - TaskGroup object
    #
    # Returns true if this task_group has completed its task.
    @abstractmethod
    def is_task_group_done(self, task_group):
        return False

    # Public: Ask if the specified TaskGroup can complete its task.
    #
    # task_group - TaskGroup object
    # game_map
    #
    # Returns true if this task_group's task is completeable.
    @abstractmethod
    def can_task_group_continue(self, task_group, game_map):
        if len(task_group.ships) > 0:
            return True
        else:
            return False

