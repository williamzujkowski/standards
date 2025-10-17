---
name: swift-coding-standards
category: coding-standards
difficulty: intermediate
estimated_time: 45 minutes
description: Master Swift coding standards with Apple's guidelines, protocol-oriented design, and modern concurrency patterns
version: 1.0.0
tags: [swift, ios, macos, mobile, apple]
related_skills: [kotlin-coding-standards, typescript-coding-standards]
---

# Swift Coding Standards

> **Learn Once, Write Anywhere**: Master Swift coding standards for iOS, macOS, watchOS, and tvOS development with protocol-oriented design, value semantics, and modern concurrency.

## Overview

Swift combines powerful type safety with expressive syntax optimized for Apple platforms. This skill teaches idiomatic Swift following Apple's API Design Guidelines, protocol-oriented programming, and modern async/await patterns.

**What You'll Learn:**
- Swift optionals and safety patterns
- Protocol-oriented design principles
- Value types vs reference types
- Memory management with ARC
- Modern async/await concurrency
- Testing with XCTest

**Prerequisites:**
- Basic programming concepts (variables, functions, control flow)
- Familiarity with object-oriented programming
- Xcode installed (for iOS/macOS development)

---

## Level 1: Quick Reference

### Optionals Cheat Sheet

```swift
// Optional declaration
var name: String? = nil
var age: Int? = 25

// Optional binding (safe unwrapping)
if let name = name {
    print("Hello, \(name)")
}

// Guard statement (early exit)
guard let age = age else {
    print("Age is nil")
    return
}
print("Age is \(age)")

// Nil coalescing (default value)
let displayName = name ?? "Anonymous"

// Optional chaining
let count = user?.profile?.posts?.count

// Force unwrapping (avoid unless certain)
let definitelyExists = optionalValue!

// Implicitly unwrapped optional (use sparingly)
var mustExist: String!
```

### Common Patterns

```swift
// Protocol definition
protocol Drawable {
    var color: Color { get set }
    func draw()
}

// Protocol extension (default implementation)
extension Drawable {
    func draw() {
        print("Drawing with \(color)")
    }
}

// Struct with protocol conformance
struct Circle: Drawable {
    var color: Color
    var radius: Double
}

// Enum with associated values
enum Result<T, E: Error> {
    case success(T)
    case failure(E)
}

// Closure syntax
let doubled = numbers.map { $0 * 2 }
let filtered = numbers.filter { $0 > 10 }

// Trailing closure
fetchData { result in
    switch result {
    case .success(let data):
        process(data)
    case .failure(let error):
        handle(error)
    }
}

// Property wrapper
@State private var isPresented = false
@Published var count: Int = 0

// Computed property
var area: Double {
    return radius * radius * .pi
}

// Property observer
var temperature: Double {
    didSet {
        if temperature > 100 {
            sendAlert()
        }
    }
}
```

### Essential Checklist

**Before Every Commit:**
- [ ] SwiftLint passes with zero warnings
- [ ] All optionals handled safely (no force unwrapping)
- [ ] Naming follows Apple conventions (camelCase, PascalCase)
- [ ] Access control specified (private, internal, public)
- [ ] Memory cycles avoided (weak/unowned references)
- [ ] Error handling implemented (throws or Result)
- [ ] Unit tests cover happy and error paths
- [ ] Documentation comments for public APIs

**Naming Conventions:**
```swift
// Types: PascalCase
class UserProfileViewController { }
struct NetworkRequest { }
enum LoadingState { }
protocol DataSource { }

// Variables/Functions: camelCase
var userName: String
func fetchUserProfile() { }

// Constants: camelCase
let maxRetryCount = 3
let apiBaseURL = "https://api.example.com"

// Booleans: use is/has/should prefix
var isLoading: Bool
var hasCompletedOnboarding: Bool
func shouldShowAlert() -> Bool

// Delegates: use -Delegate suffix
protocol UserManagerDelegate: AnyObject { }

// Enums: use singular noun
enum Result { case success, failure }
enum Direction { case north, south, east, west }
```

**Quick SwiftLint Setup:**
```bash
# Install SwiftLint
brew install swiftlint

# Add to Xcode build phase
if which swiftlint >/dev/null; then
  swiftlint
fi

# Run manually
swiftlint lint
swiftlint autocorrect
```

---

## Level 2: Implementation Guide

### 1. Optionals and Safety

