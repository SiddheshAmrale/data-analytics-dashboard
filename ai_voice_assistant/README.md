# AI Voice Assistant

A comprehensive voice-based AI assistant that provides speech-to-text, text-to-speech, and natural language conversation capabilities using OpenAI's advanced AI models.

## 🎤 Features

### Core Functionality
- **Speech-to-Text**: Convert spoken words to text using OpenAI Whisper
- **Text-to-Speech**: Generate natural-sounding speech from text
- **Voice Commands**: Process and respond to voice commands
- **Conversation Mode**: Conduct natural voice conversations
- **Audio Recording**: Record audio from microphone
- **Voice Settings**: Customize voice type, speed, and model

### Advanced Features
- **Conversation History**: Track and manage conversation exchanges
- **Audio File Management**: Save and load audio files
- **Settings Configuration**: Customize audio and voice parameters
- **Error Handling**: Robust error handling and logging
- **File Operations**: Save/load conversation history

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Microphone and speakers
- Internet connection

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai_voice_assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Create .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

4. **Run the assistant**:
   ```bash
   python main.py
   ```

## 📖 Usage

### Interactive Mode

The assistant provides an interactive command-line interface:

```bash
python main.py
```

Available commands:
- `record` - Record and transcribe audio
- `conversation` - Start voice conversation
- `settings` - Configure voice settings
- `history` - View conversation history
- `save` - Save conversation
- `load` - Load conversation
- `clear` - Clear conversation history
- `quit` - Exit

### Programmatic Usage

```python
from main import AIVoiceAssistant

# Initialize assistant
assistant = AIVoiceAssistant(api_key="your-api-key")

# Record and transcribe audio
audio_file = assistant.record_audio(duration=5)
transcription = assistant.transcribe_audio(audio_file)

# Process voice command
response = assistant.process_voice_command(transcription)

# Generate voice response
voice_file = assistant.generate_voice_response(response)

# Start voice conversation
conversation = assistant.voice_conversation(duration=30)
```

## 🔧 Configuration

### Voice Settings

```python
# Configure voice parameters
assistant.set_voice_settings(
    voice="alloy",      # Options: alloy, echo, fable, onyx, nova, shimmer
    model="tts-1",      # TTS model
    speed=1.0           # Speech speed (0.25 to 4.0)
)
```

### Audio Settings

```python
# Configure audio recording parameters
assistant.set_audio_settings(
    sample_rate=16000,  # Audio sample rate
    channels=1,         # Number of audio channels
    chunk_size=1024     # Audio chunk size
)
```

## 📊 API Reference

### AIVoiceAssistant Class

#### Initialization
```python
AIVoiceAssistant(api_key: str = None)
```

#### Methods

##### `record_audio(duration: int = 5) -> Optional[str]`
Record audio from microphone.

**Parameters:**
- `duration`: Recording duration in seconds

**Returns:**
- Path to recorded audio file or None if failed

##### `transcribe_audio(audio_file_path: str) -> Optional[str]`
Transcribe audio file to text using OpenAI Whisper.

**Parameters:**
- `audio_file_path`: Path to audio file

**Returns:**
- Transcribed text or None if failed

##### `generate_voice_response(text: str, output_file: str = None) -> Optional[str]`
Generate speech from text using OpenAI TTS.

**Parameters:**
- `text`: Text to convert to speech
- `output_file`: Output file path (optional)

**Returns:**
- Path to generated audio file or None if failed

##### `process_voice_command(command: str) -> str`
Process voice command and generate response.

**Parameters:**
- `command`: Voice command text

**Returns:**
- Response text

##### `voice_conversation(duration: int = 30) -> Dict[str, Any]`
Conduct a voice conversation.

**Parameters:**
- `duration`: Conversation duration in seconds

**Returns:**
- Dictionary with conversation results

##### `set_voice_settings(voice: str = None, model: str = None, speed: float = None)`
Update voice settings.

**Parameters:**
- `voice`: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
- `model`: TTS model to use
- `speed`: Speech speed (0.25 to 4.0)

##### `set_audio_settings(sample_rate: int = None, channels: int = None, chunk_size: int = None)`
Update audio recording settings.

**Parameters:**
- `sample_rate`: Audio sample rate
- `channels`: Number of audio channels
- `chunk_size`: Audio chunk size

##### `get_conversation_history() -> List[Dict[str, Any]]`
Get conversation history.

**Returns:**
- List of conversation exchanges

##### `clear_conversation_history()`
Clear conversation history.

##### `save_conversation(filename: str)`
Save conversation history to file.

**Parameters:**
- `filename`: Output file path

##### `load_conversation(filename: str)`
Load conversation history from file.

**Parameters:**
- `filename`: Input file path

## 🎯 Examples

### Basic Voice Recording and Transcription

```python
from main import AIVoiceAssistant

assistant = AIVoiceAssistant()

# Record audio
audio_file = assistant.record_audio(duration=5)
if audio_file:
    # Transcribe audio
    transcription = assistant.transcribe_audio(audio_file)
    print(f"Transcription: {transcription}")
```

### Voice Conversation

```python
# Start a 30-second voice conversation
conversation = assistant.voice_conversation(duration=30)
print(f"Conversation completed with {len(conversation['exchanges'])} exchanges")
```

### Custom Voice Settings

```python
# Configure custom voice settings
assistant.set_voice_settings(
    voice="nova",
    speed=1.2
)

# Generate voice response with custom settings
voice_file = assistant.generate_voice_response("Hello, this is a test.")
```

### Conversation Management

```python
# Save conversation history
assistant.save_conversation("conversation.json")

# Load conversation history
assistant.load_conversation("conversation.json")

# Clear conversation history
assistant.clear_conversation_history()
```

## 🔒 Security Considerations

### API Key Management
- Store API keys in environment variables
- Never commit API keys to version control
- Use `.env` files for local development
- Consider using secret management services in production

### Audio Privacy
- Audio files are temporarily stored and should be cleaned up
- Consider implementing automatic cleanup of audio files
- Be aware of privacy implications when recording audio

## 🚨 Troubleshooting

### Common Issues

#### PyAudio Installation
If you encounter issues installing PyAudio:

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Linux:**
```bash
sudo apt-get install python3-pyaudio
pip install pyaudio
```

#### Microphone Access
- Ensure microphone permissions are granted
- Check if microphone is working in other applications
- Verify audio input device is properly configured

#### API Key Issues
- Verify OpenAI API key is valid and has sufficient credits
- Check internet connection
- Ensure API key has access to Whisper and TTS models

### Error Messages

#### "Error recording audio"
- Check microphone permissions
- Verify audio input device
- Ensure PyAudio is properly installed

#### "Error transcribing audio"
- Check OpenAI API key
- Verify internet connection
- Ensure audio file is valid

#### "Error generating voice response"
- Check OpenAI API key
- Verify TTS model access
- Ensure text input is valid

## 📈 Performance Optimization

### Audio Quality
- Adjust sample rate for better quality vs. file size
- Use appropriate chunk size for your system
- Consider audio compression for storage

### API Usage
- Implement caching for repeated requests
- Batch API calls when possible
- Monitor API usage and costs

### Memory Management
- Clean up temporary audio files
- Limit conversation history size
- Use streaming for large audio files

## 🔄 Development

### Adding New Features
1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests for new functionality
5. Submit a pull request

### Testing
```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=. --cov-report=html
```

### Contributing
- Follow PEP 8 style guidelines
- Add docstrings for all functions
- Include type hints
- Write comprehensive tests

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information

---

**Note**: This project requires an OpenAI API key with access to Whisper and TTS models. Please ensure you have sufficient API credits for your usage. 