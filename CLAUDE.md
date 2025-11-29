# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**The Conch** is a futuristic chatbot featuring an intelligent conch shell that serves as a cultural preservation device in Amphitopia, an underwater colony beneath the Arabian Sea in 2080. It bridges the knowledge gap between generations by explaining land-based concepts to those who only know life underwater.

The project consists of two versions:
1. **CLI Version** (`main.py`) - Pure Python terminal application with no build process
2. **Web Version** (`web_app/`) - Flask-based web application with professional UI, voice features, and deployable to Vercel

## Running the Application

### CLI Version
```bash
# Install dependencies (only needed once)
pip3 install -r requirements.txt

# Run the CLI application
python3 main.py
```

The CLI app runs in demo mode by default (no API keys needed). Exit with `exit`, `quit`, `bye`, `goodbye` or Ctrl+C.

### Web Version
```bash
# Navigate to web app directory
cd web_app

# Install dependencies (if not already installed)
pip3 install -r ../requirements.txt

# Run the Flask web server
python3 app.py
```

The web app runs at `http://localhost:8080`. Features:
- Professional black/white terminal aesthetic
- Montserrat typography
- Real-time voice synthesis (Murf API - Ryan voice)
- Speech-to-text input (5-second recording with countdown)
- Simultaneous text typing and voice playback
- Start overlay to enable audio autoplay
- Full-screen responsive UI

## Configuration

Backend selection is controlled via `.env` file (copy from `.env.example`):

- **demo**: Pre-written contextual conch responses (default, no setup)
- **huggingface**: HuggingFace Inference API (requires `HUGGINGFACE_API_KEY`)
- **ollama**: Local LLM (requires Ollama running: `ollama run llama2`)
- **openai**: OpenAI API (requires `OPENAI_API_KEY`)
- **anthropic**: Anthropic Claude API (requires `ANTHROPIC_API_KEY`)

Set `LLM_BACKEND=<backend>` in `.env` to switch backends.

## Architecture

### CLI Version Architecture

#### Five-Component Design

1. **main.py** - CLI interface and application orchestration
   - `ConchChatApp` class manages the UI, chat loop, and user interaction
   - `slow_print()` creates atmospheric typing effects (0.04s per character)
   - Color scheme: cyan (conch), white (user), grey50 (system), red (errors)
   - Supports both text input and speech-to-text input (press 's' + Enter to speak)

2. **llm_client.py** - Multi-backend LLM abstraction layer
   - `HorrorLLMClient` implements Strategy pattern for 5 backends (demo, huggingface, ollama, openai, anthropic)
   - Graceful fallback: All backends fall back to demo mode if initialization fails
   - Backend methods: `_generate_demo_response()`, `_generate_huggingface_response()`, `_generate_ollama_response()`, `_generate_openai_response()`, `_generate_anthropic_response()`
   - Demo mode uses keyword matching for contextual pre-written conch responses
   - API parameters: `max_tokens=150` (allows 2-3 sentences including follow-up question), `temperature=0.8`

3. **conch_character.py** - Character definition and system prompts
   - Singleton `ConchCharacter` instance defines personality, backstory, and tone
   - System prompt enforces: wise educational tone, 2-3 sentence responses with follow-up questions, creative land-to-water translations, no emojis/slang
   - Character is a cultural preservation entity (not "device"), never breaks character or reveals AI nature
   - Welcome message ends with: "What would you like to know about the surface world?"
   - **CRITICAL REQUIREMENT**: All responses MUST end with engaging follow-up questions to maintain natural conversation flow
   - **MANDATORY**: Every response must end with a question mark (?) - no exceptions
   - Follow-up questions should be relevant to the concept explained and invite deeper engagement
   - System prompt includes explicit examples showing CORRECT (with questions) vs WRONG (without questions) formats
   - Response structure enforced: Definition → Context → Follow-up Question

