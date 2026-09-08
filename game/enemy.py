class Enemy:
    def __init__(self, name, health, damage, drops=None, score = 10, presence_text=None):
        self.name = name
        self.health = health
        self.damage = damage
        self.drops = drops or []#list of Item instances, guaranteed drops
        self.score = score
        self.presence_text = presence_text or f"You see a {name} here."