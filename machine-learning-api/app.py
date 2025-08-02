from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import joblib
import numpy as np
import pandas as pd
import os
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Rate limiting
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Global variables for model management
models = {}
model_metadata = {}

class MLModel:
    def __init__(self, name, model_type, description):
        self.name = name
        self.model_type = model_type
        self.description = description
        self.model = None
        self.features = []
        self.created_at = datetime.now()
        self.last_updated = datetime.now()
    
    def load_model(self, model_path):
        """Load a trained model from file."""
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Model {self.name} loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model {self.name}: {e}")
            return False
    
    def predict(self, data):
        """Make predictions using the loaded model."""
        if self.model is None:
            raise ValueError("Model not loaded")
        
        try:
            # Convert input data to numpy array
            if isinstance(data, list):
                data = np.array(data)
            elif isinstance(data, dict):
                # Extract features in order
                data = np.array([data.get(feature, 0) for feature in self.features])
            
            # Reshape if needed
            if len(data.shape) == 1:
                data = data.reshape(1, -1)
            
            prediction = self.model.predict(data)
            probability = None
            
            # Get probability if available
            if hasattr(self.model, 'predict_proba'):
                probability = self.model.predict_proba(data).tolist()
            
            return {
                'prediction': prediction.tolist(),
                'probability': probability,
                'model_name': self.name,
                'model_type': self.model_type,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Prediction error for model {self.name}: {e}")
            raise

# Initialize sample models
def initialize_models():
    """Initialize sample models for demonstration."""
    # Sample linear regression model
    from sklearn.linear_model import LinearRegression
    from sklearn.ensemble import RandomForestClassifier
    
    # Create sample data and train models
    np.random.seed(42)
    X_reg = np.random.rand(100, 3)
    y_reg = X_reg[:, 0] * 2 + X_reg[:, 1] * 3 + X_reg[:, 2] * 1.5 + np.random.rand(100) * 0.1
    
    X_clf = np.random.rand(100, 4)
    y_clf = (X_clf[:, 0] + X_clf[:, 1] > 1).astype(int)
    
    # Train and save models
    reg_model = LinearRegression()
    reg_model.fit(X_reg, y_reg)
    joblib.dump(reg_model, 'models/regression_model.pkl')
    
    clf_model = RandomForestClassifier(n_estimators=10, random_state=42)
    clf_model.fit(X_clf, y_clf)
    joblib.dump(clf_model, 'models/classification_model.pkl')
    
    # Register models
    models['regression'] = MLModel('regression', 'regression', 'Linear regression model for numerical prediction')
    models['regression'].model = reg_model
    models['regression'].features = ['feature1', 'feature2', 'feature3']
    
    models['classification'] = MLModel('classification', 'classification', 'Random forest classifier for binary classification')
    models['classification'].model = clf_model
    models['classification'].features = ['feature1', 'feature2', 'feature3', 'feature4']

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'models_loaded': len([m for m in models.values() if m.model is not None])
    })

# Model management endpoints
@app.route('/models', methods=['GET'])
@limiter.limit("100 per minute")
def list_models():
    """List all available models."""
    model_list = []
    for name, model in models.items():
        model_list.append({
            'name': name,
            'type': model.model_type,
            'description': model.description,
            'loaded': model.model is not None,
            'features': model.features,
            'created_at': model.created_at.isoformat(),
            'last_updated': model.last_updated.isoformat()
        })
    
    return jsonify({
        'models': model_list,
        'total_models': len(model_list)
    })

@app.route('/models/<model_name>', methods=['GET'])
@limiter.limit("100 per minute")
def get_model_info(model_name):
    """Get information about a specific model."""
    if model_name not in models:
        return jsonify({'error': 'Model not found'}), 404
    
    model = models[model_name]
    return jsonify({
        'name': model.name,
        'type': model.model_type,
        'description': model.description,
        'loaded': model.model is not None,
        'features': model.features,
        'created_at': model.created_at.isoformat(),
        'last_updated': model.last_updated.isoformat()
    })

# Prediction endpoints
@app.route('/predict/<model_name>', methods=['POST'])
@limiter.limit("50 per minute")
def predict(model_name):
    """Make predictions using a specific model."""
    if model_name not in models:
        return jsonify({'error': 'Model not found'}), 404
    
    model = models[model_name]
    if model.model is None:
        return jsonify({'error': 'Model not loaded'}), 400
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Handle different input formats
        if 'features' in data:
            input_data = data['features']
        elif 'data' in data:
            input_data = data['data']
        else:
            input_data = data
        
        result = model.predict(input_data)
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/predict/batch/<model_name>', methods=['POST'])
@limiter.limit("20 per minute")
def predict_batch(model_name):
    """Make batch predictions using a specific model."""
    if model_name not in models:
        return jsonify({'error': 'Model not found'}), 404
    
    model = models[model_name]
    if model.model is None:
        return jsonify({'error': 'Model not loaded'}), 400
    
    try:
        data = request.get_json()
        if not data or 'instances' not in data:
            return jsonify({'error': 'No instances provided'}), 400
        
        instances = data['instances']
        if not isinstance(instances, list):
            return jsonify({'error': 'Instances must be a list'}), 400
        
        results = []
        for i, instance in enumerate(instances):
            try:
                result = model.predict(instance)
                results.append({
                    'index': i,
                    'success': True,
                    'result': result
                })
            except Exception as e:
                results.append({
                    'index': i,
                    'success': False,
                    'error': str(e)
                })
        
        return jsonify({
            'model_name': model_name,
            'total_instances': len(instances),
            'successful_predictions': len([r for r in results if r['success']]),
            'results': results
        })
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        return jsonify({'error': str(e)}), 400

# Model management endpoints
@app.route('/models/<model_name>/load', methods=['POST'])
@limiter.limit("10 per minute")
def load_model(model_name):
    """Load a model from file."""
    if model_name not in models:
        return jsonify({'error': 'Model not found'}), 404
    
    try:
        data = request.get_json() or {}
        model_path = data.get('model_path', f'models/{model_name}_model.pkl')
        
        model = models[model_name]
        success = model.load_model(model_path)
        
        if success:
            model.last_updated = datetime.now()
            return jsonify({
                'message': f'Model {model_name} loaded successfully',
                'model_path': model_path
            })
        else:
            return jsonify({'error': f'Failed to load model {model_name}'}), 500
    
    except Exception as e:
        logger.error(f"Model loading error: {e}")
        return jsonify({'error': str(e)}), 400

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Create models directory if it doesn't exist
    os.makedirs('models', exist_ok=True)
    
    # Initialize models
    initialize_models()
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 