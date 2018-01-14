import hlt
import logging
import math

game = hlt.Game('Alexy2')
logging.info("Starting my Alexy bot!")

strategy = hlt.StrategyX(game)

while True:
    game_map = game.update_map()
    command_queue = strategy.get_commands(game_map)
    game.send_command_queue(command_queue)
    # TURN END
# GAME END
