---
name: unit-testing
description: Unit testing standards following TDD methodology, test pyramid principles, and comprehensive coverage practices. Covers pytest, Jest, mocking, fixtures, and CI integration for reliable test suites.
---

# Unit Testing Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Test-Driven Development (TDD)**: Write tests before implementation (Red-Green-Refactor)
2. **Test Pyramid**: 70% unit tests, 20% integration, 10% E2E
3. **Fast and Isolated**: Tests run in milliseconds, no external dependencies
4. **Comprehensive Coverage**: Aim for 80-90% code coverage minimum
5. **Clear and Maintainable**: Tests serve as living documentation

### Essential Checklist

- [ ] **TDD workflow**: Write failing test → Implement → Refactor
- [ ] **Coverage targets**: 80%+ overall, 95%+ for critical paths
- [ ] **Naming convention**: `test_<function>_<scenario>_<expected_result>`
- [ ] **AAA pattern**: Arrange, Act, Assert structure in every test
- [ ] **Mocking**: Mock external dependencies (database, APIs, filesystem)
- [ ] **Fixtures**: Reusable test data and setup/teardown
- [ ] **Parametrized tests**: Test multiple inputs efficiently
- [ ] **CI integration**: Tests run automatically on every commit

### Quick Example

```python
# pytest unit testing example
import pytest
from datetime import datetime

def calculate_discount(user_age: int, purchase_amount: float) -> float:
    """Calculate discount based on age and purchase amount."""
    if user_age < 18:
        return 0.0
    elif user_age >= 65:
        return purchase_amount * 0.15
    elif purchase_amount >= 100:
        return purchase_amount * 0.10
    return 0.0

# Unit tests following TDD
def test_calculate_discount_no_discount_for_minors():
    """Test that users under 18 receive no discount."""
    # Arrange
    user_age = 16
    purchase_amount = 100.0

    # Act
    discount = calculate_discount(user_age, purchase_amount)

    # Assert
    assert discount == 0.0

def test_calculate_discount_senior_discount():
    """Test that seniors (65+) receive 15% discount."""
    assert calculate_discount(65, 100.0) == 15.0
    assert calculate_discount(70, 200.0) == 30.0

def test_calculate_discount_large_purchase():
    """Test that purchases >= $100 receive 10% discount."""
    assert calculate_discount(30, 100.0) == 10.0
    assert calculate_discount(30, 150.0) == 15.0

@pytest.mark.parametrize("age,amount,expected", [
    (16, 100, 0.0),   # Minor
    (30, 50, 0.0),    # No discount
    (30, 100, 10.0),  # Large purchase
    (65, 50, 7.5),    # Senior
    (70, 200, 30.0),  # Senior large purchase
])
def test_calculate_discount_parametrized(age, amount, expected):
    """Test multiple discount scenarios."""
    assert calculate_discount(age, amount) == expected
```

### Quick Links to Level 2

