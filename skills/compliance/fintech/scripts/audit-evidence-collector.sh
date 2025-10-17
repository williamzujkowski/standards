#!/bin/bash
#
# Audit Evidence Collection Script
# PCI-DSS and SOC2 Compliance Evidence Automation
#
# Usage: ./audit-evidence-collector.sh [quarterly|annual]
#
# Collects evidence for:
# - Access controls (user lists, MFA status, access reviews)
# - Encryption configurations
# - Logging and monitoring
# - Vulnerability management
# - Change management
# - Physical security (if applicable)
#

set -euo pipefail

# Configuration
EVIDENCE_BASE_DIR="${EVIDENCE_BASE_DIR:-/var/audit/evidence}"
AUDIT_PERIOD="${1:-quarterly}"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
EVIDENCE_DIR="$EVIDENCE_BASE_DIR/$AUDIT_PERIOD/$TIMESTAMP"
CLOUD_PROVIDER="${CLOUD_PROVIDER:-aws}"  # aws, azure, gcp

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Create evidence directory structure
setup_evidence_directory() {
    log_info "Setting up evidence directory: $EVIDENCE_DIR"
    mkdir -p "$EVIDENCE_DIR"/{access_control,encryption,logging,vulnerability,change_management,network,physical}

    # Create manifest file
    cat > "$EVIDENCE_DIR/MANIFEST.txt" << MANIFEST
Audit Evidence Collection
=========================
Period: $AUDIT_PERIOD
Collection Date: $(date)
Cloud Provider: $CLOUD_PROVIDER
Collector: $(whoami)@$(hostname)

Evidence Categories:
- access_control/    : User accounts, MFA, access reviews
- encryption/        : Encryption configurations, key management
- logging/           : Log retention, SIEM configs, audit logs
- vulnerability/     : Scan reports, patch status
- change_management/ : Change tickets, approvals
- network/           : Firewall rules, segmentation
- physical/          : Badge logs, visitor logs (if applicable)
MANIFEST
}

# AWS Evidence Collection
collect_aws_evidence() {
    log_info "Collecting AWS evidence..."

    # IAM users and MFA status (Access Control)
    log_info "  - IAM credential report"
    aws iam generate-credential-report --output json > /dev/null 2>&1 || true
    sleep 2
    aws iam get-credential-report --output json | \
        jq -r '.Content' | base64 -d > "$EVIDENCE_DIR/access_control/iam-credentials.csv"

    # MFA enforcement
    log_info "  - MFA enforcement status"
    aws iam get-account-summary --output json > "$EVIDENCE_DIR/access_control/mfa-status.json"

    # IAM policies (least privilege)
    log_info "  - IAM policies"
    aws iam list-policies --scope Local --output json > "$EVIDENCE_DIR/access_control/custom-policies.json"

    # Security groups (network controls)
    log_info "  - Security groups"
    aws ec2 describe-security-groups --output json > "$EVIDENCE_DIR/network/security-groups.json"

    # Network ACLs
    log_info "  - Network ACLs"
    aws ec2 describe-network-acls --output json > "$EVIDENCE_DIR/network/network-acls.json"

    # VPC flow logs (logging)
    log_info "  - VPC flow logs"
    aws ec2 describe-flow-logs --output json > "$EVIDENCE_DIR/logging/vpc-flow-logs.json"

    # CloudTrail configuration (logging)
    log_info "  - CloudTrail trails"
    aws cloudtrail describe-trails --output json > "$EVIDENCE_DIR/logging/cloudtrail-trails.json"

    # CloudWatch log groups and retention
    log_info "  - CloudWatch log retention"
    aws logs describe-log-groups --output json | \
        jq '[.logGroups[] | {logGroupName, retentionInDays}]' > \
        "$EVIDENCE_DIR/logging/log-retention.json"

    # S3 bucket encryption
    log_info "  - S3 bucket encryption"
    aws s3api list-buckets --output json | jq -r '.Buckets[].Name' | while read bucket; do
        encryption=$(aws s3api get-bucket-encryption --bucket "$bucket" 2>/dev/null || echo "{}")
        echo "{\"bucket\": \"$bucket\", \"encryption\": $encryption}" >> "$EVIDENCE_DIR/encryption/s3-encryption.jsonl"
    done

    # RDS encryption status
    log_info "  - RDS encryption"
    aws rds describe-db-instances --output json | \
        jq '[.DBInstances[] | {DBInstanceIdentifier, StorageEncrypted, KmsKeyId}]' > \
        "$EVIDENCE_DIR/encryption/rds-encryption.json"

    # EBS encryption
    log_info "  - EBS default encryption"
    aws ec2 get-ebs-encryption-by-default --output json > "$EVIDENCE_DIR/encryption/ebs-default-encryption.json"

    # KMS key rotation
    log_info "  - KMS key rotation"
    aws kms list-keys --output json | jq -r '.Keys[].KeyId' | while read key_id; do
        rotation=$(aws kms get-key-rotation-status --key-id "$key_id" 2>/dev/null || echo "{}")
        echo "{\"KeyId\": \"$key_id\", \"rotation\": $rotation}" >> "$EVIDENCE_DIR/encryption/kms-rotation.jsonl"
    done

    # GuardDuty (threat detection)
    log_info "  - GuardDuty detectors"
    aws guardduty list-detectors --output json > "$EVIDENCE_DIR/logging/guardduty-detectors.json"

    # Config rules (compliance)
    log_info "  - AWS Config rules"
    aws configservice describe-config-rules --output json > "$EVIDENCE_DIR/vulnerability/config-rules.json"

    # Systems Manager patch compliance
    log_info "  - Patch compliance"
    aws ssm describe-instance-patch-states --output json > "$EVIDENCE_DIR/vulnerability/patch-compliance.json" 2>/dev/null || true

    # Inspector findings (vulnerability scanning)
    log_info "  - Inspector findings"
    aws inspector2 list-findings --output json > "$EVIDENCE_DIR/vulnerability/inspector-findings.json" 2>/dev/null || true
}

