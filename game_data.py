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
    # TODO: Implement this function
    if not os.path.exists(filename):
        # File does not exist → raise custom exception
        raise MissingDataFileError(f"Quest data file '{filename}' not found.")

    quests = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            block = []
            for line in f:
                line = line.strip()
                if line == "":
                    # Blank line indicates end of a quest block
                    if block:
                        quest = parse_quest_block(block)
                        quests[quest['quest_id']] = quest
                        block = []
                else:
                    block.append(line)
            # Handle last block if file doesn't end with blank line
            if block:
                quest = parse_quest_block(block)
                quests[quest['quest_id']] = quest
    except UnicodeDecodeError:
        # File content cannot be read → treat as corrupted
        raise CorruptedDataError(f"Quest data file '{filename}' is corrupted.")
    except InvalidDataFormatError:
        # Re-raise parsing errors
        raise
    except Exception as e:
        # Any other unexpected error
        raise InvalidDataFormatError(f"Error loading quest data: {e}")

    return quests


def load_items(filename="data/items.txt"):
    """
    Load item data from file

    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    if not os.path.exists(filename):
        raise MissingDataFileError(f"Item data file '{filename}' not found.")

    items = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            block = []
            for line in f:
                line = line.strip()
                if line == "":
                    # Blank line → end of item block
                    if block:
                        item = parse_item_block(block)
                        items[item['item_id']] = item
                        block = []
                else:
                    block.append(line)
            # Handle last block if file doesn't end with blank line
            if block:
                item = parse_item_block(block)
                items[item['item_id']] = item
    except UnicodeDecodeError:
        raise CorruptedDataError(f"Item data file '{filename}' is corrupted.")
    except InvalidDataFormatError:
        raise
    except Exception as e:
        raise InvalidDataFormatError(f"Error loading item data: {e}")

    return items


def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    """
    # TODO: Implement validation
    required_fields = ['quest_id', 'title', 'description', 'reward_xp',
                       'reward_gold', 'required_level', 'prerequisite']
    for field in required_fields:
        if field not in quest_dict:
            raise InvalidDataFormatError(f"Quest missing required field '{field}'")

    # Ensure numeric fields are integers
    for numeric_field in ['reward_xp', 'reward_gold', 'required_level']:
        if not isinstance(quest_dict[numeric_field], int):
            raise InvalidDataFormatError(f"Quest field '{numeric_field}' must be an integer")

    return True


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    """
    # TODO: Implement validation
    required_fields = ['item_id', 'name', 'type', 'effect', 'cost', 'description']
    for field in required_fields:
        if field not in item_dict:
            raise InvalidDataFormatError(f"Item missing required field '{field}'")

    valid_types = ['weapon', 'armor', 'consumable']
    if item_dict['type'] not in valid_types:
        raise InvalidDataFormatError(f"Invalid item type '{item_dict['type']}'")

    # Ensure cost is numeric
    if not isinstance(item_dict['cost'], int):
        raise InvalidDataFormatError(f"Item 'cost' must be an integer")

    return True


def create_default_data_files():
    """
    Create default data files if they don't exist
    """
    # TODO: Implement this function
    os.makedirs("data", exist_ok=True)  # Ensure data directory exists

    # Default quest file
    quest_file = "data/quests.txt"
    if not os.path.exists(quest_file):
        with open(quest_file, "w", encoding="utf-8") as f:
            f.write(
                "QUEST_ID:quest_001\n"
                "TITLE:First Adventure\n"
                "DESCRIPTION:Complete your first quest.\n"
                "REWARD_XP:100\n"
                "REWARD_GOLD:50\n"
                "REQUIRED_LEVEL:1\n"
                "PREREQUISITE:NONE\n\n"
            )

    # Default item file
    item_file = "data/items.txt"
    if not os.path.exists(item_file):
        with open(item_file, "w", encoding="utf-8") as f:
            f.write(
                "ITEM_ID:item_001\n"
                "NAME:Health Potion\n"
                "TYPE:consumable\n"
                "EFFECT:health:50\n"
                "COST:20\n"
                "DESCRIPTION:Restores 50 health.\n\n"
            )


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    """
    # TODO: Implement parsing logic
    quest = {}
    try:
        for line in lines:
            key, value = line.split(":", 1)  # Split only on first colon
            key = key.strip().lower()
            value = value.strip()
            if key == "reward_xp" or key == "reward_gold" or key == "required_level":
                value = int(value)  # Convert numeric fields to int
            quest[key] = value
        # Validate quest data
        validate_quest_data({
            'quest_id': quest.get('quest_id'),
            'title': quest.get('title'),
            'description': quest.get('description'),
            'reward_xp': quest.get('reward_xp'),
            'reward_gold': quest.get('reward_gold'),
            'required_level': quest.get('required_level'),
            'prerequisite': quest.get('prerequisite')
        })
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse quest block: {e}")

    return quest


def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    """
    # TODO: Implement parsing logic
    item = {}
    try:
        for line in lines:
            key, value = line.split(":", 1)
            key = key.strip().lower()
            value = value.strip()
            if key == "cost":
                value = int(value)  # Convert cost to integer
            item[key] = value
        # Validate item data
        validate_item_data({
            'item_id': item.get('item_id'),
            'name': item.get('name'),
            'type': item.get('type'),
            'effect': item.get('effect'),
            'cost': item.get('cost'),
            'description': item.get('description')
        })
    except Exception as e:
        raise InvalidDataFormatError(f"Failed to parse item block: {e}")

    return item


# ============================================================================
# TESTING
# ============================================================================


if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")

    # Create default files if missing
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


