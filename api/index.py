from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import sys
import os

# Add paths
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), 'web_app'))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Import modules
from llm_client import HorrorLLMClient
from conch_character import conch
from tts_client import ConchTTSClient

app = Flask(__name__,
            template_folder=os.path.join(os.path.dirname(__file__), '..', 'web_app', 'templates'),
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'web_app', 'static'))
CORS(app)

# Initialize clients
llm_client = None
tts_client = None
welcome_audio_cache = None

def init_llm():
    global llm_client
    try:
        llm_client = HorrorLLMClient()
        print(f"✓ LLM client initialized with backend: {llm_client.backend}")
    except Exception as e:
        print(f"Error initializing LLM: {e}")
        llm_client = None

def init_tts():
    global tts_client
    try:
        tts_client = ConchTTSClient()
        if tts_client.enabled:
            print(f"✓ Murf TTS enabled - Voice: {tts_client.voice_id} ({tts_client.style})")
        else:
            print("ℹ Murf TTS disabled")
    except Exception as e:
        print(f"Warning: Could not initialize TTS: {e}")
        tts_client = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint to verify environment setup"""
    import os
    return jsonify({
        'status': 'ok',
        'llm_client_initialized': llm_client is not None,
        'llm_backend': llm_client.backend if llm_client else None,
        'tts_client_initialized': tts_client is not None,
        'tts_enabled': tts_client.enabled if tts_client else False,
        'env_check': {
            'ANTHROPIC_API_KEY': 'set' if os.getenv('ANTHROPIC_API_KEY') else 'missing',
            'MURF_API_KEY': 'set' if os.getenv('MURF_API_KEY') else 'missing',
            'LLM_BACKEND': os.getenv('LLM_BACKEND', 'not set'),
            'TTS_ENABLED': os.getenv('TTS_ENABLED', 'not set')
        }
    })

@app.route('/api/welcome', methods=['GET'])
def get_welcome():
    global welcome_audio_cache
    welcome_message = conch.get_welcome_message()

    if welcome_audio_cache:
        return jsonify({
            'message': welcome_message,
            'audio_url': welcome_audio_cache,
            'success': True
        })

    audio_url = None
    if tts_client and tts_client.enabled:
        try:
            audio_path = tts_client.generate_speech(welcome_message)
            if audio_path:
                import uuid
                audio_id = str(uuid.uuid4())
                app.config.setdefault('audio_cache', {})[audio_id] = audio_path
                audio_url = f"/api/audio/{audio_id}"
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
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()

        if not user_message:
            return jsonify({'error': 'Empty message', 'success': False}), 400

        if user_message.lower() in ['exit', 'quit', 'bye', 'goodbye']:
            return jsonify({
                'message': conch.get_goodbye_message(),
                'is_goodbye': True,
                'success': True
            })

        if llm_client:
            response = llm_client.generate_response(
                user_message=user_message,
                system_prompt=conch.system_prompt
            )
        else:
            response = "The conch is currently unavailable. Please try again later."

        response = clean_response(response)

        audio_url = None
        if tts_client and tts_client.enabled:
            try:
                audio_path = tts_client.generate_speech(response)
                if audio_path:
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
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/audio/<audio_id>', methods=['GET'])
def get_audio(audio_id):
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
    import re
    response = re.sub(r'\*[^*]+\*', '', response)
    response = response.replace('*', '')
    response = response.replace('...', '')
    response = ' '.join(response.split())
    response = response.strip()
    sentences = re.split(r'(?<=[.!?])\s+', response)
    if len(sentences) > 3:
        response = ' '.join(sentences[:3])
    if response and response[-1] not in '.!?':
        response += '.'
    return response

# Initialize on import
init_llm()
init_tts()
