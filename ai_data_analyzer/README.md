# AI Data Analyzer

A powerful AI-powered data analysis tool that leverages OpenAI's GPT models to provide intelligent insights, visualizations, and comprehensive reports from your datasets.

## 🚀 Features

### Core Analysis Capabilities
- **Intelligent Data Analysis**: AI-powered insights and pattern detection
- **Multi-format Support**: CSV, Excel, JSON file formats
- **Comprehensive Reports**: Detailed analysis with recommendations
- **Anomaly Detection**: Identify outliers and unusual patterns
- **Statistical Analysis**: Descriptive statistics and correlations
- **Trend Analysis**: Time-series and pattern recognition

### Visualization Features
- **Automatic Chart Generation**: Histograms, scatter plots, correlation matrices
- **Custom Visualizations**: Tailored charts based on data characteristics
- **Export Capabilities**: Save charts as PNG, PDF, or interactive HTML
- **Dashboard Creation**: Multi-panel visualization layouts

### AI-Powered Insights
- **Natural Language Explanations**: Human-readable analysis summaries
- **Recommendations**: Actionable insights and suggestions
- **Pattern Recognition**: Identify trends and relationships
- **Predictive Insights**: Basic forecasting and trend analysis

## 🛠️ Installation

### Prerequisites
- Python 3.7+
- OpenAI API key
- Required Python packages (see requirements.txt)

### Setup

1. **Clone or download the project**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## 📊 Usage

### Basic Usage

```python
from ai_data_analyzer.main import AIDataAnalyzer

# Initialize the analyzer
analyzer = AIDataAnalyzer()

# Load your dataset
analyzer.load_dataset("your_data.csv")

# Get basic dataset information
info = analyzer.get_dataset_info()
print(f"Dataset shape: {info['shape']}")

# Perform comprehensive analysis
analysis = analyzer.analyze_dataset("comprehensive")
print(analysis['summary'])
```

### Advanced Usage

```python
# Detect anomalies
anomalies = analyzer.detect_anomalies(['column1', 'column2'])

# Generate visualizations
charts = analyzer.generate_visualizations(
    columns=['column1', 'column2'],
    output_dir="./charts"
)

# Generate comprehensive report
report = analyzer.generate_report(analysis, "analysis_report.html")
```

### Command Line Interface

```bash
python main.py --file your_data.csv --analysis comprehensive
```

## 🔧 API Reference

### Core Methods

#### `load_dataset(file_path: str) -> bool`
Load a dataset from file (CSV, Excel, JSON).

**Parameters:**
- `file_path`: Path to the dataset file

**Returns:**
- `bool`: True if successful, False otherwise

#### `get_dataset_info() -> Dict[str, Any]`
Get basic information about the loaded dataset.

**Returns:**
- Dictionary with dataset shape, columns, data types, and basic statistics

#### `analyze_dataset(analysis_type: str = "comprehensive") -> Dict[str, Any]`
Perform AI-powered analysis on the dataset.

**Parameters:**
- `analysis_type`: Type of analysis ("comprehensive", "basic", "statistical")

**Returns:**
- Dictionary with analysis results, insights, and recommendations

#### `detect_anomalies(columns: List[str] = None) -> Dict[str, Any]`
Detect anomalies and outliers in the dataset.

**Parameters:**
- `columns`: List of columns to analyze (None for all numeric columns)

**Returns:**
- Dictionary with detected anomalies and their characteristics

#### `generate_visualizations(columns: List[str] = None, output_dir: str = "./visualizations") -> Dict[str, Any]`
Generate charts and visualizations for the dataset.

**Parameters:**
- `columns`: List of columns to visualize (None for all columns)
- `output_dir`: Directory to save generated charts

**Returns:**
- Dictionary with paths to generated visualizations

#### `generate_report(analysis_result: Dict[str, Any] = None, output_file: str = None) -> str`
Generate a comprehensive HTML report.

**Parameters:**
- `analysis_result`: Analysis results to include in report
- `output_file`: Path for the output HTML file

**Returns:**
- Path to the generated report file

