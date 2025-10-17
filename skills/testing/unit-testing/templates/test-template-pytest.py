"""pytest unit test template with fixtures and mocking."""

from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest


# Fixtures
@pytest.fixture
def sample_user():
    """Create sample user for testing."""
    return {"id": 1, "email": "test@example.com", "name": "Test User", "created_at": datetime(2024, 1, 1)}


@pytest.fixture
def mock_database():
    """Create mock database connection."""
    db = Mock()
    db.query = MagicMock(return_value=[])
    db.insert = MagicMock(return_value=1)
    db.update = MagicMock(return_value=True)
    return db


# Test class organization
class TestUserService:
    """Test suite for UserService."""

    def test_create_user_success(self, mock_database):
        """Test successful user creation."""
        # Arrange
        service = UserService(database=mock_database)
        user_data = {"email": "new@example.com", "name": "New User"}

        # Act
        user_id = service.create_user(user_data)

        # Assert
        assert user_id == 1
        mock_database.insert.assert_called_once()

    def test_get_user_by_id(self, mock_database, sample_user):
        """Test retrieving user by ID."""
        # Arrange
        mock_database.query.return_value = [sample_user]
        service = UserService(database=mock_database)

        # Act
        user = service.get_user_by_id(1)

        # Assert
        assert user["email"] == "test@example.com"
        mock_database.query.assert_called_once()

    @pytest.mark.parametrize(
        "user_id,expected",
        [
            (1, True),
            (999, False),
            (None, False),
        ],
    )
    def test_user_exists(self, mock_database, user_id, expected):
        """Test user existence check with multiple scenarios."""
        service = UserService(database=mock_database)
        if expected:
            mock_database.query.return_value = [{"id": user_id}]
        else:
            mock_database.query.return_value = []

        result = service.user_exists(user_id)
        assert result == expected


# Mocking external dependencies
@patch("requests.get")
def test_fetch_external_api(mock_get):
    """Test fetching data from external API."""
    # Arrange
    mock_response = Mock()
    mock_response.json.return_value = {"data": "test"}
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Act
    result = fetch_api_data("https://api.example.com/data")

    # Assert
    assert result["data"] == "test"
    mock_get.assert_called_once()


# Exception testing
def test_divide_by_zero_raises_exception():
    """Test that division by zero raises appropriate exception."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)


# Async testing
@pytest.mark.asyncio
async def test_async_function():
    """Test async function execution."""
    result = await async_operation()
    assert result == "success"
