"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """Accept a new quest"""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")

    quest = quest_data_dict[quest_id]

    if character['level'] < quest['required_level']:
        raise InsufficientLevelError(f"Level {quest['required_level']} required.")

    prereq = quest.get('prerequisite', 'NONE')
    if prereq != "NONE" and prereq not in character['completed_quests']:
        raise QuestRequirementsNotMetError(f"Prerequisite quest {prereq} not completed.")

    if quest_id in character['completed_quests']:
        raise QuestAlreadyCompletedError(f"Quest {quest_id} already completed.")

    if quest_id in character['active_quests']:
        raise QuestRequirementsNotMetError(f"Quest {quest_id} is already active.")

    character['active_quests'].append(quest_id)
    return True


def complete_quest(character, quest_id, quest_data_dict):
    """Complete an active quest and grant rewards"""
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")

    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest {quest_id} is not active.")

    quest = quest_data_dict[quest_id]
    character['active_quests'].remove(quest_id)
    character['completed_quests'].append(quest_id)
    character['experience'] += quest.get('reward_xp', 0)
    character['gold'] += quest.get('reward_gold', 0)

    return {"reward_xp": quest.get('reward_xp', 0), "reward_gold": quest.get('reward_gold', 0)}


def abandon_quest(character, quest_id):
    """Remove a quest from active quests without completing it"""
    if quest_id not in character['active_quests']:
        raise QuestNotActiveError(f"Quest {quest_id} is not active.")
    character['active_quests'].remove(quest_id)
    return True


def get_active_quests(character, quest_data_dict):
    """Get full data for all active quests"""
    return [quest_data_dict[qid] for qid in character['active_quests'] if qid in quest_data_dict]


def get_completed_quests(character, quest_data_dict):
    """Get full data for all completed quests"""
    return [quest_data_dict[qid] for qid in character['completed_quests'] if qid in quest_data_dict]


def get_available_quests(character, quest_data_dict):
    """Get quests that character can currently accept"""
    available = []
    for qid, quest in quest_data_dict.items():
        if can_accept_quest(character, qid, quest_data_dict):
            available.append(quest)
    return available


# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    return quest_id in character['completed_quests']


def is_quest_active(character, quest_id):
    return quest_id in character['active_quests']


def can_accept_quest(character, quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        return False
    quest = quest_data_dict[quest_id]
    prereq = quest.get('prerequisite', 'NONE')
    return (
            character['level'] >= quest.get('required_level', 1) and
            (prereq == "NONE" or prereq in character['completed_quests']) and
            quest_id not in character['active_quests'] and
            quest_id not in character['completed_quests']
    )


def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    if quest_id not in quest_data_dict:
        raise QuestNotFoundError(f"Quest {quest_id} not found.")
    chain = []
    current = quest_id
    while current != "NONE":
        if current not in quest_data_dict:
            raise QuestNotFoundError(f"Prerequisite {current} not found.")
        chain.insert(0, current)
        current = quest_data_dict[current].get('prerequisite', 'NONE')
    return chain


# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    total = len(quest_data_dict)
    completed = len(character['completed_quests'])
    if total == 0:
        return 0.0
    return (completed / total) * 100


def get_total_quest_rewards_earned(character, quest_data_dict):
    total_xp = sum(
        quest_data_dict[qid].get('reward_xp', 0) for qid in character['completed_quests'] if qid in quest_data_dict)
    total_gold = sum(
        quest_data_dict[qid].get('reward_gold', 0) for qid in character['completed_quests'] if qid in quest_data_dict)
    return {"total_xp": total_xp, "total_gold": total_gold}


def get_quests_by_level(quest_data_dict, min_level, max_level):
    return [quest for quest in quest_data_dict.values() if min_level <= quest.get('required_level', 1) <= max_level]


# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    print(f"Rewards: XP={quest_data.get('reward_xp', 0)}, Gold={quest_data.get('reward_gold', 0)}")
    print(f"Required Level: {quest_data.get('required_level', 1)}")
    print(f"Prerequisite: {quest_data.get('prerequisite', 'NONE')}")


def display_quest_list(quest_list):
    for quest in quest_list:
        print(
            f"- {quest['title']} (Level {quest.get('required_level', 1)}): XP={quest.get('reward_xp', 0)}, Gold={quest.get('reward_gold', 0)}")


def display_character_quest_progress(character, quest_data_dict):
    active = len(character['active_quests'])
    completed = len(character['completed_quests'])
    percent = get_quest_completion_percentage(character, quest_data_dict)
    rewards = get_total_quest_rewards_earned(character, quest_data_dict)
    print(f"\nQuest Progress for {character['name']}:")
    print(f"Active Quests: {active}")
    print(f"Completed Quests: {completed}")
    print(f"Completion Percentage: {percent:.2f}%")
    print(f"Total Rewards Earned: XP={rewards['total_xp']}, Gold={rewards['total_gold']}")


# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    for qid, quest in quest_data_dict.items():
        prereq = quest.get('prerequisite', 'NONE')
        if prereq != "NONE" and prereq not in quest_data_dict:
            raise QuestNotFoundError(f"Quest {qid} has invalid prerequisite {prereq}.")
    return True

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }

    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }

    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

