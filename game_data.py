"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)


# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file '{filename}' not found")

    quests = {}
    try:
        with open(filename, "r") as f:
            lines = [line.rstrip() for line in f]
        block = []
        for line in lines + [""]:  # add empty line at end to process last block
            if line.strip() == "":
                if block:
                    quest = parse_quest_block(block)
                    quests[quest["quest_id"]] = quest
                    block = []
            else:
                block.append(line)
        return quests
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading quests: {e}")


def load_items(filename="data/items.txt"):
    """
    Load item data from file
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item file '{filename}' not found")

    items = {}
    try:
        with open(filename, "r") as f:
            lines = [line.rstrip() for line in f]
        block = []
        for line in lines + [""]:
            if line.strip() == "":
                if block:
                    item = parse_item_block(block)
                    items[item["item_id"]] = item
                    block = []
            else:
                block.append(line)
        return items
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise CorruptedDataError(f"Error reading items: {e}")


def validate_quest_data(quest_dict):
    required_keys = ["quest_id", "title", "description", "reward_xp",
                     "reward_gold", "required_level", "prerequisite"]
    for key in required_keys:
        if key not in quest_dict:
            raise InvalidDataFormatError(f"Missing quest field: {key}")
    for num_field in ["reward_xp", "reward_gold", "required_level"]:
        if not isinstance(quest_dict[num_field], int):
            raise InvalidDataFormatError(f"Field '{num_field}' must be integer")
    return True


def validate_item_data(item_dict):
    required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
    valid_types = {"weapon", "armor", "consumable"}
    for key in required_keys:
        if key not in item_dict:
            raise InvalidDataFormatError(f"Missing item field: {key}")
    if item_dict["type"].lower() not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    if not isinstance(item_dict["cost"], int):
        raise InvalidDataFormatError(f"Item cost must be integer")
    return True


def create_default_data_files():
    """
    Create default data files if they don't exist
    """
    os.makedirs("data", exist_ok=True)

    quests_file = "data/quests.txt"
    items_file = "data/items.txt"

    if not os.path.exists(quests_file):
        default_quests = """QUEST_ID: quest1
TITLE: The Beginning
DESCRIPTION: Start your journey
REWARD_XP: 100
REWARD_GOLD: 50
REQUIRED_LEVEL: 1
PREREQUISITE: NONE

QUEST_ID: quest2
TITLE: The Next Step
DESCRIPTION: Continue your adventure
REWARD_XP: 200
REWARD_GOLD: 75
REQUIRED_LEVEL: 2
PREREQUISITE: quest1
"""
        with open(quests_file, "w") as f:
            f.write(default_quests)

    if not os.path.exists(items_file):
        default_items = """ITEM_ID: sword1
NAME: Iron Sword
TYPE: weapon
EFFECT: strength:5
COST: 100
DESCRIPTION: Basic iron sword

ITEM_ID: potion1
NAME: Health Potion
TYPE: consumable
EFFECT: health:20
COST: 50
DESCRIPTION: Restores health
"""
        with open(items_file, "w") as f:
            f.write(default_items)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    quest = {}
    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing separator ': ': {line}")
            key, value = line.split(": ", 1)
            key = key.lower()
            if key in ["reward_xp", "reward_gold", "required_level"]:
                try:
                    value = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Expected numeric value for {key}, got '{value}'")
            quest[key] = value
        required_keys = ["quest_id", "title", "description", "reward_xp",
                         "reward_gold", "required_level", "prerequisite"]
        for rk in required_keys:
            if rk not in quest:
                raise InvalidDataFormatError(f"Missing required field: {rk}")
        return quest
    except Exception as e:
        if isinstance(e, InvalidDataFormatError):
            raise e
        raise InvalidDataFormatError(f"Failed to parse quest block: {e}")


def parse_item_block(lines):
    item = {}
    valid_types = {"weapon", "armor", "consumable"}
    try:
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if ": " not in line:
                raise InvalidDataFormatError(f"Line missing separator ': ': {line}")
            key, value = line.split(": ", 1)
            key = key.lower()
            if key == "cost":
                try:
                    value = int(value)
                except ValueError:
                    raise InvalidDataFormatError(f"Expected numeric value for cost, got '{value}'")
            if key == "type" and value.lower() not in valid_types:
                raise InvalidDataFormatError(f"Invalid item type: {value}")
            item[key] = value
        required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
        for rk in required_keys:
            if rk not in item:
                raise InvalidDataFormatError(f"Missing required field: {rk}")
        return item
    except Exception as e:
        if isinstance(e, InvalidDataFormatError):
            raise e
        raise InvalidDataFormatError(f"Failed to parse item block: {e}")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    create_default_data_files()

    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")

    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")


