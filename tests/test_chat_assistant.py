#!/usr/bin/env python3
"""
Unit tests for AI Chat Assistant.

Tests cover core functionality, error handling, and edge cases.
"""

import unittest
from unittest.mock import patch, MagicMock
import json
import os
import tempfile
from datetime import datetime

# Import the module to test
import sys
sys.path.append('ai_chat_assistant')
from main import AIChatAssistant


class TestAIChatAssistant(unittest.TestCase):
    """Test cases for AIChatAssistant class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key-12345"
        self.assistant = AIChatAssistant(api_key=self.api_key)
    
    def test_initialization_with_api_key(self):
        """Test assistant initialization with API key."""
        assistant = AIChatAssistant(api_key=self.api_key)
        self.assertEqual(assistant.api_key, self.api_key)
        self.assertEqual(len(assistant.conversation_history), 0)
        self.assertEqual(assistant.max_history_length, 10)
    
    def test_initialization_without_api_key(self):
        """Test assistant initialization without API key raises error."""
        # Temporarily remove environment variable
        original_key = os.environ.get('OPENAI_API_KEY')
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        with self.assertRaises(ValueError):
            AIChatAssistant()
        
        # Restore environment variable
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
    
    def test_add_message(self):
        """Test adding messages to conversation history."""
        self.assistant.add_message("user", "Hello")
        self.assertEqual(len(self.assistant.conversation_history), 1)
        self.assertEqual(self.assistant.conversation_history[0]["role"], "user")
        self.assertEqual(self.assistant.conversation_history[0]["content"], "Hello")
        
        self.assistant.add_message("assistant", "Hi there!")
        self.assertEqual(len(self.assistant.conversation_history), 2)
        self.assertEqual(self.assistant.conversation_history[1]["role"], "assistant")
        self.assertEqual(self.assistant.conversation_history[1]["content"], "Hi there!")
    
    def test_history_length_limit(self):
        """Test that conversation history respects max length."""
        # Add more messages than max_history_length
        for i in range(15):
            self.assistant.add_message("user", f"Message {i}")
        
        # Should only keep the last 10 messages
        self.assertEqual(len(self.assistant.conversation_history), 10)
        self.assertEqual(self.assistant.conversation_history[0]["content"], "Message 5")
        self.assertEqual(self.assistant.conversation_history[-1]["content"], "Message 14")
    
    @patch('openai.ChatCompletion.create')
    def test_get_chat_response_success(self, mock_openai):
        """Test successful chat response generation."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Hello! How can I help you?"
        mock_openai.return_value = mock_response
        
        response = self.assistant.get_chat_response("Hello")
        
        self.assertEqual(response, "Hello! How can I help you?")
        self.assertEqual(len(self.assistant.conversation_history), 2)  # user + assistant
        mock_openai.assert_called_once()
    
    @patch('openai.ChatCompletion.create')
    def test_get_chat_response_with_system_prompt(self, mock_openai):
        """Test chat response with custom system prompt."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "I'm a helpful assistant!"
        mock_openai.return_value = mock_response
        
        system_prompt = "You are a helpful coding assistant."
        response = self.assistant.get_chat_response("Hello", system_prompt)
        
        self.assertEqual(response, "I'm a helpful assistant!")
        # Verify system prompt was included in the call
        call_args = mock_openai.call_args
        messages = call_args[1]['messages']
        self.assertEqual(messages[0]['role'], 'system')
        self.assertEqual(messages[0]['content'], system_prompt)
    
    @patch('openai.ChatCompletion.create')
    def test_get_chat_response_error_handling(self, mock_openai):
        """Test error handling in chat response generation."""
        mock_openai.side_effect = Exception("API Error")
        
        response = self.assistant.get_chat_response("Hello")
        
        self.assertIn("Sorry, I encountered an error", response)
        self.assertIn("API Error", response)
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        self.assistant.add_message("user", "Hello")
        self.assistant.add_message("assistant", "Hi!")
        
        self.assertEqual(len(self.assistant.conversation_history), 2)
        
        self.assistant.clear_history()
        self.assertEqual(len(self.assistant.conversation_history), 0)
    
    def test_get_history(self):
        """Test getting conversation history."""
        self.assistant.add_message("user", "Hello")
        self.assistant.add_message("assistant", "Hi!")
        
        history = self.assistant.get_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["role"], "user")
        self.assertEqual(history[1]["role"], "assistant")
        # Verify it's a copy, not the original
        self.assertIsNot(history, self.assistant.conversation_history)
    
    def test_save_conversation(self):
        """Test saving conversation to file."""
        self.assistant.add_message("user", "Hello")
        self.assistant.add_message("assistant", "Hi!")
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            self.assistant.save_conversation(temp_filename)
            
            # Verify file was created and contains correct data
            with open(temp_filename, 'r') as f:
                saved_data = json.load(f)
            
            self.assertEqual(len(saved_data), 2)
            self.assertEqual(saved_data[0]["role"], "user")
            self.assertEqual(saved_data[1]["role"], "assistant")
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_load_conversation(self):
        """Test loading conversation from file."""
        # Create test conversation data
        test_conversation = [
            {"role": "user", "content": "Hello", "timestamp": "2024-01-01T00:00:00"},
            {"role": "assistant", "content": "Hi!", "timestamp": "2024-01-01T00:00:01"}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(test_conversation, f)
            temp_filename = f.name
        
        try:
            self.assistant.load_conversation(temp_filename)
            
            self.assertEqual(len(self.assistant.conversation_history), 2)
            self.assertEqual(self.assistant.conversation_history[0]["role"], "user")
            self.assertEqual(self.assistant.conversation_history[1]["role"], "assistant")
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_load_conversation_file_not_found(self):
        """Test loading conversation from non-existent file."""
        # Should not raise an exception, just log error
        self.assistant.load_conversation("non_existent_file.json")
        self.assertEqual(len(self.assistant.conversation_history), 0)


class TestAIChatAssistantIntegration(unittest.TestCase):
    """Integration tests for AIChatAssistant."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key-12345"
    
    @patch('openai.ChatCompletion.create')
    def test_conversation_flow(self, mock_openai):
        """Test a complete conversation flow."""
        # Mock responses for a conversation
        responses = [
            "Hello! How can I help you today?",
            "I can help you with that!",
            "That's a great question!"
        ]
        
        mock_openai.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content=response))])
            for response in responses
        ]
        
        assistant = AIChatAssistant(api_key=self.api_key)
        
        # Simulate a conversation
        response1 = assistant.get_chat_response("Hello")
        response2 = assistant.get_chat_response("Can you help me?")
        response3 = assistant.get_chat_response("What's the weather like?")
        
        self.assertEqual(response1, "Hello! How can I help you today?")
        self.assertEqual(response2, "I can help you with that!")
        self.assertEqual(response3, "That's a great question!")
        
        # Verify conversation history
        self.assertEqual(len(assistant.conversation_history), 6)  # 3 user + 3 assistant
        
        # Verify API was called 3 times
        self.assertEqual(mock_openai.call_count, 3)


if __name__ == '__main__':
    unittest.main() 