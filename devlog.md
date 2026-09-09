# Development Log: Legendary Goose Assassin 2026

## Overview

This log documents the development of Legendary Goose Assassin 2026, which is a text adventure I made from a set of given starter code files. This log covers the challenges I had while building the four required modules (`command_parser.py`, `monster_fight.py`, `inventory.py`, `status.py`), evidence of the needed data types (Tuples, Lists, Dictionaries, Sets, Comprehensions), and a reflection.

Development was version controlled, with incremental commits. Except for this file, which I made retroactively at the end.

## Development Diary

### Restructuring the starter template

The provided starter code (`game.py`, `gui.py`, `inventory.py`, `item.py`, `location.py`, `player.py`) only supported a 3-room map connected by north/south, and used background colours instead of images for scenes. Before I could add any new logic, I had to restructure things. 

I Moved the provided files into a `game` folder.
I Added `east`/`west` directions to `Location`, since the full map needs them.
I Removed the `colour` attribute and replaced the colours with images.
I Fixed a bug where the spawn location string didn't match the actual location name used elsewhere, causing it not to match when starting the application. 

### Building the grid map

Rather than writing 20 `Location` objects for the grid myself, `map_data.py` builds them from row and column coords, with the locked door at `row4column1` as a special case. For the door, its north exit is to the 3 corridor scenes but is  behind a `locked` flag. The three corridor scenes after
the door (leading to the boss and golden peas) I added as a separate function and put them both into the same dictionary in `game.py` for locations.

### `command_parser` / `Game` / GUI being split up

Originally, `gui.py` did input validation itself. `command_parser.py` was built to take over this and other functionality. it splits the input into a word and a target, validates the word, and calls the matching method on `Game`. I updated `refactored.py`'s headless test mode and `gui.py` to go through the same `CommandParser` instance, so headless testing has the same logic path as the GUI rather than separate.

### Inventory and equip logic

`inventory.py` was built with item lookup, add and remove, and gold tracking, plus `equip_item` and `use_item` methods that change the player's stats or heal them. Originally, multiple items could be equipped (stacking bonuses), but I didnt want this, so I updated `equip_item` so equipping a new item automatically unequipped whatever was already equipped, and I changed `status.py`'s equipped item tracking from being
incremental add or remove to a `sync_equipped` method that gets the equipped set from the inventory. Doing this avoided a bug where the tracked set could be out of sync with the inventory after swapping.

### `status.py` 

I added `status.py` to track health, score, and equipped items in one place, so that other modules didn't each build their own version of logic to check the status of the player (like if they are alive). I added score specifically because it was important to the rubric. I don't think it adds much to my game but it could be useful if I extended it in the future. 

### Combat and `get_display_text`

built `monster_fight.py` to manage battle state and resolve one attack + one counter attack per turn. Once combat existed, the game needed a way to say who you were fighting instead of just repeating the room description. Added 
`get_display_text()` to `game.py` to decide what text to show after any command, which switched between the battle status and the location's story depending on the state. Everywhere that used to reference `self.get_current_location().story` I updated to go through this function instead, including inside `command_parser.py` 

### Enemy placement and dynamic scene text

Changed `enemy.py` with adding a `presence_text` field, and `Location.get_full_story()` was made so that I could add the presence text of any enemy still alive in that scene. since
defeated enemies are removed from `location.enemies` this meant there was no problem with before/after scene text as the presence_text was removed along with the enemy.

### Special interactions (pirate, fishing rod, key)

Instead of doing `if` checks for each puzzle interaction in `handle_use`, I added `special_interactions.py` with a lookup table keyed by `(location_name, item_name)`. Each was mapped to a handler function. This kept the three specific behaviours (buying the fishing rod, fishing for the key, unlocking
the door) away from the regular inventory logic, which also had a fallback so that gold (which is tracked as a counter rather than an `Item`) doesn't say "you don't have that" if you use it outside of the pirate scene.

### Ambush mechanic and the win condition

The ambush mechanic (enemy attacking before the player can act) needed to trigger when entering a scene, otherwise the player still had a chance to attack first. This meant there was a bug. My first version checked for an ambush using the destination before making sure that the direction was a valid move, which crashed the application when trying to move past walls (referencing images that didnt exist). I fixed this by reordering `validate_move` to validate the destination first, then do the move, and then check the ambush/win state against the current location. A similar bug caused the win message to need two commands before it would appear, because the win check happened before the move instead of after it.

### Defeat, restart, and locking out commands

Important bug: after the player's health reached zero, commands were still being accepted, just in a weird way. If you tried to attack again, it wouldn't work. But if you tried to move, it would say you couldnt. THEN if you tried to attack again it would would. Repeating this would repeatedly attack a boss until you defeated it. This was fixed by adding a `is_game_over()` check in `command_parser.py`, which was checked before any other command got processed, and only
allows a `restart` command through once the player is defeated (or has won). Restarting meant putting `Game.__init__` into a separate `setup_new_game()` method so the same setup logic could run again upon restarting, including setting the player's stats back to their original values (important because equipped items otherwise permanently modified `player.damage`/`player.block`, which needed to be undone upon restarting rather than carried over, unless I wanted some kind of rogue like mechanic which could be interesting if I had more time.).

### Testing and polishing

