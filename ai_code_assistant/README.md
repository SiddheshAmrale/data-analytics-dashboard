# AI Code Assistant

An intelligent code generation, debugging, and analysis tool powered by OpenAI's GPT models that helps developers write better code, fix bugs, and understand complex codebases.

## Features

- 💻 **Code Generation**: Generate code from natural language descriptions
- 🐛 **Code Debugging**: Identify and fix code issues automatically
- 📖 **Code Explanation**: Understand what code does with detailed explanations
- ⚡ **Code Optimization**: Optimize code for performance, readability, and security
- 🧪 **Test Generation**: Generate comprehensive unit tests
- 🔄 **Code Conversion**: Convert code between different programming languages
- 📊 **Complexity Analysis**: Analyze code complexity and maintainability
- 📋 **History Management**: Track all code operations and changes
- 💾 **Export Capabilities**: Save code history and analysis results

## Installation

1. Clone or download this project
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your OpenAI API key:
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```
   Or create a `.env` file:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## Usage

### Basic Usage

Run the main script:
```bash
python main.py
```

### Programmatic Usage

```python
from main import AICodeAssistant

# Initialize the assistant
assistant = AICodeAssistant(api_key="your-api-key")

# Generate code
code = assistant.generate_code("Create a function to calculate fibonacci numbers")
print(code)

# Debug code
fixed_code = assistant.debug_code("def fib(n): return n if n < 2 else fib(n-1) + fib(n-2)")
print(fixed_code)

# Explain code
explanation = assistant.explain_code("def quicksort(arr): return arr if len(arr) <= 1 else quicksort([x for x in arr[1:] if x <= arr[0]]) + [arr[0]] + quicksort([x for x in arr[1:] if x > arr[0]])")
print(explanation)
```

### Advanced Features

#### Code Generation with Different Styles
```python
# Clean code
code = assistant.generate_code("Sort a list of numbers", style="clean")

# Commented code
code = assistant.generate_code("Parse JSON data", style="commented")

# Production-ready code
code = assistant.generate_code("API endpoint for user authentication", style="production")

# Simple code
code = assistant.generate_code("Calculate area of circle", style="simple")
```

#### Code Optimization
```python
# Optimize for performance
optimized = assistant.optimize_code(code, focus="performance")

# Optimize for readability
optimized = assistant.optimize_code(code, focus="readability")

# Optimize for memory usage
optimized = assistant.optimize_code(code, focus="memory")

# Optimize for security
optimized = assistant.optimize_code(code, focus="security")
```

#### Code Conversion
```python
# Convert Python to JavaScript
python_code = "def greet(name): return f'Hello, {name}!'"
js_code = assistant.convert_code(python_code, "python", "javascript")
```

#### Test Generation
```python
# Generate tests for your code
tests = assistant.test_code("""
def add(a, b):
    return a + b
""")
```

#### Complexity Analysis
```python
# Analyze code complexity
analysis = assistant.analyze_code_complexity(complex_code)
print(f"Complexity: {analysis['ai_analysis']['complexity_level']}")
print(f"Maintainability: {analysis['ai_analysis']['maintainability_score']}/10")
```

## API Reference

### AICodeAssistant Class

#### Constructor
```python
AICodeAssistant(api_key: str = None)
```
- `api_key`: OpenAI API key (optional if set as environment variable)

#### Methods

- `generate_code(description: str, language: str = "python", style: str = "clean") -> Optional[str]`
  - Generate code from description
  - `description`: What the code should do
  - `language`: Programming language
  - `style`: Code style (clean, commented, production, simple)

- `debug_code(code: str, error_message: str = None, language: str = "python") -> Optional[str]`
  - Debug and fix code issues
  - `code`: Code to debug
  - `error_message`: Error message if available
  - `language`: Programming language

- `explain_code(code: str, language: str = "python") -> Optional[str]`
  - Explain what code does
  - `code`: Code to explain
  - `language`: Programming language

- `optimize_code(code: str, language: str = "python", focus: str = "performance") -> Optional[str]`
  - Optimize code for various aspects
  - `code`: Code to optimize
  - `language`: Programming language
  - `focus`: Optimization focus (performance, readability, memory, security)

- `test_code(code: str, language: str = "python") -> Optional[str]`
  - Generate tests for code
  - `code`: Code to test
  - `language`: Programming language

- `convert_code(code: str, from_language: str, to_language: str) -> Optional[str]`
  - Convert code between languages
  - `code`: Code to convert
  - `from_language`: Source language
  - `to_language`: Target language

- `analyze_code_complexity(code: str, language: str = "python") -> Optional[Dict[str, Any]]`
  - Analyze code complexity
  - `code`: Code to analyze
  - `language`: Programming language

- `get_code_history() -> List[Dict[str, Any]]`
  - Get history of all code operations

- `clear_history()`
  - Clear code history

- `save_history(filename: str = None)`
  - Save code history to JSON file

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key

### Supported Languages
- Python, JavaScript, Java, C++, C#, PHP
- Ruby, Go, Rust, Swift, Kotlin, TypeScript

### Code Styles

1. **clean**: Well-structured, minimal code
2. **commented**: Code with helpful comments
3. **production**: Production-ready with error handling
4. **simple**: Easy-to-understand, minimal code

### Optimization Focus

1. **performance**: Speed and efficiency
2. **readability**: Code clarity and maintainability
3. **memory**: Memory usage optimization
4. **security**: Security best practices

## Examples

### Example 1: Code Generation
```
Enter command: generate Create a function to find the longest common subsequence between two strings
💻 Generating code...
✅ Generated code:
def longest_common_subsequence(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]
```

### Example 2: Code Debugging
```
Enter command: debug def factorial(n): return n * factorial(n-1)
🐛 Debugging code...
✅ Debugged code:
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n-1)
```

### Example 3: Code Explanation
```
Enter command: explain def quicksort(arr): return arr if len(arr) <= 1 else quicksort([x for x in arr[1:] if x <= arr[0]]) + [arr[0]] + quicksort([x for x in arr[1:] if x > arr[0]])
📖 Explaining code...
✅ Explanation:
This is a quicksort implementation that:
1. Uses the first element as pivot
2. Recursively sorts elements less than pivot
3. Recursively sorts elements greater than pivot
4. Combines the results
```

### Example 4: Code Optimization
```
Enter command: optimize def fibonacci(n): return n if n < 2 else fibonacci(n-1) + fibonacci(n-2)
⚡ Optimizing code...
✅ Optimized code:
def fibonacci(n):
    if n < 2:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```

### Example 5: Test Generation
```
Enter command: test def add(a, b): return a + b
🧪 Generating tests...
✅ Generated tests:
import unittest