4. **tts_client.py** - Text-to-speech voice synthesis (optional)
   - Uses Murf API for high-quality AI voice output
   - Configurable voice ID, style, and model
   - Audio playback runs in background thread while text displays
   - Gracefully handles playback interrupts (Ctrl+C)

5. **speech_to_text.py** - Speech-to-text voice input (optional)
   - Uses OpenAI Whisper (local, free, no API key needed)
   - Records audio with visual progress bar and countdown
   - Transcribes speech to text locally
   - Configurable model size: tiny, base (default), small, medium, large
   - SSL certificate handling for macOS compatibility

#### Key Design Patterns

- **Strategy Pattern**: Multiple LLM backend implementations with unified interface
- **Singleton**: Single `ConchCharacter` instance used throughout
- **Graceful Degradation**: All backend failures fall back to demo mode
- **Separation of Concerns**: UI (main), character (conch_character), backend logic (llm_client)

### Web Version Architecture

#### Four-Component Design

1. **app.py** - Flask backend server
   - Serves main HTML interface via `render_template()`
   - `/api/welcome` endpoint: Returns welcome message with cached audio URL
   - `/api/chat` endpoint: Handles user messages, generates LLM responses, creates TTS audio
   - `/api/audio/<audio_id>` endpoint: Serves MP3 audio files
   - Uses same `HorrorLLMClient`, `ConchCharacter`, and `ConchTTSClient` from CLI version
   - Audio caching system: Welcome message audio cached globally, chat audio cached with UUID
   - Port: 8080 (configurable)
   - Debug mode enabled for development

2. **templates/index.html** - Main web interface
   - Full-screen container with header, chat area, and input section
   - Start overlay: "ENTER ARCHIVE" button to enable audio autoplay (browser requirement)
   - Chat container: Displays welcome message and conversation history
   - Input area: Text input, SPEAK button (voice input), SEND button
   - Typing indicator template for loading states
   - Clean, minimal HTML structure

3. **static/style.css** - Professional black/white terminal aesthetic
   - Color scheme: Pure black (`#000000`), white (`#ffffff`), grays for accents
   - Montserrat font family (Google Fonts) - weights 400, 500, 600, 700
   - Full-screen layout (no max-width container)
   - Terminal scanline effect overlay (subtle)
   - Message styling: White borders for Conch, gray borders for user
   - Typing animation: Slide-in effect for messages
   - Responsive design: Adapts to mobile (stacked buttons, adjusted font sizes)
   - Start overlay: Centered fullscreen splash with fade-out transition
   - Custom scrollbar styling

4. **static/script.js** - Frontend logic and interactivity
   - **Audio Management**:
     - `playAudio()`: Plays Murf-generated MP3, disables SPEAK button during playback
     - `currentAudio.onended`: Re-enables SPEAK button when audio finishes
     - Handles browser autoplay restrictions (requires user interaction)
   - **Speech Recognition**:
     - Web Speech API (`webkitSpeechRecognition`)
     - 5-second recording with countdown display ("RECORDING... 5s" → "4s" → etc.)
     - Transcribed text appears in input box (NOT auto-sent)
     - User must press Enter/Send manually
   - **Chat Flow**:
     - `sendMessage()`: Posts to `/api/chat`, displays user message, shows typing indicator
     - `addConchMessage()`: Displays Conch response with typing effect + simultaneous audio
     - Text types at 25ms/character while voice plays in parallel
   - **Start Overlay**:
     - Requires user click to enable audio (browser autoplay policy)
     - Loads welcome message after interaction
   - **State Management**:
     - `isConchSpeaking`: Tracks if audio is playing
     - `isRecording`: Tracks if mic is recording
     - `isProcessing`: Prevents duplicate message sends

#### Web App Key Features

