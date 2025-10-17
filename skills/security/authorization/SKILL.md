---
name: authorization-security
description: Authorization security standards covering RBAC, ABAC, policy enforcement, OAuth2 scopes, resource-based access control, and NIST 800-53 compliance (AC-3, AC-4, AC-6) for production systems
tags: [security, authorization, rbac, abac, access-control, oauth2, nist-800-53]
category: security
difficulty: intermediate
estimated_time: 45 minutes
prerequisites: [security-practices, authentication-security]
related_skills: [authentication, api-security, secrets-management]
nist_controls: [AC-3, AC-4, AC-6, AC-2, AC-5, AC-16]
---

# Authorization Security

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-800-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-4500-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<800 tokens, 5 minutes)

### Core Principles

1. **Least Privilege**: Grant minimum permissions required (NIST AC-6)
2. **Separation of Duties**: No single user controls entire critical process
3. **Defense in Depth**: Multiple authorization checks at different layers
4. **Fail Secure**: Default deny, explicit allow
5. **Audit Everything**: Log all authorization decisions (AU-2)

### RBAC vs ABAC Comparison

| Aspect | RBAC (Role-Based) | ABAC (Attribute-Based) |
|--------|-------------------|------------------------|
| **Model** | Roles → Permissions | Attributes → Policies |
| **Flexibility** | Low (fixed roles) | High (dynamic rules) |
| **Complexity** | Simple to implement | Complex policy engine |
| **Use Case** | Traditional enterprise | Context-aware access |
| **Example** | `admin`, `user`, `guest` | `dept=finance AND time=business_hours` |
| **NIST Control** | AC-3 (Access Enforcement) | AC-3, AC-4, AC-16 |

### Essential Checklist

- [ ] **Least privilege**: Users have minimum required permissions (AC-6)
- [ ] **Separation of duties**: Critical operations require multiple approvals (AC-5)
- [ ] **Role hierarchies**: Roles inherit permissions logically
- [ ] **Policy enforcement**: Authorization checked at API gateway + service level
- [ ] **OAuth2 scopes**: Fine-grained permissions in access tokens
- [ ] **Resource ownership**: Users can only access their own resources
- [ ] **Deny by default**: Unknown requests rejected automatically
- [ ] **Audit logging**: All authorization decisions logged with user/resource/action
- [ ] **Time-based access**: Support for temporary permissions
- [ ] **Policy testing**: Unit tests for all authorization rules

### Quick Example

```python
# @nist ac-3 "Access enforcement"
# @nist ac-6 "Least privilege"

# ❌ NEVER do this (no authorization)
@app.route('/api/documents/<doc_id>')
def get_document(doc_id):
    return Document.query.get(doc_id)

# ✅ Enforce ownership and permissions
@app.route('/api/documents/<doc_id>')
@require_auth
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)

    # Check ownership OR read permission
    if doc.owner_id != current_user.id and not current_user.has_permission('documents:read'):
        abort(403, "Insufficient permissions")

    # Audit the access
    audit_log.info(f"User {current_user.id} accessed document {doc_id}")
    return doc.to_dict()
```

### Common Patterns

**Role Hierarchy:**

```
superadmin
  └── admin
       └── manager
            └── user
                 └── guest
```

**Permission Naming:**

- `resource:action` (e.g., `documents:read`, `users:write`)
- `service:resource:action` (e.g., `api:documents:delete`)

**Scope Patterns:**

- `read:profile` - Read own profile
- `read:all_profiles` - Read all profiles (admin)
- `write:documents` - Create/update documents
- `admin:*` - Full administrative access

### Quick Links to Level 2

