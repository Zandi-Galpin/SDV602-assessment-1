from game.item import Item

def pirate_trade(game):
    """row1column2, 'use gold' buys fishing rod from the pirate."""
    inventory = game.inventory

    if inventory.has_item('fishing rod'):
        return "ARGGGGHGH!!!! YOU'VE ALREADY BOUGHT ME FISHING ROD!!"

    if not inventory.spend_gold(50):
        return f"YOU TAKE ME FOR A FOOL??? YE ONLY HAVE {inventory.gold}" + \
            " GOLD!! ME FISHING ROD WILL COST YE AT LEAST 50!!!"

    inventory.add_item(Item('fishing rod'))
    return "The pirate hands you a fishing rod. \"Pleasure doing business. NOW BEGONE!\""


def use_fishing_rod(game):
    """row4column4, 'use fishing rod' at the lake gives a key."""
    inventory = game.inventory

    if not inventory.has_item('fishing rod'):
        return None  #usual inventory message works here i think

    if inventory.has_item('key'):
        return "You keep fishing but don't find anything else useful"

    inventory.add_item(Item('key'))
    return "You send the fishing rod into the lake and reel in a key!"


def use_key(game):
    """row4column1, 'use key' unlocks the door north."""
    door = game.get_current_location()

    if not door.locked:
        return "The door is already open."

    inventory = game.inventory
    if not inventory.has_item('key'):
        return None  #usual inventory message should work here too

    inventory.remove_item('key')
    door.locked = False
    door.image = 'assets/images/row4column1open.png'
    return "The massive door opens and you see a golden path leading north."


SPECIAL_INTERACTIONS = {
    ('row1column2', 'gold'): pirate_trade,
    ('row4column4', 'fishing rod'): use_fishing_rod,
    ('row4column1', 'key'): use_key,
}