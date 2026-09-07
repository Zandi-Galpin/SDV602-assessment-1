from game.player import Player
from game.game import Game
from game.command_parser import CommandParser
from gui import GUI
from game.item import Item


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
        #add items the user would normally get from enemies
        game.inventory.add_item(Item('sword', damage=5))
        game.inventory.add_item(Item('health potion', heal=25))
        game.inventory.add_gold(50)

        test_commands = [
            "equip sword",
            "equip sword",          #unequip (toggled)
            "equip shield",         #not in inventory
            "attack goblin",     
            "use health potion",
            "use health potion",    #already used
            "use sword",            #not usable, only equippable
            "move sideways",        #invalid direction
            "adfasdfasd",           #invalid word
        ]

        print(game.player)
        print(game.get_current_location().story)
        print('\n')

        for command in test_commands:
            print(game.player)
            print(f"> {command}")
            print(parser.execute(command))
            print('\n')