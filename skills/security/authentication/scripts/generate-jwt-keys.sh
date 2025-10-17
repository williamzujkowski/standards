#!/bin/bash

###############################################################################
# Generate RSA Keypair for JWT RS256 Signing
#
# This script generates a 4096-bit RSA keypair suitable for JWT RS256 signing.
# - Private key: Used by authentication server to sign tokens
# - Public key: Used by resource servers to verify tokens
#
# @nist sc-12 "Cryptographic key establishment and management"
# @nist sc-13 "Cryptographic protection"
###############################################################################

set -euo pipefail

# Configuration
KEYS_DIR="${1:-./keys}"
PRIVATE_KEY_FILE="$KEYS_DIR/private.pem"
PUBLIC_KEY_FILE="$KEYS_DIR/public.pem"
KEY_SIZE=4096

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print with color
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if OpenSSL is installed
check_dependencies() {
    if ! command -v openssl &> /dev/null; then
        print_error "OpenSSL is not installed. Please install OpenSSL first."
        exit 1
    fi

    print_info "OpenSSL version: $(openssl version)"
}

# Create keys directory
create_keys_directory() {
    if [ -d "$KEYS_DIR" ]; then
        print_warning "Keys directory already exists: $KEYS_DIR"

        # Check if keys already exist
        if [ -f "$PRIVATE_KEY_FILE" ] || [ -f "$PUBLIC_KEY_FILE" ]; then
            print_warning "Existing keys found. Do you want to overwrite them? (y/N)"
            read -r response
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                print_info "Key generation cancelled."
                exit 0
            fi
        fi
    else
        mkdir -p "$KEYS_DIR"
        print_info "Created keys directory: $KEYS_DIR"
    fi
}

# Generate private key
generate_private_key() {
    print_info "Generating ${KEY_SIZE}-bit RSA private key..."

    openssl genrsa -out "$PRIVATE_KEY_FILE" "$KEY_SIZE" 2>/dev/null

    # Set restrictive permissions (owner read/write only)
    chmod 600 "$PRIVATE_KEY_FILE"

    print_info "Private key generated: $PRIVATE_KEY_FILE"
}

# Extract public key from private key
generate_public_key() {
    print_info "Extracting public key from private key..."

    openssl rsa -in "$PRIVATE_KEY_FILE" -pubout -out "$PUBLIC_KEY_FILE" 2>/dev/null

    # Set read-only permissions
    chmod 644 "$PUBLIC_KEY_FILE"

    print_info "Public key generated: $PUBLIC_KEY_FILE"
}

# Display key information
display_key_info() {
    print_info "\n=== Key Generation Complete ==="
    print_info "Private key: $PRIVATE_KEY_FILE (keep secure!)"
    print_info "Public key: $PUBLIC_KEY_FILE (distribute to services)"

    echo ""
    print_warning "IMPORTANT SECURITY NOTES:"
    echo "1. Keep private key secure - NEVER commit to version control"
    echo "2. Add to .gitignore: $KEYS_DIR/*.pem"
    echo "3. Store private key in secrets manager (Vault, AWS Secrets Manager)"
    echo "4. Rotate keys periodically (recommended: every 6-12 months)"
    echo "5. Use different keypairs for different environments (dev/staging/prod)"

    echo ""
    print_info "Public key fingerprint:"
    openssl rsa -in "$PUBLIC_KEY_FILE" -pubin -outform DER 2>/dev/null | \
        openssl dgst -sha256 -binary | \
        openssl base64
}

# Generate .gitignore entry
generate_gitignore() {
    local gitignore_file="$KEYS_DIR/.gitignore"

    if [ ! -f "$gitignore_file" ]; then
        cat > "$gitignore_file" << EOF
# Private keys - NEVER commit to version control
*.pem
!public.pem

# Key backups
*.key
*.bak
EOF
        print_info "Created .gitignore: $gitignore_file"
    fi
}

# Generate example usage
generate_example_usage() {
    local example_file="$KEYS_DIR/USAGE.md"

    cat > "$example_file" << 'EOF'
# JWT RS256 Keys Usage

## Node.js Example

```javascript
const jwt = require('jsonwebtoken');
const fs = require('fs');

// Sign JWT with private key
const privateKey = fs.readFileSync('./keys/private.pem');
const token = jwt.sign(
  { sub: 'user123', roles: ['admin'] },
  privateKey,
  { algorithm: 'RS256', expiresIn: '15m' }
);

// Verify JWT with public key
const publicKey = fs.readFileSync('./keys/public.pem');
const decoded = jwt.verify(token, publicKey, { algorithms: ['RS256'] });
```

## Python Example

```python
import jwt
from pathlib import Path

# Sign JWT with private key
private_key = Path('./keys/private.pem').read_text()
token = jwt.encode(
    {'sub': 'user123', 'roles': ['admin']},
    private_key,
    algorithm='RS256'
)

# Verify JWT with public key
public_key = Path('./keys/public.pem').read_text()
decoded = jwt.decode(token, public_key, algorithms=['RS256'])
```

## Key Rotation Process

1. Generate new keypair: `./generate-jwt-keys.sh ./keys-new`
2. Deploy new public key to all services
3. Update auth server to sign with new private key (keep old key for verification)
4. Wait for all tokens signed with old key to expire
5. Remove old public key from services
6. Archive old private key securely

## Security Checklist

- [ ] Private key has 600 permissions (owner read/write only)
- [ ] Private key is NOT in version control
- [ ] Private key is stored in secrets manager
- [ ] Public key is distributed to all resource servers
- [ ] Different keypairs used for different environments
- [ ] Key rotation schedule established (6-12 months)
- [ ] Key backup and recovery process documented
EOF

    print_info "Created usage guide: $example_file"
}

# Main execution
main() {
    print_info "JWT RS256 Key Generator"
    print_info "======================="
    echo ""

    check_dependencies
    create_keys_directory
    generate_private_key
    generate_public_key
    generate_gitignore
    generate_example_usage
    display_key_info

    echo ""
    print_info "✓ Key generation complete!"
}

# Run main function
main "$@"
