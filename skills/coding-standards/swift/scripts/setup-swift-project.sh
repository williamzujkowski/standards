#!/bin/bash

# Swift Project Setup Script
# Usage: ./setup-swift-project.sh ProjectName

set -e

PROJECT_NAME="${1:-MySwiftProject}"
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TEMPLATES_DIR="$(dirname "$SCRIPT_DIR")/templates"
CONFIG_DIR="$(dirname "$SCRIPT_DIR")/config"

echo "Setting up Swift project: $PROJECT_NAME"

# Create project directory
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize Swift package
swift package init --type executable --name "$PROJECT_NAME"

echo "Created Swift package structure"

# Create directory structure
mkdir -p Sources/"$PROJECT_NAME"/{Models,Services,ViewModels,Views}
mkdir -p Tests/"$PROJECT_NAME"Tests/{Mocks,Helpers}
mkdir -p .github/workflows

echo "Created directory structure"

# Copy SwiftLint configuration
if [ -f "$CONFIG_DIR/.swiftlint.yml" ]; then
    cp "$CONFIG_DIR/.swiftlint.yml" .swiftlint.yml
    echo "Copied SwiftLint configuration"
fi

# Copy templates if available
if [ -d "$TEMPLATES_DIR" ]; then
    [ -f "$TEMPLATES_DIR/ViewModel.swift" ] && cp "$TEMPLATES_DIR/ViewModel.swift" "Sources/$PROJECT_NAME/ViewModels/"
    [ -f "$TEMPLATES_DIR/Protocol.swift" ] && cp "$TEMPLATES_DIR/Protocol.swift" "Sources/$PROJECT_NAME/"
    [ -f "$TEMPLATES_DIR/NetworkService.swift" ] && cp "$TEMPLATES_DIR/NetworkService.swift" "Sources/$PROJECT_NAME/Services/"
    [ -f "$TEMPLATES_DIR/TestCase.swift" ] && cp "$TEMPLATES_DIR/TestCase.swift" "Tests/${PROJECT_NAME}Tests/"
    echo "Copied template files"
fi

# Create README
cat > README.md << README_EOF
# $PROJECT_NAME

## Description

A Swift project following modern best practices.

## Requirements

- Swift 6.0+
- Xcode 16.0+

## Setup

\`\`\`bash
# Install dependencies
swift package resolve

# Build project
swift build

# Run tests
swift test
\`\`\`

## Project Structure

\`\`\`
$PROJECT_NAME/
├── Sources/
│   └── $PROJECT_NAME/
│       ├── Models/
│       ├── Services/
│       ├── ViewModels/
│       └── Views/
├── Tests/
│   └── ${PROJECT_NAME}Tests/
│       ├── Mocks/
│       └── Helpers/
└── Package.swift
\`\`\`

## Coding Standards

This project follows:
- Swift API Design Guidelines
- Protocol-oriented design
- Value types over reference types
- Modern concurrency (async/await)

## Testing

Run tests with:
\`\`\`bash
swift test
\`\`\`

Run with coverage:
\`\`\`bash
swift test --enable-code-coverage
\`\`\`

## Linting

\`\`\`bash
# Install SwiftLint
brew install swiftlint

# Run linter
swiftlint

# Auto-fix issues
swiftlint autocorrect
\`\`\`
README_EOF

echo "Created README.md"

# Create GitHub Actions workflow
cat > .github/workflows/swift.yml << WORKFLOW_EOF
name: Swift CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: macos-latest

    steps:
    - uses: actions/checkout@v3

    - name: Setup Swift
      uses: swift-actions/setup-swift@v1
      with:
        swift-version: '6.0'

    - name: Install SwiftLint
      run: brew install swiftlint

    - name: Run SwiftLint
      run: swiftlint lint --strict

    - name: Build
      run: swift build -v

    - name: Run tests
      run: swift test -v
WORKFLOW_EOF

echo "Created GitHub Actions workflow"

# Create .gitignore
cat > .gitignore << GITIGNORE_EOF
# Xcode
.DS_Store
build/
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3
xcuserdata/
*.xccheckout
*.moved-aside
DerivedData
*.hmap
*.ipa
*.xcuserstate

# Swift Package Manager
.build/
Packages/
Package.pins
Package.resolved
.swiftpm/

# CocoaPods
Pods/

# Carthage
Carthage/Build/

# SPM
.swiftpm/xcode/package.xcworkspace/contents.xcworkspacedata
GITIGNORE_EOF

echo "Created .gitignore"

# Initialize git repository
git init
git add .
git commit -m "Initial commit: Swift project setup"

echo ""
echo "✅ Project setup complete!"
echo ""
echo "Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. swift build"
echo "3. swift test"
echo "4. swiftlint"
echo ""
echo "Project structure created with templates and configurations."
