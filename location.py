"""
Location classes for 'The Line: A Border Journey'

This module defines the locations and environments that characters
can navigate through in the game world.
"""

import random
from character import Migrant, BorderPatrol

class Location:
    """Base class for all game locations."""
    
    def __init__(self, name, description, danger_level=0):
        """Initialize a location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            danger_level (int): How dangerous the location is (0-10)
        """
        self.name = name
        self.description = description
        self.danger_level = danger_level
        self.characters = []  # Characters present at this location
        self.items = []       # Items available at this location
        self.connections = {} # Connected locations {direction: location}
        self.visited = False  # Whether player has visited this location
        self.events = []      # Possible events at this location
        
    def describe(self, detailed=False):
        """Return a description of the location."""
        base_desc = f"{self.name}: {self.description}"
        
        if not detailed:
            return base_desc
            
        # Add details about danger
        danger_desc = "\nDanger Level: "
        if self.danger_level <= 2:
            danger_desc += "Low - Relatively safe area."
        elif self.danger_level <= 5:
            danger_desc += "Medium - Exercise caution."
        elif self.danger_level <= 8:
            danger_desc += "High - Very dangerous area."
        else:
            danger_desc += "Extreme - Life-threatening conditions."
            
        # Add details about connections
        connections_desc = "\nPaths: "
        if self.connections:
            connections_desc += ", ".join([f"{direction} to {location.name}" 
                                         for direction, location in self.connections.items()])
        else:
            connections_desc += "No obvious paths from here."
            
        # Add details about characters present
        characters_desc = "\nPresent: "
        if self.characters:
            characters_desc += ", ".join([character.name for character in self.characters])
        else:
            characters_desc += "No one else is here."
            
        # Add details about items
        items_desc = "\nItems: "
        if self.items:
            items_desc += ", ".join(self.items)
        else:
            items_desc += "Nothing useful found here."
            
        return base_desc + danger_desc + connections_desc + characters_desc + items_desc
    
    def add_connection(self, direction, location):
        """Connect this location to another in the specified direction."""
        self.connections[direction] = location
        
    def add_character(self, character):
        """Add a character to this location."""
        self.characters.append(character)
        character.location = self
        
    def remove_character(self, character):
        """Remove a character from this location."""
        if character in self.characters:
            self.characters.remove(character)
            if character.location == self:
                character.location = None
                
    def add_item(self, item):
        """Add an item to this location."""
        self.items.append(item)
        
    def remove_item(self, item):
        """Remove an item from this location if present."""
        if item in self.items:
            self.items.remove(item)
            return True
        return False
    
    def add_event(self, event):
        """Add a possible event to this location."""
        self.events.append(event)
        
    def get_random_event(self):
        """Return a random event from this location, or None if no events."""
        if not self.events:
            return None
        return random.choice(self.events)


class Desert(Location):
    """A desert location with extreme conditions."""
    
    def __init__(self, name, description, water_scarcity=8, danger_level=7):
        """Initialize a desert location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            water_scarcity (int): How scarce water is (0-10)
            danger_level (int): How dangerous the location is (0-10)
        """
        super().__init__(name, description, danger_level)
        self.water_scarcity = water_scarcity
        
    def describe(self, detailed=False):
        """Return a description of the desert location."""
        base_desc = super().describe(detailed)
        
        if detailed:
            water_desc = "\nWater: "
            if self.water_scarcity >= 8:
                water_desc += "Critically scarce - No water sources visible."
            elif self.water_scarcity >= 5:
                water_desc += "Very limited - Might find small amounts if lucky."
            else:
                water_desc += "Limited - Some water sources may be found."
            return base_desc + water_desc
            
        return base_desc
    
    # location.py - Desert class modifications
    def apply_effects(self, character):
        effects = []
        
        # Common effects for all characters
        if hasattr(character, 'water'):
            if character.water < 30:
                effects.append("severely dehydrated")
            elif character.water < 50:
                effects.append("feeling thirsty")

        if self.danger_level > 5 and hasattr(character, 'health') and character.health < 50:
            effects.append("weakened by the harsh conditions")
        elif self.danger_level > 7:
            effects.append("struggling against the extreme heat")

        # Additional stress for Border Patrol
        if isinstance(character, BorderPatrol) and hasattr(character, 'stress'):
            character.stress = min(100, character.stress + 5)
            effects.append("stressed from desert conditions")

        if effects:
            return f"The desert is harsh. {character.name} is {' and '.join(effects)}."
        return f"{character.name} endures the challenging desert conditions."


