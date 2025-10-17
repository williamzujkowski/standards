# NIST 800-53 Access Control (AC) Family - Authorization Controls Checklist

> **Purpose**: Detailed implementation guidance for NIST 800-53 Rev 5 Access Control controls related to authorization.

---

## AC-2: Account Management

**Control Statement**: The organization manages information system accounts including creation, enabling, modification, review, disabling, and removal.

### Implementation Requirements

- [ ] **AC-2(1)**: Automated account management (create/modify/disable accounts via API)
- [ ] **AC-2(2)**: Automated removal of temporary/emergency accounts after time period
- [ ] **AC-2(3)**: Disable accounts after 90 days of inactivity
- [ ] **AC-2(4)**: Audit account creation, modification, disabling, and removal
- [ ] **AC-2(7)**: Role-based schemes for access authorization
- [ ] **AC-2(11)**: Usage conditions enforced (time-of-day, location, device)
- [ ] **AC-2(12)**: Account monitoring for atypical usage

### Implementation Example

```sql
CREATE TABLE user_roles (
    user_id INTEGER,
    role_id INTEGER,
    granted_by INTEGER REFERENCES users(id),
    granted_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,  -- AC-2(2): temporary access
    last_used TIMESTAMP,   -- AC-2(3): inactivity tracking
    PRIMARY KEY (user_id, role_id)
);

-- Audit trail for AC-2(4)
CREATE TABLE account_audit (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    action VARCHAR(50),  -- 'created', 'modified', 'disabled', 'removed'
    performed_by INTEGER,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

---

## AC-3: Access Enforcement

**Control Statement**: The information system enforces approved authorizations for logical access to information and system resources.

### Implementation Requirements

- [ ] **AC-3**: Policy Enforcement Point (PEP) at all entry points
- [ ] **AC-3**: Policy Decision Point (PDP) evaluates all requests
- [ ] **AC-3**: Default deny (fail secure)
- [ ] **AC-3**: Authorization decisions logged
- [ ] **AC-3(3)**: Mandatory access control enforced
- [ ] **AC-3(4)**: Discretionary access control enforced
- [ ] **AC-3(7)**: Role-based access control enforced
- [ ] **AC-3(8)**: Revoke access on role/privilege change
- [ ] **AC-3(9)**: Controlled release of information

### Implementation Example

```python
# Policy Enforcement Point (PEP)
@app.route('/api/documents/<doc_id>')
@require_auth
@enforce_policy  # AC-3: Enforce authorization
def get_document(doc_id):
    # Policy evaluated before reaching here
    pass

# Default deny (AC-3)
def enforce_policy(f):
    def wrapper(*args, **kwargs):
        allowed, reason = pdp.evaluate(subject, resource, action, environment)
        audit_log.info(f"Authorization: {allowed} - {reason}")  # AC-3: Audit
        if not allowed:
            abort(403, "Access denied")
        return f(*args, **kwargs)
    return wrapper
```

---

## AC-4: Information Flow Enforcement

**Control Statement**: The information system enforces approved authorizations for controlling the flow of information within the system and between interconnected systems.

### Implementation Requirements

- [ ] **AC-4**: Cross-domain access controls enforced
- [ ] **AC-4**: Classification-based restrictions enforced
- [ ] **AC-4**: Network-based access controls (IP allowlisting)
- [ ] **AC-4(4)**: Flow control for encrypted information
- [ ] **AC-4(17)**: Domain authentication for flow enforcement
- [ ] **AC-4(21)**: Physical/logical separation of information flows

### Implementation Example

```python
# AC-4: Network-based flow control
def evaluate_policy(subject, resource, environment):
    # Deny classified docs outside secure network
    if resource['classification'] == 'classified':
        if not is_ip_in_secure_network(environment['ip_address']):
            return (False, "Classified documents require secure network")
    
    # Cross-department flow control
    if subject['department'] != resource['department']:
        if not subject['role'] in ['admin', 'auditor']:
            return (False, "Cross-department access denied")
    
    return (True, "Flow allowed")
```

---

## AC-5: Separation of Duties

**Control Statement**: The organization separates duties of individuals to reduce the risk of malevolent activity without collusion.

### Implementation Requirements

- [ ] **AC-5**: Define conflicting duties and responsibilities
- [ ] **AC-5**: Implement separation in role assignments
- [ ] **AC-5**: No single user has complete control over critical processes
- [ ] **AC-5**: Multi-person approval for sensitive operations
- [ ] **AC-5(3)**: Dual authorization for high-risk operations

### Implementation Example

```python
# AC-5: Separation of duties
MUTUALLY_EXCLUSIVE_ROLES = [
    ('admin', 'auditor'),         # Admins can't audit themselves
    ('developer', 'approver'),    # Developers can't approve own code
    ('requestor', 'approver')     # Can't approve own requests
]

