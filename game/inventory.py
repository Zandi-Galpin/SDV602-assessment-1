class Inventory:
    """Tracks the player's items and gold.

    Items are looked up by name (not case sensitive, because command parser
     makes the inputs lowercase before it gets to this).
    """

    def __init__(self):
        self.items = []
        self.gold = 0

    def find_item(self, item_name):
        for item in self.items:
            if item.name == item_name:
                return item
        return None

    def has_item(self, item_name):
        return self.find_item(item_name) is not None

    def add_item(self, item):
        self.items.append(item)
        return True

    def remove_item(self, item_name):
        item = self.find_item(item_name)
        if item:
            self.items.remove(item)
            return True
        return False

    def add_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False

    def equip_item(self, item_name, player):
        item = self.find_item(item_name)
        if not item:
            return f"You don't have {item_name}.", None

        if item.equipped:
            item.equipped = False
            player.damage -= item.damage
            player.block -= item.block
            return f"You unequipped {item.name}.", False

        item.equipped = True
        player.damage += item.damage
        player.block += item.block
        return f"You equipped {item.name}, gaining {item.damage} attack damage and {item.block} block.", True

    def use_item(self, item_name, player):
        #Uses a consumable (healing or gold)
        if item_name == 'gold':
            return "There's nothing to use gold on here."#only falls through to this if the use case isnt "special"

        item = self.find_item(item_name)
        if not item:
            return f"You don't have {item_name}."

        if not item.heal:
            return f"{item.name} can't be used."

        if item.used:
            return f"{item.name} has already been used."

        item.used = True
        healed = min(item.heal, player.health_max - player.health_current)
        player.health_current += healed
        self.remove_item(item_name)

        return f"You used {item.name} and healed {healed} HP."
    