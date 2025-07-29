# AI Chat Assistant

A conversational AI assistant with memory and context management built using OpenAI's GPT models.

## Features

- 🤖 **Intelligent Conversations**: Powered by OpenAI's GPT-3.5-turbo model
- 💾 **Conversation Memory**: Maintains context across multiple interactions
- 📝 **History Management**: Save and load conversation histories
- ⚙️ **Customizable**: Configurable system prompts and parameters
- 🔄 **Session Management**: Clear history and manage conversation flow

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Basic Usage

Run the main script:
```bash
python main.py
```

### Programmatic Usage

```python
from main import AIChatAssistant

# Initialize the assistant
assistant = AIChatAssistant(api_key="your-api-key")

# Start a conversation
response = assistant.get_chat_response("Hello, how are you?")
print(response)

# Continue the conversation
response = assistant.get_chat_response("What's the weather like?")
print(response)
```

### Advanced Features

#### Custom System Prompt
```python
system_prompt = "You are a helpful coding assistant. Provide code examples when relevant."
response = assistant.get_chat_response("How do I create a Python function?", system_prompt)
```

#### Save and Load Conversations
```python
# Save current conversation
assistant.save_conversation("my_conversation.json")

# Load a previous conversation
assistant.load_conversation("my_conversation.json")
```

#### Clear History
```python
assistant.clear_history()
```

## API Reference

### AIChatAssistant Class

#### Constructor
```python
AIChatAssistant(api_key: str = None)
```
- `api_key`: OpenAI API key (optional if set as environment variable)

#### Methods

- `get_chat_response(user_message: str, system_prompt: str = None) -> str`
  - Get AI response to user message
  - `user_message`: The user's input text
  - `system_prompt`: Optional system prompt to guide AI behavior

- `add_message(role: str, content: str)`
  - Add message to conversation history
  - `role`: "user" or "assistant"
  - `content`: Message content

- `clear_history()`
  - Clear all conversation history

- `get_history() -> List[Dict[str, Any]]`
  - Get current conversation history

- `save_conversation(filename: str = None)`
  - Save conversation to JSON file
  - `filename`: Optional filename (auto-generated if not provided)

- `load_conversation(filename: str)`
  - Load conversation from JSON file
  - `filename`: Path to JSON file

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key

### Model Parameters
The assistant uses these default parameters:
- Model: `gpt-3.5-turbo`
- Max tokens: 500
- Temperature: 0.7
- Max history length: 10 messages

## Error Handling

The assistant includes comprehensive error handling:
- API key validation
- Network error handling
- File I/O error handling
- Graceful degradation with user-friendly error messages

## Examples

### Example 1: Basic Chat
```
You: Hello, how are you?
🤖 Assistant: Hello! I'm doing well, thank you for asking. I'm here to help you with any questions or tasks you might have. How can I assist you today?

You: What's the capital of France?
🤖 Assistant: The capital of France is Paris. It's a beautiful city known for its rich history, culture, and iconic landmarks like the Eiffel Tower, Louvre Museum, and Notre-Dame Cathedral.
```

### Example 2: Code Assistance
```
You: How do I create a Python function?
🤖 Assistant: Here's how to create a Python function:

```python
def function_name(parameters):
    # Function body
    return value
```

Basic example:
```python
def greet(name):
    return f"Hello, {name}!"

# Usage
result = greet("Alice")
print(result)  # Output: Hello, Alice!
```
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is set correctly
   - Check that the key has sufficient credits

2. **Network Errors**
   - Check your internet connection
   - Verify OpenAI API service status

3. **Memory Issues**
   - The assistant automatically manages conversation length
   - Use `clear_history()` if needed

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving error handling
- Enhancing documentation
- Reporting bugs

## License

This project is open source and available under the MIT License. 