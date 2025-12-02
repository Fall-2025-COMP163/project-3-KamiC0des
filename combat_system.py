"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)
import random


# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type

    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    if enemy_type.lower() == "goblin":
        enemy = {
            'name': 'Goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        }
    elif enemy_type.lower() == "orc":
        enemy = {
            'name': 'Orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        }
    elif enemy_type.lower() == "dragon":
        enemy = {
            'name': 'Dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    else:
        # Raise error if the enemy type is not recognized
        raise InvalidTargetError(f"Enemy type '{enemy_type}' is invalid.")

    # Return the created enemy dictionary
    return enemy


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level

    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons

    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"

    # Create and return enemy using create_enemy()
    return create_enemy(enemy_type)


# ============================================================================
# COMBAT SYSTEM
# ============================================================================


class SimpleBattle:
    """
    Simple turn-based combat system
    """

    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        self.character = character  # Store reference to player's character
        self.enemy = enemy  # Store reference to enemy
        self.combat_active = True  # Flag to track if battle is ongoing
        self.turn_counter = 0  # Count turns to manage abilities or AI
        # NOTE: We no longer initialize special_cooldown here; handled in use_special_ability()

    def start_battle(self):
        """
        Start the combat loop

        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy'|'escaped', 'xp_gained': int, 'gold_gained': int}

        Raises: CharacterDeadError if character is already dead

        Important: This function DOES NOT mutate the character's experience/gold.
        It returns rewards so the caller (or character manager) can apply them.
        This keeps data flow explicit and avoids duplication in integration tests.
        """
        # TODO: Implement battle loop
        if self.character.get('health', 0) <= 0:
            raise CharacterDeadError("Character is already dead!")

        # Battle loop continues until someone dies or player escapes
        while self.combat_active:
            self.player_turn()  # Player acts first
            if not self.combat_active:  # Could have escaped
                break
            winner = self.check_battle_end()
            if winner:
                break
            self.enemy_turn()  # Enemy acts next
            winner = self.check_battle_end()
            if winner:
                break
            self.turn_counter += 1  # Increment turn counter

        # Determine outcome and return rewards (do not apply to character here)
        winner = self.check_battle_end()
        if winner == 'player':
            rewards = get_victory_rewards(self.enemy)
            # Return rewards but DO NOT mutate character['experience'] or character['gold']
            return {'winner': 'player', 'xp_gained': rewards['xp'], 'gold_gained': rewards['gold']}
        elif winner == 'enemy':
            return {'winner': 'enemy', 'xp_gained': 0, 'gold_gained': 0}
        else:
            return {'winner': 'escaped', 'xp_gained': 0, 'gold_gained': 0}

    def player_turn(self):
        """
        Handle player's turn

        For deterministic testing we default to 'attack'. In a real game this
        would be replaced with player input or an AI decision.
        """
        # TODO: Implement player turn
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take a turn, combat is not active.")

        display_combat_stats(self.character, self.enemy)

        # For deterministic integration tests, choose 'attack' by default
        action = 'attack'  # Replace with player input in a real game

        if action == 'attack':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {damage} damage!")
        elif action == 'special':
            # special ability may raise AbilityOnCooldownError
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif action == 'run':
            if self.attempt_escape():
                display_battle_log(f"{self.character['name']} successfully escaped!")
            else:
                display_battle_log(f"{self.character['name']} failed to escape.")

        # Decrement special cooldown at end of turn if present
        # TODO: Note: cooldown bookkeeping is optional; we keep it consistent if present.
        if self.character.get('special_cooldown', 0) > 0:
            # Explain: we reduce cooldown once per player turn; using get avoids KeyError
            self.character['special_cooldown'] -= 1

    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI

        Enemy always attacks. This is intentionally simple to keep integration deterministic.
        """
        # TODO: Implement enemy turn
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take a turn, combat is not active.")

        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage!")

    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack

        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1

        Returns: Integer damage amount

        Explanation comment: integer division (//) is used for predictable, test-friendly
        reduction. We always clamp to at least 1 so even weak attacks do damage.
        """
        # TODO: Implement damage calculation
        # Formula: attacker's strength minus 1/4 of defender's strength
        attacker_str = attacker.get('strength', 0)
        defender_str = defender.get('strength', 0)
        damage = attacker_str - (defender_str // 4)
        return max(1, damage)  # Minimum damage is always 1

    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy

        Reduces health, prevents negative health.
        """
        # TODO: Implement damage application
        # Use get to avoid KeyError if target missing fields in tests
        current = target.get('health', 0)
        new_hp = max(0, current - damage)
        target['health'] = new_hp  # Put new HP back in target dict

    def check_battle_end(self):
        """
        Check if battle is over

        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy.get('health', 0) <= 0:
            self.combat_active = False
            return 'player'
        elif self.character.get('health', 0) <= 0:
            self.combat_active = False
            return 'enemy'
        return None

    def attempt_escape(self, force_success=None):
        """
        Try to escape from battle

        Accepts optional force_success for tests to simulate guaranteed escape.
        50% success chance by default.

        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        if force_success is not None:
            success = force_success
        else:
            success = random.random() < 0.5  # 50% chance
        if success:
            self.combat_active = False
        return success


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================


def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability

    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)

    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities

    # Initialize cooldown if not yet set
    if 'special_cooldown' not in character:
        character['special_cooldown'] = 0

    # Check if ability is on cooldown
    if character['special_cooldown'] > 0:
        raise AbilityOnCooldownError("Special ability is on cooldown")

    char_class = character.get('class', '').lower()
    if char_class == 'warrior':
        result = warrior_power_strike(character, enemy)
    elif char_class == 'mage':
        result = mage_fireball(character, enemy)
    elif char_class == 'rogue':
        result = rogue_critical_strike(character, enemy)
    elif char_class == 'cleric':
        result = cleric_heal(character)
    else:
        result = f"{character.get('name', 'Unknown')} has no special ability."

    # Set cooldown after using ability (kept simple; tests expect predictable behavior)
    character['special_cooldown'] = 3  # Example: 3 turns
    return result


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    damage = character.get('strength', 0) * 2
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return f"{character['name']} uses Power Strike on {enemy['name']} for {damage} damage!"


def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    damage = character.get('magic', 0) * 2
    enemy['health'] = max(0, enemy.get('health', 0) - damage)
    return f"{character['name']} casts Fireball on {enemy['name']} for {damage} damage!"


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    if random.random() < 0.5:  # 50% chance
        damage = character.get('strength', 0) * 3
        enemy['health'] = max(0, enemy.get('health', 0) - damage)
        return f"{character['name']} lands a Critical Strike on {enemy['name']} for {damage} damage!"
    else:
        damage = character.get('strength', 0)
        enemy['health'] = max(0, enemy.get('health', 0) - damage)
        return f"{character['name']} attacks normally for {damage} damage."


def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    heal_amount = 30
    character['health'] = min(character.get('max_health', character.get('health', 0)),
                              character.get('health', 0) + heal_amount)
    return f"{character['name']} heals for {heal_amount} HP!"


# ============================================================================
# COMBAT UTILITIES
# ============================================================================


def can_character_fight(character):
    """
    Check if character is in condition to fight

    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    return character.get('health', 0) > 0  # Simple check, could add battle flag


def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy

    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    # Use keys consistent with the rest of the project: 'xp' (returned) but calling code
    # should apply to 'experience' via character_manager.gain_experience()
    return {'xp': enemy.get('xp_reward', 0), 'gold': enemy.get('gold_reward', 0)}


def display_combat_stats(character, enemy):
    """
    Display current combat status
    """
    # TODO: Implement status display
    # Defensive .get used to avoid KeyErrors in tests that pass simplified dicts
    print(f"\n{character.get('name', 'Player')}: HP={character.get('health', 0)}/{character.get('max_health', 0)}")
    print(f"{enemy.get('name', 'Enemy')}: HP={enemy.get('health', 0)}/{enemy.get('max_health', 0)}")


def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")


# ============================================================================
# TESTING
# ============================================================================


if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")

    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")

    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }

    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")
    except CombatNotActiveError:
        print("Combat is not active!")
    except AbilityOnCooldownError:
        print("Ability is on cooldown!")

