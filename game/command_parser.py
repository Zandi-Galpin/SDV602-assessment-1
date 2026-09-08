class CommandParser:
    #parses player input and put it through to the right game system.
    #it only knows four words and what valid direction is

    VALID_WORDS = {'move', 'attack', 'equip', 'use'}
    VALID_DIRECTIONS = {'north', 'south', 'east', 'west'}

    def __init__(self, game):
        self.game = game

    def parse(self, raw_input: str) -> tuple:
        #Splits input into (word, target) and removes empty space
        cleaned = raw_input.strip().lower()
        parts = cleaned.split(' ', 1)
        word = parts[0] if parts else ''
        target = parts[1].strip() if len(parts) > 1 else ''
        return word, target

    def execute(self, raw_input: str) -> str:
        #Parses input and calls the game action that matches.
        #Returns a message to display to the player.
        
        word, target = self.parse(raw_input)

        if self.game.is_game_over():
            if word == 'restart':
                return self.game.restart()
            return ("You were defeated. Type 'restart' to try again.")


        if word not in self.VALID_WORDS:
            return (f"'{raw_input}' is not a valid command.\n"
                    + self.game.get_display_text())

        match word:
            case 'move':
                return self.handle_move(target)
            case 'attack':
                return self.handle_attack(target)
            case 'equip':
                return self.handle_equip(target)
            case 'use':
                return self.handle_use(target)

    def handle_move(self, target: str) -> str:
        if target not in self.VALID_DIRECTIONS:
            return (f"'{target}' is not a valid direction.\n"
                    + self.game.get_display_text())
        return self.game.validate_move(target)

    def handle_attack(self, target: str) -> str:
        if not target:
            return "Attack what?\n" + self.game.get_display_text()
        return self.game.handle_attack(target)

    def handle_equip(self, target: str) -> str:
        if not target:
            return "Equip what?\n" + self.game.get_display_text()
        return self.game.handle_equip(target)

    def handle_use(self, target: str) -> str:
        if not target:
            return "Use what?\n" + self.game.get_display_text()
        return self.game.handle_use(target)