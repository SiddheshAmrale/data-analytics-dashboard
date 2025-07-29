# Deployment Guide

This guide covers deployment options for the AI Projects Collection, from local development to production environments.

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/ai-projects-collection.git
   cd ai-projects-collection
   ```

2. **Set up environment**:
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r ai_chat_assistant/requirements.txt
   pip install -r ai_image_generator/requirements.txt
   pip install -r ai_text_summarizer/requirements.txt
   pip install -r ai_sentiment_analyzer/requirements.txt
   pip install -r ai_code_assistant/requirements.txt
   ```

3. **Set API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

4. **Run any project**:
   ```bash
   python ai_chat_assistant/main.py
   ```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

1. **Set environment variables**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

2. **Build and run**:
   ```bash
   # Production
   docker-compose up -d
   
   # Development with hot reload
   docker-compose --profile dev up -d
   
   # Run tests
   docker-compose --profile test up
   
   # Run linting
   docker-compose --profile lint up
   
   # Run security scan
   docker-compose --profile security up
   ```

3. **Access the application**:
   - Production: http://localhost:8000
   - Development: http://localhost:8001

### Using Docker directly

1. **Build the image**:
   ```bash
   docker build -t ai-projects-collection .
   ```

2. **Run the container**:
   ```bash
   docker run -d \
     --name ai-projects \
     -p 8000:8000 \
     -e OPENAI_API_KEY="your-api-key" \
     -v $(pwd)/data:/app/data \
     -v $(pwd)/logs:/app/logs \
     -v $(pwd)/generated_images:/app/generated_images \
     ai-projects-collection
   ```

## ☁️ Cloud Deployment

### AWS Deployment

#### Using AWS ECS

1. **Create ECR repository**:
   ```bash
   aws ecr create-repository --repository-name ai-projects-collection
   ```

2. **Build and push image**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   docker build -t ai-projects-collection .
   docker tag ai-projects-collection:latest $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-projects-collection:latest
   docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-projects-collection:latest
   ```

3. **Deploy to ECS**:
   ```bash
   aws ecs create-service \
     --cluster your-cluster \
     --service-name ai-projects \
     --task-definition ai-projects-task \
     --desired-count 1
   ```

#### Using AWS Lambda

1. **Create deployment package**:
   ```bash
   pip install -r requirements.txt -t package/
   cp *.py package/
   cd package && zip -r ../deployment.zip .
   ```

2. **Deploy to Lambda**:
   ```bash
   aws lambda create-function \
     --function-name ai-projects \
     --runtime python3.11 \
     --role arn:aws:iam::ACCOUNT:role/lambda-role \
     --handler main.lambda_handler \
     --zip-file fileb://deployment.zip
   ```

### Google Cloud Platform

#### Using Google Cloud Run

1. **Build and push to Container Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/ai-projects-collection
   ```

2. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy ai-projects \
     --image gcr.io/PROJECT_ID/ai-projects-collection \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Azure Deployment

#### Using Azure Container Instances

1. **Build and push to Azure Container Registry**:
   ```bash
   az acr build --registry your-registry --image ai-projects-collection .
   ```

2. **Deploy to Container Instances**:
   ```bash
   az container create \
     --resource-group your-rg \
     --name ai-projects \
     --image your-registry.azurecr.io/ai-projects-collection:latest \
     --dns-name-label ai-projects \
     --ports 8000
   ```

## 🔧 Environment Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your-openai-api-key

# Application Configuration
ENVIRONMENT=production
LOG_LEVEL=INFO
DEBUG=false

# Database Configuration (if using)
DATABASE_URL=postgresql://user:password@localhost/dbname

# Redis Configuration (if using)
REDIS_URL=redis://localhost:6379

# Monitoring Configuration
SENTRY_DSN=your-sentry-dsn
```

### Configuration Files

Create `config.py` for application configuration:

```python
import os
from typing import Optional

