# Swift Coding Standards Skill

## Overview

This skill teaches comprehensive Swift coding standards following Apple's guidelines, protocol-oriented design principles, and modern concurrency patterns.

## Structure

- **SKILL.md** (1,165 lines) - Main skill document with 3 progressive levels
- **6 bundled resources** - Ready-to-use templates and configurations

## Skill Levels

### Level 1: Quick Reference (~600-800 tokens)
- Optionals cheat sheet (?, !, guard, if let, nil coalescing)
- Common patterns (protocols, extensions, closures, property wrappers)
- Essential checklist (SwiftLint, naming conventions, access control)

### Level 2: Implementation Guide (~2,500-3,500 tokens)
1. Optionals and Safety - Optional fundamentals, unwrapping patterns
2. Protocols and Protocol-Oriented Design - Composition over inheritance
3. Value Types vs Reference Types - Struct, class, enum usage
4. Memory Management with ARC - Retain cycles, weak/unowned
5. Error Handling - Throwing functions, Result type, try?/try!
6. Modern Concurrency - async/await, actors, TaskGroup, MainActor
7. Testing with XCTest - Unit tests, mocks, async testing, UI tests

### Level 3: Deep Dive Resources (~500-800 tokens)
- Advanced topics (generics, property wrappers, result builders)
- SwiftUI architecture patterns
- Performance optimization techniques
- Official documentation links
- Practice projects (beginner to advanced)
- Validation checklist

## Bundled Resources

### 1. config/.swiftlint.yml (158 lines)
Comprehensive SwiftLint configuration with:
- 30+ opt-in rules enabled
- Reasonable limits (line: 120, function: 50, file: 500)
- Custom rules for weak self, force unwrapping
- Proper exclusions for build artifacts

### 2. templates/ViewModel.swift (124 lines)
MVVM ViewModel template featuring:
- @MainActor for UI safety
- @Published properties with Combine
- Async/await patterns
- Search debouncing
- Error handling
- Repository pattern

### 3. templates/Protocol.swift (229 lines)
10 protocol-oriented design examples:
- Basic protocols with extensions
- Protocol composition
- Associated types
- Generic implementations
- Dependency injection
- Conditional conformance
- Strategy pattern
- Event handling

### 4. templates/NetworkService.swift (289 lines)
Modern network layer with:
- Protocol-based design
- Async/await throughout
- Custom Endpoint type
- Authentication wrapper
- Actor-based caching
- Error handling
- Request/response modeling

### 5. templates/TestCase.swift (268 lines)
XCTest template with:
- Proper setUp/tearDown
- Mock objects for dependencies
- Async test patterns
- Performance testing
- Edge case coverage
- Test helpers
- Supporting protocols

### 6. scripts/setup-swift-project.sh (216 lines)
Project setup script that:
- Creates Swift package structure
- Copies SwiftLint configuration
- Sets up directory organization
- Creates README with documentation
- Configures GitHub Actions CI
- Generates .gitignore
- Initializes git repository

## Key Features

- **Protocol-Oriented**: Emphasis on composition over inheritance
- **Modern Concurrency**: async/await, actors, structured concurrency
- **Type Safety**: Optionals, value types, compile-time guarantees
- **Memory Safety**: ARC, weak/unowned, avoiding retain cycles
- **Testing Focus**: Comprehensive XCTest examples and patterns
- **Production Ready**: Real-world patterns and best practices

## Usage

```bash
# View the skill
cat SKILL.md

# Setup new project with templates
./scripts/setup-swift-project.sh MyProject

# Use SwiftLint configuration
swiftlint lint --config config/.swiftlint.yml

# Copy templates to your project
cp templates/*.swift MyProject/Sources/
```

## Learning Path

1. **Week 1-2**: Master optionals, protocols, and value/reference types
2. **Week 3-4**: Learn memory management and error handling
3. **Week 5-6**: Study async/await and actor-based concurrency
4. **Week 7-8**: Build with SwiftUI and advanced patterns

## Target Audience

- iOS/macOS developers (beginner to intermediate)
- Developers transitioning from Objective-C
- Teams establishing Swift coding standards
- Anyone learning modern Swift patterns

## Related Skills

- kotlin-coding-standards (similar modern language)
- typescript-coding-standards (type safety patterns)
- ios-development (application-level patterns)

## Validation Checklist

✅ Explain Optional type with 5 unwrapping patterns
✅ Design systems using protocols instead of inheritance
✅ Identify and fix retain cycles
✅ Write async/await code with error handling
✅ Create actors for thread safety
✅ Write unit tests with mocks
✅ Set up SwiftLint in projects
✅ Explain value semantics and struct vs class
✅ Implement protocol extensions
✅ Use TaskGroup for parallel operations

## Maintenance

- **Version**: 1.0.0
- **Last Updated**: October 2025
- **Swift Version**: 6.0
- **Platform**: iOS 18, macOS 15, Xcode 16

---

*Part of the Standards Repository coding-standards skill collection*
