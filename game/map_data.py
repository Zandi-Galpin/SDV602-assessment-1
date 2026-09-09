from game.location import Location
from game.enemy import Enemy
from game.item import Item

#set here in case map gets made bigger later.
GRID_ROWS = 4
GRID_COLUMNS = 5

#images are named row1column1.png, row1column2.png, etc
#this helps to set that up for image retrieval later
def key(row, column):
    return f"row{row}column{column}"

#dictionary of descriptions for each scene to appear to the player in the default grid
SCENE_TEXT = {
    (1, 1): "You are on a sandy beach. You see ocean to the south and a wall of rock to the west.",
    (1, 2): "You are on a sandy beach. You see a ship floating in the water to the south. A pirate calls out from the deck.",
    (1, 3): "You are on a sandy beach. You see ocean to the south.",
    (1, 4): "You are on a sandy beach. You see ocean to the south.",
    (1, 5): "You are on a sandy beach. You see ocean to the south and a wall of rock to the east.",
    (2, 1): "You are on some grassy plains. You see a beach to the south and a wall of rock to the west.",
    (2, 2): "You are on some grassy plains. You see a beach to the south.",
    (2, 3): "You are in a forest. You see a beach to the south.",
    (2, 4): "You are in a forest. You see a beach to the south.",
    (2, 5): "You are in a forest. You see a beach to the south and a wall of rock to the east.",
    (3, 1): "You are on some grassy plains. You see a wall of rock to the west and more plains to the north, east and south",
    (3, 2): "You are on some grassy plains. You see a few trees creeping in from the east.",
    (3, 3): "You are in a dense forest.",
    (3, 4): "You are in a dense forest.",
    (3, 5): "You are in a dense forest. You see a wall of rock to the east.",
    (4, 1): "You are on some grassy plains. A massive locked door sits in front of the wall to the north. You see a wall of rock to the west.",
    (4, 2): "You are on some grassy plains. You see some forest creeping in from the east and a wall of rock to the north.",
    (4, 3): "You are in a dense forest. You see a wall of rock to the north.",
    (4, 4): "You arrive at a small clearing in the forest next to a still lake. You see something glinting at the bottom of the lake. You see a wall of rock to the north.",
    (4, 5): "You are in a dense forest. You see walls of rock to the north and east."
}

#builds the grid locations based 
def build_grid_locations():
    locations = {}
    for row in range(1, GRID_ROWS + 1):
        for column in range(1, GRID_COLUMNS + 1):
            north = key(row + 1, column) if row < GRID_ROWS else None
            south = key(row - 1, column) if row > 1 else None
            east = key(row, column + 1) if column < GRID_COLUMNS else None
            west = key(row, column - 1) if column > 1 else None

            locations[key(row, column)] = Location(
                name=key(row, column),
                story=SCENE_TEXT[(row, column)],
                north=north, south=south, east=east, west=west
            )
    #row 4 column 1 north exit is the locked door. it has two images
    door = locations[key(4, 1)]
    door.north = "row5column1"
    door.locked = True
    door.locked_message = "A massive locked door blocks the way north."
    door.image = "assets/images/row4column1closed.png"

    return locations


def build_corridor_locations():
    #the 3 scenes after the door is unlocked.
    return {
        "row5column1": Location(
            name="row5column1",
            story="You enter the corridor. A golden path leads north.",
            south="row4column1", north="row6column1",
        ),
        "row6column1": Location(
            name="row6column1",
            story="The corridor continues. Something huge blocks the path ahead.",
            south="row5column1", north="row7column1",
        ),
        "row7column1": Location(
            name="row7column1",
            story="The corridor opens up and you see the pile of peas you have searched for.\n"
                  "Beyond the peas you see rolling fields. You are free.",
            south="row6column1", north=None,
        ),
    }

def populate_enemies(locations):
    """put enemies on their scenes. Called after the grid is built."""
    locations["row6column1"].enemies.append(
        Enemy(
            name="king goose",
            health=200,
            damage=15,
            score=100,
            presence_text="A massive king goose blocks the path. 'Your journey ends here.' he says coldly.",
            drops=[Item("crown"), Item("gold", amount=999)],
            ambush=True
        )
    )

    locations["row1column1"].enemies.append(
            Enemy(
                name="mouse",
                health=5,
                damage=1,
                score=5,
                presence_text="You see a mouse scuttering across the sand",
                drops=[Item("cheese", heal=10), Item("gold", amount=5)],
                ambush=False
            )
        )

    locations["row1column5"].enemies.append(
                Enemy(
                    name="horseshoe crab",
                    health=50,
                    damage=5,
                    score=20,
                    presence_text="You see a horseshoe crab, watching you menacingly",
                    drops=[Item("sashimi", heal=25), Item("crab shell", block=5), Item("gold", amount=15)],
                    ambush=False
                )
            )