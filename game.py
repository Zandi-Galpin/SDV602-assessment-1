from inventory import Inventory
from item import Item
from player import Player
from location import Location


class Game:
    def __init__(self, player: Player):
        self.player = player
        self.inventory = Inventory()

        self.current_location: str = 'Forest'
        self.locations = {
            'Forest': Location(
                name='Forest',
                story='You are in the forest.\nTo the north is a cave.\nTo the south is a castle',
                north='Cave',
                south='Castle',
                colour="#0000FF",
                item=Item('health potion', heal=25)
            ),
            'Castle': Location(
                name='Castle',
                story='You are at the castle.\nTo the north is forest.',
                north='Forest',
                south='',
                colour="#00FF00",
                item=Item('sword', damage=5)
            ),
            'Cave': Location(
                name='Cave',
                story='You are at the cave.\nTo the south is forest.',
                north='',
                south='Forest',
                colour="#FF0000",
                item=Item('shield', block=4)
            ),
        }

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
