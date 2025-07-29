# Contributing to AI Projects Collection

Thank you for your interest in contributing to the AI Projects Collection! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please:

1. **Check existing issues** to see if your problem has already been reported
2. **Search the documentation** to see if your question is already answered
3. **Provide detailed information** when creating a new issue

When creating an issue, please include:

- **Clear description** of the problem
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Error messages** or logs if applicable

### Suggesting Features

We welcome feature suggestions! When suggesting a feature:

1. **Describe the feature** clearly and concisely
2. **Explain the use case** and why it would be valuable
3. **Provide examples** of how it would work
4. **Consider implementation** complexity and impact

### Code Contributions

#### Before You Start

1. **Fork the repository** to your GitHub account
2. **Clone your fork** to your local machine
3. **Create a new branch** for your changes
4. **Set up the development environment**

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/ai-projects-collection.git
cd ai-projects-collection

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8 mypy
```

#### Making Changes

1. **Follow the coding style** (see Style Guide below)
2. **Write tests** for new functionality
3. **Update documentation** as needed
4. **Test your changes** thoroughly

#### Code Style Guide

We follow PEP 8 with some modifications:

- **Line length**: 88 characters (Black default)
- **Import organization**: Use isort
- **Type hints**: Use type hints for all functions
- **Docstrings**: Use Google-style docstrings
- **Comments**: Write clear, helpful comments

Example:

```python
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)


def process_data(data: List[str], config: Optional[Dict[str, Any]] = None) -> List[str]:
    """Process a list of data items according to configuration.
    
    Args:
        data: List of data items to process
        config: Optional configuration dictionary
        
    Returns:
        Processed list of data items
        
    Raises:
        ValueError: If data is empty or invalid
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    # Process each item
    processed = []
    for item in data:
        processed_item = _process_single_item(item, config)
        processed.append(processed_item)
    
    return processed


def _process_single_item(item: str, config: Optional[Dict[str, Any]]) -> str:
    """Process a single data item."""
    # Implementation here
    return item.upper()
```

#### Testing

- **Write unit tests** for all new functionality
- **Maintain test coverage** above 80%
- **Run tests locally** before submitting
- **Include integration tests** for complex features

Example test:

```python
import pytest
from your_module import process_data


def test_process_data_empty_list():
    """Test that empty list raises ValueError."""
    with pytest.raises(ValueError, match="Data cannot be empty"):
        process_data([])


def test_process_data_basic():
    """Test basic data processing."""
    data = ["hello", "world"]
    result = process_data(data)
    assert result == ["HELLO", "WORLD"]


def test_process_data_with_config():
    """Test data processing with configuration."""
    data = ["test"]
    config = {"uppercase": False}
    result = process_data(data, config)
    assert result == ["test"]
```

#### Documentation

- **Update README.md** if adding new features
- **Add docstrings** to all new functions and classes
- **Update API documentation** if changing interfaces
- **Include usage examples** for new features

### Submitting Changes

#### Pull Request Process

1. **Push your changes** to your fork
2. **Create a pull request** with a clear description
3. **Link any related issues** in the PR description
4. **Wait for review** and address feedback

#### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test addition/update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes (or documented if necessary)
- [ ] Self-review completed

## Additional Notes
Any additional information or context.
```

## 🏗️ Project Structure

```
ai-projects-collection/
├── README.md                    # Main project documentation
├── LICENSE                      # MIT License
├── CONTRIBUTING.md             # This file
├── requirements.txt             # Main dependencies
├── .gitignore                  # Git ignore rules
├── evaluate_ai_projects.py     # Repository quality evaluator
├── repository_quality_checklist.md  # Quality checklist
├── ai_chat_assistant/          # Chat assistant project
├── ai_image_generator/         # Image generator project
├── ai_text_summarizer/         # Text summarizer project
├── ai_sentiment_analyzer/      # Sentiment analyzer project
└── ai_code_assistant/          # Code assistant project
```

## 🧪 Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_chat_assistant.py

# Run tests with verbose output
pytest -v
```

### Test Structure

```
tests/
├── test_chat_assistant.py
├── test_image_generator.py
├── test_text_summarizer.py
├── test_sentiment_analyzer.py
└── test_code_assistant.py
```

## 🔧 Development Tools

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports with isort
isort .

# Check code style with flake8
flake8 .
```

### Type Checking

```bash
# Run mypy for type checking
mypy .
```

### Pre-commit Hooks

We recommend setting up pre-commit hooks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install
```

## 📋 Issue Templates

### Bug Report Template

```markdown
## Bug Description
Clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. Step 3

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- OS: [e.g., Windows 10, macOS 12.1]
- Python Version: [e.g., 3.9.7]
- Package Version: [e.g., 1.2.3]

## Additional Context
Any other context about the problem.
```

### Feature Request Template

```markdown
## Feature Description
Clear description of the feature.

## Use Case
Why this feature would be useful.

## Proposed Implementation
How you think this could be implemented.

## Alternatives Considered
Other approaches you considered.

## Additional Context
Any other context or examples.
```

## 🎯 Contribution Areas

We welcome contributions in these areas:

### High Priority
- **Bug fixes** and error handling improvements
- **Documentation** updates and clarifications
- **Test coverage** improvements
- **Performance** optimizations

### Medium Priority
- **New features** for existing projects
- **Code refactoring** and cleanup
- **Additional AI models** integration
- **UI/UX improvements**

### Low Priority
- **New project ideas** (create separate repository)
- **Experimental features**
- **Cosmetic changes**

## 📞 Getting Help

If you need help with contributing:

1. **Check the documentation** first
2. **Search existing issues** for similar problems
3. **Ask in discussions** if available
4. **Create an issue** for complex problems

## 🙏 Recognition

Contributors will be recognized in:

- **README.md** contributors section
- **Release notes** for significant contributions
- **GitHub contributors** page

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the AI Projects Collection! 🚀 