# 🤖 Machine Learning API

A RESTful API for machine learning models with Python Flask backend, featuring model training and prediction endpoints. Supports multiple ML frameworks and provides a unified interface for model deployment.

## ✨ Features

- **Multiple ML Frameworks**: Support for scikit-learn, TensorFlow, PyTorch, XGBoost, LightGBM
- **Model Training**: Train models via API endpoints
- **Prediction Endpoints**: Make predictions with trained models
- **Model Management**: Version control and model registry
- **Batch Processing**: Handle large datasets efficiently
- **Real-time Predictions**: Low-latency inference
- **Model Monitoring**: Track model performance and drift
- **Authentication**: Secure API access with JWT
- **Documentation**: Auto-generated API docs
- **Docker Support**: Containerized deployment

## 🛠️ Tech Stack

### Backend
- **Flask** - Web framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Redis** - Caching and task queue
- **Celery** - Background task processing
- **JWT** - Authentication

### Machine Learning
- **scikit-learn** - Traditional ML algorithms
- **TensorFlow** - Deep learning framework
- **PyTorch** - Deep learning framework
- **XGBoost** - Gradient boosting
- **LightGBM** - Light gradient boosting
- **NumPy** - Numerical computing
- **Pandas** - Data manipulation

### Development & Testing
- **Pytest** - Testing framework
- **Black** - Code formatting
- **Flake8** - Code linting
- **Docker** - Containerization

## 🚀 Installation

### Prerequisites
- Python 3.8+
- PostgreSQL
- Redis
- Docker (optional)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/siddheshamrale/machine-learning-api.git
   cd machine-learning-api
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment variables**
   Create `.env` file:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   DATABASE_URL=postgresql://username:password@localhost:5432/ml_api
   REDIS_URL=redis://localhost:6379
   JWT_SECRET_KEY=your_jwt_secret
   MODEL_STORAGE_PATH=/path/to/models
   ```

5. **Database setup**
   ```bash
   # Create PostgreSQL database
   createdb ml_api
   
   # Run migrations
   flask db upgrade
   ```

6. **Start the API**
   ```bash
   flask run
   ```

## 📁 Project Structure

```
machine-learning-api/
├── app/
│   ├── __init__.py        # Flask app initialization
│   ├── models/            # Database models
│   ├── routes/            # API routes
│   ├── services/          # Business logic
│   │   ├── ml_models/    # ML model implementations
│   │   ├── training/      # Model training services
│   │   └── prediction/    # Prediction services
│   ├── utils/             # Utility functions
│   └── schemas/           # Request/response schemas
├── tests/                 # Test files
├── docs/                  # Documentation
├── models/                # Trained model storage
├── data/                  # Sample datasets
└── docker/                # Docker configuration
```

## 🔧 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Refresh token
- `POST /api/auth/logout` - User logout

### Model Management
- `GET /api/models` - List all models
- `POST /api/models` - Create new model
- `GET /api/models/:id` - Get model details
- `PUT /api/models/:id` - Update model
- `DELETE /api/models/:id` - Delete model

### Model Training
- `POST /api/models/:id/train` - Train model
- `GET /api/models/:id/training-status` - Get training status
- `POST /api/models/:id/retrain` - Retrain model

### Predictions
- `POST /api/models/:id/predict` - Single prediction
- `POST /api/models/:id/predict-batch` - Batch predictions
- `GET /api/models/:id/predictions` - Get prediction history

### Model Performance
- `GET /api/models/:id/metrics` - Get model metrics
- `POST /api/models/:id/evaluate` - Evaluate model
- `GET /api/models/:id/performance` - Performance history

## 🤖 Supported ML Frameworks

### scikit-learn
- **Classification**: Random Forest, SVM, Logistic Regression
- **Regression**: Linear Regression, Ridge, Lasso
- **Clustering**: K-means, DBSCAN, Hierarchical
- **Dimensionality Reduction**: PCA, LDA, t-SNE

### TensorFlow
- **Neural Networks**: Dense, CNN, RNN, LSTM
- **Transfer Learning**: Pre-trained models
- **Custom Models**: Build custom architectures

### PyTorch
- **Neural Networks**: Custom architectures
- **Computer Vision**: CNN models
- **NLP**: Transformer models

### XGBoost & LightGBM
- **Gradient Boosting**: Classification and regression
- **Feature Importance**: Model interpretability
- **Hyperparameter Tuning**: Automated optimization

## 📊 Model Management

### Model Registry
- **Version Control**: Track model versions
- **Metadata**: Store model information
- **Artifacts**: Save model files and dependencies
- **Lifecycle**: Model deployment and retirement

### Model Monitoring
- **Performance Tracking**: Monitor accuracy, loss
- **Data Drift**: Detect concept drift
- **Model Health**: Alert on model degradation
- **A/B Testing**: Compare model versions

### Model Deployment
- **Production Ready**: Optimized for inference
- **Scalable**: Handle high traffic
- **Reliable**: Fault tolerance and recovery
- **Secure**: Input validation and sanitization

## 🔒 Security Features

- **JWT Authentication**: Secure API access
- **Input Validation**: Validate all inputs
- **Rate Limiting**: Prevent API abuse
- **CORS**: Cross-origin resource sharing
- **HTTPS**: Secure communication

## 📈 Performance Optimization

- **Caching**: Redis-based response caching
- **Async Processing**: Background model training
- **Batch Processing**: Efficient bulk predictions
- **Model Optimization**: Quantization and pruning
- **Load Balancing**: Distribute traffic

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_models.py

# Run linting
flake8 app/

# Format code
black app/
```

## 📦 Deployment

### Docker Deployment
```bash
# Build Docker image
docker build -t ml-api .

# Run container
docker run -p 5000:5000 ml-api
```

### Production Deployment
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Using Docker Compose
docker-compose up -d
```

## 📚 API Documentation

Access interactive API documentation at:
```
http://localhost:5000/api/docs
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Siddhesh Amrale**
- GitHub: [@siddheshamrale](https://github.com/siddheshamrale)
- LinkedIn: [Siddhesh Amrale](https://linkedin.com/in/siddhesh-amrale)

## 🙏 Acknowledgments

- Flask community
- scikit-learn team
- TensorFlow and PyTorch teams
- PostgreSQL and Redis communities 