# Azure Evidence Collection
collect_azure_evidence() {
    log_info "Collecting Azure evidence..."

    # User accounts
    log_info "  - Azure AD users"
    az ad user list --output json > "$EVIDENCE_DIR/access_control/azuread-users.json"

    # MFA status
    log_info "  - MFA status"
    az ad user list --query "[].{userPrincipalName:userPrincipalName, mfaEnabled:strongAuthenticationMethods[0].methodType}" \
        --output json > "$EVIDENCE_DIR/access_control/mfa-status.json"

    # Network security groups
    log_info "  - Network security groups"
    az network nsg list --output json > "$EVIDENCE_DIR/network/nsgs.json"

    # Storage account encryption
    log_info "  - Storage account encryption"
    az storage account list --query "[].{name:name, encryption:encryption}" \
        --output json > "$EVIDENCE_DIR/encryption/storage-encryption.json"

    # SQL Database encryption
    log_info "  - SQL TDE status"
    az sql db list --output json | \
        jq '[.[] | {name, transparentDataEncryption}]' > "$EVIDENCE_DIR/encryption/sql-tde.json" 2>/dev/null || true

    # Key Vault configuration
    log_info "  - Key Vaults"
    az keyvault list --output json > "$EVIDENCE_DIR/encryption/keyvaults.json"

    # Azure Monitor log retention
    log_info "  - Log Analytics workspaces"
    az monitor log-analytics workspace list --output json > "$EVIDENCE_DIR/logging/log-analytics.json"

    # Security Center recommendations
    log_info "  - Security Center"
    az security assessment list --output json > "$EVIDENCE_DIR/vulnerability/security-center.json" 2>/dev/null || true
}

