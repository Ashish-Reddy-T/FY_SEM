from flask import Flask, render_template, request, jsonify, session
from game_engine import GameEngine
from story import Story
import os
import secrets
import json

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Game sessions storage
game_sessions = {}

@app.route('/')
def index():
    """Render the home page"""
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start_game():
    """Initialize a new game session"""
    # Generate a unique session ID
    session_id = secrets.token_hex(8)
    session['session_id'] = session_id
    
    # Create a new game instance
    story = Story()
    game = GameEngine(story)
    
    # Store the game instance
    game_sessions[session_id] = {
        'game': game,
        'story': story,
        'state': 'intro'  # Current state of the game flow
    }
    
    return jsonify({
        'status': 'success',
        'session_id': session_id,
        'message': "Welcome to 'The Line: A Border Journey'",
        'state': 'intro'
    })

@app.route('/create_character', methods=['POST'])
def create_character():
    """Create a character based on player input"""
    session_id = session.get('session_id')
    if not session_id or session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session'})
    
    data = request.json
    name = data.get('name', '').strip()
    character_type = data.get('character_type', 'migrant')
    
    game_data = game_sessions[session_id]
    game = game_data['game']
    
    # Additional character info
    extra_info = {}
    if character_type == 'migrant':
        extra_info['origin'] = data.get('origin', 'Central Mexico')
        extra_info['motivation'] = data.get('motivation', 'Economic opportunity')
    else:  # Border Patrol
        try:
            extra_info['years_of_service'] = int(data.get('years', 5))
        except:
            extra_info['years_of_service'] = 5
    
    # Initialize game world and player
    game.create_world()
    game.create_characters()
    game.create_player(name, character_type, **extra_info)
    game.load_events()
    game.initialize_embeddings()
    
    # Update state
    game_data['state'] = 'playing'
    game_data['story'].display_intro(game.current_location.name)
    
    # Get initial location description
    location_desc = game.current_location.describe(detailed=True)
    
    return jsonify({
        'status': 'success',
        'message': "Character created successfully",
        'location': game.current_location.name,
        'description': location_desc,
        'state': 'playing'
    })

@app.route('/command', methods=['POST'])
def process_command():
    """Process a player command"""
    session_id = session.get('session_id')
    if not session_id or session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session'})
    
    data = request.json
    command = data.get('command', '').strip()
    
    game_data = game_sessions[session_id]
    game = game_data['game']
    
    # Process command
    result = game.process_command(command)
    
    # Check if game is over
    game_over = game.game_over
    ending = game.ending if game_over else None
    
    # Get updated status
    status = game.get_status() if not game_over else "Game Over"
    
    response = {
        'status': 'success',
        'result': result,
        'game_status': status,
        'game_over': game_over,
        'state': 'ended' if game_over else 'playing'
    }
    
    # Add ending information if game is over
    if game_over:
        game_data['state'] = 'ended'
        ending_msg = game.get_ending_message()
        ending_type = game.ending
        
        # Get journey summary
        game_data['story'].display_journey_summary(game.player)
        journey_summary = {
            'distance': game_data['story'].journey_stats['distance_traveled'],
            'lives': game_data['story'].journey_stats['lives_impacted'],
            'choices': game_data['story'].journey_stats['moral_choices_made'],
            'trauma': game_data['story'].journey_stats['trauma_experienced'],
            'events': game_data['story'].journey_stats['key_events'][-5:] if game_data['story'].journey_stats['key_events'] else []
        }
        
        response.update({
            'ending_message': ending_msg,
            'ending_type': ending_type,
            'journey_summary': journey_summary
        })
    
    return jsonify(response)

@app.route('/status', methods=['GET'])
def get_status():
    """Get the current game status"""
    session_id = session.get('session_id')
    if not session_id or session_id not in game_sessions:
        return jsonify({'status': 'error', 'message': 'Invalid session'})
    
    game_data = game_sessions[session_id]
    game = game_data['game']
    
    return jsonify({
        'status': 'success',
        'game_status': game.get_status(),
        'state': game_data['state'],
        'location': game.current_location.name if hasattr(game, 'current_location') and game.current_location else None
    })

@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game session"""
    session_id = session.get('session_id')
    if session_id and session_id in game_sessions:
        del game_sessions[session_id]
    
    session.clear()
    
    return jsonify({
        'status': 'success',
        'message': "Game reset successfully"
    })

# Clean up expired sessions periodically (could be expanded)
@app.before_request
def cleanup_sessions():
    """Simple cleanup of idle sessions"""
    # In a production app, you'd want more sophisticated session management
    if len(game_sessions) > 100:  # Arbitrary limit
        # Remove oldest sessions
        oldest = list(game_sessions.keys())[:20]
        for key in oldest:
            if key in game_sessions:
                del game_sessions[key]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)