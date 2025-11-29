#!/bin/bash
# One-command setup and run for The Conch

echo "🐚 The Conch - Starting..."
echo ""

# Check if we need to reinstall (new voice system)
if [ -d "venv" ] && [ -f "venv/pyvenv.cfg" ]; then
    # Check if old edge-tts or PyTorch installation exists
    if [ -d "venv/lib/python3.*/site-packages/torch" ] 2>/dev/null || [ -d "venv/lib/python3.*/site-packages/edge_tts" ] 2>/dev/null; then
        echo "🔄 Updating to new Murf API voice system..."
        echo "   (Removing old TTS installation)"
        rm -rf venv
        echo "✓ Old installation removed"
    fi
fi

# Check if venv exists, if not create it
if [ ! -d "venv" ]; then
    echo "📦 Setting up virtual environment..."
    python3 -m venv venv

    echo "📥 Installing dependencies (lightweight - only ~50MB)..."
    source venv/bin/activate
    pip install --quiet --upgrade pip
    pip install --quiet -r requirements.txt

    echo "✅ Setup complete!"
    echo ""
else
    source venv/bin/activate
fi

# Run the application
python main.py

# Deactivate when done
deactivate
