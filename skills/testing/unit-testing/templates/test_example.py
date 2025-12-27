"""
Unit Testing Examples - Python/pytest

This module demonstrates best practices for writing unit tests with pytest,
including fixtures, parametrization, mocking, and async testing.

@see https://docs.pytest.org/
"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest


# ===== Example Code Under Test =====


class Calculator:
    """Simple calculator for demonstration purposes"""

    def add(self, a: int, b: int) -> int:
        return a + b

    def subtract(self, a: int, b: int) -> int:
        return a - b

    def divide(self, a: int, b: int) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def multiply(self, a: int, b: int) -> int:
        return a * b


class User:
    """User model for demonstration"""

    def __init__(self, user_id: int, name: str, email: str, is_active: bool = True):
        self.id = user_id
        self.name = name
        self.email = email
        self.is_active = is_active

    def deactivate(self) -> None:
        self.is_active = False

    def get_display_name(self) -> str:
        return f"{self.name} ({self.email})"


class UserRepository:
    """Repository for user data access"""

    def __init__(self, database_connection):
        self.db = database_connection

    def get_user_by_id(self, user_id: int) -> User:
        # Simulated database query
        result = self.db.query(f"SELECT * FROM users WHERE id = {user_id}")
        return User(**result)

    def save_user(self, user: User) -> bool:
        # Simulated database save
        return self.db.execute(f"INSERT INTO users VALUES {user.id}")


class EmailService:
    """Email service for sending notifications"""

    async def send_email(self, to: str, subject: str, body: str) -> bool:
        # Simulated async email sending
        await asyncio.sleep(0.1)  # Simulate network delay
        return True


# ===== Test Fixtures =====


@pytest.fixture
def calculator():
    """Fixture that provides a Calculator instance"""
    return Calculator()


@pytest.fixture
def mock_database():
    """Fixture that provides a mock database connection"""
    mock_db = Mock()
    mock_db.query.return_value = {"user_id": 1, "name": "Alice", "email": "alice@example.com", "is_active": True}
    mock_db.execute.return_value = True
    return mock_db


@pytest.fixture
def user_repository(mock_database):
    """Fixture that provides a UserRepository with mocked database"""
    return UserRepository(mock_database)


@pytest.fixture
def sample_user():
    """Fixture that provides a sample User instance"""
    return User(user_id=1, name="Alice", email="alice@example.com")


@pytest.fixture(scope="module")
def email_service():
    """Module-scoped fixture for email service (shared across tests in module)"""
    return EmailService()


@pytest.fixture(autouse=True)
def reset_state():
    """Fixture that runs automatically before each test to reset state"""
    # Setup (runs before each test)
    return
    # Teardown (runs after each test)


# ===== Basic Unit Tests =====


def test_calculator_add(calculator):
    """Test that calculator correctly adds two numbers"""
    result = calculator.add(2, 3)
    assert result == 5


def test_calculator_subtract(calculator):
    """Test that calculator correctly subtracts two numbers"""
    result = calculator.subtract(10, 3)
    assert result == 7


def test_calculator_multiply(calculator):
    """Test that calculator correctly multiplies two numbers"""
    result = calculator.multiply(4, 5)
    assert result == 20


def test_calculator_divide(calculator):
    """Test that calculator correctly divides two numbers"""
    result = calculator.divide(10, 2)
    assert result == 5.0


def test_calculator_divide_by_zero(calculator):
    """Test that calculator raises ValueError when dividing by zero"""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        calculator.divide(10, 0)


# ===== Parametrized Tests =====


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300),
        (-5, -3, -8),
    ],
)
def test_calculator_add_parametrized(calculator, a, b, expected):
    """Parametrized test for addition with multiple test cases"""
    result = calculator.add(a, b)
    assert result == expected


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (10, 2, 5.0),
        (100, 10, 10.0),
        (7, 2, 3.5),
        (-10, 2, -5.0),
    ],
)
def test_calculator_divide_parametrized(calculator, a, b, expected):
    """Parametrized test for division with multiple test cases"""
    result = calculator.divide(a, b)
    assert result == expected


@pytest.mark.parametrize("divisor", [0, 0.0, -0])
def test_calculator_divide_by_zero_parametrized(calculator, divisor):
    """Parametrized test for division by zero"""
    with pytest.raises(ValueError):
        calculator.divide(10, divisor)


# ===== Mocking Tests =====


def test_user_repository_get_user(user_repository, mock_database):
    """Test that user repository correctly retrieves a user from database"""
    user = user_repository.get_user_by_id(1)

    # Verify database was queried
    mock_database.query.assert_called_once_with("SELECT * FROM users WHERE id = 1")

    # Verify user data
    assert user.id == 1
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.is_active is True


def test_user_repository_save_user(user_repository, mock_database, sample_user):
    """Test that user repository correctly saves a user to database"""
    result = user_repository.save_user(sample_user)

    # Verify database execute was called
    mock_database.execute.assert_called_once()

    # Verify result
    assert result is True


@patch("builtins.print")
def test_user_display_name_with_patch(mock_print, sample_user):
    """Test using patch decorator to mock built-in functions"""
    display_name = sample_user.get_display_name()

    assert display_name == "Alice (alice@example.com)"


# ===== Async Tests =====


@pytest.mark.asyncio
async def test_email_service_send_email(email_service):
    """Test that email service successfully sends an email"""
    result = await email_service.send_email(to="alice@example.com", subject="Test Subject", body="Test Body")

    assert result is True


@pytest.mark.asyncio
async def test_email_service_send_email_with_mock():
    """Test email service with a mock"""
    mock_email_service = AsyncMock(spec=EmailService)
    mock_email_service.send_email.return_value = True

    result = await mock_email_service.send_email(to="test@example.com", subject="Test", body="Test")

    assert result is True
    mock_email_service.send_email.assert_awaited_once()


# ===== Test Markers =====


@pytest.mark.slow
def test_slow_operation():
    """Test marked as slow (can be skipped with pytest -m "not slow")"""
    import time

    time.sleep(0.5)
    assert True


@pytest.mark.skip(reason="Feature not implemented yet")
def test_unimplemented_feature():
    """Test that is skipped"""
    assert False


@pytest.mark.skipif(pytest.__version__ < "7.0", reason="Requires pytest 7.0+")
def test_new_pytest_feature():
    """Test that is conditionally skipped based on pytest version"""
    assert True


@pytest.mark.xfail(reason="Known bug - will be fixed in next release")
def test_known_bug():
    """Test that is expected to fail"""
    assert False


# ===== Test Classes (Grouping Related Tests) =====


class TestUser:
    """Group of tests for User class"""

    def test_user_creation(self):
        """Test that user can be created with correct attributes"""
        user = User(user_id=1, name="Bob", email="bob@example.com")

        assert user.id == 1
        assert user.name == "Bob"
        assert user.email == "bob@example.com"
        assert user.is_active is True

    def test_user_deactivate(self, sample_user):
        """Test that user can be deactivated"""
        sample_user.deactivate()

        assert sample_user.is_active is False

    def test_user_display_name(self, sample_user):
        """Test that user display name is formatted correctly"""
        display_name = sample_user.get_display_name()

        assert display_name == "Alice (alice@example.com)"

    @pytest.mark.parametrize(
        "user_id, name, email",
        [
            (1, "Alice", "alice@example.com"),
            (2, "Bob", "bob@example.com"),
            (3, "Charlie", "charlie@example.com"),
        ],
    )
    def test_user_creation_parametrized(self, user_id, name, email):
        """Parametrized test for user creation"""
        user = User(user_id=user_id, name=name, email=email)

        assert user.id == user_id
        assert user.name == name
        assert user.email == email


# ===== Advanced: Context Managers and Cleanup =====


@pytest.fixture
def temp_file(tmp_path):
    """Fixture that creates a temporary file and cleans up after test"""
    file_path = tmp_path / "test_file.txt"
    file_path.write_text("test content")

    yield file_path

    # Cleanup (if needed, though pytest handles tmp_path cleanup)
    if file_path.exists():
        file_path.unlink()


def test_with_temp_file(temp_file):
    """Test that uses a temporary file"""
    content = temp_file.read_text()
    assert content == "test content"


# ===== Coverage and Test Quality Tips =====
#
# 1. Aim for >80% code coverage (use pytest-cov plugin):
#    pytest --cov=mymodule --cov-report=html
#
# 2. Use descriptive test names that explain what is being tested
#
# 3. Follow AAA pattern: Arrange, Act, Assert
#
# 4. Keep tests independent (no shared state between tests)
#
# 5. Use fixtures for reusable test setup
#
# 6. Parametrize tests to avoid code duplication
#
# 7. Mock external dependencies (databases, APIs, etc.)
#
# 8. Test edge cases and error conditions
#
# 9. Use markers to organize and selectively run tests
#
# 10. Keep tests fast (mock slow operations)
