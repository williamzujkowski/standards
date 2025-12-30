# Python Coding Standards - Extended Reference

This document contains comprehensive examples, configurations, and advanced patterns for Python development. It supplements the main [SKILL.md](SKILL.md) with detailed reference material.

---

## Table of Contents

- [Complete Type Hint Patterns](#complete-type-hint-patterns)
- [Full Configuration Files](#full-configuration-files)
- [Advanced Testing Patterns](#advanced-testing-patterns)
- [Production Examples](#production-examples)
- [Error Handling Templates](#error-handling-templates)
- [Structured Logging](#structured-logging)
- [Async Patterns](#async-patterns)
- [Performance Profiling](#performance-profiling)
- [NIST Control Tags](#nist-control-tags)
- [Common Pitfalls](#common-pitfalls)
- [Tool Ecosystem](#tool-ecosystem)
- [Integration Points](#integration-points)

---

## Complete Type Hint Patterns

### Basic Types

```python
from typing import Optional, Union, Any
from collections.abc import Sequence, Mapping, Iterator

# Basic types
def process_items(items: list[str], count: int = 10) -> dict[str, int]:
    """Process items and return counts."""
    return {item: len(item) for item in items[:count]}

# Optional (None allowed)
def find_user(user_id: int) -> Optional[User]:
    """Find user by ID, returns None if not found."""
    return db.query(User).filter(User.id == user_id).first()

# Union types (Python 3.10+ syntax)
def parse_id(value: str | int) -> int:
    """Parse user ID from string or int."""
    return int(value) if isinstance(value, str) else value

# Legacy Union syntax (Python 3.9 and earlier)
from typing import Union
def parse_id_legacy(value: Union[str, int]) -> int:
    return int(value) if isinstance(value, str) else value
```

### Protocols (Structural Typing)

```python
from typing import Protocol, runtime_checkable

class Drawable(Protocol):
    """Protocol for drawable objects."""
    def draw(self) -> None: ...

class Resizable(Protocol):
    """Protocol for resizable objects."""
    def resize(self, width: int, height: int) -> None: ...

# Combine protocols
class Widget(Drawable, Resizable, Protocol):
    """Widget must be drawable and resizable."""
    pass

def render(obj: Drawable) -> None:
    """Render any drawable object."""
    obj.draw()

# Runtime checkable protocol
@runtime_checkable
class Serializable(Protocol):
    def serialize(self) -> bytes: ...

def save_if_serializable(obj: Any) -> None:
    if isinstance(obj, Serializable):
        data = obj.serialize()
        # ... save data
```

### Generics

```python
from typing import TypeVar, Generic
from collections.abc import Callable

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')

class Stack(Generic[T]):
    """Generic stack implementation."""
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0


class Registry(Generic[K, V]):
    """Generic registry with key-value pairs."""
    def __init__(self) -> None:
        self._items: dict[K, V] = {}

    def register(self, key: K, value: V) -> None:
        self._items[key] = value

    def get(self, key: K) -> V | None:
        return self._items.get(key)


# Bounded type variables
from typing import TypeVar
Numeric = TypeVar('Numeric', int, float, complex)

def add_numbers(a: Numeric, b: Numeric) -> Numeric:
    return a + b
```

### TypedDict

```python
from typing import TypedDict, Required, NotRequired

class UserDict(TypedDict):
    """User data dictionary with typed fields."""
    id: int
    username: str
    email: str
    is_active: bool

class CreateUserDict(TypedDict, total=False):
    """User creation with optional fields."""
    username: Required[str]
    email: Required[str]
    bio: NotRequired[str]
    age: NotRequired[int]

def create_user(data: CreateUserDict) -> UserDict:
    """Create user from typed dictionary."""
    return {
        "id": generate_id(),
        "username": data["username"],
        "email": data["email"],
        "is_active": True,
    }
```

### Callable Types

```python
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec('P')
R = TypeVar('R')

def retry(times: int) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry decorator with proper typing."""
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == times - 1:
                        raise
            raise RuntimeError("Unreachable")
        return wrapper
    return decorator

@retry(3)
def fetch_data(url: str) -> dict:
    """Fetch data with automatic retry."""
    return requests.get(url).json()
```

### Literal Types

```python
from typing import Literal, get_args

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
HTTPMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]

def set_log_level(level: LogLevel) -> None:
    """Set logging level (compile-time checked)."""
    logging.getLogger().setLevel(level)

def make_request(method: HTTPMethod, url: str) -> Response:
    """Make HTTP request with typed method."""
    return requests.request(method, url)

# Get all literal values at runtime
all_levels = get_args(LogLevel)  # ("DEBUG", "INFO", ...)
```

---

## Full Configuration Files

### pyproject.toml

```toml
[build-system]
requires = ["setuptools>=65", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "myapp"
version = "1.0.0"
description = "Production Python application"
readme = "README.md"
requires-python = ">=3.10"
license = {text = "MIT"}
authors = [
    {name = "Your Name", email = "you@example.com"}
]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
]
dependencies = [
    "fastapi>=0.100.0",
    "pydantic>=2.0.0",
    "pydantic-settings>=2.0.0",
    "sqlalchemy>=2.0.0",
    "uvicorn>=0.23.0",
    "httpx>=0.25.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-asyncio>=0.21.0",
    "pytest-mock>=3.11.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.5.0",
    "ruff>=0.1.0",
    "pre-commit>=3.4.0",
]

[project.scripts]
myapp = "myapp.cli:main"

[project.urls]
Homepage = "https://github.com/you/myapp"
Documentation = "https://myapp.readthedocs.io"
Repository = "https://github.com/you/myapp.git"

[tool.setuptools.packages.find]
where = ["src"]

[tool.black]
line-length = 88
target-version = ["py310", "py311", "py312"]
include = '\.pyi?$'
extend-exclude = '''
/(
    \.eggs
    | \.git
    | \.hg
    | \.mypy_cache
    | \.tox
    | \.venv
    | _build
    | buck-out
    | build
    | dist
)/
'''

[tool.isort]
profile = "black"
line_length = 88
known_first_party = ["myapp"]
skip_gitignore = true

[tool.ruff]
line-length = 88
target-version = "py310"
select = [
    "E",    # pycodestyle errors
    "F",    # pyflakes
    "W",    # pycodestyle warnings
    "I",    # isort
    "UP",   # pyupgrade
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "S",    # flake8-bandit (security)
    "T20",  # flake8-print
    "SIM",  # flake8-simplify
    "ARG",  # flake8-unused-arguments
    "PTH",  # flake8-use-pathlib
]
ignore = [
    "E501",  # line too long (handled by black)
    "S101",  # assert usage (needed for tests)
]
exclude = [
    ".git",
    ".venv",
    "__pycache__",
    "build",
    "dist",
]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101", "ARG"]

[tool.mypy]
python_version = "3.10"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
strict_equality = true
show_error_codes = true
plugins = ["pydantic.mypy"]

[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--tb=short",
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80",
]
asyncio_mode = "auto"
markers = [
    "slow: marks tests as slow",
    "integration: marks integration tests",
    "unit: marks unit tests",
]

[tool.coverage.run]
source = ["src"]
branch = true
omit = [
    "*/tests/*",
    "*/__pycache__/*",
    "*/migrations/*",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "@abstractmethod",
]
show_missing = true
skip_covered = true
```

### .pre-commit-config.yaml

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: detect-private-key
      - id: no-commit-to-branch
        args: [--branch, main, --branch, master]

  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.6
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.1
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic>=2.0.0
          - types-requests
        args: [--config-file, pyproject.toml]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: [-c, pyproject.toml]
        additional_dependencies: ["bandit[toml]"]

  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest tests/unit -q
        language: system
        pass_filenames: false
        always_run: true
```

### mypy.ini (Standalone)

```ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
disallow_incomplete_defs = True
check_untyped_defs = True
no_implicit_optional = True
warn_redundant_casts = True
warn_unused_ignores = True
strict_equality = True
show_error_codes = True
show_column_numbers = True
pretty = True

# Pydantic plugin
plugins = pydantic.mypy

[pydantic-mypy]
init_forbid_extra = True
init_typed = True
warn_required_dynamic_aliases = True

[mypy-tests.*]
disallow_untyped_defs = False
disallow_incomplete_defs = False

[mypy-alembic.*]
ignore_missing_imports = True

[mypy-sqlalchemy.*]
ignore_missing_imports = True
```

### .coveragerc

```ini
[run]
source = src
branch = True
omit =
    */tests/*
    */venv/*
    */__pycache__/*
    */migrations/*
    */conftest.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if TYPE_CHECKING:
    if __name__ == .__main__.:
    @abstractmethod
    @abc.abstractmethod

show_missing = True
skip_covered = True
fail_under = 80

[html]
directory = htmlcov
```

---

## Advanced Testing Patterns

### Comprehensive Fixture Patterns

```python
# tests/conftest.py
"""Shared test fixtures and configuration."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from typing import Any

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from myapp.config import Settings, get_settings
from myapp.database import Base, get_db
from myapp.main import app


# Async event loop fixture
@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# Test settings override
@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """Override settings for testing."""
    return Settings(
        database_url="sqlite:///./test.db",
        secret_key="test-secret-key",
        debug=True,
    )


# Database fixtures
@pytest.fixture(scope="session")
def db_engine(test_settings):
    """Create test database engine."""
    engine = create_engine(
        test_settings.database_url,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db_session(db_engine) -> Generator[Session, None, None]:
    """Create database session for each test."""
    SessionLocal = sessionmaker(bind=db_engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


# Async HTTP client
@pytest_asyncio.fixture
async def async_client(
    db_session: Session,
    test_settings: Settings,
) -> AsyncGenerator[AsyncClient, None]:
    """Create async HTTP client for API testing."""

    def override_get_db():
        yield db_session

    def override_get_settings():
        return test_settings

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_settings] = override_get_settings

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


# Factory fixtures
@pytest.fixture
def user_factory(db_session: Session):
    """Factory for creating test users."""

    def create_user(
        username: str = "testuser",
        email: str = "test@example.com",
        **kwargs: Any,
    ) -> User:
        user = User(username=username, email=email, **kwargs)
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user

    return create_user


# Mock fixtures
@pytest.fixture
def mock_external_api(mocker):
    """Mock external API calls."""
    mock = mocker.patch("myapp.services.external_api.fetch_data")
    mock.return_value = {"status": "ok", "data": []}
    return mock
```

### Parametrized Testing

```python
import pytest
from myapp.validators import validate_email, validate_password


class TestEmailValidation:
    """Email validation tests with parametrization."""

    @pytest.mark.parametrize(
        "email,expected",
        [
            ("user@example.com", True),
            ("user.name@example.co.uk", True),
            ("user+tag@example.com", True),
            ("invalid-email", False),
            ("@example.com", False),
            ("user@", False),
            ("", False),
            (None, False),
        ],
        ids=[
            "valid-simple",
            "valid-subdomain",
            "valid-plus-tag",
            "invalid-no-at",
            "invalid-no-local",
            "invalid-no-domain",
            "invalid-empty",
            "invalid-none",
        ],
    )
    def test_email_validation(self, email, expected):
        """Test email validation with various inputs."""
        result = validate_email(email) if email else False
        assert result == expected


class TestPasswordValidation:
    """Password validation with custom markers."""

    @pytest.mark.parametrize(
        "password,errors",
        [
            ("Str0ng!Pass", []),
            ("weakpass", ["uppercase", "digit", "special"]),
            ("ALLCAPS123!", ["lowercase"]),
            ("Short1!", ["length"]),
        ],
    )
    def test_password_requirements(self, password, errors):
        """Test password validation returns correct errors."""
        result = validate_password(password)
        assert result.errors == errors
        assert result.is_valid == (len(errors) == 0)
```

### Async Testing

```python
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUserAPI:
    """Async API tests for user endpoints."""

    async def test_create_user(self, async_client: AsyncClient):
        """Test user creation endpoint."""
        response = await async_client.post(
            "/api/users/",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "Secure123!",
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "newuser"
        assert "id" in data
        assert "password" not in data  # Password not returned

    async def test_get_user(self, async_client: AsyncClient, user_factory):
        """Test user retrieval endpoint."""
        user = user_factory(username="testuser")

        response = await async_client.get(f"/api/users/{user.id}")

        assert response.status_code == 200
        assert response.json()["username"] == "testuser"

    async def test_get_nonexistent_user(self, async_client: AsyncClient):
        """Test 404 for nonexistent user."""
        response = await async_client.get("/api/users/99999")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
```

### Mock and Patch Patterns

```python
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


class TestExternalIntegration:
    """Tests with mocked external services."""

    @pytest.fixture
    def mock_payment_service(self):
        """Mock payment service."""
        with patch("myapp.services.payment.PaymentService") as mock:
            instance = mock.return_value
            instance.process_payment = AsyncMock(
                return_value={"status": "success", "transaction_id": "tx123"}
            )
            instance.refund = AsyncMock(return_value={"status": "refunded"})
            yield instance

    @pytest.mark.asyncio
    async def test_process_order_payment(self, mock_payment_service):
        """Test order processing with mocked payment."""
        from myapp.services.order import OrderService

        order_service = OrderService(payment_service=mock_payment_service)
        result = await order_service.process_order(
            user_id=1, items=[{"product_id": 1, "quantity": 2}]
        )

        assert result.status == "completed"
        mock_payment_service.process_payment.assert_called_once()

    def test_with_context_manager_mock(self):
        """Test using context manager for patching."""
        with patch("myapp.utils.current_time") as mock_time:
            from datetime import datetime

            mock_time.return_value = datetime(2024, 1, 1, 12, 0, 0)

            from myapp.utils import get_formatted_time

            result = get_formatted_time()
            assert result == "2024-01-01 12:00:00"
```

---

## Production Examples

### FastAPI Service with Database

```python
# src/myapp/main.py
"""Production FastAPI service."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from myapp.config import get_settings, Settings
from myapp.database import get_db, init_db
from myapp.models import User
from myapp.services.user import UserService
import logging

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan: startup and shutdown."""
    # Startup
    logger.info("Starting application...")
    init_db()
    yield
    # Shutdown
    logger.info("Shutting down application...")


app = FastAPI(
    title="User Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Schemas
class UserCreate(BaseModel):
    """User creation request."""
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response (no password)."""
    id: int
    username: str
    email: EmailStr
    is_active: bool

    class Config:
        from_attributes = True


# Dependencies
def get_user_service(db: Session = Depends(get_db)) -> UserService:
    """Get user service instance."""
    return UserService(db)


# Endpoints
@app.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Create a new user."""
    try:
        return user_service.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    user_service: UserService = Depends(get_user_service),
) -> User:
    """Get user by ID."""
    user = user_service.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/health")
async def health_check(settings: Settings = Depends(get_settings)):
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": settings.environment,
    }
```

### Database Models with SQLAlchemy

```python
# src/myapp/models.py
"""Database models."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from myapp.database import Base


class User(Base):
    """User database model."""
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # Relationships
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"


class Post(Base):
    """Post database model."""
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_published: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
```

### Service Layer Pattern

```python
# src/myapp/services/user.py
"""User service layer."""

from typing import Optional
import bcrypt
from sqlalchemy.orm import Session

from myapp.models import User


class UserService:
    """User business logic service."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create_user(
        self,
        username: str,
        email: str,
        password: str,
    ) -> User:
        """Create new user with hashed password."""
        # Validate uniqueness
        if self.get_by_username(username):
            raise ValueError(f"Username '{username}' already exists")
        if self.get_by_email(email):
            raise ValueError(f"Email '{email}' already exists")

        # Hash password
        password_hash = self._hash_password(password)

        # Create user
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.db.query(User).filter(User.username == username).first()

    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        return self.db.query(User).filter(User.email == email).first()

    def verify_password(self, user: User, password: str) -> bool:
        """Verify user password."""
        return bcrypt.checkpw(
            password.encode("utf-8"),
            user.password_hash.encode("utf-8"),
        )

    def _hash_password(self, password: str) -> str:
        """Hash password with bcrypt."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
```

---

## Error Handling Templates

### Complete Exception Hierarchy

```python
# src/myapp/exceptions.py
"""Application exception hierarchy."""

from datetime import datetime
from typing import Any, Optional


class AppError(Exception):
    """Base exception for all application errors."""

    def __init__(
        self,
        message: str,
        code: str,
        details: Optional[dict[str, Any]] = None,
        status_code: int = 500,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.details = details or {}
        self.status_code = status_code
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "timestamp": self.timestamp,
            }
        }


class ValidationError(AppError):
    """Input validation failed."""

    def __init__(self, field: str, message: str, value: Any = None) -> None:
        super().__init__(
            message=f"Validation failed for '{field}': {message}",
            code="VALIDATION_ERROR",
            details={"field": field, "value": str(value) if value else None},
            status_code=400,
        )


class AuthenticationError(AppError):
    """Authentication failed."""

    def __init__(self, reason: str = "Invalid credentials") -> None:
        super().__init__(
            message=reason,
            code="AUTHENTICATION_ERROR",
            status_code=401,
        )


class AuthorizationError(AppError):
    """Authorization failed (permission denied)."""

    def __init__(self, resource: str, action: str) -> None:
        super().__init__(
            message=f"Not authorized to {action} {resource}",
            code="AUTHORIZATION_ERROR",
            details={"resource": resource, "action": action},
            status_code=403,
        )


class ResourceNotFoundError(AppError):
    """Requested resource not found."""

    def __init__(self, resource_type: str, resource_id: str | int) -> None:
        super().__init__(
            message=f"{resource_type} with id '{resource_id}' not found",
            code="NOT_FOUND",
            details={"resource_type": resource_type, "resource_id": str(resource_id)},
            status_code=404,
        )


class ConflictError(AppError):
    """Resource conflict (duplicate, version mismatch)."""

    def __init__(self, resource_type: str, field: str, value: Any) -> None:
        super().__init__(
            message=f"{resource_type} with {field}='{value}' already exists",
            code="CONFLICT",
            details={"resource_type": resource_type, "field": field, "value": str(value)},
            status_code=409,
        )


class RateLimitError(AppError):
    """Rate limit exceeded."""

    def __init__(self, limit: int, window: int, retry_after: int) -> None:
        super().__init__(
            message=f"Rate limit exceeded: {limit} requests per {window} seconds",
            code="RATE_LIMIT_EXCEEDED",
            details={"limit": limit, "window": window, "retry_after": retry_after},
            status_code=429,
        )


class ExternalServiceError(AppError):
    """External service failure."""

    def __init__(self, service: str, error: str) -> None:
        super().__init__(
            message=f"External service '{service}' failed: {error}",
            code="EXTERNAL_SERVICE_ERROR",
            details={"service": service, "error": error},
            status_code=502,
        )
```

### FastAPI Exception Handlers

```python
# src/myapp/error_handlers.py
"""FastAPI exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from myapp.exceptions import AppError


def register_exception_handlers(app: FastAPI) -> None:
    """Register all exception handlers."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        """Handle application errors."""
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_dict(),
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
        """Handle value errors as validation errors."""
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(exc),
                }
            },
        )

    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected errors."""
        # Log the full error
        import logging
        logging.getLogger(__name__).exception("Unexpected error")

        return JSONResponse(
            status_code=500,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An unexpected error occurred",
                }
            },
        )
```

---

## Structured Logging

```python
# src/myapp/logging_config.py
"""Structured logging configuration."""

import logging
import sys
from typing import Any

import structlog


def configure_logging(
    level: str = "INFO",
    json_format: bool = True,
) -> None:
    """Configure structured logging."""

    # Shared processors
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.dev.set_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if json_format:
        # Production: JSON format
        structlog.configure(
            processors=shared_processors + [
                structlog.processors.dict_tracebacks,
                structlog.processors.JSONRenderer(),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )
    else:
        # Development: colored console output
        structlog.configure(
            processors=shared_processors + [
                structlog.dev.ConsoleRenderer(colors=True),
            ],
            wrapper_class=structlog.make_filtering_bound_logger(
                getattr(logging, level)
            ),
            context_class=dict,
            logger_factory=structlog.PrintLoggerFactory(),
            cache_logger_on_first_use=True,
        )


# Usage example
logger = structlog.get_logger()

# Structured log with context
logger.info(
    "user_login",
    user_id=123,
    username="alice",
    ip_address="192.168.1.1",
    success=True,
)

# Error with exception
try:
    process_payment(order)
except PaymentError as e:
    logger.error(
        "payment_failed",
        order_id=order.id,
        amount=order.total,
        error=str(e),
        exc_info=True,
    )
```

---

## Async Patterns

```python
# src/myapp/async_patterns.py
"""Advanced async patterns."""

import asyncio
from typing import AsyncIterator, TypeVar
from collections.abc import Awaitable, Callable

import aiohttp
import aiofiles

T = TypeVar("T")


async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch URL asynchronously with error handling."""
    async with session.get(url) as response:
        response.raise_for_status()
        return await response.json()


async def fetch_all_urls(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=True)


async def fetch_with_semaphore(
    urls: list[str],
    max_concurrent: int = 10,
) -> list[dict]:
    """Fetch URLs with concurrency limit."""
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_limited(session: aiohttp.ClientSession, url: str) -> dict:
        async with semaphore:
            return await fetch_url(session, url)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_limited(session, url) for url in urls]
        return await asyncio.gather(*tasks)


async def stream_large_file(file_path: str) -> AsyncIterator[bytes]:
    """Stream large file asynchronously."""
    async with aiofiles.open(file_path, "rb") as f:
        while chunk := await f.read(8192):
            yield chunk


async def retry_async(
    coro_func: Callable[..., Awaitable[T]],
    *args,
    retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    **kwargs,
) -> T:
    """Retry async function with exponential backoff."""
    last_exception = None
    current_delay = delay

    for attempt in range(retries):
        try:
            return await coro_func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            if attempt < retries - 1:
                await asyncio.sleep(current_delay)
                current_delay *= backoff

    raise last_exception


async def timeout_wrapper(
    coro: Awaitable[T],
    timeout: float,
) -> T:
    """Wrap coroutine with timeout."""
    return await asyncio.wait_for(coro, timeout=timeout)
```

---

## Performance Profiling

```python
# src/myapp/profiling.py
"""Performance profiling utilities."""

import cProfile
import functools
import time
from contextlib import contextmanager
from typing import Callable, Generator, TypeVar

import structlog

logger = structlog.get_logger()

T = TypeVar("T")


def timeit(func: Callable[..., T]) -> Callable[..., T]:
    """Measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(
            "function_timing",
            function=func.__name__,
            elapsed_seconds=round(elapsed, 4),
        )
        return result
    return wrapper


@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    """Context manager for timing code blocks."""
    start = time.perf_counter()
    yield
    elapsed = time.perf_counter() - start
    logger.info("block_timing", name=name, elapsed_seconds=round(elapsed, 4))


def profile_function(func: Callable[..., T]) -> Callable[..., T]:
    """Profile function with cProfile."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> T:
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        profiler.print_stats(sort="cumulative")
        return result
    return wrapper


# Memoization with TTL
from functools import lru_cache
from datetime import datetime, timedelta


def timed_lru_cache(seconds: int = 60, maxsize: int = 128):
    """LRU cache with time-based expiration."""
    def decorator(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return func(*args, **kwargs)

        wrapper.cache_clear = func.cache_clear
        wrapper.cache_info = func.cache_info
        return wrapper

    return decorator


# Usage
@timed_lru_cache(seconds=300, maxsize=100)
def fetch_user_profile(user_id: int) -> dict:
    """Fetch user profile with 5-minute cache."""
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
```

---

## NIST Control Tags

```python
# src/myapp/auth.py
"""Authentication module with NIST control tags."""


# @nist IA-2 "User identification and authentication"
# @nist IA-5.1 "Password-based authentication"
def authenticate_user(username: str, password: str) -> User | None:
    """Authenticate user with secure password verification.

    NIST Controls:
        - IA-2: Identifies and authenticates organizational users
        - IA-5.1: Enforces password complexity requirements
    """
    pass


# @nist AC-3 "Access enforcement"
# @nist AC-6 "Least privilege"
def check_permission(user: User, resource: str, action: str) -> bool:
    """Enforce role-based access control.

    NIST Controls:
        - AC-3: Enforces approved authorizations
        - AC-6: Employs principle of least privilege
    """
    pass


# @nist SC-8 "Transmission confidentiality and integrity"
# @nist SC-13 "Cryptographic protection"
def encrypt_sensitive_data(data: str) -> str:
    """Encrypt data with AES-256-GCM.

    NIST Controls:
        - SC-8: Protects confidentiality of transmitted information
        - SC-13: Implements FIPS-validated cryptography
    """
    pass


# @nist AU-2 "Audit events"
# @nist AU-3 "Content of audit records"
def log_security_event(event_type: str, user: User, details: dict) -> None:
    """Log security-relevant events.

    NIST Controls:
        - AU-2: Identifies auditable events
        - AU-3: Generates audit records with required content
    """
    pass
```

---

## Common Pitfalls

### Pitfall 1: Mutable Default Arguments

```python
# Bad: Shared mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

# Good: Use None sentinel
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### Pitfall 2: Bare Except Clauses

```python
# Bad: Catches everything including KeyboardInterrupt
try:
    risky_operation()
except:
    pass

# Good: Specific exceptions with logging
try:
    risky_operation()
except (ValueError, KeyError) as e:
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise
```

### Pitfall 3: Import Star

```python
# Bad: Pollutes namespace
from os import *
from sys import *

# Good: Explicit imports
from os import path, environ
from sys import argv, exit
```

### Pitfall 4: Not Using Context Managers

```python
# Bad: Manual resource cleanup
f = open("file.txt")
try:
    data = f.read()
finally:
    f.close()

# Good: Context manager
with open("file.txt") as f:
    data = f.read()
```

### Pitfall 5: String Concatenation in Loops

```python
# Bad: O(n^2) string concatenation
result = ""
for item in items:
    result += str(item)

# Good: Use join
result = "".join(str(item) for item in items)
```

---

## Tool Ecosystem

| Tool | Purpose | Command |
|------|---------|---------|
| black | Code formatting | `black src/ tests/` |
| isort | Import sorting | `isort src/ tests/` |
| ruff | Fast linter | `ruff check src/` |
| mypy | Type checking | `mypy src/` |
| pylint | Code analysis | `pylint src/` |
| bandit | Security scanning | `bandit -r src/` |
| pytest | Testing | `pytest tests/` |
| coverage | Test coverage | `pytest --cov=src` |
| pre-commit | Git hooks | `pre-commit run --all-files` |

---

## Integration Points

### Upstream Dependencies

- **Development Tools**: Black, isort, mypy, pylint for code quality
- **Testing Framework**: pytest with pytest-cov for testing
- **Type Checking**: mypy for static type analysis
- **Package Management**: pip, poetry, or pipenv

### Downstream Consumers

- **CI/CD Systems**: GitHub Actions, GitLab CI, Jenkins
- **Code Review Tools**: pre-commit hooks, SonarQube
- **Documentation**: Sphinx or MkDocs
- **Containerization**: Docker for packaging

### Related Skills

- [Testing Standards](../../testing/SKILL.md)
- [Security Practices](../../security-practices/SKILL.md)
- [API Design](../../api/graphql/SKILL.md)
- [DevOps CI/CD](../../devops/ci-cd/SKILL.md)
- [Database SQL](../../database/sql/SKILL.md)