class TestAdd(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add(2, 3), 5)
    
    def test_negative_numbers(self):
        self.assertEqual(add(-1, -2), -3)
    
    def test_zero(self):
        self.assertEqual(add(0, 5), 5)
```

## Best Practices

### Writing Effective Descriptions
1. **Be Specific**: "Create a function to sort a list of objects by a specific property"
2. **Include Requirements**: "Handle edge cases and provide error handling"
3. **Specify Language**: "Write this in Python with type hints"
4. **Mention Style**: "Use clean, production-ready code"

### Code Debugging
1. **Provide Error Messages**: Include actual error messages when available
2. **Describe Expected Behavior**: Explain what the code should do
3. **Include Context**: Provide surrounding code if relevant

### Code Optimization
1. **Choose Focus**: Select the most important optimization target
2. **Consider Trade-offs**: Performance vs readability vs memory
3. **Review Results**: Always test optimized code

## Use Cases

### Development Workflow
- **Rapid Prototyping**: Quickly generate code for new features
- **Bug Fixing**: Automatically identify and fix common issues
- **Code Review**: Get explanations of complex code
- **Refactoring**: Optimize existing code for better performance

### Learning and Education
- **Code Examples**: Generate examples for learning concepts
- **Code Explanation**: Understand unfamiliar codebases
- **Best Practices**: Learn proper coding patterns
- **Language Migration**: Convert code between languages

### Testing and Quality
- **Test Generation**: Create comprehensive test suites
- **Code Analysis**: Assess code quality and complexity
- **Security Review**: Identify potential security issues
- **Performance Optimization**: Improve code efficiency

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Ensure your OpenAI API key is set correctly
   - Check that the key has sufficient credits

2. **Poor Code Quality**
   - Be more specific in your descriptions
   - Try different code styles
   - Provide more context

3. **Language Support**
   - Check if your language is in the supported list
   - Some languages may have better support than others

4. **Complex Code**
   - Break down complex requirements into smaller parts
   - Generate code incrementally
   - Use the explanation feature to understand generated code

## Cost Considerations

- **GPT-3.5-turbo**: ~$0.002 per 1K tokens
- **Typical Code Generation**: 200-500 tokens
- **Cost per Generation**: ~$0.0004-0.001
- **Complex Operations**: May use more tokens
- Monitor usage in OpenAI dashboard

## Contributing

Feel free to contribute to this project by:
- Adding support for more programming languages
- Improving code generation quality
- Enhancing debugging capabilities
- Adding new optimization strategies
- Reporting bugs and issues

## License

This project is open source and available under the MIT License. 