#!/bin/bash
set -e

##############################################################################
# E2E Test Execution Script for CI/CD
# Supports: Playwright, Cypress, Docker, Multiple browsers, Reporting
##############################################################################

# Configuration
FRAMEWORK="${TEST_FRAMEWORK:-playwright}" # playwright or cypress
BROWSER="${BROWSER:-chromium}"             # chromium, firefox, webkit, chrome
ENVIRONMENT="${ENVIRONMENT:-staging}"      # development, staging, production
PARALLEL="${PARALLEL:-false}"              # Run tests in parallel
HEADLESS="${HEADLESS:-true}"               # Headless mode
RETRIES="${RETRIES:-2}"                    # Number of retries
WORKERS="${WORKERS:-1}"                    # Number of parallel workers
VIDEO="${VIDEO:-on-failure}"               # Video recording: on, off, on-failure
REPORT="${REPORT:-html}"                   # Report format: html, json, junit

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_dependencies() {
    log_info "Checking dependencies..."

    if [ "$FRAMEWORK" = "playwright" ]; then
        if ! command -v npx &> /dev/null || ! npx playwright --version &> /dev/null; then
            log_error "Playwright not found. Installing..."
            npm install -D @playwright/test
            npx playwright install --with-deps
        fi
    elif [ "$FRAMEWORK" = "cypress" ]; then
        if ! command -v npx &> /dev/null || ! npx cypress version &> /dev/null; then
            log_error "Cypress not found. Installing..."
            npm install -D cypress
        fi
    fi
}

setup_environment() {
    log_info "Setting up environment: $ENVIRONMENT"

    # Load environment-specific variables
    if [ -f ".env.$ENVIRONMENT" ]; then
        export $(cat ".env.$ENVIRONMENT" | xargs)
    elif [ -f ".env" ]; then
        export $(cat ".env" | xargs)
    fi

    # Set base URL based on environment
    case $ENVIRONMENT in
        development)
            export BASE_URL="${BASE_URL:-http://localhost:3000}"
            ;;
        staging)
            export BASE_URL="${BASE_URL:-https://staging.example.com}"
            ;;
        production)
            export BASE_URL="${BASE_URL:-https://example.com}"
            ;;
    esac

    log_info "Base URL: $BASE_URL"
}

wait_for_server() {
    local url=$1
    local timeout=${2:-300}
    local elapsed=0

    log_info "Waiting for server at $url..."

    while [ $elapsed -lt $timeout ]; do
        if curl -sf "$url" > /dev/null 2>&1; then
            log_info "Server is ready!"
            return 0
        fi
        sleep 5
        elapsed=$((elapsed + 5))
        echo -n "."
    done

    log_error "Server did not become ready after ${timeout}s"
    return 1
}

run_playwright_tests() {
    log_info "Running Playwright tests..."

    local args=""

    # Browser selection
    if [ "$BROWSER" != "all" ]; then
        args="--project=$BROWSER"
    fi

    # Headless mode
    if [ "$HEADLESS" = "false" ]; then
        args="$args --headed"
    fi

    # Workers
    args="$args --workers=$WORKERS"

    # Retries
    args="$args --retries=$RETRIES"

    # Reporter
    case $REPORT in
        html)
            args="$args --reporter=html"
            ;;
        json)
            args="$args --reporter=json"
            ;;
        junit)
            args="$args --reporter=junit"
            ;;
    esac

    log_info "Playwright command: npx playwright test $args"

    if npx playwright test $args; then
        log_info "Playwright tests passed!"
        return 0
    else
        log_error "Playwright tests failed!"
        return 1
    fi
}

run_cypress_tests() {
    log_info "Running Cypress tests..."

    local args=""

    # Browser selection
    if [ "$BROWSER" != "all" ]; then
        args="--browser=$BROWSER"
    fi

    # Headless mode
    if [ "$HEADLESS" = "false" ]; then
        args="$args --headed"
    fi

    # Parallel execution
    if [ "$PARALLEL" = "true" ]; then
        args="$args --parallel"
    fi

    # Reporter
    args="$args --reporter=$REPORT"

    log_info "Cypress command: npx cypress run $args"

    if npx cypress run $args; then
        log_info "Cypress tests passed!"
        return 0
    else
        log_error "Cypress tests failed!"
        return 1
    fi
}

generate_report() {
    log_info "Generating test report..."

    if [ "$FRAMEWORK" = "playwright" ]; then
        if [ -d "playwright-report" ]; then
            log_info "Playwright report available at: playwright-report/index.html"

            # Open report in CI (if supported)
            if [ "$CI" != "true" ]; then
                npx playwright show-report
            fi
        fi
    elif [ "$FRAMEWORK" = "cypress" ]; then
        if [ -d "cypress/reports" ]; then
            log_info "Cypress report available at: cypress/reports/"
        fi
    fi
}

upload_artifacts() {
    log_info "Uploading test artifacts..."

    # This function can be extended to upload to S3, Azure, etc.
    local artifact_dir="test-artifacts"
    mkdir -p "$artifact_dir"

    if [ "$FRAMEWORK" = "playwright" ]; then
        [ -d "playwright-report" ] && cp -r playwright-report "$artifact_dir/"
        [ -d "test-results" ] && cp -r test-results "$artifact_dir/"
    elif [ "$FRAMEWORK" = "cypress" ]; then
        [ -d "cypress/videos" ] && cp -r cypress/videos "$artifact_dir/"
        [ -d "cypress/screenshots" ] && cp -r cypress/screenshots "$artifact_dir/"
        [ -d "cypress/reports" ] && cp -r cypress/reports "$artifact_dir/"
    fi

    log_info "Artifacts saved to: $artifact_dir"
}

cleanup() {
    log_info "Cleaning up..."

    # Kill any remaining processes
    pkill -f "node.*webpack" || true
    pkill -f "node.*server" || true

    # Remove temporary files
    rm -rf .tmp-test-* || true
}

# Main execution
main() {
    log_info "Starting E2E test execution..."
    log_info "Framework: $FRAMEWORK"
    log_info "Browser: $BROWSER"
    log_info "Environment: $ENVIRONMENT"

    # Trap cleanup on exit
    trap cleanup EXIT

    # Check dependencies
    check_dependencies

    # Setup environment
    setup_environment

    # Wait for server if needed
    if [ "$WAIT_FOR_SERVER" = "true" ]; then
        wait_for_server "$BASE_URL" || exit 1
    fi

    # Run tests
    local exit_code=0
    if [ "$FRAMEWORK" = "playwright" ]; then
        run_playwright_tests || exit_code=$?
    elif [ "$FRAMEWORK" = "cypress" ]; then
        run_cypress_tests || exit_code=$?
    else
        log_error "Unknown framework: $FRAMEWORK"
        exit 1
    fi

    # Generate report
    generate_report

    # Upload artifacts if in CI
    if [ "$CI" = "true" ]; then
        upload_artifacts
    fi

    if [ $exit_code -eq 0 ]; then
        log_info "All tests passed successfully!"
    else
        log_error "Tests failed with exit code: $exit_code"
    fi

    exit $exit_code
}

# Run main function
main "$@"
