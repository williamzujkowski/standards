#!/bin/bash
# Terraform CI/CD Pipeline Script
# This script orchestrates Terraform operations in CI/CD pipelines

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${PROJECT_ROOT:-$(dirname "$SCRIPT_DIR")}"
TF_DIR="${TF_DIR:-$PROJECT_ROOT}"
TF_VERSION="${TF_VERSION:-1.6.0}"
ENVIRONMENT="${ENVIRONMENT:-dev}"
ACTION="${1:-plan}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $*"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $*"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

# Error handler
error_handler() {
    local line=$1
    log_error "Script failed at line $line"
    exit 1
}

trap 'error_handler $LINENO' ERR

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Terraform
    if ! command -v terraform &> /dev/null; then
        log_error "Terraform not found. Installing..."
        install_terraform
    fi
    
    local installed_version
    installed_version=$(terraform version -json | jq -r '.terraform_version')
    log_info "Terraform version: $installed_version"
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI not found. Please install it."
        exit 1
    fi
    
    # Check required tools
    for tool in jq git; do
        if ! command -v "$tool" &> /dev/null; then
            log_error "$tool not found. Please install it."
            exit 1
        fi
    done
    
    log_success "Prerequisites check passed"
}

# Install Terraform
install_terraform() {
    local os
    local arch
    
    os=$(uname -s | tr '[:upper:]' '[:lower:]')
    arch=$(uname -m)
    
    case $arch in
        x86_64)
            arch="amd64"
            ;;
        aarch64)
            arch="arm64"
            ;;
    esac
    
    local download_url="https://releases.hashicorp.com/terraform/${TF_VERSION}/terraform_${TF_VERSION}_${os}_${arch}.zip"
    
    log_info "Downloading Terraform $TF_VERSION from $download_url"
    
    curl -fsSL "$download_url" -o /tmp/terraform.zip
    unzip -q /tmp/terraform.zip -d /tmp
    sudo mv /tmp/terraform /usr/local/bin/
    rm /tmp/terraform.zip
    
    log_success "Terraform $TF_VERSION installed"
}

# Validate Terraform configuration
validate_terraform() {
    log_info "Validating Terraform configuration..."
    
    cd "$TF_DIR"
    
    # Format check
    log_info "Checking Terraform formatting..."
    if ! terraform fmt -check -recursive; then
        log_error "Terraform files are not formatted correctly"
        log_info "Run 'terraform fmt -recursive' to fix"
        exit 1
    fi
    
    # Initialize without backend
    log_info "Initializing Terraform (validation mode)..."
    terraform init -backend=false -input=false
    
    # Validate
    log_info "Running Terraform validate..."
    terraform validate
    
    log_success "Terraform configuration is valid"
}

# Run TFLint
run_tflint() {
    log_info "Running TFLint..."
    
    if ! command -v tflint &> /dev/null; then
        log_warning "TFLint not found. Skipping..."
        return 0
    fi
    
    cd "$TF_DIR"
    
    tflint --init
    tflint --recursive --format=compact
    
    log_success "TFLint passed"
}

# Run Checkov security scan
run_checkov() {
    log_info "Running Checkov security scan..."
    
    if ! command -v checkov &> /dev/null; then
        log_warning "Checkov not found. Skipping..."
        return 0
    fi
    
    cd "$TF_DIR"
    
    checkov -d . --framework terraform --quiet --compact
    
    log_success "Checkov security scan passed"
}

# Initialize Terraform
init_terraform() {
    log_info "Initializing Terraform for $ENVIRONMENT..."
    
    cd "$TF_DIR"
    
    # Backend config file
    local backend_config="${TF_DIR}/backend-${ENVIRONMENT}.hcl"
    
    if [[ -f "$backend_config" ]]; then
        log_info "Using backend config: $backend_config"
        terraform init -backend-config="$backend_config" -input=false -upgrade
    else
        log_info "Using default backend configuration"
        terraform init -input=false -upgrade
    fi
    
    # Select workspace
    if terraform workspace list | grep -q "$ENVIRONMENT"; then
        terraform workspace select "$ENVIRONMENT"
    else
        terraform workspace new "$ENVIRONMENT"
    fi
    
    log_success "Terraform initialized for workspace: $ENVIRONMENT"
}

# Plan Terraform changes
plan_terraform() {
    log_info "Planning Terraform changes for $ENVIRONMENT..."
    
    cd "$TF_DIR"
    
    local plan_file="${TF_DIR}/tfplan-${ENVIRONMENT}"
    local plan_output="${TF_DIR}/plan-${ENVIRONMENT}.txt"
    local plan_json="${TF_DIR}/plan-${ENVIRONMENT}.json"
    
    # Generate plan
    terraform plan \
        -var-file="environments/${ENVIRONMENT}.tfvars" \
        -out="$plan_file" \
        -input=false \
        | tee "$plan_output"
    
    # Convert plan to JSON
    terraform show -json "$plan_file" > "$plan_json"
    
    # Analyze plan
    local changes
    changes=$(jq -r '.resource_changes | length' "$plan_json")
    local creates
    creates=$(jq -r '[.resource_changes[] | select(.change.actions[] == "create")] | length' "$plan_json")
    local updates
    updates=$(jq -r '[.resource_changes[] | select(.change.actions[] == "update")] | length' "$plan_json")
    local deletes
    deletes=$(jq -r '[.resource_changes[] | select(.change.actions[] == "delete")] | length' "$plan_json")
    
    log_info "Plan Summary:"
    log_info "  Total changes: $changes"
    log_info "  Creates: $creates"
    log_info "  Updates: $updates"
    log_info "  Deletes: $deletes"
    
    if [[ $deletes -gt 0 ]]; then
        log_warning "Plan includes resource deletions!"
    fi
    
    # Save plan summary
    cat > "${TF_DIR}/plan-summary-${ENVIRONMENT}.json" <<EOF
{
  "environment": "$ENVIRONMENT",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "changes": {
    "total": $changes,
    "creates": $creates,
    "updates": $updates,
    "deletes": $deletes
  }
}
EOF
    
    log_success "Terraform plan completed"
}

