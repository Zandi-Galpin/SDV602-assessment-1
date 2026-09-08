from game.player import Player
from game.game import Game
from game.command_parser import CommandParser
from gui import GUI
from game.item import Item

from game.enemy import Enemy


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
        game.inventory.add_item(Item('sword', damage=5))
        game.inventory.add_item(Item('health potion', heal=25))
        game.inventory.add_gold(50)

        # Test-only enemy placed at spawn — real placement happens later
        test_goblin = Enemy(
            name='goblin', health=12, damage=4,
            drops=[Item('gold', amount=15)]
        )
        game.get_current_location().enemies.append(test_goblin)

        test_commands = [
            "equip sword",
            "attack goblin",     #starts battle, first hit
            "move north",        #blocked, in battle
            "equip sword",       #blocked, in battle
            "use health potion", #allowed in battle, doesn't end turn
            "attack goblin",     #continue fight
            "attack goblin",     #should defeat it 
            "move north",        #should work again after battle
        ]

        print(game.player)
        print(game.get_current_location().story)
        print('\n')

        for command in test_commands:
            print(game.player)
            print(f"> {command}")
            print(parser.execute(command))
            print('\n')