class Config:
    """Application configuration."""
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv('OPENAI_API_KEY', '')
    
    # Application
    ENVIRONMENT: str = os.getenv('ENVIRONMENT', 'development')
    DEBUG: bool = os.getenv('DEBUG', 'false').lower() == 'true'
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # Paths
    DATA_DIR: str = os.getenv('DATA_DIR', './data')
    LOGS_DIR: str = os.getenv('LOGS_DIR', './logs')
    GENERATED_IMAGES_DIR: str = os.getenv('GENERATED_IMAGES_DIR', './generated_images')
    
    # Security
    SECRET_KEY: str = os.getenv('SECRET_KEY', 'your-secret-key-here')
    
    @classmethod
    def validate(cls) -> None:
        """Validate required configuration."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
```

## 📊 Monitoring and Logging

### Logging Configuration

Create `logging_config.py`:

```python
import logging
import logging.handlers
import os
from datetime import datetime

def setup_logging(log_level: str = "INFO", log_dir: str = "./logs"):
    """Set up application logging."""
    
    # Create logs directory
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.handlers.RotatingFileHandler(
                os.path.join(log_dir, 'app.log'),
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            )
        ]
    )
    
    # Set specific loggers
    logging.getLogger('openai').setLevel(logging.WARNING)
    logging.getLogger('requests').setLevel(logging.WARNING)
```

### Health Checks

Create `health_check.py`:

```python
import requests
import time
from typing import Dict, Any

def health_check() -> Dict[str, Any]:
    """Perform health check of the application."""
    
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {}
    }
    
    # Check OpenAI API connectivity
    try:
        # Add your health check logic here
        health_status["checks"]["openai_api"] = "healthy"
    except Exception as e:
        health_status["checks"]["openai_api"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check disk space
    try:
        import shutil
        total, used, free = shutil.disk_usage(".")
        health_status["checks"]["disk_space"] = {
            "total": total,
            "used": used,
            "free": free,
            "status": "healthy" if free > 1024*1024*1024 else "low_space"
        }
    except Exception as e:
        health_status["checks"]["disk_space"] = f"error: {str(e)}"
    
    return health_status
```

## 🔒 Security Considerations

### API Key Management

1. **Never commit API keys**:
   ```bash
   # Add to .gitignore
   echo "*.key" >> .gitignore
   echo "secrets/" >> .gitignore
   ```

2. **Use environment variables**:
   ```bash
   export OPENAI_API_KEY="your-key"
   ```

3. **Use secret management services**:
   - AWS Secrets Manager
   - Google Secret Manager
   - Azure Key Vault

### Security Best Practices

1. **Run as non-root user** (already configured in Dockerfile)
2. **Use HTTPS in production**
3. **Implement rate limiting**
4. **Add input validation**
5. **Use security scanning tools**

## 📈 Performance Optimization

### Caching Strategy

```python
import redis
import json
from functools import wraps

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def cache_result(expire_time: int = 3600):
    """Cache function results."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"
            
            # Try to get from cache
            cached_result = redis_client.get(cache_key)
            if cached_result:
                return json.loads(cached_result)
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            redis_client.setex(cache_key, expire_time, json.dumps(result))
            
            return result
        return wrapper
    return decorator
```

### Load Balancing

For high-traffic deployments, use a load balancer:

```yaml
# docker-compose.yml with load balancer
version: '3.8'

services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - ai-projects-1
      - ai-projects-2
      - ai-projects-3

  ai-projects-1:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}

  ai-projects-2:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}

  ai-projects-3:
    build: .
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
```

## 🚨 Troubleshooting

### Common Issues

1. **API Key Issues**:
   ```bash
   # Check if API key is set
   echo $OPENAI_API_KEY
   
   # Test API connectivity
   curl -H "Authorization: Bearer $OPENAI_API_KEY" \
     https://api.openai.com/v1/models
   ```

2. **Docker Issues**:
   ```bash
   # Check container logs
   docker logs ai-projects-collection
   
   # Check container status
   docker ps -a
   
   # Restart container
   docker restart ai-projects-collection
   ```

3. **Performance Issues**:
   ```bash
   # Check resource usage
   docker stats ai-projects-collection
   
   # Check disk space
   df -h
   
   # Check memory usage
   free -h
   ```

### Debug Mode

Enable debug mode for troubleshooting:

```bash
export DEBUG=true
export LOG_LEVEL=DEBUG
docker-compose up
```

## 📋 Deployment Checklist

- [ ] Environment variables configured
- [ ] API keys secured
- [ ] SSL certificates installed (production)
- [ ] Monitoring configured
- [ ] Logging configured
- [ ] Health checks implemented
- [ ] Backup strategy in place
- [ ] Security scanning completed
- [ ] Performance testing done
- [ ] Documentation updated

## 🔄 Continuous Deployment

### GitHub Actions Workflow

The repository includes a comprehensive CI/CD pipeline that:

1. **Runs tests** on multiple Python versions
2. **Performs security scans**
3. **Builds Docker images**
4. **Deploys to staging/production**

### Manual Deployment

```bash
# Build and deploy
docker-compose build
docker-compose up -d

# Check deployment status
docker-compose ps
docker-compose logs -f
```

---

For more information, see the [Contributing Guide](CONTRIBUTING.md) and [README](README.md). 