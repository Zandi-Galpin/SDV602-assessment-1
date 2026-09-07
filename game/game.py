from game.inventory import Inventory
from game.item import Item
from game.player import Player
from game.location import Location
from game.map_data import build_grid_locations, build_corridor_locations


class Game:
    def __init__(self, player: Player):
        self.player = player
        self.inventory = Inventory()

        self.current_location: str = 'row3column1'   #spawn: row 3, col 1
        self.locations = {**build_grid_locations(), **build_corridor_locations()}


    def get_current_location(self):
        """Return the story text for the current `game_state`."""
        return self.locations[self.current_location]

    def move(self, location: Location):
        """Attempt to move in `direction`.

        Returns the new location story string or an error message when the
        move is not allowed.
        """
        self.current_location = location.name
        return self.get_current_location().story

    def validate_move(self, direction: str):
        current_location: Location = self.get_current_location()
        destination = current_location.get_direction(direction)

        if direction == 'north' and current_location.locked:
            return current_location.locked_message + '\n' + \
                current_location.story

        if destination:
            proposed_location: Location = self.locations[destination]
            return self.move(proposed_location)

        return 'You can not go that way.\n' + \
            self.get_current_location().story

    def handle_attack(self, enemy_name: str) -> str:
        return (f"(not finished yet, target is {enemy_name} "
            "\n" + self.get_current_location().story)

    def handle_equip(self, item_name: str) -> str:
        return (f"(not finished yet "
                f"{item_name})\n" + self.get_current_location().story)

    def handle_use(self, item_name: str) -> str:
        return (f"(not finished yet "
                f"{item_name})\n" + self.get_current_location().story)
