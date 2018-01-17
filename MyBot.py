import hlt
import logging
import math

game = hlt.Game('Alexy:EdgeSettler')
logging.info("Starting the Alexy:EdgeSettler bot")

strategy_factory = hlt.StrategyFactory()
me = game.map.get_me()

strategy = strategy_factory.get_strategy(game)

while True:
    game_map = game.update_map()

    # 0. Delete all ships not in the game anymore.
    living_ships = {}
    for ship in game_map.get_me().all_ships():
        living_ships[ship.id] = ship
    for ship_id, task_group in dict(hlt.entity.Ship.ship_task_groups).items():
        if ship_id in living_ships:
            # Update the ship in the task_group.
            task_group.ships[ship_id] = living_ships[ship_id]
        else:
            del hlt.entity.Ship.ship_task_groups[ship_id]
            if ship_id in task_group.ships:
                logging.info("- DELETING Ship(%d) FROM TaskGroup(%d)" % (ship_id, task_group.id))
                del task_group.ships[ship_id]

    # 1. Delete TaskGroups with completed/impossible goals.
    for task_group in list(hlt.task_group.TaskGroup.task_groups.values()):
        if strategy.is_task_group_done(task_group):
            hlt.task_group.TaskGroup.delete(task_group)
        elif not strategy.can_task_group_continue(task_group, game_map):
            hlt.task_group.TaskGroup.delete(task_group)

    # 2. Get all unassigned ships (including newly created ships), and
    #    assign to new TaskGroups (with new goals).
    my_unassigned_ships = []
    for ship in hlt.entity.Ship.unassigned_ships[me.id].values():
        my_unassigned_ships.append(ship)

    while len(my_unassigned_ships) > 0:
        strategy.create_task_group(game_map, my_unassigned_ships)

    # 3. Get commands for all TaskGroup ships.
    command_queue = []
    for task_group in list(hlt.task_group.TaskGroup.task_groups.values()):
        logging.info("***** RUNNING COMMANDS FOR TaskGroup(%d) *****" % task_group.id)
        command_queue += strategy.get_commands(game_map, task_group)

    # 4. Send all commands to the game.
    game.send_command_queue(command_queue)

    # TURN END
# GAME END
