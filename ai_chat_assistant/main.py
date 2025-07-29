import openai
import json
import os
from datetime import datetime
from typing import List, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIChatAssistant:
    def __init__(self, api_key: str = None):
        """Initialize the AI Chat Assistant with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        openai.api_key = self.api_key
        self.conversation_history = []
        self.max_history_length = 10
        
    def add_message(self, role: str, content: str):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        
        # Keep only the last max_history_length messages
        if len(self.conversation_history) > self.max_history_length:
            self.conversation_history = self.conversation_history[-self.max_history_length:]
    
    def get_chat_response(self, user_message: str, system_prompt: str = None) -> str:
        """Get a response from the AI assistant."""
        try:
            # Add user message to history
            self.add_message("user", user_message)
            
            # Prepare messages for OpenAI API
            messages = []
            
            # Add system prompt if provided
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            
            # Add conversation history
            for msg in self.conversation_history[:-1]:  # Exclude the current user message
                messages.append({"role": msg["role"], "content": msg["content"]})
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to history
            self.add_message("assistant", assistant_response)
            
            return assistant_response
            
        except Exception as e:
            logger.error(f"Error getting chat response: {e}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Get the conversation history."""
        return self.conversation_history.copy()
    
    def save_conversation(self, filename: str = None):
        """Save the conversation history to a JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.conversation_history, f, indent=2)
        
        logger.info(f"Conversation saved to {filename}")
    
    def load_conversation(self, filename: str):
        """Load a conversation history from a JSON file."""
        try:
            with open(filename, 'r') as f:
                self.conversation_history = json.load(f)
            logger.info(f"Conversation loaded from {filename}")
        except Exception as e:
            logger.error(f"Error loading conversation: {e}")

def main():
    """Main function to demonstrate the AI Chat Assistant."""
    print("🤖 AI Chat Assistant")
    print("=" * 50)
    
    # Initialize the assistant
    try:
        assistant = AIChatAssistant()
        print("✅ Assistant initialized successfully!")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenAI API key as an environment variable: OPENAI_API_KEY")
        return
    
    # Example conversation
    system_prompt = "You are a helpful AI assistant. Be concise, friendly, and informative."
    
    print("\n💬 Starting conversation...")
    print("Type 'quit' to exit, 'clear' to clear history, 'save' to save conversation")
    print("-" * 50)
    
    while True:
        user_input = input("\nYou: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'clear':
            assistant.clear_history()
            print("🗑️ Conversation history cleared!")
            continue
        elif user_input.lower() == 'save':
            assistant.save_conversation()
            continue
        elif not user_input:
            continue
        
        # Get AI response
        response = assistant.get_chat_response(user_input, system_prompt)
        print(f"\n🤖 Assistant: {response}")

if __name__ == "__main__":
    main() 