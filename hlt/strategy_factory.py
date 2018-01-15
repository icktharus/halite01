from . import constants
import logging
import math
import random
import hlt.strategies
from hlt.strategies.strategy_utils import ScoredPlanet

class StrategyFactory:
    """
    Get new Strategies
    """

    STRATEGIES = [
        [ hlt.strategies.SettlerStrategy, 100 ]
        ]

    def __init__(self):
        return

    def get_strategy(self, game):
        rand_num = random.randint(0,100)
        current = 0
        last_strategy = None
        for strategy_entry in StrategyFactory.STRATEGIES:
            strategy_class, percent = strategy_entry
            if current > rand_num:
                return last_strategy(game)
            current += percent
            last_strategy = strategy_class
        # If we got here, there's only one entry.
        return last_strategy(game)

