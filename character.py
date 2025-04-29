"""
Character classes for 'The Line: A Border Journey'

This module defines the character classes used in the game,
including the base Character class and specialized character types.
"""

import random


class Character:
    """Base character class for all game characters."""
    
    def __init__(self, name, description, health=100):
        """Initialize a character with basic attributes.
        
        Args:
            name (str): Character's name
            description (str): Brief description of the character
            health (int): Character's health points (default: 100)
        """
        self.name = name
        self.description = description
        self.health = health
        self.inventory = []
        self.location = None
        self.story_flags = {}
    
    def describe(self):
        """Return a description of the character."""
        return f"{self.name}: {self.description}"
    
    def add_to_inventory(self, item):
        """Add an item to the character's inventory."""
        self.inventory.append(item)
        return f"{self.name} acquired {item}."
    
    def remove_from_inventory(self, item):
        """Remove an item from the character's inventory if present."""
        if item in self.inventory:
            self.inventory.remove(item)
            return f"{self.name} no longer has {item}."
        return f"{self.name} doesn't have {item}."
    
    def set_flag(self, flag_name, value):
        """Set a story flag for this character."""
        self.story_flags[flag_name] = value
    
    def has_flag(self, flag_name):
        """Check if a story flag exists and is True."""
        return self.story_flags.get(flag_name, False)


class Migrant(Character):
    """Class representing a migrant character."""
    
    def __init__(self, name, description, origin, motivation, health=100):
        """Initialize a migrant character.
        
        Args:
            name (str): Character's name
            description (str): Brief description of the character
            origin (str): Character's place of origin
            motivation (str): Reason for migration
            health (int): Character's health points (default: 100)
        """
        super().__init__(name, description, health)
        self.origin = origin
        self.motivation = motivation
        self.water = 100  # Water level (0-100)
        self.food = 100   # Food level (0-100)
        self.hope = 100   # Hope level (0-100)
        self.money = 100  # Starting money
        self.family_ties = []  # List of family members
        
    def describe(self):
        """Return a detailed description of the migrant."""
        base_desc = super().describe()
        return f"{base_desc}\nOrigin: {self.origin}\nMotivation: {self.motivation}"
    
    def consume_resources(self, water_amount=5, food_amount=5):
        """Consume water and food resources."""
        self.water = max(0, self.water - water_amount)
        self.food = max(0, self.food - food_amount)
        
        # Health decreases more severely when resources are low
        health_loss = 0
        if self.water <= 0:
            health_loss += 20  # Increased from 10 to 20 for severe dehydration
        elif self.water < 20:
            health_loss += 5   # Moderate dehydration damage
            
        if self.food <= 0:
            health_loss += 8   # Starvation damage
        elif self.food < 20:
            health_loss += 3   # Hunger damage
            
        self.health = max(0, self.health - health_loss)
        
        status = []
        if self.water <= 0:
            status.append("severely dehydrated")
        elif self.water < 20:
            status.append("thirsty")
            
        if self.food <= 0:
            status.append("starving")
        elif self.food < 20:
            status.append("hungry")
            
        if not status:
            return f"{self.name} is doing well."
        return f"{self.name} is {' and '.join(status)}."
    
    def change_hope(self, amount):
        """Change the character's hope level."""
        self.hope = max(0, min(100, self.hope + amount))
        
        if amount > 0:
            return f"{self.name} feels more hopeful."
        elif amount < 0:
            return f"{self.name} feels more discouraged."
        return f"{self.name}'s resolve remains unchanged."
    
    def add_family_tie(self, name, relationship):
        """Add a family member with their relationship."""
        self.family_ties.append({"name": name, "relationship": relationship})


class BorderPatrol(Character):
    """Class representing a border patrol agent."""
    
    def __init__(self, name, description, years_of_service=0, health=100):
        """Initialize a border patrol agent character.
        
        Args:
            name (str): Character's name
            description (str): Brief description of the character
            years_of_service (int): Years served in border patrol
            health (int): Character's health points (default: 100)
        """
        super().__init__(name, description, health)
        self.years_of_service = years_of_service
        self.moral_compass = 50  # Scale from 0 (corrupt) to 100 (strictly moral)
        self.stress = 0  # Stress level from 0 to 100
        self.encounters = 0  # Number of migrant encounters
        self.money = 200 # Border patrol money
        self.water = 100
        self.food = 100
        
    def describe(self):
        """Return a detailed description of the agent."""
        base_desc = super().describe()
        return f"{base_desc}\nYears of Service: {self.years_of_service}"
    
    def encounter_migrant(self, migrant, action="detain"):
        """Handle an encounter with a migrant.
        
        Args:
            migrant (Migrant): The migrant character encountered
            action (str): The action taken ("detain", "help", "ignore")
            
        Returns:
            str: Description of what happened
        """
        self.encounters += 1
        self.stress += random.randint(1, 10)
        
        # Cap stress at 100
        self.stress = min(100, self.stress)
        
        # Different actions affect moral compass
        if action == "detain":
            # Standard procedure, slight moral impact based on migrant condition
            if migrant.health < 30 or migrant.water < 20:
                self.moral_compass -= 5
                return f"{self.name} detained {migrant.name}, who was in poor condition. This weighs on {self.name}'s conscience."
            return f"{self.name} detained {migrant.name} according to protocol."
            
        elif action == "help":
            # Helping improves moral compass but may violate protocol
            self.moral_compass += 10
            return f"{self.name} chose to help {migrant.name}, providing water and medical attention before processing."
            
        elif action == "ignore":
            # Ignoring duty decreases moral compass
            self.moral_compass -= 15
            return f"{self.name} chose to look the other way, allowing {migrant.name} to continue undetained."
            
        return f"{self.name} encountered {migrant.name}."
    
    def process_stress(self):
        """Process the effects of accumulated stress."""
        if self.stress > 80:
            self.health -= 5
            return f"{self.name} is experiencing severe burnout and health issues from job stress."
        elif self.stress > 60:
            return f"{self.name} is having trouble sleeping due to job-related stress."
        elif self.stress > 40:
            return f"{self.name} occasionally thinks about work during off hours."
        return f"{self.name} is managing work stress well."
    
    # In character.py - BorderPatrol class
    def consume_resources(self, water_amount=3, food_amount=3):
        """Consume water and food resources (slower than migrants)."""
        self.water = max(0, self.water - water_amount)
        self.food = max(0, self.food - food_amount)
        
        # Health decreases when resources are low
        health_loss = 0
        if self.water <= 0:
            health_loss += 5  # Less severe than migrants
        elif self.water < 20:
            health_loss += 2
            
        if self.food <= 0:
            health_loss += 4
        elif self.food < 20:
            health_loss += 1
            
        self.health = max(0, self.health - health_loss)
        
        status = []
        if self.water <= 0:
            status.append("severely dehydrated")
        elif self.water < 20:
            status.append("thirsty")
            
        if self.food <= 0:
            status.append("starving")
        elif self.food < 20:
            status.append("hungry")
            
        if not status:
            return f"{self.name} is doing well."
        return f"{self.name} is {' and '.join(status)}."