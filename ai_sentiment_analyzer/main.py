import openai
import os
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AISentimentAnalyzer:
    def __init__(self, api_key: str = None):
        """Initialize the AI Sentiment Analyzer with OpenAI API key."""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass it to constructor.")
        
        openai.api_key = self.api_key
        self.analysis_history = []
        
    def analyze_sentiment(self, text: str, detailed: bool = False) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment of text using AI.
        
        Args:
            text: Text to analyze
            detailed: Whether to return detailed analysis
            
        Returns:
            Dictionary with sentiment analysis results or None if failed
        """
        try:
            logger.info(f"Analyzing sentiment for text of length {len(text)}")
            
            if detailed:
                prompt = f"""Analyze the sentiment of the following text and provide a detailed analysis including:
1. Overall sentiment (positive, negative, neutral)
2. Sentiment score (0-10, where 0 is very negative and 10 is very positive)
3. Confidence level (0-100%)
4. Key emotional indicators
5. Tone analysis
6. Specific emotions detected

Text: {text}

Please respond in JSON format with the following structure:
{{
    "sentiment": "positive/negative/neutral",
    "score": 7.5,
    "confidence": 85,
    "emotional_indicators": ["joy", "excitement"],
    "tone": "enthusiastic",
    "emotions": ["happiness", "optimism"],
    "reasoning": "The text expresses positive emotions..."
}}"""
            else:
                prompt = f"""Analyze the sentiment of the following text and provide a simple analysis:

Text: {text}

Please respond in JSON format with the following structure:
{{
    "sentiment": "positive/negative/neutral",
    "score": 7.5,
    "confidence": 85,
    "summary": "Brief explanation of the sentiment"
}}"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Provide accurate, consistent analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON response
            try:
                result = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback: extract basic sentiment
                result = self._extract_basic_sentiment(result_text)
            
            # Add metadata
            result["text_length"] = len(text)
            result["timestamp"] = datetime.now().isoformat()
            
            # Save to history
            self.analysis_history.append(result)
            
            logger.info(f"Sentiment analysis completed: {result.get('sentiment', 'unknown')}")
            return result
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return None
    
    def _extract_basic_sentiment(self, text: str) -> Dict[str, Any]:
        """Extract basic sentiment from non-JSON response."""
        text_lower = text.lower()
        
        # Simple keyword-based sentiment detection
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "happy", "love", "like"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "sad", "angry", "frustrated"]
        
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = "positive"
            score = min(10, 5 + positive_count)
        elif negative_count > positive_count:
            sentiment = "negative"
            score = max(0, 5 - negative_count)
        else:
            sentiment = "neutral"
            score = 5
        
        return {
            "sentiment": sentiment,
            "score": score,
            "confidence": 60,
            "summary": "Basic sentiment analysis based on keyword detection"
        }
    
    def analyze_batch(self, texts: List[str], detailed: bool = False) -> List[Optional[Dict[str, Any]]]:
        """
        Analyze sentiment of multiple texts.
        
        Args:
            texts: List of texts to analyze
            detailed: Whether to return detailed analysis
            
        Returns:
            List of analysis results (None for failed analyses)
        """
        results = []
        for i, text in enumerate(texts):
            logger.info(f"Processing text {i+1}/{len(texts)}")
            result = self.analyze_sentiment(text, detailed)
            results.append(result)
        return results
    
    def analyze_file(self, file_path: str, detailed: bool = False) -> Optional[Dict[str, Any]]:
        """
        Analyze sentiment of text from a file.
        
        Args:
            file_path: Path to the text file
            detailed: Whether to return detailed analysis
            
        Returns:
            Analysis result or None if failed
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            return self.analyze_sentiment(text, detailed)
            
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return None
    
    def get_sentiment_trends(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze trends from multiple sentiment analyses.
        
        Args:
            analyses: List of sentiment analysis results
            
        Returns:
            Dictionary with trend analysis
        """
        if not analyses:
            return {}
        
        sentiments = [a.get('sentiment', 'neutral') for a in analyses if a]
        scores = [a.get('score', 5) for a in analyses if a and 'score' in a]
        
        sentiment_counts = Counter(sentiments)
        avg_score = sum(scores) / len(scores) if scores else 5
        
        trends = {
            "total_analyses": len(analyses),
            "sentiment_distribution": dict(sentiment_counts),
            "average_score": avg_score,
            "most_common_sentiment": sentiment_counts.most_common(1)[0][0] if sentiment_counts else "neutral",
            "score_range": {
                "min": min(scores) if scores else 0,
                "max": max(scores) if scores else 10
            }
        }
        
        return trends
    
    def compare_sentiments(self, text1: str, text2: str, detailed: bool = False) -> Optional[Dict[str, Any]]:
        """
        Compare sentiment between two texts.
        
        Args:
            text1: First text to analyze
            text2: Second text to analyze
            detailed: Whether to return detailed analysis
            
        Returns:
            Comparison results or None if failed
        """
        try:
            analysis1 = self.analyze_sentiment(text1, detailed)
            analysis2 = self.analyze_sentiment(text2, detailed)
            
            if not analysis1 or not analysis2:
                return None
            
            comparison = {
                "text1": {
                    "text": text1[:100] + "..." if len(text1) > 100 else text1,
                    "analysis": analysis1
                },
                "text2": {
                    "text": text2[:100] + "..." if len(text2) > 100 else text2,
                    "analysis": analysis2
                },
                "comparison": {
                    "sentiment_difference": analysis1.get('sentiment') != analysis2.get('sentiment'),
                    "score_difference": abs(analysis1.get('score', 5) - analysis2.get('score', 5)),
                    "more_positive": "text1" if analysis1.get('score', 5) > analysis2.get('score', 5) else "text2"
                }
            }
            
            return comparison
            
        except Exception as e:
            logger.error(f"Error comparing sentiments: {e}")
            return None
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get history of all sentiment analyses."""
        return self.analysis_history.copy()
    
    def clear_history(self):
        """Clear the analysis history."""
        self.analysis_history = []
    
    def save_history(self, filename: str = None):
        """Save analysis history to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"sentiment_analysis_history_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.analysis_history, f, indent=2)
        
        logger.info(f"Analysis history saved to {filename}")