def assign_role(user_id, new_role):
    current_roles = get_user_roles(user_id)
    
    # Check for conflicts (AC-5)
    for role_a, role_b in MUTUALLY_EXCLUSIVE_ROLES:
        if new_role == role_a and role_b in current_roles:
            raise ConflictError(f"Cannot assign {new_role}: conflicts with {role_b}")
        if new_role == role_b and role_a in current_roles:
            raise ConflictError(f"Cannot assign {new_role}: conflicts with {role_a}")
    
    db.assign_role(user_id, new_role)

# AC-5(3): Dual authorization
@require_approvals(count=2, roles=['manager', 'admin'])
def delete_all_data():
    # Requires 2 approvals from managers/admins
    pass
```

---

## AC-6: Least Privilege

**Control Statement**: The organization employs the principle of least privilege, allowing only authorized accesses for users necessary to accomplish assigned tasks.

### Implementation Requirements

- [ ] **AC-6**: Users granted minimum permissions required
- [ ] **AC-6**: Regular review of user permissions
- [ ] **AC-6(1)**: Explicit authorization for privileged functions
- [ ] **AC-6(2)**: Non-privileged accounts for non-privileged functions
- [ ] **AC-6(5)**: Privileged accounts restricted to specific devices
- [ ] **AC-6(7)**: Review of user privileges every 90 days
- [ ] **AC-6(9)**: Log execution of privileged functions

### Implementation Example

```python
# AC-6: Least privilege enforcement
def assign_role(user_id, role):
    # AC-6(1): Explicit authorization for privileged roles
    if role in ['admin', 'superadmin']:
        if not current_user.has_permission('roles:grant_privileged'):
            raise PermissionError("Cannot grant privileged role")
        audit_log.warning(f"Privileged role {role} granted to user {user_id}")
    
    db.assign_role(user_id, role)

# AC-6(2): Non-privileged accounts
def get_user_for_operation(operation):
    if operation in PRIVILEGED_OPERATIONS:
        return get_privileged_user()
    else:
        return get_service_account()  # Non-privileged

# AC-6(7): Regular permission review
def review_user_permissions():
    users = db.query("SELECT user_id FROM user_roles WHERE granted_at < NOW() - INTERVAL '90 days'")
    for user in users:
        notify_manager(user, "Permission review required")
```

---

## AC-16: Security Attributes

**Control Statement**: The information system associates and maintains security attributes with information.

### Implementation Requirements

- [ ] **AC-16**: Security attributes assigned to all resources
- [ ] **AC-16**: User attributes maintained and current
- [ ] **AC-16**: Environment attributes captured in authorization
- [ ] **AC-16(1)**: Dynamic attribute association
- [ ] **AC-16(3)**: Maintenance of attribute associations
- [ ] **AC-16(5)**: Attribute displays for authorized users

### Implementation Example

```python
# AC-16: Security attributes
resource_attributes = {
    'type': 'document',
    'id': 12345,
    'owner_id': 456,
    'classification': 'confidential',  # AC-16: Security attribute
    'department': 'finance',           # AC-16: Organizational attribute
    'created_at': '2025-10-17T10:00:00',
    'sensitivity': 'high'              # AC-16: Data sensitivity
}

subject_attributes = {
    'id': 789,
    'role': 'manager',
    'department': 'finance',
    'clearance_level': 3,              # AC-16: Security clearance
    'groups': ['finance_team', 'managers']
}

environment_attributes = {
    'current_time': '2025-10-17T14:30:00',
    'ip_address': '10.0.1.50',         # AC-16: Network context
    'day_of_week': 'Thursday',
    'device_type': 'laptop'            # AC-16: Device attribute
}

# Use attributes in policy evaluation (AC-16)
allowed = abac.evaluate(subject_attributes, resource_attributes, 'read', environment_attributes)
```

---

## Compliance Checklist

### Pre-Production

- [ ] AC-2: Account management procedures documented and implemented
- [ ] AC-3: PEP deployed at all entry points (API gateway, service layer)
- [ ] AC-3: PDP evaluates all authorization requests
- [ ] AC-4: Cross-domain and classification controls enforced
- [ ] AC-5: Separation of duties defined and enforced
- [ ] AC-6: Least privilege review completed
- [ ] AC-16: Security attributes assigned to all resources

### Production

- [ ] AC-2(4): Account audit logs reviewed weekly
- [ ] AC-3: Authorization logs monitored for anomalies
- [ ] AC-6(7): User permission reviews conducted quarterly
- [ ] AC-16(3): Attribute maintenance procedures in place

### Continuous

- [ ] Authorization decisions logged with full context (AC-3, AU-2)
- [ ] Failed authorization attempts trigger alerts (AC-3)
- [ ] Privileged role grants logged and reviewed (AC-6(9))
- [ ] Policy updates tested before deployment

---

## References

- [NIST SP 800-53 Rev 5](https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final)
- [NIST RBAC Model](https://csrc.nist.gov/projects/role-based-access-control)
- [NIST Attribute-Based Access Control](https://csrc.nist.gov/projects/attribute-based-access-control)
