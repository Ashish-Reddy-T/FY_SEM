"""
Game Engine for 'The Line: A Border Journey'

This module handles the core game mechanics, player interactions,
and gameplay flow for the narrative experience.
"""

import random
import time
import sys
from unittest import result
from character import Character, Migrant, BorderPatrol
from location import Location, Desert, Border, Settlement
from events import Event, create_common_events
from embeddings import EmbeddingsEngine


class GameEngine:
    """Main game engine that manages the game state and mechanics."""
    
    def __init__(self, story):
        """Initialize the game engine.
        
        Args:
            story: The Story instance containing narrative elements
        """
        self.story = story
        self.player = None
        self.world = {}
        self.current_location = None
        self.events = []
        self.items = [
            "Water Bottle", "Canned Food", "Blanket", "Map", "Flashlight",
            "First Aid Kit", "Compass", "Family Photo", "Money", "ID Papers", "Radio"
        ]
        self.turn_count = 0
        self.game_over = False
        self.ending = None
        self.ending_type = None  # Track the type of ending the player reaches
        
        # Initialize AI embeddings engine
        self.embeddings_engine = None
        try:
            self.embeddings_engine = EmbeddingsEngine()
            print("AI embeddings engine initialized successfully.")
        except Exception as e:
            print(f"Warning: Could not initialize AI embeddings engine: {e}")
            print("Game will fall back to basic command processing.")
            self.embeddings_engine = None
        
    def create_world(self):
        """Create the game world with locations."""
        # Create locations
        # Mexican side
        nogales_mx = Settlement(
            "Nogales (Mexico)", 
            "A border city in Sonora - where desparation and dreams collide.",
            population=212000,
            danger_level=4
        )
        nogales_mx.add_service("food")
        nogales_mx.add_service("shelter")
        
        sonoran_desert = Desert(
            "Sonoran Desert", 
            "A vast, unforgiving expanse where the border dissolves into sand and shadow.",
            water_scarcity=9,
            danger_level=8
        )
        
        border_fence = Border(
            "Border Wall", 
            "A steel serpent cutting through the landscape - a symbol of division and hope, of policy and desperation.",
            patrol_intensity=8,
            danger_level=7
        )
        
        # US side
        nogales_us = Settlement(
            "Nogales (USA)", 
            "The American side of Nogales, in Arizona.",
            population=20000,
            danger_level=3
        )
        nogales_us.add_service("food")
        nogales_us.add_service("medical")
        
        tucson = Settlement(
            "Tucson", 
            "A major city in Arizona, about 70 miles north of the border.",
            population=545000,
            danger_level=2
        )
        tucson.add_service("food")
        tucson.add_service("shelter")
        tucson.add_service("medical")
        
        detention_center = Border(
            "Detention Center", 
            "A facility where apprehended migrants are processed and detained.",
            patrol_intensity=10,
            danger_level=5
        )
        
        # Connect locations
        nogales_mx.add_connection("north", border_fence)
        nogales_mx.add_connection("west", sonoran_desert)
        
        sonoran_desert.add_connection("east", nogales_mx)
        sonoran_desert.add_connection("north", border_fence)
        
        border_fence.add_connection("south", sonoran_desert)
        border_fence.add_connection("south", nogales_mx)
        border_fence.add_connection("north", nogales_us)
        
        nogales_us.add_connection("south", border_fence)
        nogales_us.add_connection("north", tucson)
        nogales_us.add_connection("east", detention_center)
        
        tucson.add_connection("south", nogales_us)
        
        detention_center.add_connection("west", nogales_us)
        
        # Add to world dictionary
        self.world = {
            "nogales_mx": nogales_mx,
            "sonoran_desert": sonoran_desert,
            "border_fence": border_fence,
            "nogales_us": nogales_us,
            "tucson": tucson,
            "detention_center": detention_center
        }
        
        # Set starting location
        self.current_location = nogales_mx
        
    def create_characters(self):
        """Create non-player characters for the game."""
        # Create a coyote (smuggler) character
        coyote = Character(
            "Manuel", 
            "A seasoned border smuggler who knows the desert routes.",
            health=90
        )
        coyote.add_to_inventory("Water Bottle")
        coyote.add_to_inventory("Map")
        
        # Create a border patrol agent
        agent = BorderPatrol(
            "Agent Hernandez", 
            "A border patrol agent with Mexican heritage, conflicted about his role.",
            years_of_service=12,
            health=100
        )
        
        # Create a fellow migrant
        fellow_migrant = Migrant(
            "Elena", 
            "A young mother from Guatemala seeking asylum.",
            origin="Guatemala City",
            motivation="Escaping gang violence and seeking a better life for her child.",
            health=80
        )
        fellow_migrant.add_family_tie("Sofia", "daughter")
        fellow_migrant.water = 60
        fellow_migrant.food = 50
        
        # Add characters to locations
        self.world["nogales_mx"].add_character(coyote)
        self.world["border_fence"].add_character(agent)
        self.world["sonoran_desert"].add_character(fellow_migrant)
        

    # game_engine.py - create_player method
    def create_player(self, name, character_type="migrant", **kwargs):
        if character_type.lower() == "migrant":
            self.player = Migrant(
                name,
                kwargs.get("description", "A migrant seeking a better life in the United States."),
                kwargs.get("origin", "Central Mexico"),
                kwargs.get("motivation", "Economic opportunity and safety."),
                kwargs.get("health", 100)
            )
            self.player.add_to_inventory("Water Bottle")
            self.player.add_to_inventory("Family Photo")
        elif character_type.lower() == "patrol":
            self.player = BorderPatrol(
                name,
                kwargs.get("description", "A border patrol agent working the southern border."),
                kwargs.get("years_of_service", 5),
                kwargs.get("health", 100)
            )
            self.player.add_to_inventory("Flashlight")
            self.player.add_to_inventory("Radio")
            self.player.add_to_inventory("Water Bottle")  # Added water bottle
        
        # Place player at starting location
        if self.current_location:
            self.current_location.add_character(self.player)
            
    def load_events(self):
        """Load events into the game."""
        self.events = create_common_events()
        
        # Add events to appropriate locations
        for event in self.events:
            for location in self.world.values():
                if event.can_occur(location):
                    location.add_event(event)
                    
    def initialize_embeddings(self):
        """Initialize the embeddings engine with game content."""
        if not self.embeddings_engine:
            return
            
        try:
            # Initialize command embeddings
            self.embeddings_engine.initialize_command_embeddings()
            
            # Initialize location embeddings
            self.embeddings_engine.initialize_location_embeddings(self.world)
            
            # Initialize character embeddings
            all_characters = []
            for location in self.world.values():
                all_characters.extend(location.characters)
            if self.player:
                all_characters.append(self.player)
            self.embeddings_engine.initialize_character_embeddings(all_characters)
            
            # Initialize item embeddings
            self.embeddings_engine.initialize_item_embeddings(self.items)
            
            print("AI embeddings initialized with game content.")
        except Exception as e:
            print(f"Warning: Error initializing embeddings with game content: {e}")
            print("Game will fall back to basic command processing.")
            self.embeddings_engine = None
    
    def start(self):
        """Start the game."""
        # Get player information
        name, character_type, extra_info = self.story.get_player_info()
        
        # Initialize game world
        self.create_world()
        self.create_characters()
        self.create_player(name, character_type, **extra_info)
        self.load_events()
        
        # Initialize AI embeddings with game content
        self.initialize_embeddings()
        
        # Display initial story
        self.story.display_intro(self.current_location.name)
        
        # Main game loop
        self.main_loop()
        
        # Display journey summary and ending
        if self.game_over:
            self.story.display_journey_summary(self.player)
            if self.ending:
                self.story.display_ending(self.ending, self.player)
            else:
                self.story.display_ending("general", self.player)
            # print("\nThank you for playing 'The Line: A Border Journey'")
    
    def main_loop(self):
        """Run the main game loop."""
        # Initial location description
        print(self.current_location.describe(detailed=True))
        print("\nType 'help' for available commands.")

        # Main loop
        while not self.game_over:
            # --- CHANGE START ---
            # Display effects from the previous turn or location entry FIRST
            location_effect_msg = ""
            if hasattr(self.current_location, "apply_effects"):
                 # Get passive description of location effect without applying resource drain here
                 location_effect_msg = self.current_location.apply_effects(self.player)
                 if location_effect_msg: print("\n" + location_effect_msg)

            # Apply per-turn resource consumption for Migrants
            resource_msg = ""
            # In game_engine.py - modify the main_loop() method
            if isinstance(self.player, Migrant):
                base_water_consumption = 5
                base_food_consumption = 5
                # Modify consumption based on location type
                if isinstance(self.current_location, Desert):
                    base_water_consumption += self.current_location.water_scarcity // 2
                    base_food_consumption += 2
                elif isinstance(self.current_location, Settlement) and self.current_location.has_service("food"):
                    base_food_consumption = max(0, base_food_consumption - 3)
                
                resource_msg = self.player.consume_resources(base_water_consumption, base_food_consumption)
                
            elif isinstance(self.player, BorderPatrol):
                # Border Patrol consumes resources at a slower rate
                base_water_consumption = 3  # Reduced from 5 for migrants
                base_food_consumption = 3   # Reduced from 5 for migrants
                
                # Still affected by desert conditions, but less severely
                if isinstance(self.current_location, Desert):
                    base_water_consumption += self.current_location.water_scarcity // 3  # Less impact than migrants
                    base_food_consumption += 1  # Less impact than migrants
                    
                resource_msg = self.player.consume_resources(base_water_consumption, base_food_consumption)

            # Check for game over AFTER resource consumption (as health might drop)
            self.check_game_over()
            if self.game_over:
                print("\n" + self.get_ending_message())
                break # Exit loop immediately if game over

            # Trigger random narrative event (e.g., 15% chance each turn)
            if random.random() < 0.15:
                player_type = "migrant" if isinstance(self.player, Migrant) else "patrol"
                narrative_event = self.story.trigger_random_event(player_type)
                if narrative_event:
                    self.story.update_journey_stats("event", narrative_event)


            # Trigger trauma event occasionally (e.g., 5% chance, maybe less often)
            if random.random() < 0.05:
                 trauma = self.story.trigger_trauma_event()
                 if trauma:
                     self.story.update_journey_stats("trauma_experienced")
                     # Optional: Could affect hope/stress
                     if hasattr(self.player, 'hope'): self.player.change_hope(-10)
                     if hasattr(self.player, 'stress'): self.player.stress = min(100, self.player.stress + 15)

            # Get player command
            command = input("\n> ").strip() # Added strip() here
            if not command: # Handle empty input
                print("Please enter a command. Type 'help' for assistance.")
                continue

            result = self.process_command(command)

            if result.upper() == "QUIT":
                if input("Are you sure you want to quit? (y/n): ").lower().startswith("y"):
                    self.story.graceful_exit(self.player)
                    return
                continue

            print("\n" + result)

            # --- MOVED game over check AFTER command processing & resource drain ---
            # Check if game is over after command processing potentially triggered events or state changes
            # (The check after resource drain handles health/timeout, this handles event/action based endings)
            if not self.game_over: # Avoid double printing ending message
                self.check_game_over()
                if self.game_over:
                    print("\n" + self.get_ending_message())
    
    def process_command(self, command):
        """Process a player command."""
        original_command = command
        command = command.lower().strip()
        
        # Empty command
        if not command:
            return "Please enter a command. Type 'help' for assistance."
        
        # Try to use AI embeddings to understand natural language commands
        if self.embeddings_engine:
            try:
                # First try to match the command type
                best_command, score = self.embeddings_engine.find_best_command(command)
                
                if best_command and score > 0.7:
                    # If it's a movement command, extract the direction
                    if best_command.startswith("move "):
                        direction = best_command.split(" ", 1)[1]
                        return self.move(direction)
                    
                    # If it's a talk command, try to find the character
                    elif best_command == "talk":
                        # Extract potential character name from input
                        potential_target = command.replace("talk", "").replace("to", "").replace("with", "").strip()
                        if potential_target:
                            best_character, char_score = self.embeddings_engine.find_best_character(potential_target)
                            if best_character and char_score > 0.6:
                                return self.interact("talk", best_character)
                    
                    # If it's a take command, try to find the item
                    elif best_command == "take":
                        potential_item = command.replace("take", "").replace("get", "").replace("pick up", "").strip()
                        if potential_item:
                            best_item, item_score = self.embeddings_engine.find_best_item(potential_item)
                            if best_item and item_score > 0.6:
                                return self.interact("take", best_item)
                    
                    # If it's a use command, try to find the item
                    elif best_command == "use":
                        potential_item = command.replace("use", "").strip()
                        if potential_item:
                            best_item, item_score = self.embeddings_engine.find_best_item(potential_item)
                            if best_item and item_score > 0.6:
                                return self.interact("use", best_item)
                    
                    # For simple commands, just execute them
                    elif best_command in ["look", "status", "help"]:
                        return self.interact(best_command)
                    
                    elif best_command == "quit":
                        return "QUIT"
            except Exception as e:
                print(f"Error in AI command processing: {e}")
                # Fall back to traditional command processing
        
        # Traditional command processing as fallback
        
        # Movement commands
        if command.startswith("move ") or command.startswith("go "):
            parts = command.split(" ", 1)
            if len(parts) > 1:
                direction = parts[1]
                return self.move(direction)
            else:
                return "Move where? Try 'move north', 'move south', etc."
        
        # Direction shortcuts
        if command in ["north", "south", "east", "west", "n", "s", "e", "w"]:
            # Convert single letter directions to full words
            if command == "n": command = "north"
            elif command == "s": command = "south"
            elif command == "e": command = "east"
            elif command == "w": command = "west"
            
            return self.move(command)
        
        # Talk command
        if command.startswith("talk ") or command.startswith("speak "):
            parts = command.split(" ", 1)
            if len(parts) > 1:
                target = parts[1]
                return self.interact("talk", target)
            else:
                return "Talk to whom? Try 'talk [character name]'."
        
        # Take command
        if command.startswith("take ") or command.startswith("get "):
            parts = command.split(" ", 1)
            if len(parts) > 1:
                target = parts[1]
                return self.interact("take", target)
            else:
                return "Take what? Try 'take [item name]'."
        
        # Use Service command
        if command.startswith("use service "):
            parts = command.split(" ", 2)
            if len(parts) > 2:
                service = parts[2]
                return self.interact("use_service", service)
            else:
                return "Use which service? Try 'use service [food/shelter/medical]'"
        
        # Use command
        if command.startswith("use "):
            parts = command.split(" ", 1)
            if len(parts) > 1:
                target = parts[1]
                return self.interact("use", target)
            else:
                return "Use what? Try 'use [item name]'."
        
        # Other commands
        if command == "look" or command == "examine":
            return self.interact("look")
        
        if command == "status" or command == "inventory":
            return self.interact("status")
        
        if command == "help":
            return self.interact("help")
        
        if command == "quit" or command == "exit":
            return "QUIT"
        
        # Unknown command
        return f"I don't understand '{original_command}'. Type 'help' for assistance."
    
    def move(self, direction):
        """Move the player in the specified direction."""
        if not self.current_location:
            return "You are nowhere."

        if direction not in self.current_location.connections:
            return f"You cannot go {direction} from here."

        # Remove player from current location
        self.current_location.remove_character(self.player)

        # Update current location
        self.current_location = self.current_location.connections[direction]

        # Add player to new location
        self.current_location.add_character(self.player)

        # Mark as visited
        self.current_location.visited = True

        # --- CHANGE START ---
        # Increment turn counter AFTER successfully moving
        self.turn_count += 1
        self.story.update_journey_stats("distance_traveled", 10) # Example: Add 10 miles per move

        # Get the description of the new location
        move_report = f"You travel {direction} to {self.current_location.name}.\n"
        move_report += self.current_location.describe(detailed=True) # Show detailed description on arrival

        # Check for location-based random event (e.g., encounter) upon arrival
        # This is separate from the per-turn random narrative events in main_loop
        event_result = self.check_for_event()
        if event_result:
            move_report += "\n\n" + event_result
            # Extract just the event description (not the full result text)
            event_desc = event_result.split('\n')[0] if '\n' in event_result else event_result
            if "moral" in event_result.lower() or "choice" in event_result.lower():
                self.story.update_journey_stats("moral_choices_made")
            if "encounter" in event_result.lower():
                self.story.update_journey_stats("lives_impacted")
                # Only add unique encounter events
                if not self.story.journey_stats["key_events"] or event_desc != self.story.journey_stats["key_events"][-1]:
                    self.story.update_journey_stats("event", narrative_event)


        # Check game over conditions AFTER moving and potential events
        self.check_game_over()
        # Note: The main loop will print the ending message if game_over is set here.

        return move_report
    
    def check_for_event(self, force=False):
        """Check if a random event occurs.
        
        Args:
            force (bool): Force an event to occur
            
        Returns:
            str: Description of the event, or None if no event occurred
        """
        # Skip if game is over
        if self.game_over:
            return None
            
        # Determine if an event should occur (30% chance by default)
        if not force and random.random() > 0.3:
            return None
            
        # Get a random event from the current location
        event = self.current_location.get_random_event()
        if not event:
            return None
            
        # Execute the event
        return event.execute(self, self.player)
    
    def check_game_over(self):
        """Check if game over conditions have been met."""
        # Check health
        if self.player.health <= 0:
            self.game_over = True
            self.ending = "death"
            return True
            
        # Check if water reached 0 (for migrants)
        if hasattr(self.player, 'water') and self.player.water <= 0:
            self.game_over = True
            self.ending = "death"
            return True
            
        # Check if reached final destination (Tucson)
        if self.current_location == self.world.get("tucson"):
            self.game_over = True
            self.ending = "success"
            return True
            
        # Check if detained
        if self.current_location == self.world.get("detention_center") and isinstance(self.player, Migrant):
            self.game_over = True
            self.ending = "detained"
            return True
            
        # Check if maximum turns reached
        if self.turn_count >= 30:
            self.game_over = True
            self.ending = "timeout"
            return True
            
        return False
    
    def get_ending_message(self):
        """Get the ending message based on how the game ended."""
        if not self.game_over:
            return "The journey continues..."
            
        if self.ending == "death":
            return "Your journey has come to a tragic end. The border crossing claimed another life."
            
        elif self.ending == "success":
            return "You've successfully reached Tucson. While challenges remain, you've completed the most dangerous part of your journey."
            
        elif self.ending == "detained":
            return "You've been detained by Border Patrol. You'll be processed and your fate now lies within the immigration system."
            
        elif self.ending == "timeout":
            return "Your journey has taken too long. Resources depleted, you can go no further."
            
        return "Your journey has ended."
    
    def get_status(self):
        if not self.player or not self.current_location:
            return "Game not properly initialized."
            
        status = f"Turn: {self.turn_count}\n"
        status += f"Location: {self.current_location.name}\n"
        status += f"Health: {self.player.health}\n"
        
        if hasattr(self.player, 'water'):
            status += f"Water: {self.player.water}\n"
            
        if hasattr(self.player, 'food'):
            status += f"Food: {self.player.food}\n"
            
        if hasattr(self.player, 'money'):
            status += f"Money: ${self.player.money}\n"
            
        if hasattr(self.player, 'hope'):
            status += f"Hope: {self.player.hope}\n"
            
        if hasattr(self.player, 'moral_compass'):
            status += f"Moral Compass: {self.player.moral_compass}\n"
            
        if hasattr(self.player, 'stress'):
            status += f"Stress: {self.player.stress}\n"
            
        status += f"Inventory: {', '.join(self.player.inventory) if self.player.inventory else 'Empty'}\n"
        
        return status
    
    def interact(self, action, target=None):
        """Perform an interaction in the game.
        
        Args:
            action (str): The action to perform ('talk', 'take', 'use', etc.)
            target (str): The target of the action
            
        Returns:
            str: Description of what happened
        """
        if self.game_over:
            return "The game is over."
            
        if action == "look":
            base_desc = self.current_location.describe(detailed=True)

            thematic_quotes = self.story.get_location_description(type(self.current_location), self.current_location.name)
            if thematic_quotes:
                base_desc += "\n\n" + random.choice(thematic_quotes)
            
            return base_desc
            
        elif action == "status":
            return self.get_status()
            
        elif action == "talk" and target:
            # Try to use AI embeddings to find the character if available
            original_target = target
            if self.embeddings_engine:
                try:
                    best_character, score = self.embeddings_engine.find_best_character(target)
                    if best_character and score > 0.6:
                        target = best_character
                except Exception as e:
                    print(f"Error in AI character matching: {e}")
                    
            # Find character in current location
            for character in self.current_location.characters:
                if character != self.player and target.lower() in character.name.lower():
                    # Increment turn counter
                    self.turn_count += 1
                    
                    # Generate dialogue based on character type with deeper narrative
                    if isinstance(character, Migrant):
                        migrant_quotes = [
                            f"We carry our dreams across this desert. I left {character.origin} because {character.motivation}",
                            "Each step north is a step away from desperation, but also from everything we know.",
                            "The border is more than just a wall - it's a test of our humanity.",
                            "Sometimes I wonder if the American dream is worth all this suffering."
                        ]
                        return f"{character.name}: '{random.choice(migrant_quotes)}'"
                    elif isinstance(character, BorderPatrol):
                        patrol_quotes = [
                            f"After {character.years_of_service} years, you see things differently. The line between duty and compassion blurs.",
                            "We're trapped in a system that has no regard for humanity.",
                            "Sometimes I wonder what it means to be good at this job.",
                            "Every face I encounter here has a story that deserves to be heard."
                        ]
                        return f"{character.name}: '{random.choice(patrol_quotes)}'"
                    else:
                        coyote_quotes = [
                            "The desert doesn't care about borders or laws. It treats everyone the same.",
                            "I've seen too many dreams end in these sands.",
                            "Each crossing leaves its mark on your soul.",
                            "The border changes everyone who encounters it."
                        ]
                        return f"{character.name}: '{random.choice(coyote_quotes)}'"
            return f"There is no one named {original_target} here."
            
        elif action == "take" and target:
            # Try to use AI embeddings to find the item if available
            original_target = target
            if self.embeddings_engine:
                try:
                    best_item, score = self.embeddings_engine.find_best_item(target)
                    if best_item and score > 0.6:
                        target = best_item
                except Exception as e:
                    print(f"Error in AI item matching: {e}")

            # Check if item is in location
            item_found = None
            for item in self.current_location.items:
                # More robust matching (check start, end, exact match)
                item_lower = item.lower()
                target_lower = target.lower()
                if item_lower == target_lower or item_lower.startswith(target_lower) or item_lower.endswith(target_lower):
                    item_found = item
                    break # Found the item

            if item_found:
                self.current_location.remove_item(item_found)
                self.player.add_to_inventory(item_found)
                self.turn_count += 1
                return f"You take the {item_found}." # Use the actual item name found

            # If loop finishes without finding item
            return f"There is no {original_target} here to take." # Report original target name
        
        elif action == "use_service":
            if isinstance(self.current_location, Settlement):
                result = self.current_location.provide_shelter(target, self.player)
                self.turn_count += 1
                return result
            else:
                return "This location doesn't have services."
            
        elif action == "use" and target:
            # Try to use AI embeddings to find the item if available
            original_target = target
            if self.embeddings_engine:
                try:
                    best_item, score = self.embeddings_engine.find_best_item(target)
                    if best_item and score > 0.6:
                        target = best_item
                except Exception as e:
                    print(f"Error in AI item matching: {e}")

            # Check if item is in inventory
            item_to_use = None
            for item in self.player.inventory:
                 # More robust matching
                 item_lower = item.lower()
                 target_lower = target.lower()
                 if item_lower == target_lower or item_lower.startswith(target_lower) or item_lower.endswith(target_lower):
                     item_to_use = item
                     break # Found item

            if item_to_use:
                item_lower = item_to_use.lower() # Use the actual found item name
                self.turn_count += 1

                # Apply item effects
                if "water bottle" in item_lower:
                    if hasattr(self.player, 'water'):
                        self.player.water = min(100, self.player.water + 30)
                        # self.player.remove_from_inventory(item_to_use)
                        return "You drink from the water bottle, restoring some hydration."
                    else:
                        return "You drink from the water bottle, but it doesn't seem to affect you much."

                elif "canned food" in item_lower:
                    if hasattr(self.player, 'food'):
                        self.player.food = min(100, self.player.food + 40)
                        # self.player.remove_from_inventory(item_to_use)
                        return "You eat the canned food, satisfying your hunger."
                    else:
                        return "You eat the canned food, but it doesn't seem to affect you much."

                elif "first aid kit" in item_lower:
                    self.player.health = min(100, self.player.health + 25)
                    # self.player.remove_from_inventory(item_to_use)
                    return "You use the first aid kit, treating some wounds."

                elif "map" in item_lower:
                     # Maybe reveal connections or provide more detail?
                     connections_desc = ", ".join([f"{direction} ({loc.name})" for direction, loc in self.current_location.connections.items()])
                     return f"You consult the map. Paths lead to: {connections_desc if connections_desc else 'Unknown'}."

                elif "flashlight" in item_lower:
                    # Could be useful in specific dark locations or events (requires adding flags/checks)
                    return "You turn on the flashlight. Its beam cuts through the ambient light."

                elif "compass" in item_lower:
                    # Could provide narrative confirmation or help if player is 'lost' (requires adding flags/checks)
                    return "You check the compass. It confirms the cardinal directions."

                elif "family photo" in item_lower:
                    if hasattr(self.player, 'hope'):
                        hope_change = self.player.change_hope(15) # Use the method from character.py
                        return f"You look at the photo of your family. {hope_change}"
                    else:
                        return "You look at the photo, feeling a mix of emotions."

                # Added effects for previously unused items
                elif "blanket" in item_lower:
                    # Could provide warmth effect (e.g., negate cold penalty at night - requires time/weather system)
                    return "You wrap the blanket around yourself. It provides some comfort against the elements."

                elif "money" in item_lower:
                    # Could be used in specific interactions (e.g., bribing, buying supplies - requires event/dialogue changes)
                    return "You count the money. It might be useful if you encounter the right people."

                elif "id papers" in item_lower:
                    # Could be crucial for certain events or endings (requires event/dialogue changes)
                    return "You check your ID papers. Having them feels important, potentially risky."
                
                # game_engine.py - interact method additions
                elif "radio" in item_lower and isinstance(self.player, BorderPatrol):
                    # Random chance to get useful information
                    if random.random() < 0.3:
                        intel = random.choice([
                            "Radio reports suspicious activity to the north.",
                            "Dispatch mentions a group crossing near your location.",
                            "Another agent reports finding abandoned supplies."
                        ])
                        return f"You use the radio. {intel}"
                    return "You use the radio but hear only static."

                elif "radio" in item_lower:
                     # Useful mainly for Border Patrol character type
                     if isinstance(self.player, BorderPatrol):
                         # Could trigger a random report or allow calling for backup (requires event system enhancements)
                         radio_chatter = random.choice([
                             "Static crackles...",
                             "A garbled voice mentions activity near Sector 4.",
                             "Control asks for a sit-rep (situation report).",
                             "Silence."
                         ])
                         return f"You use the radio. {radio_chatter}"
                     else:
                         return "You fiddle with the radio, but can't make sense of the transmissions."

                else:
                    return f"You use the {item_to_use}, but nothing special happens."

            # If loop finishes without finding item in inventory
            return f"You don't have {original_target} in your inventory."

            
        elif action == "help":
            help_text = "\nAvailable commands: \n"
            help_text += "- look: Examine your surroundings\n"
            help_text += "- status: Check your current status\n"
            help_text += "- talk [character]: Talk to a character\n"
            help_text += "- take [item]: Take an item\n"
            help_text += "- use [item]: Use an item from your inventory\n"
            help_text += "- use service [type]: Access settlement services (food/shelter/medical)\n"
            help_text += "- move [direction]: Move in a direction (north, south, east, west)\n"
            help_text += "- help: Show this help text\n"
            help_text += "- quit: Exit the game\n"
            
            # Add information about AI natural language processing if available
            if self.embeddings_engine:
                help_text += "\nThis game features AI-powered natural language understanding.\n"
                help_text += "You can use more natural phrases like:\n"
                help_text += "- 'check my health' instead of 'status'\n"
                help_text += "- 'speak with Manuel' instead of 'talk Manuel'\n"
                help_text += "- 'grab the water' instead of 'take water bottle'\n"
                help_text += "- 'drink from my bottle' instead of 'use water bottle'\n"
                help_text += "- 'head north' instead of 'move north'\n"
            
            return help_text
            
        return f"I don't understand '{action}'."