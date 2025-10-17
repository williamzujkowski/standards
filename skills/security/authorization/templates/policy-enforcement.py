# @nist ac-3 "Access enforcement"
# @nist ac-6 "Least privilege"
"""
Python Policy Enforcement - RBAC and ABAC implementation
Supports Flask/Django applications with SQLAlchemy
"""

from functools import wraps
from datetime import datetime
from typing import Optional, List, Tuple
from flask import abort, g, request
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

    def _get_user_roles_with_hierarchy(self, user_id: int) -> List[int]:
        """Get all roles including parent roles."""
        from models import UserRole, Role

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

    def _get_parent_roles(self, role_id: int) -> set:
        """Recursively get all parent roles."""
        from models import Role

        parents = set()
        role = self.db.session.query(Role).get(role_id)

        if role and role.parent_role_id:
            parents.add(role.parent_role_id)
            parents.update(self._get_parent_roles(role.parent_role_id))

        return parents

    def audit_authorization(self, user_id: int, resource: str, action: str,
                          allowed: bool, reason: Optional[str] = None):
        """
        Log authorization decision for compliance.

        @nist au-2 "Audit events"
        @nist ac-3 "Access enforcement"
        """
        from models import AuthorizationAudit

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

    def clear_cache(self):
        """Clear permission cache (call after role changes)."""
        self._permission_cache.clear()


def require_permission(resource: str, action: str):
    """
    Decorator to enforce permissions on routes.

    @nist ac-3 "Access enforcement"

    Usage:
        @app.route('/api/documents/<int:doc_id>', methods=['DELETE'])
        @require_auth
        @require_permission('documents', 'delete')
        def delete_document(doc_id):
            ...
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


def require_role(*allowed_roles):
    """
    Decorator to enforce role membership.

    @nist ac-3 "Access enforcement"
    @nist ac-6 "Least privilege"

    Usage:
        @app.route('/api/admin/users')
        @require_auth
        @require_role('admin', 'superadmin')
        def list_users():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.current_user.role not in allowed_roles:
                abort(403, f"Required role: {' or '.join(allowed_roles)}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_ownership(resource_getter):
    """
    Decorator to enforce resource ownership.

    @nist ac-3 "Access enforcement"

    Usage:
        @app.route('/api/documents/<int:doc_id>')
        @require_auth
        @require_ownership(lambda doc_id: Document.query.get(doc_id))
        def get_document(doc_id):
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            resource = resource_getter(*args, **kwargs)

            if not resource:
                abort(404, "Resource not found")

            # Check ownership or admin override
            if resource.owner_id != g.current_user.id and g.current_user.role != 'admin':
                abort(403, "You do not own this resource")

            return f(*args, **kwargs)
        return decorated_function
    return decorator


class ABACEngine:
    """
    Attribute-Based Access Control policy engine.

    @nist ac-3 "Access enforcement"
    @nist ac-16 "Security attributes"
    """

    def __init__(self, policy_file: str):
        import json
        with open(policy_file) as f:
            self.policies = json.load(f)['policies']

    def evaluate(self, subject: dict, resource: dict, action: str,
                 environment: dict) -> Tuple[bool, str]:
        """
        Evaluate ABAC policy.

        Returns: (allowed: bool, reason: str)
        """
        for policy in self.policies:
            if not self._matches_target(policy.get('target', {}), subject, resource, action):
                continue

            # Evaluate conditions
            if self._evaluate_conditions(policy.get('conditions', []), subject, resource, environment):
                effect = policy.get('effect', 'deny')
                reason = policy.get('description', f"Matched policy {policy.get('id')}")
                return (effect == 'permit', reason)

        # Default deny
        return (False, "No matching policy found (default deny)")

    def _matches_target(self, target: dict, subject: dict, resource: dict, action: str) -> bool:
        """Check if request matches policy target."""
        if 'resource_type' in target and resource.get('type') != target['resource_type']:
            return False
        if 'action' in target and action != target['action']:
            return False
        if 'subject_role' in target and subject.get('role') != target['subject_role']:
            return False
        return True

    def _evaluate_conditions(self, conditions: list, subject: dict,
                            resource: dict, environment: dict) -> bool:
        """Evaluate all conditions (AND logic)."""
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
            return left == condition['right']

        elif operator == 'in':
            left = self._get_attribute(condition['left'], subject, resource, environment)
            return left in condition['right']

        elif operator == 'time_between':
            current_time = datetime.fromisoformat(environment['current_time']).time()
            start = datetime.strptime(condition['start'], '%H:%M:%S').time()
            end = datetime.strptime(condition['end'], '%H:%M:%S').time()
            return start <= current_time <= end

        elif operator == 'ip_in_network':
            from ipaddress import ip_address, ip_network
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

        elif operator == 'not':
            return not self._evaluate_condition(condition['condition'], subject, resource, environment)

        return False

    def _get_attribute(self, path: str, subject: dict, resource: dict, environment: dict):
        """Get attribute value from subject/resource/environment."""
        namespace, key = path.split('.', 1)

        if namespace == 'subject':
            return subject.get(key)
        elif namespace == 'resource':
            return resource.get(key)
        elif namespace == 'environment':
            return environment.get(key)

        return None
