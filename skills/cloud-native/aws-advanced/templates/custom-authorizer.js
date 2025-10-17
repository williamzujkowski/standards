/**
 * API Gateway Custom Authorizer (Lambda Authorizer)
 * Validates JWT tokens and generates IAM policies
 */

import { verify } from 'jsonwebtoken';

// JWT secret - should be stored in AWS Secrets Manager in production
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key';

/**
 * Lambda handler for custom authorizer
 */
export const handler = async (event) => {
  console.log('Authorizer event:', JSON.stringify(event, null, 2));

  try {
    // Extract token from Authorization header
    const token = extractToken(event);

    // Verify and decode JWT
    const decoded = verify(token, JWT_SECRET, {
      algorithms: ['HS256'],
      issuer: 'myapp.com',
      audience: 'api.myapp.com'
    });

    console.log('Token decoded:', decoded);

    // Generate IAM policy
    const policy = generatePolicy(
      decoded.sub,           // principalId (user ID)
      'Allow',               // effect
      event.methodArn,       // resource
      {
        userId: decoded.sub,
        email: decoded.email,
        roles: decoded.roles || [],
        tenantId: decoded.tenantId
      }
    );

    return policy;

  } catch (error) {
    console.error('Authorization failed:', error);

    // Return Unauthorized for invalid tokens
    if (error.name === 'JsonWebTokenError') {
      throw new Error('Unauthorized: Invalid token');
    }
    if (error.name === 'TokenExpiredError') {
      throw new Error('Unauthorized: Token expired');
    }

    throw new Error('Unauthorized');
  }
};

/**
 * Extract token from Authorization header
 */
function extractToken(event) {
  // TOKEN authorizer
  if (event.authorizationToken) {
    const match = event.authorizationToken.match(/^Bearer (.+)$/);
    if (!match) {
      throw new Error('Invalid authorization header format');
    }
    return match[1];
  }

  // REQUEST authorizer
  if (event.headers && event.headers.Authorization) {
    const match = event.headers.Authorization.match(/^Bearer (.+)$/);
    if (!match) {
      throw new Error('Invalid authorization header format');
    }
    return match[1];
  }

  throw new Error('No authorization token found');
}

/**
 * Generate IAM policy document
 */
function generatePolicy(principalId, effect, resource, context = {}) {
  const policy = {
    principalId,
    policyDocument: {
      Version: '2012-10-17',
      Statement: [
        {
          Action: 'execute-api:Invoke',
          Effect: effect,
          Resource: resource
        }
      ]
    },
    context: {}
  };

  // Add context (available in integration as $context.authorizer.*)
  // Context values must be strings, numbers, or booleans
  for (const [key, value] of Object.entries(context)) {
    if (Array.isArray(value)) {
      policy.context[key] = JSON.stringify(value);
    } else if (typeof value === 'object') {
      policy.context[key] = JSON.stringify(value);
    } else {
      policy.context[key] = String(value);
    }
  }

  return policy;
}

/**
 * Advanced authorizer with role-based access control
 */
export const rbacHandler = async (event) => {
  try {
    const token = extractToken(event);
    const decoded = verify(token, JWT_SECRET);

    // Extract API method and resource
    const { httpMethod, resource } = event;

    // Check permissions based on roles
    const hasPermission = checkPermissions(
      decoded.roles,
      httpMethod,
      resource
    );

    if (!hasPermission) {
      return generatePolicy(decoded.sub, 'Deny', event.methodArn);
    }

    return generatePolicy(
      decoded.sub,
      'Allow',
      event.methodArn,
      {
        userId: decoded.sub,
        roles: decoded.roles,
        permissions: getPermissions(decoded.roles)
      }
    );

  } catch (error) {
    console.error('RBAC authorization failed:', error);
    throw new Error('Unauthorized');
  }
};

/**
 * Check if roles have permission for method and resource
 */
function checkPermissions(roles, httpMethod, resource) {
  const permissions = {
    admin: ['*'],
    editor: ['GET', 'POST', 'PUT'],
    viewer: ['GET']
  };

  for (const role of roles) {
    const allowedMethods = permissions[role] || [];
    if (allowedMethods.includes('*') || allowedMethods.includes(httpMethod)) {
      return true;
    }
  }

  return false;
}

/**
 * Get all permissions for roles
 */
function getPermissions(roles) {
  const allPermissions = new Set();

  const rolePermissions = {
    admin: ['read', 'write', 'delete', 'manage'],
    editor: ['read', 'write'],
    viewer: ['read']
  };

  for (const role of roles) {
    const perms = rolePermissions[role] || [];
    perms.forEach(p => allPermissions.add(p));
  }

  return Array.from(allPermissions);
}

/**
 * Authorizer with API key and IP whitelist
 */
export const apiKeyHandler = async (event) => {
  try {
    const apiKey = event.headers['x-api-key'];
    const sourceIp = event.requestContext.identity.sourceIp;

    if (!apiKey) {
      throw new Error('API key required');
    }

    // Validate API key (check DynamoDB in production)
    const isValid = await validateApiKey(apiKey, sourceIp);

    if (!isValid) {
      return generatePolicy('user', 'Deny', event.methodArn);
    }

    return generatePolicy(
      apiKey,
      'Allow',
      event.methodArn,
      {
        apiKey: apiKey,
        sourceIp: sourceIp
      }
    );

  } catch (error) {
    console.error('API key authorization failed:', error);
    throw new Error('Unauthorized');
  }
};

/**
 * Validate API key and IP whitelist
 */
async function validateApiKey(apiKey, sourceIp) {
  // In production, query DynamoDB for API key details
  const validKeys = {
    'test-key-123': {
      active: true,
      allowedIps: ['*'] // or specific IPs
    }
  };

  const keyData = validKeys[apiKey];
  if (!keyData || !keyData.active) {
    return false;
  }

  // Check IP whitelist
  if (keyData.allowedIps.includes('*')) {
    return true;
  }

  return keyData.allowedIps.includes(sourceIp);
}

/**
 * Caching authorizer with TTL
 * Returns policy with usageIdentifierKey for caching
 */
export const cachedHandler = async (event) => {
  try {
    const token = extractToken(event);
    const decoded = verify(token, JWT_SECRET);

    const policy = generatePolicy(
      decoded.sub,
      'Allow',
      event.methodArn,
      {
        userId: decoded.sub,
        email: decoded.email
      }
    );

    // Enable caching with usage identifier
    policy.usageIdentifierKey = decoded.sub;

    return policy;

  } catch (error) {
    console.error('Cached authorization failed:', error);
    throw new Error('Unauthorized');
  }
};
