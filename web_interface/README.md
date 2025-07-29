# AI Projects Web Interface

A modern, responsive web application that provides a unified interface for all AI projects including chat assistant, image generation, text summarization, sentiment analysis, and code assistance.

## 🚀 Features

### Unified Dashboard
- **Single Interface**: Access all AI tools from one web application
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live chat and real-time responses
- **Session Management**: Persistent user sessions and history

### AI Tools Integration
- **🤖 Chat Assistant**: Intelligent conversations with memory
- **🎨 Image Generator**: Create images from text descriptions
- **📝 Text Summarizer**: Condense long texts into summaries
- **😊 Sentiment Analyzer**: Analyze emotions and tone in text
- **💻 Code Assistant**: Generate, debug, and explain code

### User Experience
- **Modern UI**: Clean, intuitive interface design
- **Interactive Elements**: Real-time feedback and animations
- **File Upload**: Support for file-based operations
- **Export Options**: Download results and reports
- **History Tracking**: Save and review past interactions

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- OpenAI API key
- Flask and related packages (see requirements.txt)

### Setup

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   export SECRET_KEY="your-secret-key-here"
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   SECRET_KEY=your-secret-key-here
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the web interface**:
   Open your browser and go to `http://localhost:5000`

## 📱 Usage

### Getting Started

1. **Home Page**: Overview of all available AI tools
2. **Navigation**: Use the menu to switch between different AI tools
3. **API Integration**: All AI projects are automatically integrated
4. **Real-time Chat**: Use WebSocket for live chat functionality

### Available Pages

#### Chat Assistant (`/chat`)
- Interactive conversation interface
- Message history and context
- System prompt customization
- Export conversation history

#### Image Generator (`/image`)
- Text-to-image generation
- Multiple size and quality options
- Download generated images
- Generation history tracking

#### Text Summarizer (`/summarizer`)
- Multiple summary styles
- File upload support
- Batch processing
- Key points extraction

#### Sentiment Analyzer (`/sentiment`)
- Detailed sentiment analysis
- Emotion detection
- Text comparison
- File analysis support

#### Code Assistant (`/code`)
- Code generation from descriptions
- Debug and fix code issues
- Code explanation and documentation
- Language conversion

## 🔧 API Endpoints

### Chat Assistant
- `POST /api/chat`: Send message and get response
- `GET /api/chat/history`: Get conversation history
- `POST /api/chat/clear`: Clear conversation history

### Image Generator
- `POST /api/generate_image`: Generate image from text
- `GET /api/images/history`: Get generation history
- `POST /api/images/download`: Download generated image

### Text Summarizer
- `POST /api/summarize`: Summarize text or file
- `POST /api/summarize/batch`: Batch summarization
- `GET /api/summarizer/history`: Get summarization history

### Sentiment Analyzer
- `POST /api/analyze_sentiment`: Analyze text sentiment
- `POST /api/analyze_sentiment/batch`: Batch sentiment analysis
- `GET /api/sentiment/history`: Get analysis history

### Code Assistant
- `POST /api/generate_code`: Generate code from description
- `POST /api/debug_code`: Debug and fix code
- `POST /api/explain_code`: Explain code functionality
- `POST /api/optimize_code`: Optimize code performance

## 🎨 UI Components

### Responsive Design
- **Mobile-first**: Optimized for mobile devices
- **Flexible Layout**: Adapts to different screen sizes
- **Touch-friendly**: Large buttons and touch targets
- **Fast Loading**: Optimized assets and caching

### Interactive Elements
- **Real-time Chat**: WebSocket-based live messaging
- **File Upload**: Drag-and-drop file upload
- **Progress Indicators**: Loading states and progress bars
- **Notifications**: Success and error messages

### Visual Design
- **Modern Theme**: Clean, professional appearance
- **Consistent Styling**: Unified design language
- **Accessibility**: WCAG compliant design
- **Dark/Light Mode**: Theme switching capability

## 🔒 Security Features

### Authentication
- Session-based authentication
- Secure cookie handling
- CSRF protection
- Input validation and sanitization

### API Security
- Rate limiting
- Request validation
- Error handling
- Secure API key management

### Data Protection
- Secure file uploads
- Input sanitization
- XSS protection
- SQL injection prevention

## 🚀 Deployment

### Local Development
```bash
# Run in development mode
python app.py

# Run with debug mode
export FLASK_ENV=development
python app.py
```

### Production Deployment
```bash
# Using Gunicorn
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker
docker build -t ai-web-interface .
docker run -p 5000:5000 ai-web-interface
```

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-secret-key

# Optional
FLASK_ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=5000
```

## 📊 Monitoring and Logging

### Application Logs
- Request/response logging
- Error tracking and reporting
- Performance monitoring
- User activity analytics

### Health Checks
- `GET /health`: Application health status
- Database connectivity checks
- API service availability
- System resource monitoring

## 🔧 Configuration

### Flask Configuration
```python
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    DEBUG=os.getenv('DEBUG', 'False').lower() == 'true',
    HOST=os.getenv('HOST', '127.0.0.1'),
    PORT=int(os.getenv('PORT', 5000))
)
```

### AI Assistant Settings
```python
# Customize AI behavior
ai_assistants['chat'].max_history_length = 20
ai_assistants['image'].default_size = "1024x1024"
ai_assistants['summarizer'].default_style = "concise"
```

## 🧪 Testing

### Unit Tests
```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest --cov=app tests/
```

### Integration Tests
```bash
# Test API endpoints
python -m pytest tests/test_api.py

# Test WebSocket functionality
python -m pytest tests/test_socketio.py
```

## 🚀 Performance Optimization

### Caching
- Redis for session storage
- File upload caching
- API response caching
- Static asset caching

### Database
- SQLite for development
- PostgreSQL for production
- Connection pooling
- Query optimization

### Static Assets
- CDN for static files
- Asset compression
- Image optimization
- Lazy loading

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Check environment variable setup
- Verify .env file format
- Ensure API key is valid

**"WebSocket connection failed"**
- Check firewall settings
- Verify WebSocket support
- Check browser compatibility

**"File upload errors"**
- Check file size limits
- Verify file type restrictions
- Ensure upload directory permissions

**"Memory issues"**
- Monitor memory usage
- Implement request limits
- Use streaming for large files

## 📚 Dependencies

### Core Dependencies
- `flask`: Web framework
- `flask-socketio`: WebSocket support
- `python-dotenv`: Environment management
- `openai`: OpenAI API integration

### UI Dependencies
- `bootstrap`: CSS framework
- `jquery`: JavaScript library
- `socket.io`: WebSocket client
- `axios`: HTTP client

### Development Dependencies
- `pytest`: Testing framework
- `pytest-cov`: Coverage reporting
- `black`: Code formatting
- `flake8`: Linting

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd web_interface

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py
```

### Areas for Contribution
- UI/UX improvements
- New AI tool integrations
- Performance optimizations
- Security enhancements
- Documentation updates

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-SocketIO Documentation](https://flask-socketio.readthedocs.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review the API documentation
- Open an issue on GitHub
- Consult the Flask documentation

---

**Note**: This web interface requires an OpenAI API key to function. Make sure to set up your API key before running the application. 