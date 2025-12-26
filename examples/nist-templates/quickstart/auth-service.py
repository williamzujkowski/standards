#!/usr/bin/env python3
"""
Simple authentication service demonstrating NIST control tagging.
This example shows how to annotate security features with NIST controls.
"""

import hashlib
import hmac
import logging
import secrets
from datetime import datetime, timedelta
from typing import Any


# Configure audit logging
# @nist au-2 "Audit events"
# @nist au-3 "Content of audit records"
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("audit.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


class AuthenticationService:
    """
    Authentication service with NIST 800-53r5 controls.

    @nist ia-2 "User authentication"
    @nist ia-8 "System user identification"
    @nist ac-2 "Account management"
    """

    def __init__(self):
        self.users: dict[str, dict[str, Any]] = {}
        self.sessions: dict[str, dict[str, Any]] = {}
        self.failed_attempts: dict[str, int] = {}

        # @nist sc-13 "Cryptographic protection"
        self.salt = secrets.token_bytes(32)

    def create_user(self, username: str, password: str, role: str = "user") -> bool:
        """
        Create a new user account with secure password storage.

        @nist ia-5 "Authenticator management"
        @nist ia-5.1 "Password-based authentication"
        @nist ac-2 "Account management"
        """
        # Validate password strength
        if not self._validate_password_strength(password):
            logger.warning(f"Weak password rejected for user: {username}")
            return False

        # Hash password with salt
        # @nist sc-13 "Cryptographic protection"
        password_hash = self._hash_password(password)

        self.users[username] = {
            "password_hash": password_hash,
            "role": role,
            "created_at": datetime.utcnow(),
            "last_login": None,
            "failed_attempts": 0,
            "locked_until": None,
        }

        # Audit log
        # @nist au-2 "Audit events"
        logger.info(f"User account created: {username}, role: {role}")
        return True

    def authenticate(self, username: str, password: str) -> str | None:
        """
        Authenticate user and create session.

        @nist ia-2 "User authentication"
        @nist ac-7 "Unsuccessful login attempts"
        @nist ac-12 "Session termination"
        """
        # Check if user exists
        if username not in self.users:
            # @nist au-2 "Audit events"
            logger.warning(f"Authentication attempt for non-existent user: {username}")
            return None

        user = self.users[username]

        # Check if account is locked
        # @nist ac-7 "Unsuccessful login attempts"
        if user["locked_until"] and user["locked_until"] > datetime.utcnow():
            logger.warning(f"Authentication attempt for locked account: {username}")
            return None

        # Verify password
        # @nist ia-5 "Authenticator management"
        if not self._verify_password(password, user["password_hash"]):
            # Track failed attempts
            user["failed_attempts"] += 1

            # Lock account after 5 failed attempts
            # @nist ac-7 "Unsuccessful login attempts"
            if user["failed_attempts"] >= 5:
                user["locked_until"] = datetime.utcnow() + timedelta(minutes=15)
                logger.warning(f"Account locked due to failed attempts: {username}")

            # @nist au-2 "Audit events"
            logger.warning(f"Failed authentication attempt: {username}")
            return None

        # Reset failed attempts on successful login
        user["failed_attempts"] = 0
        user["locked_until"] = None
        user["last_login"] = datetime.utcnow()

        # Create session token
        # @nist ac-12 "Session termination"
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            "username": username,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(hours=1),
            "last_activity": datetime.utcnow(),
        }

        # @nist au-2 "Audit events"
        logger.info(f"Successful authentication: {username}")
        return session_token

    def authorize(self, session_token: str, required_role: str) -> bool:
        """
        Check if session has required role.

        @nist ac-3 "Access enforcement"
        @nist ac-6 "Least privilege"
        """
        # Validate session
        if not self.validate_session(session_token):
            return False

        session = self.sessions[session_token]
        username = session["username"]
        user = self.users[username]

        # Check role-based access
        # @nist ac-3 "Access enforcement"
        # @nist ac-6 "Least privilege"
        if user["role"] == "admin":
            return True  # Admins can access everything

        if user["role"] == required_role:
            return True

        # @nist au-2 "Audit events"
        logger.warning(f"Authorization denied: {username} attempted to access {required_role} resource")
        return False

    def validate_session(self, session_token: str) -> bool:
        """
        Validate session token and check expiration.

        @nist ac-12 "Session termination"
        @nist ac-12.1 "Session timeout"
        """
        if session_token not in self.sessions:
            return False

        session = self.sessions[session_token]

        # Check session expiration
        # @nist ac-12 "Session termination"
        if session["expires_at"] < datetime.utcnow():
            del self.sessions[session_token]
            logger.info(f"Session expired for user: {session['username']}")
            return False

        # Check idle timeout (15 minutes)
        # @nist ac-12.1 "Session timeout"
        idle_time = datetime.utcnow() - session["last_activity"]
        if idle_time > timedelta(minutes=15):
            del self.sessions[session_token]
            logger.info(f"Session terminated due to inactivity: {session['username']}")
            return False

        # Update last activity
        session["last_activity"] = datetime.utcnow()
        return True

    def logout(self, session_token: str) -> bool:
        """
        Terminate user session.

        @nist ac-12 "Session termination"
        """
        if session_token in self.sessions:
            username = self.sessions[session_token]["username"]
            del self.sessions[session_token]

            # @nist au-2 "Audit events"
            logger.info(f"User logged out: {username}")
            return True
        return False

    def _hash_password(self, password: str) -> bytes:
        """
        Hash password using PBKDF2-HMAC-SHA256.

        @nist sc-13 "Cryptographic protection"
        """
        return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), self.salt, 100000)  # iterations

    def _verify_password(self, password: str, password_hash: bytes) -> bool:
        """
        Verify password against hash.

        @nist sc-13 "Cryptographic protection"
        @nist ia-5 "Authenticator management"
        """
        test_hash = self._hash_password(password)
        return hmac.compare_digest(test_hash, password_hash)

    def _validate_password_strength(self, password: str) -> bool:
        """
        Validate password meets complexity requirements.

        @nist ia-5 "Authenticator management"
        @nist ia-5.1 "Password-based authentication"
        """
        # Minimum 12 characters
        if len(password) < 12:
            return False

        # Must contain uppercase, lowercase, digit, and special character
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        return all([has_upper, has_lower, has_digit, has_special])


