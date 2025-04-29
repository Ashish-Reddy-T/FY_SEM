# The Line: A Border Journey - Player Manual

## 1. Introduction

Welcome to "The Line: A Border Journey," a text-based narrative game inspired by Francisco Cantú's book, "The Line Becomes a River". This game explores the human stories, moral complexities, and harsh realities faced by those who cross the US-Mexico border and those who patrol it.

You will step into the shoes of either a Migrant seeking a new life or a Border Patrol agent enforcing the line. Your choices, interactions, and resource management will determine your path through the challenging borderlands. The game aims to immerse you in the themes of humanity, duty, compassion, trauma, and the profound impact of the border on individual lives.

## 2. Getting Started

### Requirements:

* Python 3 installed.
* Required Python libraries: `requests`, `numpy`. Install them using pip:
    ```bash
    pip install -r requirements.txt
    ```
* **(Optional AI Feature)**: An Ollama instance running locally (usually at `http://localhost:11434`) with the `nomic-embed-text` model available, if you want to use the natural language command processing. If Ollama isn't running or the model isn't found, the game will gracefully fall back to standard text commands.

### Running the Game:

1.  Navigate to the game's directory in your terminal.
2.  Run the main script (assuming it's `main.py` or `laa.py`):
    ```bash
    python main.py
    ```
    (Replace `main.py` with `laa.py` if that's your main file name).

### Character Creation:

* The game will first ask you to choose your role: **Migrant** or **Border Patrol**.
* You will then enter your character's name.
* Depending on your chosen role, you'll provide additional details:
    * **Migrant**: Your place of origin and your motivation for the journey.
    * **Border Patrol**: Your years of service.
* Based on your role, you will start with some basic inventory items.

## 3. Core Gameplay Mechanics

### Turns:

* The game progresses in turns. Each significant action, like moving between locations, taking an item, or using an item, typically advances the turn count.
* There's a maximum turn limit (currently 30). If you exceed this, your journey ends.

### Locations & Navigation:

* The game world consists of different locations connected by paths (North, South, East, West).
* Use the `move [direction]` command (e.g., `move north`, `move s`) to travel between locations.
* Each location has a name, description, danger level, and potentially characters, items, and events.
* Some location types have special characteristics:
    * **Desert**: High danger, scarce water. Consuming resources happens faster here.
    * **Border**: Moderate to high danger, high patrol intensity (chance of encounters).
    * **Settlement**: Lower danger, potential population, may offer services like food, shelter, or medical aid.
* Use the `look` command to get a detailed description of your current location, including paths, characters, items, and danger level.

### Interaction:

* You interact with the world using text commands (see Section 5).
* You can interact with characters (`talk`) and objects (`take`, `use`).

### Events:

* As you move and progress through turns, random events can occur. These can include:
    * **Encounter Events**: Meeting other migrants, patrol agents, or locals. These can affect your stats (like Hope or Stress).
    * **Resource Events**: Finding or losing essential resources like water, food, or items.
    * **Moral Events**: Situations presenting you with a difficult choice. Your decision has consequences, affecting your stats (Hope, Moral Compass) and potentially setting story flags that influence later events.
    * **Narrative/Trauma Events**: Short descriptive events adding flavor, atmosphere, or reflecting the psychological toll of the journey. These are recorded in your journey summary.

## 4. Character Roles & Stats

Your character has several stats that track your condition and progress. Some stats are specific to your chosen role (Migrant or Border Patrol). Use the `status` command to check your current stats.

### Common Stats:

* **Health (0-100)**: Your physical well-being. Reaching 0 health ends the game. Health can be lost due to lack of resources, harsh environments, or specific events. It can be regained using items like a "First Aid Kit".
* **Inventory**: A list of items you are carrying. Items can be found in locations (`take`) or obtained through events.
* **Location**: Your current position in the game world.
* **Story Flags**: Internal markers set by events or choices that can affect future possibilities (not directly visible via `status`).

### Migrant Stats:

* **Water (0-100)**: Your hydration level. Decreases each turn, faster in the Desert. Low water drains health. Can be replenished using a "Water Bottle" or finding water sources.
* **Food (0-100)**: Your hunger level. Decreases each turn. Low food drains health. Can be replenished using "Canned Food" or finding food sources.
* **Hope (0-100)**: Your mental resilience and optimism. Affected by events, encounters, moral choices, and using items like a "Family Photo".

### Border Patrol Stats:

* **Moral Compass (0-100)**: Represents your adherence to strict protocol versus acting on personal conscience. Affected by moral choices and actions taken during encounters.
* **Stress (0-100)**: Your mental strain from the job. Increases with encounters. High stress can negatively impact your health.

## 5. Commands

You interact with the game by typing commands at the `>` prompt.

### Basic Commands:

* `look` or `examine`: Get a detailed description of your current location, including exits, characters, and items.
* `status` or `inventory`: Display your current health, resources (Water, Food, Hope, etc. if applicable), and inventory items.
* `move [direction]` or `go [direction]`: Move to an adjacent location. Directions are `north`, `south`, `east`, `west`. You can also use shortcuts: `n`, `s`, `e`, `w`. (e.g., `move north`, `go w`).
* `take [item name]` or `get [item name]`: Pick up an item from your current location and add it to your inventory (e.g., `take water bottle`).
* `use [item name]`: Use an item from your inventory. This may restore stats, provide information, or have other effects (e.g., `use first aid kit`). See Section 6 for item effects.
* `talk [character name]` or `speak [character name]`: Interact with a character present in your location (e.g., `talk manuel`).
* `help`: Display a list of available commands and information about AI command input (if enabled).
* `quit` or `exit`: Exit the game. You will be asked for confirmation and shown a journey summary before quitting.

### AI Natural Language Commands (Optional):

* If the AI embedding engine is active (requires Ollama setup), you can try using more natural phrases instead of the exact commands. The game will attempt to understand your intent.
* Examples:
    * `"check my health"` instead of `status`
    * `"speak with Agent Hernandez"` instead of `talk agent hernandez`
    * `"grab the map"` instead of `take map`
    * `"drink water"` instead of `use water bottle`
    * `"head north"` instead of `move north`
* If the AI doesn't understand or makes a mistake, you can always use the standard commands listed above. The `help` command will indicate if AI processing is active.

## 6. Items and Their Uses

You can find various items during your journey. Use the `use [item name]` command to activate their effects.

* **Water Bottle**: Restores Water (+30).
* **Canned Food**: Restores Food (+40).
* **First Aid Kit**: Restores Health (+25).
* **Map**: Provides information about connected locations.
* **Flashlight**: Illuminates surroundings (potential use in specific dark events/locations).
* **Compass**: Confirms cardinal directions (potential use if "lost").
* **Family Photo**: Restores Hope (+15) for Migrant characters.
* **Blanket**: Provides comfort (potential future use against cold).
* **Money**: Currency (potential use in specific interactions/events).
* **ID Papers**: Identification (potential use in specific interactions/events).
* **Radio**: (Border Patrol only) Listen to radio chatter, potentially gaining information.

*(Note: Some item effects might be situational or primarily narrative).*

## 7. Ending the Game

Your journey can end in several ways:

* **Success (Migrant)**: Reaching the final destination (Tucson).
* **Detained (Migrant)**: Being apprehended and sent to the Detention Center.
* **Death**: Your Health drops to 0 or below.
* **Timeout**: You exceed the maximum number of turns (30).
* **Quit**: You choose to exit the game early.

Upon game completion (or quitting), you will be presented with a **Journey Summary** detailing your stats, key events experienced, and a reflection based on your character's final state. An epilogue reflecting your specific ending will also be shown.

## 8. Tips for Playing

* **Read Carefully**: Pay attention to location descriptions, character dialogue, and event text. They provide crucial information and atmosphere.
* **Manage Resources (Migrant)**: Keep a close eye on your Water and Food levels, especially in the Desert. Use items wisely.
* **Check Status Often**: Use the `status` command regularly to monitor your health and resources.
* **Consider Your Choices**: Moral Events present difficult dilemmas. Your choices impact your character's stats (Hope, Moral Compass) and may have unseen long-term consequences via story flags.
* **Explore**: Use `look` frequently to find items or identify characters to talk to. Check paths revealed by `look` or the `map`.
* **Use `help`**: If you're unsure about commands, type `help`.

Good luck on your journey through "The Line."