"""
The Line: A Border Journey
A text-based game inspired by Francisco Cantú's 'The Line Becomes a River'

This game explores the human stories and moral complexities of border migration
and enforcement through interactive storytelling.
"""

import time
import random
import os
from character import Character, Migrant, BorderPatrol
from location import Location
from game_engine import GameEngine
from story import Story


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else "clear")


def print_slow(text, delay=0.03, end='\n'):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print(end=end)


def display_title():
    """Display the game title."""
    title = """
    ╔════════════════════════════════════════════════════════════╗
    ║                                                            ║
    ║                      THE LINE                              ║
    ║                  A Border Journey                          ║
    ║                                                            ║
    ║          Inspired by 'The Line Becomes a River'            ║
    ║                  by Francisco Cantú                        ║
    ║                                                            ║
    ╚════════════════════════════════════════════════════════════╝
    """
    print_slow(title, 0.005)

def intro_page():
    clear_screen()
    display_title()

    print_slow("\t\tWelcome to 'The Line: A Border Journey'\n")
    print_slow("This game explores the human stories and moral complexities of border")
    print_slow("migration through interactive storytelling. I've created this because")
    print_slow("I am interested in coding and, henceforth I felt narrating a story-line")
    print_slow("is something cool and creative that can be done!")
    print()

    print_slow('\nPress Enter to continue ', end='')
    print_slow("... ", delay=0.6, end='')
    input()

def main():
    """Main function to run the game."""
    intro_page()

    # Initialize game components
    story = Story()
    game = GameEngine(story)
    
    # Start the game
    game.start()


if __name__ == "__main__":
    main()