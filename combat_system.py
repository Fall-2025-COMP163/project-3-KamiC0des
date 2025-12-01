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
    """Create an enemy based on type"""
    enemies = {
        "goblin": {"health": 50, "strength": 8, "magic": 2, "xp_reward": 25, "gold_reward": 10},
        "orc": {"health": 80, "strength": 12, "magic": 5, "xp_reward": 50, "gold_reward": 25},
        "dragon": {"health": 200, "strength": 25, "magic": 15, "xp_reward": 200, "gold_reward": 100},
    }
    if enemy_type not in enemies:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    data = enemies[enemy_type]
    return {
        "name": enemy_type,
        "health": data["health"],
        "max_health": data["health"],
        "strength": data["strength"],
        "magic": data["magic"],
        "xp_reward": data["xp_reward"],
        "gold_reward": data["gold_reward"],
    }


def get_random_enemy_for_level(character_level):
    """Get an appropriate enemy for character's level"""
    if character_level <= 2:
        enemy_type = "goblin"
    elif 3 <= character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"
    return create_enemy(enemy_type)


# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """Simple turn-based combat system"""

    def __init__(self, character, enemy):
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn = 1

    def start_battle(self):
        """Start the combat loop"""
        if self.character['health'] <= 0:
            raise CharacterDeadError("Character is already dead.")
        while self.combat_active:
            self.player_turn()
            if not self.combat_active:
                break
            self.enemy_turn()
        winner = self.check_battle_end()
        rewards = {"xp_gained": 0, "gold_gained": 0}
        if winner == "player":
            rewards["xp_gained"] = self.enemy["xp_reward"]
            rewards["gold_gained"] = self.enemy["gold_reward"]
        return {"winner": winner, "xp_gained": rewards["xp_gained"], "gold_gained": rewards["gold_gained"]}

    def player_turn(self):
        """Handle player's turn"""
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        # Placeholder: always basic attack
        damage = self.calculate_damage(self.character, self.enemy)
        self.apply_damage(self.enemy, damage)
        display_battle_log(f"{self.character['name']} attacks {self.enemy['name']} for {damage} damage.")

    def enemy_turn(self):
        """Handle enemy's turn - simple AI"""
        if not self.combat_active:
            raise CombatNotActiveError("Combat is not active.")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"{self.enemy['name']} attacks {self.character['name']} for {damage} damage.")

    def calculate_damage(self, attacker, defender):
        """Calculate damage from attack"""
        damage = attacker['strength'] - (defender['strength'] // 4)
        return max(damage, 1)

    def apply_damage(self, target, damage):
        """Apply damage to a character or enemy"""
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0

    def check_battle_end(self):
        """Check if battle is over"""
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return "player"
        elif self.character['health'] <= 0:
            self.combat_active = False
            return "enemy"
        return None

    def attempt_escape(self):
        """Try to escape from battle"""
        if random.randint(0, 1) == 1:
            self.combat_active = False
            display_battle_log(f"{self.character['name']} escaped successfully!")
            return True
        else:
            display_battle_log(f"{self.character['name']} failed to escape.")
            return False


# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """Use character's class-specific special ability"""
    if 'last_ability_turn' in character and character.get('turn_counter', 0) - character['last_ability_turn'] < 1:
        raise AbilityOnCooldownError("Ability is on cooldown.")

    ability_class = character.get("class")
    if ability_class == "Warrior":
        return warrior_power_strike(character, enemy)
    elif ability_class == "Mage":
        return mage_fireball(character, enemy)
    elif ability_class == "Rogue":
        return rogue_critical_strike(character, enemy)
    elif ability_class == "Cleric":
        return cleric_heal(character)
    else:
        raise InvalidTargetError(f"No special ability for class: {ability_class}")


def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character['strength'] * 2
    SimpleBattle(character, enemy).apply_damage(enemy, damage)
    return f"{character['name']} uses Power Strike for {damage} damage!"


def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character['magic'] * 2
    SimpleBattle(character, enemy).apply_damage(enemy, damage)
    return f"{character['name']} casts Fireball for {damage} damage!"


def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        damage = character['strength'] * 3
        SimpleBattle(character, enemy).apply_damage(enemy, damage)
        return f"{character['name']} lands Critical Strike for {damage} damage!"
    else:
        damage = character['strength']
        SimpleBattle(character, enemy).apply_damage(enemy, damage)
        return f"{character['name']}'s Critical Strike missed! Deals {damage} damage instead."


def cleric_heal(character):
    """Cleric special ability"""
    heal_amount = 30
    character['health'] += heal_amount
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    return f"{character['name']} heals for {heal_amount} HP!"


# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """Check if character is in condition to fight"""
    return character['health'] > 0 and not character.get('in_battle', False)


def get_victory_rewards(enemy):
    """Calculate rewards for defeating enemy"""
    return {"xp": enemy["xp_reward"], "gold": enemy["gold_reward"]}


def display_combat_stats(character, enemy):
    """Display current combat status"""
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")


def display_battle_log(message):
    """Display a formatted battle message"""
    print(f">>> {message}")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
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
