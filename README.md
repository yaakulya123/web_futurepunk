# The Conch: A Cultural Preservation Experience

A futuristic CLI chat software featuring an intelligent conch shell that preserves cultural heritage for the residents of Amphitopia, an underwater colony beneath the Arabian Sea in 2080. The conch bridges the knowledge gap between generations, explaining land-based concepts to those who only know life underwater.

## The Story

The year is 2080. The Paris Agreement failed, and Earth's temperatures rose beyond habitability on the surface. The UAE ventured beneath the depths of the Arabian Sea, creating Amphitopia - a central hub underwater colony amongst many spread across the region.

You are conversing with a conch—an intelligent cultural preservation device designed to bridge the knowledge gap between older generations who migrated from land and younger generations who only know life under water. The transition from land to water shifted meanings in how humans interact with objects, concepts, and life. The conch helps preserve these memories and explain land-based concepts in ways that make sense to underwater colony residents.

## Features

- Terminal-based chat interface with futuristic underwater aesthetics
- Multiple LLM backend options: Demo mode, Ollama (local), OpenAI, Anthropic, or HuggingFace
- Cultural preservation responses from an intelligent conch character
- Atmospheric typing effects and underwater-themed visual elements
- **Works out of the box in demo mode - no API keys needed!**

## Quick Start

### Windows Users (Super Easy!)

1. **First time setup** - Double-click `setup.bat` (or run in Command Prompt)
   - This creates a virtual environment and installs all dependencies

2. **Run the app** - Double-click `run.bat` (or run in Command Prompt)
   - That's it! The conch will start chatting

3. **Your .env file** - The app will automatically copy `.env.example` to `.env` on first run
   - Edit `.env` to add your API keys if you have them
   - Default backend is already configured to work with your settings

**Exit the app**: Type `exit`, `quit`, `bye`, `goodbye` or press Ctrl+C

---

### macOS/Linux Users

#### Option 1: Automated Setup (Recommended)

Use the setup script to create a virtual environment and install everything:

```bash
./setup_venv.sh
```

Then run the app with:

```bash
./run.sh
```

That's it! The conch will respond with AI-generated text and voice.

#### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### What You Get:

- **AI-powered responses** from Claude API (or demo mode if no API key)
- **Voice synthesis** using Microsoft SpeechT5 (text-to-speech)
- **Isolated environment** that won't affect your other Python projects
- Pre-written conch responses in demo mode that adapt to your input

## Advanced Setup (Optional LLM Backends)

Want AI-generated responses? Choose one of these backends:

### Option 1: HuggingFace Inference API (Recommended for This Project)

