# AI Sentiment Analyzer

An advanced sentiment analysis tool powered by OpenAI's GPT models that can analyze emotions, tone, and sentiment in text with high accuracy and detailed insights.

## Features

- 😊 **Intelligent Sentiment Analysis**: AI-powered sentiment detection using GPT-3.5-turbo
- 📊 **Detailed Analysis**: Comprehensive sentiment analysis with scores, confidence, and emotions
- 🔄 **Batch Processing**: Analyze multiple texts efficiently
- 📄 **File Support**: Analyze sentiment in text files
- ⚖️ **Text Comparison**: Compare sentiment between different texts
- 📈 **Trend Analysis**: Track sentiment trends across multiple analyses
- 📋 **History Management**: Keep track of all sentiment analyses
- 💾 **Export Capabilities**: Save analysis results and trends

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
from main import AISentimentAnalyzer

# Initialize the analyzer
analyzer = AISentimentAnalyzer(api_key="your-api-key")

# Basic sentiment analysis
result = analyzer.analyze_sentiment("I love this product! It's amazing!")
print(f"Sentiment: {result['sentiment']}")
print(f"Score: {result['score']}/10")

# Detailed analysis
detailed_result = analyzer.analyze_sentiment("I'm so excited about this!", detailed=True)
print(f"Tone: {detailed_result['tone']}")
print(f"Emotions: {detailed_result['emotions']}")
```

### Advanced Features

#### Batch Analysis
```python
# Analyze multiple texts
texts = [
    "I love this movie!",
    "This is terrible.",
    "It's okay, nothing special."
]
results = analyzer.analyze_batch(texts)
```

#### Text Comparison
```python
# Compare sentiment between two texts
comparison = analyzer.compare_sentiments(
    "I love this product!",
    "I hate this product!"
)
print(f"More positive: {comparison['comparison']['more_positive']}")
```

#### File Analysis
```python
# Analyze sentiment in a text file
result = analyzer.analyze_file("customer_reviews.txt", detailed=True)
```

#### Trend Analysis
```python
# Get trends from multiple analyses
history = analyzer.get_analysis_history()
trends = analyzer.get_sentiment_trends(history)
print(f"Average score: {trends['average_score']}")
```

## API Reference

### AISentimentAnalyzer Class

#### Constructor
```python
AISentimentAnalyzer(api_key: str = None)
```
- `api_key`: OpenAI API key (optional if set as environment variable)

#### Methods

- `analyze_sentiment(text: str, detailed: bool = False) -> Optional[Dict[str, Any]]`
  - Analyze sentiment of text
  - `text`: Text to analyze
  - `detailed`: Whether to return detailed analysis

- `analyze_batch(texts: List[str], detailed: bool = False) -> List[Optional[Dict[str, Any]]]`
  - Analyze sentiment of multiple texts
  - `texts`: List of texts to analyze
  - `detailed`: Whether to return detailed analysis

- `analyze_file(file_path: str, detailed: bool = False) -> Optional[Dict[str, Any]]`
  - Analyze sentiment of text file
  - `file_path`: Path to text file
  - `detailed`: Whether to return detailed analysis

- `compare_sentiments(text1: str, text2: str, detailed: bool = False) -> Optional[Dict[str, Any]]`
  - Compare sentiment between two texts
  - `text1`: First text to analyze
  - `text2`: Second text to analyze
  - `detailed`: Whether to return detailed analysis

- `get_sentiment_trends(analyses: List[Dict[str, Any]]) -> Dict[str, Any]`
  - Analyze trends from multiple sentiment analyses
  - `analyses`: List of sentiment analysis results

- `get_analysis_history() -> List[Dict[str, Any]]`
  - Get history of all sentiment analyses

- `clear_history()`
  - Clear analysis history

- `save_history(filename: str = None)`
  - Save analysis history to JSON file

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key

### Analysis Types

#### Basic Analysis
Returns:
- `sentiment`: positive/negative/neutral
- `score`: 0-10 sentiment score
- `confidence`: 0-100% confidence level
- `summary`: Brief explanation

#### Detailed Analysis
Returns all basic fields plus:
- `emotional_indicators`: List of emotional keywords
- `tone`: Overall tone description
- `emotions`: Specific emotions detected
- `reasoning`: Detailed explanation

## Examples

### Example 1: Basic Sentiment Analysis
```
Enter command: analyze I absolutely love this new phone! The camera quality is amazing and the battery life is incredible.
😊 Analyzing sentiment...
✅ Sentiment: positive
Score: 9.2/10
Confidence: 92%
Summary: The text expresses strong positive emotions about a new phone, highlighting excellent features.
```

### Example 2: Detailed Analysis
```
Enter command: detailed I'm really disappointed with the service. The customer support was unhelpful and the product quality is poor.
🔍 Detailed sentiment analysis...
✅ Sentiment: negative
Score: 2.1/10
Confidence: 88%
Tone: frustrated
Emotions: ['disappointment', 'frustration', 'dissatisfaction']
Reasoning: The text clearly expresses negative emotions through words like "disappointed", "unhelpful", and "poor".
```

### Example 3: Text Comparison
```
Enter command: compare I love this restaurant! | I hate this restaurant!
⚖️ Comparing sentiments...
✅ Comparison Results:
Text 1: positive (score: 8.5)
Text 2: negative (score: 1.8)
More positive: text1
```

### Example 4: Trend Analysis
```
Enter command: trends
📊 Sentiment Trends:
Total Analyses: 15
Average Score: 6.8
Most Common: positive
Distribution: {'positive': 10, 'neutral': 3, 'negative': 2}
```

## Analysis Results

### Sentiment Categories
- **Positive**: Expresses happiness, satisfaction, excitement
- **Negative**: Expresses anger, sadness, disappointment, frustration
- **Neutral**: Balanced or factual statements

### Score Interpretation
- **0-3**: Very negative
- **3-5**: Slightly negative to neutral
- **5-7**: Neutral to slightly positive
- **7-10**: Positive to very positive

### Confidence Levels
- **90-100%**: High confidence in analysis
- **70-89%**: Good confidence
- **50-69%**: Moderate confidence
- **Below 50%**: Low confidence

## Use Cases

### Business Applications
- **Customer Feedback Analysis**: Analyze reviews and feedback
- **Social Media Monitoring**: Track brand sentiment
- **Market Research**: Understand customer opinions
- **Product Development**: Gauge feature reception

### Research Applications
- **Survey Analysis**: Analyze open-ended responses
- **Content Analysis**: Study text sentiment patterns
- **Psychological Research**: Analyze emotional expression
- **Linguistic Studies**: Study sentiment in different contexts

### Personal Applications
- **Journal Analysis**: Track personal emotional patterns
- **Communication Analysis**: Understand message tone
- **Writing Improvement**: Analyze writing sentiment
- **Social Media Analysis**: Understand online sentiment

## Best Practices

### Writing Effective Prompts
1. **Be Specific**: Provide context when needed
2. **Consider Length**: Very short texts may be harder to analyze
3. **Check Context**: Ensure the AI understands the domain
4. **Review Results**: Always verify analysis accuracy

### Interpreting Results
1. **Consider Context**: Sentiment can vary by domain
2. **Check Confidence**: Higher confidence means more reliable results
3. **Look at Details**: Detailed analysis provides more insights
4. **Compare Trends**: Look at patterns over time

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is set correctly
   - Check that the key has sufficient credits

2. **Poor Analysis Quality**
   - Try detailed analysis for more insights
   - Provide more context in the text
   - Check if the text is too short or ambiguous

3. **JSON Parsing Errors**
   - The system has fallback mechanisms
   - Basic keyword analysis will be used if JSON parsing fails

4. **File Reading Errors**
   - Ensure file exists and is readable
   - Check file encoding (UTF-8 recommended)

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical Analysis**: 100-300 tokens
- **Cost per Analysis**: ~$0.0002-0.0006
- **Batch Processing**: More cost-effective for multiple analyses
- Monitor usage in OpenAI dashboard

## Contributing

Feel free to contribute to this project by:
- Adding new analysis features
- Improving sentiment detection accuracy
- Enhancing trend analysis capabilities
- Adding support for more languages
- Reporting bugs and issues

## License

This project is open source and available under the MIT License. 