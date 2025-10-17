# Advanced Python Patterns

> **Level 3 Resource**: Deep dive into advanced Python patterns and techniques

## Table of Contents

- [Decorators](#decorators)
- [Context Managers](#context-managers)
- [Descriptors](#descriptors)
- [Metaclasses](#metaclasses)
- [Async Patterns](#async-patterns)
- [Design Patterns](#design-patterns)

---

## Decorators

### Function Decorators

```python
import functools
import time
import logging
from typing import Callable, TypeVar, ParamSpec

P = ParamSpec('P')
T = TypeVar('T')

logger = logging.getLogger(__name__)


def timeit(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0):
    """Decorator to retry function on failure."""
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    logger.warning(
                        f"{func.__name__} attempt {attempt + 1} failed: {e}"
                    )
                    time.sleep(delay)
            raise RuntimeError("Should never reach here")
        return wrapper
    return decorator


def cache_result(ttl: int = 300):
    """Decorator to cache function results with TTL."""
    cache: dict = {}

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = (args, tuple(sorted(kwargs.items())))
            now = time.time()

            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < ttl:
                    return result

            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        return wrapper
    return decorator


# Usage
@timeit
@retry(max_attempts=3)
def fetch_data(url: str) -> dict:
    """Fetch data from URL with retry and timing."""
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
```

### Class Decorators

```python
from dataclasses import dataclass
from typing import Type


def singleton(cls: Type[T]) -> Type[T]:
    """Decorator to make class a singleton."""
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def add_logging(cls: Type[T]) -> Type[T]:
    """Decorator to add logging to all class methods."""
    for name, method in cls.__dict__.items():
        if callable(method) and not name.startswith("_"):
            setattr(cls, name, timeit(method))
    return cls


# Usage
@singleton
class Database:
    """Singleton database connection."""
    def __init__(self, url: str):
        self.url = url
        self.connection = self._connect()

    def _connect(self):
        logger.info(f"Connecting to {self.url}")
        return None  # Actual connection logic


@add_logging
class DataProcessor:
    """Data processor with automatic logging."""
    def process(self, data: list) -> list:
        return [item * 2 for item in data]
```

---

## Context Managers

### Custom Context Managers

```python
from contextlib import contextmanager
from typing import Generator
import tempfile
import shutil


class DatabaseTransaction:
    """Context manager for database transactions."""

    def __init__(self, connection):
        self.connection = connection
        self.transaction = None

    def __enter__(self):
        self.transaction = self.connection.begin()
        return self.transaction

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.transaction.commit()
        else:
            self.transaction.rollback()
            logger.error(f"Transaction rolled back: {exc_val}")
        return False  # Don't suppress exceptions


@contextmanager
def temporary_directory() -> Generator[str, None, None]:
    """Context manager for temporary directory with cleanup."""
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@contextmanager
def timer(name: str) -> Generator[None, None, None]:
    """Context manager to time code blocks."""
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        logger.info(f"{name} took {elapsed:.4f}s")


# Usage
with DatabaseTransaction(db.connection) as txn:
    db.execute("INSERT INTO users VALUES (?)", (user_data,))
    db.execute("INSERT INTO audit_log VALUES (?)", (log_data,))


with temporary_directory() as temp_dir:
    file_path = os.path.join(temp_dir, "data.txt")
    with open(file_path, "w") as f:
        f.write("temporary data")


with timer("Data processing"):
    process_large_dataset(data)
```

---

## Descriptors

### Property Descriptors

```python
class ValidatedProperty:
    """Descriptor with validation."""

    def __init__(self, validator: Callable[[any], bool], error_msg: str):
        self.validator = validator
        self.error_msg = error_msg
        self.data = {}

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(id(obj))

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(self.error_msg)
        self.data[id(obj)] = value


class Email(ValidatedProperty):
    """Email validation descriptor."""

    def __init__(self):
        super().__init__(
            validator=lambda x: isinstance(x, str) and "@" in x,
            error_msg="Invalid email format"
        )


class Age(ValidatedProperty):
    """Age validation descriptor."""

    def __init__(self):
        super().__init__(
            validator=lambda x: isinstance(x, int) and 0 <= x <= 150,
            error_msg="Age must be between 0 and 150"
        )


# Usage
class User:
    email = Email()
    age = Age()

    def __init__(self, email: str, age: int):
        self.email = email  # Validated
        self.age = age      # Validated


user = User("test@example.com", 25)  # OK
user = User("invalid", 25)  # Raises ValueError
```

---

## Metaclasses

### Registry Pattern with Metaclass

```python
class RegistryMeta(type):
    """Metaclass that registers all subclasses."""

    registry = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != "Plugin":  # Don't register base class
            mcs.registry[name] = cls
        return cls

    @classmethod
    def get_plugin(mcs, name: str):
        """Get plugin by name."""
        return mcs.registry.get(name)


class Plugin(metaclass=RegistryMeta):
    """Base plugin class."""
    pass


class EmailPlugin(Plugin):
    """Email plugin implementation."""
    def send(self, message: str):
        logger.info(f"Sending email: {message}")


class SMSPlugin(Plugin):
    """SMS plugin implementation."""
    def send(self, message: str):
        logger.info(f"Sending SMS: {message}")


# Usage
email_plugin = RegistryMeta.get_plugin("EmailPlugin")()
email_plugin.send("Hello!")
```

---

## Async Patterns

### Async Context Managers

```python
import asyncio
import aiohttp
from typing import AsyncIterator


class AsyncDatabaseConnection:
    """Async context manager for database connection."""

    def __init__(self, url: str):
        self.url = url
        self.connection = None

    async def __aenter__(self):
        self.connection = await asyncio.sleep(0.1)  # Simulate connect
        logger.info(f"Connected to {self.url}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await asyncio.sleep(0.1)  # Simulate disconnect
        logger.info("Disconnected from database")
        return False


async def fetch_urls_concurrent(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)


async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch single URL."""
    async with session.get(url) as response:
        return await response.json()


async def stream_data(source: AsyncIterator) -> AsyncIterator[bytes]:
    """Stream data with backpressure."""
    async for chunk in source:
        # Process chunk
        processed = process_chunk(chunk)
        yield processed
        await asyncio.sleep(0)  # Allow other tasks to run


# Usage
async def main():
    async with AsyncDatabaseConnection("postgresql://localhost") as db:
        result = await db.query("SELECT * FROM users")

    urls = ["https://api.example.com/1", "https://api.example.com/2"]
    results = await fetch_urls_concurrent(urls)


asyncio.run(main())
```

---

## Design Patterns

### Factory Pattern

```python
from abc import ABC, abstractmethod
from enum import Enum


class NotificationType(Enum):
    """Notification types."""
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class Notification(ABC):
    """Abstract notification base class."""

    @abstractmethod
    def send(self, recipient: str, message: str) -> None:
        """Send notification."""
        pass


class EmailNotification(Notification):
    """Email notification implementation."""

    def send(self, recipient: str, message: str) -> None:
        logger.info(f"Sending email to {recipient}: {message}")


class SMSNotification(Notification):
    """SMS notification implementation."""

    def send(self, recipient: str, message: str) -> None:
        logger.info(f"Sending SMS to {recipient}: {message}")


class NotificationFactory:
    """Factory for creating notifications."""

    _creators = {
        NotificationType.EMAIL: EmailNotification,
        NotificationType.SMS: SMSNotification,
    }

    @classmethod
    def create(cls, notification_type: NotificationType) -> Notification:
        """Create notification of specified type."""
        creator = cls._creators.get(notification_type)
        if not creator:
            raise ValueError(f"Unknown notification type: {notification_type}")
        return creator()


# Usage
factory = NotificationFactory()
notification = factory.create(NotificationType.EMAIL)
notification.send("user@example.com", "Hello!")
```

### Strategy Pattern

```python
class SortStrategy(ABC):
    """Abstract sorting strategy."""

    @abstractmethod
    def sort(self, data: list) -> list:
        """Sort data."""
        pass


class QuickSort(SortStrategy):
    """Quick sort implementation."""

    def sort(self, data: list) -> list:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class MergeSort(SortStrategy):
    """Merge sort implementation."""

    def sort(self, data: list) -> list:
        # Implementation...
        return sorted(data)  # Simplified


class Sorter:
    """Context class using strategy."""

    def __init__(self, strategy: SortStrategy):
        self._strategy = strategy

    def sort(self, data: list) -> list:
        """Sort using configured strategy."""
        return self._strategy.sort(data)


# Usage
data = [3, 1, 4, 1, 5, 9, 2, 6]
sorter = Sorter(QuickSort())
sorted_data = sorter.sort(data)
```

---

## See Also

- [SKILL.md](../SKILL.md) - Main Python skill documentation
- [Testing Strategies](testing-strategies.md) - Advanced testing patterns
- [Architecture Patterns](architecture-patterns.md) - Software architecture
