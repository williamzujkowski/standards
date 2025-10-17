#!/usr/bin/env node

/**
 * OAuth2 Client with PKCE Implementation
 *
 * Complete OAuth2 authorization code flow with PKCE for SPAs and mobile apps.
 * Includes token refresh and secure storage patterns.
 *
 * @nist ia-2 "User authentication"
 * @nist sc-8 "Transmission confidentiality"
 */

const crypto = require('crypto');
const axios = require('axios');
const express = require('express');

class OAuth2Client {
  /**
   * @param {Object} config Configuration object
   * @param {string} config.clientId OAuth2 client ID
   * @param {string} config.redirectUri Redirect URI after authorization
   * @param {string} config.authorizationEndpoint Authorization endpoint URL
   * @param {string} config.tokenEndpoint Token endpoint URL
   * @param {string} config.scope OAuth2 scope (default: 'openid profile email')
   */
  constructor(config) {
    this.clientId = config.clientId;
    this.redirectUri = config.redirectUri;
    this.authorizationEndpoint = config.authorizationEndpoint;
    this.tokenEndpoint = config.tokenEndpoint;
    this.scope = config.scope || 'openid profile email';

    // In-memory storage (use Redis/database in production)
    this.sessionStore = new Map();
  }

  /**
   * Generate PKCE code verifier and challenge
   * @returns {Object} Object with codeVerifier and codeChallenge
   */
  generatePKCE() {
    // Generate random code verifier (43-128 characters)
    const codeVerifier = crypto.randomBytes(32).toString('base64url');

    // Create code challenge using SHA256
    const codeChallenge = crypto
      .createHash('sha256')
      .update(codeVerifier)
      .digest('base64url');

    return { codeVerifier, codeChallenge };
  }

  /**
   * Generate random state parameter for CSRF protection
   * @returns {string} Random state value
   */
  generateState() {
    return crypto.randomBytes(16).toString('hex');
  }

  /**
   * Generate authorization URL to redirect user
   * @param {string} sessionId Session identifier
   * @returns {string} Authorization URL
   */
  getAuthorizationUrl(sessionId) {
    const { codeVerifier, codeChallenge } = this.generatePKCE();
    const state = this.generateState();

    // Store PKCE and state in session
    this.sessionStore.set(sessionId, {
      codeVerifier,
      state,
      timestamp: Date.now()
    });

    // Build authorization URL
    const params = new URLSearchParams({
      response_type: 'code',
      client_id: this.clientId,
      redirect_uri: this.redirectUri,
      scope: this.scope,
      state: state,
      code_challenge: codeChallenge,
      code_challenge_method: 'S256'
    });

    return `${this.authorizationEndpoint}?${params.toString()}`;
  }

