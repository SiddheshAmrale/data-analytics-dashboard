#!/usr/bin/env python3
"""
Mobile App Interface for AI Projects Collection

A Kivy-based mobile application that provides a touch-friendly interface
for all AI projects including chat, image generation, text summarization,
sentiment analysis, and code assistance.
"""

import os
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
from kivy.storage.jsonstore import JsonStore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set window size for desktop testing
if platform == 'desktop':
    Window.size = (400, 600)


class AIChatTab(BoxLayout):
    """Chat assistant tab."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Chat history
        self.chat_history = ScrollView()
        self.chat_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_layout.bind(minimum_height=self.chat_layout.setter('height'))
        self.chat_history.add_widget(self.chat_layout)
        self.add_widget(self.chat_history)
        
        # Input area
        input_layout = BoxLayout(size_hint_y=None, height=50)
        self.message_input = TextInput(
            hint_text='Type your message...',
            multiline=False,
            size_hint_x=0.7
        )
        self.send_button = Button(
            text='Send',
            size_hint_x=0.3,
            on_press=self.send_message
        )
        input_layout.add_widget(self.message_input)
        input_layout.add_widget(self.send_button)
        self.add_widget(input_layout)
        
        # API configuration
        self.api_url = "http://localhost:5000/api/chat"
        
    def send_message(self, instance):
        """Send message to AI chat."""
        message = self.message_input.text.strip()
        if not message:
            return
            
        # Add user message to chat
        self.add_message_to_chat("You", message, "user")
        self.message_input.text = ""
        
        # Show loading
        loading_label = Label(text="AI is thinking...", size_hint_y=None, height=30)
        self.chat_layout.add_widget(loading_label)
        
        # Send to API
        try:
            response = requests.post(self.api_url, json={'message': message})
            if response.status_code == 200:
                data = response.json()
                ai_response = data.get('response', 'No response received')
                self.add_message_to_chat("AI", ai_response, "assistant")
            else:
                self.add_message_to_chat("System", "Error: Failed to get response", "error")
        except Exception as e:
            self.add_message_to_chat("System", f"Error: {str(e)}", "error")
        finally:
            # Remove loading message
            self.chat_layout.remove_widget(loading_label)
            
    def add_message_to_chat(self, sender: str, message: str, message_type: str):
        """Add message to chat history."""
        message_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=60)
        
        # Sender label
        sender_label = Label(
            text=sender,
            size_hint_y=None,
            height=20,
            color=(0.2, 0.6, 1, 1) if message_type == "user" else (0.2, 0.8, 0.2, 1)
        )
        message_layout.add_widget(sender_label)
        
        # Message text
        message_label = Label(
            text=message,
            size_hint_y=None,
            height=40,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top'
        )
        message_layout.add_widget(message_label)
        
        self.chat_layout.add_widget(message_layout)


class AIImageTab(BoxLayout):
    """Image generator tab."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Prompt input
        self.prompt_input = TextInput(
            hint_text='Describe the image you want to generate...',
            multiline=True,
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.prompt_input)
        
        # Generate button
        self.generate_button = Button(
            text='Generate Image',
            size_hint_y=None,
            height=50,
            on_press=self.generate_image
        )
        self.add_widget(self.generate_button)
        
        # Progress bar
        self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=20)
        self.progress_bar.opacity = 0
        self.add_widget(self.progress_bar)
        
        # Image display
        self.image_widget = Image(size_hint_y=None, height=300)
        self.add_widget(self.image_widget)
        
        # API configuration
        self.api_url = "http://localhost:5000/api/generate_image"
        
    def generate_image(self, instance):
        """Generate image from prompt."""
        prompt = self.prompt_input.text.strip()
        if not prompt:
            return
            
        # Show progress
        self.progress_bar.opacity = 1
        self.generate_button.disabled = True
        
        try:
            response = requests.post(self.api_url, json={'prompt': prompt})
            if response.status_code == 200:
                data = response.json()
                image_url = data.get('image_url')
                if image_url:
                    # Download and display image
                    img_response = requests.get(image_url)
                    if img_response.status_code == 200:
                        # Save image temporarily
                        temp_path = f"temp_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                        with open(temp_path, 'wb') as f:
                            f.write(img_response.content)
                        self.image_widget.source = temp_path
                    else:
                        self.show_error("Failed to download image")
                else:
                    self.show_error("No image URL received")
            else:
                self.show_error("Failed to generate image")
        except Exception as e:
            self.show_error(f"Error: {str(e)}")
        finally:
            # Hide progress
            self.progress_bar.opacity = 0
            self.generate_button.disabled = False
            
    def show_error(self, message: str):
        """Show error popup."""
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(None, None),
            size=(300, 200)
        )
        popup.open()


