class Location:
    def __init__(self, name, story, north, south, east, west, colour, item, image=None):
        self.name = name
        self.story = story
        self.north = north
        self.south = south
        self.east = east
        self.west = west
        self.colour = colour
        self.item = item
        self.image = image or f'assets/images/{name.lower()}.png'

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