Swift's optional system eliminates null pointer exceptions through compile-time safety.

**Optional Fundamentals:**
```swift
// Optional represents presence or absence of a value
var middleName: String? = nil  // Can be nil
var firstName: String = "John"  // Cannot be nil

// Optional is an enum under the hood
enum Optional<Wrapped> {
    case none
    case some(Wrapped)
}
```

**Safe Unwrapping Patterns:**
```swift
// 1. Optional binding (most common)
if let unwrapped = optionalValue {
    // Use unwrapped value safely
    print(unwrapped)
}

// Multiple bindings
if let name = userName, let age = userAge, age >= 18 {
    print("\(name) is an adult")
}

// 2. Guard statement (early exit)
func processUser(_ user: User?) {
    guard let user = user else {
        print("No user provided")
        return
    }
    
    // user is available for rest of scope
    print(user.name)
}

// 3. Nil coalescing (default value)
let displayName = user?.name ?? "Guest"
let count = items?.count ?? 0

// 4. Optional chaining (safe navigation)
let streetName = user?.address?.street?.name
user?.profile?.updateLastSeen()

// 5. Optional map/flatMap
let uppercasedName = userName.map { $0.uppercased() }
let userID = userIDString.flatMap { Int($0) }
```

**When to Use Force Unwrapping:**
```swift
// ❌ Avoid in production code
let user = users.first!  // Crashes if empty

// ✅ Only when guaranteed non-nil
let url = URL(string: "https://example.com")!  // Literal URLs

// ✅ In fatalError scenarios
guard let apiKey = ProcessInfo.processInfo.environment["API_KEY"] else {
    fatalError("API_KEY not set in environment")
}
```

**Implicitly Unwrapped Optionals:**
```swift
// Use only for delayed initialization
class ViewController: UIViewController {
    @IBOutlet weak var tableView: UITableView!  // Set by storyboard
    
    var viewModel: ViewModel!  // Set before viewDidLoad
    
    override func viewDidLoad() {
        super.viewDidLoad()
        // Both guaranteed to exist here
        tableView.dataSource = viewModel
    }
}
```

### 2. Protocols and Protocol-Oriented Design

Swift favors composition over inheritance through protocols.

**Protocol Basics:**
```swift
// Protocol definition
protocol Identifiable {
    var id: UUID { get }
}

protocol Nameable {
    var name: String { get set }
}

protocol Drawable {
    func draw()
}

// Multiple protocol conformance
struct User: Identifiable, Nameable {
    let id: UUID
    var name: String
}

// Protocol inheritance
protocol Entity: Identifiable, Nameable {
    var createdAt: Date { get }
}
```

**Protocol Extensions (Superpowers):**
```swift
// Provide default implementations
extension Collection {
    func chunked(into size: Int) -> [[Element]] {
        stride(from: 0, to: count, by: size).map {
            Array(self[$0..<Swift.min($0 + size, count)])
        }
    }
}

// Now all collections have this method
let numbers = [1, 2, 3, 4, 5, 6]
let chunks = numbers.chunked(into: 2)  // [[1, 2], [3, 4], [5, 6]]

// Conditional conformance
extension Array: Drawable where Element: Drawable {
    func draw() {
        forEach { $0.draw() }
    }
}
```

**Protocol-Oriented Architecture:**
```swift
// Define capabilities through protocols
protocol DataStore {
    func save<T: Codable>(_ item: T, key: String) throws
    func load<T: Codable>(key: String) throws -> T?
}

// Multiple implementations
struct UserDefaultsStore: DataStore {
    func save<T: Codable>(_ item: T, key: String) throws {
        let data = try JSONEncoder().encode(item)
        UserDefaults.standard.set(data, forKey: key)
    }
    
    func load<T: Codable>(key: String) throws -> T? {
        guard let data = UserDefaults.standard.data(forKey: key) else {
            return nil
        }
        return try JSONDecoder().decode(T.self, from: data)
    }
}

struct FileStore: DataStore {
    let directory: URL
    
    func save<T: Codable>(_ item: T, key: String) throws {
        let url = directory.appendingPathComponent(key)
        let data = try JSONEncoder().encode(item)
        try data.write(to: url)
    }
    
    func load<T: Codable>(key: String) throws -> T? {
        let url = directory.appendingPathComponent(key)
        guard FileManager.default.fileExists(atPath: url.path) else {
            return nil
        }
        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode(T.self, from: data)
    }
}

// Dependency injection with protocols
class UserRepository {
    private let store: DataStore
    
    init(store: DataStore) {
        self.store = store
    }
    
    func saveUser(_ user: User) throws {
        try store.save(user, key: "user_\(user.id)")
    }
    
    func loadUser(id: UUID) throws -> User? {
        try store.load(key: "user_\(id)")
    }
}
```

