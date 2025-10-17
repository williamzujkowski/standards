#!/bin/bash
# @nist ac-2 "Account management"
# @nist ac-3 "Access enforcement"
# Generate RBAC roles and permissions from organizational chart

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default values
ORG_CHART_FILE="${1:-org-chart.yaml}"
OUTPUT_FILE="${2:-rbac-policy.yaml}"

usage() {
    cat << EOF
Usage: $0 [ORG_CHART_FILE] [OUTPUT_FILE]

Generate RBAC policy from organizational chart.

Arguments:
    ORG_CHART_FILE    Input YAML with org structure (default: org-chart.yaml)
    OUTPUT_FILE       Output RBAC policy file (default: rbac-policy.yaml)

Example org-chart.yaml:
    departments:
      - name: engineering
        teams:
          - name: backend
            roles: [developer, senior_developer, tech_lead]
          - name: frontend
            roles: [developer, senior_developer]
      - name: operations
        teams:
          - name: sre
            roles: [sre_engineer, sre_lead]

EOF
    exit 1
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
    usage
fi

if [[ ! -f "$ORG_CHART_FILE" ]]; then
    echo "Error: Org chart file not found: $ORG_CHART_FILE"
    usage
fi

echo "Generating RBAC policy from $ORG_CHART_FILE..."

# Parse org chart and generate roles
python3 << PYPYTHON
import yaml
import sys

# Load org chart
with open('$ORG_CHART_FILE') as f:
    org = yaml.safe_load(f)

# Define permission mappings by role type
PERMISSION_MAPPINGS = {
    'developer': ['documents:read', 'documents:write', 'code:read', 'code:write'],
    'senior_developer': ['documents:read', 'documents:write', 'code:read', 'code:write', 'code:review'],
    'tech_lead': ['documents:*', 'code:*', 'team:read'],
    'manager': ['documents:*', 'team:read', 'team:write', 'reports:read'],
    'sre_engineer': ['infrastructure:read', 'infrastructure:write', 'deployments:execute'],
    'sre_lead': ['infrastructure:*', 'deployments:*', 'team:read'],
    'admin': ['users:*', 'roles:*', 'audit:read'],
    'superadmin': ['*:*']
}

# Build RBAC policy
policy = {
    'version': '1.0',
    'description': 'Auto-generated RBAC policy from organizational chart',
    'permissions': [],
    'roles': [],
    'defaults': {
        'new_user_role': 'guest'
    }
}

# Extract unique permissions
all_permissions = set()
for perms in PERMISSION_MAPPINGS.values():
    for perm in perms:
        if ':' in perm and perm != '*:*':
            resource, action = perm.split(':', 1)
            all_permissions.add((resource, action))

# Add permission definitions
for resource, action in sorted(all_permissions):
    policy['permissions'].append({
        'id': f'{resource}:{action}',
        'resource': resource,
        'action': action,
        'description': f'{action.title()} {resource}'
    })

# Generate roles from org chart
role_hierarchy = {
    'guest': None,
    'user': 'guest'
}

for dept in org.get('departments', []):
    dept_name = dept['name']
    
    for team in dept.get('teams', []):
        team_name = team['name']
        
        for role_name in team.get('roles', []):
            full_role_name = f'{dept_name}_{team_name}_{role_name}'
            
            # Determine parent role
            if role_name == 'developer':
                parent = 'user'
            elif role_name == 'senior_developer':
                parent = f'{dept_name}_{team_name}_developer'
            elif role_name in ['tech_lead', 'manager']:
                parent = 'user'
            else:
                parent = 'user'
            
            role_hierarchy[full_role_name] = parent
            
            # Get permissions for this role type
            permissions = PERMISSION_MAPPINGS.get(role_name, ['documents:read'])
            
            policy['roles'].append({
                'name': full_role_name,
                'description': f'{role_name.replace("_", " ").title()} in {dept_name}/{team_name}',
                'parent': parent,
                'permissions': permissions
            })

# Add common roles
for common_role in ['admin', 'superadmin']:
    policy['roles'].append({
        'name': common_role,
        'description': f'{common_role.title()} role',
        'parent': 'user' if common_role != 'superadmin' else 'admin',
        'permissions': PERMISSION_MAPPINGS[common_role]
    })

# Write output
with open('$OUTPUT_FILE', 'w') as f:
    f.write('# Auto-generated RBAC policy\n')
    f.write('# @nist ac-2 "Account management"\n')
    f.write('# @nist ac-3 "Access enforcement"\n\n')
    yaml.dump(policy, f, default_flow_style=False, sort_keys=False)

print(f"Generated {len(policy['roles'])} roles with {len(policy['permissions'])} permissions")
print(f"Output written to: $OUTPUT_FILE")

PYPYTHON

echo "RBAC policy generation complete!"
echo
echo "Next steps:"
echo "  1. Review generated policy: $OUTPUT_FILE"
echo "  2. Customize permissions as needed"
echo "  3. Load policy into database"
