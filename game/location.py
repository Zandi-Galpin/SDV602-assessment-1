# game/location.py
class Location:
    def __init__(self, name, story, north=None, south=None, 
                 east=None, west=None, item=None, image=None,
                 locked=False, locked_message=None):
        self.name = name
        self.story = story
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.item = item
        self.image = image or f'assets/images/{name}.png'
        self.locked = locked
        self.locked_message = locked_message or "It's locked. You'll need a key."

    def __getitem__(self, attribute):
        match attribute:
            case 'name':
                return self.name
            case 'north':
                return self.north
            case 'south':
                return self.south

    def get_direction(self, direction):
        match direction:
            case 'north':
                return self.north
            case 'south':
                return self.south
            case 'east':
                return self.east
            case 'west':
                return self.west