# Example usage with input validation
def handle_login_request(auth_service: AuthenticationService, request_data: dict) -> dict:
    """
    Handle login API request with input validation.

    @nist si-10 "Information input validation"
    @nist si-11 "Error handling"
    """
    try:
        # Validate input
        # @nist si-10 "Information input validation"
        if not isinstance(request_data, dict):
            return {"error": "Invalid request format"}

        username = request_data.get("username", "")
        password = request_data.get("password", "")

        # Sanitize username (alphanumeric + underscore only)
        if not username or not username.replace("_", "").isalnum():
            return {"error": "Invalid username format"}

        # Length limits
        if len(username) > 50 or len(password) > 128:
            return {"error": "Input exceeds maximum length"}

        # Attempt authentication
        session_token = auth_service.authenticate(username, password)

        if session_token:
            return {"success": True, "session_token": session_token, "expires_in": 3600}
        return {"success": False, "error": "Authentication failed"}

    except Exception as e:
        # @nist si-11 "Error handling"
        # Don't expose internal errors to client
        logger.error(f"Error in login request: {e!s}")
        return {"error": "An error occurred during authentication"}


if __name__ == "__main__":
    # Demo the authentication service
    auth = AuthenticationService()

    # Create users
    auth.create_user("alice", "SecureP@ssw0rd123!", "admin")
    auth.create_user("bob", "AnotherP@ssw0rd456!", "user")

    # Test authentication
    alice_token = auth.authenticate("alice", "SecureP@ssw0rd123!")
    print(f"Alice token: {alice_token}")

    # Test authorization
    if auth.authorize(alice_token, "admin"):
        print("Alice has admin access")

    # Test logout
    auth.logout(alice_token)
    print("Alice logged out")
