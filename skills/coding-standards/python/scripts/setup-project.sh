#!/usr/bin/env bash
# setup-project.sh - Initialize new Python project with best practices

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="3.10"
PROJECT_NAME=""
PROJECT_DIR=""

# Print colored message
print_message() {
    local color=$1
    shift
    echo -e "${color}$*${NC}"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Print usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Initialize a new Python project with best practices structure.

OPTIONS:
    -n, --name NAME        Project name (required)
    -d, --dir DIR          Project directory (default: ./NAME)
    -p, --python VERSION   Python version (default: 3.10)
    -h, --help             Show this help message

EXAMPLE:
    $0 --name myproject --dir ~/projects/myproject
EOF
    exit 1
}

# Parse arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -n|--name)
                PROJECT_NAME="$2"
                shift 2
                ;;
            -d|--dir)
                PROJECT_DIR="$2"
                shift 2
                ;;
            -p|--python)
                PYTHON_VERSION="$2"
                shift 2
                ;;
            -h|--help)
                usage
                ;;
            *)
                print_message "$RED" "Error: Unknown option: $1"
                usage
                ;;
        esac
    done

    if [[ -z "$PROJECT_NAME" ]]; then
        print_message "$RED" "Error: Project name is required"
        usage
    fi

    if [[ -z "$PROJECT_DIR" ]]; then
        PROJECT_DIR="./$PROJECT_NAME"
    fi
}

# Check prerequisites
check_prerequisites() {
    print_message "$YELLOW" "Checking prerequisites..."

    if ! command_exists python3; then
        print_message "$RED" "Error: python3 is not installed"
        exit 1
    fi

    if ! command_exists git; then
        print_message "$RED" "Error: git is not installed"
        exit 1
    fi

    print_message "$GREEN" "✓ All prerequisites met"
}

# Create project structure
create_structure() {
    print_message "$YELLOW" "Creating project structure..."

    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"

    # Create directory structure
    mkdir -p src/"$PROJECT_NAME"/{api,models,services,utils}
    mkdir -p tests/{unit,integration,e2e}
    mkdir -p docs
    mkdir -p scripts
    mkdir -p .github/workflows

    # Create __init__.py files
    touch src/"$PROJECT_NAME"/__init__.py
    touch src/"$PROJECT_NAME"/api/__init__.py
    touch src/"$PROJECT_NAME"/models/__init__.py
    touch src/"$PROJECT_NAME"/services/__init__.py
    touch src/"$PROJECT_NAME"/utils/__init__.py
    touch tests/__init__.py
    touch tests/unit/__init__.py
    touch tests/integration/__init__.py
    touch tests/e2e/__init__.py

    print_message "$GREEN" "✓ Project structure created"
}

# Create configuration files
create_configs() {
    print_message "$YELLOW" "Creating configuration files..."

    # pyproject.toml
    cat > pyproject.toml << EOF
[build-system]
requires = ["setuptools>=65.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "TODO: Add description"
readme = "README.md"
requires-python = ">=$PYTHON_VERSION"
authors = [
    {name = "Your Name", email = "your.email@example.com"}
]
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.5.0",
    "ruff>=0.0.290",
    "pre-commit>=3.3.0",
]

[tool.black]
line-length = 88
target-version = ["py${PYTHON_VERSION//./}"]

[tool.isort]
profile = "black"

[tool.pytest.ini_options]
testpaths = ["tests"]
EOF

    # .gitignore
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
.venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/

# Type checking
.mypy_cache/
.dmypy.json
dmypy.json

# Environment
.env
.env.local
EOF

    # README.md
    cat > README.md << EOF
# $PROJECT_NAME

TODO: Add project description

## Setup

\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -e ".[dev]"
\`\`\`

## Development

\`\`\`bash
# Format code
black src/ tests/
isort src/ tests/

# Type check
mypy src/

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
\`\`\`

## License

TODO: Add license
EOF

    # .env.example
    cat > .env.example << EOF
# Example environment variables
# Copy to .env and fill in actual values

DATABASE_URL=postgresql://localhost/dbname
SECRET_KEY=your-secret-key-here
API_KEY=your-api-key-here
EOF

    # conftest.py
    cat > tests/conftest.py << EOF
"""Shared pytest fixtures."""

import pytest


@pytest.fixture
def sample_data():
    """Sample data for testing."""
    return {"key": "value"}
EOF

    print_message "$GREEN" "✓ Configuration files created"
}

# Initialize virtual environment
setup_venv() {
    print_message "$YELLOW" "Setting up virtual environment..."

    python3 -m venv venv
    source venv/bin/activate

    pip install --upgrade pip setuptools wheel
    pip install -e ".[dev]"

    print_message "$GREEN" "✓ Virtual environment setup complete"
}

# Initialize git repository
init_git() {
    print_message "$YELLOW" "Initializing git repository..."

    git init
    git add .
    git commit -m "Initial commit: Project setup"

    print_message "$GREEN" "✓ Git repository initialized"
}

# Setup pre-commit hooks
setup_precommit() {
    print_message "$YELLOW" "Setting up pre-commit hooks..."

    if command_exists pre-commit; then
        pre-commit install
        print_message "$GREEN" "✓ Pre-commit hooks installed"
    else
        print_message "$YELLOW" "⚠ pre-commit not found, skipping"
    fi
}

# Print success message
print_success() {
    cat << EOF

${GREEN}✓ Project setup complete!${NC}

Next steps:
  1. cd $PROJECT_DIR
  2. source venv/bin/activate
  3. Edit pyproject.toml with your project details
  4. Start coding in src/$PROJECT_NAME/

Run tests:
  pytest

Format code:
  black src/ tests/
  isort src/ tests/

Type check:
  mypy src/

EOF
}

# Main function
main() {
    parse_args "$@"
    check_prerequisites
    create_structure
    create_configs
    setup_venv
    init_git
    setup_precommit
    print_success
}

main "$@"
