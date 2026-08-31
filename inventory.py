class Inventory:
    def __init__(self):
        self.items = []

    def has_item(self, item):
        return item in self.items

    def add_item(self, item):
        if not self.has_item(item):
            self.items.append(item)
            return True

        return False

    def use_item(self, item, player):
        print('Not Implemented')
        pass
