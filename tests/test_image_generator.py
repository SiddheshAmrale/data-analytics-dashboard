#!/usr/bin/env python3
"""
Unit tests for AI Image Generator.

Tests cover core functionality, error handling, and edge cases.
"""

import unittest
from unittest.mock import patch, MagicMock, mock_open
import json
import os
import tempfile
from datetime import datetime

# Import the module to test
import sys
sys.path.append('ai_image_generator')
from main import AIImageGenerator


class TestAIImageGenerator(unittest.TestCase):
    """Test cases for AIImageGenerator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key-12345"
        self.generator = AIImageGenerator(api_key=self.api_key)
    
    def test_initialization_with_api_key(self):
        """Test generator initialization with API key."""
        generator = AIImageGenerator(api_key=self.api_key)
        self.assertEqual(generator.api_key, self.api_key)
        self.assertEqual(len(generator.generated_images), 0)
    
    def test_initialization_without_api_key(self):
        """Test generator initialization without API key raises error."""
        # Temporarily remove environment variable
        original_key = os.environ.get('OPENAI_API_KEY')
        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']
        
        with self.assertRaises(ValueError):
            AIImageGenerator()
        
        # Restore environment variable
        if original_key:
            os.environ['OPENAI_API_KEY'] = original_key
    
    @patch('openai.Image.create')
    def test_generate_image_success(self, mock_openai):
        """Test successful image generation."""
        # Mock OpenAI response
        mock_response = MagicMock()
        mock_response['data'] = [{'url': 'https://example.com/image.png'}]
        mock_openai.return_value = mock_response
        
        url = self.generator.generate_image("A beautiful sunset")
        
        self.assertEqual(url, 'https://example.com/image.png')
        self.assertEqual(len(self.generator.generated_images), 1)
        self.assertEqual(self.generator.generated_images[0]['prompt'], "A beautiful sunset")
        mock_openai.assert_called_once()
    
    @patch('openai.Image.create')
    def test_generate_image_with_custom_parameters(self, mock_openai):
        """Test image generation with custom parameters."""
        mock_response = MagicMock()
        mock_response['data'] = [{'url': 'https://example.com/image.png'}]
        mock_openai.return_value = mock_response
        
        url = self.generator.generate_image(
            "A futuristic city",
            size="1792x1024",
            quality="hd",
            style="vivid"
        )
        
        self.assertEqual(url, 'https://example.com/image.png')
        # Verify custom parameters were passed
        call_args = mock_openai.call_args
        self.assertEqual(call_args[1]['size'], "1792x1024")
        self.assertEqual(call_args[1]['quality'], "hd")
        self.assertEqual(call_args[1]['style'], "vivid")
    
    @patch('openai.Image.create')
    def test_generate_image_error_handling(self, mock_openai):
        """Test error handling in image generation."""
        mock_openai.side_effect = Exception("API Error")
        
        url = self.generator.generate_image("A beautiful sunset")
        
        self.assertIsNone(url)
        self.assertEqual(len(self.generator.generated_images), 0)
    
    @patch('openai.Image.create_variation')
    def test_generate_variations_success(self, mock_openai):
        """Test successful image variation generation."""
        mock_response = MagicMock()
        mock_response['data'] = [
            {'url': 'https://example.com/variation1.png'},
            {'url': 'https://example.com/variation2.png'}
        ]
        mock_openai.return_value = mock_response
        
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_image_path = f.name
            f.write(b'fake image data')
        
        try:
            urls = self.generator.generate_variations(temp_image_path, n=2)
            
            self.assertEqual(len(urls), 2)
            self.assertEqual(urls[0], 'https://example.com/variation1.png')
            self.assertEqual(urls[1], 'https://example.com/variation2.png')
            self.assertEqual(len(self.generator.generated_images), 2)
        finally:
            # Clean up
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
    
    @patch('openai.Image.create_variation')
    def test_generate_variations_error_handling(self, mock_openai):
        """Test error handling in variation generation."""
        mock_openai.side_effect = Exception("API Error")
        
        # Create a temporary image file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_image_path = f.name
            f.write(b'fake image data')
        
        try:
            urls = self.generator.generate_variations(temp_image_path)
            
            self.assertEqual(urls, [])
            self.assertEqual(len(self.generator.generated_images), 0)
        finally:
            # Clean up
            if os.path.exists(temp_image_path):
                os.unlink(temp_image_path)
    
    @patch('requests.get')
    def test_download_image_success(self, mock_requests):
        """Test successful image download."""
        mock_response = MagicMock()
        mock_response.content = b'fake image data'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        url = "https://example.com/image.png"
        filename = self.generator.download_image(url)
        
        self.assertIsNotNone(filename)
        self.assertTrue(os.path.exists(filename))
        
        # Verify file content
        with open(filename, 'rb') as f:
            content = f.read()
        self.assertEqual(content, b'fake image data')
        
        # Clean up
        if os.path.exists(filename):
            os.unlink(filename)
    
    @patch('requests.get')
    def test_download_image_with_custom_filename(self, mock_requests):
        """Test image download with custom filename."""
        mock_response = MagicMock()
        mock_response.content = b'fake image data'
        mock_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_response
        
        url = "https://example.com/image.png"
        custom_filename = "my_custom_image.png"
        filename = self.generator.download_image(url, custom_filename)
        
        self.assertEqual(filename, custom_filename)
        self.assertTrue(os.path.exists(filename))
        
        # Clean up
        if os.path.exists(filename):
            os.unlink(filename)
    
    @patch('requests.get')
    def test_download_image_error_handling(self, mock_requests):
        """Test error handling in image download."""
        mock_requests.side_effect = Exception("Download Error")
        
        url = "https://example.com/image.png"
        filename = self.generator.download_image(url)
        
        self.assertIsNone(filename)
    
    def test_get_generation_history(self):
        """Test getting generation history."""
        # Add some test data
        self.generator.generated_images = [
            {"prompt": "Test 1", "url": "url1"},
            {"prompt": "Test 2", "url": "url2"}
        ]
        
        history = self.generator.get_generation_history()
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["prompt"], "Test 1")
        self.assertEqual(history[1]["prompt"], "Test 2")
        # Verify it's a copy, not the original
        self.assertIsNot(history, self.generator.generated_images)
    
    def test_clear_history(self):
        """Test clearing generation history."""
        self.generator.generated_images = [
            {"prompt": "Test 1", "url": "url1"},
            {"prompt": "Test 2", "url": "url2"}
        ]
        
        self.assertEqual(len(self.generator.generated_images), 2)
        
        self.generator.clear_history()
        self.assertEqual(len(self.generator.generated_images), 0)
    
    def test_save_history(self):
        """Test saving generation history to file."""
        self.generator.generated_images = [
            {"prompt": "Test 1", "url": "url1", "timestamp": "2024-01-01T00:00:00"},
            {"prompt": "Test 2", "url": "url2", "timestamp": "2024-01-01T00:00:01"}
        ]
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_filename = f.name
        
        try:
            self.generator.save_history(temp_filename)
            
            # Verify file was created and contains correct data
            with open(temp_filename, 'r') as f:
                saved_data = json.load(f)
            
            self.assertEqual(len(saved_data), 2)
            self.assertEqual(saved_data[0]["prompt"], "Test 1")
            self.assertEqual(saved_data[1]["prompt"], "Test 2")
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


class TestAIImageGeneratorIntegration(unittest.TestCase):
    """Integration tests for AIImageGenerator."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.api_key = "test-api-key-12345"
    
    @patch('openai.Image.create')
    @patch('requests.get')
    def test_complete_workflow(self, mock_requests, mock_openai):
        """Test a complete image generation and download workflow."""
        # Mock image generation
        mock_gen_response = MagicMock()
        mock_gen_response['data'] = [{'url': 'https://example.com/image.png'}]
        mock_openai.return_value = mock_gen_response
        
        # Mock image download
        mock_download_response = MagicMock()
        mock_download_response.content = b'fake image data'
        mock_download_response.raise_for_status.return_value = None
        mock_requests.return_value = mock_download_response
        
        generator = AIImageGenerator(api_key=self.api_key)
        
        # Generate image
        url = generator.generate_image("A beautiful sunset")
        self.assertEqual(url, 'https://example.com/image.png')
        
        # Download image
        filename = generator.download_image(url)
        self.assertIsNotNone(filename)
        self.assertTrue(os.path.exists(filename))
        
        # Verify history
        self.assertEqual(len(generator.generated_images), 1)
        self.assertEqual(generator.generated_images[0]['prompt'], "A beautiful sunset")
        
        # Clean up
        if os.path.exists(filename):
            os.unlink(filename)
    
    @patch('openai.Image.create')
    def test_batch_generation(self, mock_openai):
        """Test generating multiple images in sequence."""
        # Mock responses for multiple generations
        responses = [
            {'data': [{'url': f'https://example.com/image{i}.png'}]}
            for i in range(3)
        ]
        mock_openai.side_effect = responses
        
        generator = AIImageGenerator(api_key=self.api_key)
        
        prompts = ["Sunset", "Mountains", "Ocean"]
        urls = []
        
        for prompt in prompts:
            url = generator.generate_image(prompt)
            urls.append(url)
        
        self.assertEqual(len(urls), 3)
        self.assertEqual(urls[0], 'https://example.com/image0.png')
        self.assertEqual(urls[1], 'https://example.com/image1.png')
        self.assertEqual(urls[2], 'https://example.com/image2.png')
        
        # Verify all generations are in history
        self.assertEqual(len(generator.generated_images), 3)
        self.assertEqual(mock_openai.call_count, 3)


if __name__ == '__main__':
    unittest.main() 