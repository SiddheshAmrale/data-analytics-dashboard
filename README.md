# AI Projects Collection

A comprehensive collection of 5 powerful AI projects built with OpenAI's GPT models. Each project is designed to be production-ready with full documentation and easy setup.

## 🚀 Projects Overview

### 1. 🤖 AI Chat Assistant
**Location**: `ai_chat_assistant/`

A conversational AI assistant with memory and context management. Features include:
- Intelligent conversations using GPT-3.5-turbo
- Conversation memory and history management
- Customizable system prompts
- Save/load conversation histories
- Session management

**Key Features**:
- 💾 Conversation memory across sessions
- 📝 History export/import capabilities
- ⚙️ Configurable system prompts
- 🔄 Session management tools

### 2. 🎨 AI Image Generator
**Location**: `ai_image_generator/`

A powerful image generation tool using OpenAI's DALL-E model. Features include:
- Text-to-image generation from descriptions
- Image variations and editing
- Multiple sizes and quality options
- Download and save capabilities
- Generation history tracking

**Key Features**:
- 🎨 Text-to-image generation
- 🔄 Image variations
- 📥 Download and save images
- 📋 Generation history
- ⚙️ Multiple quality settings

### 3. 📝 AI Text Summarizer
**Location**: `ai_text_summarizer/`

An intelligent text summarization tool that condenses long texts while preserving key information. Features include:
- Multiple summary styles (concise, detailed, bullet points)
- File support for document summarization
- Batch processing capabilities
- Key points extraction
- Text statistics and analysis

**Key Features**:
- 📊 Multiple summary styles
- 📄 File processing support
- 🔄 Batch processing
- 🔑 Key points extraction
- 📈 Text statistics

### 4. 😊 AI Sentiment Analyzer
**Location**: `ai_sentiment_analyzer/`

An advanced sentiment analysis tool that analyzes emotions, tone, and sentiment in text. Features include:
- Detailed sentiment analysis with scores
- Emotion and tone detection
- Text comparison capabilities
- Trend analysis across multiple texts
- File analysis support

**Key Features**:
- 📊 Detailed sentiment scoring
- 😊 Emotion detection
- ⚖️ Text comparison
- 📈 Trend analysis
- 📄 File analysis

### 5. 💻 AI Code Assistant
**Location**: `ai_code_assistant/`

An intelligent code generation, debugging, and analysis tool. Features include:
- Code generation from natural language
- Automatic debugging and error fixing
- Code explanation and documentation
- Code optimization for various aspects
- Test generation and code conversion

**Key Features**:
- 💻 Code generation
- 🐛 Automatic debugging
- 📖 Code explanation
- ⚡ Code optimization
- 🧪 Test generation
- 🔄 Language conversion

## 🛠️ Quick Start

### Prerequisites
- Python 3.7+
- OpenAI API key

### Installation

1. **Clone or download the projects**
2. **Set up your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file in each project directory:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

3. **Install dependencies for each project**:
   ```bash
   # For each project directory
   cd ai_chat_assistant
   pip install -r requirements.txt
   
   cd ../ai_image_generator
   pip install -r requirements.txt
   
   cd ../ai_text_summarizer
   pip install -r requirements.txt
   
   cd ../ai_sentiment_analyzer
   pip install -r requirements.txt
   
   cd ../ai_code_assistant
   pip install -r requirements.txt
   ```

### Running the Projects

Each project can be run independently:

```bash
# Chat Assistant
cd ai_chat_assistant
python main.py

# Image Generator
cd ai_image_generator
python main.py

# Text Summarizer
cd ai_text_summarizer
python main.py

# Sentiment Analyzer
cd ai_sentiment_analyzer
python main.py

# Code Assistant
cd ai_code_assistant
python main.py
```

## 📚 Documentation

Each project includes comprehensive documentation:

- **Individual README files** in each project directory
- **API reference** for programmatic usage
- **Examples and use cases**
- **Troubleshooting guides**
- **Best practices**

## 🔧 Common Features

All projects share these common features:

- **OpenAI Integration**: Powered by GPT-3.5-turbo and DALL-E
- **Error Handling**: Comprehensive error handling and logging
- **History Management**: Track and save operation history
- **Export Capabilities**: Save results to JSON files
- **Interactive CLI**: User-friendly command-line interfaces
- **Programmatic API**: Use as libraries in your own projects

## 💰 Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **DALL-E**: ~$0.02 per image (standard quality)
- **Typical usage**: Very cost-effective for most use cases
- **Monitor usage**: Check OpenAI dashboard for usage tracking

## 🎯 Use Cases

### Business Applications
- **Customer Support**: AI Chat Assistant for automated responses
- **Content Creation**: AI Image Generator for marketing materials
- **Document Analysis**: AI Text Summarizer for reports and documents
- **Customer Feedback**: AI Sentiment Analyzer for reviews and surveys
- **Development**: AI Code Assistant for rapid prototyping

### Personal Applications
- **Learning**: All tools can be used for educational purposes
- **Content Creation**: Generate images and summarize content
- **Code Learning**: Understand and improve code with explanations
- **Writing**: Analyze sentiment and summarize text

### Research Applications
- **Data Analysis**: Sentiment analysis of large text datasets
- **Content Analysis**: Summarize research papers and documents
- **Code Analysis**: Analyze code complexity and quality
- **Image Research**: Generate images for research purposes

## 🚀 Getting Started Examples

### Chat Assistant
```python
from ai_chat_assistant.main import AIChatAssistant

assistant = AIChatAssistant()
response = assistant.get_chat_response("Hello, how are you?")
print(response)
```

### Image Generator
```python
from ai_image_generator.main import AIImageGenerator

generator = AIImageGenerator()
url = generator.generate_image("A beautiful sunset over mountains")
print(f"Generated: {url}")
```

### Text Summarizer
```python
from ai_text_summarizer.main import AITextSummarizer

summarizer = AITextSummarizer()
summary = summarizer.summarize_text("Your long text here...")
print(summary)
```

### Sentiment Analyzer
```python
from ai_sentiment_analyzer.main import AISentimentAnalyzer

analyzer = AISentimentAnalyzer()
result = analyzer.analyze_sentiment("I love this product!")
print(f"Sentiment: {result['sentiment']}")
```

### Code Assistant
```python
from ai_code_assistant.main import AICodeAssistant

assistant = AICodeAssistant()
code = assistant.generate_code("Create a function to calculate fibonacci numbers")
print(code)
```

## 🤝 Contributing

Feel free to contribute to any of these projects by:
- Adding new features
- Improving error handling
- Enhancing documentation
- Reporting bugs
- Suggesting improvements

## 📄 License

All projects are open source and available under the MIT License.

## 🔗 Links

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [OpenAI Pricing](https://openai.com/pricing)
- [Python Documentation](https://docs.python.org/)

---

**Note**: These projects require an OpenAI API key to function. Make sure to set up your API key before running any of the projects. 