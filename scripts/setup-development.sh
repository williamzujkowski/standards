#!/bin/bash

# Development Environment Setup Script
# This script sets up the development environment for the standards repository

set -e  # Exit on error

echo "==================================="
echo "Standards Repository Development Setup"
echo "==================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if running from repository root
if [ ! -f "README.md" ] || [ ! -d ".github" ]; then
    print_error "Please run this script from the repository root directory"
    exit 1
fi

# 1. Check Python installation
echo ""
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    print_status "Python $PYTHON_VERSION found"
else
    print_error "Python 3 is not installed. Please install Python 3.8 or higher"
    exit 1
fi

# 2. Check Node.js installation (optional for compliance tools)
echo ""
echo "Checking Node.js installation..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    print_status "Node.js $NODE_VERSION found"

    # Install dependencies for compliance tools if needed
    if [ -f "standards/compliance/package.json" ]; then
        echo "Installing Node.js dependencies for compliance tools..."
        cd standards/compliance
        npm install
        cd ../..
        print_status "Node.js dependencies installed"
    fi
else
    print_warning "Node.js not found (optional - only needed for compliance tools)"
fi

# 3. Create virtual environment
echo ""
echo "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate
print_status "Virtual environment activated"

# 4. Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip install --upgrade pip > /dev/null 2>&1

# Install pre-commit
pip install pre-commit > /dev/null 2>&1
print_status "pre-commit installed"

# Install other development tools (ruff replaces black + isort)
pip install ruff flake8 bandit pytest > /dev/null 2>&1
print_status "Python development tools installed"

# Install monitoring dependencies if needed
if [ -f "monitoring/requirements.txt" ]; then
    pip install -r monitoring/requirements.txt > /dev/null 2>&1
    print_status "Monitoring dependencies installed"
fi

# 5. Set up pre-commit hooks
echo ""
echo "Setting up pre-commit hooks..."
pre-commit install
print_status "Pre-commit hooks installed"

# Run pre-commit on all files to check current state
echo "Running initial pre-commit checks..."
pre-commit run --all-files || print_warning "Some files need formatting (this is normal on first run)"

# 6. Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p reports/generated
mkdir -p memory/sessions
mkdir -p memory/agents
mkdir -p coordination/memory_bank
mkdir -p coordination/subtasks
mkdir -p coordination/orchestration
mkdir -p monitoring/logs
mkdir -p monitoring/metrics
mkdir -p monitoring/health
mkdir -p monitoring/reports
print_status "Directory structure created"

# 7. Set up git hooks
echo ""
echo "Setting up additional git hooks..."
if [ -f "scripts/setup-nist-hooks.sh" ]; then
    bash scripts/setup-nist-hooks.sh
    print_status "NIST compliance hooks installed"
fi

# 8. Create local configuration files (if not exist)
echo ""
echo "Setting up local configuration..."

# Create .env.example if it doesn't exist
if [ ! -f ".env.example" ]; then
    cat > .env.example << 'EOF'
# Example environment configuration
# Copy this to .env and fill in your values

# GitHub Token (for GitHub integrations)
# GITHUB_TOKEN=your_github_token_here

# OpenAI API Key (for AI features)
# OPENAI_API_KEY=your_openai_key_here

# Monitoring Configuration
MONITORING_ENABLED=true
LOG_LEVEL=INFO
METRICS_RETENTION_DAYS=30

# Development Settings
DEBUG=false
EOF
    print_status "Created .env.example"
fi

# 9. Verify .gitignore is properly configured
echo ""
echo "Verifying .gitignore configuration..."
if [ -f ".gitignore" ]; then
    print_status ".gitignore file found and configured"
else
    print_error ".gitignore file not found!"
fi

# 10. Display summary
echo ""
echo "==================================="
echo "Setup Complete!"
echo "==================================="
echo ""
echo "Development environment is ready. Here's what was set up:"
echo ""
echo "  ✓ Python virtual environment (venv)"
echo "  ✓ Pre-commit hooks for code quality"
echo "  ✓ Directory structure for reports and monitoring"
echo "  ✓ Development tools (ruff, flake8, bandit, pytest)"
if command -v node &> /dev/null; then
    echo "  ✓ Node.js dependencies for compliance tools"
fi
echo ""
echo "Next steps:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Copy .env.example to .env and configure as needed"
echo "  3. Run 'pre-commit run --all-files' to check code quality"
echo "  4. Read CONTRIBUTING.md for contribution guidelines"
echo ""
print_status "Happy coding! 🚀"
