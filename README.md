# LiveKit Voice AI Assistant

A real-time voice AI assistant built with LiveKit, featuring speech-to-text, natural language processing, and text-to-speech capabilities.

## Features

- 🎤 Real-time voice communication using LiveKit
- 🗣️ Speech-to-text with Deepgram
- 🧠 AI responses using Groq's Llama 3.3 70B model
- 🔊 Text-to-speech with Cartesia
- 🌐 Web-based client interface
- 🔒 Secure token-based authentication

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Web Client    │────│   Flask Server   │────│  LiveKit Agent  │
│  (Browser)      │    │   (app.py)       │    │   (main.py)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │               ┌───────────────┐               │
         └───────────────│   LiveKit     │───────────────┘
                         │   Server      │
                         └───────────────┘
```

## Prerequisites

- Python 3.8+
- LiveKit server (local or cloud)
- API keys for:
  - Deepgram (speech-to-text)
  - Groq (LLM)
  - Cartesia (text-to-speech)

## Setup

### 1. Environment Configuration

Create a `.env` file in the `ai_assistant` directory with your API keys:

```env
LIVEKIT_URL=wss://your-livekit-server.com
LIVEKIT_API_KEY=your_livekit_api_key
LIVEKIT_API_SECRET=your_livekit_secret
DEEPGRAM_API_KEY=your_deepgram_api_key
GROQ_API_KEY=your_groq_api_key
CARTESIA_API_KEY=your_cartesia_api_key
```

### 2. Installation

```bash
cd ai_assistant
pip install -r requirements.txt
```

### 3. LiveKit Server

#### Option A: Local Development
Run LiveKit locally using the provided configuration:

```bash
livekit-server --config livekit.yaml
```

#### Option B: LiveKit Cloud
Use [LiveKit Cloud](https://cloud.livekit.io/) for a managed solution.

### 4. Running the Application

#### Start the Flask Web Server
```bash
python web/app.py
```
The web interface will be available at `http://localhost:5000`

#### Start the LiveKit Agent
```bash
python main.py
```

## Usage

1. **Access the Web Interface**: Open `http://localhost:5000` in your browser
2. **Connect**: Click the "Connect" button to join the voice room
3. **Speak**: The AI will greet you and listen for your voice input
4. **Interact**: Have a natural conversation with the AI assistant

## API Keys Setup

### Deepgram API Key
1. Sign up at [Deepgram](https://deepgram.com/)
2. Create a new project and get your API key
3. Add to `.env` as `DEEPGRAM_API_KEY`

### Groq API Key
1. Sign up at [Groq](https://groq.com/)
2. Generate an API key from your dashboard
3. Add to `.env` as `GROQ_API_KEY`

### Cartesia API Key
1. Sign up at [Cartesia](https://cartesia.ai/)
2. Create an API key from your account
3. Add to `.env` as `CARTESIA_API_KEY`

## Project Structure

```
ai_assistant/
├── web/
│   ├── app.py              # Flask web server
│   ├── templates/
│   │   └── index.html      # Web client interface
│   └── static/
│       ├── lk-client.js    # LiveKit client (empty - uses CDN)
│       └── livekit-client.umd.js
├── main.py                 # LiveKit agent entry point
├── requirements.txt        # Python dependencies
├── livekit.yaml           # LiveKit server configuration
├── .env                   # Environment variables
└── .gitignore
```

## Configuration

### LiveKit Server (livekit.yaml)
- Port: 7880 (WebSocket connections)
- RTC ports: 50000-60000 (WebRTC media)
- Auto-create rooms enabled
- Development keys for testing

### Agent Configuration (main.py)
- **VAD**: Silero Voice Activity Detection
- **STT**: Deepgram Nova-2 model
- **LLM**: Groq Llama 3.3 70B via OpenAI-compatible API
- **TTS**: Cartesia Sonic English model

## Troubleshooting

### Common Issues

1. **Connection Failures**
   - Verify LiveKit server is running
   - Check LIVEKIT_URL in `.env` matches your server
   - Ensure ports are not blocked by firewall

2. **Audio Issues**
   - Check browser microphone permissions
   - Verify audio input devices are working
   - Test with the "Test Audio" button

3. **API Key Errors**
   - Verify all API keys are set in `.env`
   - Check API key permissions and quotas
   - Ensure no trailing spaces in `.env` values

### Logs
- Web server logs: Check Flask console output
- Agent logs: Check main.py console output
- Client logs: Available in browser debug panel

## Development

### Adding New Features
- Modify `main.py` to change agent behavior
- Update `web/templates/index.html` for UI changes
- Extend `web/app.py` for additional server endpoints

### Customizing the AI Personality
Edit the agent instructions in `main.py`:

```python
instructions="""Your custom personality and behavior instructions here.
Keep responses natural and conversational."""
```

## License

This project is for educational and development purposes. Ensure compliance with API providers' terms of service.

## Support

For issues related to:
- LiveKit: [LiveKit Documentation](https://docs.livekit.io/)
- Deepgram: [Deepgram Docs](https://developers.deepgram.com/)
- Groq: [Groq Documentation](https://groq.com/)
- Cartesia: [Cartesia Docs](https://docs.cartesia.ai/)