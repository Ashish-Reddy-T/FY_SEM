"""
Embeddings module for 'The Line: A Border Journey'

This module handles the AI interface using Ollama's mxbai-embed-large* model
to create vector representations of game content and enable more natural
interactions through semantic search.

* can use smaller embedding models like nomic-embed-text if you would like to run it faster on your device!
"""

import json
import requests
import numpy as np
from typing import List, Dict, Any, Tuple, Optional



class EmbeddingsEngine:
    """Handles embeddings generation and semantic search using Ollama's API."""
    
    def __init__(self, model_name="mxbai-embed-large", api_url="http://localhost:11434/api/embeddings"):
        """
        Initialize the embeddings engine.
        
        Args:
            model_name (str): Name of the embedding model to use
            api_url (str): URL of the Ollama API endpoint
        """
        self.model_name = model_name
        self.api_url = api_url
        self.command_embeddings = {}
        self.location_embeddings = {}
        self.character_embeddings = {}
        self.item_embeddings = {}
        
    def get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get embedding vector for a text using Ollama's API.
        
        Args:
            text (str): Text to embed
            
        Returns:
            List[float] or None: Embedding vector or None if request failed
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": text
            }
            response = requests.post(self.api_url, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("embedding")
            else:
                print(f"Error getting embedding: {response.status_code}")
                print(f"Response: {response.text}")
                return None
        except Exception as e:
            print(f"Exception when calling Ollama API: {e}")
            return None
    
    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors.
        
        Args:
            vec1 (List[float]): First vector
            vec2 (List[float]): Second vector
            
        Returns:
            float: Cosine similarity (-1 to 1, higher is more similar)
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    
    def initialize_command_embeddings(self):
        """
        Initialize embeddings for standard game commands.
        """
        commands = {
            "look": "examine surroundings, check environment, see what's around, observe area",
            "status": "check health, view inventory, see stats, character status, personal condition",
            "talk": "speak to character, converse with person, chat with npc, communicate",
            "take": "pick up item, grab object, collect thing, acquire item",
            "use": "utilize item, employ object, make use of, activate",
            "move north": "go north, travel northward, head north, walk north",
            "move south": "go south, travel southward, head south, walk south",
            "move east": "go east, travel eastward, head east, walk east",
            "move west": "go west, travel westward, head west, walk west",
            "help": "show commands, display help, list options, assistance",
            "quit": "exit game, end session, stop playing, leave game"
        }
        
        for cmd, description in commands.items():
            embedding = self.get_embedding(description)
            if embedding:
                self.command_embeddings[cmd] = embedding
    
    def initialize_location_embeddings(self, locations):
        """
        Initialize embeddings for game locations.
        
        Args:
            locations (dict): Dictionary of location objects
        """
        for location_id, location in locations.items():
            # Create rich description for embedding
            description = f"{location.name}: {location.description}"
            
            # Add location type specific details
            if hasattr(location, 'water_scarcity'):
                description += f" Desert area with water scarcity level {location.water_scarcity}."
            if hasattr(location, 'patrol_intensity'):
                description += f" Border area with patrol intensity level {location.patrol_intensity}."
            if hasattr(location, 'population'):
                description += f" Settlement with population of approximately {location.population}."
                if hasattr(location, 'services') and location.services:
                    description += f" Services available: {', '.join(location.services)}."
            
            embedding = self.get_embedding(description)
            if embedding:
                self.location_embeddings[location_id] = embedding
    
    def initialize_character_embeddings(self, characters):
        """
        Initialize embeddings for game characters.
        
        Args:
            characters (list): List of character objects
        """
        for character in characters:
            # Create rich description for embedding
            description = f"{character.name}: {character.description}"
            
            # Add character type specific details
            if hasattr(character, 'origin') and hasattr(character, 'motivation'):
                description += f" From {character.origin}. Motivation: {character.motivation}."
            if hasattr(character, 'years_of_service'):
                description += f" {character.years_of_service} years of service in border patrol."
            
            embedding = self.get_embedding(description)
            if embedding:
                self.character_embeddings[character.name.lower()] = embedding
    
    def initialize_item_embeddings(self, items):
        """
        Initialize embeddings for game items.
        
        Args:
            items (list): List of item names
        """
        item_descriptions = {
            "water bottle": "container for drinking water, hydration, liquid container",
            "canned food": "preserved food, nutrition, sustenance, meal",
            "blanket": "cloth for warmth, covering, protection from cold",
            "map": "navigation tool, directions, guide, area layout",
            "flashlight": "portable light, torch, illumination tool",
            "first aid kit": "medical supplies, bandages, treatment, health items",
            "compass": "navigation tool, direction finder, orientation device",
            "family photo": "picture of loved ones, personal memento, memory",
            "money": "currency, cash, funds, financial resource",
            "id papers": "identification documents, passport, legal papers"
        }
        
        for item in items:
            item_lower = item.lower()
            description = item_descriptions.get(item_lower, item)
            embedding = self.get_embedding(description)
            if embedding:
                self.item_embeddings[item_lower] = embedding
    
    def find_best_command(self, user_input: str, threshold: float = 0.7) -> Tuple[Optional[str], float]:
        """
        Find the best matching command for user input using semantic similarity.
        
        Args:
            user_input (str): User's input text
            threshold (float): Minimum similarity threshold to consider a match
            
        Returns:
            Tuple[str, float]: Best matching command and similarity score, or (None, 0)
        """
        if not self.command_embeddings:
            return None, 0
            
        input_embedding = self.get_embedding(user_input)
        if not input_embedding:
            return None, 0
            
        best_command = None
        best_score = 0
        
        for command, cmd_embedding in self.command_embeddings.items():
            similarity = self.cosine_similarity(input_embedding, cmd_embedding)
            if similarity > best_score:
                best_score = similarity
                best_command = command
        
        if best_score >= threshold:
            return best_command, best_score
        return None, 0
    
    def find_best_match(self, user_input: str, embedding_dict: Dict[str, List[float]], 
                       threshold: float = 0.7) -> Tuple[Optional[str], float]:
        """
        Find the best matching entity for user input using semantic similarity.
        
        Args:
            user_input (str): User's input text
            embedding_dict (Dict[str, List[float]]): Dictionary of entity embeddings
            threshold (float): Minimum similarity threshold to consider a match
            
        Returns:
            Tuple[str, float]: Best matching entity and similarity score, or (None, 0)
        """
        if not embedding_dict:
            return None, 0
            
        input_embedding = self.get_embedding(user_input)
        if not input_embedding:
            return None, 0
            
        best_entity = None
        best_score = 0
        
        for entity, entity_embedding in embedding_dict.items():
            similarity = self.cosine_similarity(input_embedding, entity_embedding)
            if similarity > best_score:
                best_score = similarity
                best_entity = entity
        
        if best_score >= threshold:
            return best_entity, best_score
        return None, 0
    
    def find_best_location(self, description: str) -> Tuple[Optional[str], float]:
        """
        Find the best matching location for a description.
        
        Args:
            description (str): Location description
            
        Returns:
            Tuple[str, float]: Best matching location ID and similarity score
        """
        return self.find_best_match(description, self.location_embeddings)
    
    def find_best_character(self, description: str) -> Tuple[Optional[str], float]:
        """
        Find the best matching character for a description.
        
        Args:
            description (str): Character description
            
        Returns:
            Tuple[str, float]: Best matching character name and similarity score
        """
        return self.find_best_match(description, self.character_embeddings)
    
    def find_best_item(self, description: str) -> Tuple[Optional[str], float]:
        """
        Find the best matching item for a description.
        
        Args:
            description (str): Item description
            
        Returns:
            Tuple[str, float]: Best matching item name and similarity score
        """
        return self.find_best_match(description, self.item_embeddings)