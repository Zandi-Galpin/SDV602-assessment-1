class MonsterFight:
    """Manages battle and attacks.

    A battle starts the moment the user attacks an enemy.
    The user always attacks first (no ambush
    yet). Attacking ends the users turn and the enemy
    attacks immediately if it survived
    """

    def __init__(self):
        self.current_enemy = None

    def in_battle(self):
        return self.current_enemy is not None

    def start_battle(self, enemy):
        self.current_enemy = enemy

    def end_battle(self):
        self.current_enemy = None

    def resolve_attack(self, player, enemy):
        """does one player attack + one enemy attack.
        Returns (messages, enemy_defeated).
        """
        messages = []

        enemy.health -= player.damage
        messages.append(f"You hit {enemy.name} for {player.damage} damage.")

        if enemy.health <= 0:
            messages.append(f"You defeated {enemy.name}!")
            return messages, True

        enemy_attack = max(enemy.damage - player.block, 0)
        player.health_current = max(player.health_current - enemy_attack, 0)
        messages.append(f"{enemy.name} hits you back for {enemy_attack} damage.")

        if player.health_current <= 0:
            messages.append("You have been defeated...")

        return messages, False