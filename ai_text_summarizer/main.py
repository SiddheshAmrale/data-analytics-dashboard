import openai
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AITextSummarizer:
    def __init__(self, api_key: str = None):
        """Initialize the AI Text Summarizer with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        openai.api_key = self.api_key
        self.summarization_history = []
        
    def summarize_text(self, text: str, max_length: int = 150, style: str = "concise") -> Optional[str]:
        """
        Summarize text using AI.
        
        Args:
            text: Text to summarize
            max_length: Maximum length of summary
            style: Summary style (concise, detailed, bullet_points, key_points)
            
        Returns:
            Summarized text or None if failed
        """
        try:
            logger.info(f"Summarizing text of length {len(text)} characters")
            
            # Create appropriate prompt based on style
            if style == "concise":
                prompt = f"Summarize the following text in {max_length} words or less:\n\n{text}"
            elif style == "detailed":
                prompt = f"Provide a detailed summary of the following text in {max_length} words or less:\n\n{text}"
            elif style == "bullet_points":
                prompt = f"Summarize the following text as bullet points:\n\n{text}"
            elif style == "key_points":
                prompt = f"Extract the key points from the following text:\n\n{text}"
            else:
                prompt = f"Summarize the following text in {max_length} words or less:\n\n{text}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful text summarizer. Provide clear, accurate summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Save summarization info
            summary_info = {
                "original_length": len(text),
                "summary_length": len(summary),
                "style": style,
                "max_length": max_length,
                "summary": summary,
                "timestamp": datetime.now().isoformat()
            }
            self.summarization_history.append(summary_info)
            
            logger.info(f"Summary generated successfully ({len(summary)} characters)")
            return summary
            
        except Exception as e:
            logger.error(f"Error summarizing text: {e}")
            return None
    
    def summarize_file(self, file_path: str, max_length: int = 150, style: str = "concise") -> Optional[str]:
        """
        Summarize text from a file.
        
        Args:
            file_path: Path to the text file
            max_length: Maximum length of summary
            style: Summary style
            
        Returns:
            Summarized text or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self.summarize_text(text, max_length, style)
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def batch_summarize(self, texts: List[str], max_length: int = 150, style: str = "concise") -> List[Optional[str]]:
        """
        Summarize multiple texts in batch.
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum length of each summary
            style: Summary style
            
        Returns:
            List of summaries (None for failed summaries)
        """
        summaries = []
        for i, text in enumerate(texts):
            logger.info(f"Processing text {i+1}/{len(texts)}")
            summary = self.summarize_text(text, max_length, style)
            summaries.append(summary)
        return summaries
    
    def extract_key_points(self, text: str, num_points: int = 5) -> Optional[List[str]]:
        """
        Extract key points from text.
        
        Args:
            text: Text to analyze
            num_points: Number of key points to extract
            
        Returns:
            List of key points or None if failed
        """
        try:
            prompt = f"Extract the {num_points} most important points from the following text:\n\n{text}"
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful text analyzer. Extract key points clearly and concisely."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            result = response.choices[0].message.content.strip()
            
            # Split into points (assuming numbered or bulleted format)
            points = re.split(r'\n+', result)
            points = [point.strip() for point in points if point.strip()]
            
            return points
            
        except Exception as e:
            logger.error(f"Error extracting key points: {e}")
            return None
    
    def get_summary_statistics(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics about the text.
        
        Args:
            text: Text to analyze
            
        Returns:
            Dictionary with text statistics
        """
        try:
            # Basic statistics
            words = text.split()
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            stats = {
                "character_count": len(text),
                "word_count": len(words),
                "sentence_count": len(sentences),
                "average_words_per_sentence": len(words) / len(sentences) if sentences else 0,
                "average_word_length": sum(len(word) for word in words) / len(words) if words else 0
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return None
    
    def get_summarization_history(self) -> List[Dict[str, Any]]:
        """Get history of all summarizations."""
        return self.summarization_history.copy()
    
    def clear_history(self):
        """Clear the summarization history."""
        self.summarization_history = []
    
    def save_history(self, filename: str = None):
        """Save summarization history to JSON file."""
        import json
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"summarization_history_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.summarization_history, f, indent=2)
        
        logger.info(f"Summarization history saved to {filename}")

def main():
    """Main function to demonstrate the AI Text Summarizer."""
    print("📝 AI Text Summarizer")
    print("=" * 50)
    
    # Initialize the summarizer
    try:
        summarizer = AITextSummarizer()
        print("✅ Text summarizer initialized successfully!")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenAI API key as an environment variable: OPENAI_API_KEY")
        return
    
    print("\n🎯 Available commands:")
    print("- 'summarize <text>' - Summarize text")
    print("- 'file <file_path>' - Summarize text file")
    print("- 'keypoints <text>' - Extract key points")
    print("- 'stats <text>' - Get text statistics")
    print("- 'history' - Show summarization history")
    print("- 'clear' - Clear history")
    print("- 'save' - Save history to file")
    print("- 'quit' - Exit")
    print("-" * 50)
    
    while True:
        user_input = input("\nEnter command: ").strip()
        
        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break
        elif user_input.lower() == 'history':
            history = summarizer.get_summarization_history()
            if history:
                print(f"\n📋 Summarization History ({len(history)} entries):")
                for i, entry in enumerate(history, 1):
                    print(f"{i}. {entry['summary'][:50]}... ({entry['style']})")
            else:
                print("📋 No summarizations yet.")
            continue
        elif user_input.lower() == 'clear':
            summarizer.clear_history()
            print("🗑️ History cleared!")
            continue
        elif user_input.lower() == 'save':
            summarizer.save_history()
            continue
        elif user_input.startswith('summarize '):
            text = user_input[10:].strip()
            if text:
                print(f"\n📝 Summarizing text...")
                summary = summarizer.summarize_text(text)
                if summary:
                    print(f"✅ Summary: {summary}")
                else:
                    print("❌ Failed to summarize text")
            else:
                print("❌ Please provide text to summarize")
            continue
        elif user_input.startswith('file '):
            file_path = user_input[5:].strip()
            if os.path.exists(file_path):
                print(f"\n📄 Summarizing file: {file_path}")
                summary = summarizer.summarize_file(file_path)
                if summary:
                    print(f"✅ Summary: {summary}")
                else:
                    print("❌ Failed to summarize file")
            else:
                print(f"❌ File not found: {file_path}")
            continue
        elif user_input.startswith('keypoints '):
            text = user_input[10:].strip()
            if text:
                print(f"\n🔑 Extracting key points...")
                points = summarizer.extract_key_points(text)
                if points:
                    print("✅ Key Points:")
                    for i, point in enumerate(points, 1):
                        print(f"{i}. {point}")
                else:
                    print("❌ Failed to extract key points")
            else:
                print("❌ Please provide text")
            continue
        elif user_input.startswith('stats '):
            text = user_input[6:].strip()
            if text:
                print(f"\n📊 Analyzing text statistics...")
                stats = summarizer.get_summary_statistics(text)
                if stats:
                    print("✅ Text Statistics:")
                    for key, value in stats.items():
                        print(f"  {key.replace('_', ' ').title()}: {value:.2f}")
                else:
                    print("❌ Failed to calculate statistics")
            else:
                print("❌ Please provide text")
            continue
        elif not user_input:
            continue
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main() 