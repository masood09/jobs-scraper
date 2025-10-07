# Coding Conventions

This document outlines the coding conventions and best practices for the JobScraper Python project.

## Python Style Guide

We follow [PEP 8](https://pep8.org/) - the official Python style guide.

### Indentation
- Use 4 spaces per indentation level
- No tabs

### Line Length
- Maximum line length: 88 characters (Black-formatted)
- Use parentheses for line continuation when needed

### Imports
- Use absolute imports
- Group imports in the following order:
  1. Standard library imports
  2. Third-party imports
  3. Local application imports
- Use `isort` to automatically format imports

### Naming Conventions
- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_single_leading_underscore`
- **Strongly Private**: `__double_leading_underscore`

### String Quotes
- Use double quotes for docstrings
- Use single quotes for all other strings

## Code Formatting

We use automated tools to maintain consistent code style:

### Black
- Use [Black](https://black.readthedocs.io/) for automatic code formatting
- Run with: `black .`
- Black is opinionated and requires no configuration

### isort
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Run with: `isort .`

### flake8
- Use [flake8](https://flake8.pycqa.org/) for linting
- Run with: `flake8 .`
- Configuration in `.flake8` and `pyproject.toml`
- Focuses on code quality, potential bugs, and complexity
- Black handles formatting, flake8 handles other quality checks

### Configuration Files
- `.flake8` - flake8-specific configuration
- `pyproject.toml` - Unified configuration for Black, isort, and flake8
- Both files are configured to work together harmoniously

## Development Workflow

### Pre-commit Checks
Before committing code, run:
```bash
black .          # Format code
isort .         # Sort imports
flake8 .        # Check for style issues
pytest          # Run tests
```

### IDE Setup
Recommended VS Code extensions:
- Python
- Pylance
- Black Formatter
- isort
- flake8

## Documentation

### Docstrings
Use Google-style docstrings:

```python
def example_function(param1: str, param2: int) -> bool:
    """Short description of the function.

    Longer description with details about what the function does,
    any important considerations, etc.

    Args:
        param1: Description of the first parameter.
        param2: Description of the second parameter.

    Returns:
        Description of the return value.

    Raises:
        ValueError: When something goes wrong.
    """
    # function body
```

### Type Hints
- Use Python type hints for all function parameters and return values
- Helps with static analysis and IDE support

## Testing

### pytest
- Write tests in `tests/` directory
- Use descriptive test function names: `test_<function_name>_<scenario>`
- Use fixtures for common setup/teardown

### Test Structure
```python
def test_function_name_success_case():
    """Test that function works correctly with valid input."""
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

## Error Handling

### Use Specific Exceptions
- Raise specific exceptions rather than generic ones
- Use built-in exceptions when appropriate
- Create custom exceptions for domain-specific errors

### Logging
- Use the built-in `logging` module
- Log at appropriate levels: DEBUG, INFO, WARNING, ERROR, CRITICAL
- Include relevant context in log messages

## Security

### Environment Variables
- Never commit sensitive data to version control
- Use environment variables for configuration
- Use `.env` files for development (add to `.gitignore`)

### Input Validation
- Validate all external inputs
- Use appropriate sanitization for different contexts

## Project Structure

Follow standard Python project structure:
```
project/
├── src/                    # Source code
│   └── package/
├── tests/                  # Test files
├── docs/                   # Documentation
├── requirements/           # Dependency files
└── scripts/               # Utility scripts
```

## Commit Messages

Use conventional commit messages:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test-related changes
- `chore:` Maintenance tasks

Example: `feat: add authentication middleware`

## Code Review

- Review all code changes before merging
- Focus on functionality, readability, and maintainability
- Ensure tests are included for new features
- Check for security considerations

## Dependencies

- Use `requirements.txt` files for dependency management
- Pin specific versions for production
- Keep dependencies updated regularly
- Use dependabot or similar tools for dependency updates

## Performance

- Write efficient code, but prioritize readability
- Use appropriate data structures
- Profile code before optimizing
- Consider caching for expensive operations

This document should be updated as the project evolves and new conventions are established.
