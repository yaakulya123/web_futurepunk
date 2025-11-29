# The Conch - Setup Guide

## Why Virtual Environment?

A virtual environment (venv) keeps all of The Conch's dependencies isolated in its own folder. This means:
- ✅ PyTorch, transformers, and other large packages won't affect your other Python projects
- ✅ No version conflicts with system Python packages
- ✅ Easy to delete everything - just remove the `venv/` folder
- ✅ Each project has its own clean dependencies

## Quick Setup (3 Steps)

### Step 1: Run the Setup Script

```bash
./setup_venv.sh
```

This will:
- Create a virtual environment in the `venv/` folder
- Install all dependencies (Python packages)
- Download AI models (~2GB on first run)

### Step 2: Run The Conch

```bash
./run.sh
```

This automatically:
- Activates the virtual environment
- Runs the application
- Deactivates when you exit

### Step 3: Chat with The Conch!

```
THE CONCH

... a faint light glows from within the conch ...

Welcome, denizen of Amphitopia...

You: What is the sky?
```

## Manual Control

If you prefer to run things manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Your prompt will change to show (venv)
# Now you're in the isolated environment

# Run the app
python main.py

# When done, deactivate
deactivate
```

## What Gets Installed?

The virtual environment contains:
- **PyTorch** (~1GB) - Deep learning framework for TTS
- **Transformers** (~500MB) - HuggingFace models library
- **SpeechT5 models** (~500MB) - Text-to-speech AI models
- **Anthropic SDK** - For Claude API
- **Rich** - Terminal UI library
- **Audio libraries** - sounddevice, soundfile for voice playback

Total size: ~2-3GB

## File Structure After Setup

```
futurepunk_finalproject/
├── venv/                   # 🆕 Virtual environment (2-3GB)
│   ├── bin/               # Python executable and scripts
│   ├── lib/               # All installed packages
│   └── ...
├── main.py
├── conch_character.py
├── tts_client.py
└── ...
```

## Checking Your Environment

To see if you're in the virtual environment:

```bash
which python
# Should show: /path/to/futurepunk_finalproject/venv/bin/python
```

To see installed packages:

```bash
pip list
```

## Removing Everything

If you want to start fresh or remove The Conch entirely:

```bash
# Just delete the venv folder
rm -rf venv

# Re-run setup if needed
./setup_venv.sh
```

## Windows Users

On Windows, the commands are slightly different:

```bash
# Create venv
python -m venv venv

# Activate
venv\Scripts\activate

# Deactivate
deactivate
```

## Common Issues

### "Permission denied: ./setup_venv.sh"

Make the script executable:
```bash
chmod +x setup_venv.sh
chmod +x run.sh
```

### "Command not found: python3"

Try `python` instead:
```bash
python -m venv venv
```

### "No module named 'transformers'"

You're not in the virtual environment. Activate it:
```bash
source venv/bin/activate
```

### Voice not working

Check TTS is enabled in `.env`:
```
TTS_ENABLED=true
```

## Benefits Summary

| Without venv | With venv |
|--------------|-----------|
| Packages installed system-wide | Isolated in venv/ folder |
| May conflict with other projects | No conflicts |
| Hard to clean up | Just delete venv/ |
| Affects all Python projects | Only this project |

## Next Steps

Once setup is complete:
1. Edit `.env` to configure your API keys
2. Run `./run.sh` to start chatting
3. Ask The Conch about land concepts!
4. Enjoy AI-powered responses with voice synthesis 🐚✨