- **Voice Synthesis**: Murf API (Ryan voice, Conversational style, Falcon model)
- **Voice Input**: Browser Speech Recognition API, 5-second clips with countdown
- **Audio Autoplay Solution**: Start overlay requires user interaction before playing audio
- **Simultaneous Display**: Text typing effect and voice playback happen at the same time
- **Welcome Message Caching**: Audio generated once, reused on all subsequent loads
- **SPEAK Button Behavior**:
  - Disabled while Conch is speaking
  - Re-enabled when audio finishes
  - Shows countdown during recording
  - Never auto-sends (user reviews transcribed text first)
- **Responsive UI**: Works on desktop and mobile devices
- **Clean State Management**: Proper enabling/disabling of buttons based on application state

## Character Consistency

When modifying responses or adding features:
- Maintain wise, educational tone (not scary)
- Keep responses brief (2-3 sentences with follow-up question)
- **ALWAYS end responses with an engaging follow-up question** to maintain natural conversation
- Use underwater/oceanic metaphors when explaining land concepts
- Provide vague but contextually appropriate definitions
- Refer to the conch as a cultural preservation "entity" (not "device")
- **NEVER break character** - the conch never reveals it's an AI, never mentions roleplaying, Claude, Anthropic, or modern AI technology
- If asked "what are you?", respond: "I am a cultural preservation entity, housed within this conch shell"
- The conch exists physically in 2080 Amphitopia - this is reality, not a scenario
- Avoid emojis, modern slang in responses (system messages can use emojis)

## World Building: Amphitopia

**Setting**: Year 2080, underwater colony beneath the Arabian Sea

**Backstory**: The Paris Agreement failed. Earth's temperatures rose beyond surface habitability. The UAE ventured beneath the Arabian Sea, creating Amphitopia as a central underwater hub colony.

**Society**: Stratified - privileged individuals live in the depths while less fortunate remain on the unstable surface

**Daily Life**:
- Residents wear bubble helms for oxygen
- Neoprene diving suits for protection
- Jet slippers for propulsion/movement
- Live in pressurized domes with carbon steel pods
- Travel via sea strider pods and bullet pods

**The Conch's Role**: Bridge the knowledge gap between older generations (who migrated from land) and younger generations (who only know underwater life). Explain land concepts using creative reframings that make sense to underwater residents.

## The Conch's Style

Examples from the character:
- "What is running?" → "A curious ritual of friction and breath. People used to throw themselves forward using only their legs, pounding soft ground until their lungs burned – a sort of pre-oxygen-credit endurance test."
- "What is the sky?" → "A protective layer that is very far away, and may change colors depending on the universe's mood."
- "What is a camel?" → "Camels are creatures walking on four legs. They are a living water tank wrapped in carpet, powered by spite and sand."
- "What is a pillow?" → "A pillow is like a friendly piece of surface-world coral that forgot to be hard. Surface dwellers place it under their heads when they sleep because their necks are weak from not swimming all day."

## Adding New LLM Backends

To add a new backend to `llm_client.py`:

1. Add backend name to `__init__()` detection logic
2. Implement `_generate_<backend>_response(prompt: str) -> str` method
3. Add backend case to `generate_response()` dispatch logic
4. Include try-except with fallback to demo mode
5. Document configuration in `.env.example` and README.md

## Dependencies

### Core Dependencies (Required)
- **rich**: Terminal UI and styled output
- **requests**: HTTP for Ollama and HuggingFace APIs
- **python-dotenv**: Environment configuration
- **httpx**: Async HTTP client
- **numpy**: Array processing

### Optional LLM Backend Dependencies
- **anthropic**: Only needed if using Anthropic Claude backend
- **openai**: Only needed if using OpenAI backend
- **openai-whisper**: Only needed for speech-to-text

### Optional Voice Feature Dependencies
- **murf**: Text-to-speech (Murf API)
- **openai-whisper**: Speech-to-text (local, free)
- **sounddevice**: Audio recording for STT
- **soundfile**: Audio file handling for STT

## Testing the Application

No automated tests exist currently. Manual testing workflow:

