"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
import json

from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InsufficientGoldError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================


# Allowed character classes and starter stats
VALID_CLASSES = {
    "Warrior": {"hp": 120, "attack": 10, "defense": 8},
    "Mage": {"hp": 80, "attack": 15, "defense": 4},
    "Rogue": {"hp": 100, "attack": 12, "defense": 6}
}

SAVE_FOLDER = "saves"


# ============================================================================
# CHARACTER CREATION & LOADING
# ============================================================================

def create_character(name, char_class):
    """Create a new character dictionary."""
    if char_class not in VALID_CLASSES:
        raise InvalidCharacterClassError(f"Invalid class: {char_class}")

    stats = VALID_CLASSES[char_class]

    character = {
        "name": name,
        "class": char_class,
        "level": 1,
        "experience": 0,
        "gold": 100,
        "hp": stats["hp"],
        "max_hp": stats["hp"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "inventory": [],
        "equipment": {"weapon": None, "armor": None},
        "active_quests": [],
        "completed_quests": []
    }

    return character


def save_character(character):
    """Save character data to disk."""
    if not os.path.exists(SAVE_FOLDER):
        os.makedirs(SAVE_FOLDER)

    filename = os.path.join(SAVE_FOLDER, character["name"] + ".json")

    try:
        with open(filename, "w") as file:
            json.dump(character, file, indent=4)
    except:
        raise SaveFileCorruptedError("Could not save character file.")


def load_character(name):
    """Load character data from disk."""
    filename = os.path.join(SAVE_FOLDER, name + ".json")

    if not os.path.exists(filename):
        raise CharacterNotFoundError(f"No save file found for {name}")

    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return data
    except:
        raise SaveFileCorruptedError("Save file is corrupted.")


def list_saved_characters():
    """Return list of saved character names."""
    if not os.path.exists(SAVE_FOLDER):
        return []

    files = os.listdir(SAVE_FOLDER)
    names = []

    for f in files:
        if f.endswith(".json"):
            names.append(f[:-5])  # remove ".json"

    return names


# ============================================================================
# EXPERIENCE & LEVELING
# ============================================================================

def gain_experience(character, amount):
    """Add experience and automatically handle level-ups."""
    character["experience"] += amount

    while character["experience"] >= experience_to_next_level(character["level"]):
        character["experience"] -= experience_to_next_level(character["level"])
        level_up(character)


def experience_to_next_level(level):
    """Simple XP formula."""
    return 100 + (level - 1) * 50


def level_up(character):
    """Increase character stats when leveling up."""
    character["level"] += 1
    character["max_hp"] += 10
    character["hp"] = character["max_hp"]
    character["attack"] += 2
    character["defense"] += 1


# ============================================================================
# GOLD MANAGEMENT
# ============================================================================

def add_gold(character, amount):
    """Increase gold."""
    character["gold"] += amount


def remove_gold(character, amount):
    """Remove gold or raise error."""
    if character["gold"] < amount:
        raise InsufficientGoldError("Not enough gold!")

    character["gold"] -= amount


# ============================================================================
# HEALTH MANAGEMENT
# ============================================================================

def take_damage(character, amount):
    """Apply damage after defense."""
    damage = amount - character["defense"]
    if damage < 1:
        damage = 1

    character["hp"] -= damage
    if character["hp"] < 0:
        character["hp"] = 0

    return damage


def heal_character(character, amount):
    """Heal but not above max HP."""
    character["hp"] += amount
    if character["hp"] > character["max_hp"]:
        character["hp"] = character["max_hp"]


def is_dead(character):
    return character["hp"] <= 0


def revive_character(character):
    """Revive the character at half HP."""
    character["hp"] = character["max_hp"] // 2


# ============================================================================
# DISPLAY
# ============================================================================

def display_character(character):
    print("\n=== CHARACTER INFO ===")
    print(f"Name: {character['name']}")
    print(f"Class: {character['class']}")
    print(f"Level: {character['level']}")
    print(f"HP: {character['hp']} / {character['max_hp']}")
    print(f"Attack: {character['attack']}")
    print(f"Defense: {character['defense']}")
    print(f"Gold: {character['gold']}")
    print()



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

