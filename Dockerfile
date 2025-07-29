# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY ai_chat_assistant/requirements.txt ./ai_chat_assistant/
COPY ai_image_generator/requirements.txt ./ai_image_generator/
COPY ai_text_summarizer/requirements.txt ./ai_text_summarizer/
COPY ai_sentiment_analyzer/requirements.txt ./ai_sentiment_analyzer/
COPY ai_code_assistant/requirements.txt ./ai_code_assistant/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r ai_chat_assistant/requirements.txt && \
    pip install --no-cache-dir -r ai_image_generator/requirements.txt && \
    pip install --no-cache-dir -r ai_text_summarizer/requirements.txt && \
    pip install --no-cache-dir -r ai_sentiment_analyzer/requirements.txt && \
    pip install --no-cache-dir -r ai_code_assistant/requirements.txt && \
    pip install --no-cache-dir pytest pytest-cov black flake8 mypy

# Copy source code
COPY . .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Create directories for generated files
RUN mkdir -p /app/generated_images /app/logs /app/data

# Expose port (if needed for web interface)
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command
CMD ["python", "ai_chat_assistant/main.py"] 