# GCP Evidence Collection
collect_gcp_evidence() {
    log_info "Collecting GCP evidence..."

    # IAM users
    log_info "  - IAM members"
    gcloud projects get-iam-policy "$(gcloud config get-value project)" \
        --format=json > "$EVIDENCE_DIR/access_control/iam-policy.json"

    # Firewall rules
    log_info "  - Firewall rules"
    gcloud compute firewall-rules list --format=json > "$EVIDENCE_DIR/network/firewall-rules.json"

    # Storage bucket encryption
    log_info "  - GCS bucket encryption"
    gcloud storage buckets list --format=json | \
        jq '[.[] | {name, encryption}]' > "$EVIDENCE_DIR/encryption/gcs-encryption.json"

    # Cloud SQL encryption
    log_info "  - Cloud SQL encryption"
    gcloud sql instances list --format=json | \
        jq '[.[] | {name, settings.ipConfiguration, diskEncryptionConfiguration}]' > \
        "$EVIDENCE_DIR/encryption/cloudsql-encryption.json"

    # Cloud KMS keys
    log_info "  - KMS keys"
    gcloud kms keys list --location=global --keyring=primary --format=json > \
        "$EVIDENCE_DIR/encryption/kms-keys.json" 2>/dev/null || true

    # Logging configuration
    log_info "  - Logging sinks"
    gcloud logging sinks list --format=json > "$EVIDENCE_DIR/logging/logging-sinks.json"

    # Security Command Center findings
    log_info "  - Security Command Center"
    gcloud scc findings list "organizations/$(gcloud organizations list --format='value(name)')" \
        --format=json > "$EVIDENCE_DIR/vulnerability/scc-findings.json" 2>/dev/null || true
}

# Application-level evidence
collect_application_evidence() {
    log_info "Collecting application-level evidence..."

    # Database users (example for PostgreSQL)
    if command -v psql &> /dev/null; then
        log_info "  - Database users"
        psql -h "${DB_HOST:-localhost}" -U "${DB_USER:-postgres}" -d postgres -c "\du" \
            > "$EVIDENCE_DIR/access_control/db-users.txt" 2>/dev/null || log_warn "Database query failed"
    fi

    # Application logs (last 1000 authentication attempts)
    if [ -f "/var/log/app/auth.log" ]; then
        log_info "  - Application authentication logs"
        tail -n 1000 /var/log/app/auth.log > "$EVIDENCE_DIR/logging/app-auth-sample.log"
    fi

    # Certificate expiration (TLS/SSL)
    log_info "  - TLS certificate expiration"
    for domain in "${DOMAINS[@]:-example.com}"; do
        expiry=$(echo | openssl s_client -servername "$domain" -connect "$domain:443" 2>/dev/null | \
                 openssl x509 -noout -enddate 2>/dev/null || echo "N/A")
        echo "$domain: $expiry" >> "$EVIDENCE_DIR/encryption/tls-certificates.txt"
    done
}

# Vulnerability scan evidence
collect_vulnerability_evidence() {
    log_info "Collecting vulnerability scan evidence..."

    # If Nessus/OpenVAS reports exist, copy them
    if [ -d "/var/scans/reports" ]; then
        log_info "  - Vulnerability scan reports"
        find /var/scans/reports -name "*.pdf" -o -name "*.html" -mtime -90 \
            -exec cp {} "$EVIDENCE_DIR/vulnerability/" \; 2>/dev/null || true
    fi

    # Package vulnerabilities (example with npm audit)
    if [ -f "package.json" ]; then
        log_info "  - NPM audit"
        npm audit --json > "$EVIDENCE_DIR/vulnerability/npm-audit.json" 2>/dev/null || true
    fi

    # Docker image vulnerabilities (if using Trivy)
    if command -v trivy &> /dev/null; then
        log_info "  - Docker image scan"
        trivy image --format json --output "$EVIDENCE_DIR/vulnerability/trivy-scan.json" \
            "${DOCKER_IMAGE:-nginx:latest}" 2>/dev/null || true
    fi
}

# Change management evidence
collect_change_evidence() {
    log_info "Collecting change management evidence..."

    # Git commits in the last 90 days (for IaC repos)
    if [ -d ".git" ]; then
        log_info "  - Git change history"
        git log --since="90 days ago" --pretty=format:"%h|%an|%ad|%s" \
            > "$EVIDENCE_DIR/change_management/git-commits.txt"
    fi

    # Terraform state changes (if applicable)
    if command -v terraform &> /dev/null && [ -f "terraform.tfstate" ]; then
        log_info "  - Terraform state"
        terraform show -json > "$EVIDENCE_DIR/change_management/terraform-state.json" 2>/dev/null || true
    fi
}

