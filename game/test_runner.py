"""Headless testingggg. Runs a set of test cases against new
game instances and returns a results object.
"""

from game.player import Player
from game.game import Game
from game.command_parser import CommandParser
from game.item import Item
from game.enemy import Enemy


def new_game():
    """Fresh game + CommandParser for one test case."""
    player = Player()
    game = Game(player)
    parser = CommandParser(game)
    return game, parser


def test_movement_and_walls():
    game, parser = new_game()
    #spawn is row3column1; west is wall
    result = parser.execute("move west")
    assert "can not go that way" in result, f"expected wall message, got: {result}"

    result = parser.execute("move north")
    assert game.current_location == "row4column1", \
        f"expected row4column1, got {game.current_location}"


def test_locked_door_blocks_until_key_used():
    game, parser = new_game()
    game.current_location = "row4column1"

    result = parser.execute("move north")
    assert "locked" in result.lower(), f"expected locked message, got: {result}"
    assert game.current_location == "row4column1", "should not have been able to go through (gulp)"


def test_pirate_trade_needs_gold():
    game, parser = new_game()
    game.current_location = "row1column2"

    result = parser.execute("use gold")
    assert "50 GOLD" in result, f"expected not enough gold message, got: {result}"
    assert not game.inventory.has_item("fishing rod")

    game.inventory.add_gold(50)
    result = parser.execute("use gold")
    assert game.inventory.has_item("fishing rod"), f"expected fishing rod after trade, got: {result}"
    assert game.inventory.gold == 0


def test_fishing_rod_gives_key():
    game, parser = new_game()
    game.inventory.add_item(Item("fishing rod"))
    game.current_location = "row4column4"

    result = parser.execute("use fishing rod")
    assert game.inventory.has_item("key"), f"expected key after fishing, got: {result}"


def test_key_unlocks_door():
    game, parser = new_game()
    game.inventory.add_item(Item("key"))
    game.current_location = "row4column1"

    parser.execute("use key")
    assert not game.locations["row4column1"].locked, "door should be unlocked after usimg key"

    result = parser.execute("move north")
    assert game.current_location == "row5column1", f"expected pass through door, got: {result}"


def test_equip_unequip_and_swap():
    game, parser = new_game()
    game.inventory.add_item(Item("sword", damage=5))
    game.inventory.add_item(Item("shield", block=4))

    parser.execute("equip sword")
    assert game.player.damage == 10, f"expected damage 10 after equip sword, got {game.player.damage}"

    parser.execute("equip shield")
    assert game.player.damage == 5, "equipping shield should unequip sword"
    assert game.player.block == 6, f"expected block 6 after equipping shield, got {game.player.block}"

    parser.execute("equip shield")
    assert game.player.block == 2, "unequipping shield should remove bonus"


def test_battle_stops_move_and_equip():
    game, parser = new_game()
    game.get_current_location().enemies.append(
        Enemy(name="test dummy", health=5000, damage=0)
    )
    parser.execute("attack test dummy")

    result = parser.execute("move north")
    assert "battle" in result.lower(), f"expected move blocked in battle, got: {result}"

    result = parser.execute("equip sword")
    assert "battle" in result.lower(), f"expected equip blocked in battle, got: {result}"


def test_defeat_stops_commands_until_restart():
    game, parser = new_game()
    game.player.health_current = 0
    game.status.player.health_current = 0

    result = parser.execute("move north")
    assert "defeated" in result.lower(), f"expected game over message, got: {result}"

    result = parser.execute("restart")
    assert game.player.health_current == game.player.health_max, "restart should reset health"
    assert not game.is_game_over(), "game should not be over after restart"


def test_ambush_triggers_when_entering():
    game, parser = new_game()
    game.current_location = "row5column1"

    result = parser.execute("move north")
    assert game.monster_fight.in_battle(), f"expected battle to start from the ambush, got: {result}"
    assert "ambush" in result.lower()


def test_win_ends_game():
    game, parser = new_game()
    game.current_location = "row6column1"
    game.monster_fight.end_battle()
    game.get_current_location().enemies.clear()  #skip the fight for this test

    result = parser.execute("move north")
    assert game.won, f"expected winning, got: {result}"

    result = parser.execute("move south")
    assert "won" in result.lower()


def test_help_works_always():
    game, parser = new_game()
    game.player.health_current = 0

    result = parser.execute("help")
    assert "Available commands" in result, "help should work even if game is over or lost"


def test_invalid_input_doesnt_crash():
    game, parser = new_game()
    assert parser.execute("asdfasdfd") is not None
    assert parser.execute("move safsdfasdf") is not None
    assert parser.execute("attack") is not None
    assert parser.execute("equip") is not None
    assert parser.execute("use") is not None


ALL_TESTS = [
    test_movement_and_walls,
    test_locked_door_blocks_until_key_used,
    test_pirate_trade_needs_gold,
    test_fishing_rod_gives_key,
    test_key_unlocks_door,
    test_equip_unequip_and_swap,
    test_battle_stops_move_and_equip,
    test_defeat_stops_commands_until_restart,
    test_ambush_triggers_when_entering,
    test_win_ends_game,
    test_help_works_always,
    test_invalid_input_doesnt_crash,
]


def run_headless_tests():
    """Run every test case, catching errors on each test so one
    broken one doesnt stop the rest running.

    Returns a results object
    """
    results = {'passed': [], 'failed': [], 'errors': []}

    for test in ALL_TESTS:
        name = test.__name__
        try:
            test()
            results['passed'].append(name)
        except AssertionError as e:
            results['failed'].append((name, str(e)))
        except Exception as e:
            results['errors'].append((name, repr(e)))

    return results


def print_results(results):
    total = len(results['passed']) + len(results['failed']) + len(results['errors'])
    print(f"Ran {total} tests: {len(results['passed'])} passed, "
          f"{len(results['failed'])} failed, {len(results['errors'])} had errors.\n")

    for name, message in results['failed']:
        print(f"FAILED  {name}: {message}")
    for name, error in results['errors']:
        print(f"ERROR   {name}: {error}")

    if not results['failed'] and not results['errors']:
        print("All tests passed.")