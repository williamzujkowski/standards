#!/usr/bin/env bash
# Setup Rust project with best practices
# Usage: ./setup-rust-project.sh <project-name> [--lib|--bin]

set -euo pipefail

PROJECT_NAME="${1:-}"
PROJECT_TYPE="${2:---bin}"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name> [--lib|--bin]"
    exit 1
fi

echo "🦀 Setting up Rust project: $PROJECT_NAME"

# Create project
if [ "$PROJECT_TYPE" = "--lib" ]; then
    cargo new --lib "$PROJECT_NAME"
    echo "📦 Created library crate"
else
    cargo new "$PROJECT_NAME"
    echo "📦 Created binary crate"
fi

cd "$PROJECT_NAME"

# Copy configurations
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/../config"

if [ -f "$CONFIG_DIR/rustfmt.toml" ]; then
    cp "$CONFIG_DIR/rustfmt.toml" .
    echo "✓ Copied rustfmt.toml"
fi

if [ -f "$CONFIG_DIR/clippy.toml" ]; then
    cp "$CONFIG_DIR/clippy.toml" .
    echo "✓ Copied clippy.toml"
fi

# Update Cargo.toml with best practices
cat >> Cargo.toml << 'CARGO_EOF'

[profile.dev]
opt-level = 0
debug = true

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
strip = true

[profile.test]
opt-level = 1

[dependencies]
# Error handling
thiserror = "1.0"
anyhow = "1.0"

# Logging
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }

# Serialization
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"

[dev-dependencies]
# Testing
proptest = "1.0"
tempfile = "3.0"

# Async testing
tokio = { version = "1.0", features = ["full", "test-util"] }
futures = "0.3"

# Benchmarking
criterion = { version = "0.5", features = ["html_reports"] }
CARGO_EOF

echo "✓ Updated Cargo.toml with dependencies"

# Create GitHub Actions workflow
mkdir -p .github/workflows

cat > .github/workflows/ci.yml << 'WORKFLOW_EOF'
name: CI

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

env:
  CARGO_TERM_COLOR: always

jobs:
  test:
    name: Test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
      
      - name: Cache dependencies
        uses: Swatinem/rust-cache@v2
      
      - name: Run tests
        run: cargo test --all-features
  
  clippy:
    name: Clippy
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      
      - name: Cache dependencies
        uses: Swatinem/rust-cache@v2
      
      - name: Run clippy
        run: cargo clippy --all-targets --all-features -- -D warnings
  
  fmt:
    name: Format
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Rust
        uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt
      
      - name: Check formatting
        run: cargo fmt --all -- --check
  
  audit:
    name: Security Audit
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install cargo-audit
        run: cargo install cargo-audit
      
      - name: Run audit
        run: cargo audit
WORKFLOW_EOF

echo "✓ Created CI workflow"

# Create .gitignore
cat > .gitignore << 'GITIGNORE_EOF'
/target/
**/*.rs.bk
*.pdb
Cargo.lock

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db
GITIGNORE_EOF

echo "✓ Created .gitignore"

# Create README
cat > README.md << README_EOF
# $PROJECT_NAME

## Development

### Prerequisites

- Rust 1.70+ (\`rustup install stable\`)

### Build

\`\`\`bash
cargo build
\`\`\`

### Test

\`\`\`bash
# Run all tests
cargo test

# Run with output
cargo test -- --nocapture

# Run specific test
cargo test test_name
\`\`\`

### Lint

\`\`\`bash
# Check code
cargo check

# Run clippy
cargo clippy -- -D warnings

# Check formatting
cargo fmt -- --check

# Fix formatting
cargo fmt
\`\`\`

### Run

\`\`\`bash
cargo run
\`\`\`

### Release Build

\`\`\`bash
cargo build --release
\`\`\`

## Project Structure

\`\`\`
$PROJECT_NAME/
├── src/          # Source code
├── tests/        # Integration tests
├── benches/      # Benchmarks
├── examples/     # Example usage
└── docs/         # Additional documentation
\`\`\`

## Best Practices

- Follow Rust naming conventions
- Write documentation for public APIs
- Add tests for all features
- Run \`cargo clippy\` before commits
- Keep dependencies minimal and audited
README_EOF

echo "✓ Created README.md"

# Create docs directory
mkdir -p docs examples benches

# Initialize git
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    git init
    echo "✓ Initialized git repository"
fi

# Create initial commit
if [ -z "$(git status --porcelain)" ]; then
    git add .
    git commit -m "Initial commit: Rust project setup with best practices"
    echo "✓ Created initial commit"
fi

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  cargo build"
echo "  cargo test"
echo "  cargo run"
echo ""
echo "🦀 Happy coding!"
