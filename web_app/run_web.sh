#!/bin/bash
# Run the web version of The Conch locally

echo "=== THE CONCH - WEB VERSION ==="
echo ""
echo "Starting local development server..."
echo ""

# Navigate to web_app directory
cd "$(dirname "$0")"

# Check if .env exists in parent directory
if [ ! -f ../.env ]; then
    echo "⚠️  No .env file found in parent directory"
    echo "📋 Copying .env.example to .env..."
    cp ../.env.example ../.env
    echo "✓ Created .env file - using demo mode by default"
    echo ""
fi

# Run the Flask app
python3 app.py
