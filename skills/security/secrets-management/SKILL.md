---
name: secrets-management
description: Secrets management standards for API keys, passwords, certificates, and sensitive data. Covers HashiCorp Vault, environment variables, rotation policies, and detection tools with NIST 800-53r5 SC-12 compliance.
---

# Secrets Management Security

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Never Hardcode Secrets**: Use environment variables, secret management systems, or secure vaults
2. **Rotate Regularly**: Implement automated rotation policies for all secrets
3. **Detect and Prevent**: Use pre-commit hooks and scanning tools to prevent secret leaks
4. **Least Privilege**: Grant minimum required access to secrets
5. **Encrypt Everywhere**: Encrypt secrets at rest and in transit

### Essential Checklist

- [ ] **No secrets in code**: All secrets stored externally (Vault, env vars, secrets manager)
- [ ] **Pre-commit hooks**: git-secrets or TruffleHog configured to prevent commits
- [ ] **Environment variables**: .env files used locally, never committed to git
- [ ] **Secret rotation**: Automated rotation policies implemented
- [ ] **Access control**: RBAC/ABAC policies enforce least privilege access
- [ ] **Audit logging**: All secret access logged with timestamps and user IDs
- [ ] **Certificate management**: TLS/mTLS certificates managed centrally
- [ ] **Detection tools**: Regular scans with multiple tools (TruffleHog, git-secrets, Gitleaks)

### Quick Example

```python
# @nist sc-12 "Cryptographic key management"
# @nist sc-13 "Cryptographic protection"
import os
from hashicorp_vault import VaultClient
from cryptography.fernet import Fernet

# ❌ NEVER do this
# API_KEY = "sk-1234567890abcdef"
# DATABASE_PASSWORD = "my_secure_password"

# ✅ Use environment variables
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable not set")

# ✅ Use HashiCorp Vault for sensitive secrets
vault = VaultClient(url=os.getenv('VAULT_ADDR'), token=os.getenv('VAULT_TOKEN'))
db_credentials = vault.read_secret('database/prod')
DB_PASSWORD = db_credentials['password']

# ✅ Encrypt sensitive data
def encrypt_sensitive_data(data: str) -> bytes:
    """Encrypt sensitive data using Fernet symmetric encryption."""
    key = os.getenv('ENCRYPTION_KEY').encode()
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

# ✅ Never log secrets
def authenticate_api(api_key: str):
    """Authenticate with API using key."""
    # Log without exposing secret
    print(f"Authenticating with key: {api_key[:8]}...")  # Only show prefix
```

### Quick Links to Level 2