# Apply Terraform changes
apply_terraform() {
    log_info "Applying Terraform changes for $ENVIRONMENT..."
    
    cd "$TF_DIR"
    
    local plan_file="${TF_DIR}/tfplan-${ENVIRONMENT}"
    
    if [[ ! -f "$plan_file" ]]; then
        log_error "Plan file not found. Run 'plan' first."
        exit 1
    fi
    
    # Apply with plan file
    terraform apply -input=false "$plan_file"
    
    # Generate outputs
    terraform output -json > "${TF_DIR}/outputs-${ENVIRONMENT}.json"
    
    log_success "Terraform apply completed"
}

# Destroy infrastructure
destroy_terraform() {
    log_info "Destroying infrastructure for $ENVIRONMENT..."
    
    cd "$TF_DIR"
    
    if [[ "$ENVIRONMENT" == "prod" ]]; then
        log_error "Cannot destroy production environment via script"
        log_error "Use manual process with approval"
        exit 1
    fi
    
    log_warning "This will destroy all infrastructure in $ENVIRONMENT"
    
    terraform destroy \
        -var-file="environments/${ENVIRONMENT}.tfvars" \
        -auto-approve \
        -input=false
    
    log_success "Infrastructure destroyed"
}

# Drift detection
detect_drift() {
    log_info "Detecting drift for $ENVIRONMENT..."
    
    cd "$TF_DIR"
    
    # Refresh state
    terraform refresh -var-file="environments/${ENVIRONMENT}.tfvars"
    
    # Generate plan to detect drift
    local drift_file="${TF_DIR}/drift-${ENVIRONMENT}.txt"
    
    set +e
    terraform plan \
        -var-file="environments/${ENVIRONMENT}.tfvars" \
        -detailed-exitcode \
        -input=false \
        > "$drift_file" 2>&1
    
    local exit_code=$?
    set -e
    
    case $exit_code in
        0)
            log_success "No drift detected"
            ;;
        1)
            log_error "Error detecting drift"
            cat "$drift_file"
            exit 1
            ;;
        2)
            log_warning "Drift detected!"
            cat "$drift_file"
            
            # Parse drift details
            local changes
            changes=$(grep -c "^  # " "$drift_file" || true)
            log_warning "Detected $changes resource changes"
            
            return 2
            ;;
    esac
}

# Cost estimation
estimate_cost() {
    log_info "Estimating infrastructure cost..."
    
    if ! command -v infracost &> /dev/null; then
        log_warning "Infracost not found. Skipping cost estimation..."
        return 0
    fi
    
    cd "$TF_DIR"
    
    local plan_file="${TF_DIR}/tfplan-${ENVIRONMENT}"
    
    if [[ ! -f "$plan_file" ]]; then
        log_error "Plan file not found. Run 'plan' first."
        exit 1
    fi
    
    infracost breakdown \
        --path "$plan_file" \
        --format table \
        --show-skipped
    
    log_success "Cost estimation completed"
}

# Generate documentation
generate_docs() {
    log_info "Generating Terraform documentation..."
    
    if ! command -v terraform-docs &> /dev/null; then
        log_warning "terraform-docs not found. Skipping..."
        return 0
    fi
    
    cd "$TF_DIR"
    
    terraform-docs markdown table . > README.md
    
    log_success "Documentation generated"
}

# Cleanup
cleanup() {
    log_info "Cleaning up temporary files..."
    
    cd "$TF_DIR"
    
    rm -f tfplan-* plan-*.txt plan-*.json drift-*.txt
    
    log_success "Cleanup completed"
}

# Main execution
main() {
    log_info "Terraform CI/CD Pipeline"
    log_info "Environment: $ENVIRONMENT"
    log_info "Action: $ACTION"
    log_info "Directory: $TF_DIR"
    
    check_prerequisites
    
    case $ACTION in
        validate)
            validate_terraform
            run_tflint
            run_checkov
            ;;
        init)
            init_terraform
            ;;
        plan)
            init_terraform
            plan_terraform
            estimate_cost
            ;;
        apply)
            init_terraform
            apply_terraform
            ;;
        destroy)
            init_terraform
            destroy_terraform
            ;;
        drift)
            init_terraform
            detect_drift
            ;;
        full)
            validate_terraform
            run_tflint
            run_checkov
            init_terraform
            plan_terraform
            estimate_cost
            ;;
        docs)
            generate_docs
            ;;
        cleanup)
            cleanup
            ;;
        *)
            log_error "Unknown action: $ACTION"
            log_info "Available actions: validate, init, plan, apply, destroy, drift, full, docs, cleanup"
            exit 1
            ;;
    esac
    
    log_success "Pipeline completed successfully"
}

# Run main function
main "$@"
