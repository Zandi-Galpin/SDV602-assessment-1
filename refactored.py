import sys
from game.player import Player
from game.game import Game
from game.command_parser import CommandParser
from game.test_runner import run_headless_tests, print_results
from gui import GUI

if __name__ == "__main__":
    if "--headless" in sys.argv:
        results = run_headless_tests()
        print_results(results)
        sys.exit(0 if not results['failed'] and not results['errors'] else 1)

    player = Player(health_current=100)
    game = Game(player)
    gui = GUI(game)
    gui.run()