- [TDD Workflow](#tdd-workflow)
- [Test Organization](#test-organization)
- [Mocking and Fixtures](#mocking-and-fixtures)
- [Coverage Analysis](#coverage-analysis)
- [Best Practices](#best-practices)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### TDD Workflow

**Red-Green-Refactor Cycle** (see [resources/tdd-workflow.md](resources/tdd-workflow.md))

```python
# Step 1: RED - Write failing test
def test_user_authentication_success():
    """Test successful user authentication."""
    auth_service = AuthenticationService()
    result = auth_service.authenticate('user@example.com', 'password123')
    assert result.success is True
    assert result.token is not None

# Step 2: GREEN - Write minimum code to pass
class AuthenticationService:
    def authenticate(self, email: str, password: str):
        # Minimal implementation
        return AuthResult(success=True, token='dummy_token')

# Step 3: REFACTOR - Improve implementation
class AuthenticationService:
    def __init__(self, user_repository, token_generator):
        self.user_repo = user_repository
        self.token_gen = token_generator

    def authenticate(self, email: str, password: str):
        user = self.user_repo.find_by_email(email)
        if not user or not user.verify_password(password):
            return AuthResult(success=False, error='Invalid credentials')

        token = self.token_gen.generate(user.id)
        return AuthResult(success=True, token=token)
```

### Test Organization

**Test Structure** (see [templates/test-template-pytest.py](templates/test-template-pytest.py))

```python
# tests/test_user_service.py
import pytest
from unittest.mock import Mock, MagicMock
from app.services.user_service import UserService
from app.models.user import User

@pytest.fixture
def mock_database():
    """Create mock database connection."""
    db = Mock()
    db.query = MagicMock(return_value=[])
    return db

@pytest.fixture
def user_service(mock_database):
    """Create UserService with mocked dependencies."""
    return UserService(database=mock_database)

class TestUserService:
    """Test suite for UserService."""

    def test_create_user_success(self, user_service, mock_database):
        """Test successful user creation."""
        # Arrange
        user_data = {'email': 'test@example.com', 'name': 'Test User'}
        mock_database.insert = MagicMock(return_value=1)

        # Act
        user_id = user_service.create_user(user_data)

        # Assert
        assert user_id == 1
        mock_database.insert.assert_called_once()

    def test_create_user_duplicate_email(self, user_service, mock_database):
        """Test user creation fails with duplicate email."""
        # Arrange
        user_data = {'email': 'existing@example.com', 'name': 'Test'}
        mock_database.find_by_email = MagicMock(return_value=User(id=1))

        # Act & Assert
        with pytest.raises(DuplicateEmailError):
            user_service.create_user(user_data)
```

### Mocking and Fixtures

**Advanced Mocking** (see [templates/test-mocking-examples.py](templates/test-mocking-examples.py))

```python
from unittest.mock import Mock, patch, MagicMock
import pytest

# Mock external API calls
@patch('requests.get')
def test_fetch_user_data(mock_get):
    """Test fetching user data from external API."""
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = {'id': 1, 'name': 'John'}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    service = ExternalAPIService()
    user_data = service.fetch_user(1)

    # Assert
    assert user_data['name'] == 'John'
    mock_get.assert_called_once_with('https://api.example.com/users/1')

# Mock database operations
@pytest.fixture
def mock_db_session():
    """Create mock database session."""
    session = MagicMock()
    session.query = MagicMock()
    session.add = MagicMock()
    session.commit = MagicMock()
    return session

def test_save_user(mock_db_session):
    """Test saving user to database."""
    repository = UserRepository(session=mock_db_session)
    user = User(name='Test', email='test@example.com')

    repository.save(user)

    mock_db_session.add.assert_called_once_with(user)
    mock_db_session.commit.assert_called_once()
```

### Coverage Analysis

**Coverage Configuration** (see [resources/configs/pytest.ini](resources/configs/pytest.ini))

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --verbose
    --cov=src
    --cov-report=term-missing
    --cov-report=html
    --cov-report=xml
    --cov-fail-under=80

[coverage:run]
source = src
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    */site-packages/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

**Running Coverage**

```bash
# Run tests with coverage
pytest --cov=src tests/

# Generate HTML report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html

# Coverage for specific module
pytest --cov=src.services.user_service tests/test_user_service.py
```

### Best Practices

**Test Naming and Organization**

```python
# ✅ Good: Descriptive test names
def test_calculate_total_with_discount_applies_10_percent_for_loyalty_members():
    """Test that loyalty members receive 10% discount on total."""
    pass

# ❌ Bad: Vague test names
def test_calculate():
    pass

# ✅ Good: Group related tests
class TestUserAuthentication:
    def test_successful_login(self):
        pass

    def test_failed_login_invalid_password(self):
        pass

    def test_failed_login_nonexistent_user(self):
        pass

# ✅ Good: Test one thing
def test_user_creation_generates_unique_id():
    user = create_user('test@example.com')
    assert isinstance(user.id, str)
    assert len(user.id) == 36  # UUID length

# ❌ Bad: Testing multiple things
def test_user_creation():
    user = create_user('test@example.com')
    assert user.id is not None
    assert user.email == 'test@example.com'
    assert user.created_at is not None
    assert user.is_active is True  # Too many assertions
```

**Parameterized Testing**

```python
@pytest.mark.parametrize("input_value,expected_output", [
    (0, 0),
    (1, 1),
    (2, 4),
    (3, 9),
    (10, 100),
])
def test_square_function(input_value, expected_output):
    """Test square function with multiple inputs."""
    assert square(input_value) == expected_output

@pytest.mark.parametrize("email", [
    "invalid.email",
    "@example.com",
    "user@",
    "user @example.com",
    "",
])
def test_email_validation_rejects_invalid(email):
    """Test email validation rejects invalid formats."""
    with pytest.raises(ValidationError):
        validate_email(email)
```

### JavaScript/Jest Testing

**Jest Configuration** (see [resources/configs/jest.config.js](resources/configs/jest.config.js))

```javascript
// jest.config.js
module.exports = {
  testEnvironment: 'node',
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,jsx}',
    '!src/**/*.test.{js,jsx}',
    '!src/index.js'
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },
  testMatch: ['**/__tests__/**/*.js', '**/?(*.)+(spec|test).js']
};
```

**Jest Testing Example** (see [templates/test-template-jest.js](templates/test-template-jest.js))

```javascript
// src/calculator.test.js
const { add, subtract, divide } = require('./calculator');

describe('Calculator', () => {
  describe('add', () => {
    test('should add two positive numbers', () => {
      expect(add(2, 3)).toBe(5);
    });

    test('should add negative numbers', () => {
      expect(add(-2, -3)).toBe(-5);
    });
  });

  describe('divide', () => {
    test('should divide two numbers', () => {
      expect(divide(10, 2)).toBe(5);
    });

    test('should throw error when dividing by zero', () => {
      expect(() => divide(10, 0)).toThrow('Division by zero');
    });
  });
});

// Mock testing
jest.mock('./apiService');
const apiService = require('./apiService');

test('fetches user data successfully', async () => {
  const mockUser = { id: 1, name: 'John' };
  apiService.getUser.mockResolvedValue(mockUser);

  const user = await fetchUser(1);

  expect(user).toEqual(mockUser);
  expect(apiService.getUser).toHaveBeenCalledWith(1);
});
```

### Go Testing

**Go Test Template** (see [templates/test-template-go.go](templates/test-template-go.go))

```go
// calculator_test.go
package calculator

import (
    "testing"
)

func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive numbers", 2, 3, 5},
        {"negative numbers", -2, -3, -5},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}

func TestDivide(t *testing.T) {
    result, err := Divide(10, 2)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if result != 5 {
        t.Errorf("got %d, want 5", result)
    }
}

func TestDivideByZero(t *testing.T) {
    _, err := Divide(10, 0)
    if err == nil {
        t.Error("expected error for division by zero")
    }
}
```

---

## Level 3: Mastery Resources

### Advanced Topics

- **[Property-Based Testing](resources/property-based-testing.md)**: Hypothesis, QuickCheck
- **[Mutation Testing](resources/mutation-testing.md)**: Verify test quality
- **[Test Doubles](resources/test-doubles.md)**: Mocks, stubs, spies, fakes

### Templates & Examples

- **[pytest Template](templates/test-template-pytest.py)**: Complete pytest example
- **[Jest Template](templates/test-template-jest.js)**: Jest with mocks
- **[Go Template](templates/test-template-go.go)**: Table-driven tests

### Configuration Files

- **[pytest.ini](resources/configs/pytest.ini)**: pytest configuration
- **[jest.config.js](resources/configs/jest.config.js)**: Jest configuration
- **[.coveragerc](resources/coverage-configs/.coveragerc)**: Coverage config

### Related Skills

- [Integration Testing](../integration-testing/SKILL.md) - API and database testing
- [Secrets Management](../../security/secrets-management/SKILL.md) - Test security

---

## Quick Reference Commands

```bash
# pytest
pytest                          # Run all tests
pytest tests/test_user.py       # Run specific file
pytest -k "test_auth"           # Run tests matching pattern
pytest --cov=src --cov-report=html  # Coverage report
pytest -v -s                    # Verbose with stdout
pytest --tb=short               # Short traceback

# Jest
npm test                        # Run all tests
npm test -- --coverage          # With coverage
npm test -- --watch             # Watch mode
npm test -- user.test.js        # Specific file

# Go
go test ./...                   # All packages
go test -v                      # Verbose
go test -cover                  # Coverage
go test -bench=.                # Benchmarks
```

---

## Examples

### Basic Usage

```python
// TODO: Add basic example for unit-testing
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for unit-testing
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how unit-testing
// works with other systems and services
```

See `examples/unit-testing/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: pytest, Jest, Go test, unittest
- **Prerequisites**: Basic understanding of testing concepts

### Downstream Consumers

- **Applications**: Production systems requiring unit-testing functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- [Integration Testing](../../integration-testing/SKILL.md)
- [E2E Testing](../../e2e-testing/SKILL.md)
- [Ci Cd](../../ci-cd/SKILL.md)

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for unit-testing
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

## Validation

- ✅ Token count: Level 1 <2,000, Level 2 <5,000
- ✅ TDD workflow: Complete Red-Green-Refactor cycle
- ✅ Coverage: 80-90% minimum standards
- ✅ Code examples: Python, JavaScript, Go