## 📈 Analysis Types

### Comprehensive Analysis
- Statistical summary
- Correlation analysis
- Distribution analysis
- AI-powered insights
- Recommendations

### Basic Analysis
- Simple statistics
- Data quality assessment
- Basic visualizations

### Statistical Analysis
- Detailed statistical tests
- Hypothesis testing
- Confidence intervals

## 🎨 Visualization Types

### Automatic Charts
- **Histograms**: Distribution analysis
- **Scatter Plots**: Correlation visualization
- **Box Plots**: Outlier detection
- **Correlation Matrices**: Relationship analysis
- **Time Series**: Trend visualization
- **Bar Charts**: Categorical analysis

### Custom Visualizations
- **Heatmaps**: Correlation and pattern visualization
- **Violin Plots**: Distribution comparison
- **Pair Plots**: Multi-variable relationships
- **3D Plots**: Three-dimensional data visualization

## 📊 Supported File Formats

### Input Formats
- **CSV**: Comma-separated values
- **Excel**: .xlsx and .xls files
- **JSON**: JavaScript Object Notation

### Output Formats
- **HTML**: Interactive reports
- **PNG**: Static image charts
- **PDF**: High-quality print-ready charts
- **JSON**: Analysis results

## 🔍 Example Use Cases

### Business Analytics
```python
# Analyze sales data
analyzer.load_dataset("sales_data.csv")
analysis = analyzer.analyze_dataset("comprehensive")
report = analyzer.generate_report(analysis, "sales_analysis.html")
```

### Research Data
```python
# Analyze survey responses
analyzer.load_dataset("survey_results.xlsx")
anomalies = analyzer.detect_anomalies(['satisfaction_score'])
charts = analyzer.generate_visualizations(['age', 'satisfaction_score'])
```

### Financial Data
```python
# Analyze stock prices
analyzer.load_dataset("stock_prices.csv")
analysis = analyzer.analyze_dataset("statistical")
trends = analyzer.detect_anomalies(['price', 'volume'])
```

## ⚙️ Configuration

### Analysis Settings
```python
analyzer.analysis_settings = {
    "max_tokens": 1000,
    "temperature": 0.3,
    "include_visualizations": True,
    "detailed_analysis": True
}
```

### Custom Prompts
You can customize the AI prompts for specific analysis types by modifying the prompt templates in the code.

## 🚀 Performance Tips

### Large Datasets
- Use sampling for very large datasets
- Focus on specific columns for detailed analysis
- Enable caching for repeated analyses

### Memory Optimization
- Clear analysis history when not needed
- Use chunked processing for large files
- Monitor memory usage during analysis

## 🔧 Troubleshooting

### Common Issues

**"OpenAI API key not found"**
- Ensure OPENAI_API_KEY environment variable is set
- Check .env file format and location

**"File format not supported"**
- Verify file extension is supported (.csv, .xlsx, .json)
- Check file is not corrupted

**"Memory error"**
- Reduce dataset size or use sampling
- Close other applications to free memory
- Use chunked processing

**"Visualization error"**
- Install required plotting libraries (matplotlib, seaborn)
- Check output directory permissions
- Verify data types are suitable for visualization

## 📚 Dependencies

### Required Packages
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computing
- `matplotlib`: Basic plotting
- `seaborn`: Statistical visualizations
- `openai`: OpenAI API integration
- `python-dotenv`: Environment variable management

### Optional Packages
- `plotly`: Interactive visualizations
- `bokeh`: Advanced plotting
- `scipy`: Scientific computing
- `scikit-learn`: Machine learning utilities

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Areas for Contribution
- Additional visualization types
- New analysis algorithms
- Performance optimizations
- Documentation improvements
- Bug fixes and enhancements

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🔗 Links

- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Matplotlib Documentation](https://matplotlib.org/)
- [Seaborn Documentation](https://seaborn.pydata.org/)

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review the example use cases
- Open an issue on GitHub
- Consult the API documentation

---

**Note**: This tool requires an OpenAI API key to function. Make sure to set up your API key before running any analyses. 