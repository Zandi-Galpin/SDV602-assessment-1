from game.inventory import Inventory
from game.player import Player
from game.location import Location
from game.map_data import build_grid_locations, build_corridor_locations, populate_enemies
from game.monster_fight import MonsterFight
from game.status import Status
from game.special_interactions import SPECIAL_INTERACTIONS

WIN_LOCATION = "row7column1"

class Game:
    def __init__(self, player: Player):
        self.starting_player_stats = {
            'health_max': player.health_max,
            'damage': player.damage,
            'block': player.block,
        }
        self.player = player
        self.setup_new_game()

    def setup_new_game(self):
        """build or rebuild the game stuff. Used by __init__ and restart()."""
        self.won = False
        self.player.health_current = self.player.health_max
        self.player.damage = self.starting_player_stats['damage']
        self.player.block = self.starting_player_stats['block']

        self.inventory = Inventory()
        self.monster_fight = MonsterFight()
        self.status = Status(self.player)
        
        self.current_location: str = 'row3column1'   #spawn: row 3, col 1
        self.locations = {**build_grid_locations(), **build_corridor_locations()}
        populate_enemies(self.locations)

    def is_game_over(self) -> bool:
        return not self.status.is_alive() or self.won

    def restart(self) -> str:
        self.setup_new_game()
        return ("You wake up in a grassy plains. What a strange dream.\n"
                + self.get_display_text())

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

        if not destination:
            return 'You can not go that way.\n' + self.get_display_text()

        if direction == 'north' and current_location.locked:
            return current_location.locked_message + '\n' + self.get_display_text()

        self.move(self.locations[destination])

        if self.current_location == WIN_LOCATION:
            self.won = True
            return self.get_display_text()

        ambush_message = self.check_for_ambush()
        if ambush_message:
            return ambush_message + '\n' + self.get_display_text()

        return self.get_display_text()

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
            messages.append(self.status.add_score(target.score, reason=target.name))

        return '\n'.join(messages) + '\n' + self.get_display_text()

    def handle_equip(self, item_name: str) -> str:
        if self.monster_fight.in_battle():
            return ("You can't equip items during battle.\n"
                    + self.get_display_text())

        message, now_equipped = self.inventory.equip_item(item_name, self.player)
        if now_equipped is not None:
            self.status.record_equip(item_name, now_equipped)

        return message + '\n' + self.get_display_text()

    def handle_use(self, item_name: str) -> str:
        location = self.get_current_location()
        special = SPECIAL_INTERACTIONS.get((location.name, item_name))

        if special:
            result = special(self)
            if result is not None:
                return result + '\n' + self.get_display_text()
            
        message = self.inventory.use_item(item_name, self.player)
        return message + '\n' + self.get_display_text()

    def get_display_text(self) -> str:
        """The  status text shown after any command result.
        Shows battle status while fighting, otherwise shows the location's story.
        """
        if self.monster_fight.in_battle():
            enemy = self.monster_fight.current_enemy
            return f"You are fighting {enemy.name} ({enemy.health} HP remaining)."
        return self.get_current_location().get_full_story()

    def check_for_ambush(self):
        """Called after every successful move. If the new scene has a
        ambush enemy, it attacks first, before the player can act.
        """
        if self.monster_fight.in_battle():
            return None

        location = self.get_current_location()
        for enemy in location.enemies:
            if enemy.ambush:
                self.monster_fight.start_battle(enemy)
                damage_taken = max(enemy.damage - self.player.block, 0)
                self.player.health_current = max(self.player.health_current - damage_taken, 0)

                message = (f"{enemy.name} ambushes you, hitting you for "
                        f"{damage_taken} damage!")
                if not self.status.is_alive():
                    message += "\nYou have been defeated..."
                return message

        return None

    def get_inventory_summary(self) -> str:
        if self.inventory.items:
            item_lines = [
                f"- {item.name}" + (" (equipped)" if item.equipped else "")
                for item in self.inventory.items
            ]
            items_text = "Inventory:\n" + '\n'.join(item_lines)
        else:
            items_text = "Inventory: empty"

        return f"{items_text}\nGold: {self.inventory.gold}\n" + self.get_display_text()