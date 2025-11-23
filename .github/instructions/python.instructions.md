---
applyTo: "**/*.py"
---

# Python-Specific Guidelines for AI_PVSim

## Code Style
- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Use docstrings (Google or NumPy style) for all functions, classes, and modules
- Prefer f-strings for string formatting

## Scientific Computing
- Use NumPy for numerical computations
- Use appropriate libraries for PV simulation (e.g., pvlib-python if applicable)
- Include units in variable names or comments (e.g., `power_w` for watts)
- Validate physical constraints (e.g., efficiency values between 0-1)

## Error Handling
- Use specific exception types rather than bare `except` clauses
- Provide informative error messages
- Validate inputs at function boundaries

## Testing
- Use pytest for testing
- Name test files as `test_*.py`
- Use descriptive test function names: `test_<function>_<scenario>_<expected_result>`
- Include parametrized tests for multiple input scenarios
