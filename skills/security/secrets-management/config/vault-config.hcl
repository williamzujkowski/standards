/**
 * HashiCorp Vault Configuration
 *
 * This configuration file defines Vault server settings for production-ready
 * secrets management, including storage backend, listeners, telemetry, and sealing.
 *
 * @see https://developer.hashicorp.com/vault/docs/configuration
 */

# ===== Storage Backend Configuration =====

# Consul Storage Backend (Recommended for HA/DR)
storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault/"

  # Consul token for authentication (use env var: CONSUL_HTTP_TOKEN)
  # token = "CONSUL_TOKEN_HERE"

  # TLS configuration for Consul
  scheme            = "https"
  tls_ca_file       = "/etc/vault/tls/consul-ca.pem"
  tls_cert_file     = "/etc/vault/tls/consul-cert.pem"
  tls_key_file      = "/etc/vault/tls/consul-key.pem"
  tls_skip_verify   = false

  # Performance tuning
  max_parallel      = "128"
  consistency_mode  = "strong"
}

# Alternative: Integrated Storage (Raft) - Simpler, built-in HA
# storage "raft" {
#   path    = "/vault/data"
#   node_id = "vault-node-1"
#
#   # Retry join configuration for HA cluster
#   retry_join {
#     leader_api_addr = "https://vault-node-2:8200"
#   }
#   retry_join {
#     leader_api_addr = "https://vault-node-3:8200"
#   }
# }

# Alternative: File Storage (Development ONLY - not for production)
# storage "file" {
#   path = "/vault/data"
# }


# ===== Listener Configuration =====

# TCP Listener with TLS
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_disable   = false

  # TLS Certificate Configuration
  tls_cert_file = "/etc/vault/tls/vault-cert.pem"
  tls_key_file  = "/etc/vault/tls/vault-key.pem"
  tls_min_version = "tls12"

  # Client certificate authentication (mutual TLS)
  tls_require_and_verify_client_cert = false
  tls_client_ca_file = "/etc/vault/tls/ca.pem"

  # Performance tuning
  tls_cipher_suites = "TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384"
}

# Unix Socket Listener (Local admin access)
listener "unix" {
  address = "/var/run/vault.sock"
}


# ===== Seal Configuration =====

# AWS KMS Auto-Unseal (Recommended for production)
seal "awskms" {
  region     = "us-west-2"
  kms_key_id = "arn:aws:kms:us-west-2:123456789012:key/12345678-1234-1234-1234-123456789012"

  # IAM authentication (uses instance role or environment variables)
  # AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY
}

# Alternative: Azure Key Vault Seal
# seal "azurekeyvault" {
#   tenant_id     = "AZURE_TENANT_ID"
#   client_id     = "AZURE_CLIENT_ID"
#   client_secret = "AZURE_CLIENT_SECRET"
#   vault_name    = "my-vault"
#   key_name      = "vault-seal-key"
# }

# Alternative: Google Cloud KMS Seal
# seal "gcpckms" {
#   project     = "my-gcp-project"
#   region      = "us-central1"
#   key_ring    = "vault-keyring"
#   crypto_key  = "vault-seal-key"
# }

# Alternative: Shamir Seal (Default - requires manual unsealing)
# No configuration needed; uses key shares for unsealing


# ===== Telemetry Configuration =====

telemetry {
  # Prometheus metrics endpoint
  prometheus_retention_time = "30s"
  disable_hostname          = false

  # StatsD configuration
  statsd_address = "127.0.0.1:8125"

  # Datadog configuration
  # dogstatsd_addr = "127.0.0.1:8125"
  # dogstatsd_tags = ["environment:production", "service:vault"]

  # Circonus configuration (optional)
  # circonus_api_token = "CIRCONUS_API_TOKEN"
  # circonus_api_app   = "vault"
}


# ===== API Configuration =====

api_addr = "https://vault.example.com:8200"
cluster_addr = "https://vault-internal.example.com:8201"

# UI Configuration
ui = true


# ===== High Availability (HA) Configuration =====

# HA parameters for cluster coordination
ha_storage "consul" {
  address = "127.0.0.1:8500"
  path    = "vault-ha/"

  # Consul token (use env var: CONSUL_HTTP_TOKEN)
  # token = "CONSUL_TOKEN_HERE"
}


# ===== Logging Configuration =====

log_level = "info"  # Options: trace, debug, info, warn, error
log_format = "json" # Options: standard, json

# Log file rotation (optional)
# log_file = "/var/log/vault/vault.log"
# log_rotate_bytes = 104857600  # 100MB
# log_rotate_duration = "24h"
# log_rotate_max_files = 7


# ===== Plugin Directory =====

plugin_directory = "/etc/vault/plugins"


# ===== Performance and Resource Limits =====

# Disable mlock (not recommended for production, but may be needed in containers)
# disable_mlock = false

# Cache size (in-memory cache for frequently accessed secrets)
# cache_size = "32000"  # Number of cache entries

# Max lease TTL
max_lease_ttl = "768h"          # 32 days
default_lease_ttl = "168h"      # 7 days


# ===== Service Registration (Consul) =====

service_registration "consul" {
  address = "127.0.0.1:8500"

  # Service name for discovery
  service = "vault"

  # Health check configuration
  check_timeout = "5s"
  scheme        = "https"

  # Consul token (use env var: CONSUL_HTTP_TOKEN)
  # token = "CONSUL_TOKEN_HERE"
}


# ===== Enterprise Features (Vault Enterprise Only) =====

# Performance Standby Nodes
# disable_performance_standby = false

# Replication
# replication {
#   resolver_discover_servers = true
# }

# Entropy Augmentation (Hardware RNG)
# entropy "seal" {
#   mode = "augmentation"
# }


# ===== Audit Device Configuration =====
# Audit devices must be enabled via CLI/API after initialization:
#
# vault audit enable file file_path=/var/log/vault/audit.log
# vault audit enable syslog tag="vault" facility="LOCAL0"


# ===== Security Best Practices =====
#
# 1. Always use TLS for listeners (tls_disable = false)
# 2. Use auto-unseal (AWS KMS, Azure Key Vault, or GCP KMS)
# 3. Enable audit logging to multiple backends
# 4. Use Consul or Raft for HA storage
# 5. Rotate root tokens regularly
# 6. Use short-lived dynamic secrets
# 7. Enable MFA for sensitive operations
# 8. Implement least-privilege access policies
# 9. Monitor telemetry metrics for anomalies
# 10. Regularly backup Vault data and unseal keys


# ===== Environment Variables =====
#
# Vault supports configuration via environment variables:
#
# VAULT_ADDR               - Vault server address
# VAULT_TOKEN              - Authentication token
# VAULT_CACERT             - CA certificate path
# VAULT_CLIENT_CERT        - Client certificate path
# VAULT_CLIENT_KEY         - Client key path
# VAULT_SKIP_VERIFY        - Skip TLS verification (DO NOT use in production)
# AWS_ACCESS_KEY_ID        - AWS credentials for KMS seal
# AWS_SECRET_ACCESS_KEY    - AWS credentials for KMS seal
# CONSUL_HTTP_TOKEN        - Consul token for storage/service registration


# ===== Initialization and Unsealing =====
#
# Initialize Vault (first-time setup):
#   vault operator init -key-shares=5 -key-threshold=3
#
# Unseal Vault (after restart, if using Shamir seal):
#   vault operator unseal <unseal-key-1>
#   vault operator unseal <unseal-key-2>
#   vault operator unseal <unseal-key-3>
#
# Check Vault status:
#   vault status
#
# Login with root token:
#   vault login <root-token>
