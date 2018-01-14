import hlt
import logging
import math

game = hlt.Game('Alexy2')
logging.info("Starting my Alexy bot!")

strategy_factory = hlt.StrategyFactory()

strategy = strategy_factory.get_strategy(game)
strategy.initialize(game)

while True:
    game_map = game.update_map()
    # 1. Delete TaskGroups with completed/impossible goals.
    # 2. Get all unassigned ships (including newly created ships), and
    #    assign to new TaskGroups (with new goals).
    unassigned_ships = Ship.unassigned_ships
    while len(unassigned_ships) > 0:
        strategy.create_task_group(game_map, unassigned_ships)

    # 3. Get commands for all TaskGroup ships.
    command_queue = []
    for task_group in TaskGroup.task_groups:
        command_queue += strategy.get_commands(task_group)

    # 4. Send all commands to the game.
    game.send_command_queue(command_queue)

    # TURN END
# GAME END
