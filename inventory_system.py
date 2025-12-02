"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20


# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory is full.")

    character["inventory"].append(item_id)
    return True


def remove_item_from_inventory(character, item_id):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(item_id)

    character["inventory"].remove(item_id)
    return True


def has_item(character, item_id):
    return item_id in character["inventory"]


def count_item(character, item_id):
    return character["inventory"].count(item_id)


def get_inventory_space_remaining(character):
    return MAX_INVENTORY_SIZE - len(character["inventory"])


def clear_inventory(character):
    removed_items = character["inventory"][:]
    character["inventory"].clear()
    return removed_items


# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(item_id)

    if not item_data or item_data.get("type") != "consumable":
        raise InvalidItemTypeError("Item data missing or not consumable")

    # Example effect processing
    if "health" in item_data.get("effect", ""):
        heal_amount = int(item_data["effect"].split(":")[1])
        character["health"] = min(character["max_health"], character["health"] + heal_amount)

    # Remove used item
    character["inventory"].remove(item_id)
    return True


# ============================================================================
# EQUIPMENT SYSTEM
# ============================================================================

def equip_weapon(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(item_id)
    if not item_data or item_data.get("type") != "weapon":
        raise InvalidItemTypeError("Item is not a weapon")

    if "strength" in item_data.get("effect", ""):
        bonus = int(item_data["effect"].split(":")[1])
        character["strength"] += bonus

    character["equipped_weapon"] = item_id
    character["inventory"].remove(item_id)
    return True


def equip_armor(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(item_id)
    if not item_data or item_data.get("type") != "armor":
        raise InvalidItemTypeError("Item is not armor.")

    effect = item_data.get("effect", "")
    stat, value = parse_item_effect(effect)

    old_armor = character.get("equipped_armor")
    if old_armor:
        old_stat, old_val = parse_item_effect(item_data["effect"])
        character[old_stat] -= old_val
        character["inventory"].append(old_armor)

    character["equipped_armor"] = item_id
    character["inventory"].remove(item_id)
    character[stat] += value

    return True

def unequip_weapon(character):
    old_weapon = character.get("equipped_weapon")
    if not old_weapon:
        return None

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full – cannot unequip.")

    # Remove stat bonus
    stat, value = parse_item_effect(character["item_data"][old_weapon]["effect"])
    apply_stat_effect(character, stat, -value)

    # Move to inventory
    character["inventory"].append(old_weapon)
    character["equipped_weapon"] = None

    return old_weapon


def unequip_armor(character):
    old_armor = character.get("equipped_armor")
    if not old_armor:
        return None

    if len(character["inventory"]) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError("Inventory full – cannot unequip.")

    stat, value = parse_item_effect(character["item_data"][old_armor]["effect"])
    apply_stat_effect(character, stat, -value)

    character["inventory"].append(old_armor)
    character["equipped_armor"] = None

    return old_armor


# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    if not item_data:
        raise ItemNotFoundError(item_id)
    cost = item_data.get("cost")
    if cost is None or not isinstance(cost, (int, float)):
        raise InvalidItemTypeError(f"Item {item_id} has invalid cost")
    if character.get("gold", 0) < cost:
        raise InsufficientResourcesError(f"Character has {character.get('gold', 0)} gold but needs {cost} to buy {item_id}")

    character["gold"] -= cost
    character.setdefault("inventory", []).append(item_id)
    return True

def sell_item(character, item_id, item_data):
    if item_id not in character["inventory"]:
        raise ItemNotFoundError(item_id)

    # Use the passed dictionary directly
    cost = item_data.get("cost", 0)
    character["gold"] += cost
    character["inventory"].remove(item_id)
    return cost


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    # Example: "health:20" → ("health", 20)
    if ":" not in effect_string:
        return ("none", 0)

    stat, value = effect_string.split(":")
    return stat, int(value)


def apply_stat_effect(character, stat_name, value):
    if stat_name not in character:
        return  # Unknown stat → ignore silently

    character[stat_name] += value

    if stat_name == "health" and character["health"] > character["max_health"]:
        character["health"] = character["max_health"]


def display_inventory(character, item_data_dict):
    print("\n=== INVENTORY ===")
    if not character["inventory"]:
        print("Inventory empty.")
        return

    counted = {}
    for item in character["inventory"]:
        counted[item] = counted.get(item, 0) + 1

    for item_id, qty in counted.items():
        name = item_data_dict.get(item_id, {}).get("name", item_id)
        print(f"{name} (x{qty})")

    print("\nEquipped:")
    print("Weapon:", character.get("equipped_weapon"))
    print("Armor:", character.get("equipped_armor"))


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")

    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}

    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
        print("Inventory is full!")

    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }

    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")
