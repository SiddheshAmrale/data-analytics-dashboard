#!/usr/bin/env python3
"""
AI Voice Assistant

A voice-based AI assistant that can:
- Convert speech to text
- Process voice commands
- Generate voice responses
- Handle natural language conversations
"""

import os
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List
import tempfile
import wave
import pyaudio
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIVoiceAssistant:
    """AI Voice Assistant for speech-to-text and text-to-speech operations."""
    
    def __init__(self, api_key: str = None):
        """Initialize the AI Voice Assistant.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from environment.
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.conversation_history = []
        self.voice_settings = {
            "voice": "alloy",
            "model": "tts-1",
            "speed": 1.0
        }
        self.audio_settings = {
            "sample_rate": 16000,
            "channels": 1,
            "chunk_size": 1024,
            "format": pyaudio.paInt16
        }
        
    def record_audio(self, duration: int = 5) -> Optional[str]:
        """Record audio from microphone.
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Path to recorded audio file or None if failed
        """
        try:
            p = pyaudio.PyAudio()
            
            # Open stream
            stream = p.open(
                format=self.audio_settings["format"],
                channels=self.audio_settings["channels"],
                rate=self.audio_settings["sample_rate"],
                input=True,
                frames_per_buffer=self.audio_settings["chunk_size"]
            )
            
            logger.info(f"Recording for {duration} seconds...")
            frames = []
            
            for i in range(0, int(self.audio_settings["sample_rate"] / self.audio_settings["chunk_size"] * duration)):
                data = stream.read(self.audio_settings["chunk_size"])
                frames.append(data)
            
            logger.info("Recording finished.")
            
            # Stop and close stream
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            # Save audio file
            temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
            temp_filename = temp_file.name
            temp_file.close()
            
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.audio_settings["channels"])
                wf.setsampwidth(p.get_sample_size(self.audio_settings["format"]))
                wf.setframerate(self.audio_settings["sample_rate"])
                wf.writeframes(b''.join(frames))
            
            return temp_filename
            
        except Exception as e:
            logger.error(f"Error recording audio: {e}")
            return None
    
    def transcribe_audio(self, audio_file_path: str) -> Optional[str]:
        """Transcribe audio file to text using OpenAI Whisper.
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text or None if failed
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            return transcript.text
            
        except Exception as e:
            logger.error(f"Error transcribing audio: {e}")
            return None
    
    def generate_voice_response(self, text: str, output_file: str = None) -> Optional[str]:
        """Generate speech from text using OpenAI TTS.
        
        Args:
            text: Text to convert to speech
            output_file: Output file path (optional)
            
        Returns:
            Path to generated audio file or None if failed
        """
        try:
            if output_file is None:
                output_file = f"voice_response_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            
            response = self.client.audio.speech.create(
                model=self.voice_settings["model"],
                voice=self.voice_settings["voice"],
                input=text,
                speed=self.voice_settings["speed"]
            )
            
            response.stream_to_file(output_file)
            logger.info(f"Voice response saved to: {output_file}")
            
            return output_file
            
        except Exception as e:
            logger.error(f"Error generating voice response: {e}")
            return None
    
    def process_voice_command(self, command: str) -> str:
        """Process voice command and generate response.
        
        Args:
            command: Voice command text
            
        Returns:
            Response text
        """
        try:
            # Add command to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": command,
                "timestamp": datetime.now().isoformat()
            })
            
            # Generate response using GPT
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful voice assistant. Provide concise, helpful responses suitable for voice output."},
                    {"role": "user", "content": command}
                ],
                max_tokens=150
            )
            
            response_text = response.choices[0].message.content
            
            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error processing voice command: {e}")
            return "I'm sorry, I encountered an error processing your request."
    
    def voice_conversation(self, duration: int = 30) -> Dict[str, Any]:
        """Conduct a voice conversation.
        
        Args:
            duration: Conversation duration in seconds
            
        Returns:
            Dictionary with conversation results
        """
        logger.info(f"Starting voice conversation for {duration} seconds...")
        
        conversation_data = {
            "start_time": datetime.now().isoformat(),
            "duration": duration,
            "exchanges": [],
            "status": "completed"
        }
        
        try:
            start_time = datetime.now()
            
            while (datetime.now() - start_time).seconds < duration:
                # Record audio
                audio_file = self.record_audio(duration=3)
                if not audio_file:
                    continue
                
                # Transcribe audio
                transcription = self.transcribe_audio(audio_file)
                if not transcription:
                    continue
                
                # Process command
                response = self.process_voice_command(transcription)
                
                # Generate voice response
                voice_file = self.generate_voice_response(response)
                
                # Record exchange
                exchange = {
                    "timestamp": datetime.now().isoformat(),
                    "user_input": transcription,
                    "assistant_response": response,
                    "audio_files": {
                        "input": audio_file,
                        "output": voice_file
                    }
                }
                conversation_data["exchanges"].append(exchange)
                
                # Clean up input audio file
                try:
                    os.unlink(audio_file)
                except:
                    pass
                
                logger.info(f"Exchange: {transcription} -> {response}")
            
        except KeyboardInterrupt:
            logger.info("Conversation interrupted by user")
            conversation_data["status"] = "interrupted"
        except Exception as e:
            logger.error(f"Error in voice conversation: {e}")
            conversation_data["status"] = "error"
        
        conversation_data["end_time"] = datetime.now().isoformat()
        return conversation_data
    
    def set_voice_settings(self, voice: str = None, model: str = None, speed: float = None):
        """Update voice settings.
        
        Args:
            voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
            model: TTS model to use
            speed: Speech speed (0.25 to 4.0)
        """
        if voice:
            self.voice_settings["voice"] = voice
        if model:
            self.voice_settings["model"] = model
        if speed:
            self.voice_settings["speed"] = max(0.25, min(4.0, speed))
    
    def set_audio_settings(self, sample_rate: int = None, channels: int = None, chunk_size: int = None):
        """Update audio recording settings.
        
        Args:
            sample_rate: Audio sample rate
            channels: Number of audio channels
            chunk_size: Audio chunk size
        """
        if sample_rate:
            self.audio_settings["sample_rate"] = sample_rate
        if channels:
            self.audio_settings["channels"] = channels
        if chunk_size:
            self.audio_settings["chunk_size"] = chunk_size
    
    def get_conversation_history(self) -> List[Dict[str, Any]]:
        """Get conversation history.
        
        Returns:
            List of conversation exchanges
        """
        return self.conversation_history.copy()
    
    def clear_conversation_history(self):
        """Clear conversation history."""
        self.conversation_history.clear()
    
    def save_conversation(self, filename: str):
        """Save conversation history to file.
        
        Args:
            filename: Output file path
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.conversation_history, f, indent=2)
            logger.info(f"Conversation saved to: {filename}")
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
    
    def load_conversation(self, filename: str):
        """Load conversation history from file.
        
        Args:
            filename: Input file path
        """
        try:
            with open(filename, 'r') as f:
                self.conversation_history = json.load(f)
            logger.info(f"Conversation loaded from: {filename}")
        except Exception as e:
            logger.error(f"Error loading conversation: {e}")


def main():
    """Main function for interactive voice assistant."""
    print("🎤 AI Voice Assistant")
    print("=" * 30)
    
    try:
        # Initialize voice assistant
        assistant = AIVoiceAssistant()
        
        print("Voice Assistant initialized successfully!")
        print("\nAvailable commands:")
        print("1. 'record' - Record and transcribe audio")
        print("2. 'conversation' - Start voice conversation")
        print("3. 'settings' - Configure voice settings")
        print("4. 'history' - View conversation history")
        print("5. 'save' - Save conversation")
        print("6. 'load' - Load conversation")
        print("7. 'clear' - Clear conversation history")
        print("8. 'quit' - Exit")
        
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                print("Goodbye!")
                break
            elif command == 'record':
                print("Recording audio... (speak now)")
                audio_file = assistant.record_audio(duration=5)
                if audio_file:
                    transcription = assistant.transcribe_audio(audio_file)
                    if transcription:
                        print(f"Transcription: {transcription}")
                        response = assistant.process_voice_command(transcription)
                        print(f"Response: {response}")
                        
                        # Generate voice response
                        voice_file = assistant.generate_voice_response(response)
                        if voice_file:
                            print(f"Voice response saved to: {voice_file}")
                    else:
                        print("Failed to transcribe audio")
                else:
                    print("Failed to record audio")
            elif command == 'conversation':
                duration = int(input("Enter conversation duration (seconds): "))
                conversation = assistant.voice_conversation(duration=duration)
                print(f"Conversation completed. Status: {conversation['status']}")
                print(f"Exchanges: {len(conversation['exchanges'])}")
            elif command == 'settings':
                print("Current voice settings:")
                for key, value in assistant.voice_settings.items():
                    print(f"  {key}: {value}")
                
                voice = input("Enter new voice (or press Enter to skip): ").strip()
                if voice:
                    assistant.set_voice_settings(voice=voice)
                print("Settings updated!")
            elif command == 'history':
                history = assistant.get_conversation_history()
                print(f"Conversation history ({len(history)} exchanges):")
                for i, exchange in enumerate(history[-5:], 1):  # Show last 5
                    print(f"{i}. {exchange['role']}: {exchange['content'][:50]}...")
            elif command == 'save':
                filename = input("Enter filename: ")
                assistant.save_conversation(filename)
            elif command == 'load':
                filename = input("Enter filename: ")
                assistant.load_conversation(filename)
            elif command == 'clear':
                assistant.clear_conversation_history()
                print("Conversation history cleared!")
            else:
                print("Unknown command. Type 'quit' to exit.")
                
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 