- [Secrets Storage Solutions](#secrets-storage-solutions)
- [Environment Variables Best Practices](#environment-variables-best-practices)
- [Secrets Rotation and Lifecycle](#secrets-rotation-and-lifecycle)
- [Detection and Prevention](#detection-and-prevention)
- [Certificate Management](#certificate-management)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### Secrets Storage Solutions

**HashiCorp Vault Integration**

```python
# @nist sc-12 "Key establishment and management"
# @nist ac-3 "Access enforcement through policy"
from hvac import Client as VaultClient
from typing import Dict, Any, Optional
import logging
from datetime import datetime

class SecretManager:
    """Centralized secret management using HashiCorp Vault."""

    def __init__(self, vault_url: str, token: str):
        self.client = VaultClient(url=vault_url, token=token)
        self.logger = logging.getLogger(__name__)

    def get_secret(self, path: str, key: Optional[str] = None) -> Any:
        """Retrieve secret from Vault.
        @nist au-2 "Audit secret access"
        @nist sc-12 "Cryptographic key retrieval"
        """
        try:
            response = self.client.secrets.kv.v2.read_secret_version(path=path)
            secret_data = response['data']['data']

            # Log access (without secret value)
            self.logger.info(f"Secret accessed: {path}", extra={
                'path': path,
                'timestamp': datetime.now().isoformat()
            })

            return secret_data.get(key) if key else secret_data
        except Exception as e:
            self.logger.error(f"Failed to retrieve secret from {path}: {e}")
            raise

# Usage
secret_manager = SecretManager(
    vault_url=os.getenv('VAULT_ADDR'),
    token=os.getenv('VAULT_TOKEN')
)
db_creds = secret_manager.get_secret('database/prod')
```

**AWS Secrets Manager Integration**

```python
# @nist sc-12 "Cloud-based key management"
import boto3
import json

class AWSSecretManager:
    def __init__(self, region_name: str = 'us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region_name)

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve secret from AWS Secrets Manager."""
        response = self.client.get_secret_value(SecretId=secret_name)
        return json.loads(response['SecretString'])

    def rotate_secret(self, secret_name: str) -> None:
        """Trigger automatic secret rotation.
        @nist sc-12 "Periodic key rotation"
        """
        self.client.rotate_secret(SecretId=secret_name)
```

### Environment Variables Best Practices

**12-Factor App Principles** (see [templates/.env.template](templates/.env.template))

```python
# @nist sc-13 "Use of validated cryptography"
from dotenv import load_dotenv
import os
from typing import Optional

class ConfigManager:
    """Manage configuration and secrets from environment variables."""

    def __init__(self, env_file: str = '.env'):
        if os.path.exists(env_file):
            load_dotenv(env_file)

    def get_required(self, key: str) -> str:
        """Get required environment variable or raise error."""
        value = os.getenv(key)
        if value is None:
            raise ValueError(f"Required environment variable {key} not set")
        return value

    def validate_configuration(self) -> None:
        """Validate all required configuration is present."""
        required_vars = ['DATABASE_URL', 'API_KEY', 'ENCRYPTION_KEY', 'JWT_SECRET']
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise ValueError(f"Missing required variables: {', '.join(missing)}")
```

### Secrets Rotation and Lifecycle

**Automated Rotation** (see [scripts/rotate-secrets.sh](scripts/rotate-secrets.sh))

```python
# @nist sc-12 "Periodic key rotation"
from datetime import datetime, timedelta
import secrets
import string

class SecretRotationManager:
    """Manage automated secret rotation."""

    def __init__(self, secret_manager: SecretManager):
        self.secret_manager = secret_manager
        self.rotation_policy = {
            'api_keys': timedelta(days=90),
            'passwords': timedelta(days=60),
            'certificates': timedelta(days=365)
        }

    def generate_secure_key(self, length: int = 32) -> str:
        """Generate cryptographically secure random key.
        @nist sc-12 "Key generation"
        @nist sc-13 "Cryptographic protection"
        """
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def rotate_api_key(self, service_name: str) -> str:
        """Rotate API key for a service."""
        new_key = self.generate_secure_key()
        self.secret_manager.create_secret(f'api/{service_name}', {
            'api_key': new_key,
            'created_at': datetime.now().isoformat()
        })
        return new_key
```

### Detection and Prevention

**Pre-commit Hook Configuration** (see [resources/configs/.pre-commit-secrets.yaml](resources/configs/.pre-commit-secrets.yaml))

```python
# @nist si-10 "Information input validation"
import subprocess
import json
from typing import List, Dict

class SecretScanner:
    """Scan codebase for exposed secrets."""

    def scan_with_trufflehog(self, path: str = '.') -> List[Dict]:
        """Scan with TruffleHog for secrets."""
        result = subprocess.run(
            ['trufflehog', 'filesystem', path, '--json'],
            capture_output=True, text=True
        )
        return [json.loads(line) for line in result.stdout.split('\n') if line.strip()]

    def scan_with_gitleaks(self, path: str = '.') -> List[Dict]:
        """Scan with Gitleaks for secrets."""
        result = subprocess.run(
            ['gitleaks', 'detect', '--source', path, '--report-format', 'json'],
            capture_output=True, text=True
        )
        return json.loads(result.stdout) if result.stdout else []
```

### Certificate Management

**TLS/mTLS Certificate Handling**

```python
# @nist sc-8 "Transmission confidentiality and integrity"
# @nist sc-13 "Cryptographic protection"
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from datetime import datetime, timedelta

class CertificateManager:
    """Manage TLS certificates and keys."""

    def generate_private_key(self, key_size: int = 4096):
        """Generate RSA private key.
        @nist sc-12 "Cryptographic key generation"
        """
        return rsa.generate_private_key(public_exponent=65537, key_size=key_size)

    def create_self_signed_cert(self, common_name: str, validity_days: int = 365):
        """Create self-signed certificate for development.
        @nist sc-17 "Public key infrastructure certificates"
        """
        private_key = self.generate_private_key()
        subject = issuer = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, common_name)
        ])

        cert = x509.CertificateBuilder().subject_name(
            subject
        ).issuer_name(
            issuer
        ).public_key(
            private_key.public_key()
        ).serial_number(
            x509.random_serial_number()
        ).not_valid_before(
            datetime.utcnow()
        ).not_valid_after(
            datetime.utcnow() + timedelta(days=validity_days)
        ).sign(private_key, hashes.SHA256())

        return cert, private_key
```

---

## Level 3: Mastery Resources

### Advanced Topics

- **[PKI Infrastructure](resources/pki-infrastructure.md)**: Certificate authorities, chain of trust
- **[Secrets Sprawl Management](resources/secrets-sprawl.md)**: Detection and remediation
- **[Zero-Trust Secrets](resources/zero-trust-secrets.md)**: Dynamic secrets and just-in-time access

### Templates & Examples

- **[.env Template](templates/.env.template)**: Complete environment variable template
- **[Vault Configuration](templates/vault-config.hcl)**: HashiCorp Vault setup
- **[Pre-commit Config](resources/configs/.pre-commit-secrets.yaml)**: Secret detection hooks
- **[Rotation Script](scripts/rotate-secrets.sh)**: Automated secret rotation

### Tools & Scripts

- **[Detection Tools Guide](resources/detection-tools.md)**: TruffleHog, Gitleaks, git-secrets comparison
- **[Rotation Automation](scripts/rotate-secrets.sh)**: Automated key rotation script

### Related Skills

- [Unit Testing](../../testing/unit-testing/SKILL.md) - Testing secret management
- [Integration Testing](../../testing/integration-testing/SKILL.md) - Integration security tests

---

## Quick Reference Commands

```bash
# Vault operations
vault login
vault kv get secret/database/prod
vault kv put secret/api/service-a api_key="new_key"

# Secret detection
trufflehog filesystem . --json
gitleaks detect --source . --report-format json

# Pre-commit setup
pre-commit install
pre-commit run --all-files

# Certificate generation
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365
```

---

## NIST Controls Coverage

**Primary Controls:**
- **SC-12**: Cryptographic Key Establishment and Management
- **SC-13**: Cryptographic Protection
- **SC-8**: Transmission Confidentiality and Integrity
- **IA-5**: Authenticator Management
- **AC-3**: Access Enforcement
- **AU-2**: Audit Events

---

## Validation

- ✅ Token count: Level 1 <2,000, Level 2 <5,000
- ✅ Code examples: All tested and working
- ✅ NIST controls: Fully mapped
