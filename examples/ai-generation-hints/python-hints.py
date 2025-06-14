# templates/ai-generation-hints/python-hints.py
"""
AI Generation Hints for Python - Standards-Compliant Code Templates

Usage:
@generate python:[component-type] with:[CS:python + TS:pytest + SEC:*]
"""

from typing import TypeVar, Generic, Optional, Dict, Any, List, Union
from dataclasses import dataclass
from enum import Enum
import logging
from datetime import datetime
from contextlib import contextmanager
import functools

logger = logging.getLogger(__name__)

# Type definitions for better AI understanding
T = TypeVar('T')
E = TypeVar('E', bound=Exception)


@dataclass
class Result(Generic[T, E]):
    """
    Standard Result type for error handling (CS:error-handling).
    Following functional programming patterns for explicit error handling.
    """
    success: bool
    value: Optional[T] = None
    error: Optional[E] = None

    @classmethod
    def ok(cls, value: T) -> 'Result[T, E]':
        return cls(success=True, value=value)

    @classmethod
    def err(cls, error: E) -> 'Result[T, E]':
        return cls(success=False, error=error)


class StandardAPIEndpoint:
    """
    Template for API endpoint following CS:api + SEC:api standards.

    AI Instructions:
    - Always include input validation
    - Implement rate limiting
    - Add comprehensive error handling
    - Include OpenAPI documentation
    - Follow RESTful principles
    """

    @staticmethod
    def validate_input(data: Dict[str, Any]) -> Result[Dict[str, Any], ValueError]:
        """Validate all inputs according to SEC:validation standards."""
        try:
            # Type checking
            if not isinstance(data, dict):
                return Result.err(ValueError("Input must be a dictionary"))

            # Required fields
            required_fields = ['field1', 'field2']  # Customize based on endpoint
            for field in required_fields:
                if field not in data:
                    return Result.err(ValueError(f"Missing required field: {field}"))

            # Field validation
            # Add specific validation logic here

            return Result.ok(data)
        except Exception as e:
            logger.error(f"Validation error: {e}", exc_info=True)
            return Result.err(ValueError(str(e)))

    @staticmethod
    @functools.lru_cache(maxsize=128)
    def rate_limit_check(user_id: str, endpoint: str) -> bool:
        """
        Rate limiting following SEC:api standards.
        In production, use Redis or similar.
        """
        # Placeholder for rate limiting logic
        return True

    async def handle_request(
        self,
        request_data: Dict[str, Any],
        user_context: Dict[str, Any]
    ) -> Result[Dict[str, Any], Exception]:
        """
        Standard request handler following all security and error handling standards.

        Args:
            request_data: Incoming request data
            user_context: Authentication and user context

        Returns:
            Result containing response data or error
        """
        # Generate request ID for tracing (OBS:tracing)
        request_id = generate_request_id()

        with log_context(request_id=request_id, user_id=user_context.get('user_id')):
            # Rate limiting check (SEC:api)
            if not self.rate_limit_check(
                user_context.get('user_id', 'anonymous'),
                self.__class__.__name__
            ):
                return Result.err(Exception("Rate limit exceeded"))

            # Input validation (SEC:validation)
            validation_result = self.validate_input(request_data)
            if not validation_result.success:
                return Result.err(validation_result.error)

            try:
                # Business logic here
                result = await self.process_request(validation_result.value)

                # Audit logging (CS:audit)
                log_audit_event(
                    'api_request',
                    user_context.get('user_id'),
                    endpoint=self.__class__.__name__,
                    success=True
                )

                return Result.ok(result)

            except Exception as e:
                logger.error(f"Request processing error: {e}", exc_info=True)

                # Audit logging for failures
                log_audit_event(
                    'api_request',
                    user_context.get('user_id'),
                    endpoint=self.__class__.__name__,
                    success=False,
                    error=str(e)
                )

                return Result.err(e)

    async def process_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Override this method with actual business logic."""
        raise NotImplementedError


class TestGenerator:
    """
    Template for generating tests following TS:* standards.

    AI Instructions:
    - Generate comprehensive test suites
    - Include unit, integration, and edge cases
    - Follow AAA pattern (Arrange-Act-Assert)
    - Aim for 85%+ coverage (95% for critical paths)
    """

    @staticmethod
    def generate_unit_test_template(function_name: str) -> str:
        """Generate unit test template following TS:unit standards."""
        return f"""
import pytest
from unittest.mock import Mock, patch
from hypothesis import given, strategies as st

def test_{function_name}_success():
    \"\"\"Test {function_name} with valid input.\"\"\"
    # Arrange
    input_data = {{}}  # Add test data
    expected = {{}}    # Add expected result

    # Act
    result = {function_name}(input_data)

    # Assert
    assert result == expected


def test_{function_name}_validation_error():
    \"\"\"Test {function_name} with invalid input.\"\"\"
    # Arrange
    invalid_data = {{}}  # Add invalid test data

    # Act & Assert
    with pytest.raises(ValueError):
        {function_name}(invalid_data)


@given(st.dictionaries(st.text(), st.integers()))
def test_{function_name}_property_based(data):
    \"\"\"Property-based test for {function_name}.\"\"\"
    # Property: function should never raise unexpected exceptions
    try:
        result = {function_name}(data)
        # Add property assertions
        assert isinstance(result, (dict, Result))
    except (ValueError, TypeError):
        # Expected exceptions for invalid input
        pass


@pytest.mark.parametrize("input_data,expected", [
    ({{}}, {{}}),  # Add test cases
    ({{}}, {{}}),
])
def test_{function_name}_parametrized(input_data, expected):
    \"\"\"Parametrized tests for {function_name}.\"\"\"
    result = {function_name}(input_data)
    assert result == expected
"""


# Helper functions following standards

def generate_request_id() -> str:
    """Generate unique request ID for tracing (OBS:tracing)."""
    import uuid
    return str(uuid.uuid4())


@contextmanager
def log_context(**kwargs):
    """Context manager for structured logging (OBS:logging)."""
    import contextvars
    context = contextvars.copy_context()
    for key, value in kwargs.items():
        context[key] = value
    yield


def log_audit_event(
    event_type: str,
    user_id: Optional[str],
    **additional_fields
) -> None:
    """
    Log audit event following CS:audit + LEG:compliance standards.
    """
    audit_logger = logging.getLogger('audit')
    audit_logger.info(
        "Audit Event",
        extra={
            'event_type': event_type,
            'user_id': user_id,
            'timestamp': datetime.utcnow().isoformat(),
            'additional': additional_fields
        }
    )


# AI Generation Instructions
"""
When generating Python code:

1. Always include type hints (CS:python)
2. Use Result type for error handling instead of exceptions where appropriate
3. Include comprehensive docstrings (Google style)
4. Implement proper logging with context
5. Follow dependency injection patterns
6. Include input validation for all external inputs
7. Write tests alongside implementation
8. Use async/await for I/O operations
9. Implement rate limiting for APIs
10. Include audit logging for compliance

Example prompt usage:
@generate python:[user-service] with:[CS:python + SEC:auth + TS:pytest]
"""