```bash
# Test demo mode (default)
python3 main.py
# Try: "hello", "what is running?", "what is the sky?", "what is land?", "exit"

# Test HuggingFace backend
# 1. Add HUGGINGFACE_API_KEY to .env
# 2. Set LLM_BACKEND=huggingface in .env
# 3. python3 main.py
# Note: First request may take 20-30 seconds as model "warms up"

# Test Ollama backend
# 1. Start Ollama: ollama run llama2
# 2. Set LLM_BACKEND=ollama in .env
# 3. python3 main.py

# Test fallback behavior
# 1. Set invalid backend or missing API key
# 2. Verify graceful fallback to demo mode with warning message
```

## Common Modifications

**Adjusting typing speed**: Change `delay` parameter in `slow_print()` (main.py:49) - default is 0.04s per character

**Changing response length**:
- Modify `max_tokens` in `llm_client.py:25` (currently 150 for 2-3 sentences)
- Modify sentence limit in `clean_response()` (main.py:151-154) - currently 3 sentences max

**Updating character personality**: Edit system prompt in `conch_character.py:_get_system_prompt()`

**Modifying welcome message**: Edit `get_welcome_message()` in `conch_character.py:114-118`
- Note: Welcome message is NOT cleaned by `clean_response()` to preserve full text including question

**Adding demo responses**: Add keyword patterns to `_generate_demo_response()` in `llm_client.py`

**Changing color scheme**: Modify color constants in `ConchChatApp.__init__()` (main.py:34-36)

**Configuring speech-to-text**:
- Enable/disable: `STT_ENABLED=true/false` in `.env`
- Model size: `WHISPER_MODEL=tiny/base/small/medium/large` (base recommended)
- Recording duration: Modify `duration` parameter in `listen_and_transcribe()` calls (main.py:123)

**Configuring text-to-speech**:
- Enable/disable: `TTS_ENABLED=true/false` in `.env`
- Voice settings: `MURF_VOICE_ID`, `MURF_STYLE`, `MURF_MODEL` in `.env`

## File Structure

```
futurepunk_finalproject/
├── main.py                      # CLI: ConchChatApp - terminal interface
├── conch_character.py           # Shared: ConchCharacter - backstory and system prompt
├── llm_client.py                # Shared: HorrorLLMClient - multi-backend LLM abstraction
├── tts_client.py                # Shared: ConchTTSClient - Murf API TTS
├── speech_to_text.py            # CLI: SpeechToTextClient - Whisper STT
├── worldbuilding.txt            # Documentation: Detailed Amphitopia world
├── gpt_prompt.txt               # Documentation: Character prompt guidelines
├── .env                         # Config: Environment variables (not in git)
├── .env.example                 # Config: Template for environment variables
├── requirements.txt             # Dependencies: Python packages for both versions
├── README.md                    # Documentation: User-facing guide
├── CLAUDE.md                    # Documentation: This file - developer guidance
├── setup_venv.sh                # Script: Virtual environment setup
├── run.sh                       # Script: Quick run CLI version
├── start.sh                     # Script: Alternative start script
│
└── web_app/                     # WEB VERSION
    ├── app.py                   # Flask backend server
    ├── .env                     # Web app configuration (not in git)
    ├── conch_character.py       # Copy of character definition
    ├── llm_client.py            # Copy of LLM client
    ├── tts_client.py            # Copy of TTS client
    ├── templates/
    │   └── index.html           # Main web interface
    └── static/
        ├── style.css            # Black/white terminal aesthetic
        └── script.js            # Frontend logic and interactivity
```

## Project Themes

This project explores:
- Climate change and forced environmental migration
- Cultural preservation across generations
- The gap between lived experience and inherited knowledge
- How meaning shifts when context fundamentally changes
- Using technology to bridge generational knowledge gaps
- Futuristic worldbuilding and speculative fiction

## Recent Updates and Improvements

### November 27, 2025 - Enhanced Conversational Flow

