# HashiCorp Vault Configuration

# Storage backend - Use Consul for HA production
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"
}

# Listener - TLS configuration for production
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault/tls/vault.crt"
  tls_key_file  = "/etc/vault/tls/vault.key"
  tls_min_version = "tls12"
}

# API address for cluster
api_addr = "https://vault.example.com:8200"
cluster_addr = "https://vault.example.com:8201"

# UI
ui = true

# Enable audit logging
audit "file" {
  file_path = "/var/log/vault/audit.log"
}

# Auto-unseal using AWS KMS (production)
seal "awskms" {
  region     = "us-east-1"
  kms_key_id = "your-kms-key-id"
}

# Default lease and max lease TTL
default_lease_ttl = "168h"  # 7 days
max_lease_ttl     = "720h"  # 30 days
