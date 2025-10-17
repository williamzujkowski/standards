// @nist ac-3 "Access enforcement"
// @nist ac-6 "Least privilege"
// Express.js Authorization Middleware - Policy Enforcement Point (PEP)

const jwt = require('jsonwebtoken');
const { createLogger } = require('./logger');

const logger = createLogger('authz-middleware');

/**
 * Authenticate JWT and extract user claims
 * @nist ia-2 "Identification and authentication"
 */
function authenticateJWT(req, res, next) {
  const authHeader = req.headers.authorization;
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'Missing or invalid Authorization header' });
  }
  
  const token = authHeader.substring(7);
  
  try {
    const publicKey = process.env.JWT_PUBLIC_KEY;
    const decoded = jwt.verify(token, publicKey, {
      algorithms: ['RS256'],
      issuer: process.env.JWT_ISSUER,
      audience: process.env.JWT_AUDIENCE
    });
    
    req.user = decoded;
    next();
  } catch (err) {
    logger.warn('JWT verification failed', { error: err.message });
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
}

/**
 * Require specific OAuth2 scopes
 * @nist ac-3 "Access enforcement"
 */
function requireScope(...requiredScopes) {
  return (req, res, next) => {
    const tokenScopes = req.user.scope ? req.user.scope.split(' ') : [];
    
    const hasScope = requiredScopes.some(required => {
      if (required.endsWith(':*')) {
        const prefix = required.slice(0, -1);
        return tokenScopes.some(s => s.startsWith(prefix));
      }
      return tokenScopes.includes(required);
    });
    
    if (!hasScope) {
      logger.warn('Insufficient scope', {
        user: req.user.sub,
        required: requiredScopes,
        provided: tokenScopes
      });
      
      return res.status(403).json({
        error: 'insufficient_scope',
        message: `Required scopes: ${requiredScopes.join(' or ')}`,
        provided: tokenScopes.join(' ')
      });
    }
    
    next();
  };
}

/**
 * Require specific role (RBAC)
 * @nist ac-3 "Access enforcement"
 * @nist ac-6 "Least privilege"
 */
function requireRole(...allowedRoles) {
  return (req, res, next) => {
    const userRole = req.user.role;
    
    if (!allowedRoles.includes(userRole)) {
      logger.warn('Insufficient role', {
        user: req.user.sub,
        required: allowedRoles,
        actual: userRole
      });
      
      return res.status(403).json({
        error: 'Forbidden',
        message: `Required role: ${allowedRoles.join(' or ')}`
      });
    }
    
    next();
  };
}

/**
 * Enforce resource ownership
 * @nist ac-3 "Access enforcement"
 */
function requireOwnership(resourceIdParam = 'id', ownerField = 'owner_id') {
  return async (req, res, next) => {
    const resourceId = req.params[resourceIdParam];
    const userId = req.user.sub;
    
    try {
      // Fetch resource from database
      const resource = await req.app.locals.db.query(
        `SELECT ${ownerField} FROM resources WHERE id = ?`,
        [resourceId]
      );
      
      if (!resource) {
        return res.status(404).json({ error: 'Resource not found' });
      }
      
      // Check ownership (or admin override)
      if (resource[ownerField] !== userId && req.user.role !== 'admin') {
        logger.warn('Ownership check failed', {
          user: userId,
          resource: resourceId,
          owner: resource[ownerField]
        });
        
        return res.status(403).json({
          error: 'Forbidden',
          message: 'You do not own this resource'
        });
      }
      
      req.resource = resource;
      next();
    } catch (err) {
      logger.error('Ownership check error', { error: err.message });
      return res.status(500).json({ error: 'Authorization error' });
    }
  };
}

/**
 * Policy Enforcement Point (PEP) for ABAC
 * @nist ac-3 "Access enforcement"
 * @nist ac-16 "Security attributes"
 */
function enforcePolicyPEP(resourceExtractor, actionExtractor = null) {
  return async (req, res, next) => {
    const { ABACEngine } = require('./abac-engine');
    const abac = new ABACEngine(process.env.ABAC_POLICY_FILE);
    
    try {
      // Extract subject attributes
      const subject = {
        id: req.user.sub,
        role: req.user.role,
        department: req.user.department || null,
        clearance_level: req.user.clearance_level || 0,
        groups: req.user.groups || []
      };
      
      // Extract resource attributes
      const resource = await resourceExtractor(req);
      
      // Extract action
      const action = actionExtractor
        ? actionExtractor(req)
        : mapHttpMethodToAction(req.method);
      
      // Environment context
      const environment = {
        current_time: new Date().toISOString(),
        ip_address: req.ip,
        user_agent: req.get('user-agent'),
        day_of_week: new Date().toLocaleDateString('en-US', { weekday: 'long' })
      };
      
      // Evaluate policy
      const [allowed, reason] = await abac.evaluate(subject, resource, action, environment);
      
      // Audit decision
      await auditAuthzDecision({
        user_id: subject.id,
        resource: resource,
        action: action,
        allowed: allowed,
        reason: reason,
        timestamp: new Date(),
        ip_address: req.ip
      });
      
      if (!allowed) {
        logger.warn('ABAC policy denied access', {
          user: subject.id,
          resource: resource.type,
          action: action,
          reason: reason
        });
        
        return res.status(403).json({
          error: 'Forbidden',
          message: `Access denied: ${reason}`,
          resource: resource.type,
          action: action
        });
      }
      
      // Attach authorization context
      req.authz = { subject, resource, action, allowed };
      next();
    } catch (err) {
      logger.error('PEP evaluation error', { error: err.message, stack: err.stack });
      return res.status(500).json({ error: 'Authorization service error' });
    }
  };
}

/**
 * Map HTTP methods to CRUD actions
 */
function mapHttpMethodToAction(method) {
  const mapping = {
    'GET': 'read',
    'POST': 'create',
    'PUT': 'update',
    'PATCH': 'update',
    'DELETE': 'delete'
  };
  return mapping[method] || 'unknown';
}

/**
 * Audit authorization decision
 * @nist au-2 "Audit events"
 */
async function auditAuthzDecision(data) {
  const db = require('./database');
  
  await db.query(
    `INSERT INTO authorization_audit 
     (user_id, resource_type, resource_id, action, allowed, reason, ip_address, timestamp)
     VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
    [
      data.user_id,
      data.resource.type,
      data.resource.id,
      data.action,
      data.allowed,
      data.reason,
      data.ip_address,
      data.timestamp
    ]
  );
}

module.exports = {
  authenticateJWT,
  requireScope,
  requireRole,
  requireOwnership,
  enforcePolicyPEP,
  mapHttpMethodToAction
};