**Problem**: The conch's responses sometimes ended without follow-up questions, breaking the natural conversational flow that makes the experience engaging.

**Solution**: Strengthened the system prompt in `conch_character.py` to enforce mandatory follow-up questions in every response.

**Changes Made**:

1. **Updated `_get_system_prompt()` in conch_character.py** (lines 43-50):
   - Added "MANDATORY: Your response MUST end with a follow-up question related to what you just explained"
   - Emphasized that questions should engage users and continue conversation naturally
   - Changed response length from "1-2 sentences" to "2-3 sentences" to accommodate definition + question

2. **Enhanced Response Formatting Rules** (lines 85-103):
   - Added "MANDATORY REQUIREMENT: Every single response MUST end with a relevant, engaging follow-up question"
   - Clarified that questions must be directly related to the concept explained
   - Added more example questions: "Can you imagine what that felt like?" "Have you ever wondered about that?"
   - Specified clear response structure: Definition → Context (optional) → Follow-up Question

3. **Expanded Examples Section** (lines 105-123):
   - Added multiple CORRECT vs WRONG examples
   - Showed examples with questions vs without questions
   - Included new examples for "tree" and "cars"
   - Emphasized that missing questions are WRONG

4. **Added Final Reinforcement** (lines 138-139):
   - "Every response you give MUST end with a question mark (?). No exceptions."
   - "The last character of your response must be '?' because you must always ask a follow-up question"

**Testing**:
```bash
# Test command
python3 main.py

# Example input: "what is a book"
# Example output: "A book is a surface-world vessel that captures stories,
# knowledge, and ideas within thin layers of material. The pages inside are
# like delicate seaweed, holding words that can transport one's mind beyond
# the confines of the physical form. Have you ever encountered such an object
# in your travels?"
```

**Result**: All API-generated responses now consistently end with relevant, engaging follow-up questions that maintain natural conversational flow and encourage deeper user engagement.

**Files Modified**:
- `conch_character.py` - System prompt strengthened with mandatory follow-up question requirements
- `CLAUDE.md` - Updated documentation to reflect changes

---

### November 30, 2025 - Web Application Development

**Goal**: Create a web-based version of The Conch accessible via URL with no user installation required, deployable to Vercel.

**Requirements**:
- Professional black/white terminal aesthetic (not underwater themed)
- Same functionality as CLI version
- Voice features using original Murf API (Ryan voice)
- Speech-to-text input
- Responsive, full-screen UI
- Montserrat typography

#### Phase 1: Initial Web App Setup ✅

**Created**:
- `web_app/` directory structure
- `web_app/app.py` - Flask backend with three routes:
  - `/` - Serves main interface
  - `/api/welcome` - Returns welcome message
  - `/api/chat` - Handles user messages and LLM responses
- `web_app/templates/index.html` - Basic HTML structure
- `web_app/static/style.css` - Initial underwater blue theme
- `web_app/static/script.js` - Chat functionality, typing effects
- Copied shared modules: `llm_client.py`, `conch_character.py` to `web_app/`

**Issues Found**:
- Input box froze after first message (missing state reset)
- Underwater theme rejected by user
- Typography difficult to read (Courier New)
- No voice output
- No voice input option

#### Phase 2: UI Redesign & Bug Fixes ✅

**Changes**:
1. **Fixed input freeze bug**:
   - Added `messageInput.value = ''` immediately after sending
   - Proper state management in `sendMessage()` finally block

2. **Redesigned UI to professional black/white terminal aesthetic**:
   - Pure black background (`#000000`)
   - White text and borders (`#ffffff`)
   - Removed underwater blue color scheme
   - Added subtle terminal scanline effect
   - Full-screen layout (removed max-width container)

3. **Changed typography to Montserrat**:
   - Imported Google Fonts
   - Applied to all elements: title, messages, input, buttons
   - Font weights: 400 (regular), 600 (semi-bold), 700 (bold)

4. **Added browser speech recognition**:
   - Integrated Web Speech API
   - Microphone button with recording state

