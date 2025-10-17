#!/usr/bin/env node

/**
 * JWT Validator using RS256
 *
 * This example demonstrates production-ready JWT validation with:
 * - RS256 asymmetric signing
 * - Standard claims validation (iss, aud, exp)
 * - Token type verification
 * - Proper error handling
 *
 * @nist ia-5 "Authenticator management"
 * @nist sc-13 "Cryptographic protection"
 */

const jwt = require('jsonwebtoken');
const fs = require('fs');
const path = require('path');

class JWTValidator {
  /**
   * @param {Object} config Configuration object
   * @param {string} config.publicKeyPath Path to RS256 public key
   * @param {string} config.issuer Expected issuer
   * @param {string} config.audience Expected audience
   */
  constructor(config) {
    this.publicKey = fs.readFileSync(config.publicKeyPath);
    this.issuer = config.issuer;
    this.audience = config.audience;
  }

  /**
   * Verify and decode JWT token
   * @param {string} token JWT token to verify
   * @param {Object} options Verification options
   * @returns {Object} Decoded token payload
   * @throws {Error} If token is invalid
   */
  verify(token, options = {}) {
    const defaultOptions = {
      algorithms: ['RS256'],
      issuer: this.issuer,
      audience: this.audience
    };

    const verifyOptions = { ...defaultOptions, ...options };

    try {
      const decoded = jwt.verify(token, this.publicKey, verifyOptions);

      // Additional custom validations
      this.validateCustomClaims(decoded);

      return decoded;
    } catch (error) {
      return this.handleVerificationError(error);
    }
  }

  /**
   * Validate custom claims
   * @param {Object} payload Token payload
   */
  validateCustomClaims(payload) {
    // Validate token type if present
    if (payload.type && !['access', 'refresh'].includes(payload.type)) {
      throw new Error('Invalid token type');
    }

    // Validate required custom claims
    if (!payload.sub) {
      throw new Error('Missing subject (sub) claim');
    }

    // Add more custom validations as needed
  }

  /**
   * Handle verification errors with descriptive messages
   * @param {Error} error JWT verification error
   * @throws {Error} Enhanced error with details
   */
  handleVerificationError(error) {
    const errorMap = {
      'TokenExpiredError': 'Token has expired',
      'JsonWebTokenError': 'Invalid token format or signature',
      'NotBeforeError': 'Token not yet valid (nbf claim)',
      'invalid signature': 'Token signature verification failed',
      'invalid issuer': 'Token issuer does not match expected issuer',
      'invalid audience': 'Token audience does not match expected audience'
    };

    const message = errorMap[error.name] || errorMap[error.message] || 'Token validation failed';

    throw new Error(`${message}: ${error.message}`);
  }

  /**
   * Decode token without verification (for debugging only)
   * @param {string} token JWT token
   * @returns {Object} Decoded token
   */
  decodeWithoutVerification(token) {
    return jwt.decode(token, { complete: true });
  }

  /**
   * Check if token is expired without full verification
   * @param {string} token JWT token
   * @returns {boolean} True if expired
   */
  isExpired(token) {
    try {
      const decoded = jwt.decode(token);
      if (!decoded || !decoded.exp) return true;

      return decoded.exp < Math.floor(Date.now() / 1000);
    } catch {
      return true;
    }
  }
}

/**
 * Middleware factory for Express.js
 * @param {JWTValidator} validator JWT validator instance
 * @returns {Function} Express middleware
 */
function createAuthMiddleware(validator) {
  return (req, res, next) => {
    try {
      // Extract token from Authorization header
      const authHeader = req.headers.authorization;
      if (!authHeader || !authHeader.startsWith('Bearer ')) {
        return res.status(401).json({ error: 'Missing or invalid Authorization header' });
      }

      const token = authHeader.substring(7);

      // Verify token
      const decoded = validator.verify(token, { type: 'access' });

      // Attach user info to request
      req.user = {
        userId: decoded.sub,
        roles: decoded.roles || [],
        email: decoded.email
      };

      next();
    } catch (error) {
      return res.status(401).json({ error: error.message });
    }
  };
}

// Example usage
if (require.main === module) {
  // Example configuration
  const config = {
    publicKeyPath: path.join(__dirname, '../keys/public.pem'),
    issuer: 'auth.example.com',
    audience: 'api.example.com'
  };

  const validator = new JWTValidator(config);

  // Example token (replace with actual token)
  const exampleToken = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...';

  try {
    const decoded = validator.verify(exampleToken);
    console.log('Token is valid:');
    console.log(JSON.stringify(decoded, null, 2));
  } catch (error) {
    console.error('Token validation failed:', error.message);
  }

  // Example: Check if token is expired
  const isExpired = validator.isExpired(exampleToken);
  console.log('Token expired:', isExpired);
}

module.exports = { JWTValidator, createAuthMiddleware };
