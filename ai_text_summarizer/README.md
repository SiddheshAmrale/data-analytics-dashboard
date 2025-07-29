# AI Text Summarizer

An intelligent text summarization tool powered by OpenAI's GPT models that can condense long texts into concise summaries while preserving key information.

## Features

- 📝 **Smart Summarization**: AI-powered text summarization using GPT-3.5-turbo
- 🎯 **Multiple Styles**: Concise, detailed, bullet points, and key points summaries
- 📄 **File Support**: Summarize text files directly
- 🔄 **Batch Processing**: Process multiple texts at once
- 📊 **Text Statistics**: Analyze text characteristics
- 🔑 **Key Points Extraction**: Extract main points from text
- 📋 **History Management**: Track all summarization activities
- 💾 **Export Capabilities**: Save summarization history

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
from main import AITextSummarizer

# Initialize the summarizer
summarizer = AITextSummarizer(api_key="your-api-key")

# Summarize text
text = "Your long text here..."
summary = summarizer.summarize_text(text)
print(summary)

# Extract key points
points = summarizer.extract_key_points(text, num_points=5)
print(points)
```

### Advanced Features

#### Different Summary Styles
```python
# Concise summary
summary = summarizer.summarize_text(text, style="concise", max_length=100)

# Detailed summary
summary = summarizer.summarize_text(text, style="detailed", max_length=200)

# Bullet points
summary = summarizer.summarize_text(text, style="bullet_points")

# Key points
summary = summarizer.summarize_text(text, style="key_points")
```

#### File Summarization
```python
# Summarize a text file
summary = summarizer.summarize_file("document.txt", max_length=150)
```

#### Batch Processing
```python
# Summarize multiple texts
texts = ["Text 1...", "Text 2...", "Text 3..."]
summaries = summarizer.batch_summarize(texts, max_length=100)
```

#### Text Statistics
```python
# Get text statistics
stats = summarizer.get_summary_statistics(text)
print(f"Words: {stats['word_count']}")
print(f"Sentences: {stats['sentence_count']}")
```

## API Reference

### AITextSummarizer Class

#### Constructor
```python
AITextSummarizer(api_key: str = None)
```
- `api_key`: OpenAI API key (optional if set as environment variable)

#### Methods

- `summarize_text(text: str, max_length: int = 150, style: str = "concise") -> Optional[str]`
  - Summarize text using AI
  - `text`: Text to summarize
  - `max_length`: Maximum length of summary
  - `style`: Summary style (concise, detailed, bullet_points, key_points)

- `summarize_file(file_path: str, max_length: int = 150, style: str = "concise") -> Optional[str]`
  - Summarize text from file
  - `file_path`: Path to text file
  - `max_length`: Maximum length of summary
  - `style`: Summary style

- `batch_summarize(texts: List[str], max_length: int = 150, style: str = "concise") -> List[Optional[str]]`
  - Summarize multiple texts
  - `texts`: List of texts to summarize
  - `max_length`: Maximum length of each summary
  - `style`: Summary style

- `extract_key_points(text: str, num_points: int = 5) -> Optional[List[str]]`
  - Extract key points from text
  - `text`: Text to analyze
  - `num_points`: Number of key points to extract

- `get_summary_statistics(text: str) -> Optional[Dict[str, Any]]`
  - Get text statistics
  - `text`: Text to analyze

- `get_summarization_history() -> List[Dict[str, Any]]`
  - Get history of all summarizations

- `clear_history()`
  - Clear summarization history

- `save_history(filename: str = None)`
  - Save summarization history to JSON file

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key

### Summary Styles

1. **concise**: Short, to-the-point summary
2. **detailed**: Comprehensive summary with more details
3. **bullet_points**: Summary formatted as bullet points
4. **key_points**: Extraction of main points only

### Parameters

- **max_length**: Maximum number of words in summary (default: 150)
- **style**: Summary style (default: "concise")
- **num_points**: Number of key points to extract (default: 5)

## Examples

### Example 1: Basic Summarization
```
Enter command: summarize Artificial intelligence has revolutionized many industries, from healthcare to finance. Machine learning algorithms can now diagnose diseases, predict market trends, and automate complex tasks. The technology continues to advance rapidly, with new breakthroughs in natural language processing and computer vision.
📝 Summarizing text...
✅ Summary: AI has transformed industries like healthcare and finance through machine learning algorithms that can diagnose diseases, predict trends, and automate tasks. The field continues advancing with breakthroughs in NLP and computer vision.
```

### Example 2: Key Points Extraction
```
Enter command: keypoints Climate change is one of the most pressing issues of our time. Rising global temperatures are causing extreme weather events, melting polar ice caps, and threatening biodiversity. Scientists warn that immediate action is needed to reduce greenhouse gas emissions and transition to renewable energy sources.
🔑 Extracting key points...
✅ Key Points:
1. Climate change is a critical global issue
2. Rising temperatures cause extreme weather and ice melt
3. Biodiversity is threatened by climate change
4. Immediate action is required
5. Transition to renewable energy is necessary
```

### Example 3: File Summarization
```
Enter command: file long_document.txt
📄 Summarizing file: long_document.txt
✅ Summary: The document discusses the history of renewable energy technologies...
```

### Example 4: Text Statistics
```
Enter command: stats This is a sample text for analysis. It contains multiple sentences and various words.
📊 Analyzing text statistics...
✅ Text Statistics:
  Character Count: 89.00
  Word Count: 15.00
  Sentence Count: 2.00
  Average Words Per Sentence: 7.50
  Average Word Length: 4.47
```

## Best Practices

### Writing Effective Summaries

1. **Clear Prompts**: Provide context when needed
2. **Appropriate Length**: Choose max_length based on original text size
3. **Style Selection**: Use appropriate style for your use case
4. **Quality Check**: Review summaries for accuracy

### Use Cases

- **Academic Papers**: Extract key findings and conclusions
- **News Articles**: Get quick overviews of current events
- **Business Documents**: Summarize reports and proposals
- **Research Papers**: Extract main points and methodology
- **Long-form Content**: Condense articles and books

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is set correctly
   - Check that the key has sufficient credits

2. **Text Too Long**
   - The API has token limits
   - Consider breaking very long texts into chunks

3. **Poor Quality Summaries**
   - Try different styles or max_length values
   - Provide more context in the original text

4. **File Reading Errors**
   - Ensure file exists and is readable
   - Check file encoding (UTF-8 recommended)

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical Summary**: 100-200 tokens
- **Cost per Summary**: ~$0.0002-0.0004
- Monitor usage in OpenAI dashboard

## Contributing

Feel free to contribute to this project by:
- Adding new summarization styles
- Improving text analysis features
- Enhancing error handling
- Adding support for more file formats
- Reporting bugs

## License

This project is open source and available under the MIT License. 