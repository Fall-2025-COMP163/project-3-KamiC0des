"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    CharacterNotFoundError,
    InvalidSaveDataError,
    SaveFileCorruptedError,
    InvalidCharacterClassError,
    CharacterDeadError
)

SAVE_DIR = "data/save_games"


ALLOWED_CLASSES = ["Warrior", "Mage", "Cleric", "Rogue"]  # added Rogue


def create_character(name, char_class):
    if char_class not in ALLOWED_CLASSES:
        raise InvalidCharacterClassError(char_class)

    character = {
        "name": name,
        "class": char_class,
        "level": 1,
        "health": 100,
        "max_health": 100,
        "strength": 10,
        "magic": 5,
        "experience": 0,
        "gold": 0,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
        "equipped_weapon": None,
        "equipped_armor": None,
    }
    return character


def save_character(character, save_directory=SAVE_DIR):
    os.makedirs(save_directory, exist_ok=True)
    filename = os.path.join(save_directory, f"{character['name']}_save.txt")
    try:
        with open(filename, "w") as f:
            for key, value in character.items():
                if isinstance(value, list):
                    value = ",".join(value)
                f.write(f"{key.upper()}: {value}\n")
        return True
    except (OSError, IOError):
        return False


def load_character(character_name, save_directory=SAVE_DIR):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(character_name)

    character = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or ": " not in line:
                    continue
                key, value = line.split(": ", 1)
                key_upper = key.upper()

                if key_upper in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"]:
                    character[key.lower()] = int(value)
                elif key_upper in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                    character[key.lower()] = value.split(",") if value else []
                else:
                    character[key.lower()] = value

        required_keys = [
            "name", "class", "level", "health", "max_health",
            "strength", "magic", "experience", "gold",
            "inventory", "active_quests", "completed_quests",
            "equipped_weapon", "equipped_armor"
        ]
        for k in required_keys:
            if k not in character:
                raise InvalidSaveDataError(f"Missing field: {k}")

        return character
    except (ValueError, KeyError):
        raise InvalidSaveDataError(character_name)
    except (OSError, IOError):
        raise SaveFileCorruptedError(character_name)


def list_saved_characters(save_directory=SAVE_DIR):
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]


def delete_character(character_name, save_directory=SAVE_DIR):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(character_name)
    os.remove(filename)
    return True


# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    if is_character_dead(character):
        raise CharacterDeadError(f"{character['name']} is dead!")
    character["experience"] += xp_amount
    while character["experience"] >= character["level"] * 100:
        character["experience"] -= character["level"] * 100
        character["level"] += 1
        character["max_health"] += 10
        character["strength"] += 2
        character["magic"] += 2
        character["health"] = character["max_health"]


def add_gold(character, amount):
    new_gold = character["gold"] + amount
    if new_gold < 0:
        raise ValueError("Not enough gold!")
    character["gold"] = new_gold
    return character["gold"]


def heal_character(character, amount):
    heal_amount = min(amount, character["max_health"] - character["health"])
    character["health"] += heal_amount
    return heal_amount


def is_character_dead(character):
    return character["health"] <= 0


def revive_character(character):
    if not is_character_dead(character):
        return False
    character["health"] = character["max_health"] // 2
    return True


# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    required_keys = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold",
        "inventory", "active_quests", "completed_quests",
        "equipped_weapon", "equipped_armor"
    ]
    for key in required_keys:
        if key not in character:
            raise InvalidSaveDataError(f"Missing key: {key}")
    if not isinstance(character["level"], int) or not isinstance(character["experience"], int):
        raise InvalidSaveDataError("Level and experience must be integers")
    for list_key in ["inventory", "active_quests", "completed_quests"]:
        if not isinstance(character[list_key], list):
            raise InvalidSaveDataError(f"{list_key} must be a list")
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")

    # Test character creation
    try:
        char = create_character("TestHero", "Warrior")
        print(f"Created: {char['name']} the {char['class']}")
        print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
        print(f"Invalid class: {e}")

    # Test saving
    try:
        save_character(char)
        print("Character saved successfully")
    except Exception as e:
        print(f"Save error: {e}")

    # Test loading
    try:
        loaded = load_character("TestHero")
        print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
        print("Character not found")
    except SaveFileCorruptedError:
        print("Save file corrupted")
