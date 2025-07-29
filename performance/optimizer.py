#!/usr/bin/env python3
"""
Performance optimization system for AI Projects Collection.

Provides tools for:
- Code performance profiling
- Memory usage optimization
- Caching strategies
- API call optimization
"""

import time
import cProfile
import pstats
import io
import psutil
import os
from functools import wraps
from typing import Dict, Any, Optional, Callable
import json
from datetime import datetime
import logging


class PerformanceProfiler:
    """Performance profiler for AI projects."""
    
    def __init__(self, output_dir: str = "./performance_logs"):
        """Initialize performance profiler.
        
        Args:
            output_dir: Directory for performance logs
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.profiles = {}
    
    def profile_function(self, func: Callable) -> Callable:
        """Decorator to profile a function.
        
        Args:
            func: Function to profile
            
        Returns:
            Decorated function
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            profiler = cProfile.Profile()
            profiler.enable()
            
            start_time = time.time()
            start_memory = psutil.Process().memory_info().rss
            
            try:
                result = func(*args, **kwargs)
                success = True
            except Exception as e:
                result = None
                success = False
                raise e
            finally:
                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss
                
                profiler.disable()
                
                # Save profile stats
                s = io.StringIO()
                ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
                ps.print_stats(20)  # Top 20 functions
                
                profile_data = {
                    "function_name": func.__name__,
                    "module": func.__module__,
                    "execution_time": end_time - start_time,
                    "memory_delta": end_memory - start_memory,
                    "success": success,
                    "timestamp": datetime.now().isoformat(),
                    "profile_stats": s.getvalue()
                }
                
                # Save to file
                filename = f"{func.__name__}_{int(time.time())}.json"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'w') as f:
                    json.dump(profile_data, f, indent=2)
                
                self.profiles[func.__name__] = profile_data
                
                self.logger.info(f"Profiled {func.__name__}: {profile_data['execution_time']:.3f}s, "
                               f"Memory: {profile_data['memory_delta'] / 1024 / 1024:.2f}MB")
            
            return result
        
        return wrapper
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get summary of all performance profiles.
        
        Returns:
            Dictionary with performance summary
        """
        if not self.profiles:
            return {"message": "No profiles available"}
        
        total_time = sum(p["execution_time"] for p in self.profiles.values())
        total_memory = sum(p["memory_delta"] for p in self.profiles.values())
        avg_time = total_time / len(self.profiles)
        avg_memory = total_memory / len(self.profiles)
        
        # Find slowest and fastest functions
        sorted_by_time = sorted(self.profiles.items(), 
                              key=lambda x: x[1]["execution_time"], 
                              reverse=True)
        
        return {
            "total_functions_profiled": len(self.profiles),
            "total_execution_time": total_time,
            "total_memory_delta": total_memory,
            "average_execution_time": avg_time,
            "average_memory_delta": avg_memory,
            "slowest_function": {
                "name": sorted_by_time[0][0],
                "time": sorted_by_time[0][1]["execution_time"]
            },
            "fastest_function": {
                "name": sorted_by_time[-1][0],
                "time": sorted_by_time[-1][1]["execution_time"]
            },
            "functions": list(self.profiles.keys())
        }


class MemoryOptimizer:
    """Memory optimization utilities."""
    
    def __init__(self):
        """Initialize memory optimizer."""
        self.logger = logging.getLogger(__name__)
    
    def get_memory_usage(self) -> Dict[str, Any]:
        """Get current memory usage.
        
        Returns:
            Dictionary with memory usage information
        """
        process = psutil.Process()
        memory_info = process.memory_info()
        
        return {
            "rss": memory_info.rss,  # Resident Set Size
            "vms": memory_info.vms,  # Virtual Memory Size
            "percent": process.memory_percent(),
            "available": psutil.virtual_memory().available,
            "total": psutil.virtual_memory().total,
            "timestamp": datetime.now().isoformat()
        }
    
    def monitor_memory(self, interval: int = 5, duration: int = 60) -> Dict[str, Any]:
        """Monitor memory usage over time.
        
        Args:
            interval: Check interval in seconds
            duration: Total monitoring duration in seconds
            
        Returns:
            Dictionary with memory monitoring results
        """
        self.logger.info(f"Starting memory monitoring for {duration} seconds...")
        
        measurements = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            measurement = self.get_memory_usage()
            measurements.append(measurement)
            
            self.logger.info(f"Memory: {measurement['rss'] / 1024 / 1024:.2f}MB "
                           f"({measurement['percent']:.1f}%)")
            
            time.sleep(interval)
        
        # Calculate statistics
        rss_values = [m["rss"] for m in measurements]
        percent_values = [m["percent"] for m in measurements]
        
        return {
            "duration": duration,
            "interval": interval,
            "measurements": measurements,
            "statistics": {
                "max_rss": max(rss_values),
                "min_rss": min(rss_values),
                "avg_rss": sum(rss_values) / len(rss_values),
                "max_percent": max(percent_values),
                "min_percent": min(percent_values),
                "avg_percent": sum(percent_values) / len(percent_values)
            }
        }


class CacheManager:
    """Cache management for performance optimization."""
    
    def __init__(self, cache_dir: str = "./cache"):
        """Initialize cache manager.
        
        Args:
            cache_dir: Directory for cache files
        """
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "evictions": 0
        }
    
    def cache_result(self, key: str, result: Any, ttl: int = 3600) -> None:
        """Cache a result.
        
        Args:
            key: Cache key
            result: Result to cache
            ttl: Time to live in seconds
        """
        cache_data = {
            "result": result,
            "timestamp": datetime.now().isoformat(),
            "ttl": ttl
        }
        
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            self.logger.info(f"Cached result for key: {key}")
        except Exception as e:
            self.logger.error(f"Failed to cache result for key {key}: {e}")
    
    def get_cached_result(self, key: str) -> Optional[Any]:
        """Get cached result.
        
        Args:
            key: Cache key
            
        Returns:
            Cached result or None if not found/expired
        """
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        if not os.path.exists(cache_file):
            self.cache_stats["misses"] += 1
            return None
        
        try:
            with open(cache_file, 'r') as f:
                cache_data = json.load(f)
            
            # Check if expired
            cached_time = datetime.fromisoformat(cache_data["timestamp"])
            current_time = datetime.now()
            age = (current_time - cached_time).total_seconds()
            
            if age > cache_data["ttl"]:
                os.remove(cache_file)
                self.cache_stats["misses"] += 1
                return None
            
            self.cache_stats["hits"] += 1
            return cache_data["result"]
            
        except Exception as e:
            self.logger.error(f"Failed to get cached result for key {key}: {e}")
            self.cache_stats["misses"] += 1
            return None
    
    def clear_cache(self) -> None:
        """Clear all cached results."""
        try:
            for file in os.listdir(self.cache_dir):
                if file.endswith('.json'):
                    os.remove(os.path.join(self.cache_dir, file))
            self.logger.info("Cache cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear cache: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics
        """
        total_requests = self.cache_stats["hits"] + self.cache_stats["misses"]
        hit_rate = (self.cache_stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.cache_stats,
            "total_requests": total_requests,
            "hit_rate": hit_rate,
            "cache_size": len([f for f in os.listdir(self.cache_dir) if f.endswith('.json')])
        }


