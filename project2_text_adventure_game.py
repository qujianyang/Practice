"""
Final Project 2: Text-Based Adventure Game
A comprehensive adventure game with OOP design, save/load functionality,
decorators for abilities, and regex-based command parsing.
"""

import json
import os
import random
import re
import time
from enum import Enum
from typing import Dict, List, Optional, Tuple
from functools import wraps

class Direction(Enum):
    """Movement directions"""
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"
    UP = "up"
    DOWN = "down"

class ItemType(Enum):
    """Item types in the game"""
    WEAPON = "weapon"
    ARMOR = "armor"
    POTION = "potion"
    KEY = "key"
    TREASURE = "treasure"
    FOOD = "food"
    TOOL = "tool"

class EnemyType(Enum):
    """Enemy types"""
    GOBLIN = "goblin"
    ORC = "orc"
    DRAGON = "dragon"
    SKELETON = "skeleton"
    WIZARD = "wizard"
    BANDIT = "bandit"

def cooldown(seconds):
    """Decorator to add cooldown to abilities"""
    def decorator(func):
        last_used = {}

        @wraps(func)
        def wrapper(self, *args, **kwargs):
            player_id = id(self)
            current_time = time.time()

            if player_id in last_used:
                time_passed = current_time - last_used[player_id]
                if time_passed < seconds:
                    remaining = seconds - time_passed
                    return f"⏱️ Ability on cooldown! Wait {remaining:.1f} more seconds."

            result = func(self, *args, **kwargs)
            last_used[player_id] = current_time
            return result

        wrapper.cooldown = seconds
        return wrapper
    return decorator

def requires_item(item_name):
    """Decorator to check if player has required item"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'inventory'):
                return "This action requires inventory access."

            has_item = any(item.name.lower() == item_name.lower()
                          for item in self.inventory)

            if not has_item:
                return f"You need '{item_name}' to use this ability!"

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

def level_required(min_level):
    """Decorator to check minimum level requirement"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not hasattr(self, 'level'):
                return "This action requires a leveled character."

            if self.level < min_level:
                return f"You need to be level {min_level} to use this ability! (Current: {self.level})"

            return func(self, *args, **kwargs)
        return wrapper
    return decorator

