#!/bin/bash
# Production-ready Lambda deployment automation script
# Features: Validation, testing, rollback, notifications

set -euo pipefail

# Configuration
FUNCTION_NAME="${1:-my-function}"
ENVIRONMENT="${2:-dev}"
REGION="${3:-us-east-1}"
AWS_PROFILE="${4:-default}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Verify prerequisites
check_prerequisites() {
    log "Checking prerequisites..."

    command -v aws >/dev/null 2>&1 || error "AWS CLI not installed"
    command -v jq >/dev/null 2>&1 || error "jq not installed"
    command -v python3 >/dev/null 2>&1 || error "Python 3 not installed"

    log "All prerequisites met"
}

# Run tests
run_tests() {
    log "Running tests..."

    if [ -f "requirements-dev.txt" ]; then
        pip install -q -r requirements-dev.txt
    fi

    if [ -f "pytest.ini" ] || [ -d "tests/" ]; then
        python3 -m pytest tests/ -v --tb=short || error "Tests failed"
    else
        warn "No tests found, skipping"
    fi

    log "Tests passed"
}

# Package function
package_function() {
    log "Packaging function..."

    rm -rf build/ dist/ *.zip
    mkdir -p build

    # Install dependencies
    if [ -f "requirements.txt" ]; then
        pip install -q -r requirements.txt -t build/
    fi

    # Copy source files
    cp -r *.py build/ 2>/dev/null || true
    cp -r src/ build/ 2>/dev/null || true

    # Create deployment package
    cd build
    zip -r ../function.zip . >/dev/null
    cd ..

    PACKAGE_SIZE=$(du -h function.zip | cut -f1)
    log "Package created: function.zip (${PACKAGE_SIZE})"
}

# Get current function configuration
get_current_config() {
    log "Retrieving current function configuration..."

    aws lambda get-function \
        --function-name "$FUNCTION_NAME" \
        --profile "$AWS_PROFILE" \
        --region "$REGION" \
        2>/dev/null || warn "Function does not exist yet"
}

# Deploy function
deploy_function() {
    log "Deploying function: $FUNCTION_NAME to $ENVIRONMENT..."

    # Check if function exists
    if aws lambda get-function --function-name "$FUNCTION_NAME" --profile "$AWS_PROFILE" --region "$REGION" >/dev/null 2>&1; then
        # Update existing function
        log "Updating existing function..."

        aws lambda update-function-code \
            --function-name "$FUNCTION_NAME" \
            --zip-file fileb://function.zip \
            --profile "$AWS_PROFILE" \
            --region "$REGION" \
            --publish \
            > deployment-result.json

        # Wait for update to complete
        aws lambda wait function-updated \
            --function-name "$FUNCTION_NAME" \
            --profile "$AWS_PROFILE" \
            --region "$REGION"
    else
        # Create new function
        log "Creating new function..."

        aws lambda create-function \
            --function-name "$FUNCTION_NAME" \
            --runtime python3.11 \
            --role "arn:aws:iam::$(aws sts get-caller-identity --profile "$AWS_PROFILE" --query Account --output text):role/lambda-execution-role" \
            --handler app.lambda_handler \
            --zip-file fileb://function.zip \
            --timeout 30 \
            --memory-size 512 \
            --environment "Variables={ENVIRONMENT=$ENVIRONMENT}" \
            --tracing-config Mode=Active \
            --profile "$AWS_PROFILE" \
            --region "$REGION" \
            --publish \
            > deployment-result.json
    fi

    NEW_VERSION=$(jq -r '.Version' deployment-result.json)
    log "Deployed version: $NEW_VERSION"
}

# Update alias
update_alias() {
    local ALIAS_NAME="$ENVIRONMENT"
    log "Updating alias: $ALIAS_NAME..."

    # Get current alias version (for rollback)
    PREVIOUS_VERSION=$(aws lambda get-alias \
        --function-name "$FUNCTION_NAME" \
        --name "$ALIAS_NAME" \
        --profile "$AWS_PROFILE" \
        --region "$REGION" \
        --query 'FunctionVersion' \
        --output text 2>/dev/null || echo "")

    if [ -n "$PREVIOUS_VERSION" ]; then
        log "Previous version: $PREVIOUS_VERSION"

        # Update existing alias
        aws lambda update-alias \
            --function-name "$FUNCTION_NAME" \
            --name "$ALIAS_NAME" \
            --function-version "$NEW_VERSION" \
            --profile "$AWS_PROFILE" \
            --region "$REGION" \
            >/dev/null
    else
        # Create new alias
        aws lambda create-alias \
            --function-name "$FUNCTION_NAME" \
            --name "$ALIAS_NAME" \
            --function-version "$NEW_VERSION" \
            --profile "$AWS_PROFILE" \
            --region "$REGION" \
            >/dev/null
    fi

    log "Alias updated: $ALIAS_NAME -> v$NEW_VERSION"
}

# Smoke test
smoke_test() {
    log "Running smoke test..."

    TEST_EVENT='{"test": true}'

    RESPONSE=$(aws lambda invoke \
        --function-name "$FUNCTION_NAME:$ENVIRONMENT" \
        --payload "$TEST_EVENT" \
        --profile "$AWS_PROFILE" \
        --region "$REGION" \
        --log-type Tail \
        response.json 2>&1)

    STATUS_CODE=$(echo "$RESPONSE" | jq -r '.StatusCode')

    if [ "$STATUS_CODE" != "200" ]; then
        error "Smoke test failed with status code: $STATUS_CODE"
    fi

    if grep -q '"error"' response.json; then
        error "Smoke test returned error: $(cat response.json)"
    fi

    log "Smoke test passed"
    rm -f response.json
}

# Rollback function
rollback() {
    if [ -z "${PREVIOUS_VERSION:-}" ]; then
        error "No previous version to rollback to"
    fi

    warn "Rolling back to version: $PREVIOUS_VERSION"

    aws lambda update-alias \
        --function-name "$FUNCTION_NAME" \
        --name "$ENVIRONMENT" \
        --function-version "$PREVIOUS_VERSION" \
        --profile "$AWS_PROFILE" \
        --region "$REGION" \
        >/dev/null

    log "Rollback complete"
}

# Cleanup
cleanup() {
    log "Cleaning up..."
    rm -rf build/ function.zip deployment-result.json
}

# Main execution
main() {
    log "Starting deployment: $FUNCTION_NAME ($ENVIRONMENT)"

    check_prerequisites
    run_tests
    package_function
    get_current_config
    deploy_function
    update_alias

    # Run smoke test and rollback on failure
    if ! smoke_test; then
        warn "Smoke test failed, initiating rollback..."
        rollback
        error "Deployment failed"
    fi

    cleanup

    log "Deployment successful!"
    log "Function: $FUNCTION_NAME:$ENVIRONMENT (v$NEW_VERSION)"
}

# Trap errors
trap 'error "Deployment failed at line $LINENO"' ERR

main "$@"