# Physical security evidence (if applicable)
collect_physical_evidence() {
    log_info "Collecting physical security evidence..."

    # If badge access logs are available
    if [ -f "/var/physical-security/badge-access.csv" ]; then
        log_info "  - Badge access logs (last 90 days)"
        tail -n 10000 /var/physical-security/badge-access.csv > \
            "$EVIDENCE_DIR/physical/badge-access-sample.csv"
    fi

    # Visitor logs
    if [ -f "/var/physical-security/visitor-log.csv" ]; then
        log_info "  - Visitor logs (last 90 days)"
        tail -n 1000 /var/physical-security/visitor-log.csv > \
            "$EVIDENCE_DIR/physical/visitor-log-sample.csv"
    fi
}

# Generate integrity checksums
generate_checksums() {
    log_info "Generating evidence integrity checksums..."
    cd "$EVIDENCE_DIR"
    find . -type f -exec sha256sum {} \; > evidence-integrity.sha256
    cd - > /dev/null
}

# Create evidence summary
create_summary() {
    log_info "Creating evidence summary..."

    cat > "$EVIDENCE_DIR/SUMMARY.md" << SUMMARY
# Audit Evidence Summary

**Collection Date:** $(date)
**Audit Period:** $AUDIT_PERIOD
**Cloud Provider:** $CLOUD_PROVIDER

## Evidence Collected

### Access Control
- IAM users and credential status
- MFA enforcement verification
- Access review documentation
- Privileged account inventory

### Encryption
- Data-at-rest encryption configuration
- Data-in-transit (TLS) verification
- Key management and rotation status
- Certificate expiration tracking

### Logging and Monitoring
- Log retention configuration
- SIEM/centralized logging verification
- Audit trail completeness
- Monitoring alert configuration

### Vulnerability Management
- Vulnerability scan reports (quarterly)
- Patch compliance status
- Security findings and remediation
- Container/image scanning results

### Change Management
- Infrastructure changes (IaC commits)
- Change approval records
- Configuration drift detection

### Network Security
- Firewall rules and segmentation
- Network access controls
- VPC/subnet configuration

### Physical Security
- Badge access logs (if applicable)
- Visitor logs (if applicable)

## Evidence Integrity

All evidence files have been checksummed for integrity verification.
See \`evidence-integrity.sha256\` for SHA-256 hashes.

## Next Steps

1. Review collected evidence for completeness
2. Provide to external auditor
3. Address any identified gaps
4. Schedule next collection: **$(date -d "+90 days" 2>/dev/null || date -v+90d 2>/dev/null || echo "90 days from now")**

---
*Generated by audit-evidence-collector.sh*
SUMMARY
}

# Compress evidence
compress_evidence() {
    log_info "Compressing evidence archive..."
    tar -czf "$EVIDENCE_DIR.tar.gz" -C "$EVIDENCE_BASE_DIR/$AUDIT_PERIOD" "$(basename "$EVIDENCE_DIR")"
    log_info "Evidence archive created: $EVIDENCE_DIR.tar.gz"
}

# Main execution
main() {
    log_info "=== Audit Evidence Collection Started ==="
    log_info "Period: $AUDIT_PERIOD"
    log_info "Cloud Provider: $CLOUD_PROVIDER"

    setup_evidence_directory

    case "$CLOUD_PROVIDER" in
        aws)
            collect_aws_evidence
            ;;
        azure)
            collect_azure_evidence
            ;;
        gcp)
            collect_gcp_evidence
            ;;
        *)
            log_warn "Unknown cloud provider: $CLOUD_PROVIDER"
            ;;
    esac

    collect_application_evidence
    collect_vulnerability_evidence
    collect_change_evidence
    collect_physical_evidence

    generate_checksums
    create_summary
    compress_evidence

    log_info "=== Evidence Collection Complete ==="
    log_info "Evidence location: $EVIDENCE_DIR"
    log_info "Archive: $EVIDENCE_DIR.tar.gz"
    log_info "Next steps:"
    log_info "  1. Review SUMMARY.md"
    log_info "  2. Verify evidence completeness"
    log_info "  3. Provide to auditor"
}

# Run main function
main
