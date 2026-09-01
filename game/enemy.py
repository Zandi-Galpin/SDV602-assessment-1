class Enemy:
    def __init__(self, name, health, damage, drops):
        self.name = name
        self.health = health
        self.damage = damage
        self.drops = drops  #list of Item instances, guaranteed drops