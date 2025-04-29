// Game UI Controller
document.addEventListener('DOMContentLoaded', function() {
    const GameUI = {
    // DOM Element references
    elements: {
        screens: {
            titleScreen: document.getElementById('title-screen'),
            characterCreation: document.getElementById('character-creation'),
            gamePlay: document.getElementById('game-play'),
            gameOver: document.getElementById('game-over')
        }
    
    // Initialize the game
    GameUI.init();
});
    
    // Submit command to the game
    async submitCommand() {
        if (!this.state.gameStarted) return;
        
        const command = this.elements.gameplay.commandInput.value.trim();
        if (!command) return;
        
        // Clear the input
        this.elements.gameplay.commandInput.value = '';
        
        // Show the command in the narrative
        this.appendToNarrative(`> ${command}`, 'command');
        
        try {
            const response = await fetch('/command', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ command: command })
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Display the result
                this.appendToNarrative(data.result);
                
                // Update inventory and status
                this.updateStatus(data.game_status);
                
                // Check if game is over
                if (data.game_over) {
                    setTimeout(() => {
                        this.handleGameOver(data);
                    }, 1500);
                }
            } else {
                this.appendToNarrative('Error: ' + data.message);
            }
        } catch (error) {
            console.error('Error processing command:', error);
            this.appendToNarrative('Could not connect to the game server. Please try again later.');
        }
    },
    
    // Update game status display
    updateStatus(statusText) {
        if (statusText) {
            // Parse status text
            const lines = statusText.split('\n');
            
            lines.forEach(line => {
                if (line.includes('Turn:')) {
                    const turn = line.split(':')[1].trim();
                    this.elements.gameplay.turn.textContent = turn;
                }
                else if (line.includes('Health:')) {
                    const health = line.split(':')[1].trim();
                    this.elements.gameplay.health.textContent = health;
                }
                else if (line.includes('Water:')) {
                    const water = line.split(':')[1].trim();
                    this.elements.gameplay.water.textContent = water;
                }
                else if (line.includes('Food:')) {
                    const food = line.split(':')[1].trim();
                    this.elements.gameplay.food.textContent = food;
                }
                else if (line.includes('Hope:')) {
                    const hope = line.split(':')[1].trim();
                    this.elements.gameplay.hope.textContent = hope;
                }
                else if (line.includes('Moral Compass:')) {
                    const moral = line.split(':')[1].trim();
                    this.elements.gameplay.moralCompass.textContent = moral;
                }
                else if (line.includes('Stress:')) {
                    const stress = line.split(':')[1].trim();
                    this.elements.gameplay.stress.textContent = stress;
                }
                else if (line.includes('Location:')) {
                    const location = line.split(':')[1].trim();
                    this.elements.gameplay.location.textContent = location;
                }
                else if (line.includes('Inventory:')) {
                    const inventoryText = line.split(':')[1].trim();
                    const inventory = inventoryText === 'Empty' ? [] : inventoryText.split(', ');
                    this.updateInventory(inventory);
                }
            });
        } else {
            // If no status text provided, fetch status from server
            this.fetchStatus();
        }
    },
    
    // Fetch status from server
    async fetchStatus() {
        try {
            const response = await fetch('/status');
            const data = await response.json();
            
            if (data.status === 'success') {
                this.updateStatus(data.game_status);
            }
        } catch (error) {
            console.error('Error fetching status:', error);
        }
    },
    
    // Update inventory display
    updateInventory(items) {
        const inventoryList = this.elements.gameplay.inventoryList;
        inventoryList.innerHTML = '';
        
        if (items && items.length > 0) {
            items.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item;
                li.addEventListener('click', () => {
                    this.elements.gameplay.commandInput.value = `use ${item}`;
                });
                inventoryList.appendChild(li);
            });
        } else {
            const li = document.createElement('li');
            li.textContent = 'Nothing';
            li.style.fontStyle = 'italic';
            li.style.color = '#999';
            inventoryList.appendChild(li);
        }
        
        this.state.inventory = items || [];
    },
    
    // Clear the narrative area
    clearNarrative() {
        this.elements.gameplay.narrative.innerHTML = '';
    },
    
    // Add text to the narrative area
    appendToNarrative(text, className = '') {
        const narrative = this.elements.gameplay.narrative;
        
        // Split text into paragraphs
        const paragraphs = text.split('\n').filter(p => p.trim());
        
        // Create elements for each paragraph
        paragraphs.forEach(paragraph => {
            const p = document.createElement('p');
            p.textContent = paragraph;
            if (className) p.classList.add(className);
            narrative.appendChild(p);
        });
        
        // Scroll to bottom
        narrative.scrollTop = narrative.scrollHeight;
    },
    
    // Handle game over
    handleGameOver(data) {
        // Update game over screen with journey summary
        this.elements.gameOver.endingMessage.textContent = data.ending_message;
        
        // Update summary stats
        const summary = data.journey_summary;
        this.elements.gameOver.summaryDistance.textContent = summary.distance;
        this.elements.gameOver.summaryLives.textContent = summary.lives;
        this.elements.gameOver.summaryChoices.textContent = summary.choices;
        this.elements.gameOver.summaryTrauma.textContent = summary.trauma;
        
        // Update events list
        const eventsList = this.elements.gameOver.summaryEvents;
        eventsList.innerHTML = '';
        
        summary.events.forEach(event => {
            const li = document.createElement('li');
            li.textContent = event;
            eventsList.appendChild(li);
        });
        
        // Set epilogue based on ending type
        let epilogue = '';
        
        switch (data.ending_type) {
            case 'success':
                epilogue = "You've made it to Tucson, but your journey is far from over. Like many migrants who cross the border, you now face the challenges of building a life in a new country.";
                break;
            case 'detained':
                epilogue = "In detention, you become one of thousands processed through America's immigration system. Your future is uncertain - you may be deported, or you may be granted asylum.";
                break;
            case 'death':
                epilogue = "Your journey ends in the borderlands, as it does for hundreds of migrants each year. The desert is an unforgiving place, and the border crossing claims many lives.";
                break;
            case 'timeout':
                epilogue = "Your resources depleted, your strength gone, your journey cannot continue. The border region has claimed another victim of its harsh realities.";
                break;
            default:
                epilogue = "Your journey along the border has ended, but the larger story continues.";
        }
        
        this.elements.gameOver.epilogueText.textContent = epilogue;
        
        // Switch to game over screen
        this.showScreen('game-over');
    },
    
    // Reset the game
    async resetGame() {
        try {
            // Reset game on server
            await fetch('/reset', {
                method: 'POST'
            });
            
            // Reset UI
            this.state.gameStarted = false;
            this.state.inventory = [];
            
            // Clear narrative
            this.clearNarrative();
            
            // Reset character creation form
            this.elements.characterCreation.characterName.value = '';
            this.elements.characterCreation.origin.value = '';
            this.elements.characterCreation.motivation.value = '';
            this.elements.characterCreation.years.value = 5;
            
            // Start new game session
            await this.startGame();
            
            // Show title screen
            this.showScreen('title');
        } catch (error) {
            console.error('Error resetting game:', error);
            alert('Could not reset the game. Please refresh the page.');
        }
    },
        buttons: {
            startGame: document.getElementById('start-game'),
            createCharacter: document.getElementById('create-character'),
            submitCommand: document.getElementById('submit-command'),
            playAgain: document.getElementById('play-again'),
            suggestionBtns: document.querySelectorAll('.suggestion-btn')
        },
        characterCreation: {
            choiceContainers: document.querySelectorAll('.choice'),
            characterName: document.getElementById('character-name'),
            origin: document.getElementById('origin'),
            motivation: document.getElementById('motivation'),
            years: document.getElementById('years'),
            migrantFields: document.getElementById('migrant-fields'),
            patrolFields: document.getElementById('patrol-fields')
        },
        gameplay: {
            narrative: document.getElementById('narrative'),
            commandInput: document.getElementById('command-input'),
            inventoryList: document.getElementById('inventory-list'),
            location: document.querySelector('#location .value'),
            health: document.querySelector('#health .value'),
            water: document.querySelector('#water .value'),
            food: document.querySelector('#food .value'),
            hope: document.querySelector('#hope .value'),
            moralCompass: document.querySelector('#moral-compass .value'),
            stress: document.querySelector('#stress .value'),
            turn: document.querySelector('#turn .value'),
            migrantStats: document.querySelectorAll('.migrant-stat'),
            patrolStats: document.querySelectorAll('.patrol-stat')
        },
        gameOver: {
            endingMessage: document.getElementById('ending-message'),
            summaryDistance: document.getElementById('summary-distance'),
            summaryLives: document.getElementById('summary-lives'),
            summaryChoices: document.getElementById('summary-choices'),
            summaryTrauma: document.getElementById('summary-trauma'),
            summaryEvents: document.getElementById('summary-events'),
            epilogueText: document.getElementById('epilogue-text')
        }
    },

    // Game state
    state: {
        sessionId: null,
        characterType: 'migrant',
        gameStarted: false,
        currentScreen: 'title',
        inventory: []
    },

    // Initialize the game UI
    init() {
        this.bindEvents();
        this.showScreen('title');
        this.startGame();
    },
    
    // Start the game and create a session
    async startGame() {
        try {
            const response = await fetch('/start', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                this.state.sessionId = data.session_id;
                console.log('Game session started:', data.session_id);
            } else {
                this.appendToNarrative('Error starting game: ' + data.message);
            }
        } catch (error) {
            console.error('Error starting game:', error);
            this.appendToNarrative('Could not connect to the game server. Please try again later.');
        }
    },

    // Bind event listeners
    bindEvents() {
        // Navigation buttons
        this.elements.buttons.startGame.addEventListener('click', () => this.showScreen('character-creation'));
        this.elements.buttons.createCharacter.addEventListener('click', () => this.createCharacter());
        this.elements.buttons.submitCommand.addEventListener('click', () => this.submitCommand());
        this.elements.buttons.playAgain.addEventListener('click', () => this.resetGame());
        
        // Make sure the command input is focused when the game starts
        document.addEventListener('keydown', (e) => {
            if (this.state.currentScreen === 'game-play' && 
                e.key !== 'Tab' && 
                document.activeElement !== this.elements.gameplay.commandInput) {
                this.elements.gameplay.commandInput.focus();
            }
        });

        // Character creation choices
        this.elements.characterCreation.choiceContainers.forEach(choice => {
            choice.addEventListener('click', () => {
                this.selectCharacterType(choice);
            });
        });
        
        // Select migrant by default
        this.selectCharacterType(document.querySelector('.choice[data-value="migrant"]'));

        // Command input enter key
        this.elements.gameplay.commandInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.submitCommand();
            }
        });

        // Suggestion buttons
        this.elements.buttons.suggestionBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const command = btn.getAttribute('data-command');
                this.elements.gameplay.commandInput.value = command;
                this.submitCommand();
            });
        });
    },
    
    // Switch between screens
    showScreen(screenName) {
        // Hide all screens
        Object.values(this.elements.screens).forEach(screen => {
            screen.classList.remove('active');
        });
        
        // Show the selected screen
        this.elements.screens[screenName + 'Screen'].classList.add('active');
        this.state.currentScreen = screenName;
        
        // Special actions for specific screens
        if (screenName === 'game-play') {
            setTimeout(() => {
                this.elements.gameplay.commandInput.focus();
            }, 100);
        }
    },
    
    // Select character type (migrant or patrol)
    selectCharacterType(choiceElement) {
        // Remove selection from all choices
        this.elements.characterCreation.choiceContainers.forEach(choice => {
            choice.classList.remove('selected');
        });
        
        // Add selection to the clicked choice
        choiceElement.classList.add('selected');
        
        // Get character type value
        this.state.characterType = choiceElement.getAttribute('data-value');
        
        // Show the appropriate fields
        if (this.state.characterType === 'migrant') {
            this.elements.characterCreation.migrantFields.classList.remove('hidden');
            this.elements.characterCreation.patrolFields.classList.add('hidden');
        } else {
            this.elements.characterCreation.migrantFields.classList.add('hidden');
            this.elements.characterCreation.patrolFields.classList.remove('hidden');
        }
    },
    
    // Create character and start the game
    async createCharacter() {
        // Check if we have a session ID
        if (!this.state.sessionId) {
            await this.startGame();
        }
        
        const name = this.elements.characterCreation.characterName.value.trim();
        
        if (!name) {
            alert('Please enter a character name');
            return;
        }
        
        // Prepare character data
        const characterData = {
            name: name,
            character_type: this.state.characterType
        };
        
        // Add type-specific information
        if (this.state.characterType === 'migrant') {
            characterData.origin = this.elements.characterCreation.origin.value || 'Central Mexico';
            characterData.motivation = this.elements.characterCreation.motivation.value || 'Economic opportunity';
        } else {
            characterData.years = this.elements.characterCreation.years.value || 5;
        }
        
        try {
            const response = await fetch('/create_character', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(characterData)
            });
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Show the appropriate stats based on character type
                if (this.state.characterType === 'migrant') {
                    this.elements.gameplay.migrantStats.forEach(stat => stat.classList.remove('hidden'));
                    this.elements.gameplay.patrolStats.forEach(stat => stat.classList.add('hidden'));
                } else {
                    this.elements.gameplay.migrantStats.forEach(stat => stat.classList.add('hidden'));
                    this.elements.gameplay.patrolStats.forEach(stat => stat.classList.remove('hidden'));
                }
                
                // Update location and description
                this.elements.gameplay.location.textContent = data.location;
                this.clearNarrative();
                this.appendToNarrative(data.description);
                
                // Switch to gameplay screen
                this.showScreen('game-play');
                this.state.gameStarted = true;
                
                // Update inventory
                this.updateInventory([]);
                
                // Update status
                this.updateStatus();
            } else {
                alert('Error creating character: ' + data.message);
            }
        } catch (error) {
            console.error('Error creating character:', error);
            alert('Could not connect to the game server. Please try again later.');
        }
    },