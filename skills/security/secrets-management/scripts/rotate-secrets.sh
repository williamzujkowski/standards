#!/usr/bin/env bash
################################################################################
# Secret Rotation Script
#
# This script automates the rotation of secrets across various systems:
# - Database passwords
# - API keys
# - JWT secrets
# - Service account credentials
#
# Usage:
#   ./rotate-secrets.sh [options]
#
# Options:
#   --service <name>    Rotate secrets for a specific service
#   --all               Rotate all secrets
#   --dry-run           Show what would be done without making changes
#   --force             Skip confirmation prompts
#
# Requirements:
#   - AWS CLI (for AWS Secrets Manager)
#   - Vault CLI (for HashiCorp Vault)
#   - psql (for PostgreSQL)
#   - jq (for JSON parsing)
#
# Best Practices:
#   - Run this script regularly (e.g., every 90 days)
#   - Test in staging before running in production
#   - Maintain audit logs of all rotations
#   - Have rollback procedures ready
################################################################################

set -euo pipefail

# ===== Configuration =====

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="${LOG_FILE:-/var/log/secret-rotation.log}"
BACKUP_DIR="${BACKUP_DIR:-/var/backups/secrets}"
VAULT_ADDR="${VAULT_ADDR:-https://vault.example.com:8200}"

# Service configuration
SERVICES=("database" "api-keys" "jwt" "oauth" "encryption")

# Flags
DRY_RUN=false
FORCE=false
SERVICE=""
ROTATE_ALL=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ===== Functions =====

log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [${level}] ${message}" | tee -a "${LOG_FILE}"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
    log "INFO" "$*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
    log "SUCCESS" "$*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
    log "WARNING" "$*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
    log "ERROR" "$*"
}

usage() {
    cat <<EOF
Usage: $0 [options]

Options:
  --service <name>    Rotate secrets for a specific service (database, api-keys, jwt, oauth, encryption)
  --all               Rotate all secrets
  --dry-run           Show what would be done without making changes
  --force             Skip confirmation prompts
  -h, --help          Show this help message

Examples:
  $0 --service database           # Rotate only database credentials
  $0 --all                        # Rotate all secrets
  $0 --dry-run --all              # Preview all rotations
  $0 --service api-keys --force   # Rotate API keys without confirmation

EOF
    exit 0
}

check_dependencies() {
    local missing_deps=()

    command -v aws >/dev/null 2>&1 || missing_deps+=("aws-cli")
    command -v vault >/dev/null 2>&1 || missing_deps+=("vault")
    command -v psql >/dev/null 2>&1 || missing_deps+=("postgresql-client")
    command -v jq >/dev/null 2>&1 || missing_deps+=("jq")

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        log_info "Install them with: apt-get install ${missing_deps[*]}"
        exit 1
    fi
}

confirm_action() {
    if [[ "$FORCE" == "true" ]]; then
        return 0
    fi

    read -rp "Are you sure you want to proceed? (yes/no): " response
    case "$response" in
        [yY][eE][sS]|[yY])
            return 0
            ;;
        *)
            log_warning "Operation cancelled by user"
            exit 0
            ;;
    esac
}

backup_current_secrets() {
    local service="$1"
    local backup_file="${BACKUP_DIR}/${service}-$(date +%Y%m%d-%H%M%S).json"

    mkdir -p "${BACKUP_DIR}"

    log_info "Backing up current secrets for ${service}..."

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would backup to: ${backup_file}"
        return 0
    fi

    # Backup from Vault
    if vault kv get -format=json "secret/${service}" > "${backup_file}"; then
        log_success "Backup saved to: ${backup_file}"
    else
        log_error "Failed to backup secrets for ${service}"
        return 1
    fi
}

generate_secure_password() {
    local length="${1:-32}"
    openssl rand -base64 "$((length * 3 / 4))" | tr -d "=+/" | cut -c1-"${length}"
}

rotate_database_password() {
    log_info "Rotating database password..."

    local db_host="${DB_HOST:-localhost}"
    local db_port="${DB_PORT:-5432}"
    local db_user="${DB_USER:-postgres}"
    local db_name="${DB_NAME:-postgres}"

    # Generate new password
    local new_password
    new_password=$(generate_secure_password 32)

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would generate new password and update database"
        return 0
    fi

    # Update password in PostgreSQL
    log_info "Updating password in PostgreSQL..."
    PGPASSWORD="${DB_PASSWORD}" psql -h "${db_host}" -p "${db_port}" -U "${db_user}" -d "${db_name}" <<EOF
ALTER USER ${db_user} WITH PASSWORD '${new_password}';
EOF

    # Update password in Vault
    log_info "Updating password in Vault..."
    vault kv put "secret/database" \
        host="${db_host}" \
        port="${db_port}" \
        user="${db_user}" \
        password="${new_password}"

    # Update password in AWS Secrets Manager (if applicable)
    if command -v aws >/dev/null 2>&1; then
        log_info "Updating password in AWS Secrets Manager..."
        aws secretsmanager update-secret \
            --secret-id "prod/database/password" \
            --secret-string "${new_password}"
    fi

    log_success "Database password rotated successfully"
}

