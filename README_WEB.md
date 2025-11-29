# The Conch - Web Edition

Welcome to **The Conch**, a futuristic CLI chatbot transformed into a beautiful web experience. Set in Amphitopia, an underwater colony beneath the Arabian Sea in 2080, The Conch serves as a cultural preservation device that explains land-based concepts to those who only know life underwater.

🌊 **Live Demo**: [Coming soon on Vercel]

## Features

✅ Beautiful underwater-themed chat interface
✅ Real-time AI-powered conch responses
✅ Atmospheric typing effects
✅ Mobile responsive design
✅ Works out-of-the-box in demo mode (no API keys needed)
✅ Multiple LLM backend support (Anthropic, OpenAI, HuggingFace, Ollama)

## Quick Start - Local Development

### 1. Install Dependencies

```bash
pip3 install -r requirements.txt
```

### 2. Run the Server

```bash
python3 app.py
```

### 3. Open Your Browser

Navigate to: **http://localhost:8080**

That's it! The Conch will respond in demo mode by default.

## Configuration (Optional)

To use AI-powered responses instead of demo mode:

1. Copy `.env.example` to `.env`
2. Choose your backend and add API key:

```env
# For Anthropic Claude (recommended)
LLM_BACKEND=anthropic
ANTHROPIC_API_KEY=your_key_here

# Or for OpenAI
LLM_BACKEND=openai
OPENAI_API_KEY=your_key_here

# Or for HuggingFace
LLM_BACKEND=huggingface
HUGGINGFACE_API_KEY=your_key_here

# Or keep demo mode (no API needed)
LLM_BACKEND=demo
```

## Deployment to Vercel

### One-Click Deploy

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yaakulya123/web_futurepunk)

### Manual Deployment

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Add environment variables in Vercel dashboard:
   - `LLM_BACKEND` - Your chosen backend (demo, anthropic, openai, etc.)
   - `ANTHROPIC_API_KEY` - If using Anthropic
   - `OPENAI_API_KEY` - If using OpenAI
   - `HUGGINGFACE_API_KEY` - If using HuggingFace

## Project Structure

```
.
├── app.py              # Flask backend API
├── conch_character.py  # Character definition and prompts
├── llm_client.py       # Multi-backend LLM client
├── templates/
│   └── index.html      # Main chat interface
├── static/
│   ├── style.css       # Underwater-themed styling
│   └── script.js       # Frontend chat logic
├── requirements.txt    # Python dependencies
├── vercel.json        # Vercel configuration
└── README_WEB.md      # This file
```

## The Story

The year is 2080. The Paris Agreement failed, and Earth's temperatures rose beyond habitability on the surface. The UAE ventured beneath the Arabian Sea, creating Amphitopia - an underwater colony.

You're conversing with The Conch, an intelligent cultural preservation device designed to bridge the knowledge gap between older generations who migrated from land and younger generations who only know life underwater.

### Example Interactions

**You:** What is running?

**The Conch:** Running is like jet-slipper movement but powered by leg muscles against ground that doesn't float. Can you imagine propelling yourself without water resistance?

**You:** What is a camel?

**The Conch:** Camels are living water tanks wrapped in carpet, powered by spite and sand. Does that sound like any creature you've encountered in our waters?

## Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **LLM**: Anthropic Claude, OpenAI GPT, HuggingFace, or Ollama
- **Deployment**: Vercel (serverless)
- **Styling**: Custom CSS with underwater theme

## Features in Detail

### 🎨 Underwater Aesthetic
- Deep ocean gradient background
- Cyan glow effects
- Bubble-themed message containers
- Animated typing indicators

### 💬 Smart Responses
- Character-consistent conch personality
- 2-3 sentence responses with follow-up questions
- Creative land-to-water concept translations
- No asterisks, ellipses, or stage directions

### 📱 Mobile Responsive
- Works on all screen sizes
- Touch-friendly interface
- Optimized for mobile browsers

## CLI Version

This project also has a terminal-based CLI version! Check out the main directory for:
- `main.py` - CLI chat application
- `tts_client.py` - Text-to-speech voice synthesis
- `speech_to_text.py` - Voice input support

## Contributing

Feel free to submit issues and pull requests!

## License

MIT License - See LICENSE file for details

---

**Dive into the depths of Amphitopia. Ask The Conch about the surface world your ancestors once knew.**
