#!/usr/bin/env python3

"""
JWT Validator using RS256

This example demonstrates production-ready JWT validation with:
- RS256 asymmetric signing
- Standard claims validation (iss, aud, exp)
- Token type verification
- Proper error handling

@nist ia-5 "Authenticator management"
@nist sc-13 "Cryptographic protection"
"""

import jwt
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from pathlib import Path


class JWTValidator:
    """Validate JWT tokens using RS256 asymmetric signing."""

    def __init__(self, config: Dict[str, str]):
        """
        Initialize JWT validator.

        Args:
            config: Configuration dictionary with:
                - public_key_path: Path to RS256 public key
                - issuer: Expected token issuer
                - audience: Expected token audience
        """
        self.public_key = Path(config['public_key_path']).read_text()
        self.issuer = config['issuer']
        self.audience = config['audience']

    def verify(self, token: str, options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Verify and decode JWT token.

        Args:
            token: JWT token string to verify
            options: Additional verification options

        Returns:
            Decoded token payload

        Raises:
            ValueError: If token is invalid
        """
        default_options = {
            'verify_signature': True,
            'verify_exp': True,
            'verify_iat': True,
            'verify_aud': True,
            'verify_iss': True
        }

        verify_options = {**default_options, **(options or {})}

        try:
            decoded = jwt.decode(
                token,
                self.public_key,
                algorithms=['RS256'],
                issuer=self.issuer,
                audience=self.audience,
                options=verify_options
            )

            # Additional custom validations
            self._validate_custom_claims(decoded)

            return decoded

        except jwt.ExpiredSignatureError:
            raise ValueError('Token has expired')
        except jwt.InvalidTokenError as e:
            raise ValueError(f'Invalid token: {str(e)}')
        except jwt.InvalidIssuerError:
            raise ValueError('Token issuer does not match expected issuer')
        except jwt.InvalidAudienceError:
            raise ValueError('Token audience does not match expected audience')

    def _validate_custom_claims(self, payload: Dict[str, Any]) -> None:
        """
        Validate custom claims in token payload.

        Args:
            payload: Decoded token payload

        Raises:
            ValueError: If custom claims are invalid
        """
        # Validate token type if present
        if 'type' in payload and payload['type'] not in ['access', 'refresh']:
            raise ValueError('Invalid token type')

        # Validate required custom claims
        if 'sub' not in payload:
            raise ValueError('Missing subject (sub) claim')

    def decode_without_verification(self, token: str) -> Dict[str, Any]:
        """
        Decode token without verification (for debugging only).

        Args:
            token: JWT token string

        Returns:
            Decoded token payload
        """
        return jwt.decode(token, options={'verify_signature': False})

    def is_expired(self, token: str) -> bool:
        """
        Check if token is expired without full verification.

        Args:
            token: JWT token string

        Returns:
            True if token is expired
        """
        try:
            decoded = jwt.decode(token, options={'verify_signature': False})
            if 'exp' not in decoded:
                return True

            return decoded['exp'] < datetime.now().timestamp()
        except:
            return True


class JWTAuthMiddleware:
    """Flask/Django middleware for JWT authentication."""

    def __init__(self, validator: JWTValidator):
        """
        Initialize middleware.

        Args:
            validator: JWTValidator instance
        """
        self.validator = validator

    def __call__(self, request):
        """
        Process request and validate JWT token.

        Args:
            request: HTTP request object

        Returns:
            Request with user info attached

        Raises:
            ValueError: If token is invalid
        """
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise ValueError('Missing or invalid Authorization header')

        token = auth_header[7:]  # Remove 'Bearer ' prefix

        try:
            # Verify token
            decoded = self.validator.verify(token)

            # Attach user info to request
            request.user = {
                'user_id': decoded['sub'],
                'roles': decoded.get('roles', []),
                'email': decoded.get('email')
            }

            return request

        except ValueError as e:
            raise ValueError(f'Authentication failed: {str(e)}')


def create_flask_decorator(validator: JWTValidator):
    """
    Create Flask route decorator for JWT authentication.

    Args:
        validator: JWTValidator instance

    Returns:
        Decorator function
    """
    from functools import wraps
    from flask import request, jsonify

    def require_auth(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'Missing or invalid Authorization header'}), 401

            token = auth_header[7:]

            try:
                decoded = validator.verify(token)
                request.user = {
                    'user_id': decoded['sub'],
                    'roles': decoded.get('roles', []),
                    'email': decoded.get('email')
                }
                return f(*args, **kwargs)
            except ValueError as e:
                return jsonify({'error': str(e)}), 401

        return decorated_function

    return require_auth


# Example usage
if __name__ == '__main__':
    # Example configuration
    config = {
        'public_key_path': '../keys/public.pem',
        'issuer': 'auth.example.com',
        'audience': 'api.example.com'
    }

    validator = JWTValidator(config)

    # Example token (replace with actual token)
    example_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...'

    try:
        decoded = validator.verify(example_token)
        print('Token is valid:')
        print(decoded)
    except ValueError as e:
        print(f'Token validation failed: {e}')

    # Example: Check if token is expired
    is_expired = validator.is_expired(example_token)
    print(f'Token expired: {is_expired}')
