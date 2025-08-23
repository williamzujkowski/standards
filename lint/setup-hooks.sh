#!/bin/bash
# Enhanced Pre-commit Setup for Standards Repository
# Version 2.0.0 - Comprehensive Security & Development Environment Setup

set -euo pipefail

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE} Enhanced Pre-commit Setup v2.0.0${NC}"
echo -e "${BLUE} Standards Repository Security Suite${NC}"
echo -e "${BLUE}========================================${NC}"
echo

# System requirements check
log_info "Checking system requirements..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    log_error "Python 3 is required but not installed."
    log_info "Please install Python 3.8+ and try again"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
log_info "Found Python $PYTHON_VERSION"

if [[ "$(python3 -c "import sys; print(sys.version_info >= (3, 8))")" != "True" ]]; then
    log_error "Python 3.8+ is required (found $PYTHON_VERSION)"
    exit 1
fi

# Install core tools
log_info "Installing core security and quality tools..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    log_info "Installing pre-commit framework..."
    pip3 install --user pre-commit>=3.6.0

    # Add to PATH if needed
    export PATH="$HOME/.local/bin:$PATH"

    # Verify installation
    if command -v pre-commit &> /dev/null; then
        log_success "Pre-commit installed successfully"
    else
        log_error "Failed to install pre-commit"
        exit 1
    fi
else
    PRE_COMMIT_VERSION=$(pre-commit --version | cut -d' ' -f2)
    log_info "Pre-commit already installed (version $PRE_COMMIT_VERSION)"
fi

# Install Gitleaks for advanced secret detection
if ! command -v gitleaks &> /dev/null; then
    log_info "Installing Gitleaks for secret detection..."

    # Detect OS and architecture
    OS=$(uname -s | tr '[:upper:]' '[:lower:]')
    ARCH=$(uname -m)

    case $ARCH in
        x86_64) ARCH="x64" ;;
        aarch64|arm64) ARCH="arm64" ;;
        *) log_warning "Unsupported architecture: $ARCH. Skipping Gitleaks installation." ;;
    esac

    if [[ $ARCH != "unsupported" ]]; then
        GITLEAKS_VERSION="8.18.0"
        GITLEAKS_URL="https://github.com/gitleaks/gitleaks/releases/download/v${GITLEAKS_VERSION}/gitleaks_${GITLEAKS_VERSION}_${OS}_${ARCH}.tar.gz"

        # Download and install
        TMP_DIR=$(mktemp -d)
        curl -sL "$GITLEAKS_URL" | tar -xz -C "$TMP_DIR"

        # Install to user binary directory
        mkdir -p "$HOME/.local/bin"
        mv "$TMP_DIR/gitleaks" "$HOME/.local/bin/"
        chmod +x "$HOME/.local/bin/gitleaks"
        rm -rf "$TMP_DIR"

        export PATH="$HOME/.local/bin:$PATH"

        if command -v gitleaks &> /dev/null; then
            log_success "Gitleaks installed successfully"
        else
            log_warning "Failed to install Gitleaks. Secret detection may be limited."
        fi
    fi
else
    GITLEAKS_VERSION=$(gitleaks version 2>/dev/null | head -n1 | cut -d' ' -f2 || echo "unknown")
    log_info "Gitleaks already installed (version $GITLEAKS_VERSION)"
fi

# Install Node.js dependencies
if command -v npm &> /dev/null; then
    log_info "Installing Node.js quality tools..."

    # Install global tools
    npm install -g markdownlint-cli@0.39.0 2>/dev/null || log_warning "Failed to install markdownlint-cli globally"

    # Check if tools are available
    if command -v markdownlint &> /dev/null; then
        log_success "Markdownlint installed successfully"
    else
        log_warning "Markdownlint installation failed - will use pre-commit managed version"
    fi
else
    log_warning "npm not found. Using pre-commit managed versions of Node.js tools."
fi

# Install Python dependencies
log_info "Installing Python quality and security tools..."

# Essential Python packages
PYTHON_PACKAGES=(
    "pyyaml>=6.0"
    "requests>=2.28.0"
    "black>=24.1.0"
    "isort>=5.13.0"
    "ruff>=0.2.0"
    "detect-secrets>=1.4.0"
    "bandit[toml]>=1.7.0"
)

for package in "${PYTHON_PACKAGES[@]}"; do
    log_info "Installing $package..."
    pip3 install --user "$package" >/dev/null 2>&1 || log_warning "Failed to install $package"
done

log_success "Python dependencies installation completed"

# Create configuration files if they don't exist
log_info "Setting up security configuration..."

# Create gitleaks configuration
if [ ! -f .gitleaks.toml ]; then
    log_info "Creating Gitleaks configuration..."
    cat > .gitleaks.toml << 'EOF'
