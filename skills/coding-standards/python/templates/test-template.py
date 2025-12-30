"""pytest test template with common patterns and fixtures.

This template demonstrates pytest best practices including:
- Fixture organization (conftest.py patterns)
- Parametrized tests
- Mocking with unittest.mock
- Async testing
- Test markers
- Custom assertions
"""

import asyncio
from collections.abc import Generator
from unittest.mock import AsyncMock, Mock, patch

import pytest


# ============================================================================
# FIXTURES
# ============================================================================


@pytest.fixture
def sample_user() -> dict:
    """Create sample user data for testing.

    Returns:
        Dict with user properties
    """
    return {"id": 1, "username": "testuser", "email": "test@example.com", "is_active": True}


@pytest.fixture
def mock_database() -> Generator[Mock, None, None]:
    """Mock database connection with cleanup.

    Yields:
        Mock database object
    """
    db = Mock()
    db.connect.return_value = True
    db.query.return_value = []

    yield db

    # Cleanup
    db.close()


@pytest.fixture
def mock_http_client() -> Mock:
    """Mock HTTP client for API testing.

    Yields:
        Mock HTTP client
    """
    client = Mock()
    client.get.return_value = Mock(status_code=200, json=lambda: {"data": "test"})

    return client


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# BASIC TESTS
# ============================================================================


def test_basic_assertion(sample_user):
    """Test basic assertions with fixture."""
    assert sample_user["username"] == "testuser"
    assert sample_user["is_active"] is True
    assert "email" in sample_user


def test_exception_raised():
    """Test that function raises expected exception."""
    with pytest.raises(ValueError, match="Invalid input"):
        raise ValueError("Invalid input")


def test_multiple_assertions(sample_user):
    """Test multiple related assertions."""
    # Given
    user = sample_user

    # When
    username = user["username"]

    # Then
    assert username is not None
    assert len(username) > 0
    assert username.islower()


# ============================================================================
# PARAMETRIZED TESTS
# ============================================================================


@pytest.mark.parametrize(
    "input,expected",
    [
        ("hello", "HELLO"),
        ("World", "WORLD"),
        ("123", "123"),
        ("", ""),
    ],
)
def test_string_upper(input: str, expected: str):
    """Test string upper conversion with multiple inputs."""
    result = input.upper()
    assert result == expected


@pytest.mark.parametrize(
    "username,email,is_valid",
    [
        ("user1", "user1@example.com", True),
        ("u", "invalid", False),  # Too short, invalid email
        ("", "test@example.com", False),  # Empty username
        ("validuser", "invalid-email", False),  # Invalid email
    ],
)
def test_user_validation(username: str, email: str, is_valid: bool):
    """Test user validation with various inputs."""
    # This would call your actual validation function
    # result = validate_user(username, email)
    # assert result == is_valid


# ============================================================================
# MOCKING
# ============================================================================


def test_mock_function_call():
    """Test function call with mock."""
    mock_func = Mock(return_value=42)

    result = mock_func(1, 2, 3)

    assert result == 42
    mock_func.assert_called_once_with(1, 2, 3)


def test_mock_side_effect():
    """Test mock with side effects."""
    mock_func = Mock(side_effect=[1, 2, 3])

    assert mock_func() == 1
    assert mock_func() == 2
    assert mock_func() == 3


@patch("builtins.open", create=True)
def test_file_operations(mock_open):
    """Test file operations with mocked open."""
    mock_open.return_value.__enter__.return_value.read.return_value = "test data"

    with open("test.txt") as f:
        content = f.read()

    assert content == "test data"
    mock_open.assert_called_once_with("test.txt")


def test_database_query(mock_database):
    """Test database operations with mock."""
    # Setup
    mock_database.query.return_value = [{"id": 1, "name": "Test"}]

    # Execute
    results = mock_database.query("SELECT * FROM users")

    # Verify
    assert len(results) == 1
    assert results[0]["name"] == "Test"
    mock_database.query.assert_called_once()


# ============================================================================
# ASYNC TESTS
# ============================================================================


