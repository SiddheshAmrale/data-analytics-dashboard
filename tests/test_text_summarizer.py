#!/usr/bin/env python3
"""
Unit tests for AI Text Summarizer.

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
sys.path.append('ai_text_summarizer')
from main import AITextSummarizer


class TestAITextSummarizer(unittest.TestCase):
    """Test cases for AITextSummarizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key-12345"
        self.summarizer = AITextSummarizer(api_key=self.api_key)
    
    def test_initialization_with_api_key(self):
        """Test summarizer initialization with API key."""
        summarizer = AITextSummarizer(api_key=self.api_key)
        self.assertEqual(summarizer.api_key, self.api_key)
        self.assertEqual(len(summarizer.summarization_history), 0)
    
    def test_initialization_without_api_key(self):
        """Test summarizer initialization without API key raises error."""
        # Temporarily remove environment variable
        original_key = os.environ.get('OPENAI_API_KEY')
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        with self.assertRaises(ValueError):
            AITextSummarizer()
        
        # Restore environment variable
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
    
    @patch('openai.ChatCompletion.create')
    def test_summarize_text_success(self, mock_openai):
        """Test successful text summarization."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "This is a concise summary of the text."
        mock_openai.return_value = mock_response
        
        text = "This is a very long text that needs to be summarized. It contains many sentences and paragraphs that should be condensed into a shorter version."
        summary = self.summarizer.summarize_text(text)
        
        self.assertEqual(summary, "This is a concise summary of the text.")
        self.assertEqual(len(self.summarizer.summarization_history), 1)
        self.assertEqual(self.summarizer.summarization_history[0]['original_length'], len(text))
        mock_openai.assert_called_once()
    
    @patch('openai.ChatCompletion.create')
    def test_summarize_text_with_custom_parameters(self, mock_openai):
        """Test text summarization with custom parameters."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Custom summary with different style."
        mock_openai.return_value = mock_response
        
        text = "Long text to summarize"
        summary = self.summarizer.summarize_text(
            text,
            max_length=100,
            style="detailed"
        )
        
        self.assertEqual(summary, "Custom summary with different style.")
        # Verify custom parameters were passed
        call_args = mock_openai.call_args
        messages = call_args[1]['messages']
        self.assertIn("detailed", messages[1]['content'])
        self.assertIn("100", messages[1]['content'])
    
    @patch('openai.ChatCompletion.create')
    def test_summarize_text_error_handling(self, mock_openai):
        """Test error handling in text summarization."""
        mock_openai.side_effect = Exception("API Error")
        
        text = "Text to summarize"
        summary = self.summarizer.summarize_text(text)
        
        self.assertIsNone(summary)
        self.assertEqual(len(self.summarizer.summarization_history), 0)
    
    def test_summarize_text_empty_input(self):
        """Test summarization with empty text."""
        summary = self.summarizer.summarize_text("")
        self.assertIsNone(summary)
        
        summary = self.summarizer.summarize_text(None)
        self.assertIsNone(summary)
    
    @patch('openai.ChatCompletion.create')
    def test_summarize_file_success(self, mock_openai):
        """Test successful file summarization."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "File content summary."
        mock_openai.return_value = mock_response
        
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_filename = f.name
            f.write("This is the content of the file that needs to be summarized.")
        
        try:
            summary = self.summarizer.summarize_file(temp_filename)
            
            self.assertEqual(summary, "File content summary.")
            self.assertEqual(len(self.summarizer.summarization_history), 1)
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_summarize_file_not_found(self):
        """Test file summarization with non-existent file."""
        summary = self.summarizer.summarize_file("non_existent_file.txt")
        self.assertIsNone(summary)
    
    @patch('openai.ChatCompletion.create')
    def test_batch_summarize_success(self, mock_openai):
        """Test successful batch summarization."""
        # Mock responses for multiple summaries
        responses = [
            "Summary 1",
            "Summary 2",
            "Summary 3"
        ]
        
        mock_openai.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content=response))])
            for response in responses
        ]
        
        texts = ["Text 1", "Text 2", "Text 3"]
        summaries = self.summarizer.batch_summarize(texts)
        
        self.assertEqual(len(summaries), 3)
        self.assertEqual(summaries[0], "Summary 1")
        self.assertEqual(summaries[1], "Summary 2")
        self.assertEqual(summaries[2], "Summary 3")
        self.assertEqual(len(self.summarizer.summarization_history), 3)
    
    @patch('openai.ChatCompletion.create')
    def test_extract_key_points_success(self, mock_openai):
        """Test successful key points extraction."""
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "1. First key point\n2. Second key point\n3. Third key point"
        mock_openai.return_value = mock_response
        
        text = "Long text with multiple key points to extract"
        key_points = self.summarizer.extract_key_points(text, num_points=3)
        
        self.assertIsNotNone(key_points)
        self.assertEqual(len(key_points), 3)
        self.assertIn("First key point", key_points[0])
        self.assertIn("Second key point", key_points[1])
        self.assertIn("Third key point", key_points[2])
    
    def test_get_summary_statistics(self):
        """Test getting summary statistics."""
        text = "This is a test text with multiple words and sentences."
        stats = self.summarizer.get_summary_statistics(text)
        
        self.assertIsNotNone(stats)
        self.assertIn('word_count', stats)
        self.assertIn('sentence_count', stats)
        self.assertIn('character_count', stats)
        self.assertIn('average_sentence_length', stats)
        
        self.assertEqual(stats['word_count'], 10)
        self.assertEqual(stats['sentence_count'], 1)
        self.assertEqual(stats['character_count'], len(text))
    
    def test_get_summarization_history(self):
        """Test getting summarization history."""
        # Add some test data
        self.summarizer.summarization_history = [
            {"text": "Test 1", "summary": "Summary 1"},
            {"text": "Test 2", "summary": "Summary 2"}
        ]
        
        history = self.summarizer.get_summarization_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["text"], "Test 1")
        self.assertEqual(history[1]["text"], "Test 2")
        # Verify it's a copy, not the original
        self.assertIsNot(history, self.summarizer.summarization_history)
    
    def test_clear_history(self):
        """Test clearing summarization history."""
        self.summarizer.summarization_history = [
            {"text": "Test 1", "summary": "Summary 1"},
            {"text": "Test 2", "summary": "Summary 2"}
        ]
        
        self.assertEqual(len(self.summarizer.summarization_history), 2)
        
        self.summarizer.clear_history()
        self.assertEqual(len(self.summarizer.summarization_history), 0)
    
    def test_save_history(self):
        """Test saving summarization history to file."""
        self.summarizer.summarization_history = [
            {"text": "Test 1", "summary": "Summary 1", "timestamp": "2024-01-01T00:00:00"},
            {"text": "Test 2", "summary": "Summary 2", "timestamp": "2024-01-01T00:00:01"}
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            self.summarizer.save_history(temp_filename)
            
            # Verify file was created and contains correct data
            with open(temp_filename, 'r') as f:
                saved_data = json.load(f)
            
            self.assertEqual(len(saved_data), 2)
            self.assertEqual(saved_data[0]["text"], "Test 1")
            self.assertEqual(saved_data[1]["text"], "Test 2")
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


class TestAITextSummarizerIntegration(unittest.TestCase):
    """Integration tests for AITextSummarizer."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key-12345"
    
    @patch('openai.ChatCompletion.create')
    def test_complete_workflow(self, mock_openai):
        """Test a complete summarization workflow."""
        # Mock responses for different operations
        responses = [
            "Main text summary",
            "File content summary",
            "Batch summary 1",
            "Batch summary 2"
        ]
        
        mock_openai.side_effect = [
            MagicMock(choices=[MagicMock(message=MagicMock(content=response))])
            for response in responses
        ]
        
        summarizer = AITextSummarizer(api_key=self.api_key)
        
        # Test text summarization
        text = "This is a long text that needs summarization."
        summary1 = summarizer.summarize_text(text)
        self.assertEqual(summary1, "Main text summary")
        
        # Test file summarization
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_filename = f.name
            f.write("File content to summarize")
        
        try:
            summary2 = summarizer.summarize_file(temp_filename)
            self.assertEqual(summary2, "File content summary")
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
        
        # Test batch summarization
        texts = ["Text 1", "Text 2"]
        summaries = summarizer.batch_summarize(texts)
        self.assertEqual(len(summaries), 2)
        self.assertEqual(summaries[0], "Batch summary 1")
        self.assertEqual(summaries[1], "Batch summary 2")
        
        # Verify history
        self.assertEqual(len(summarizer.summarization_history), 4)
    
    def test_statistics_calculation(self):
        """Test text statistics calculation."""
        summarizer = AITextSummarizer(api_key=self.api_key)
        
        # Test with simple text
        text = "Hello world. This is a test."
        stats = summarizer.get_summary_statistics(text)
        
        self.assertEqual(stats['word_count'], 6)
        self.assertEqual(stats['sentence_count'], 2)
        self.assertEqual(stats['character_count'], len(text))
        self.assertEqual(stats['average_sentence_length'], 3.0)
        
        # Test with empty text
        stats = summarizer.get_summary_statistics("")
        self.assertEqual(stats['word_count'], 0)
        self.assertEqual(stats['sentence_count'], 0)
        self.assertEqual(stats['character_count'], 0)
        self.assertEqual(stats['average_sentence_length'], 0)


if __name__ == '__main__':
    unittest.main() 