- [RBAC Implementation](#rbac-implementation)
- [ABAC Implementation](#abac-implementation)
- [Policy Enforcement Points](#policy-enforcement-points)
- [OAuth2 Scopes](#oauth2-scopes-and-claims)
- [NIST Compliance](#nist-800-53-compliance)

---

## Level 2: Implementation (<4,500 tokens, 30 minutes)

### RBAC Implementation

**Role-Based Access Control** assigns permissions to roles, then roles to users. Ideal for traditional enterprise systems with stable organizational structures.

#### Core Components

1. **Roles**: Named collections of permissions (e.g., `admin`, `editor`, `viewer`)
2. **Permissions**: Specific actions on resources (e.g., `documents:read`, `users:write`)
3. **Users**: Assigned one or more roles
4. **Role Hierarchy**: Roles can inherit from parent roles

#### Database Schema

```sql
-- @nist ac-2 "Account management"
-- @nist ac-3 "Access enforcement"

CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    parent_role_id INTEGER REFERENCES roles(id),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE permissions (
    id SERIAL PRIMARY KEY,
    resource VARCHAR(50) NOT NULL,  -- e.g., 'documents', 'users'
    action VARCHAR(50) NOT NULL,    -- e.g., 'read', 'write', 'delete'
    description TEXT,
    UNIQUE(resource, action)
);

CREATE TABLE role_permissions (
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    permission_id INTEGER REFERENCES permissions(id) ON DELETE CASCADE,
    PRIMARY KEY (role_id, permission_id)
);

CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,  -- Support temporary access
    PRIMARY KEY (user_id, role_id)
);

-- Audit trail
CREATE TABLE authorization_audit (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    resource VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    allowed BOOLEAN NOT NULL,
    reason TEXT,
    ip_address INET,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_audit_user ON authorization_audit(user_id, timestamp);
CREATE INDEX idx_audit_resource ON authorization_audit(resource, timestamp);
```

#### Python Implementation

See [templates/policy-enforcement.py](templates/policy-enforcement.py) for complete implementation.

```python
# @nist ac-3 "Access enforcement"
# @nist ac-6 "Least privilege"
from functools import wraps
from flask import abort, g
from sqlalchemy import or_

class RBACManager:
    """Role-Based Access Control manager with hierarchy support."""

    def __init__(self, db):
        self.db = db
        self._permission_cache = {}

    def has_permission(self, user_id: int, resource: str, action: str) -> bool:
        """
        Check if user has permission (directly or via role hierarchy).

        @nist ac-3 "Access enforcement"
        @nist ac-6 "Least privilege"
        """
        cache_key = f"{user_id}:{resource}:{action}"
        if cache_key in self._permission_cache:
            return self._permission_cache[cache_key]

        # Get all user roles (including inherited)
        user_roles = self._get_user_roles_with_hierarchy(user_id)

        # Check if any role has the permission
        result = self.db.session.query(Permission).join(
            RolePermission
        ).filter(
            RolePermission.role_id.in_(user_roles),
            Permission.resource == resource,
            Permission.action == action
        ).first() is not None

        self._permission_cache[cache_key] = result
        return result

    def _get_user_roles_with_hierarchy(self, user_id: int) -> list[int]:
        """Get all roles including parent roles."""
        direct_roles = self.db.session.query(UserRole.role_id).filter(
            UserRole.user_id == user_id,
            or_(UserRole.expires_at.is_(None), UserRole.expires_at > datetime.utcnow())
        ).all()

        all_roles = set(role[0] for role in direct_roles)

        # Traverse hierarchy upwards
        for role_id in list(all_roles):
            parent_roles = self._get_parent_roles(role_id)
            all_roles.update(parent_roles)

        return list(all_roles)

    def _get_parent_roles(self, role_id: int) -> set[int]:
        """Recursively get all parent roles."""
        parents = set()
        role = self.db.session.query(Role).get(role_id)

        if role and role.parent_role_id:
            parents.add(role.parent_role_id)
            parents.update(self._get_parent_roles(role.parent_role_id))

        return parents

    def audit_authorization(self, user_id: int, resource: str, action: str,
                          allowed: bool, reason: str = None):
        """
        Log authorization decision for compliance.

        @nist au-2 "Audit events"
        @nist ac-3 "Access enforcement"
        """
        audit = AuthorizationAudit(
            user_id=user_id,
            resource=resource,
            action=action,
            allowed=allowed,
            reason=reason,
            ip_address=request.remote_addr,
            timestamp=datetime.utcnow()
        )
        self.db.session.add(audit)
        self.db.session.commit()

# Decorator for route protection
def require_permission(resource: str, action: str):
    """
    Decorator to enforce permissions on routes.

    @nist ac-3 "Access enforcement"
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.rbac_manager.has_permission(g.current_user.id, resource, action):
                g.rbac_manager.audit_authorization(
                    g.current_user.id, resource, action,
                    allowed=False, reason="Insufficient permissions"
                )
                abort(403, f"Permission denied: {resource}:{action}")

            g.rbac_manager.audit_authorization(
                g.current_user.id, resource, action,
                allowed=True
            )
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Usage example
@app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
@require_auth
@require_permission('documents', 'delete')
def delete_document(doc_id):
    doc = Document.query.get_or_404(doc_id)
    db.session.delete(doc)
    db.session.commit()
    return {'status': 'deleted'}, 200
```

#### Role Hierarchy Example

```python
# Create role hierarchy: superadmin > admin > manager > user > guest
roles = {
    'guest': None,
    'user': 'guest',
    'manager': 'user',
    'admin': 'manager',
    'superadmin': 'admin'
}

for role_name, parent_name in roles.items():
    parent = Role.query.filter_by(name=parent_name).first() if parent_name else None
    role = Role(
        name=role_name,
        description=f"{role_name.title()} role",
        parent_role_id=parent.id if parent else None
    )
    db.session.add(role)

# Assign permissions to base roles
permissions = [
    ('guest', 'documents', 'read'),      # Guests can read
    ('user', 'documents', 'write'),      # Users can write (inherits read)
    ('manager', 'documents', 'delete'),  # Managers can delete (inherits read+write)
    ('admin', 'users', 'write'),         # Admins can manage users
    ('superadmin', 'roles', 'write')     # Superadmins can manage roles
]

for role_name, resource, action in permissions:
    role = Role.query.filter_by(name=role_name).first()
    perm = Permission.query.filter_by(resource=resource, action=action).first()
    if not perm:
        perm = Permission(resource=resource, action=action)
        db.session.add(perm)
        db.session.flush()

    role_perm = RolePermission(role_id=role.id, permission_id=perm.id)
    db.session.add(role_perm)

db.session.commit()
```

See [templates/rbac-policy.yaml](templates/rbac-policy.yaml) for declarative policy definition.

---

### ABAC Implementation

**Attribute-Based Access Control** uses policies that evaluate attributes (user, resource, environment) to make dynamic authorization decisions. Ideal for complex, context-aware access control.

#### Core Components

1. **Attributes**: Properties of users, resources, or environment (e.g., `user.department`, `resource.classification`, `env.time`)
2. **Policies**: Rules written in policy language (XACML, Rego, Cedar)
3. **Policy Decision Point (PDP)**: Evaluates policies
4. **Policy Enforcement Point (PEP)**: Enforces PDP decisions

#### XACML Policy Example

See [templates/abac-policy.json](templates/abac-policy.json) for complete policy.

```xml
<!-- @nist ac-3 "Access enforcement" -->
<!-- @nist ac-4 "Information flow enforcement" -->
<!-- @nist ac-16 "Security attributes" -->

<Policy PolicyId="DocumentAccessPolicy"
        RuleCombiningAlgId="deny-overrides">

  <!-- Rule 1: Users can access their own documents -->
  <Rule RuleId="OwnerAccess" Effect="Permit">
    <Target>
      <Resources>
        <Resource>
          <ResourceMatch MatchId="string-equal">
            <AttributeValue DataType="string">document</AttributeValue>
            <ResourceAttributeDesignator
              AttributeId="resource-type"
              DataType="string"/>
          </ResourceMatch>
        </Resource>
      </Resources>
    </Target>
    <Condition>
      <Apply FunctionId="string-equal">
        <Apply FunctionId="string-one-and-only">
          <SubjectAttributeDesignator
            AttributeId="user-id"
            DataType="string"/>
        </Apply>
        <Apply FunctionId="string-one-and-only">
          <ResourceAttributeDesignator
            AttributeId="owner-id"
            DataType="string"/>
        </Apply>
      </Apply>
    </Condition>
  </Rule>

  <!-- Rule 2: Managers can access department documents during business hours -->
  <Rule RuleId="ManagerDepartmentAccess" Effect="Permit">
    <Target>
      <Subjects>
        <Subject>
          <SubjectMatch MatchId="string-equal">
            <AttributeValue DataType="string">manager</AttributeValue>
            <SubjectAttributeDesignator
              AttributeId="role"
              DataType="string"/>
          </SubjectMatch>
        </Subject>
      </Subjects>
    </Target>
    <Condition>
      <Apply FunctionId="and">
        <!-- Same department -->
        <Apply FunctionId="string-equal">
          <SubjectAttributeDesignator
            AttributeId="department"
            DataType="string"/>
          <ResourceAttributeDesignator
            AttributeId="department"
            DataType="string"/>
        </Apply>
        <!-- Business hours (9 AM - 5 PM) -->
        <Apply FunctionId="and">
          <Apply FunctionId="time-greater-than-or-equal">
            <EnvironmentAttributeDesignator
              AttributeId="current-time"
              DataType="time"/>
            <AttributeValue DataType="time">09:00:00</AttributeValue>
          </Apply>
          <Apply FunctionId="time-less-than-or-equal">
            <EnvironmentAttributeDesignator
              AttributeId="current-time"
              DataType="time"/>
            <AttributeValue DataType="time">17:00:00</AttributeValue>
          </Apply>
        </Apply>
      </Apply>
    </Condition>
  </Rule>

  <!-- Rule 3: Deny access to classified documents outside secure network -->
  <Rule RuleId="ClassifiedNetworkOnly" Effect="Deny">
    <Target>
      <Resources>
        <Resource>
          <ResourceMatch MatchId="string-equal">
            <AttributeValue DataType="string">classified</AttributeValue>
            <ResourceAttributeDesignator
              AttributeId="classification"
              DataType="string"/>
          </ResourceMatch>
        </Resource>
      </Resources>
    </Target>
    <Condition>
      <Apply FunctionId="not">
        <Apply FunctionId="ipAddress-in-range">
          <EnvironmentAttributeDesignator
            AttributeId="source-ip"
            DataType="ipAddress"/>
          <AttributeValue DataType="ipAddress">10.0.0.0/8</AttributeValue>
        </Apply>
      </Apply>
    </Condition>
  </Rule>

  <!-- Default deny -->
  <Rule RuleId="DefaultDeny" Effect="Deny"/>
</Policy>
```

#### Python ABAC Implementation

```python
# @nist ac-3 "Access enforcement"
# @nist ac-16 "Security attributes"
import json
from datetime import datetime, time
from ipaddress import ip_address, ip_network

class ABACEngine:
    """Attribute-Based Access Control policy engine."""

    def __init__(self, policy_file: str):
        with open(policy_file) as f:
            self.policies = json.load(f)

    def evaluate(self, subject: dict, resource: dict, action: str,
                 environment: dict) -> tuple[bool, str]:
        """
        Evaluate ABAC policy.

        @nist ac-3 "Access enforcement"
        @nist ac-16 "Security attributes"

        Args:
            subject: User attributes (id, role, department, clearance, etc.)
            resource: Resource attributes (type, owner, classification, etc.)
            action: Action being requested (read, write, delete)
            environment: Context attributes (time, ip_address, location, etc.)

        Returns:
            (allowed: bool, reason: str)
        """
        for policy in self.policies:
            if not self._matches_target(policy.get('target', {}), subject, resource, action):
                continue

            # Evaluate rules in order (first match wins)
            for rule in policy.get('rules', []):
                if self._evaluate_rule(rule, subject, resource, environment):
                    effect = rule.get('effect', 'deny')
                    reason = rule.get('description', f"Matched rule {rule.get('id')}")
                    return (effect == 'permit', reason)

        # Default deny
        return (False, "No matching policy found (default deny)")

    def _matches_target(self, target: dict, subject: dict,
                       resource: dict, action: str) -> bool:
        """Check if request matches policy target."""
        if 'resource_type' in target and resource.get('type') != target['resource_type']:
            return False
        if 'action' in target and action != target['action']:
            return False
        if 'subject_role' in target and subject.get('role') != target['subject_role']:
            return False
        return True

    def _evaluate_rule(self, rule: dict, subject: dict,
                      resource: dict, environment: dict) -> bool:
        """Evaluate rule conditions."""
        conditions = rule.get('conditions', [])

        for condition in conditions:
            if not self._evaluate_condition(condition, subject, resource, environment):
                return False

        return True

    def _evaluate_condition(self, condition: dict, subject: dict,
                          resource: dict, environment: dict) -> bool:
        """Evaluate individual condition."""
        operator = condition['operator']

        if operator == 'equals':
            left = self._get_attribute(condition['left'], subject, resource, environment)
            right = condition['right']
            return left == right

        elif operator == 'in':
            left = self._get_attribute(condition['left'], subject, resource, environment)
            right = condition['right']
            return left in right

        elif operator == 'time_between':
            current_time = datetime.fromisoformat(environment['current_time']).time()
            start = time.fromisoformat(condition['start'])
            end = time.fromisoformat(condition['end'])
            return start <= current_time <= end

        elif operator == 'ip_in_network':
            client_ip = ip_address(environment['ip_address'])
            network = ip_network(condition['network'])
            return client_ip in network

        elif operator == 'and':
            return all(
                self._evaluate_condition(c, subject, resource, environment)
                for c in condition['conditions']
            )

        elif operator == 'or':
            return any(
                self._evaluate_condition(c, subject, resource, environment)
                for c in condition['conditions']
            )

        return False

    def _get_attribute(self, path: str, subject: dict,
                      resource: dict, environment: dict) -> any:
        """Get attribute value from subject/resource/environment."""
        namespace, key = path.split('.', 1)

        if namespace == 'subject':
            return subject.get(key)
        elif namespace == 'resource':
            return resource.get(key)
        elif namespace == 'environment':
            return environment.get(key)

        return None

# Usage example
abac = ABACEngine('policies/document-access.json')

@app.route('/api/documents/<int:doc_id>')
@require_auth
def get_document(doc_id):
    doc = Document.query.get_or_404(doc_id)

    # Build attribute sets
    subject = {
        'id': current_user.id,
        'role': current_user.role,
        'department': current_user.department,
        'clearance_level': current_user.clearance_level
    }

    resource = {
        'type': 'document',
        'id': doc.id,
        'owner_id': doc.owner_id,
        'classification': doc.classification,
        'department': doc.department
    }

    environment = {
        'current_time': datetime.utcnow().isoformat(),
        'ip_address': request.remote_addr,
        'day_of_week': datetime.utcnow().strftime('%A')
    }

    # Evaluate policy
    allowed, reason = abac.evaluate(subject, resource, 'read', environment)

    # Audit
    audit_log.info(f"ABAC decision for user {current_user.id} on document {doc_id}: "
                   f"allowed={allowed}, reason={reason}")

    if not allowed:
        abort(403, f"Access denied: {reason}")

    return doc.to_dict()
```

---

### Policy Enforcement Points

**PEP (Policy Enforcement Point)** intercepts requests and enforces authorization decisions from the PDP (Policy Decision Point). Common locations: API gateway, middleware, service mesh.

#### Architecture

```
Client Request
    ↓
[API Gateway PEP] ──query──> [PDP (Policy Engine)]
    ↓                              ↓
[Service PEP] ────────────────> [Policy Store]
    ↓                              ↓
[Resource]                    [Attribute Store]
```

#### Express Middleware Example

See [templates/middleware.js](templates/middleware.js) for complete implementation.

```javascript
// @nist ac-3 "Access enforcement"
// @nist ac-6 "Least privilege"

const { ABACEngine } = require('./abac-engine');
const abac = new ABACEngine('./policies/main.json');

/**
 * Policy Enforcement Point (PEP) middleware
 * @nist ac-3 "Access enforcement"
 */
function enforcePolicyPEP(resourceExtractor, actionExtractor) {
  return async (req, res, next) => {
    try {
      // Extract subject attributes from authenticated user
      const subject = {
        id: req.user.id,
        role: req.user.role,
        department: req.user.department,
        clearance_level: req.user.clearance_level,
        groups: req.user.groups || []
      };

      // Extract resource attributes (custom per route)
      const resource = await resourceExtractor(req);

      // Extract action from HTTP method or custom function
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

      // Query Policy Decision Point (PDP)
      const [allowed, reason] = await abac.evaluate(
        subject, resource, action, environment
      );

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
        return res.status(403).json({
          error: 'Forbidden',
          message: `Access denied: ${reason}`,
          resource: resource.type,
          action: action
        });
      }

      // Attach authorization context for downstream use
      req.authz = { subject, resource, action, allowed };
      next();
    } catch (error) {
      console.error('Authorization error:', error);
      res.status(500).json({ error: 'Authorization service error' });
    }
  };
}

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

// Usage example
app.get('/api/documents/:id',
  authenticateJWT,
  enforcePolicyPEP(
    // Resource extractor
    async (req) => {
      const doc = await Document.findById(req.params.id);
      return {
        type: 'document',
        id: doc.id,
        owner_id: doc.owner_id,
        classification: doc.classification,
        department: doc.department
      };
    },
    // Action extractor (optional, defaults to HTTP method mapping)
    (req) => 'read'
  ),
  async (req, res) => {
    const doc = await Document.findById(req.params.id);
    res.json(doc);
  }
);
```

#### Multi-Layer Enforcement

**Defense in Depth**: Enforce at multiple layers.

```javascript
// Layer 1: API Gateway (coarse-grained)
app.use('/api/admin/*', requireRole('admin'));

// Layer 2: Route middleware (fine-grained)
app.delete('/api/documents/:id',
  authenticateJWT,
  enforcePolicyPEP(/* ... */),
  deleteDocument
);

// Layer 3: Service layer (resource ownership)
async function deleteDocument(req, res) {
  const doc = await Document.findById(req.params.id);

  // Extra check: ensure user owns the resource
  if (doc.owner_id !== req.user.id && !req.user.hasRole('admin')) {
    return res.status(403).json({ error: 'Not the owner' });
  }

  await doc.delete();
  res.json({ status: 'deleted' });
}
```

---

### OAuth2 Scopes and Claims

**OAuth2 scopes** provide coarse-grained authorization. **JWT claims** carry fine-grained attributes for ABAC.

#### Scope Design

**Best Practices:**

- Use `resource:action` format (e.g., `documents:read`, `users:write`)
- Separate read/write/admin scopes
- Use `*` sparingly (e.g., `admin:*` for full access)

```javascript
// @nist ac-3 "Access enforcement"
// @nist ac-6 "Least privilege"

// Scope definitions
const scopes = {
  'profile:read': 'Read user profile',
  'profile:write': 'Update user profile',
  'documents:read': 'Read documents',
  'documents:write': 'Create/update documents',
  'documents:delete': 'Delete documents',
  'admin:users': 'Manage users (admin)',
  'admin:*': 'Full administrative access'
};

// OAuth2 authorization endpoint
app.get('/oauth/authorize', (req, res) => {
  const { client_id, scope, redirect_uri, state } = req.query;

  // Validate client
  const client = clients.find(c => c.id === client_id);
  if (!client) {
    return res.status(400).json({ error: 'invalid_client' });
  }

  // Parse and validate scopes
  const requestedScopes = scope.split(' ');
  const validScopes = requestedScopes.filter(s => scopes[s]);

  // Show consent screen
  res.render('consent', {
    client: client,
    scopes: validScopes.map(s => ({ name: s, description: scopes[s] })),
    redirect_uri: redirect_uri,
    state: state
  });
});

// Token endpoint - embed scopes in JWT
app.post('/oauth/token', async (req, res) => {
  // ... validate grant, exchange code for token ...

  const accessToken = jwt.sign(
    {
      sub: user.id,
      scope: grantedScopes.join(' '),  // Space-delimited scopes
      iss: 'auth.example.com',
      aud: 'api.example.com'
    },
    privateKey,
    { algorithm: 'RS256', expiresIn: '15m' }
  );

  res.json({
    access_token: accessToken,
    token_type: 'Bearer',
    expires_in: 900,
    scope: grantedScopes.join(' ')
  });
});
```

#### Scope Validation Middleware

```javascript
// @nist ac-3 "Access enforcement"
function requireScope(...requiredScopes) {
  return (req, res, next) => {
    const token = req.user; // Decoded JWT from authenticateJWT
    const tokenScopes = token.scope ? token.scope.split(' ') : [];

    // Check if token has any of the required scopes
    const hasScope = requiredScopes.some(required => {
      if (required.endsWith(':*')) {
        // Wildcard match (e.g., admin:* matches admin:users, admin:roles)
        const prefix = required.slice(0, -1);
        return tokenScopes.some(s => s.startsWith(prefix));
      }
      return tokenScopes.includes(required);
    });

    if (!hasScope) {
      return res.status(403).json({
        error: 'insufficient_scope',
        message: `Required scopes: ${requiredScopes.join(' or ')}`,
        provided: tokenScopes.join(' ')
      });
    }

    next();
  };
}

// Usage
app.get('/api/documents',
  authenticateJWT,
  requireScope('documents:read'),
  listDocuments
);

app.delete('/api/documents/:id',
  authenticateJWT,
  requireScope('documents:delete', 'admin:*'),  // Either scope works
  deleteDocument
);
```

#### Claims-Based Authorization (ABAC with JWT)

Embed user attributes in JWT for distributed ABAC.

```javascript
// Token with rich claims
const accessToken = jwt.sign(
  {
    sub: user.id,
    email: user.email,
    role: user.role,
    department: user.department,
    clearance_level: user.clearance_level,
    scope: 'documents:read documents:write',
    // Custom claims (use namespaced keys to avoid collisions)
    'https://example.com/claims/groups': user.groups,
    'https://example.com/claims/manager_id': user.manager_id
  },
  privateKey,
  { algorithm: 'RS256', expiresIn: '15m' }
);

// Validate claims in middleware
function requireClaim(claimPath, expectedValue) {
  return (req, res, next) => {
    const token = req.user;
    const actualValue = getNestedProperty(token, claimPath);

    if (actualValue !== expectedValue) {
      return res.status(403).json({
        error: 'Forbidden',
        message: `Required claim ${claimPath}=${expectedValue}`
      });
    }

    next();
  };
}

// Usage: only finance department can access
app.get('/api/financial-reports',
  authenticateJWT,
  requireClaim('department', 'finance'),
  getFinancialReports
);
```

---

### Testing Authorization

Comprehensive testing ensures authorization logic is correct and secure.

#### Unit Tests

```javascript
// @nist ac-3 "Access enforcement"
const { RBACManager } = require('./rbac-manager');
const { expect } = require('chai');

describe('RBACManager', () => {
  let rbac;

  beforeEach(() => {
    rbac = new RBACManager(testDb);
  });

  describe('has_permission', () => {
    it('should grant permission when user has direct role', async () => {
      // Arrange: user has 'editor' role with 'documents:write' permission
      await seedRole('editor', [{ resource: 'documents', action: 'write' }]);
      await assignRole(userId, 'editor');

      // Act
      const result = rbac.has_permission(userId, 'documents', 'write');

      // Assert
      expect(result).to.be.true;
    });

    it('should grant permission through role hierarchy', async () => {
      // Arrange: admin inherits from editor
      await seedRole('editor', [{ resource: 'documents', action: 'write' }]);
      await seedRole('admin', [], 'editor');  // admin parent is editor
      await assignRole(userId, 'admin');

      // Act
      const result = rbac.has_permission(userId, 'documents', 'write');

      // Assert
      expect(result).to.be.true;
    });

    it('should deny permission when user lacks role', async () => {
      // Arrange: user has 'viewer' role (no write permission)
      await seedRole('viewer', [{ resource: 'documents', action: 'read' }]);
      await assignRole(userId, 'viewer');

      // Act
      const result = rbac.has_permission(userId, 'documents', 'write');

      // Assert
      expect(result).to.be.false;
    });

    it('should respect temporary role expiration', async () => {
      // Arrange: user has expired temporary role
      const yesterday = new Date(Date.now() - 24 * 60 * 60 * 1000);
      await assignRole(userId, 'editor', { expires_at: yesterday });

      // Act
      const result = rbac.has_permission(userId, 'documents', 'write');

      // Assert
      expect(result).to.be.false;
    });
  });

  describe('audit_authorization', () => {
    it('should log authorization decisions', async () => {
      // Act
      await rbac.audit_authorization(userId, 'documents', 'write', true, 'Has permission');

      // Assert
      const audit = await db.query('SELECT * FROM authorization_audit WHERE user_id = ?', [userId]);
      expect(audit).to.have.lengthOf(1);
      expect(audit[0].allowed).to.be.true;
      expect(audit[0].reason).to.equal('Has permission');
    });
  });
});
```

#### Integration Tests

```python
# @nist ac-3 "Access enforcement"
import pytest
from flask import Flask
from app import create_app, db
from app.models import User, Role, Permission

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_user_can_access_own_document(client, auth_headers):
    """Test user can read their own document."""
    # Arrange
    user = create_user('alice', role='user')
    doc = create_document(owner=user, title='Alice Document')

    # Act
    response = client.get(
        f'/api/documents/{doc.id}',
        headers=auth_headers(user)
    )

    # Assert
    assert response.status_code == 200
    assert response.json['title'] == 'Alice Document'

def test_user_cannot_access_others_document(client, auth_headers):
    """Test user cannot read another user's document."""
    # Arrange
    alice = create_user('alice', role='user')
    bob = create_user('bob', role='user')
    doc = create_document(owner=bob, title='Bob Document')

    # Act
    response = client.get(
        f'/api/documents/{doc.id}',
        headers=auth_headers(alice)
    )

    # Assert
    assert response.status_code == 403
    assert 'Access denied' in response.json['message']

def test_admin_can_access_all_documents(client, auth_headers):
    """Test admin can read any document."""
    # Arrange
    admin = create_user('admin', role='admin')
    user = create_user('user', role='user')
    doc = create_document(owner=user, title='User Document')

    # Act
    response = client.get(
        f'/api/documents/{doc.id}',
        headers=auth_headers(admin)
    )

    # Assert
    assert response.status_code == 200
    assert response.json['title'] == 'User Document'

def test_manager_can_access_department_docs_during_business_hours(client, auth_headers):
    """Test ABAC policy: manager can access dept docs 9-5."""
    # Arrange
    manager = create_user('manager', role='manager', department='engineering')
    doc = create_document(owner=None, department='engineering')

    # Act (during business hours)
    with freeze_time('2025-10-17 14:00:00'):  # 2 PM
        response = client.get(
            f'/api/documents/{doc.id}',
            headers=auth_headers(manager)
        )

    # Assert
    assert response.status_code == 200

def test_manager_cannot_access_department_docs_outside_hours(client, auth_headers):
    """Test ABAC policy: manager blocked outside 9-5."""
    # Arrange
    manager = create_user('manager', role='manager', department='engineering')
    doc = create_document(owner=None, department='engineering')

    # Act (outside business hours)
    with freeze_time('2025-10-17 22:00:00'):  # 10 PM
        response = client.get(
            f'/api/documents/{doc.id}',
            headers=auth_headers(manager)
        )

    # Assert
    assert response.status_code == 403
    assert 'business hours' in response.json['message'].lower()

def test_authorization_audit_trail(client, auth_headers):
    """Test all authorization decisions are logged."""
    # Arrange
    user = create_user('user', role='user')
    doc = create_document(owner=user)

    # Act
    client.get(f'/api/documents/{doc.id}', headers=auth_headers(user))

    # Assert
    audit = db.session.query(AuthorizationAudit).filter_by(user_id=user.id).first()
    assert audit is not None
    assert audit.resource == f'document:{doc.id}'
    assert audit.action == 'read'
    assert audit.allowed is True
```

#### Policy Testing

```python
# Test ABAC policies in isolation
from abac_engine import ABACEngine

def test_owner_access_policy():
    """Test policy: users can access their own documents."""
    engine = ABACEngine('policies/test-policy.json')

    subject = {'id': 123, 'role': 'user'}
    resource = {'type': 'document', 'owner_id': 123}
    environment = {}

    allowed, reason = engine.evaluate(subject, resource, 'read', environment)

    assert allowed is True
    assert 'owner' in reason.lower()

def test_department_access_policy():
    """Test policy: same department access."""
    engine = ABACEngine('policies/test-policy.json')

    subject = {'id': 123, 'role': 'manager', 'department': 'finance'}
    resource = {'type': 'document', 'department': 'finance'}
    environment = {'current_time': '2025-10-17T14:00:00'}

    allowed, reason = engine.evaluate(subject, resource, 'read', environment)

    assert allowed is True
```

---

### NIST 800-53 Compliance

#### AC-3: Access Enforcement

**Control**: The information system enforces approved authorizations for logical access to information and system resources.

**Implementation:**

- ✅ PEP at API gateway and service layer
- ✅ PDP evaluates policies before granting access
- ✅ Deny by default (fail secure)
- ✅ Authorization decisions logged (audit trail)

```python
# @nist ac-3 "Access enforcement"
@require_permission('documents', 'read')
def get_document(doc_id):
    # PEP enforces policy before reaching this handler
    pass
```

#### AC-4: Information Flow Enforcement

**Control**: The information system enforces approved authorizations for controlling the flow of information within the system and between interconnected systems.

**Implementation:**

- ✅ ABAC policies control data flow based on classification
- ✅ Network-based restrictions (IP allowlisting)
- ✅ Cross-department access controls

```xml
<!-- @nist ac-4 "Information flow enforcement" -->
<Rule RuleId="ClassifiedNetworkOnly" Effect="Deny">
  <!-- Deny classified doc access outside secure network -->
</Rule>
```

#### AC-6: Least Privilege

**Control**: The organization employs the principle of least privilege, allowing only authorized accesses for users necessary to accomplish assigned tasks.

**Implementation:**

- ✅ Users granted minimum required permissions
- ✅ Role hierarchy (users don't automatically get admin)
- ✅ Temporary permissions with expiration
- ✅ Regular permission audits

```python
# @nist ac-6 "Least privilege"
# Users assigned specific roles, not blanket admin access
user.roles = ['documents:read', 'documents:write']  # NOT 'admin:*'
```

#### AC-2: Account Management

**Control**: The organization manages information system accounts including creation, enabling, modification, review, disabling, and removal.

**Implementation:**

- ✅ Role assignment audit trail (granted_by, granted_at)
- ✅ Temporary role expiration (expires_at)
- ✅ Account review process

```sql
-- @nist ac-2 "Account management"
CREATE TABLE user_roles (
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP,
    expires_at TIMESTAMP  -- Support temporary access
);
```

#### AC-5: Separation of Duties

**Control**: The organization separates duties of individuals to reduce the risk of malevolent activity without collusion.

**Implementation:**

- ✅ Multi-approval workflows for critical operations
- ✅ No single user has complete control
- ✅ Admin operations require dual authorization

```python
# @nist ac-5 "Separation of duties"
@require_approvals(count=2, roles=['manager', 'admin'])
def delete_all_documents():
    # Requires 2 approvals from managers/admins
    pass
```

#### AC-16: Security Attributes

**Control**: The information system associates and maintains security attributes with information.

**Implementation:**

- ✅ Resource attributes (classification, department, owner)
- ✅ User attributes (clearance_level, department, role)
- ✅ ABAC policies use attributes for decisions

```python
# @nist ac-16 "Security attributes"
resource = {
    'classification': 'confidential',
    'department': 'finance',
    'owner_id': user.id
}
```

#### Compliance Checklist

- [ ] **AC-3**: All resources protected by PEP, default deny enforced
- [ ] **AC-4**: Cross-boundary access controlled by classification/network
- [ ] **AC-6**: Least privilege verified, no unnecessary admin grants
- [ ] **AC-2**: Account management audit trail complete
- [ ] **AC-5**: Separation of duties for critical operations
- [ ] **AC-16**: Security attributes assigned and maintained
- [ ] **AU-2**: All authorization decisions logged with context

See [resources/nist-ac-controls.md](resources/nist-ac-controls.md) for detailed control mappings.

---

## Level 3: Mastery Resources

### Reference Materials

- [NIST SP 800-53 Rev 5 - Access Control Family](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [XACML 3.0 Core Specification](http://docs.oasis-open.org/xacml/3.0/xacml-3.0-core-spec-os-en.html)
- [OAuth 2.0 Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-security-topics)
- [NIST RBAC Model](https://csrc.nist.gov/projects/role-based-access-control)
- [Cedar Policy Language (AWS)](https://www.cedarpolicy.com/)
- [Open Policy Agent (OPA) Rego](https://www.openpolicyagent.org/docs/latest/policy-language/)

### Templates

- [templates/rbac-policy.yaml](templates/rbac-policy.yaml) - Declarative RBAC policy
- [templates/abac-policy.json](templates/abac-policy.json) - ABAC policy with conditions
- [templates/middleware.js](templates/middleware.js) - Express PEP middleware
- [templates/policy-enforcement.py](templates/policy-enforcement.py) - Python RBAC/ABAC
- [scripts/generate-rbac.sh](scripts/generate-rbac.sh) - Auto-generate RBAC from org chart
- [resources/nist-ac-controls.md](resources/nist-ac-controls.md) - NIST control checklist

### Advanced Topics

- **Policy Languages**: XACML, Rego (OPA), Cedar
- **Distributed Authorization**: Service mesh (Istio), sidecar pattern
- **ReBAC**: Relationship-Based Access Control (Google Zanzibar)
- **Fine-Grained Authorization**: Field-level, row-level security
- **Dynamic Permissions**: Context-aware, time-based, location-based
- **Authorization at Scale**: Caching strategies, policy compilation

### Tools

- **Open Policy Agent (OPA)**: General-purpose policy engine
- **Keycloak**: Identity and access management with RBAC/ABAC
- **Casbin**: Authorization library for multiple languages
- **AWS IAM/Cedar**: Cloud authorization services
- **Oso**: Authorization framework with Polar language

### Practice Exercises

1. Implement RBAC for a multi-tenant SaaS application
2. Design ABAC policy for healthcare system (HIPAA compliance)
3. Build PEP middleware for microservices architecture
4. Create dynamic permission system with temporary grants
5. Implement separation of duties for financial system
6. Audit existing authorization logic for NIST compliance

---

**Next Steps**: Review [api-security](../api-security/SKILL.md) for securing APIs, [authentication-security](../authentication/SKILL.md) for auth fundamentals, and [secrets-management](../secrets-management/SKILL.md) for credential handling.