rotate_api_keys() {
    log_info "Rotating API keys..."

    local services=("stripe" "sendgrid" "twilio")

    for service in "${services[@]}"; do
        log_info "Rotating ${service} API key..."

        if [[ "$DRY_RUN" == "true" ]]; then
            log_info "[DRY RUN] Would rotate API key for ${service}"
            continue
        fi

        # Generate new API key (implementation depends on service)
        # This is a placeholder - each service has its own API for key rotation
        case "${service}" in
            stripe)
                log_warning "Manual rotation required for Stripe API keys"
                log_info "Visit: https://dashboard.stripe.com/apikeys"
                ;;
            sendgrid)
                log_warning "Manual rotation required for SendGrid API keys"
                log_info "Visit: https://app.sendgrid.com/settings/api_keys"
                ;;
            twilio)
                log_warning "Manual rotation required for Twilio API keys"
                log_info "Visit: https://www.twilio.com/console/project/api-keys"
                ;;
        esac
    done

    log_success "API key rotation review complete"
}

rotate_jwt_secret() {
    log_info "Rotating JWT secret..."

    local new_secret
    new_secret=$(generate_secure_password 64)

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would generate new JWT secret"
        return 0
    fi

    # Update JWT secret in Vault
    vault kv put "secret/jwt" \
        secret="${new_secret}" \
        algorithm="HS256" \
        expiration="1h"

    # Update in environment variables (requires application restart)
    log_warning "Application restart required to use new JWT secret"

    log_success "JWT secret rotated successfully"
}

rotate_oauth_credentials() {
    log_info "Rotating OAuth credentials..."

    local providers=("github" "google")

    for provider in "${providers[@]}"; do
        log_warning "Manual rotation required for ${provider} OAuth credentials"
        case "${provider}" in
            github)
                log_info "Visit: https://github.com/settings/developers"
                ;;
            google)
                log_info "Visit: https://console.cloud.google.com/apis/credentials"
                ;;
        esac
    done

    log_success "OAuth credentials rotation review complete"
}

rotate_encryption_key() {
    log_info "Rotating encryption key..."

    local new_key
    new_key=$(openssl rand -hex 32)

    if [[ "$DRY_RUN" == "true" ]]; then
        log_info "[DRY RUN] Would generate new encryption key"
        return 0
    fi

    # Update encryption key in Vault
    vault kv put "secret/encryption" \
        key="${new_key}" \
        algorithm="aes-256-gcm"

    log_warning "Data re-encryption required with new key"
    log_info "Run: ./scripts/re-encrypt-data.sh"

    log_success "Encryption key rotated successfully"
}

rotate_service() {
    local service="$1"

    log_info "Starting rotation for service: ${service}"

    # Backup current secrets
    backup_current_secrets "${service}"

    # Rotate based on service type
    case "${service}" in
        database)
            rotate_database_password
            ;;
        api-keys)
            rotate_api_keys
            ;;
        jwt)
            rotate_jwt_secret
            ;;
        oauth)
            rotate_oauth_credentials
            ;;
        encryption)
            rotate_encryption_key
            ;;
        *)
            log_error "Unknown service: ${service}"
            return 1
            ;;
    esac
}

main() {
    log_info "Secret rotation script started"

    # Check dependencies
    check_dependencies

    # Show summary
    if [[ "$ROTATE_ALL" == "true" ]]; then
        log_info "Rotating ALL secrets"
    elif [[ -n "$SERVICE" ]]; then
        log_info "Rotating secrets for service: ${SERVICE}"
    else
        log_error "No service specified. Use --service or --all"
        usage
    fi

    if [[ "$DRY_RUN" == "true" ]]; then
        log_warning "DRY RUN MODE - No changes will be made"
    fi

    # Confirm action
    confirm_action

    # Perform rotation
    if [[ "$ROTATE_ALL" == "true" ]]; then
        for service in "${SERVICES[@]}"; do
            rotate_service "${service}"
        done
    else
        rotate_service "${SERVICE}"
    fi

    log_success "Secret rotation completed successfully"
}

# ===== Parse Arguments =====

while [[ $# -gt 0 ]]; do
    case "$1" in
        --service)
            SERVICE="$2"
            shift 2
            ;;
        --all)
            ROTATE_ALL=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --force)
            FORCE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            log_error "Unknown option: $1"
            usage
            ;;
    esac
done

# ===== Run Main =====

main "$@"
