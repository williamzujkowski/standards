import hashlib
import hmac
import logging
import traceback
import uuid
from datetime import datetime
from functools import wraps

import jwt
import redis
from flask import Flask, g, jsonify, request
from werkzeug.exceptions import BadRequest, Forbidden, Unauthorized


"""
Secure API Template with NIST Controls
@nist ac-3 "API access control"
@nist sc-8 "API transmission security"
@nist si-10 "API input validation"
"""

# Configure structured logging
# @nist au-3 "Structured audit logging"
logging.basicConfig(
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
redis_client = redis.Redis(decode_responses=True)


class RateLimiter:
    """
    Rate limiting implementation
    @nist ac-7 "Protection against brute force"
    """

    def __init__(self, redis_client):
        self.redis = redis_client
        self.default_limit = 100  # requests per minute
        self.burst_limit = 10  # burst allowance

    def check_rate_limit(self, identifier: str, limit: int | None = None) -> bool:
        """
        Check if request should be rate limited
        @nist ac-7 "Rate limiting implementation"
        """
        limit = limit or self.default_limit
        key = f"rate_limit:{identifier}"

        try:
            current = self.redis.incr(key)
            if current == 1:
                self.redis.expire(key, 60)  # 1 minute window

            if current > limit:
                # @nist au-2 "Log rate limit violations"
                logger.warning(f"Rate limit exceeded for {identifier}")
                return False

            return True

        except Exception as e:
            # @nist si-11 "Error handling"
            logger.error(f"Rate limit check failed: {e}")
            return True  # Fail open for availability


class InputValidator:
    """
    Input validation utilities
    @nist si-10 "Information input validation"
    """

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        import re

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    @staticmethod
    def validate_uuid(uuid_string: str) -> bool:
        """Validate UUID format"""
        try:
            uuid.UUID(uuid_string)
            return True
        except ValueError:
            return False

    @staticmethod
    def sanitize_string(input_string: str, max_length: int = 255) -> str:
        """
        Sanitize string input
        @nist si-10 "Input sanitization"
        """
        if not input_string:
            return ""

        # Remove control characters
        sanitized = "".join(char for char in input_string if ord(char) >= 32)

        # Truncate to max length
        sanitized = sanitized[:max_length]

        # Escape special characters
        sanitized = sanitized.replace("<", "&lt;").replace(">", "&gt;")

        return sanitized


def require_auth(scopes: list[str] = None):
    """
    Authentication decorator
    @nist ia-2 "API authentication"
    @nist ac-3 "API authorization"
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Extract token from Authorization header
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                # @nist au-2 "Log authentication failures"
                logger.warning(f"Missing or invalid auth header from {request.remote_addr}")
                raise Unauthorized("Invalid authentication")

            token = auth_header.split(" ")[1]

            try:
                # Verify JWT token
                # @nist ia-5 "Token validation"
                payload = jwt.decode(token, app.config["JWT_SECRET"], algorithms=["HS256"])

                # Check token expiration is handled by jwt.decode

                # Verify required scopes
                # @nist ac-3 "Scope-based authorization"
                if scopes:
                    token_scopes = payload.get("scopes", [])
                    if not any(scope in token_scopes for scope in scopes):
                        # @nist au-2 "Log authorization failures"
                        logger.warning(f"Insufficient scopes for user {payload.get('user_id')}")
                        raise Forbidden("Insufficient permissions")

                # Store user info in g for access in route
                g.user_id = payload.get("user_id")
                g.scopes = payload.get("scopes", [])

                # @nist au-2 "Log successful authentication"
                logger.info(f"Authenticated user {g.user_id}")

            except jwt.ExpiredSignatureError as e:
                # @nist ac-12 "Session termination"
                logger.warning(f"Expired token from {request.remote_addr}")
                raise Unauthorized("Token expired") from e
            except jwt.InvalidTokenError as e:
                logger.warning(f"Invalid token from {request.remote_addr}: {e}")
                raise Unauthorized("Invalid token") from e

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_request_signature():
    """
    Validate request signature for webhook endpoints
    @nist sc-8 "Message authenticity"
    @nist sc-13 "Cryptographic protection"
    """

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Get signature from header
            signature = request.headers.get("X-Webhook-Signature")
            if not signature:
                logger.warning(f"Missing signature from {request.remote_addr}")
                raise Unauthorized("Missing signature")

            # Calculate expected signature
            webhook_secret = app.config["WEBHOOK_SECRET"]
            body = request.get_data()

            expected_signature = hmac.new(webhook_secret.encode("utf-8"), body, hashlib.sha256).hexdigest()

            # Compare signatures
            if not hmac.compare_digest(signature, expected_signature):
                # @nist au-2 "Log signature validation failures"
                logger.warning(f"Invalid signature from {request.remote_addr}")
                raise Unauthorized("Invalid signature")

            return f(*args, **kwargs)

        return decorated_function

    return decorator


@app.before_request
def before_request():
    """
    Pre-request processing
    @nist au-2 "Log all API requests"
    @nist ac-7 "Rate limiting check"
    """
    # Generate correlation ID for request tracking
    g.correlation_id = str(uuid.uuid4())

    # Log request
    logger.info(
        "Request started",
        extra={
            "correlation_id": g.correlation_id,
            "method": request.method,
            "path": request.path,
            "remote_addr": request.remote_addr,
            "user_agent": request.headers.get("User-Agent"),
        },
    )

    # Check rate limit
    rate_limiter = RateLimiter(redis_client)
    if not rate_limiter.check_rate_limit(request.remote_addr):
        # @nist ac-7 "Enforce rate limits"
        raise BadRequest("Rate limit exceeded")


@app.after_request
def after_request(response):
    """
    Post-request processing
    @nist au-3 "Complete audit trail"
    """
    # Log response
    logger.info(
        "Request completed",
        extra={
            "correlation_id": g.get("correlation_id"),
            "status_code": response.status_code,
            "content_length": response.content_length,
        },
    )

    # Add security headers
    # @nist sc-8 "Security headers"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-Correlation-ID"] = g.get("correlation_id", "")

    return response


@app.errorhandler(Exception)
def handle_error(error):
    """
    Global error handler
    @nist si-11 "Error handling"
    @nist au-2 "Log errors"
    """
    # Log the error with full details
    logger.error(
        f"Unhandled error: {error!s}",
        extra={
            "correlation_id": g.get("correlation_id"),
            "error_type": type(error).__name__,
            "traceback": traceback.format_exc(),
        },
    )

    # Return sanitized error response
    # @nist si-11 "Prevent information disclosure"
    if isinstance(error, (BadRequest, Unauthorized, Forbidden)):
        return jsonify({"error": str(error)}), error.code

    # Generic error for unexpected exceptions
    return jsonify({"error": "Internal server error"}), 500


@app.route("/api/v1/users/<user_id>", methods=["GET"])
@require_auth(scopes=["users:read"])
def get_user(user_id: str):
    """
    Get user details
    @nist ac-3 "User data access control"
    @nist si-10 "Validate user ID input"
    """
    # Validate input
    if not InputValidator.validate_uuid(user_id):
        raise BadRequest("Invalid user ID format")

    # Check if requesting user has permission to view this user
    # @nist ac-3 "Enforce access control"
    if g.user_id != user_id and "admin" not in g.scopes:
        # @nist au-2 "Log unauthorized access attempts"
        logger.warning(f"User {g.user_id} attempted to access user {user_id} without permission")
        raise Forbidden("Access denied")

    # Fetch user data (placeholder)
    user_data = {
        "id": user_id,
        "username": "example_user",
        "email": "user@example.com",
        "created_at": datetime.utcnow().isoformat(),
    }

    return jsonify(user_data)


@app.route("/api/v1/webhook", methods=["POST"])
@validate_request_signature()
def webhook_handler():
    """
    Handle webhook events
    @nist sc-8 "Webhook security"
    @nist si-10 "Webhook payload validation"
    """
    # Parse and validate webhook payload
    try:
        payload = request.get_json()
        if not payload or "event_type" not in payload:
            raise BadRequest("Invalid webhook payload")

        # @nist si-10 "Validate event type"
        valid_events = ["user.created", "user.updated", "user.deleted"]
        if payload["event_type"] not in valid_events:
            raise BadRequest("Invalid event type")

        # Process webhook (placeholder)
        # @nist au-2 "Log webhook processing"
        logger.info(
            "Processing webhook",
            extra={
                "event_type": payload["event_type"],
                "event_id": payload.get("event_id"),
            },
        )

        return jsonify({"status": "processed"}), 200

    except Exception as e:
        # @nist si-11 "Webhook error handling"
        logger.error(f"Webhook processing failed: {e}")
        return jsonify({"status": "failed"}), 500


if __name__ == "__main__":
    # Configure for production
    app.config.update(
        JWT_SECRET="your-secret-key",  # Load from environment
        WEBHOOK_SECRET="webhook-secret",  # Load from environment
        # @nist sc-8 "HTTPS only in production"
        # Use proper WSGI server like gunicorn in production
    )

    # Development only
    app.run(debug=False, host="127.0.0.1", port=5000)