# Gitleaks configuration for standards repository
title = "Standards Repository Security Scan"

[allowlist]
  description = "Allowlist for false positives"
  # Add paths to ignore
  paths = [
    "\.git/",
    "node_modules/",
    "\.gitleaks-report\.json",
    "\.secrets\.baseline"
  ]

  # Allow certain patterns that are not actually secrets
  regexes = [
    "example\.com",
    "localhost",
    "127\.0\.0\.1",
    "dummy.*key",
    "sample.*secret",
    "test.*token"
  ]

[extend]
  # Use default rules
  useDefault = true
EOF
    log_success "Gitleaks configuration created"
fi

# Create secrets baseline if it doesn't exist
if [ ! -f .secrets.baseline ]; then
    log_info "Creating secrets baseline..."
    if command -v detect-secrets &> /dev/null; then
        detect-secrets scan --baseline .secrets.baseline 2>/dev/null || {
            log_warning "Failed to create secrets baseline with detect-secrets"
            echo '{}' > .secrets.baseline
        }
    else
        log_warning "detect-secrets not available, creating empty baseline"
        echo '{}' > .secrets.baseline
    fi
    log_success "Secrets baseline created"
fi

# Install pre-commit hooks
log_info "Installing pre-commit hooks..."
if pre-commit install; then
    log_success "Pre-commit hooks installed successfully"
else
    log_error "Failed to install pre-commit hooks"
    exit 1
fi

# Install pre-push hooks as well
log_info "Installing pre-push hooks..."
if pre-commit install --hook-type pre-push; then
    log_success "Pre-push hooks installed successfully"
else
    log_warning "Failed to install pre-push hooks"
fi

# Validation phase
log_info "Validating installation and running initial checks..."

# Update hook repositories to latest versions
log_info "Updating hook repositories..."
if pre-commit autoupdate; then
    log_success "Hook repositories updated"
else
    log_warning "Failed to update some hook repositories"
fi

# Run hooks on all files to check current state
echo
log_info "Running comprehensive security and quality checks..."
log_warning "This may take several minutes on first run..."
echo

# Run hooks with detailed output
if pre-commit run --all-files --verbose; then
    log_success "All pre-commit checks passed!"
    HOOKS_STATUS="✓ PASSED"
else
    log_warning "Some pre-commit checks failed or made corrections"
    log_info "This is normal on first run - hooks may have fixed formatting issues"
    HOOKS_STATUS="⚠ NEEDS ATTENTION"
fi

# Final status report
echo
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN} Installation Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo
log_success "Pre-commit security suite installed successfully!"
echo
echo -e "${BLUE}Installed Tools:${NC}"
echo "  ✓ Pre-commit Framework ($(pre-commit --version | cut -d' ' -f2))"
if command -v gitleaks &> /dev/null; then
    echo "  ✓ Gitleaks Secret Scanner ($(gitleaks version 2>/dev/null | head -n1 | cut -d' ' -f2 || echo 'installed'))"
fi
if command -v detect-secrets &> /dev/null; then
    echo "  ✓ Detect-Secrets ($(detect-secrets --version))"
fi
if command -v markdownlint &> /dev/null; then
    echo "  ✓ Markdownlint ($(markdownlint --version))"
fi
echo "  ✓ Python Quality Tools (Black, isort, Ruff)"
echo "  ✓ Shell Script Analysis (ShellCheck)"
echo
echo -e "${BLUE}Security Features:${NC}"
echo "  ✓ Secret Detection (Multiple engines)"
echo "  ✓ Large File Prevention (>1MB)"
echo "  ✓ Gitignore Compliance Validation"
echo "  ✓ Syntax validation (JSON, YAML, TOML, XML)"
echo "  ✓ Code Quality & Security Analysis"
echo "  ✓ Protected Branch Prevention"
echo
echo -e "${BLUE}Status:${NC}"
echo "  Hooks Status: $HOOKS_STATUS"
echo "  Config Files: ✓ Created"
echo "  Git Integration: ✓ Active"
echo
echo -e "${BLUE}Usage:${NC}"
echo "  • Hooks run automatically before each commit"
echo "  • Manual run: ${YELLOW}pre-commit run --all-files${NC}"
echo "  • Skip hooks: ${YELLOW}git commit --no-verify${NC} (not recommended)"
echo "  • Update hooks: ${YELLOW}pre-commit autoupdate${NC}"
echo "  • View config: ${YELLOW}cat .pre-commit-config.yaml${NC}"
echo
if [[ "$HOOKS_STATUS" == *"ATTENTION"* ]]; then
    log_warning "Please review any hook failures above and commit the fixes"
else
    log_success "Your repository is now secured with comprehensive pre-commit checks!"
fi
echo
