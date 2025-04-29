"""
Events for 'The Line: A Border Journey'

This module defines the narrative events that can occur during gameplay,
representing key moments and challenges from 'The Line Becomes a River'.
"""

import random


class Event:
    """Base class for all game events."""
    
    def __init__(self, name, description, location_types=None):
        """
        Initialize an event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            location_types (list): Types of locations where this event can occur
        """
        self.name = name
        self.description = description
        self.location_types = location_types or []
        
    def can_occur(self, location):
        """Check if this event can occur at the given location."""
        if not self.location_types:
            return True  # Can occur anywhere if no specific types
        
        for location_type in self.location_types:
            if isinstance(location, location_type):
                return True
        return False
    
    def execute(self, game, character):
        """Execute the event for the given character.
        
        Args:
            game: The game instance
            character: The character experiencing the event
            
        Returns:
            str: Description of what happened
        """
        return self.description


class EncounterEvent(Event):
    """An event where the character encounters someone or something."""
    
    def __init__(self, name, description, encounter_type, location_types=None):
        """
        Initialize an encounter event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            encounter_type (str): Type of encounter ('migrant', 'patrol', 'local')
            location_types (list): Types of locations where this event can occur
        """
        super().__init__(name, description, location_types)
        self.encounter_type = encounter_type
        
    def execute(self, game, character):
        """Execute the encounter event."""
        base_result = super().execute(game, character)
        
        # Different outcomes based on encounter type
        if self.encounter_type == 'patrol' and hasattr(character, 'hope'):
            # Migrants lose hope when encountering patrol
            character.hope = max(0, character.hope - 20)
            return f"{base_result}\n{character.name}'s hope diminishes."
            
        elif self.encounter_type == 'migrant' and hasattr(character, 'stress'):
            # Border patrol agents gain stress when encountering migrants
            character.stress = min(100, character.stress + 10)
            return f"{base_result}\n{character.name}'s stress increases."
            
        elif self.encounter_type == 'local' and hasattr(character, 'hope'):
            # Migrants gain hope when encountering helpful locals
            character.hope = min(100, character.hope + 10)
            return f"{base_result}\n{character.name} feels more hopeful."
            
        return base_result


class ResourceEvent(Event):
    """An event related to finding or losing resources."""
    
    def __init__(self, name, description, resource_type, amount, location_types=None):
        """
        Initialize a resource event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            resource_type (str): Type of resource ('water', 'food', 'health', 'item')
            amount (int): Amount gained (positive) or lost (negative)
            location_types (list): Types of locations where this event can occur
        """
        super().__init__(name, description, location_types)
        self.resource_type = resource_type
        self.amount = amount
        
    def execute(self, game, character):
        """Execute the resource event."""
        base_result = super().execute(game, character)
        
        if self.resource_type == 'water' and hasattr(character, 'water'):
            character.water = max(0, min(100, character.water + self.amount))
            if self.amount > 0:
                return f"{base_result}\n{character.name} found water."
            else:
                return f"{base_result}\n{character.name} lost water."
                
        elif self.resource_type == 'food' and hasattr(character, 'food'):
            character.food = max(0, min(100, character.food + self.amount))
            if self.amount > 0:
                return f"{base_result}\n{character.name} found food."
            else:
                return f"{base_result}\n{character.name} lost food."
                
        elif self.resource_type == 'health':
            character.health = max(0, min(100, character.health + self.amount))
            if self.amount > 0:
                return f"{base_result}\n{character.name}'s health improved."
            else:
                return f"{base_result}\n{character.name}'s health worsened."
                
        elif self.resource_type == 'item':
            if self.amount > 0 and hasattr(game, 'items') and game.items:
                # Add a random item from game's item pool
                item = random.choice(game.items)
                character.add_to_inventory(item)
                return f"{base_result}\n{character.name} found {item}."
            elif self.amount < 0 and character.inventory:
                # Remove a random item from inventory
                item = random.choice(character.inventory)
                character.remove_from_inventory(item)
                return f"{base_result}\n{character.name} lost {item}."
        
        elif self.resource_type == 'item' and item == 'Money':
            self.player.set_flag("has_money", True)
                
        return base_result