**Associated Types:**
```swift
protocol Repository {
    associatedtype Item
    
    func fetchAll() async throws -> [Item]
    func save(_ item: Item) async throws
    func delete(_ item: Item) async throws
}

struct UserRepository: Repository {
    typealias Item = User
    
    func fetchAll() async throws -> [User] {
        // Implementation
    }
    
    func save(_ user: User) async throws {
        // Implementation
    }
    
    func delete(_ user: User) async throws {
        // Implementation
    }
}
```

### 3. Value Types vs Reference Types

Understanding the difference is crucial for performance and correctness.

**Value Types (struct, enum):**
```swift
struct Point {
    var x: Double
    var y: Double
}

var point1 = Point(x: 0, y: 0)
var point2 = point1  // Copies the value

point2.x = 10
print(point1.x)  // 0 (unchanged)
print(point2.x)  // 10

// Structs are thread-safe by default
let sharedPoint = Point(x: 5, y: 5)
// Can safely pass to multiple threads
```

**Reference Types (class):**
```swift
class Rectangle {
    var width: Double
    var height: Double
    
    init(width: Double, height: Double) {
        self.width = width
        self.height = height
    }
}

let rect1 = Rectangle(width: 10, height: 20)
let rect2 = rect1  // Copies the reference

rect2.width = 30
print(rect1.width)  // 30 (shared instance)
print(rect2.width)  // 30
```

**When to Use Each:**
```swift
// ✅ Use struct (value type) for:
// - Simple data models
// - Mathematical types (Point, Vector, Matrix)
// - Independent copies desired
struct User {
    var name: String
    var email: String
}

// ✅ Use class (reference type) for:
// - Shared mutable state
// - Object identity matters
// - Inheritance needed
class NetworkManager {
    static let shared = NetworkManager()
    private var sessions: [URLSession] = []
}

// ✅ Use enum for:
// - Finite set of options
// - State machines
enum LoadingState {
    case idle
    case loading
    case success(Data)
    case failure(Error)
}
```

**Copy-on-Write (COW):**
```swift
// Swift arrays, dictionaries, and sets use COW
var array1 = [1, 2, 3, 4, 5]
var array2 = array1  // Shares storage initially

array2.append(6)  // Now copies and modifies

// Implementing COW in custom types
struct MyArray<Element> {
    private var storage: ArrayStorage<Element>
    
    mutating func append(_ element: Element) {
        if !isKnownUniquelyReferenced(&storage) {
            storage = storage.copy()  // Copy before mutating
        }
        storage.append(element)
    }
}
```

### 4. Memory Management with ARC

Automatic Reference Counting manages memory automatically but requires understanding of retain cycles.

**Strong References (Default):**
```swift
class Person {
    let name: String
    var apartment: Apartment?
    
    init(name: String) {
        self.name = name
    }
    
    deinit {
        print("\(name) is being deinitialized")
    }
}

class Apartment {
    let unit: String
    var tenant: Person?
    
    init(unit: String) {
        self.unit = unit
    }
    
    deinit {
        print("Apartment \(unit) is being deinitialized")
    }
}

// Strong reference cycle (memory leak)
var john: Person? = Person(name: "John")
var unit4A: Apartment? = Apartment(unit: "4A")

john?.apartment = unit4A
unit4A?.tenant = john  // Cycle created

john = nil
unit4A = nil
// Neither deinit is called - memory leak!
```

**Breaking Cycles with weak and unowned:**
```swift
class Person {
    let name: String
    var apartment: Apartment?
    
    init(name: String) {
        self.name = name
    }
    
    deinit {
        print("\(name) is being deinitialized")
    }
}

class Apartment {
    let unit: String
    weak var tenant: Person?  // weak breaks the cycle
    
    init(unit: String) {
        self.unit = unit
    }
    
    deinit {
        print("Apartment \(unit) is being deinitialized")
    }
}

var john: Person? = Person(name: "John")
var unit4A: Apartment? = Apartment(unit: "4A")

john?.apartment = unit4A
unit4A?.tenant = john

john = nil  // "John is being deinitialized"
unit4A = nil  // "Apartment 4A is being deinitialized"
```