  /**
   * Exchange authorization code for tokens
   * @param {string} code Authorization code from callback
   * @param {string} state State parameter from callback
   * @param {string} sessionId Session identifier
   * @returns {Promise<Object>} Token response
   */
  async exchangeCode(code, state, sessionId) {
    // Retrieve session data
    const session = this.sessionStore.get(sessionId);
    if (!session) {
      throw new Error('Session not found or expired');
    }

    // Validate state parameter (CSRF protection)
    if (state !== session.state) {
      throw new Error('Invalid state parameter - possible CSRF attack');
    }

    // Check session age (prevent replay attacks)
    const maxAge = 10 * 60 * 1000; // 10 minutes
    if (Date.now() - session.timestamp > maxAge) {
      this.sessionStore.delete(sessionId);
      throw new Error('Authorization session expired');
    }

    try {
      // Exchange code for tokens
      const response = await axios.post(this.tokenEndpoint, {
        grant_type: 'authorization_code',
        code: code,
        redirect_uri: this.redirectUri,
        client_id: this.clientId,
        code_verifier: session.codeVerifier
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      // Clean up session
      this.sessionStore.delete(sessionId);

      return {
        access_token: response.data.access_token,
        refresh_token: response.data.refresh_token,
        id_token: response.data.id_token,
        expires_in: response.data.expires_in,
        token_type: response.data.token_type
      };

    } catch (error) {
      throw new Error(`Token exchange failed: ${error.response?.data?.error_description || error.message}`);
    }
  }

  /**
   * Refresh access token using refresh token
   * @param {string} refreshToken Refresh token
   * @returns {Promise<Object>} New token response
   */
  async refreshAccessToken(refreshToken) {
    try {
      const response = await axios.post(this.tokenEndpoint, {
        grant_type: 'refresh_token',
        refresh_token: refreshToken,
        client_id: this.clientId
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });

      return {
        access_token: response.data.access_token,
        refresh_token: response.data.refresh_token, // New refresh token (rotation)
        expires_in: response.data.expires_in,
        token_type: response.data.token_type
      };

    } catch (error) {
      throw new Error(`Token refresh failed: ${error.response?.data?.error_description || error.message}`);
    }
  }

  /**
   * Revoke token (logout)
   * @param {string} token Token to revoke
   * @param {string} tokenTypeHint Token type ('access_token' or 'refresh_token')
   * @returns {Promise<void>}
   */
  async revokeToken(token, tokenTypeHint = 'refresh_token') {
    try {
      await axios.post(`${this.tokenEndpoint.replace('/token', '/revoke')}`, {
        token: token,
        token_type_hint: tokenTypeHint,
        client_id: this.clientId
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
    } catch (error) {
      throw new Error(`Token revocation failed: ${error.message}`);
    }
  }
}

/**
 * Express.js example integration
 */
function createExpressApp(oauth2Client) {
  const app = express();
  const session = require('express-session');

  app.use(session({
    secret: process.env.SESSION_SECRET,
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true,
      httpOnly: true,
      sameSite: 'lax', // Allow redirect from auth server
      maxAge: 10 * 60 * 1000 // 10 minutes
    }
  }));

  // Login endpoint - redirect to authorization server
  app.get('/login', (req, res) => {
    const authUrl = oauth2Client.getAuthorizationUrl(req.session.id);
    res.redirect(authUrl);
  });

  // Callback endpoint - handle authorization code
  app.get('/callback', async (req, res) => {
    const { code, state, error } = req.query;

    if (error) {
      return res.status(400).send(`Authorization failed: ${error}`);
    }

    try {
      const tokens = await oauth2Client.exchangeCode(code, state, req.session.id);

      // Store tokens securely
      // - Access token: Return to client (store in memory)
      // - Refresh token: Store in httpOnly cookie
      res.cookie('refresh_token', tokens.refresh_token, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000 // 7 days
      });

      res.json({
        access_token: tokens.access_token,
        expires_in: tokens.expires_in
      });

    } catch (error) {
      res.status(400).send(`Token exchange failed: ${error.message}`);
    }
  });

  // Refresh endpoint - get new access token
  app.post('/refresh', async (req, res) => {
    const refreshToken = req.cookies.refresh_token;

    if (!refreshToken) {
      return res.status(401).json({ error: 'No refresh token' });
    }

    try {
      const tokens = await oauth2Client.refreshAccessToken(refreshToken);

      // Update refresh token cookie (rotation)
      res.cookie('refresh_token', tokens.refresh_token, {
        httpOnly: true,
        secure: true,
        sameSite: 'strict',
        maxAge: 7 * 24 * 60 * 60 * 1000
      });

      res.json({
        access_token: tokens.access_token,
        expires_in: tokens.expires_in
      });

    } catch (error) {
      res.status(401).json({ error: error.message });
    }
  });

  // Logout endpoint - revoke tokens
  app.post('/logout', async (req, res) => {
    const refreshToken = req.cookies.refresh_token;

    if (refreshToken) {
      try {
        await oauth2Client.revokeToken(refreshToken);
      } catch (error) {
        console.error('Token revocation failed:', error);
      }
    }

    res.clearCookie('refresh_token');
    res.json({ message: 'Logged out' });
  });

  return app;
}

// Example usage
if (require.main === module) {
  const config = {
    clientId: process.env.OAUTH2_CLIENT_ID || 'your_client_id',
    redirectUri: process.env.OAUTH2_REDIRECT_URI || 'http://localhost:3000/callback',
    authorizationEndpoint: process.env.OAUTH2_AUTH_ENDPOINT || 'https://auth.example.com/authorize',
    tokenEndpoint: process.env.OAUTH2_TOKEN_ENDPOINT || 'https://auth.example.com/token',
    scope: 'openid profile email'
  };

  const client = new OAuth2Client(config);
  const app = createExpressApp(client);

  const PORT = process.env.PORT || 3000;
  app.listen(PORT, () => {
    console.log(`OAuth2 client listening on port ${PORT}`);
    console.log(`Visit http://localhost:${PORT}/login to start authentication`);
  });
}

module.exports = { OAuth2Client, createExpressApp };