class Border(Location):
    """A border location with patrol presence."""
    
    def __init__(self, name, description, patrol_intensity=5, danger_level=6):
        """Initialize a border location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            patrol_intensity (int): Level of border patrol presence (0-10)
            danger_level (int): How dangerous the location is (0-10)
        """
        super().__init__(name, description, danger_level)
        self.patrol_intensity = patrol_intensity
        
    def describe(self, detailed=False):
        """Return a description of the border location."""
        base_desc = super().describe(detailed)
        
        if detailed:
            patrol_desc = "\nPatrol: "
            if self.patrol_intensity >= 8:
                patrol_desc += "Heavy presence - Constant surveillance and patrols."
            elif self.patrol_intensity >= 5:
                patrol_desc += "Moderate presence - Regular patrols pass through."
            else:
                patrol_desc += "Light presence - Occasional patrols in the area."
            return base_desc + patrol_desc
            
        return base_desc
    
    def encounter_chance(self):
        """Return the chance (0-100) of encountering border patrol."""
        return self.patrol_intensity * 10


class Settlement(Location):
    """A settlement location with people and resources."""
    
    def __init__(self, name, description, population=0, danger_level=3):
        """Initialize a settlement location.
        
        Args:
            name (str): Name of the location
            description (str): Description of the location
            population (int): Approximate population of the settlement
            danger_level (int): How dangerous the location is (0-10)
        """
        super().__init__(name, description, danger_level)
        self.population = population
        self.services = []  # Available services ("food", "shelter", "medical")
        
    def describe(self, detailed=False):
        """Return a description of the settlement location."""
        base_desc = super().describe(detailed)
        
        if detailed:
            pop_desc = "\nPopulation: "
            if self.population > 10000:
                pop_desc += "Large community"
            elif self.population > 1000:
                pop_desc += "Medium-sized community"
            elif self.population > 100:
                pop_desc += "Small community"
            else:
                pop_desc += "Tiny settlement"
                
            services_desc = "\nServices: "
            if self.services:
                services_desc += ", ".join(self.services)
            else:
                services_desc += "No services available"
                
            return base_desc + pop_desc + services_desc
            
        return base_desc
    
    def add_service(self, service):
        """Add an available service to this settlement."""
        if service not in self.services:
            self.services.append(service)
            
    def has_service(self, service):
        """Check if a specific service is available."""
        return service in self.services

    def provide_shelter(self, service_name, character):
        if service_name not in self.services:
            return f"No {service_name} service available here."

        service_costs = {
            "food": 20,
            "shelter": 30,
            "medical": 50
        }

        cost = service_costs.get(service_name.lower(), 0)
        
        if not hasattr(character, 'money') or character.money < cost:
            return f"You don't have enough money for {service_name} service (needs ${cost})."

        if service_name.lower() == "food":
            if hasattr(character, 'food'):
                character.food = min(100, character.food + 40)
                character.money -= cost
                return f"{character.name} pays ${cost} and receives a meal from the local community."
        elif service_name.lower() == "shelter":
            if hasattr(character, 'health'):
                character.health = min(100, character.health + 20)
                character.money -= cost
                return f"{character.name} pays ${cost} for shelter and rests safely."
        elif service_name.lower() == "medical":
            if hasattr(character, "health"):
                character.health = min(100, character.health + 35)
                character.money -= cost
                return f"{character.name} pays ${cost} and receives medical care."
        
        return f"Used {service_name} service."
        