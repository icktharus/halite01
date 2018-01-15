import hlt
import logging
import math

game = hlt.Game('Alexy2')
logging.info("Starting my Alexy bot!")

strategy_factory = hlt.StrategyFactory()
me = game.map.get_me()

strategy = strategy_factory.get_strategy(game)

while True:
    game_map = game.update_map()
    # 1. Delete TaskGroups with completed/impossible goals.
    for task_group in list(hlt.task_group.TaskGroup.task_groups.values()):
        if strategy.is_task_group_done(task_group):
            hlt.task_group.TaskGroup.delete(task_group)
        elif strategy.can_task_group_continue(task_group, game_map):
            hlt.task_group.TaskGroup.delete(task_group)

    # 2. Get all unassigned ships (including newly created ships), and
    #    assign to new TaskGroups (with new goals).
    my_unassigned_ships = []
    for ship in hlt.entity.Ship.unassigned_ships[me.id].values():
        my_unassigned_ships.append(ship)

    logging.info("* my ships: %d" % len(my_unassigned_ships))

    while len(my_unassigned_ships) > 0:
        strategy.create_task_group(game_map, my_unassigned_ships)

    # 3. Get commands for all TaskGroup ships.
    command_queue = []
    for task_group in list(hlt.task_group.TaskGroup.task_groups.values()):
        command_queue += strategy.get_commands(game_map, task_group)

    # 4. Send all commands to the game.
    game.send_command_queue(command_queue)

    # TURN END
# GAME END