def main():
    """Main function to demonstrate the AI Sentiment Analyzer."""
    print("😊 AI Sentiment Analyzer")
    print("=" * 50)
    
    # Initialize the analyzer
    try:
        analyzer = AISentimentAnalyzer()
        print("✅ Sentiment analyzer initialized successfully!")
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("Please set your OpenAI API key as an environment variable: OPENAI_API_KEY")
        return
    
    print("\n🎯 Available commands:")
    print("- 'analyze <text>' - Analyze sentiment")
    print("- 'detailed <text>' - Detailed sentiment analysis")
    print("- 'file <file_path>' - Analyze text file")
    print("- 'compare <text1> | <text2>' - Compare two texts")
    print("- 'trends' - Show sentiment trends")
    print("- 'history' - Show analysis history")
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
            history = analyzer.get_analysis_history()
            if history:
                print(f"\n📋 Analysis History ({len(history)} entries):")
                for i, entry in enumerate(history, 1):
                    sentiment = entry.get('sentiment', 'unknown')
                    score = entry.get('score', 'N/A')
                    print(f"{i}. {sentiment} (score: {score})")
            else:
                print("📋 No analyses yet.")
            continue
        elif user_input.lower() == 'clear':
            analyzer.clear_history()
            print("🗑️ History cleared!")
            continue
        elif user_input.lower() == 'save':
            analyzer.save_history()
            continue
        elif user_input.lower() == 'trends':
            history = analyzer.get_analysis_history()
            if history:
                trends = analyzer.get_sentiment_trends(history)
                print("\n📊 Sentiment Trends:")
                print(f"Total Analyses: {trends['total_analyses']}")
                print(f"Average Score: {trends['average_score']:.2f}")
                print(f"Most Common: {trends['most_common_sentiment']}")
                print(f"Distribution: {trends['sentiment_distribution']}")
            else:
                print("📊 No data for trend analysis.")
            continue
        elif user_input.startswith('analyze '):
            text = user_input[8:].strip()
            if text:
                print(f"\n😊 Analyzing sentiment...")
                result = analyzer.analyze_sentiment(text)
                if result:
                    print(f"✅ Sentiment: {result['sentiment']}")
                    print(f"Score: {result['score']}/10")
                    print(f"Confidence: {result['confidence']}%")
                    if 'summary' in result:
                        print(f"Summary: {result['summary']}")
                else:
                    print("❌ Failed to analyze sentiment")
            else:
                print("❌ Please provide text to analyze")
            continue
        elif user_input.startswith('detailed '):
            text = user_input[9:].strip()
            if text:
                print(f"\n🔍 Detailed sentiment analysis...")
                result = analyzer.analyze_sentiment(text, detailed=True)
                if result:
                    print(f"✅ Sentiment: {result['sentiment']}")
                    print(f"Score: {result['score']}/10")
                    print(f"Confidence: {result['confidence']}%")
                    if 'tone' in result:
                        print(f"Tone: {result['tone']}")
                    if 'emotions' in result:
                        print(f"Emotions: {', '.join(result['emotions'])}")
                    if 'reasoning' in result:
                        print(f"Reasoning: {result['reasoning']}")
                else:
                    print("❌ Failed to analyze sentiment")
            else:
                print("❌ Please provide text to analyze")
            continue
        elif user_input.startswith('file '):
            file_path = user_input[5:].strip()
            if os.path.exists(file_path):
                print(f"\n📄 Analyzing file: {file_path}")
                result = analyzer.analyze_sentiment(file_path)
                if result:
                    print(f"✅ Sentiment: {result['sentiment']}")
                    print(f"Score: {result['score']}/10")
                else:
                    print("❌ Failed to analyze file")
            else:
                print(f"❌ File not found: {file_path}")
            continue
        elif user_input.startswith('compare '):
            parts = user_input[8:].split('|')
            if len(parts) == 2:
                text1 = parts[0].strip()
                text2 = parts[1].strip()
                if text1 and text2:
                    print(f"\n⚖️ Comparing sentiments...")
                    comparison = analyzer.compare_sentiments(text1, text2)
                    if comparison:
                        print("✅ Comparison Results:")
                        print(f"Text 1: {comparison['text1']['analysis']['sentiment']} (score: {comparison['text1']['analysis']['score']})")
                        print(f"Text 2: {comparison['text2']['analysis']['sentiment']} (score: {comparison['text2']['analysis']['score']})")
                        print(f"More positive: {comparison['comparison']['more_positive']}")
                    else:
                        print("❌ Failed to compare sentiments")
                else:
                    print("❌ Please provide two texts separated by |")
            else:
                print("❌ Please provide two texts separated by |")
            continue
        elif not user_input:
            continue
        else:
            print("❌ Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main() 