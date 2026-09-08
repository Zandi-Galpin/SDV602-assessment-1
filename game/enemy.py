class Enemy:
    def __init__(self, name, health, damage, drops=None, score = 10):
        self.name = name
        self.health = health
        self.damage = damage
        self.drops = drops or []#list of Item instances, guaranteed drops
        self.score = score