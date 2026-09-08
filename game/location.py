# game/location.py
class Location:
    def __init__(self, name, story, north=None, south=None, 
                 east=None, west=None, item=None, image=None,
                 locked=False, locked_message=None, enemies=None):
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
        #returns enemies if truthy, else empty list. 
        self.enemies = enemies or []

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

    def get_enemy(self, name):
        for enemy in self.enemies:
            if enemy.name.lower() == name:
                return enemy
        return None

    def get_full_story(self):
        #Base story text plus a line for each currently alive enemy.
        story = self.story
        for enemy in self.enemies:
            story += '\n' + enemy.presence_text
        return story