class AISummarizerTab(BoxLayout):
    """Text summarizer tab."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Text input
        self.text_input = TextInput(
            hint_text='Enter text to summarize...',
            multiline=True,
            size_hint_y=None,
            height=150
        )
        self.add_widget(self.text_input)
        
        # Summarize button
        self.summarize_button = Button(
            text='Summarize',
            size_hint_y=None,
            height=50,
            on_press=self.summarize_text
        )
        self.add_widget(self.summarize_button)
        
        # Summary display
        self.summary_label = Label(
            text='Summary will appear here...',
            size_hint_y=None,
            height=200,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top'
        )
        self.add_widget(self.summary_label)
        
        # API configuration
        self.api_url = "http://localhost:5000/api/summarize"
        
    def summarize_text(self, instance):
        """Summarize text."""
        text = self.text_input.text.strip()
        if not text:
            return
            
        self.summarize_button.disabled = True
        
        try:
            response = requests.post(self.api_url, json={'text': text})
            if response.status_code == 200:
                data = response.json()
                summary = data.get('summary', 'No summary generated')
                self.summary_label.text = summary
            else:
                self.summary_label.text = "Error: Failed to generate summary"
        except Exception as e:
            self.summary_label.text = f"Error: {str(e)}"
        finally:
            self.summarize_button.disabled = False


class AISentimentTab(BoxLayout):
    """Sentiment analyzer tab."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Text input
        self.text_input = TextInput(
            hint_text='Enter text to analyze sentiment...',
            multiline=True,
            size_hint_y=None,
            height=150
        )
        self.add_widget(self.text_input)
        
        # Analyze button
        self.analyze_button = Button(
            text='Analyze Sentiment',
            size_hint_y=None,
            height=50,
            on_press=self.analyze_sentiment
        )
        self.add_widget(self.analyze_button)
        
        # Results display
        self.results_label = Label(
            text='Sentiment analysis results will appear here...',
            size_hint_y=None,
            height=200,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top'
        )
        self.add_widget(self.results_label)
        
        # API configuration
        self.api_url = "http://localhost:5000/api/analyze_sentiment"
        
    def analyze_sentiment(self, instance):
        """Analyze sentiment of text."""
        text = self.text_input.text.strip()
        if not text:
            return
            
        self.analyze_button.disabled = True
        
        try:
            response = requests.post(self.api_url, json={'text': text, 'detailed': True})
            if response.status_code == 200:
                data = response.json()
                analysis = data.get('analysis', {})
                
                # Format results
                sentiment = analysis.get('sentiment', 'Unknown')
                confidence = analysis.get('confidence', 0)
                emotions = analysis.get('emotions', {})
                
                results = f"Sentiment: {sentiment}\n"
                results += f"Confidence: {confidence:.2f}\n\n"
                results += "Emotions:\n"
                for emotion, score in emotions.items():
                    results += f"  {emotion}: {score:.2f}\n"
                
                self.results_label.text = results
            else:
                self.results_label.text = "Error: Failed to analyze sentiment"
        except Exception as e:
            self.results_label.text = f"Error: {str(e)}"
        finally:
            self.analyze_button.disabled = False


class AICodeTab(BoxLayout):
    """Code assistant tab."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 10
        self.spacing = 10
        
        # Description input
        self.desc_input = TextInput(
            hint_text='Describe the code you want to generate...',
            multiline=True,
            size_hint_y=None,
            height=100
        )
        self.add_widget(self.desc_input)
        
        # Generate button
        self.generate_button = Button(
            text='Generate Code',
            size_hint_y=None,
            height=50,
            on_press=self.generate_code
        )
        self.add_widget(self.generate_button)
        
        # Code display
        self.code_label = Label(
            text='Generated code will appear here...',
            size_hint_y=None,
            height=300,
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            font_name='Courier'
        )
        self.add_widget(self.code_label)
        
        # API configuration
        self.api_url = "http://localhost:5000/api/generate_code"
        
    def generate_code(self, instance):
        """Generate code from description."""
        description = self.desc_input.text.strip()
        if not description:
            return
            
        self.generate_button.disabled = True
        
        try:
            response = requests.post(self.api_url, json={
                'description': description,
                'language': 'python',
                'style': 'clean'
            })
            if response.status_code == 200:
                data = response.json()
                code = data.get('code', 'No code generated')
                self.code_label.text = code
            else:
                self.code_label.text = "Error: Failed to generate code"
        except Exception as e:
            self.code_label.text = f"Error: {str(e)}"
        finally:
            self.generate_button.disabled = False


class AIProjectsMobileApp(App):
    """Main mobile app class."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "AI Projects Collection"
        
    def build(self):
        """Build the app interface."""
        # Create main layout
        main_layout = BoxLayout(orientation='vertical')
        
        # Create tabbed panel
        tab_panel = TabbedPanel()
        
        # Chat tab
        chat_tab = TabbedPanelItem(text='Chat')
        chat_tab.add_widget(AIChatTab())
        tab_panel.add_widget(chat_tab)
        
        # Image tab
        image_tab = TabbedPanelItem(text='Image')
        image_tab.add_widget(AIImageTab())
        tab_panel.add_widget(image_tab)
        
        # Summarizer tab
        summarizer_tab = TabbedPanelItem(text='Summarizer')
        summarizer_tab.add_widget(AISummarizerTab())
        tab_panel.add_widget(summarizer_tab)
        
        # Sentiment tab
        sentiment_tab = TabbedPanelItem(text='Sentiment')
        sentiment_tab.add_widget(AISentimentTab())
        tab_panel.add_widget(sentiment_tab)
        
        # Code tab
        code_tab = TabbedPanelItem(text='Code')
        code_tab.add_widget(AICodeTab())
        tab_panel.add_widget(code_tab)
        
        main_layout.add_widget(tab_panel)
        
        return main_layout


if __name__ == '__main__':
    AIProjectsMobileApp().run() 