**weak vs unowned:**
```swift
// Use weak when reference can become nil
class ParentView {
    var childView: ChildView?
}

class ChildView {
    weak var parent: ParentView?  // Parent might be deallocated
}

// Use unowned when reference should never be nil
class Customer {
    let name: String
    var card: CreditCard?
    
    init(name: String) {
        self.name = name
    }
}

class CreditCard {
    let number: String
    unowned let customer: Customer  // Card can't exist without customer
    
    init(number: String, customer: Customer) {
        self.number = number
        self.customer = customer
    }
}
```

**Closure Capture Lists:**
```swift
class NetworkClient {
    var onComplete: (() -> Void)?
    
    func fetchData() {
        // ❌ Strong reference cycle
        onComplete = {
            self.processResult()  // Captures self strongly
        }
        
        // ✅ Break cycle with capture list
        onComplete = { [weak self] in
            self?.processResult()  // Safe optional call
        }
        
        // ✅ Unowned when self outlives closure
        onComplete = { [unowned self] in
            self.processResult()  // No optional needed
        }
    }
    
    private func processResult() { }
}
```

### 5. Error Handling

Swift provides multiple error handling strategies.

**Throwing Functions:**
```swift
enum NetworkError: Error {
    case invalidURL
    case noConnection
    case serverError(statusCode: Int)
    case decodingFailed
}

func fetchUser(id: Int) throws -> User {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        throw NetworkError.invalidURL
    }
    
    let (data, response) = try await URLSession.shared.data(from: url)
    
    guard let httpResponse = response as? HTTPURLResponse else {
        throw NetworkError.noConnection
    }
    
    guard (200...299).contains(httpResponse.statusCode) else {
        throw NetworkError.serverError(statusCode: httpResponse.statusCode)
    }
    
    do {
        return try JSONDecoder().decode(User.self, from: data)
    } catch {
        throw NetworkError.decodingFailed
    }
}

// Calling throwing functions
do {
    let user = try fetchUser(id: 123)
    print("Fetched: \(user.name)")
} catch NetworkError.invalidURL {
    print("Invalid URL provided")
} catch NetworkError.serverError(let code) {
    print("Server error: \(code)")
} catch {
    print("Unknown error: \(error)")
}
```

**Result Type:**
```swift
func fetchUser(id: Int, completion: @escaping (Result<User, NetworkError>) -> Void) {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        completion(.failure(.invalidURL))
        return
    }
    
    URLSession.shared.dataTask(with: url) { data, response, error in
        if let error = error {
            completion(.failure(.noConnection))
            return
        }
        
        guard let data = data else {
            completion(.failure(.noConnection))
            return
        }
        
        do {
            let user = try JSONDecoder().decode(User.self, from: data)
            completion(.success(user))
        } catch {
            completion(.failure(.decodingFailed))
        }
    }.resume()
}

// Using Result
fetchUser(id: 123) { result in
    switch result {
    case .success(let user):
        print("Fetched: \(user.name)")
    case .failure(let error):
        print("Error: \(error)")
    }
}
```

**try? and try!:**
```swift
// try? converts result to optional
let user = try? fetchUser(id: 123)  // Returns nil on error

// try! force-unwraps (crashes on error)
let configFile = try! String(contentsOf: configURL)  // Use only when certain
```

### 6. Modern Concurrency (async/await)

Swift's structured concurrency makes asynchronous code safe and readable.

**Async Functions:**
```swift
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}

// Calling async functions
Task {
    do {
        let user = try await fetchUser(id: 123)
        print("Fetched: \(user.name)")
    } catch {
        print("Error: \(error)")
    }
}
```

**Parallel Execution:**
```swift
// Sequential (slow)
func fetchAllUsersSequential(ids: [Int]) async throws -> [User] {
    var users: [User] = []
    for id in ids {
        let user = try await fetchUser(id: id)  // Waits for each
        users.append(user)
    }
    return users
}

// Parallel (fast)
func fetchAllUsersParallel(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)  // All execute concurrently
            }
        }
        
        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```