class GameObject:
    """Base class for all game objects"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

class Item(GameObject):
    """Represents an item in the game"""

    def __init__(self, name: str, description: str, item_type: ItemType,
                 value: int = 0, stats: Dict = None):
        super().__init__(name, description)
        self.item_type = item_type
        self.value = value
        self.stats = stats or {}
        self.is_equipable = item_type in [ItemType.WEAPON, ItemType.ARMOR]
        self.is_consumable = item_type in [ItemType.POTION, ItemType.FOOD]

    def use(self, player):
        """Use the item"""
        if self.item_type == ItemType.POTION:
            healing = self.stats.get('healing', 20)
            player.heal(healing)
            return f"You drink the {self.name} and restore {healing} HP!"
        elif self.item_type == ItemType.FOOD:
            energy = self.stats.get('energy', 10)
            player.energy = min(100, player.energy + energy)
            return f"You eat the {self.name} and gain {energy} energy!"
        else:
            return f"You can't use the {self.name} that way."

class Character(GameObject):
    """Base class for characters (players and NPCs)"""

    def __init__(self, name: str, description: str, health: int = 100,
                 attack: int = 10, defense: int = 5):
        super().__init__(name, description)
        self.max_health = health
        self.health = health
        self.base_attack = attack
        self.base_defense = defense
        self.inventory: List[Item] = []
        self.equipped_weapon: Optional[Item] = None
        self.equipped_armor: Optional[Item] = None

    @property
    def attack(self):
        """Calculate total attack including equipment"""
        total = self.base_attack
        if self.equipped_weapon:
            total += self.equipped_weapon.stats.get('attack', 0)
        return total

    @property
    def defense(self):
        """Calculate total defense including equipment"""
        total = self.base_defense
        if self.equipped_armor:
            total += self.equipped_armor.stats.get('defense', 0)
        return total

    def take_damage(self, damage: int):
        """Take damage after defense calculation"""
        actual_damage = max(1, damage - self.defense)
        self.health -= actual_damage
        return actual_damage

    def heal(self, amount: int):
        """Heal the character"""
        old_health = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - old_health

    def is_alive(self):
        """Check if character is alive"""
        return self.health > 0

class Enemy(Character):
    """Enemy character"""

    def __init__(self, enemy_type: EnemyType, level: int = 1):
        self.enemy_type = enemy_type
        self.level = level

        # Set stats based on enemy type and level
        stats = self._get_enemy_stats(enemy_type, level)

        super().__init__(
            name=stats['name'],
            description=stats['description'],
            health=stats['health'],
            attack=stats['attack'],
            defense=stats['defense']
        )

        self.experience_reward = stats['exp_reward']
        self.gold_reward = stats['gold_reward']
        self.loot_table = stats['loot_table']

    def _get_enemy_stats(self, enemy_type: EnemyType, level: int):
        """Get enemy stats based on type and level"""
        base_stats = {
            EnemyType.GOBLIN: {
                'name': 'Goblin',
                'description': 'A small, sneaky creature',
                'health': 30,
                'attack': 8,
                'defense': 2,
                'exp_reward': 10,
                'gold_reward': 5
            },
            EnemyType.ORC: {
                'name': 'Orc',
                'description': 'A brutish warrior',
                'health': 50,
                'attack': 12,
                'defense': 5,
                'exp_reward': 20,
                'gold_reward': 10
            },
            EnemyType.DRAGON: {
                'name': 'Dragon',
                'description': 'A mighty, fire-breathing beast',
                'health': 200,
                'attack': 25,
                'defense': 15,
                'exp_reward': 100,
                'gold_reward': 100
            },
            EnemyType.SKELETON: {
                'name': 'Skeleton',
                'description': 'An undead warrior',
                'health': 40,
                'attack': 10,
                'defense': 3,
                'exp_reward': 15,
                'gold_reward': 7
            },
            EnemyType.WIZARD: {
                'name': 'Dark Wizard',
                'description': 'A master of dark magic',
                'health': 60,
                'attack': 18,
                'defense': 8,
                'exp_reward': 30,
                'gold_reward': 20
            },
            EnemyType.BANDIT: {
                'name': 'Bandit',
                'description': 'A highway robber',
                'health': 45,
                'attack': 11,
                'defense': 4,
                'exp_reward': 17,
                'gold_reward': 15
            }
        }

        stats = base_stats.get(enemy_type, base_stats[EnemyType.GOBLIN]).copy()

        # Scale stats with level
        level_multiplier = 1 + (level - 1) * 0.2
        stats['health'] = int(stats['health'] * level_multiplier)
        stats['attack'] = int(stats['attack'] * level_multiplier)
        stats['defense'] = int(stats['defense'] * level_multiplier)
        stats['exp_reward'] = int(stats['exp_reward'] * level_multiplier)
        stats['gold_reward'] = int(stats['gold_reward'] * level_multiplier)

        stats['loot_table'] = self._generate_loot_table(enemy_type)

        return stats

    def _generate_loot_table(self, enemy_type: EnemyType):
        """Generate loot table for enemy"""
        common_loot = [
            Item("Health Potion", "Restores 20 HP", ItemType.POTION, 10, {'healing': 20}),
            Item("Bread", "Restores energy", ItemType.FOOD, 5, {'energy': 10})
        ]

        if enemy_type in [EnemyType.DRAGON, EnemyType.WIZARD]:
            return common_loot + [
                Item("Magic Sword", "A powerful enchanted blade", ItemType.WEAPON, 100, {'attack': 15}),
                Item("Dragon Scale Armor", "Armor made from dragon scales", ItemType.ARMOR, 150, {'defense': 12})
            ]
        else:
            return common_loot + [
                Item("Iron Sword", "A basic sword", ItemType.WEAPON, 30, {'attack': 5}),
                Item("Leather Armor", "Basic protection", ItemType.ARMOR, 25, {'defense': 3})
            ]

class Player(Character):
    """Player character with special abilities"""

    def __init__(self, name: str):
        super().__init__(
            name=name,
            description="The hero of this adventure",
            health=100,
            attack=10,
            defense=5
        )
        self.level = 1
        self.experience = 0
        self.gold = 0
        self.energy = 100
        self.skills = {
            'strength': 5,
            'agility': 5,
            'intelligence': 5
        }
        self.quest_flags = {}
        self.abilities_unlocked = []

    @cooldown(10)
    def power_strike(self, enemy: Enemy):
        """Special attack with cooldown"""
        damage = self.attack * 2
        actual_damage = enemy.take_damage(damage)
        self.energy -= 20
        return f"⚔️ Power Strike! Dealt {actual_damage} damage to {enemy.name}!"

    @level_required(3)
    def heal_spell(self):
        """Healing spell requiring level 3"""
        heal_amount = 30
        healed = self.heal(heal_amount)
        self.energy -= 15
        return f"✨ You cast Heal and restore {healed} HP!"

    @requires_item("Magic Staff")
    def fireball(self, enemy: Enemy):
        """Fireball spell requiring Magic Staff"""
        damage = self.intelligence * 3
        actual_damage = enemy.take_damage(damage)
        self.energy -= 25
        return f"🔥 Fireball! Dealt {actual_damage} damage to {enemy.name}!"

    def gain_experience(self, exp: int):
        """Gain experience and potentially level up"""
        self.experience += exp
        exp_needed = self.level * 50

        messages = [f"You gained {exp} experience!"]

        while self.experience >= exp_needed:
            self.experience -= exp_needed
            self.level += 1
            self.max_health += 10
            self.health = self.max_health
            self.base_attack += 2
            self.base_defense += 1

            messages.append(f"🎉 LEVEL UP! You are now level {self.level}!")

            # Unlock abilities
            if self.level == 3 and 'heal_spell' not in self.abilities_unlocked:
                self.abilities_unlocked.append('heal_spell')
                messages.append("New ability unlocked: Heal Spell!")

            exp_needed = self.level * 50

        return " ".join(messages)

    def add_item(self, item: Item):
        """Add item to inventory"""
        self.inventory.append(item)
        return f"You picked up: {item.name}"

    def equip_item(self, item_name: str):
        """Equip a weapon or armor"""
        for item in self.inventory:
            if item.name.lower() == item_name.lower():
                if item.item_type == ItemType.WEAPON:
                    old_weapon = self.equipped_weapon
                    self.equipped_weapon = item
                    if old_weapon:
                        return f"Equipped {item.name} (replaced {old_weapon.name})"
                    return f"Equipped {item.name}"
                elif item.item_type == ItemType.ARMOR:
                    old_armor = self.equipped_armor
                    self.equipped_armor = item
                    if old_armor:
                        return f"Equipped {item.name} (replaced {old_armor.name})"
                    return f"Equipped {item.name}"
                else:
                    return f"{item.name} cannot be equipped"

        return f"Item '{item_name}' not found in inventory"

class Room:
    """Represents a room in the game"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.exits: Dict[Direction, 'Room'] = {}
        self.items: List[Item] = []
        self.enemies: List[Enemy] = []
        self.npcs: List[Character] = []
        self.is_locked = False
        self.lock_message = "This door is locked."
        self.first_visit = True

    def add_exit(self, direction: Direction, room: 'Room', locked: bool = False):
        """Add an exit to another room"""
        self.exits[direction] = room
        if locked:
            self.is_locked = True

    def get_full_description(self):
        """Get complete room description"""
        desc = [f"\n📍 {self.name}"]
        desc.append(self.description)

        if self.exits:
            exits = ", ".join(d.value for d in self.exits.keys())
            desc.append(f"Exits: {exits}")

        if self.items:
            item_list = ", ".join(item.name for item in self.items)
            desc.append(f"Items: {item_list}")

        if self.enemies:
            enemy_list = ", ".join(enemy.name for enemy in self.enemies)
            desc.append(f"⚔️ Enemies: {enemy_list}")

        if self.npcs:
            npc_list = ", ".join(npc.name for npc in self.npcs)
            desc.append(f"👤 NPCs: {npc_list}")

        return "\n".join(desc)

