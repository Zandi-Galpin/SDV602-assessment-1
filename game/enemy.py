class Enemy:
    def __init__(self, name, health, damage, drops=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.drops = drops or []#list of Item instances, guaranteed drops