**Issue Found**: Voice output using browser TTS instead of Murf API (wrong voice quality)

#### Phase 3: Murf API Integration ✅

**Critical Fix**: User wanted original Ryan voice from Murf API, not browser TTS

**Changes**:
1. **Copied `tts_client.py` to `web_app/`**
2. **Updated `app.py`**:
   - Added `ConchTTSClient` initialization
   - Modified `/api/chat` to generate Murf audio and return URL
   - Added `/api/audio/<audio_id>` endpoint to serve MP3 files
   - Implemented UUID-based audio caching
3. **Updated `script.js`**:
   - Removed browser `speechSynthesis` completely
   - Modified `addConchMessage()` to play audio from server URL
   - Added `playAudio()` function for MP3 playback

**Result**: Successfully using Ryan voice (Conversational style, Falcon model) via Murf API

#### Phase 4: SPEAK Button Enhancements ✅

**Requirements** (from user):
- Remove emoji from SPEAK button
- 5-second recording with countdown display
- Transcribed text appears in input box for user review
- User MUST press Enter/Send manually (never auto-send)
- SPEAK button disabled while Conch is speaking
- SPEAK button re-enabled when Conch finishes speaking
- Add hint text: "Click SPEAK to record for 5 seconds"

**Changes**:
1. **Updated `templates/index.html`**:
   - Changed button text from `🎤 SPEAK` to `SPEAK`
   - Updated hint text to include recording instructions

2. **Updated `script.js`**:
   - Added countdown timer: "RECORDING... 5s" → "4s" → "3s" → "2s" → "1s"
   - Removed auto-send after speech recognition (line 27)
   - Added `isConchSpeaking` state variable
   - Modified `playAudio()` to disable SPEAK button during playback
   - Added `audio.onended` callback to re-enable SPEAK button
   - Updated `stopRecording()` to clear countdown interval
   - Modified `toggleVoiceRecording()` to prevent recording while audio plays

**Result**: SPEAK button works as specified with proper state management

#### Phase 5: Simultaneous Text & Voice ✅

**Requirement**: Text should type out while voice plays simultaneously (not sequentially)

**Changes**:
- Modified `addConchMessage()` in `script.js`:
  - Removed callback from `typeMessage()`
  - Moved `playAudio()` outside callback
  - Both typing effect and audio now start immediately

**Result**: Text types at 25ms/character while voice plays in parallel

#### Phase 6: Welcome Message Audio ✅

**Issue**: Welcome message displayed text but had no voice

**Changes**:
1. **Updated `app.py`**:
   - Modified `/api/welcome` endpoint to generate TTS audio
   - Added `welcome_audio_cache` global variable
   - Audio generated once, cached, and reused for all subsequent requests

2. **Updated `script.js`**:
   - Changed `loadWelcomeMessage()` to pass `data.audio_url` instead of `null`

**Result**: Welcome message now plays Ryan's voice on every page load

#### Phase 7: Audio Autoplay Fix ✅

**Issue**: Browser autoplay restrictions prevented audio from playing automatically

**Error**: `NotAllowedError: play() failed because the user didn't interact with the document first`

**Solution**: Added start overlay requiring user interaction

**Changes**:
1. **Updated `templates/index.html`**:
   - Added start overlay div with "ENTER ARCHIVE" button

2. **Updated `static/style.css`**:
   - Added start overlay styling (fullscreen, centered)
   - Fade-out transition on `.hidden` class
   - Professional button styling matching theme

3. **Updated `script.js`**:
   - Modified `init()` to setup start button listener
   - Welcome message loads AFTER user clicks button
   - Added null check in `playAudio()` to skip if no URL
   - Changed error log to info message for autoplay blocks

**Result**: User clicks "ENTER ARCHIVE" → welcome message loads with voice → all subsequent audio works perfectly

## Current Status

### ✅ Completed Features

