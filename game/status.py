class Status:
    """Tracks and reports player attributes like health, score, and
    currently equipped items.\
    """

    def __init__(self, player):
        self.player = player
        self.score = 0
        self.equipped_items = set()  #item names is a set since you can't equip the same item twice

    def add_score(self, amount, reason=""):
        self.score += amount
        return f"+{amount} score" + (f" ({reason})" if reason else "")

    def record_equip(self, item_name, equipped):
        if equipped:
            self.equipped_items.add(item_name)
        else:
            self.equipped_items.discard(item_name)

    def is_alive(self):
        return self.player.health_current > 0

    def summary_line(self):
        equipped = ', '.join(sorted(self.equipped_items)) or 'nothing'
        return (f"HP: {self.player.health_current}/{self.player.health_max}  "
                f"DMG: {self.player.damage}  BLOCK: {self.player.block}  "
                f"Score: {self.score}  Equipped: {equipped}")