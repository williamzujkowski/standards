#!/usr/bin/env python3
"""
Test suite for authentication service with NIST compliance checks.

@nist si-11 "Error handling"
@nist cm-3 "Configuration change control"
"""

import unittest
from datetime import datetime, timedelta
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from auth-service.py
auth_service = __import__('auth-service')
AuthenticationService = auth_service.AuthenticationService


class TestAuthenticationService(unittest.TestCase):
    """Test authentication service NIST controls."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.auth = AuthenticationService()
        self.test_user = "testuser"
        self.test_password = "TestP@ssw0rd123!"
        self.weak_password = "weak"
    
    def test_user_creation_with_strong_password(self):
        """
        Test user creation with strong password.
        
        @nist ia-5 "Authenticator management"
        @nist ia-5.1 "Password-based authentication"
        """
        result = self.auth.create_user(self.test_user, self.test_password)
        self.assertTrue(result)
        self.assertIn(self.test_user, self.auth.users)
    
    def test_user_creation_with_weak_password(self):
        """
        Test that weak passwords are rejected.
        
        @nist ia-5 "Authenticator management"
        """
        result = self.auth.create_user(self.test_user, self.weak_password)
        self.assertFalse(result)
        self.assertNotIn(self.test_user, self.auth.users)
    
    def test_successful_authentication(self):
        """
        Test successful authentication flow.
        
        @nist ia-2 "User authentication"
        @nist ac-12 "Session termination"
        """
        self.auth.create_user(self.test_user, self.test_password)
        token = self.auth.authenticate(self.test_user, self.test_password)
        
        self.assertIsNotNone(token)
        self.assertIn(token, self.auth.sessions)
    
    def test_failed_authentication(self):
        """
        Test failed authentication with wrong password.
        
        @nist ia-2 "User authentication"
        @nist au-2 "Audit events"
        """
        self.auth.create_user(self.test_user, self.test_password)
        token = self.auth.authenticate(self.test_user, "WrongPassword")
        
        self.assertIsNone(token)
    
    def test_account_lockout(self):
        """
        Test account lockout after failed attempts.
        
        @nist ac-7 "Unsuccessful login attempts"
        """
        self.auth.create_user(self.test_user, self.test_password)
        
        # Make 5 failed attempts
        for _ in range(5):
            self.auth.authenticate(self.test_user, "WrongPassword")
        
        # Account should be locked
        user = self.auth.users[self.test_user]
        self.assertIsNotNone(user['locked_until'])
        
        # Authentication should fail even with correct password
        token = self.auth.authenticate(self.test_user, self.test_password)
        self.assertIsNone(token)
    
    def test_session_expiration(self):
        """
        Test session expiration.
        
        @nist ac-12 "Session termination"
        @nist ac-12.1 "Session timeout"
        """
        self.auth.create_user(self.test_user, self.test_password)
        token = self.auth.authenticate(self.test_user, self.test_password)
        
        # Manually expire the session
        self.auth.sessions[token]['expires_at'] = datetime.utcnow() - timedelta(hours=1)
        
        # Session should be invalid
        self.assertFalse(self.auth.validate_session(token))
        self.assertNotIn(token, self.auth.sessions)
    
    def test_role_based_authorization(self):
        """
        Test role-based access control.
        
        @nist ac-3 "Access enforcement"
        @nist ac-6 "Least privilege"
        """
        # Create admin and regular user
        self.auth.create_user("admin", self.test_password, "admin")
        self.auth.create_user("user", self.test_password, "user")
        
        admin_token = self.auth.authenticate("admin", self.test_password)
        user_token = self.auth.authenticate("user", self.test_password)
        
        # Admin should have access to admin resources
        self.assertTrue(self.auth.authorize(admin_token, "admin"))
        self.assertTrue(self.auth.authorize(admin_token, "user"))
        
        # Regular user should not have admin access
        self.assertFalse(self.auth.authorize(user_token, "admin"))
        self.assertTrue(self.auth.authorize(user_token, "user"))
    
    def test_logout(self):
        """
        Test logout functionality.
        
        @nist ac-12 "Session termination"
        """
        self.auth.create_user(self.test_user, self.test_password)
        token = self.auth.authenticate(self.test_user, self.test_password)
        
        # Logout should succeed
        result = self.auth.logout(token)
        self.assertTrue(result)
        
        # Session should be terminated
        self.assertNotIn(token, self.auth.sessions)
        self.assertFalse(self.auth.validate_session(token))
    
    def test_password_complexity_requirements(self):
        """
        Test password complexity validation.
        
        @nist ia-5 "Authenticator management"
        @nist ia-5.1 "Password-based authentication"
        """
        test_cases = [
            ("short", False),  # Too short
            ("nouppercase123!", False),  # No uppercase
            ("NOLOWERCASE123!", False),  # No lowercase
            ("NoDigits!@#$", False),  # No digits
            ("NoSpecial123ABC", False),  # No special chars
            ("ValidP@ssw0rd!", True),  # Valid password
        ]
        
        for password, expected in test_cases:
            result = self.auth._validate_password_strength(password)
            self.assertEqual(result, expected, f"Password '{password}' validation failed")


if __name__ == "__main__":
    unittest.main()