@pytest.mark.asyncio
async def test_async_function():
    """Test async function."""

    async def async_add(a: int, b: int) -> int:
        await asyncio.sleep(0.1)
        return a + b

    result = await async_add(1, 2)
    assert result == 3


@pytest.mark.asyncio
async def test_async_with_mock():
    """Test async function with AsyncMock."""
    mock_async_func = AsyncMock(return_value="async result")

    result = await mock_async_func()

    assert result == "async result"
    mock_async_func.assert_called_once()


# ============================================================================
# MARKERS
# ============================================================================


@pytest.mark.slow
def test_slow_operation():
    """Test marked as slow (can be skipped with -m "not slow")."""
    import time

    time.sleep(0.5)
    assert True


@pytest.mark.integration
def test_integration_with_database(mock_database):
    """Test marked as integration test."""
    mock_database.connect()
    result = mock_database.query("SELECT 1")
    assert mock_database.connect.called


@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    """Test skipped until feature is implemented."""


@pytest.mark.skipif(pytest.__version__ < "7.0", reason="Requires pytest 7.0+")
def test_new_pytest_feature():
    """Test skipped on older pytest versions."""


# ============================================================================
# FIXTURES WITH CLEANUP
# ============================================================================


@pytest.fixture
def temp_file(tmp_path):
    """Create temporary file for testing.

    Args:
        tmp_path: pytest's built-in tmp_path fixture

    Yields:
        Path to temporary file
    """
    file_path = tmp_path / "test.txt"
    file_path.write_text("initial content")

    yield file_path

    # Cleanup (if needed, pytest cleans tmp_path automatically)
    if file_path.exists():
        file_path.unlink()


def test_temp_file_operations(temp_file):
    """Test file operations with temporary file."""
    content = temp_file.read_text()
    assert content == "initial content"

    temp_file.write_text("modified content")
    assert temp_file.read_text() == "modified content"


# ============================================================================
# CUSTOM ASSERTIONS
# ============================================================================


def assert_user_valid(user: dict):
    """Custom assertion for user validation.

    Args:
        user: User dict to validate

    Raises:
        AssertionError: If user is invalid
    """
    assert "id" in user, "User must have id"
    assert "username" in user, "User must have username"
    assert "email" in user, "User must have email"
    assert "@" in user["email"], "Email must be valid"


def test_custom_assertion(sample_user):
    """Test using custom assertion."""
    assert_user_valid(sample_user)


# ============================================================================
# ERROR HANDLING
# ============================================================================


def test_error_message_contains_text():
    """Test that error message contains expected text."""
    with pytest.raises(ValueError) as exc_info:
        raise ValueError("Invalid user ID: 123")

    assert "Invalid user ID" in str(exc_info.value)
    assert "123" in str(exc_info.value)


def test_no_exception_raised():
    """Test that no exception is raised."""
    try:
        result = 1 + 1
        assert result == 2
    except Exception as e:
        pytest.fail(f"Unexpected exception: {e}")


# ============================================================================
# SETUP/TEARDOWN
# ============================================================================


class TestUserService:
    """Test class with setup/teardown methods."""

    def setup_method(self):
        """Setup before each test method."""
        self.user_service = Mock()
        self.test_user = {"id": 1, "name": "Test"}

    def teardown_method(self):
        """Cleanup after each test method."""
        self.user_service = None
        self.test_user = None

    def test_get_user(self):
        """Test get_user method."""
        self.user_service.get_user.return_value = self.test_user

        result = self.user_service.get_user(1)

        assert result == self.test_user

    def test_create_user(self):
        """Test create_user method."""
        self.user_service.create_user.return_value = self.test_user

        result = self.user_service.create_user({"name": "Test"})

        assert result["id"] == 1


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_module.py

# Run specific test
pytest tests/test_module.py::test_function

# Run tests matching pattern
pytest -k "test_user"

# Run with coverage
pytest --cov=src --cov-report=html

# Run marked tests
pytest -m "not slow"  # Skip slow tests
pytest -m integration  # Only integration tests

# Run with output
pytest -s  # Show print statements

# Stop at first failure
pytest -x

# Run last failed tests
pytest --lf

# Parallel execution
pytest -n auto  # Requires pytest-xdist
"""
