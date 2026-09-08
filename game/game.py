from game.inventory import Inventory
from game.player import Player
from game.location import Location
from game.map_data import build_grid_locations, build_corridor_locations
from game.monster_fight import MonsterFight

class Game:
    def __init__(self, player: Player):
        self.player = player
        self.inventory = Inventory()
        self.monster_fight = MonsterFight()

        self.current_location: str = 'row3column1'   #spawn: row 3, col 1
        self.locations = {**build_grid_locations(), **build_corridor_locations()}


    def get_current_location(self):
        """Return the story text for the current `game_state`."""
        return self.locations[self.current_location]

    def move(self, location: Location):
        """Attempt to move in `direction`.

        Returns the new location story string or an error message when the
        move is not allowed.
        """
        self.current_location = location.name
        return self.get_display_text()

    def validate_move(self, direction: str):
        if self.monster_fight.in_battle():
            return ("You can't move while in battle!\n"
                    + self.get_display_text())

        current_location: Location = self.get_current_location()
        destination = current_location.get_direction(direction)

        if direction == 'north' and current_location.locked:
            return current_location.locked_message + '\n' + \
                current_location.story

        if destination:
            proposed_location: Location = self.locations[destination]
            return self.move(proposed_location)

        return 'You can not go that way.\n' + \
            self.get_display_text()

    def handle_attack(self, enemy_name: str) -> str:
        location = self.get_current_location()

        if self.monster_fight.in_battle():
            target = self.monster_fight.current_enemy
            if target.name.lower() != enemy_name:
                return (f"You're already fighting {target.name}.\n" + self.get_display_text())
        else:
            target = location.get_enemy(enemy_name)
            if not target:
                return f"There is no {enemy_name} here.\n" + self.get_display_text()
            self.monster_fight.start_battle(target)

        messages, defeated = self.monster_fight.resolve_attack(self.player, target)

        if defeated:
            for drop in target.drops:
                if drop.name == 'gold':
                    self.inventory.add_gold(drop.amount)
                else:
                    self.inventory.add_item(drop)
            location.enemies.remove(target)
            self.monster_fight.end_battle()

        return '\n'.join(messages) + '\n' + self.get_display_text()

    def handle_equip(self, item_name: str) -> str:
        if self.monster_fight.in_battle():
            return ("You can't equip items during battle.\n"
                    + self.get_display_text())
        message = self.inventory.equip_item(item_name, self.player)
        return message + '\n' + self.get_display_text()

    def handle_use(self, item_name: str) -> str:
        message = self.inventory.use_item(item_name, self.player)
        return message + '\n' + self.get_display_text()

    def get_display_text(self) -> str:
        """The  status text shown after any command result.
        Shows battle status while fighting, otherwise shows the location's story.
        """
        if self.monster_fight.in_battle():
            enemy = self.monster_fight.current_enemy
            return f"You are fighting {enemy.name} ({enemy.health} HP remaining)."
        return self.get_current_location().story