Headless testing originall had a hardcoded script of commands, manually read by the user. This I replaced with `test_runner.py` which was a set of test functions, with each running against a new `Game` instance, with assertions and a runner
that caught failures/errors for each test (so that one broken test didn't stop the rest) and returned a results object which said the summary for passed/failed/error tests. I then updated `refactored.py` to accept a `--headless` flag rather hardcoded boolean, this was a cool discovery because switching between the GUI and the test suite now does't require editing the file.

Smaller issues along the way included the GUI cutting off the image (from when the display was a `sg.Graph`, fixed by removing the fixed size and enabling `resizable=True`). Another issue was the text getting cut off since only 4 lines of text could be shown at once. I set this to 20 instead. I also added a `help` command that works at any time, including during battle and after the game over.


## Data Type Evidence

### Tuples

`game/command_parser.py`, inside `parse()`:

```python
def parse(self, raw_input: str) -> tuple:
    #Splits input into (word, target) and removes empty space
    cleaned = raw_input.strip().lower()
    parts = cleaned.split(' ', 1)
    word = parts[0] if parts else ''
    target = parts[1].strip() if len(parts) > 1 else ''
    return word, target
```

A tuple is used here because the function always needs to return two related (but different) values as a single unit, which gets unpacksed with `word, target = self.parse(raw_input)`. A list wasn't appropriate because the two values have different meanings based on their position (1st or 2nd).

`game/special_interactions.py`, in the `SPECIAL_INTERACTIONS` dictionary:

```python
SPECIAL_INTERACTIONS = {
    ('row1column2', 'gold'): pirate_trade,
    ('row4column4', 'fishing rod'): use_fishing_rod,
    ('row4column1', 'key'): use_key,
}
```

Tuples are used as dictionary keys here because a dictionary key must be immutable (lists can't be used as keys) and each interaction is unique and identified by the
combination of a location and an item, not by either one alone.

### Lists

`game/inventory.py`, in `Inventory.__init__`:

```python
def __init__(self):
    self.items = []
    self.gold = 0
```

A list is used for `items` because the number of items a player is carrying changes constantly (added upon pickup, removed when used) and the order doesn't need to have meaning, so a list supports this kind of mutable collection.

`game/enemy.py`, in `Enemy.__init__`:

```python
def __init__(self, name, health, damage, drops=None, score = 10, presence_text=None, ambush=False):
    self.name = name
    self.health = health
    self.damage = damage
    self.drops = drops or []#list of Item instances, guaranteed drops
```

Each enemy can drop a certain number of items (some drop one item, others drop more), so a list holds however many `Item` instances that enemy has.

### Dictionaries

`game/map_data.py`, in `SCENE_TEXT`:

```python
SCENE_TEXT = {
    (1, 1): "You are on a sandy beach. You see ocean to the south and a wall of rock to the west.",
    (1, 2): "You are on a sandy beach. You see a ship floating in the water to the south. There is a sign pointing to a pirate. 'FISHING ROD FOR SALE, 50 GOLD'",
    ...
}
```

A dictionary maps each grid coordinate to its story text, so `build_grid_locations()` can look up the description for any `(row, col)` pair while generating the grid in a loop, (instead of writing a bunch of `if` statements to match coords to text).

`game/game.py`, in `Game.setup_new_game()`:

```python
self.locations = {**build_grid_locations(), **build_corridor_locations()}
```

The two location dictionaries (the main grid and the 3 corridor scenes) I merged into one dictionary using the `**` to unpack them, so every scene in the game is in the same place can be looked up by name from a single `self.locations` dictionary in `get_current_location()`.

### Sets

`game/command_parser.py`, in `CommandParser`:

```python
VALID_WORDS = {'move', 'attack', 'equip', 'use', 'inventory'}
VALID_DIRECTIONS = {'north', 'south', 'east', 'west'}
```

Sets are used here because this type of checking (`word not in self.VALID_WORDS`) is the only operation these collections need to support, so order doesn't matter and duplicate values wouldn't make sense, so a set communicates that well.

`game/status.py`, in `Status.__init__` and `sync_equipped`:

```python
self.equipped_items = set()
...
def sync_equipped(self, inventory):
    self.equipped_items = {item.name for item in inventory.items if item.equipped}
```

A set is used for equipped item names because an item can't be equipped twice, and set makes it easy to check whether an item is currently equipped without caring about order.

### Comprehensions

`game/status.py`, in `sync_equipped` (set comprehension, shown above):

```python
self.equipped_items = {item.name for item in inventory.items if item.equipped}
```

This builds the set of currently equipped item names from the inventory in one line, filtering out any item where `equipped` is `False`, rather than looping and
appending to an empty set manually.

`game/game.py`, in `get_inventory_summary()` (list comprehension):

```python
item_lines = [
    f"- {item.name} ({item.describe_effect()})" +
    (" (equipped)" if item.equipped else "")
    for item in self.inventory.items
]
```

This builds one formatted display line for each inventory item, including its effect description and an "(equipped)" marker for equipped items, which is done in a single expression instead of a loop with manual list building.

---

## Reflection

I think starting with a big scripted test in refactored.py was a good starting point, it let me make sure that each new module worked as I built it, without having to write assertions before deciding what the functions should return. Althought, once the game had lots of interacting systems, the single script wasnt as useful and instead i just tested it manually through running the gui and putting in commands myself. or at least i did until I made the test runner to test everything easily and having an easily readable output to see if anything failed. If I did a similar project I would make the test functions structure from the beginning just to prepare for it to get bigger.

The main lesson I took from the bugs I encountered was that a function shouldnt check the game's current state and change the games current state without deciding what order they should be done in. Once I got into a better way of writing the functions in order I didnt encounter that type of bug again. If I did this again, I would try to order things better from the beginning.

Even though python was the first language I ever learned, I had gotten more used to other languages as I hadn't used it since year 13. Because of this, it was interesting to see how much I could do wrong and have the code still run in the first place. For example, the fact that the code ran until I encountered the bug trying to pass through a wall caught me by surprise. This made it faster to do things but caused more bugs.

If I was starting again from the beginning, I would design the structure from the beginning rather than getting to it through refactoring.