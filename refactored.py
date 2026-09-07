from game.player import Player
from game.game import Game
from game.command_parser import CommandParser
from gui import GUI

HEADLESS = True

if __name__ == "__main__":
    player = Player(
        health_current=50
    )
    game = Game(player)
    parser = CommandParser(game)

    if not HEADLESS:
        gui = GUI(game)
        gui.run()

    else:
        test_commands = [
            "move north",
            "move north",
            "move north",   #blocked (locked door)
            "move south",
            "move south",
            "move south",
            "attack goblin",
            "equip sword",
            "use health potion",
            "move sideways",  #invalid direction
            "adfasdfasd",          #invalid word
        ]

        print(game.player)
        print(game.get_current_location().story)
        print('\n')

        for command in test_commands:
            print(game.player)
            print(f"> {command}")
            print(parser.execute(command))
            print('\n')