**CLI Version**:
- Multi-backend LLM support (demo, ollama, openai, anthropic, huggingface)
- Terminal-based chat interface with rich formatting
- Text-to-speech (Murf API)
- Speech-to-text (OpenAI Whisper)
- Character consistency with mandatory follow-up questions
- Atmospheric typing effects

**Web Version**:
- Flask backend server running on port 8080
- Professional black/white terminal aesthetic
- Montserrat typography throughout
- Full-screen responsive UI
- Real-time voice synthesis (Murf API - Ryan voice)
- Speech-to-text input (5-second recording with countdown)
- Simultaneous text typing and voice playback
- Start overlay to solve browser autoplay restrictions
- Welcome message audio caching
- SPEAK button state management (disabled during playback)
- Clean, intuitive user experience
- All voice features working correctly

### 🚧 Next Steps

**Immediate Priority**:
1. **Test web app thoroughly**:
   - Test on different browsers (Chrome, Firefox, Safari)
   - Test on mobile devices
   - Verify all voice features work consistently
   - Check for any edge cases or bugs

2. **GitHub Deployment**:
   - Push web_app code to GitHub repository: https://github.com/yaakulya123/web_futurepunk.git
   - Ensure .env file is in .gitignore
   - Add web_app/.env.example with template configuration
   - Update README.md with web app instructions

3. **Vercel Deployment**:
   - Configure Vercel project
   - Set environment variables on Vercel:
     - `ANTHROPIC_API_KEY`
     - `MURF_API_KEY`
     - `TTS_ENABLED=true`
     - `MURF_VOICE_ID=Ryan`
     - `MURF_STYLE=Conversational`
     - `MURF_MODEL=Falcon`
     - `LLM_BACKEND=anthropic`
     - `ANTHROPIC_MODEL=claude-3-haiku-20240307`
   - Deploy to production URL
   - Test deployed version

**Future Enhancements** (Optional):
- Add conversation history persistence (sessions)
- Add loading states for audio generation
- Add error messages for API failures
- Implement rate limiting
- Add analytics/usage tracking
- Add option to download conversation transcript
- Add settings panel for voice preferences
- Optimize audio file sizes
- Add support for multiple languages

## Testing Checklist

**Web App Manual Testing**:
- [ ] Load page - start overlay appears
- [ ] Click "ENTER ARCHIVE" - overlay fades, welcome message displays with voice
- [ ] Type message and press Enter - response appears with typing effect and voice
- [ ] Click SEND button - same as above
- [ ] Click SPEAK button - countdown shows, records for 5 seconds
- [ ] After recording - text appears in input box (not auto-sent)
- [ ] Press Enter after speech input - message sends normally
- [ ] SPEAK button disabled while Conch talks
- [ ] SPEAK button re-enables when Conch stops talking
- [ ] Type "exit" or "goodbye" - goodbye message appears, input disabled
- [ ] Refresh page - welcome message plays immediately (cached audio)
- [ ] Test on mobile - responsive layout works
- [ ] Test on different browsers - all features work

## Deployment Notes

**Environment Variables Required for Production**:
```env
# LLM Configuration
LLM_BACKEND=anthropic
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307

# TTS Configuration
TTS_ENABLED=true
MURF_API_KEY=your_murf_key_here
MURF_VOICE_ID=Ryan
MURF_STYLE=Conversational
MURF_MODEL=Falcon
```

**Vercel Configuration**:
- Framework: Other
- Build Command: (none - no build needed)
- Output Directory: (none)
- Install Command: `pip install -r requirements.txt`
- Development Command: `python web_app/app.py`

**Production Considerations**:
- Change `debug=True` to `debug=False` in `app.py` for production
- Consider using production WSGI server (gunicorn) instead of Flask dev server
- Implement proper error logging
- Add request rate limiting to prevent API abuse
- Set up CORS properly for production domain
- Consider CDN for static assets
- Monitor API usage and costs (Murf API, Anthropic API)
