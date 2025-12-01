"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *
import sys

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice in ['1', '2', '3']:
            return int(choice)
        print("Invalid input. Please enter 1, 2, or 3.")

def new_game():
    global current_character
    print("\n=== NEW GAME ===")
    name = input("Enter your character's name: ")
    print("Select class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Cleric")
    class_map = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue', '4': 'Cleric'}
    while True:
        class_choice = input("Enter class number (1-4): ")
        if class_choice in class_map:
            char_class = class_map[class_choice]
            break
        print("Invalid choice.")
    try:
        current_character = character_manager.create_character(name, char_class)
        print(f"Character '{name}' the {char_class} created successfully!")
        game_loop()
    except InvalidCharacterClassError as e:
        print(f"Error: {e}")

def load_game():
    global current_character
    print("\n=== LOAD GAME ===")
    saved = character_manager.list_saved_characters()
    if not saved:
        print("No saved characters found.")
        return
    print("Saved characters:")
    for i, char_name in enumerate(saved, 1):
        print(f"{i}. {char_name}")
    while True:
        choice = input(f"Select a character (1-{len(saved)}): ")
        if choice.isdigit() and 1 <= int(choice) <= len(saved):
            idx = int(choice) - 1
            break
        print("Invalid choice.")
    try:
        current_character = character_manager.load_character(saved[idx])
        print(f"Loaded character '{current_character['name']}' successfully!")
        game_loop()
    except (CharacterNotFoundError, SaveFileCorruptedError) as e:
        print(f"Error loading character: {e}")

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    global game_running
    game_running = True
    while game_running:
        choice = game_menu()
        if choice == 1:
            view_character_stats()
        elif choice == 2:
            view_inventory()
        elif choice == 3:
            quest_menu()
        elif choice == 4:
            explore()
        elif choice == 5:
            shop()
        elif choice == 6:
            save_game()
            print("Game saved. Exiting...")
            break
        else:
            print("Invalid choice.")

def game_menu():
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    while True:
        choice = input("Choose an action (1-6): ")
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return int(choice)
        print("Invalid input. Enter 1-6.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    global current_character
    character_manager.display_character_stats(current_character)
    quest_handler.display_character_quest_progress(current_character, all_quests)

def view_inventory():
    global current_character, all_items
    inventory_system.display_inventory(current_character, all_items)
    # Inventory actions could be added here (use/equip/drop)

def quest_menu():
    global current_character, all_quests
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest")
        print("7. Back")
        choice = input("Choose an option (1-7): ")
        if choice == '1':
            active = quest_handler.get_active_quests(current_character, all_quests)
            quest_handler.display_quest_list(active)
        elif choice == '2':
            available = quest_handler.get_available_quests(current_character, all_quests)
            quest_handler.display_quest_list(available)
        elif choice == '3':
            completed = quest_handler.get_completed_quests(current_character, all_quests)
            quest_handler.display_quest_list(completed)
        elif choice == '4':
            quest_id = input("Enter quest ID to accept: ")
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' accepted!")
            except (QuestNotFoundError, InsufficientLevelError,
                    QuestRequirementsNotMetError, QuestAlreadyCompletedError) as e:
                print(f"Cannot accept quest: {e}")
        elif choice == '5':
            quest_id = input("Enter quest ID to abandon: ")
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                print(f"Quest '{quest_id}' abandoned.")
            except QuestNotActiveError as e:
                print(f"Cannot abandon quest: {e}")
        elif choice == '6':
            quest_id = input("Enter quest ID to complete: ")
            try:
                rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
                print(f"Quest '{quest_id}' completed! Rewards: XP={rewards['reward_xp']}, Gold={rewards['reward_gold']}")
            except (QuestNotFoundError, QuestNotActiveError) as e:
                print(f"Cannot complete quest: {e}")
        elif choice == '7':
            break
        else:
            print("Invalid input.")

def explore():
    global current_character
    enemy = combat_system.get_random_enemy_for_level(current_character.get('level', 1))
    print(f"\nYou encountered a {enemy['name']}!")
    battle = combat_system.SimpleBattle(current_character, enemy)
    try:
        results = battle.start_battle()
        print(f"Battle ended. Winner: {results['winner']}")
        if results['winner'] == 'player':
            current_character['experience'] += results.get('xp_gained', 0)
            current_character['gold'] += results.get('gold_gained', 0)
        else:
            handle_character_death()
    except CharacterDeadError:
        handle_character_death()

def shop():
    global current_character, all_items
    print("\n=== SHOP ===")
    print(f"Your Gold: {current_character['gold']}")
    print("Available items for purchase:")
    for item_id, item in all_items.items():
        print(f"{item_id}: {item['name']} - Cost: {item.get('cost', 0)}")
    print("Shop menu not fully implemented yet.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    global current_character
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully!")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game_data():
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except MissingDataFileError:
        print("Data files missing. Creating defaults...")
        game_data.create_default_data_files()
        all_quests = game_data.load_quests()
        all_items = game_data.load_items()
    except InvalidDataFormatError as e:
        print(f"Invalid data format: {e}")
        sys.exit(1)

def handle_character_death():
    global current_character, game_running
    print("\nYour character has died!")
    choice = input("Revive for 50 gold? (y/n): ").lower()
    if choice == 'y':
        try:
            character_manager.revive_character(current_character, cost=50)
            print("You have been revived!")
        except InsufficientResourcesError:
            print("Not enough gold to revive. Game over.")
            game_running = False
    else:
        print("Game over.")
        game_running = False

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

