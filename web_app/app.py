"""
The Conch Web Application
Flask backend serving the conch chat experience with Murf TTS
"""

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import existing modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from llm_client import HorrorLLMClient
from conch_character import conch
from tts_client import ConchTTSClient

app = Flask(__name__)
CORS(app)

# Initialize clients
llm_client = None
tts_client = None
welcome_audio_cache = None  # Cache for welcome message audio

def init_llm():
    """Initialize the LLM client."""
    global llm_client
    try:
        llm_client = HorrorLLMClient()
        print(f"✓ LLM client initialized with backend: {llm_client.backend}")
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        llm_client = None

def init_tts():
    """Initialize the TTS client."""
    global tts_client
    try:
        tts_client = ConchTTSClient()
        if tts_client.enabled:
            print(f"✓ Murf TTS enabled - Voice: {tts_client.voice_id} ({tts_client.style})")
        else:
            print("ℹ Murf TTS disabled (set TTS_ENABLED=true in .env to enable)")
    except Exception as e:
        print(f"Warning: Could not initialize TTS: {e}")
        tts_client = None


@app.route('/')
def index():
    """Serve the main chat interface."""
    return render_template('index.html')


@app.route('/api/welcome', methods=['GET'])
def get_welcome():
    """Get the welcome message with audio."""
    global welcome_audio_cache

    welcome_message = conch.get_welcome_message()

    # Use cached audio URL if available
    if welcome_audio_cache:
        return jsonify({
            'message': welcome_message,
            'audio_url': welcome_audio_cache,
            'success': True
        })

    # Generate audio for welcome message if TTS is enabled (first time only)
    audio_url = None
    if tts_client and tts_client.enabled:
        try:
            audio_path = tts_client.generate_speech(welcome_message)
            if audio_path:
                # Store audio path with unique ID
                import uuid
                audio_id = str(uuid.uuid4())
                app.config.setdefault('audio_cache', {})[audio_id] = audio_path
                audio_url = f"/api/audio/{audio_id}"
                # Cache the welcome audio URL for future requests
                welcome_audio_cache = audio_url
                print(f"✓ Welcome message audio cached: {audio_id}")
        except Exception as e:
            print(f"TTS generation error for welcome message: {e}")

    return jsonify({
        'message': welcome_message,
        'audio_url': audio_url,
        'success': True
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages."""
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({
                'error': 'Empty message',
                'success': False
            }), 400

        # Check for exit commands
        if user_message.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            return jsonify({
                'message': conch.get_goodbye_message(),
                'is_goodbye': True,
                'success': True
            })

        # Generate response using LLM client
        if llm_client:
            response = llm_client.generate_response(
                user_message=user_message,
                system_prompt=conch.system_prompt
            )
        else:
            response = "The conch is currently unavailable. Please try again later."

        # Clean the response (remove asterisks, ellipses, etc.)
        response = clean_response(response)

        # Generate audio if TTS is enabled
        audio_url = None
        if tts_client and tts_client.enabled:
            try:
                audio_path = tts_client.generate_speech(response)
                if audio_path:
                    # Store audio path with unique ID
                    import uuid
                    audio_id = str(uuid.uuid4())
                    app.config.setdefault('audio_cache', {})[audio_id] = audio_path
                    audio_url = f"/api/audio/{audio_id}"
            except Exception as e:
                print(f"TTS generation error: {e}")

        return jsonify({
            'message': response,
            'audio_url': audio_url,
            'success': True
        })

    except Exception as e:
        print(f"Error in chat endpoint: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500


@app.route('/api/audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
    """Serve generated audio file."""
    try:
        audio_cache = app.config.get('audio_cache', {})
        audio_path = audio_cache.get(audio_id)

        if audio_path and os.path.exists(audio_path):
            return send_file(audio_path, mimetype='audio/mpeg')
        else:
            return jsonify({'error': 'Audio not found'}), 404

    except Exception as e:
        print(f"Error serving audio: {e}")
        return jsonify({'error': str(e)}), 500


def clean_response(response: str) -> str:
    """
    Clean the LLM response to enforce formatting rules.

    Args:
        response: Raw response from LLM

    Returns:
        Cleaned response
    """
    import re

    # Remove anything between asterisks (stage directions)
    response = re.sub(r'\*[^*]+\*', '', response)

    # Remove standalone asterisks
    response = response.replace('*', '')

    # Remove ellipses
    response = response.replace('...', '')

    # Clean up whitespace
    response = ' '.join(response.split())
    response = response.strip()

    # Limit to first 3 sentences maximum
    sentences = re.split(r'(?<=[.!?])\s+', response)
    if len(sentences) > 3:
        response = ' '.join(sentences[:3])

    # If still no ending punctuation, add period
    if response and response[-1] not in '.!?':
        response += '.'

    return response


if __name__ == '__main__':
    # Initialize clients
    init_llm()
    init_tts()

    # Run the Flask app
    print("\n=== THE CONCH WEB APPLICATION ===")
    print("Starting server...")
    print("Open http://localhost:8080 in your browser\n")

    app.run(debug=True, host='0.0.0.0', port=8080)
