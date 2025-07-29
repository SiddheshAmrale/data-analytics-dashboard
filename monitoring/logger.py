#!/usr/bin/env python3
"""
Comprehensive logging system for AI Projects Collection.

Provides structured logging with different levels, file rotation,
and integration with monitoring services.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from typing import Dict, Any, Optional
import json
from pathlib import Path


class AILogger:
    """Advanced logger for AI projects with structured logging."""
    
    def __init__(self, name: str, log_dir: str = "./logs", level: str = "INFO"):
        """Initialize the logger.
        
        Args:
            name: Logger name
            log_dir: Directory for log files
            level: Logging level
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.level = getattr(logging, level.upper())
        
        # Create log directory
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.level)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Add handlers
        self._setup_handlers()
        
    def _setup_handlers(self):
        """Set up logging handlers."""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(self.level)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.name}.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(self.level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / f"{self.name}_error.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        error_handler.setLevel(logging.ERROR)
        error_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s\n'
            'Exception: %(exc_info)s\n'
        )
        error_handler.setFormatter(error_formatter)
        self.logger.addHandler(error_handler)
    
    def log_api_call(self, api_name: str, endpoint: str, duration: float, 
                     success: bool, error: Optional[str] = None):
        """Log API call details.
        
        Args:
            api_name: Name of the API (e.g., 'openai')
            endpoint: API endpoint
            duration: Call duration in seconds
            success: Whether the call was successful
            error: Error message if failed
        """
        log_data = {
            "api_name": api_name,
            "endpoint": endpoint,
            "duration": duration,
            "success": success,
            "timestamp": datetime.now().isoformat()
        }
        
        if error:
            log_data["error"] = error
            self.logger.error(f"API Call Failed: {json.dumps(log_data)}")
        else:
            self.logger.info(f"API Call Success: {json.dumps(log_data)}")
    
    def log_performance(self, operation: str, duration: float, 
                       input_size: Optional[int] = None,
                       output_size: Optional[int] = None):
        """Log performance metrics.
        
        Args:
            operation: Operation name
            duration: Duration in seconds
            input_size: Size of input data
            output_size: Size of output data
        """
        log_data = {
            "operation": operation,
            "duration": duration,
            "input_size": input_size,
            "output_size": output_size,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.info(f"Performance: {json.dumps(log_data)}")
    
    def log_user_action(self, user_id: str, action: str, 
                       details: Optional[Dict[str, Any]] = None):
        """Log user actions.
        
        Args:
            user_id: User identifier
            action: Action performed
            details: Additional details
        """
        log_data = {
            "user_id": user_id,
            "action": action,
            "timestamp": datetime.now().isoformat()
        }
        
        if details:
            log_data["details"] = details
        
        self.logger.info(f"User Action: {json.dumps(log_data)}")
    
    def log_error(self, error: Exception, context: Optional[Dict[str, Any]] = None):
        """Log errors with context.
        
        Args:
            error: Exception object
            context: Additional context
        """
        log_data = {
            "error_type": type(error).__name__,
            "error_message": str(error),
            "timestamp": datetime.now().isoformat()
        }
        
        if context:
            log_data["context"] = context
        
        self.logger.error(f"Error: {json.dumps(log_data)}", exc_info=True)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log security events.
        
        Args:
            event_type: Type of security event
            details: Event details
        """
        log_data = {
            "event_type": event_type,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        self.logger.warning(f"Security Event: {json.dumps(log_data)}")


class MetricsCollector:
    """Collect and store metrics for monitoring."""
    
    def __init__(self, metrics_file: str = "./logs/metrics.json"):
        """Initialize metrics collector.
        
        Args:
            metrics_file: File to store metrics
        """
        self.metrics_file = Path(metrics_file)
        self.metrics_file.parent.mkdir(parents=True, exist_ok=True)
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Load existing metrics from file."""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}
    
    def _save_metrics(self):
        """Save metrics to file."""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except IOError as e:
            logging.error(f"Failed to save metrics: {e}")
    
    def increment_counter(self, metric_name: str, value: int = 1):
        """Increment a counter metric.
        
        Args:
            metric_name: Name of the metric
            value: Value to increment by
        """
        if metric_name not in self.metrics:
            self.metrics[metric_name] = 0
        self.metrics[metric_name] += value
        self._save_metrics()
    
    def record_timing(self, metric_name: str, duration: float):
        """Record timing metric.
        
        Args:
            metric_name: Name of the metric
            duration: Duration in seconds
        """
        if f"{metric_name}_count" not in self.metrics:
            self.metrics[f"{metric_name}_count"] = 0
            self.metrics[f"{metric_name}_total"] = 0.0
            self.metrics[f"{metric_name}_min"] = float('inf')
            self.metrics[f"{metric_name}_max"] = 0.0
        
        self.metrics[f"{metric_name}_count"] += 1
        self.metrics[f"{metric_name}_total"] += duration
        self.metrics[f"{metric_name}_min"] = min(self.metrics[f"{metric_name}_min"], duration)
        self.metrics[f"{metric_name}_max"] = max(self.metrics[f"{metric_name}_max"], duration)
        self.metrics[f"{metric_name}_avg"] = self.metrics[f"{metric_name}_total"] / self.metrics[f"{metric_name}_count"]
        
        self._save_metrics()
    
    def record_gauge(self, metric_name: str, value: float):
        """Record gauge metric.
        
        Args:
            metric_name: Name of the metric
            value: Current value
        """
        self.metrics[metric_name] = value
        self._save_metrics()
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get all metrics.
        
        Returns:
            Dictionary of all metrics
        """
        return self.metrics.copy()


def setup_logging(name: str, log_dir: str = "./logs", level: str = "INFO") -> AILogger:
    """Set up logging for a component.
    
    Args:
        name: Logger name
        log_dir: Directory for log files
        level: Logging level
        
    Returns:
        Configured logger instance
    """
    return AILogger(name, log_dir, level)


def get_metrics_collector(metrics_file: str = "./logs/metrics.json") -> MetricsCollector:
    """Get metrics collector instance.
    
    Args:
        metrics_file: File to store metrics
        
    Returns:
        Metrics collector instance
    """
    return MetricsCollector(metrics_file)


# Example usage
if __name__ == "__main__":
    # Set up logger
    logger = setup_logging("ai_projects", "./logs", "DEBUG")
    
    # Set up metrics collector
    metrics = get_metrics_collector()
    
    # Example usage
    logger.logger.info("Logger initialized successfully")
    logger.log_api_call("openai", "/v1/chat/completions", 1.5, True)
    logger.log_performance("text_summarization", 2.3, input_size=1000, output_size=150)
    
    # Record metrics
    metrics.increment_counter("api_calls")
    metrics.record_timing("api_response_time", 1.5)
    metrics.record_gauge("memory_usage", 85.5)
    
    print("Logging system initialized successfully!") 