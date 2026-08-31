class Location:
    def __init__(self, name, story, north, south, colour, item):
        self.name = name
        self.story = story
        self.north = north
        self.south = south
        self.colour = colour
        self.item = item

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
