from inventory import Inventory
from game.item import Item
from game.player import Player
from game.location import Location
from game.map_data import build_grid_locations, build_corridor_locations


class Game:
    def __init__(self, player: Player):
        self.player = player
        self.inventory = Inventory()

        self.current_location = '3-1'   #spawn: row 3, col 1
        self.locations = {**build_grid_locations(), **build_corridor_locations()}


    def get_current_location(self):
        """Return the story text for the current `game_state`.

        Kept as a separate function so the GUI layout can call it when
        building the initial window contents.
        """
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
        if destination:
            proposed_location: Location = self.locations[destination]
            return self.move(proposed_location)

        return 'You can not go that way.\n' + \
            self.get_current_location().story
