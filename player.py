class Player:
    def __init__(self, health_max=100, health_current=100, damage=5, block=2):
        self.health_max = health_max
        self.health_current = health_current
        self.damage = damage
        self.block = block

    def __str__(self):
        return ('HP: ' + str(self.health_current) +
                '/' + str(self.health_max) +
                ' DMG: ' + str(self.damage) +
                ' BLOCK: ' + str(self.block))
