"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    valid_classes = {
        "Warrior": {"health": 120, "strength": 15, "magic": 5},
        "Mage": {"health": 80, "strength": 8, "magic": 20},
        "Rogue": {"health": 90, "strength": 12, "magic": 10},
        "Cleric": {"health": 100, "strength": 10, "magic": 15},
    }
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid class: {character_class}")

    base = valid_classes[character_class]
    character = {
        "name": name,
        "class": character_class,
        "level": 1,
        "health": base["health"],
        "max_health": base["health"],
        "strength": base["strength"],
        "magic": base["magic"],
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": [],
    }
    return character

def save_character(character, save_directory="data/save_games"):
    try:
        os.makedirs(save_directory, exist_ok=True)
        filename = os.path.join(save_directory, f"{character['name']}_save.txt")
        with open(filename, "w") as f:
            f.write(f"NAME: {character['name']}\n")
            f.write(f"CLASS: {character['class']}\n")
            f.write(f"LEVEL: {character['level']}\n")
            f.write(f"HEALTH: {character['health']}\n")
            f.write(f"MAX_HEALTH: {character['max_health']}\n")
            f.write(f"STRENGTH: {character['strength']}\n")
            f.write(f"MAGIC: {character['magic']}\n")
            f.write(f"EXPERIENCE: {character['experience']}\n")
            f.write(f"GOLD: {character['gold']}\n")
            f.write(f"INVENTORY: {','.join(character['inventory'])}\n")
            f.write(f"ACTIVE_QUESTS: {','.join(character['active_quests'])}\n")
            f.write(f"COMPLETED_QUESTS: {','.join(character['completed_quests'])}\n")
        return True
    except (PermissionError, IOError) as e:
        raise e

def load_character(character_name, save_directory="data/save_games"):
    filename = os.path.join(save_directory, f"{character_name}_save.txt")
    if not os.path.exists(filename):
        raise CharacterNotFoundError(character_name)
    try:
        character = {}
        with open(filename, "r") as f:
            for line in f:
                key, value = line.strip().split(": ", 1)
                if key in ["LEVEL", "HEALTH", "MAX_HEALTH", "STRENGTH", "MAGIC", "EXPERIENCE", "GOLD"]:
                    character[key.lower()] = int(value)
                elif key in ["INVENTORY", "ACTIVE_QUESTS", "COMPLETED_QUESTS"]:
                    character[key.lower()] = value.split(",") if value else []
                else:
                    character[key.lower()] = value
        # validate required fields
        required_keys = [
            "name", "class", "level", "health", "max_health",
            "strength", "magic", "experience", "gold",
            "inventory", "active_quests", "completed_quests"
        ]
        for k in required_keys:
            if k not in character:
                raise InvalidSaveDataError(f"Missing field: {k}")
        return character
    except FileNotFoundError:
        raise CharacterNotFoundError(character_name)
    except (OSError, IOError):
        raise SaveFileCorruptedError(character_name)
    except (ValueError, KeyError):
        raise InvalidSaveDataError(character_name)

def list_saved_characters(save_directory="data/save_games"):
    if not os.path.exists(save_directory):
        return []
    files = os.listdir(save_directory)
    return [f.replace("_save.txt", "") for f in files if f.endswith("_save.txt")]

def delete_character(character_name, save_directory="data/save_games"):
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
        "inventory", "active_quests", "completed_quests"
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
    
    #Test saving
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

