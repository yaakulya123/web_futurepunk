#!/bin/bash
# Convenience script to run The Conch with virtual environment

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo ""
    echo "Please run setup first:"
    echo "  ./setup_venv.sh"
    echo ""
    echo "Or create manually:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🐚 Activating virtual environment..."
source venv/bin/activate

# Run the application
echo "Starting The Conch..."
echo ""
python main.py

# Deactivate when done
deactivate