class MoralEvent(Event):
    """An event that presents a moral choice to the character."""
    
    def __init__(self, name, description, choices, consequences, location_types=None):
        """
        Initialize a moral event.
        
        Args:
            name (str): Name of the event
            description (str): Description of the event
            choices (list): List of possible choices
            consequences (list): List of consequences for each choice
            location_types (list): Types of locations where this event can occur
        """
        super().__init__(name, description, location_types)
        self.choices = choices
        self.consequences = consequences
        
    def execute(self, game, character):
        """Execute the moral event."""
        base_result = super().execute(game, character)
        
                # Print the event description FIRST
        print(f"\n{self.description}") # Use print() directly here

        # Present choices to the player
        choice_text = "\nChoices:\n"
        for i, choice in enumerate(self.choices):
            choice_text += f"{i+1}. {choice}\n"
        print(choice_text) # Print the choices directly

        # NOW get player input for the choice
        while True:
            try:
                # Modified the prompt text slightly for clarity
                choice_input = input(f"Enter choice (1-{len(self.choices)}): ")
                choice_index = int(choice_input) - 1
                if 0 <= choice_index < len(self.choices):
                    break
                else:
                    print("Invalid choice. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")
                
        consequence = self.consequences[choice_index]
        
        # Apply the consequence based on character type
        if hasattr(character, 'moral_compass'):
            # Border patrol moral compass adjustment
            moral_impact = consequence.get('moral_impact', 0)
            character.moral_compass = max(0, min(100, character.moral_compass + moral_impact))
            
        if hasattr(character, 'hope'):
            # Migrant hope adjustment
            hope_impact = consequence.get('hope_impact', 0)
            character.hope = max(0, min(100, character.hope + hope_impact))
            
        # Set any story flags from the consequence
        for flag, value in consequence.get('flags', {}).items():
            character.set_flag(flag, value)
            
        result_description = consequence.get('description', '')
        return f"You chose: {self.choices[choice_index]}\n{result_description}"


# Define some common events that can be used in the game
def create_common_events():
    """Create a list of common events."""
    from location import Desert, Border, Settlement  # Import here to avoid circular dependency

    border_wall_event = MoralEvent(
        "Border Wall Encounter",
        "You see a small gap in the border wall, seemingly unguarded. Nearby, a Border Patrol vehicle sits idle, engine running. It looks like the agent might be taking a break.",
        [
            "Attempt to slip through the gap quickly.",
            "Wait and observe the patrol vehicle for longer.",
            "Create a diversion to draw attention away from the gap."
        ],
        [
            {'description': "You dash through the gap. A sensor triggers an alarm! You hear shouting behind you as you run into US territory.", 'hope_impact': 10, 'flags': {'crossed_border': True}},
            {'description': "You wait. The agent returns to the vehicle and drives off. The gap remains, but you've lost valuable time.", 'hope_impact': -5},
            {'description': "You throw a rock to create noise away from the gap. It seems to work, but the sudden sound puts nearby wildlife on alert, potentially revealing your position later.", 'hope_impact': 5, 'flags': {'created_diversion': True}}
        ],
        location_types=[Border]
    )
    
    events = [
        border_wall_event, # Add the new event here
        # Desert events
        ResourceEvent(
            "Dehydration", 
            "The scorching sun beats down mercilessly.", 
            "water", -15, [Desert]
        ),
        ResourceEvent(
            "Water Cache", 
            "You discover a hidden cache of water left by humanitarian aid workers.", 
            "water", 30, [Desert]
        ),
        EncounterEvent(
            "Fellow Travelers", 
            "You encounter a group of migrants also making the journey north.", 
            "migrant", [Desert]
        ),
        
        # Border events
        EncounterEvent(
            "Border Patrol", 
            "A Border Patrol vehicle approaches in the distance.", 
            "patrol", [Border]
        ),
        MoralEvent(
            "Abandoned Child", 
            "You find a child alone, separated from their family during crossing.", 
            ["Take the child with you", "Leave them for Border Patrol to find", "Try to find their family"],
            [
                {"description": "You take responsibility for the child's safety.", "hope_impact": -10, "moral_impact": 15, "flags": {"has_child": True}},
                {"description": "You cannot risk the extra burden and leave them behind.", "hope_impact": -20, "moral_impact": -20},
                {"description": "You spend precious time searching for the family.", "hope_impact": 5, "moral_impact": 10, "flags": {"helped_family": True}}
            ],
            [Border]
        ),
        
        # Settlement events
        ResourceEvent(
            "Local Charity", 
            "A local church is providing meals to migrants.", 
            "food", 40, [Settlement]
        ),
        EncounterEvent(
            "Hostile Locals", 
            "Some residents are not welcoming to migrants passing through.", 
            "local", [Settlement]
        ),
        MoralEvent(
            "Job Offer", 
            "A local offers you under-the-table work, but it seems suspicious.", 
            ["Accept the work", "Decline politely", "Report to authorities"],
            [
                {"description": "The work is difficult but provides needed money.", "hope_impact": 10, "flags": {"employed": True}},
                {"description": "You avoid potential trouble but remain without resources.", "hope_impact": -5},
                {"description": "Authorities investigate but your status is now known.", "hope_impact": -15, "moral_impact": 5}
            ],
            [Settlement]
        )
    ]

    # Add more events here as needed
    
    return events