import FreeSimpleGUI as sg
from player import Player
from game import Game
from gui import GUI

HEADLESS = True

if __name__ == "__main__":
    player = Player(
        health_current=50
    )
    game = Game(player)

    if not HEADLESS:
        gui = GUI(game)
        gui.run()

    else:
        print(game.player)
        print(game.get_current_location().story)
        print('\n')

        print(game.player)
        print(game.validate_move("north"))
        print('\n')

        print(game.player)
        print(game.validate_move("north"))
        print('\n')

        print(game.player)
        print(game.validate_move("south"))
        print('\n')

        print(game.player)
        print(game.validate_move("south"))
        print('\n')

        print(game.player)
        print(game.validate_move("south"))
        print('\n')