**Actors (Thread-Safe Classes):**
```swift
actor BankAccount {
    private var balance: Double = 0
    
    func deposit(_ amount: Double) {
        balance += amount
    }
    
    func withdraw(_ amount: Double) throws {
        guard balance >= amount else {
            throw BankError.insufficientFunds
        }
        balance -= amount
    }
    
    func getBalance() -> Double {
        balance
    }
}

// Usage (automatically thread-safe)
let account = BankAccount()

Task {
    await account.deposit(100)
    let balance = await account.getBalance()
    print("Balance: \(balance)")
}
```

**MainActor (UI Updates):**
```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var isLoading = false
    @Published var users: [User] = []
    @Published var error: Error?
    
    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            // Background work
            users = try await fetchAllUsers()
        } catch {
            self.error = error
        }
    }
}

// In SwiftUI view
Button("Load") {
    Task {
        await viewModel.loadUsers()  // Automatically on main thread
    }
}
```

### 7. Testing with XCTest

Write comprehensive tests for reliability.

**Unit Test Structure:**
```swift
import XCTest
@testable import MyApp

final class UserManagerTests: XCTestCase {
    var sut: UserManager!
    var mockStore: MockDataStore!
    
    override func setUp() {
        super.setUp()
        mockStore = MockDataStore()
        sut = UserManager(store: mockStore)
    }
    
    override func tearDown() {
        sut = nil
        mockStore = nil
        super.tearDown()
    }
    
    func testFetchUser_Success() async throws {
        // Arrange
        let expectedUser = User(id: 1, name: "John")
        mockStore.userToReturn = expectedUser
        
        // Act
        let user = try await sut.fetchUser(id: 1)
        
        // Assert
        XCTAssertEqual(user.id, expectedUser.id)
        XCTAssertEqual(user.name, expectedUser.name)
        XCTAssertTrue(mockStore.fetchUserCalled)
    }
    
    func testFetchUser_NetworkError() async {
        // Arrange
        mockStore.errorToThrow = NetworkError.noConnection
        
        // Act & Assert
        do {
            _ = try await sut.fetchUser(id: 1)
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is NetworkError)
        }
    }
}
```

**Mock Objects:**
```swift
class MockDataStore: DataStore {
    var userToReturn: User?
    var errorToThrow: Error?
    var fetchUserCalled = false
    var saveUserCalled = false
    
    func fetchUser(id: Int) async throws -> User {
        fetchUserCalled = true
        if let error = errorToThrow {
            throw error
        }
        guard let user = userToReturn else {
            throw DataError.notFound
        }
        return user
    }
    
    func saveUser(_ user: User) async throws {
        saveUserCalled = true
        if let error = errorToThrow {
            throw error
        }
    }
}
```

**Testing Async Code:**
```swift
func testAsyncFunction() async throws {
    let result = await someAsyncFunction()
    XCTAssertEqual(result, expectedValue)
}

func testWithExpectation() {
    let expectation = expectation(description: "Callback called")
    
    service.fetchData { result in
        XCTAssertNotNil(result)
        expectation.fulfill()
    }
    
    waitForExpectations(timeout: 5)
}
```

**UI Testing:**
```swift
final class AppUITests: XCTestCase {
    var app: XCUIApplication!
    
    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }
    
    func testLoginFlow() {
        // Find and tap elements
        let emailField = app.textFields["Email"]
        emailField.tap()
        emailField.typeText("test@example.com")
        
        let passwordField = app.secureTextFields["Password"]
        passwordField.tap()
        passwordField.typeText("password123")
        
        app.buttons["Log In"].tap()
        
        // Assert navigation occurred
        XCTAssertTrue(app.navigationBars["Home"].exists)
    }
}
```

---

## Level 3: Deep Dive Resources

### Advanced Topics

**Generics Deep Dive:**
- Generic type constraints and where clauses
- Associated types with constraints
- Generic subscripts and operators
- Type erasure patterns (AnySequence, etc.)
- Phantom types for compile-time safety

**Property Wrappers:**
- @State, @Binding, @Published, @Environment in SwiftUI
- Creating custom property wrappers
- Projected values ($-syntax)
- Composition of property wrappers

**Result Builders:**
- Understanding @resultBuilder (SwiftUI views, etc.)
- Creating custom DSLs
- buildBlock, buildOptional, buildEither
- Declarative syntax patterns

**SwiftUI Architecture:**
- MVVM pattern with Combine/async-await
- State management (State, StateObject, ObservedObject)
- Environment and dependency injection
- Navigation patterns (NavigationStack, NavigationPath)
- Custom view modifiers and view builders

