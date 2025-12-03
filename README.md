[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/wnCpjX4n)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=21879122&assignment_repo_type=AssignmentRepo)
### COMP 163: Project 3 - Quest Chronicles

# DESCRIPTION

This project is a text-based RPG game. Players create a character, complete quests, fight enemies, and manage items. The game is organized into separate modules for character, combat, inventory, quests, and game data.

# MODULE ORGANIZATION

# character_manager.py
  Handles character creation, loading, saving, and leveling. Manages character stats and revival after death.
  
# combat_system.py
  Handles combat mechanics, including generating enemies, turn-based battle logic, and outcomes (win, loss, escape).
  
# custom_exceptions.py
  Defines all game-specific exceptions such as inventory errors, quest errors, combat errors, and invalid operations. These make error handling clearer and prevent crashes.
  
# game_data.py
  Loads and stores game data such as items and quests from files. Handles missing or corrupted data by generating defaults.
  
# inventory_system.py
  Manages inventory, item usage, equipping weapons/armor, purchasing, and selling items. Supports inventory limits and consumable effects.
  
# quest_handler.py
  Handles quests: accepting, completing, abandoning, checking prerequisites, tracking progress, and displaying quests.
  
# main_game.py
  Integrates all modules. Runs the main menu, game loop, and in-game menus. Handles exploration, shop interactions, and player actions.
  
# EXCEPTION STRATEGY

InventoryFullError – Raised when the player tries to add an item but their inventory is full.

ItemNotFoundError – Raised when the player tries to use, equip, sell, or remove an item they don’t have.

InsufficientResourcesError – Raised when the player doesn’t have enough gold to buy an item or revive a character.

InvalidItemTypeError – Raised when the player tries to use or equip an item in a way that doesn’t match its type (like using a weapon as a potion).

QuestNotFoundError – Raised when a quest ID doesn’t exist in the game data.

QuestRequirementsNotMetError – Raised when the player tries to accept a quest but hasn’t completed the prerequisite quest.

QuestAlreadyCompletedError – Raised when the player tries to accept a quest they already finished.

QuestNotActiveError – Raised when the player tries to complete or abandon a quest that isn’t active.

InsufficientLevelError – Raised when the player’s level is too low to accept a quest.

CharacterNotFoundError – Raised when trying to load a saved character that doesn’t exist.

SaveFileCorruptedError – Raised if a saved character file is broken or unreadable.

CharacterDeadError – Raised during combat if the player character dies.

CombatNotActiveError – Raised if combat actions are attempted outside an active battle.

MissingDataFileError – Raised if required game data files are missing.

InvalidDataFormatError – Raised if game data files are in the wrong format.

# DESIGN CHOICES

The game is split into different modules so each part is easy to understand and change. A global game state keeps track of the current character, items, and quests. Custom exceptions show clear errors, like when the inventory is full or a quest is missing. Items and quests are stored in files so they can be updated without changing the code. Different item types are handled separately to make inventory management easier. Helper functions reduce repeated code, and text menus let the play

# AI USAGE

I used ChatGPT for debugging assistance for module integration and exception handling.

# HOW TO PLAY

python main.py