1. Get a free API key from [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Edit `.env` and set:
```
LLM_BACKEND=huggingface
HUGGINGFACE_API_KEY=your_hf_token_here
HUGGINGFACE_MODEL=mistralai/Mistral-7B-Instruct-v0.2
```

### Option 2: Ollama (Local, Free)

1. Install Ollama from [https://ollama.ai](https://ollama.ai)
2. Run: `ollama run llama2`
3. Edit `.env` and set:
```
LLM_BACKEND=ollama
OLLAMA_MODEL=llama2
```

### Option 3: OpenAI API

Edit `.env` and set:
```
LLM_BACKEND=openai
OPENAI_API_KEY=your_openai_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

### Option 4: Anthropic Claude

Edit `.env` and set:
```
LLM_BACKEND=anthropic
ANTHROPIC_API_KEY=your_anthropic_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307
```

## Installation

### Recommended: Using Virtual Environment

Using a virtual environment keeps this project's dependencies isolated from your other Python projects.

1. Clone or download this repository

2. Create a virtual environment:
```bash
python3 -m venv venv
```

3. Activate the virtual environment:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. (Optional) Copy and edit the `.env` file if you want to use a specific LLM backend:
```bash
cp .env.example .env
# Edit .env to configure your preferred backend
```

**Note:** You'll need to activate the virtual environment each time you want to run the app. To deactivate the environment when you're done, simply run:
```bash
deactivate
```

### Alternative: System-wide Installation

If you prefer not to use a virtual environment:

```bash
pip3 install -r requirements.txt
```

**Warning:** This installs packages system-wide and may conflict with other Python projects.

## Usage

**If using virtual environment**, activate it first:
```bash
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate     # Windows
```

Then run the application:
```bash
python main.py
```

**Quick run (with helper script):**
```bash
./run.sh  # Automatically activates venv and runs the app
```

### Using The Conch:
- Type your messages and press Enter to chat with the conch
- Ask questions like "What is walking?" or "What is the sky?" to learn about land concepts
- The conch will respond with text AND voice (if TTS is enabled)
- Type `exit` or press `Ctrl+C` to quit

When you're done, deactivate the virtual environment:
```bash
deactivate
```

## Project Structure

```
futurepunk_finalproject/
├── venv/                  # Virtual environment (not in git)
├── .env                   # Your configuration (optional, not in git)
├── .env.example          # Template for .env file
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── CLAUDE.md          # Project instructions for Claude Code
├── worldbuilding.txt  # Amphitopia world description
├── gpt_prompt.txt     # Character prompt guidelines
├── setup_venv.sh      # Automated setup script
├── run.sh             # Quick run script
├── main.py            # Main application entry point
├── conch_character.py # Character backstory and prompt
├── llm_client.py      # Multi-backend LLM client
└── tts_client.py      # Text-to-speech voice synthesis
```

## Example Interaction

```
... a faint light glows from within the conch ...

Welcome, denizen of Amphitopia. I am a cultural preservation device, designed
to bridge the knowledge between the land world your ancestors knew and the
underwater life you experience now.

Activate me by asking: "What is ..." and I will explore my archive to help you
understand the surface world that once was.

You: What is running?

Walking or running... A curious ritual of friction and breath. People used to
throw themselves forward using only their legs, pounding soft ground until their
lungs burned – a sort of pre-oxygen-credit endurance test.

You: What is a camel?

Camels are creatures walking on four legs. They are a living water tank wrapped
in carpet, powered by spite and sand. They thrived in the deserts your
grandparents fled from.
```

## World Building

### Amphitopia
- **Location**: Beneath the Arabian Sea
- **Year**: 2080
- **Origin**: Created by the UAE after the Paris Agreement failed and surface temperatures became uninhabitable
- **Society**: Stratified - privileged individuals live in the depths while less fortunate remain on the unstable surface
- **Lifestyle**: Residents wear bubble helms, neoprene diving suits, use jet slippers for movement, and live in pressurized domes

### The Conch's Purpose
The conch explains land-based concepts to underwater residents using:
- Creative reframings that bridge the knowledge gap
- Underwater/oceanic metaphors
- Vague but contextually appropriate definitions
- Poetic interpretations that honor both past and present

## Technical Details

- **Default Mode**: Demo mode with contextual pre-written responses
- **LLM Options**: HuggingFace Inference API, Ollama (local), OpenAI GPT, Anthropic Claude
- **Interface**: Rich library for terminal UI with slow-typing effects
- **Language**: Python 3.10+
- **Theme**: Futuristic underwater cultural preservation

## Troubleshooting

**Virtual environment issues**:
- If `./setup_venv.sh` fails, make sure you have Python 3.8+ installed: `python3 --version`
- On Windows, use `python -m venv venv` instead
- Make sure to activate venv before running: `source venv/bin/activate`

**Demo mode not working**: Make sure you have the `rich` library installed (`pip install rich`)

**Voice/TTS not working**:
- First time running will download ~2GB of models (PyTorch + SpeechT5)
- Check that `TTS_ENABLED=true` in your `.env` file
- Make sure all audio dependencies are installed: `pip install sounddevice soundfile`

**HuggingFace API errors**: Check that your `.env` file has a valid API key. The model may take 20-30 seconds to "warm up" on first request.

**Ollama not connecting**: Ensure Ollama is running (`ollama serve`) and you've pulled a model (`ollama pull llama2`)

**API key errors**: Check that your `.env` file has the correct API key for your chosen backend

**Import errors**: Make sure you're in the virtual environment (`source venv/bin/activate`) before running

## Project Context

This project explores themes of:
- Climate change and environmental migration
- Cultural preservation across generations
- The gap between lived experience and inherited knowledge
- How meaning shifts when context fundamentally changes
- The role of technology in preserving heritage
