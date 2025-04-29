"""
Story module for 'The Line: A Border Journey'

This module handles the narrative elements, player interactions,
and storytelling aspects of the game.
"""

import time
import os
import sys
import random


class Story:
    """Manages the narrative elements of the game."""
    
    def __init__(self):
        """Initialize the story."""
        self.themes = [
            "humanity across borders",          
            "moral complexity of enforcement",
            "personal cost of migration",
            "impact of policy on individual lives",
            "trauma and healing",
            "identity and belonging",
            "duty versus compassion",
            "memory and forgetting"
        ]
        self.quotes = [
            "The border is a place characterized by flux and tension, a landscape of convergence where the realities of two nations meet.",
            "We are trapped in a system that has no regard for humanity.",
            "There are days when I feel I am becoming good at what I do. And then I wonder, what does it mean to be good at this?",
            "The border divides the past from the future, and we stand always in its present shadow.",
            "Each body recovered from the desert has a story, a dream that ended too soon.",
            "The border makes ghosts of us all - those who cross, those who guard, those who never return.",
            "In the end, we're all just people trying to do what we believe is right.",
            "Some wounds never heal; they just become part of who we are."
        ]

        # Two choices for the user to experience!
        self.moral_choices = {
            # Migrant: Random cases that popped up!
            "migrant": [
                "Share limited water with a struggling fellow migrant",
                "Help an injured companion who will slow you down",
                "Trust a coyote's risky shortcut through cartel territory",
                "Reveal sensitive information to gain asylum",
                "Hide a family with children from patrol",
                "Abandon your belongings to move faster",
                "Risk exposure to avoid cartel territory",
                "Share your last food with a starving child"
            ],
            # Patrol: Did what felt right!
            "patrol": [
                "Look the other way for a desperate family",
                "Report a fellow agent's abuse of power",
                "Provide aid to an injured migrant at risk of disciplinary action",
                "Follow orders that conflict with personal values",
                "Share water with dehydrated migrants",
                "Investigate suspicious cartel activity alone",
                "Warn migrants about dangerous conditions ahead",
                "Choose between pursuing smugglers or helping injured migrants"
            ]
        }

        self.trauma_events = [
            "Finding remains in the desert",
            "Witnessing cartel violence",
            "Separation from loved ones",
            "Near-death from exposure",
            "Discovering abandoned children",
            "Encountering human trafficking victims",
            "Witnessing a fatal accident",
            "Finding evidence of torture"
        ]

        # Random events to induce engrossment
        self.random_events = {
            "migrant": [
                "A helicopter spotlight sweeps across your position",
                "You find an abandoned backpack with supplies",
                "Distant gunshots echo through the canyon",
                "You discover a hidden water cache",
                "A dust storm approaches from the horizon",
                "You spot border patrol vehicles in the distance",
                "You find recent footprints heading north",
                "The howl of coyotes fills the night"
            ],
            "patrol": [
                "You receive reports of cartel activity nearby",
                "Your radio crackles with reports of multiple crossings",
                "You find evidence of human trafficking",
                "A migrant family surrenders to your unit",
                "You discover a sophisticated tunnel entrance",
                "Your thermal imaging detects movement ahead",
                "You find an abandoned vehicle with supplies",
                "A fellow agent requests immediate backup"
            ]
        }

        # Journey stats (Similar to health levels in a game)
        self.journey_stats = {
            "distance_traveled": 0,
            "lives_impacted": 0,
            "moral_choices_made": 0,
            "trauma_experienced": 0,
            "key_events": []
        }
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else "clear")
    
    def print_slow(self, text, delay=0.03):
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    
    def display_intro(self, starting_location):
        """Display the game introduction."""
        self.clear_screen()
        
        intro_text = """
        The border is not just a line on a map. It's a place where lives intersect,
        where dreams and desperation collide with policy and duty.
        
        In this narrative experience, you will walk in the footsteps of those who
        cross the border and those who patrol it. Your choices will shape your
        journey and reveal the complex human stories behind headlines.
        
        As Francisco Cantú writes in 'The Line Becomes a River', the border leaves
        its mark on all who encounter it - those who cross it, those who enforce it,
        and those who live in its shadow.
        """
        
        self.print_slow(intro_text)
        print(f"\nYour journey begins in {starting_location}.")
        input("\nPress Enter to continue ... ")
        self.clear_screen()
    
    def get_player_info(self):
        """Get the player's character information."""
        self.clear_screen()
        print("CHARACTER CREATION")
        print("==================\n")
        
        # Choose character type
        print("Choose your role:")
        print("1. Migrant           -   Seeking a better life across the border")
        print("2. Border Patrol     -   Enforcing the boundary between nations")
        
        while True:
            choice = input("\nEnter your choice (1 or 2): ")
            if choice in ["1", "2"]:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        character_type = "migrant" if choice == "1" else "patrol"
        
        # Get character name
        name = input("\nEnter your character's name: ")
        while not name.strip():
            name = input("Name cannot be empty. Please enter a name: ")
        
        # Get additional info based on character type
        if character_type == "migrant":
            origin = input("\nWhere are you from? (e.g., 'Central Mexico', 'Guatemala'): ")
            motivation = input("\nWhy are you making this journey? ")
            return name, character_type, {"origin": origin, "motivation": motivation}
        else:
            years = input("\nHow many years have you served in Border Patrol? ")
            try:
                years = int(years)
            except ValueError:
                years = 5
                print("Using default: 5 years")
            return name, character_type, {"years_of_service": years}
    
    def display_ending(self, ending_type, player):
        """Display the game ending based on ending type."""
        self.clear_screen()
        print("EPILOGUE")
        print("========\n")
        
        if ending_type == "success" and hasattr(player, 'origin'):
            epilogue = """
            You've made it to Tucson, but your journey is far from over. Like many migrants
            who cross the border, you now face the challenges of building a life in a new country.
            
            Some find opportunity and safety, others face continued hardship and the constant
            fear of deportation. The border crossing was just the beginning of a longer journey.
            
            As Francisco Cantú writes, the border leaves its mark on all who encounter it - those who 
            cross it, those who enforce it, and those who live in its shadow 👋🏻.
            """
        
        elif ending_type == "detained":
            epilogue = """
            In detention, you become one of thousands processed through America's immigration system.
            Your future is uncertain - you may be deported, or you may be granted asylum.
            
            The system is complex and often arbitrary. Your story, your reasons for crossing,
            become reduced to paperwork and case numbers.
            
            As Cantú observed during his time in Border Patrol, the individual humanity of migrants
            is often lost in the machinery of enforcement and policy.
            """
        
        elif ending_type == "death":
            epilogue = """
            Your journey ends in the borderlands, as it does for hundreds of migrants each year.
            The desert is an unforgiving place, and the border crossing claims many lives.
            
            These deaths often go unnoticed by the wider world. A cross in the desert, perhaps,
            or a body never found.
            
            Cantú writes of finding the remains of those who didn't make it, a grim reminder of
            the human cost of border policies and the desperate circumstances that drive people
            to risk everything.
            """
        
        elif ending_type == "timeout":
            epilogue = """
            Your resources depleted, your strength gone, your journey cannot continue.
            The border region has claimed another victim of its harsh realities.
            
            The journey across the border is not just a physical one, but a test of
            endurance, will, and luck. Not everyone makes it through 😶.
            
            As Cantú's book shows us, the border is a place of extremes, where small
            decisions can have life-altering consequences.
            """
        
        else:
            epilogue = """
            Your journey along the border has ended, but the larger story continues.
            
            Every day, people cross the border seeking better lives. Every day, agents patrol
            the line between nations. The complex interplay of policy, duty, desperation, and hope
            continues to shape countless lives.
            
            As 'The Line Becomes a River' shows us, there are no simple answers to the questions
            the border raises, only human stories that deserve to be understood in all their complexity.
            """
        
        self.print_slow(epilogue)
        
        print("\nThank you for experiencing 'The Line: A Border Journey'.")
        print("This narrative was inspired by 'The Line Becomes a River' by Francisco Cantú.")
        print()
    
    def get_character_dialogue(self, character, player):
        """Get dialogue for a character based on their type and relationship to player."""
        from character import Migrant, BorderPatrol
        
        # Enhanced dialogue templates with more emotional depth
        if isinstance(character, Migrant):
            if isinstance(player, Migrant):
                return [
                    f"We're all trying to find a better life. I'm from {character.origin}. The violence there... it changes you.",
                    "Each step north carries the weight of those we left behind. But we must keep moving.",
                    "I saw someone collapse from dehydration yesterday. The Border Patrol found them... I don't know if they survived.",
                    f"My {', '.join([tie['name'] for tie in character.family_ties])} back home... they're all I think about. Their faces keep me going.",
                    "Sometimes I wonder if we're just chasing shadows across the desert."
                ]
            else:  # Player is Border Patrol
                return [
                    "Please... my children haven't eaten in days. We had no choice but to leave.",
                    "I know you're just doing your job. But can you look at me and see a human being, not just another case number?",
                    "Send me back if you must, but please, let me keep my dignity.",
                    "You wear that uniform, but I see the conflict in your eyes. You understand, don't you?",
                    "I've buried friends in this desert. How many more must die before something changes?"
                ]
        
        elif isinstance(character, BorderPatrol):
            if isinstance(player, BorderPatrol):
                return [
                    f"Been doing this {character.years_of_service} years now. Each year, the weight gets heavier.",
                    "Found a child's backpack yesterday. Pink, with butterflies. Still had a family photo inside...",
                    "We're supposed to be protecting the border, but sometimes I wonder what we're really protecting.",
                    "The desert doesn't discriminate. It takes from both sides of the line.",
                    "Some nights, I still hear their voices. The ones we couldn't save."
                ]
            else:  # Player is Migrant
                return [
                    "I've seen too many deaths in these borderlands. Please, don't make me witness another.",
                    "The law is clear, but the heart... the heart sometimes speaks louder.",
                    "I have water if you need it. At least let me do that much.",
                    "Every face I send back haunts me. But what choice do I have?",
                    "My own grandparents crossed this same desert. The irony isn't lost on me."
                ]
        
        else:  # Generic character with deeper perspective
            return [
                "The border draws a line on the map, but the real divisions run deeper.",
                "In the end, we're all just trying to survive this place.",
                "I've seen the best and worst of humanity in these borderlands.",
                "The stories here could fill a thousand books. Most will never be told.",
                "Some say the desert holds the spirits of those who never made it. Some nights, I believe them."
            ]
    
    def present_moral_choice(self, player_type, situation=None):
        """Present a moral choice to the player based on their character type."""
        if situation:
            choices = [situation]
        else:
            choices = self.moral_choices.get(player_type, [])
            if choices:
                choices = [random.choice(choices)]
        
        if not choices:
            return None
        
        choice = choices[0]
        self.print_slow(f"\nYou face a difficult decision:\n{choice}")
        self.print_slow("\nWhat will you do?")
        return choice
    
    def trigger_trauma_event(self):
        """Trigger a random traumatic event from the story's trauma events."""
        if not self.trauma_events:
            return None
        
        event = random.choice(self.trauma_events)
        self.print_slow(f"\nA haunting moment sears itself into your memory:\n{event}")
        return event
    
    def get_location_description(self, location_type, name):
        """Get additional thematic description for a location type."""
        from location import Desert, Border, Settlement
        
        if isinstance(location_type, Desert):
            return [
                "The desert stretches endlessly, a vast graveyard of dreams and desperation.",
                "The sun beats down like judgment from above, while the sand below holds countless untold stories.",
                "Between the saguaros, you glimpse remnants of others' journeys - a child's shoe, a tattered backpack, a rosary.",
                "The wind whispers names of those who never made it, their hopes scattered among sun-bleached bones.",
                "Even the cacti seem to weep here, their shadows stretching like mourners across the sand."
            ]
        
        elif isinstance(location_type, Border):
            return [
                "The wall rises like an iron curtain, dividing not just land, but dreams, families, and futures.",
                "Surveillance cameras stare with unblinking eyes, while sensors pulse beneath the ground like a mechanical heartbeat.",
                "The air thrums with tension - helicopter rotors above, desperate prayers below.",
                "Here, policy meets humanity in a clash of steel and flesh, law and desperation.",
                "Every footprint in the dust tells a story of choice - to cross, to turn back, to enforce, to defy."
            ]
        
        elif isinstance(location_type, Settlement):
            return [
                "The community lives and breathes the border, its rhythms shaped by the ebb and flow of crossings.",
                "In every face you see the weight of choice - to help, to hinder, to look away.",
                "Children play in the shadow of the wall, their laughter a defiant song against the barrier's silence.",
                "The streets hold secrets: safe houses marked with subtle signs, routes whispered in hushed tones.",
                "Even the church bells sound different here, their toll a reminder of lives interrupted, journeys unfinished."
            ]
        
        else:
            return [
                f"{name} pulses with the heartbeat of the borderlands, each moment pregnant with possibility and peril.",
                "The border's gravity pulls at everything here, bending lives like light through a prism.",
                "Time feels different in this place, stretched taut between before and after, between here and there.",
                "The air itself carries stories - of courage and fear, of mercy and indifference, of hope and despair.",
                "In every shadow lurks a choice, in every choice, a story waiting to be told."
            ]
    
    def trigger_random_event(self, player_type):
        """Trigger a random event based on player type."""
        if not self.random_events.get(player_type):
            return None
        
        event = random.choice(self.random_events[player_type])
        self.print_slow(f"\nSuddenly:\n{event}")
        
        # Only add if not already in the last few events to avoid duplicates
        if not self.journey_stats["key_events"] or event != self.journey_stats["key_events"][-1]:
            self.journey_stats["key_events"].append(event)
        
        return event
    
    def update_journey_stats(self, stat_type, value=1):
        """Update journey statistics."""
        if stat_type in self.journey_stats:
            if isinstance(self.journey_stats[stat_type], list):
                self.journey_stats[stat_type].append(value)
            else:
                self.journey_stats[stat_type] += value
    
    def display_journey_summary(self, player):
        """Display a summary of the player's journey and statistics."""
        self.clear_screen()
        print("JOURNEY SUMMARY")
        print("===============\n")
        
        # Basic stats
        print(f"Distance Traveled: {self.journey_stats['distance_traveled']} miles")
        print(f"Lives Impacted: {self.journey_stats['lives_impacted']} individuals")
        print(f"Moral Choices Made: {self.journey_stats['moral_choices_made']} decisions")
        print(f"Traumatic Events Experienced: {self.journey_stats['trauma_experienced']} incidents\n")
        
        # Key events
        if self.journey_stats['key_events']:
            print("Memorable Moments:")
            for event in self.journey_stats['key_events'][-5:]:  # Show last 5 events
                print(f"- {event}")
            print()
        
        # Character-specific summary
        if hasattr(player, 'origin'):  # Migrant
            print(f"You began your journey in {player.origin}, carrying dreams of a better life.")
            if player.hope > 70:
                print("Despite the hardships, your spirit remains unbroken.")
            elif player.hope > 30:
                print("The journey has taken its toll, but you persist.")
            else:
                print("The weight of the journey has left deep scars.")
        else:  # Border Patrol
            print(f"After {player.years_of_service} years of service, each day brings new challenges.")
            if player.moral_compass > 70:
                print("You've maintained your humanity while upholding the law.")
            elif player.moral_compass > 30:
                print("The job has forced you to make difficult compromises.")
            else:
                print("The border has changed you in ways you never expected.")
        
        # Thematic quote
        print("\nReflection:")
        self.print_slow(random.choice(self.quotes))
        
        input("\nPress Enter to exit ... ")
    
    def graceful_exit(self, player):
        """Handle graceful exit from the game with journey summary."""
        self.clear_screen()
        print("Preparing your journey summary...\n")
        time.sleep(1)
        self.display_journey_summary(player)
        sys.exit(0)