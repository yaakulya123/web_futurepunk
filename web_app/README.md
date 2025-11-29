# The Conch - Web Version

A web-based chat interface for The Conch, Amphitopia's cultural preservation experience.

## Running Locally

### Quick Start

1. Install dependencies:
```bash
pip3 install -r requirements.txt
```

2. Run the server:
```bash
./run_web.sh
# OR
python3 app.py
```

3. Open your browser to: **http://localhost:5000**

That's it! The conch will work in demo mode by default (no API keys needed).

## Configuration

The web app uses the same `.env` file from the parent directory. To use AI-powered responses:

1. Copy `.env.example` to `.env` in the parent directory
2. Set your preferred backend:
```env
LLM_BACKEND=demo  # or anthropic, openai, huggingface, ollama
```

## Deploying to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy from the `web_app` directory:
```bash
cd web_app
vercel
```

3. Follow the prompts to deploy

### Environment Variables on Vercel

If using AI backends, add these in your Vercel project settings:

- `LLM_BACKEND` - Backend to use (demo, anthropic, openai, etc.)
- `ANTHROPIC_API_KEY` - If using Anthropic
- `OPENAI_API_KEY` - If using OpenAI
- `HUGGINGFACE_API_KEY` - If using HuggingFace

## Project Structure

```
web_app/
├── app.py              # Flask backend API
├── templates/
│   └── index.html      # Main chat interface
├── static/
│   ├── style.css       # Underwater-themed styling
│   └── script.js       # Frontend chat logic
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel deployment config
└── README.md          # This file
```

## Features

✅ Beautiful underwater-themed chat interface
✅ Real-time typing indicators
✅ Atmospheric typing effects
✅ Mobile responsive
✅ Same conch personality and responses as CLI version
✅ Works in demo mode (no API keys needed)
✅ Easy deployment to Vercel

## How It Works

- **Frontend**: HTML/CSS/JS with underwater aesthetics
- **Backend**: Flask API serving LLM responses
- **LLM**: Uses the same `llm_client.py` and `conch_character.py` from parent project
- **Deployment**: Configured for Vercel serverless deployment
