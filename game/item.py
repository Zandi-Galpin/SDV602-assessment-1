class Item:
    def __init__(self, name, heal=0, damage=0, block=0, amount = 0):
        self.name = name
        self.heal = heal
        self.block = block
        self.damage = damage

        self.amount = amount  #used for gold or else ignored 

        self.used = False
        self.equipped = False

    def describe_effect(self):
        """description of what this item does,
        displays in the inventory list."""
        parts = []
        if self.heal:
            parts.append(f"heals {self.heal} HP")
        if self.damage:
            parts.append(f"+{self.damage} attack")
        if self.block:
            parts.append(f"+{self.block} block")

        return ', '.join(parts) if parts else "no effect"