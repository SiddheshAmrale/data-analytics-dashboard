#!/usr/bin/env python3
"""
Web Interface for AI Projects Collection

A Flask-based web application that provides a user-friendly interface
for all AI projects including chat, image generation, text summarization,
sentiment analysis, and code assistance.
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import sys
sys.path.append('..')

# Import AI project modules
from ai_chat_assistant.main import AIChatAssistant
from ai_image_generator.main import AIImageGenerator
from ai_text_summarizer.main import AITextSummarizer
from ai_sentiment_analyzer.main import AISentimentAnalyzer
from ai_code_assistant.main import AICodeAssistant

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
socketio = SocketIO(app)

# Initialize AI assistants
ai_assistants = {
    'chat': None,
    'image': None,
    'summarizer': None,
    'sentiment': None,
    'code': None
}

def initialize_ai_assistants():
    """Initialize all AI assistants."""
    try:
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            logger.error("OpenAI API key not found")
            return False
        
        ai_assistants['chat'] = AIChatAssistant(api_key=api_key)
        ai_assistants['image'] = AIImageGenerator(api_key=api_key)
        ai_assistants['summarizer'] = AITextSummarizer(api_key=api_key)
        ai_assistants['sentiment'] = AISentimentAnalyzer(api_key=api_key)
        ai_assistants['code'] = AICodeAssistant(api_key=api_key)
        
        logger.info("All AI assistants initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Error initializing AI assistants: {e}")
        return False

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/chat')
def chat():
    """Chat assistant page."""
    return render_template('chat.html')

@app.route('/image')
def image():
    """Image generator page."""
    return render_template('image.html')

@app.route('/summarizer')
def summarizer():
    """Text summarizer page."""
    return render_template('summarizer.html')

@app.route('/sentiment')
def sentiment():
    """Sentiment analyzer page."""
    return render_template('sentiment.html')

@app.route('/code')
def code():
    """Code assistant page."""
    return render_template('code.html')

# API Routes

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Chat API endpoint."""
    try:
        data = request.get_json()
        message = data.get('message', '')
        system_prompt = data.get('system_prompt', None)
        
        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        if not ai_assistants['chat']:
            return jsonify({'error': 'Chat assistant not initialized'}), 500
        
        response = ai_assistants['chat'].get_chat_response(message, system_prompt)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Chat API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_image', methods=['POST'])
def api_generate_image():
    """Image generation API endpoint."""
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        size = data.get('size', '1024x1024')
        quality = data.get('quality', 'standard')
        style = data.get('style', 'vivid')
        
        if not prompt:
            return jsonify({'error': 'Prompt is required'}), 400
        
        if not ai_assistants['image']:
            return jsonify({'error': 'Image generator not initialized'}), 500
        
        image_url = ai_assistants['image'].generate_image(prompt, size, quality, style)
        
        if image_url:
            return jsonify({
                'image_url': image_url,
                'prompt': prompt,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to generate image'}), 500
    except Exception as e:
        logger.error(f"Image generation API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def api_summarize():
    """Text summarization API endpoint."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        max_length = data.get('max_length', 150)
        style = data.get('style', 'concise')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not ai_assistants['summarizer']:
            return jsonify({'error': 'Text summarizer not initialized'}), 500
        
        summary = ai_assistants['summarizer'].summarize_text(text, max_length, style)
        
        if summary:
            return jsonify({
                'summary': summary,
                'original_length': len(text),
                'summary_length': len(summary),
                'compression_ratio': len(summary) / len(text) if text else 0,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to generate summary'}), 500
    except Exception as e:
        logger.error(f"Summarization API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze_sentiment', methods=['POST'])
def api_analyze_sentiment():
    """Sentiment analysis API endpoint."""
    try:
        data = request.get_json()
        text = data.get('text', '')
        detailed = data.get('detailed', False)
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        if not ai_assistants['sentiment']:
            return jsonify({'error': 'Sentiment analyzer not initialized'}), 500
        
        analysis = ai_assistants['sentiment'].analyze_sentiment(text, detailed)
        
        if analysis:
            return jsonify({
                'analysis': analysis,
                'text_length': len(text),
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to analyze sentiment'}), 500
    except Exception as e:
        logger.error(f"Sentiment analysis API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate_code', methods=['POST'])
def api_generate_code():
    """Code generation API endpoint."""
    try:
        data = request.get_json()
        description = data.get('description', '')
        language = data.get('language', 'python')
        style = data.get('style', 'clean')
        
        if not description:
            return jsonify({'error': 'Description is required'}), 400
        
        if not ai_assistants['code']:
            return jsonify({'error': 'Code assistant not initialized'}), 500
        
        code = ai_assistants['code'].generate_code(description, language, style)
        
        if code:
            return jsonify({
                'code': code,
                'language': language,
                'description': description,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to generate code'}), 500
    except Exception as e:
        logger.error(f"Code generation API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/debug_code', methods=['POST'])
def api_debug_code():
    """Code debugging API endpoint."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        error_message = data.get('error_message', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        if not ai_assistants['code']:
            return jsonify({'error': 'Code assistant not initialized'}), 500
        
        fixed_code = ai_assistants['code'].debug_code(code, error_message, language)
        
        if fixed_code:
            return jsonify({
                'fixed_code': fixed_code,
                'language': language,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to debug code'}), 500
    except Exception as e:
        logger.error(f"Code debugging API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/explain_code', methods=['POST'])
def api_explain_code():
    """Code explanation API endpoint."""
    try:
        data = request.get_json()
        code = data.get('code', '')
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({'error': 'Code is required'}), 400
        
        if not ai_assistants['code']:
            return jsonify({'error': 'Code assistant not initialized'}), 500
        
        explanation = ai_assistants['code'].explain_code(code, language)
        
        if explanation:
            return jsonify({
                'explanation': explanation,
                'language': language,
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'error': 'Failed to explain code'}), 500
    except Exception as e:
        logger.error(f"Code explanation API error: {e}")
        return jsonify({'error': str(e)}), 500

# WebSocket events for real-time communication

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info(f"Client connected: {request.sid}")
    emit('status', {'message': 'Connected to AI Projects Web Interface'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info(f"Client disconnected: {request.sid}")

@socketio.on('chat_message')
def handle_chat_message(data):
    """Handle real-time chat messages."""
    try:
        message = data.get('message', '')
        if message and ai_assistants['chat']:
            response = ai_assistants['chat'].get_chat_response(message)
            emit('chat_response', {
                'response': response,
                'timestamp': datetime.now().isoformat()
            })
        else:
            emit('error', {'message': 'Invalid message or assistant not available'})
    except Exception as e:
        logger.error(f"Chat message error: {e}")
        emit('error', {'message': str(e)})

# Error handlers

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', error='Internal server error'), 500

# Health check endpoint

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'ai_assistants': {
            name: 'initialized' if assistant else 'not_initialized'
            for name, assistant in ai_assistants.items()
        }
    })

if __name__ == '__main__':
    # Initialize AI assistants
    if initialize_ai_assistants():
        logger.info("Starting web interface...")
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to initialize AI assistants. Exiting.")
        sys.exit(1) 