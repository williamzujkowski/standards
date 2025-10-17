# Sample Coding Standard

**Version:** 1.0.0
**Standard Code:** CS-001
**Last Updated:** 2025-01-01

## Overview

This is a sample standard document for testing migration functionality.
It contains typical structure found in standards documents.

## Core Principles

- Write clean code
- Follow conventions
- Test thoroughly
- Document properly
- Review regularly

## Code Style

### Naming Conventions

Use descriptive names for variables and functions:

```python
# Good
def calculate_total_price(items):
    return sum(item.price for item in items)

# Bad
def calc(x):
    return sum(i.p for i in x)
```

### Formatting

- Use consistent indentation (4 spaces)
- Limit line length to 80 characters
- Add blank lines between functions

## Testing Requirements

### Unit Tests

All functions must have unit tests:

```python
def test_calculate_total_price():
    items = [Item(price=10), Item(price=20)]
    assert calculate_total_price(items) == 30
```

### Integration Tests

Test end-to-end workflows.

## Documentation

- Add docstrings to all public functions
- Include examples in documentation
- Keep README files updated

## Common Pitfalls

- Not writing tests first
- Ignoring code review feedback
- Inconsistent naming
- Poor error handling

## Resources

- [PEP 8](https://peps.python.org/pep-0008/)
- [Clean Code](https://example.com/clean-code)
- [Testing Guide](https://example.com/testing)

## Advanced Topics

### Performance Optimization

Optimize after profiling, not before.

### Security Considerations

Validate all inputs and sanitize outputs.

## References

See also:
- Internal coding guidelines
- Team best practices