**Performance Optimization:**
- Instruments profiling (Time Profiler, Allocations)
- Copy-on-write optimization
- Lazy initialization patterns
- Struct vs class performance characteristics
- Swift compiler optimization levels

### Official Documentation

- [Swift Language Guide](https://docs.swift.org/swift-book/)
- [API Design Guidelines](https://swift.org/documentation/api-design-guidelines/)
- [Swift Evolution Proposals](https://github.com/apple/swift-evolution)
- [WWDC Videos](https://developer.apple.com/videos/)
- [Swift Forums](https://forums.swift.org/)

### Recommended Learning Path

1. **Week 1-2**: Optionals, protocols, value/reference types
2. **Week 3-4**: Memory management, error handling, testing
3. **Week 5-6**: Async/await, actors, structured concurrency
4. **Week 7-8**: SwiftUI, Combine, advanced patterns

### Community Resources

- [Swift by Sundell](https://www.swiftbysundell.com/) - Articles and podcasts
- [Hacking with Swift](https://www.hackingwithswift.com/) - Tutorials and examples
- [Point-Free](https://www.pointfree.co/) - Advanced functional Swift
- [Swift Forums](https://forums.swift.org/) - Official community discussions

---

## Practice Projects

### Beginner: Todo App with SwiftUI
Build a todo list with local persistence using UserDefaults and protocol-oriented architecture.

**Skills practiced:**
- SwiftUI views and state management
- Protocol-oriented design (DataStore protocol)
- MVVM architecture
- Unit testing with XCTest

### Intermediate: GitHub Client
Create a GitHub repository browser using async/await and URLSession.

**Skills practiced:**
- Modern concurrency (async/await)
- Network layer architecture
- Error handling with Result type
- JSON decoding with Codable
- Actor-based caching

### Advanced: Real-time Chat
Build a chat application with WebSocket support and local database.

**Skills practiced:**
- Structured concurrency with TaskGroup
- Actor isolation for thread safety
- CoreData or Realm integration
- Custom Combine publishers
- Memory management with delegates

---

## Bundled Resources

This skill includes the following resources in the `swift/` directory:

1. **config/.swiftlint.yml** - Comprehensive SwiftLint configuration
2. **templates/ViewModel.swift** - MVVM ViewModel template with async patterns
3. **templates/Protocol.swift** - Protocol-oriented design examples
4. **templates/NetworkService.swift** - Modern network layer with async/await
5. **templates/TestCase.swift** - XCTest template with mocking
6. **scripts/setup-swift-project.sh** - Project setup automation script

### Usage

```bash
# Setup new Swift project
./scripts/setup-swift-project.sh MyProject

# Run SwiftLint
swiftlint lint --config config/.swiftlint.yml

# Copy templates
cp templates/ViewModel.swift MyProject/Sources/
cp templates/NetworkService.swift MyProject/Sources/
```

---

## Validation Checklist

Before considering this skill mastered, ensure you can:

- [ ] Explain the Optional type and demonstrate 5 unwrapping patterns
- [ ] Design a system using protocols instead of inheritance
- [ ] Identify and fix retain cycles in code
- [ ] Write async/await code with proper error handling
- [ ] Create actors to prevent data races
- [ ] Write unit tests with mocks for network code
- [ ] Set up SwiftLint in an Xcode project
- [ ] Explain value semantics and when to use struct vs class
- [ ] Implement protocol extensions with default behavior
- [ ] Use Task Groups for parallel async operations

---

## Additional Learning Resources

### Books
- "Swift Programming: The Big Nerd Ranch Guide"
- "Advanced Swift" by objc.io
- "Thinking in SwiftUI"

### Video Courses
- Stanford CS193p (SwiftUI)
- Ray Wenderlich iOS & Swift tutorials
- WWDC session videos

### Practice Platforms
- LeetCode (Swift problems)
- HackerRank (Swift track)
- Project Euler (algorithm practice)

---

## Maintenance & Updates

**Current Version:** 1.0.0 (October 2025)

**Last Updated:** Swift 6.0, iOS 18, Xcode 16

This skill is maintained in alignment with:
- Apple's Swift Evolution roadmap
- Current Xcode releases
- iOS/macOS SDK updates
- Community best practices

For updates and contributions, see the [standards repository](https://github.com/williamzujkowski/standards).

---

*Remember: Swift is designed for safety, speed, and expressiveness. Embrace optionals, leverage protocols, and write tests. Happy coding!*
