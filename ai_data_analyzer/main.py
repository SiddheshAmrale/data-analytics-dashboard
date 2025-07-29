#!/usr/bin/env python3
"""
AI Data Analyzer

A comprehensive data analysis tool that uses AI to:
- Analyze datasets and generate insights
- Create visualizations and reports
- Detect patterns and anomalies
- Generate data summaries and recommendations
"""

import os
import json
import logging
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Optional, Dict, Any, List, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
from openai import OpenAI
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AIDataAnalyzer:
    """AI-powered data analysis tool."""
    
    def __init__(self, api_key: str = None):
        """Initialize the AI Data Analyzer.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from environment.
        """
        if api_key is None:
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        self.api_key = api_key
        self.client = OpenAI(api_key=api_key)
        self.analysis_history = []
        self.current_dataset = None
        self.analysis_settings = {
            "max_tokens": 1000,
            "temperature": 0.3,
            "include_visualizations": True,
            "detailed_analysis": True
        }
        
    def load_dataset(self, file_path: str) -> bool:
        """Load dataset from file.
        
        Args:
            file_path: Path to dataset file (CSV, Excel, JSON)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_extension = file_path.lower().split('.')[-1]
            
            if file_extension == 'csv':
                self.current_dataset = pd.read_csv(file_path)
            elif file_extension in ['xlsx', 'xls']:
                self.current_dataset = pd.read_excel(file_path)
            elif file_extension == 'json':
                self.current_dataset = pd.read_json(file_path)
            else:
                logger.error(f"Unsupported file format: {file_extension}")
                return False
            
            logger.info(f"Dataset loaded successfully: {len(self.current_dataset)} rows, {len(self.current_dataset.columns)} columns")
            return True
            
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def get_dataset_info(self) -> Dict[str, Any]:
        """Get basic information about the current dataset.
        
        Returns:
            Dictionary with dataset information
        """
        if self.current_dataset is None:
            return {"error": "No dataset loaded"}
        
        info = {
            "shape": self.current_dataset.shape,
            "columns": list(self.current_dataset.columns),
            "dtypes": self.current_dataset.dtypes.to_dict(),
            "missing_values": self.current_dataset.isnull().sum().to_dict(),
            "numeric_columns": list(self.current_dataset.select_dtypes(include=[np.number]).columns),
            "categorical_columns": list(self.current_dataset.select_dtypes(include=['object']).columns),
            "memory_usage": self.current_dataset.memory_usage(deep=True).sum(),
            "duplicates": self.current_dataset.duplicated().sum()
        }
        
        # Add basic statistics for numeric columns
        if info["numeric_columns"]:
            info["numeric_stats"] = self.current_dataset[info["numeric_columns"]].describe().to_dict()
        
        return info
    
    def analyze_dataset(self, analysis_type: str = "comprehensive") -> Dict[str, Any]:
        """Analyze the current dataset using AI.
        
        Args:
            analysis_type: Type of analysis (comprehensive, quick, detailed)
            
        Returns:
            Dictionary with analysis results
        """
        if self.current_dataset is None:
            return {"error": "No dataset loaded"}
        
        try:
            # Prepare dataset summary for AI
            dataset_info = self.get_dataset_info()
            sample_data = self.current_dataset.head(10).to_dict('records')
            
            # Create prompt for AI analysis
            prompt = f"""
            Analyze the following dataset and provide insights:
            
            Dataset Information:
            - Shape: {dataset_info['shape']}
            - Columns: {dataset_info['columns']}
            - Numeric columns: {dataset_info['numeric_columns']}
            - Categorical columns: {dataset_info['categorical_columns']}
            - Missing values: {dataset_info['missing_values']}
            
            Sample data (first 10 rows):
            {json.dumps(sample_data, indent=2)}
            
            Please provide a {analysis_type} analysis including:
            1. Data quality assessment
            2. Key insights and patterns
            3. Potential issues or anomalies
            4. Recommendations for further analysis
            5. Business implications (if applicable)
            
            Format the response as JSON with the following structure:
            {{
                "summary": "Brief dataset overview",
                "data_quality": {{
                    "issues": ["list of data quality issues"],
                    "completeness": "percentage of complete data",
                    "consistency": "assessment of data consistency"
                }},
                "insights": {{
                    "patterns": ["list of key patterns"],
                    "anomalies": ["list of anomalies"],
                    "correlations": ["notable correlations"]
                }},
                "recommendations": ["list of recommendations"],
                "business_implications": ["business insights"]
            }}
            """
            
            # Get AI analysis
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a data analyst expert. Provide detailed, accurate analysis in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.analysis_settings["max_tokens"],
                temperature=self.analysis_settings["temperature"]
            )
            
            # Parse AI response
            analysis_text = response.choices[0].message.content
            
            # Try to extract JSON from response
            try:
                # Find JSON in the response
                start_idx = analysis_text.find('{')
                end_idx = analysis_text.rfind('}') + 1
                json_str = analysis_text[start_idx:end_idx]
                analysis_result = json.loads(json_str)
            except:
                # If JSON parsing fails, create structured response
                analysis_result = {
                    "summary": "Analysis completed",
                    "raw_response": analysis_text,
                    "data_quality": {"issues": [], "completeness": "Unknown", "consistency": "Unknown"},
                    "insights": {"patterns": [], "anomalies": [], "correlations": []},
                    "recommendations": [],
                    "business_implications": []
                }
            
            # Add metadata
            analysis_result["metadata"] = {
                "timestamp": datetime.now().isoformat(),
                "analysis_type": analysis_type,
                "dataset_shape": dataset_info["shape"],
                "columns_analyzed": len(dataset_info["columns"])
            }
            
            # Store in history
            self.analysis_history.append(analysis_result)
            
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error analyzing dataset: {e}")
            return {"error": f"Analysis failed: {str(e)}"}
    
    def detect_anomalies(self, columns: List[str] = None) -> Dict[str, Any]:
        """Detect anomalies in the dataset.
        
        Args:
            columns: List of columns to analyze (if None, uses all numeric columns)
            
        Returns:
            Dictionary with anomaly detection results
        """
        if self.current_dataset is None:
            return {"error": "No dataset loaded"}
        
        try:
            if columns is None:
                columns = list(self.current_dataset.select_dtypes(include=[np.number]).columns)
            
            anomalies = {}
            
            for column in columns:
                if column in self.current_dataset.columns:
                    data = self.current_dataset[column].dropna()
                    
                    if len(data) > 0:
                        # Calculate statistics
                        mean_val = data.mean()
                        std_val = data.std()
                        q1 = data.quantile(0.25)
                        q3 = data.quantile(0.75)
                        iqr = q3 - q1
                        
                        # Define anomaly thresholds
                        z_score_threshold = 3
                        iqr_threshold = 1.5
                        
                        # Detect anomalies using multiple methods
                        z_scores = np.abs((data - mean_val) / std_val)
                        z_anomalies = data[z_scores > z_score_threshold]
                        
                        lower_bound = q1 - iqr_threshold * iqr
                        upper_bound = q3 + iqr_threshold * iqr
                        iqr_anomalies = data[(data < lower_bound) | (data > upper_bound)]
                        
                        anomalies[column] = {
                            "total_values": len(data),
                            "anomalies_z_score": len(z_anomalies),
                            "anomalies_iqr": len(iqr_anomalies),
                            "anomaly_percentage": (len(z_anomalies) / len(data)) * 100,
                            "statistics": {
                                "mean": mean_val,
                                "std": std_val,
                                "q1": q1,
                                "q3": q3,
                                "iqr": iqr
                            },
                            "anomaly_values": list(z_anomalies.index)
                        }
            
            return {
                "anomalies": anomalies,
                "summary": {
                    "columns_analyzed": len(anomalies),
                    "total_anomalies": sum(a["anomalies_z_score"] for a in anomalies.values()),
                    "average_anomaly_percentage": np.mean([a["anomaly_percentage"] for a in anomalies.values()]) if anomalies else 0
                }
            }
            
        except Exception as e:
            logger.error(f"Error detecting anomalies: {e}")
            return {"error": f"Anomaly detection failed: {str(e)}"}
    
    def generate_visualizations(self, columns: List[str] = None, output_dir: str = "./visualizations") -> Dict[str, Any]:
        """Generate visualizations for the dataset.
        
        Args:
            columns: List of columns to visualize (if None, uses all columns)
            output_dir: Directory to save visualizations
            
        Returns:
            Dictionary with visualization results
        """
        if self.current_dataset is None:
            return {"error": "No dataset loaded"}
        
        try:
            os.makedirs(output_dir, exist_ok=True)
            
            if columns is None:
                columns = list(self.current_dataset.columns)
            
            visualizations = {}
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            for column in columns:
                if column not in self.current_dataset.columns:
                    continue
                
                plt.figure(figsize=(10, 6))
                
                # Determine plot type based on data type
                if self.current_dataset[column].dtype in ['object', 'category']:
                    # Categorical data
                    value_counts = self.current_dataset[column].value_counts()
                    plt.bar(range(len(value_counts)), value_counts.values)
                    plt.title(f'Distribution of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Count')
                    plt.xticks(range(len(value_counts)), value_counts.index, rotation=45)
                    
                else:
                    # Numeric data
                    plt.hist(self.current_dataset[column].dropna(), bins=30, alpha=0.7)
                    plt.title(f'Distribution of {column}')
                    plt.xlabel(column)
                    plt.ylabel('Frequency')
                
                # Save plot
                filename = f"{column}_distribution_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                plt.close()
                
                visualizations[column] = filepath
            
            # Create correlation heatmap for numeric columns
            numeric_columns = self.current_dataset.select_dtypes(include=[np.number]).columns
            if len(numeric_columns) > 1:
                plt.figure(figsize=(12, 10))
                correlation_matrix = self.current_dataset[numeric_columns].corr()
                sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0)
                plt.title('Correlation Heatmap')
                
                filename = f"correlation_heatmap_{timestamp}.png"
                filepath = os.path.join(output_dir, filename)
                plt.savefig(filepath, dpi=300, bbox_inches='tight')
                plt.close()
                
                visualizations["correlation_heatmap"] = filepath
            
            return {
                "visualizations": visualizations,
                "output_directory": output_dir,
                "total_plots": len(visualizations)
            }
            
        except Exception as e:
            logger.error(f"Error generating visualizations: {e}")
            return {"error": f"Visualization generation failed: {str(e)}"}
    
    def generate_report(self, analysis_result: Dict[str, Any] = None, output_file: str = None) -> str:
        """Generate a comprehensive analysis report.
        
        Args:
            analysis_result: Analysis result to include in report
            output_file: Output file path (optional)
            
        Returns:
            Report content as string
        """
        if self.current_dataset is None:
            return "Error: No dataset loaded"
        
        if analysis_result is None:
            analysis_result = self.analyze_dataset()
        
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"data_analysis_report_{timestamp}.txt"
        
        # Generate report content
        report_lines = [
            "=" * 60,
            "AI DATA ANALYSIS REPORT",
            "=" * 60,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Dataset: {len(self.current_dataset)} rows, {len(self.current_dataset.columns)} columns",
            "",
            "EXECUTIVE SUMMARY",
            "-" * 20,
            analysis_result.get("summary", "No summary available"),
            "",
            "DATA QUALITY ASSESSMENT",
            "-" * 25,
        ]
        
        # Add data quality information
        data_quality = analysis_result.get("data_quality", {})
        for key, value in data_quality.items():
            report_lines.append(f"{key.title()}: {value}")
        
        report_lines.extend([
            "",
            "KEY INSIGHTS",
            "-" * 15,
        ])
        
        # Add insights
        insights = analysis_result.get("insights", {})
        for category, items in insights.items():
            report_lines.append(f"{category.title()}:")
            if isinstance(items, list):
                for item in items:
                    report_lines.append(f"  - {item}")
            else:
                report_lines.append(f"  {items}")
            report_lines.append("")
        
        report_lines.extend([
            "RECOMMENDATIONS",
            "-" * 20,
        ])
        
        # Add recommendations
        recommendations = analysis_result.get("recommendations", [])
        for i, rec in enumerate(recommendations, 1):
            report_lines.append(f"{i}. {rec}")
        
        report_lines.extend([
            "",
            "BUSINESS IMPLICATIONS",
            "-" * 25,
        ])
        
        # Add business implications
        business_implications = analysis_result.get("business_implications", [])
        for i, impl in enumerate(business_implications, 1):
            report_lines.append(f"{i}. {impl}")
        
        report_content = "\n".join(report_lines)
        
        # Save report
        try:
            with open(output_file, 'w') as f:
                f.write(report_content)
            logger.info(f"Report saved to: {output_file}")
        except Exception as e:
            logger.error(f"Error saving report: {e}")
        
        return report_content
    
    def get_analysis_history(self) -> List[Dict[str, Any]]:
        """Get analysis history.
        
        Returns:
            List of previous analyses
        """
        return self.analysis_history.copy()
    
    def clear_analysis_history(self):
        """Clear analysis history."""
        self.analysis_history.clear()
    
    def save_analysis(self, filename: str):
        """Save analysis history to file.
        
        Args:
            filename: Output file path
        """
        try:
            with open(filename, 'w') as f:
                json.dump(self.analysis_history, f, indent=2)
            logger.info(f"Analysis history saved to: {filename}")
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
    
    def load_analysis(self, filename: str):
        """Load analysis history from file.
        
        Args:
            filename: Input file path
        """
        try:
            with open(filename, 'r') as f:
                self.analysis_history = json.load(f)
            logger.info(f"Analysis history loaded from: {filename}")
        except Exception as e:
            logger.error(f"Error loading analysis: {e}")


def main():
    """Main function for interactive data analyzer."""
    print("📊 AI Data Analyzer")
    print("=" * 30)
    
    try:
        # Initialize analyzer
        analyzer = AIDataAnalyzer()
        
        print("Data Analyzer initialized successfully!")
        print("\nAvailable commands:")
        print("1. 'load' - Load dataset")
        print("2. 'info' - Show dataset information")
        print("3. 'analyze' - Analyze dataset")
        print("4. 'anomalies' - Detect anomalies")
        print("5. 'visualize' - Generate visualizations")
        print("6. 'report' - Generate analysis report")
        print("7. 'history' - View analysis history")
        print("8. 'save' - Save analysis")
        print("9. 'load_analysis' - Load analysis")
        print("10. 'clear' - Clear analysis history")
        print("11. 'quit' - Exit")
        
        while True:
            command = input("\nEnter command: ").strip().lower()
            
            if command == 'quit':
                print("Goodbye!")
                break
            elif command == 'load':
                file_path = input("Enter dataset file path: ")
                if analyzer.load_dataset(file_path):
                    print("Dataset loaded successfully!")
                else:
                    print("Failed to load dataset")
            elif command == 'info':
                info = analyzer.get_dataset_info()
                if "error" not in info:
                    print(f"Dataset shape: {info['shape']}")
                    print(f"Columns: {info['columns']}")
                    print(f"Numeric columns: {info['numeric_columns']}")
                    print(f"Categorical columns: {info['categorical_columns']}")
                else:
                    print(info["error"])
            elif command == 'analyze':
                analysis_type = input("Enter analysis type (comprehensive/quick/detailed): ").strip() or "comprehensive"
                result = analyzer.analyze_dataset(analysis_type)
                if "error" not in result:
                    print("Analysis completed!")
                    print(f"Summary: {result.get('summary', 'N/A')}")
                else:
                    print(f"Analysis failed: {result['error']}")
            elif command == 'anomalies':
                columns_input = input("Enter columns to analyze (comma-separated, or press Enter for all numeric): ").strip()
                columns = [col.strip() for col in columns_input.split(',')] if columns_input else None
                result = analyzer.detect_anomalies(columns)
                if "error" not in result:
                    print("Anomaly detection completed!")
                    print(f"Total anomalies found: {result['summary']['total_anomalies']}")
                else:
                    print(f"Anomaly detection failed: {result['error']}")
            elif command == 'visualize':
                columns_input = input("Enter columns to visualize (comma-separated, or press Enter for all): ").strip()
                columns = [col.strip() for col in columns_input.split(',')] if columns_input else None
                result = analyzer.generate_visualizations(columns)
                if "error" not in result:
                    print(f"Visualizations generated: {result['total_plots']} plots")
                    print(f"Saved to: {result['output_directory']}")
                else:
                    print(f"Visualization failed: {result['error']}")
            elif command == 'report':
                output_file = input("Enter output file name (or press Enter for default): ").strip() or None
                report = analyzer.generate_report(output_file=output_file)
                print("Report generated successfully!")
            elif command == 'history':
                history = analyzer.get_analysis_history()
                print(f"Analysis history ({len(history)} analyses):")
                for i, analysis in enumerate(history[-5:], 1):  # Show last 5
                    print(f"{i}. {analysis.get('summary', 'No summary')[:50]}...")
            elif command == 'save':
                filename = input("Enter filename: ")
                analyzer.save_analysis(filename)
            elif command == 'load_analysis':
                filename = input("Enter filename: ")
                analyzer.load_analysis(filename)
            elif command == 'clear':
                analyzer.clear_analysis_history()
                print("Analysis history cleared!")
            else:
                print("Unknown command. Type 'quit' to exit.")
                
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main() 