class APIOptimizer:
    """API call optimization utilities."""
    
    def __init__(self):
        """Initialize API optimizer."""
        self.logger = logging.getLogger(__name__)
        self.call_history = []
    
    def optimize_batch_calls(self, calls: list, batch_size: int = 10) -> list:
        """Optimize API calls by batching them.
        
        Args:
            calls: List of API calls to optimize
            batch_size: Size of each batch
            
        Returns:
            List of batched calls
        """
        batches = []
        
        for i in range(0, len(calls), batch_size):
            batch = calls[i:i + batch_size]
            batches.append(batch)
        
        self.logger.info(f"Optimized {len(calls)} calls into {len(batches)} batches")
        return batches
    
    def track_api_call(self, endpoint: str, duration: float, success: bool, 
                      tokens_used: Optional[int] = None) -> None:
        """Track API call performance.
        
        Args:
            endpoint: API endpoint
            duration: Call duration
            success: Whether call was successful
            tokens_used: Number of tokens used
        """
        call_data = {
            "endpoint": endpoint,
            "duration": duration,
            "success": success,
            "tokens_used": tokens_used,
            "timestamp": datetime.now().isoformat()
        }
        
        self.call_history.append(call_data)
        
        # Keep only last 1000 calls
        if len(self.call_history) > 1000:
            self.call_history = self.call_history[-1000:]
    
    def get_api_performance_stats(self) -> Dict[str, Any]:
        """Get API performance statistics.
        
        Returns:
            Dictionary with API performance statistics
        """
        if not self.call_history:
            return {"message": "No API calls tracked"}
        
        successful_calls = [c for c in self.call_history if c["success"]]
        failed_calls = [c for c in self.call_history if not c["success"]]
        
        durations = [c["duration"] for c in self.call_history]
        tokens_used = [c["tokens_used"] for c in self.call_history if c["tokens_used"]]
        
        return {
            "total_calls": len(self.call_history),
            "successful_calls": len(successful_calls),
            "failed_calls": len(failed_calls),
            "success_rate": len(successful_calls) / len(self.call_history) * 100,
            "average_duration": sum(durations) / len(durations),
            "min_duration": min(durations),
            "max_duration": max(durations),
            "total_tokens_used": sum(tokens_used) if tokens_used else 0,
            "average_tokens_per_call": sum(tokens_used) / len(tokens_used) if tokens_used else 0
        }


def main():
    """Main function for performance optimization."""
    print("🚀 Performance Optimization System")
    print("=" * 40)
    
    # Initialize components
    profiler = PerformanceProfiler()
    memory_optimizer = MemoryOptimizer()
    cache_manager = CacheManager()
    api_optimizer = APIOptimizer()
    
    # Example usage
    print("\n📊 Memory Usage:")
    memory_info = memory_optimizer.get_memory_usage()
    print(f"RSS: {memory_info['rss'] / 1024 / 1024:.2f}MB")
    print(f"Percent: {memory_info['percent']:.1f}%")
    
    print("\n💾 Cache Statistics:")
    cache_stats = cache_manager.get_cache_stats()
    print(f"Hit Rate: {cache_stats['hit_rate']:.1f}%")
    print(f"Total Requests: {cache_stats['total_requests']}")
    
    print("\n🔧 Performance profiling and optimization ready!")
    
    return {
        "profiler": profiler,
        "memory_optimizer": memory_optimizer,
        "cache_manager": cache_manager,
        "api_optimizer": api_optimizer
    }


if __name__ == "__main__":
    main() 