class Game:
    """Main game engine"""

    def __init__(self):
        self.player: Optional[Player] = None
        self.current_room: Optional[Room] = None
        self.rooms: Dict[str, Room] = {}
        self.game_over = False
        self.commands = self._setup_commands()
        self.command_patterns = self._setup_command_patterns()
        self.save_file = "adventure_save.json"

    def _setup_commands(self):
        """Setup command handlers"""
        return {
            'look': self.cmd_look,
            'go': self.cmd_go,
            'take': self.cmd_take,
            'inventory': self.cmd_inventory,
            'use': self.cmd_use,
            'equip': self.cmd_equip,
            'attack': self.cmd_attack,
            'stats': self.cmd_stats,
            'help': self.cmd_help,
            'save': self.cmd_save,
            'load': self.cmd_load,
            'quit': self.cmd_quit
        }

    def _setup_command_patterns(self):
        """Setup regex patterns for command parsing"""
        return {
            r'^(go|move|walk|run)\s+(north|south|east|west|up|down)$': self.parse_movement,
            r'^(take|get|pick up|grab)\s+(.+)$': self.parse_take,
            r'^(use|consume|drink|eat)\s+(.+)$': self.parse_use,
            r'^(equip|wear|wield)\s+(.+)$': self.parse_equip,
            r'^(attack|fight|kill)\s+(.+)$': self.parse_attack,
            r'^(look|examine|inspect)(\s+(.+))?$': self.parse_look,
            r'^(talk|speak)\s+(?:to\s+)?(.+)$': self.parse_talk,
            r'^cast\s+(\w+)(?:\s+on\s+(.+))?$': self.parse_cast
        }

    def parse_command(self, command: str):
        """Parse user command using regex"""
        command = command.lower().strip()

        # Check exact commands first
        parts = command.split(maxsplit=1)
        if parts and parts[0] in self.commands:
            return self.commands[parts[0]](parts[1] if len(parts) > 1 else "")

        # Check regex patterns
        for pattern, handler in self.command_patterns.items():
            match = re.match(pattern, command, re.IGNORECASE)
            if match:
                return handler(match)

        return "I don't understand that command. Type 'help' for available commands."

    def parse_movement(self, match):
        """Parse movement commands"""
        direction = match.group(2).lower()
        return self.cmd_go(direction)

    def parse_take(self, match):
        """Parse take commands"""
        item = match.group(2)
        return self.cmd_take(item)

    def parse_use(self, match):
        """Parse use commands"""
        item = match.group(2)
        return self.cmd_use(item)

    def parse_equip(self, match):
        """Parse equip commands"""
        item = match.group(2)
        return self.cmd_equip(item)

    def parse_attack(self, match):
        """Parse attack commands"""
        target = match.group(2)
        return self.cmd_attack(target)

    def parse_look(self, match):
        """Parse look commands"""
        target = match.group(3) if match.group(3) else ""
        return self.cmd_look(target)

    def parse_talk(self, match):
        """Parse talk commands"""
        target = match.group(2)
        return self.cmd_talk(target)

    def parse_cast(self, match):
        """Parse spell casting commands"""
        spell = match.group(1).lower()
        target = match.group(2) if match.group(2) else None

        if spell == "heal":
            if hasattr(self.player, 'heal_spell'):
                return self.player.heal_spell()
        elif spell == "fireball" and target:
            for enemy in self.current_room.enemies:
                if enemy.name.lower() == target.lower():
                    return self.player.fireball(enemy)

        return f"You can't cast '{spell}'"

    def cmd_look(self, args):
        """Look around or at specific thing"""
        if not args:
            return self.current_room.get_full_description()

        # Look at item in room
        for item in self.current_room.items:
            if item.name.lower() == args.lower():
                return f"{item.name}: {item.description}"

        # Look at item in inventory
        for item in self.player.inventory:
            if item.name.lower() == args.lower():
                desc = [f"{item.name}: {item.description}"]
                if item.value:
                    desc.append(f"Value: {item.value} gold")
                if item.stats:
                    stats_str = ", ".join(f"{k}: {v}" for k, v in item.stats.items())
                    desc.append(f"Stats: {stats_str}")
                return "\n".join(desc)

        return f"You don't see '{args}' here."

    def cmd_go(self, args):
        """Move in a direction"""
        try:
            direction = Direction(args.lower())
        except ValueError:
            return f"'{args}' is not a valid direction."

        if direction not in self.current_room.exits:
            return "You can't go that way."

        next_room = self.current_room.exits[direction]

        if next_room.is_locked:
            # Check if player has a key
            has_key = any(item.item_type == ItemType.KEY for item in self.player.inventory)
            if has_key:
                next_room.is_locked = False
                self.current_room = next_room
                return f"You unlock the door with a key.\n{self.current_room.get_full_description()}"
            else:
                return next_room.lock_message

        self.current_room = next_room

        # Trigger first visit events
        if self.current_room.first_visit:
            self.current_room.first_visit = False
            if self.current_room.enemies:
                return f"⚠️ Enemies attack as you enter!\n{self.current_room.get_full_description()}"

        return self.current_room.get_full_description()

    def cmd_take(self, args):
        """Take an item"""
        if not args:
            return "Take what?"

        for item in self.current_room.items:
            if item.name.lower() == args.lower():
                self.current_room.items.remove(item)
                return self.player.add_item(item)

        return f"There's no '{args}' here."

    def cmd_inventory(self, args):
        """Show inventory"""
        if not self.player.inventory:
            return "Your inventory is empty."

        inv = ["Inventory:"]
        for item in self.player.inventory:
            status = ""
            if item == self.player.equipped_weapon:
                status = " [EQUIPPED - Weapon]"
            elif item == self.player.equipped_armor:
                status = " [EQUIPPED - Armor]"
            inv.append(f"  - {item.name} ({item.item_type.value}){status}")

        inv.append(f"\nGold: {self.player.gold}")
        return "\n".join(inv)

    def cmd_use(self, args):
        """Use an item"""
        if not args:
            return "Use what?"

        for item in self.player.inventory:
            if item.name.lower() == args.lower():
                if item.is_consumable:
                    result = item.use(self.player)
                    self.player.inventory.remove(item)
                    return result
                else:
                    return f"You can't use {item.name} like that."

        return f"You don't have '{args}'."

    def cmd_equip(self, args):
        """Equip an item"""
        if not args:
            return "Equip what?"

        return self.player.equip_item(args)

    def cmd_attack(self, args):
        """Attack an enemy"""
        if not args:
            if self.current_room.enemies:
                target = self.current_room.enemies[0]
            else:
                return "There's nothing to attack here."
        else:
            target = None
            for enemy in self.current_room.enemies:
                if enemy.name.lower() == args.lower():
                    target = enemy
                    break

            if not target:
                return f"There's no '{args}' to attack."

        # Player attacks
        damage = target.take_damage(self.player.attack)
        messages = [f"You attack {target.name} for {damage} damage!"]

        if not target.is_alive():
            self.current_room.enemies.remove(target)
            messages.append(f"💀 You defeated {target.name}!")

            # Gain rewards
            self.player.gold += target.gold_reward
            messages.append(f"You gained {target.gold_reward} gold!")
            messages.append(self.player.gain_experience(target.experience_reward))

            # Drop loot
            if random.random() < 0.5 and target.loot_table:
                loot = random.choice(target.loot_table)
                self.current_room.items.append(loot)
                messages.append(f"{target.name} dropped: {loot.name}")
        else:
            # Enemy counter-attacks
            damage = self.player.take_damage(target.attack)
            messages.append(f"{target.name} attacks you for {damage} damage!")
            messages.append(f"Your HP: {self.player.health}/{self.player.max_health}")

            if not self.player.is_alive():
                self.game_over = True
                messages.append("☠️ You have been defeated! Game Over!")

        return "\n".join(messages)

    def cmd_stats(self, args):
        """Show player stats"""
        stats = [
            f"{'='*30}",
            f"Name: {self.player.name}",
            f"Level: {self.player.level}",
            f"Experience: {self.player.experience}/{self.player.level * 50}",
            f"HP: {self.player.health}/{self.player.max_health}",
            f"Energy: {self.player.energy}/100",
            f"Gold: {self.player.gold}",
            f"",
            f"Attack: {self.player.attack} (Base: {self.player.base_attack})",
            f"Defense: {self.player.defense} (Base: {self.player.base_defense})",
            f"",
            f"Skills:",
            f"  Strength: {self.player.skills['strength']}",
            f"  Agility: {self.player.skills['agility']}",
            f"  Intelligence: {self.player.skills['intelligence']}",
            f"{'='*30}"
        ]

        if self.player.abilities_unlocked:
            stats.append("Abilities:")
            for ability in self.player.abilities_unlocked:
                stats.append(f"  - {ability.replace('_', ' ').title()}")

        return "\n".join(stats)

    def cmd_talk(self, target):
        """Talk to NPCs"""
        for npc in self.current_room.npcs:
            if npc.name.lower() == target.lower():
                # Simple dialogue system
                dialogues = {
                    "merchant": "I have many wares, if you have the gold!",
                    "elder": "Beware the dragon in the mountain!",
                    "guard": "Move along, citizen."
                }
                return f"{npc.name} says: '{dialogues.get(npc.name.lower(), 'Hello, adventurer!')}'"

        return f"There's no one named '{target}' here."

    def cmd_help(self, args):
        """Show help"""
        help_text = [
            "Available Commands:",
            "  Movement: go/move/walk <direction>",
            "  Interaction: look, take/get <item>, talk to <npc>",
            "  Inventory: inventory, use <item>, equip <item>",
            "  Combat: attack <enemy>, cast <spell>",
            "  System: stats, save, load, help, quit",
            "",
            "Directions: north, south, east, west, up, down",
            "",
            "Tips:",
            "  - Look around each room carefully",
            "  - Equip weapons and armor to increase stats",
            "  - Save your game frequently",
            "  - Some abilities unlock at higher levels"
        ]
        return "\n".join(help_text)

    def cmd_save(self, args):
        """Save game"""
        save_data = {
            'player': {
                'name': self.player.name,
                'level': self.player.level,
                'experience': self.player.experience,
                'health': self.player.health,
                'max_health': self.player.max_health,
                'energy': self.player.energy,
                'gold': self.player.gold,
                'skills': self.player.skills,
                'quest_flags': self.player.quest_flags,
                'abilities_unlocked': self.player.abilities_unlocked
            },
            'current_room': self.current_room.name,
            'inventory': [{'name': item.name, 'type': item.item_type.value}
                         for item in self.player.inventory],
            'equipped': {
                'weapon': self.player.equipped_weapon.name if self.player.equipped_weapon else None,
                'armor': self.player.equipped_armor.name if self.player.equipped_armor else None
            }
        }

        with open(self.save_file, 'w') as f:
            json.dump(save_data, f, indent=2)

        return f"Game saved to {self.save_file}"

    def cmd_load(self, args):
        """Load game"""
        if not os.path.exists(self.save_file):
            return "No save file found."

        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)

            # Restore player
            self.player = Player(save_data['player']['name'])
            for key, value in save_data['player'].items():
                if hasattr(self.player, key):
                    setattr(self.player, key, value)

            # Restore room
            self.current_room = self.rooms.get(save_data['current_room'])

            return f"Game loaded from {self.save_file}"

        except Exception as e:
            return f"Failed to load game: {e}"

    def cmd_quit(self, args):
        """Quit game"""
        confirm = input("Save before quitting? (y/n): ").lower()
        if confirm == 'y':
            self.cmd_save("")
        self.game_over = True
        return "Thanks for playing! Goodbye!"

    def setup_world(self):
        """Create the game world"""
        # Create rooms
        entrance = Room("Entrance Hall", "A grand entrance with marble floors.")
        corridor = Room("Dark Corridor", "A dimly lit corridor stretches ahead.")
        armory = Room("Armory", "Weapons line the walls of this room.")
        throne_room = Room("Throne Room", "A majestic throne dominates this chamber.")
        dungeon = Room("Dungeon", "A dank, dark dungeon filled with cells.")
        treasure_room = Room("Treasure Room", "Gold and jewels sparkle in the light!")

        # Connect rooms
        entrance.add_exit(Direction.NORTH, corridor)
        corridor.add_exit(Direction.SOUTH, entrance)
        corridor.add_exit(Direction.EAST, armory)
        corridor.add_exit(Direction.WEST, throne_room)
        corridor.add_exit(Direction.DOWN, dungeon)
        armory.add_exit(Direction.WEST, corridor)
        throne_room.add_exit(Direction.EAST, corridor)
        throne_room.add_exit(Direction.NORTH, treasure_room, locked=True)
        treasure_room.add_exit(Direction.SOUTH, throne_room)
        dungeon.add_exit(Direction.UP, corridor)

        # Add items
        entrance.items.append(
            Item("Health Potion", "Restores 20 HP", ItemType.POTION, 10, {'healing': 20})
        )
        armory.items.extend([
            Item("Iron Sword", "A sturdy iron blade", ItemType.WEAPON, 50, {'attack': 8}),
            Item("Leather Armor", "Basic leather protection", ItemType.ARMOR, 40, {'defense': 5}),
            Item("Magic Staff", "A staff crackling with energy", ItemType.WEAPON, 100, {'attack': 12})
        ])
        dungeon.items.append(
            Item("Dungeon Key", "An old rusty key", ItemType.KEY, 5)
        )
        treasure_room.items.extend([
            Item("Golden Crown", "A crown of pure gold", ItemType.TREASURE, 500),
            Item("Dragon Scale Armor", "Legendary armor", ItemType.ARMOR, 200, {'defense': 15})
        ])

        # Add enemies
        corridor.enemies.append(Enemy(EnemyType.GOBLIN, level=1))
        armory.enemies.append(Enemy(EnemyType.SKELETON, level=2))
        throne_room.enemies.append(Enemy(EnemyType.WIZARD, level=3))
        dungeon.enemies.extend([
            Enemy(EnemyType.SKELETON, level=1),
            Enemy(EnemyType.ORC, level=2)
        ])
        treasure_room.enemies.append(Enemy(EnemyType.DRAGON, level=5))

        # Add NPCs
        merchant = Character("Merchant", "A traveling merchant", 50, 0, 0)
        entrance.npcs.append(merchant)

        # Store rooms
        self.rooms = {
            'Entrance Hall': entrance,
            'Dark Corridor': corridor,
            'Armory': armory,
            'Throne Room': throne_room,
            'Dungeon': dungeon,
            'Treasure Room': treasure_room
        }

        # Set starting room
        self.current_room = entrance

    def run(self):
        """Main game loop"""
        print("\n" + "="*60)
        print("TEXT-BASED ADVENTURE GAME")
        print("="*60)

        # Character creation
        name = input("\nEnter your character name: ").strip() or "Hero"
        self.player = Player(name)

        print(f"\nWelcome, {name}!")
        print("Your adventure begins...")

        # Setup world
        self.setup_world()

        print(self.current_room.get_full_description())
        print("\nType 'help' for available commands.")

        # Game loop
        while not self.game_over:
            command = input("\n> ").strip()
            if command:
                result = self.parse_command(command)
                print(result)

                # Check game over conditions
                if not self.player.is_alive():
                    self.game_over = True
                    print("\n☠️ GAME OVER ☠️")

                # Check win condition
                golden_crown = any(item.name == "Golden Crown" for item in self.player.inventory)
                if golden_crown and self.current_room.name == "Entrance Hall":
                    print("\n🎉 VICTORY! 🎉")
                    print("You escaped with the Golden Crown!")
                    print(f"Final Score: {self.player.level * 1000 + self.player.gold}")
                    self.game_over = True

def demo_mode():
    """Run a demo of the game"""
    game = Game()

    # Setup demo player
    game.player = Player("Demo Hero")
    game.player.level = 3
    game.player.gold = 100
    game.player.abilities_unlocked = ['heal_spell']

    # Add some items to inventory
    game.player.add_item(
        Item("Demo Sword", "A demonstration weapon", ItemType.WEAPON, 50, {'attack': 10})
    )
    game.player.add_item(
        Item("Health Potion", "Restores HP", ItemType.POTION, 10, {'healing': 20})
    )

    # Setup world
    game.setup_world()

    print("\n" + "="*60)
    print("ADVENTURE GAME - DEMO MODE")
    print("="*60)

    # Simulate some commands
    demo_commands = [
        "look",
        "stats",
        "inventory",
        "go north",
        "attack goblin",
        "take health potion",
        "go east",
        "take iron sword",
        "equip iron sword",
        "stats"
    ]

    print("\nExecuting demo commands...")
    for cmd in demo_commands:
        print(f"\n> {cmd}")
        result = game.parse_command(cmd)
        print(result)

        if game.game_over:
            break

    print("\nDemo completed! Run the game normally to play.")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        demo_mode()
    else:
        game = Game()
        game.run()