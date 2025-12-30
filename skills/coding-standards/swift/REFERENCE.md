# Swift Coding Standards - Complete Reference

> This document contains comprehensive examples, detailed configurations, and production-ready templates for Swift development. For the quick reference guide, see [SKILL.md](./SKILL.md).

## Table of Contents

- [Optionals Deep Dive](#optionals-deep-dive)
- [Protocol-Oriented Architecture](#protocol-oriented-architecture)
- [Value Types vs Reference Types](#value-types-vs-reference-types)
- [Memory Management with ARC](#memory-management-with-arc)
- [Error Handling Patterns](#error-handling-patterns)
- [Modern Concurrency](#modern-concurrency)
- [Testing Patterns](#testing-patterns)
- [SwiftUI Patterns](#swiftui-patterns)
- [SwiftLint Configuration](#swiftlint-configuration)
- [Practice Projects](#practice-projects)

---

## Optionals Deep Dive

### Optional Fundamentals

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

### Complete Unwrapping Patterns

```swift
// 1. Optional binding (most common)
if let unwrapped = optionalValue {
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

### When to Use Force Unwrapping

```swift
// Avoid in production code
let user = users.first!  // Crashes if empty

// Only when guaranteed non-nil
let url = URL(string: "https://example.com")!  // Literal URLs

// In fatalError scenarios
guard let apiKey = ProcessInfo.processInfo.environment["API_KEY"] else {
    fatalError("API_KEY not set in environment")
}
```

### Implicitly Unwrapped Optionals

```swift
// Use only for delayed initialization
class ViewController: UIViewController {
    @IBOutlet weak var tableView: UITableView!  // Set by storyboard
    var viewModel: ViewModel!  // Set before viewDidLoad

    override func viewDidLoad() {
        super.viewDidLoad()
        tableView.dataSource = viewModel
    }
}
```

---

## Protocol-Oriented Architecture

### Complete DataStore Implementation

```swift
// Define capabilities through protocols
protocol DataStore {
    func save<T: Codable>(_ item: T, key: String) throws
    func load<T: Codable>(key: String) throws -> T?
}

// UserDefaults implementation
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

// File-based implementation
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

### Protocol Extensions

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

### Associated Types

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

---

## Value Types vs Reference Types

### Value Types (struct, enum)

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

### Reference Types (class)

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

### When to Use Each

```swift
// Use struct (value type) for:
// - Simple data models
// - Mathematical types (Point, Vector, Matrix)
// - Independent copies desired
struct User {
    var name: String
    var email: String
}

// Use class (reference type) for:
// - Shared mutable state
// - Object identity matters
// - Inheritance needed
class NetworkManager {
    static let shared = NetworkManager()
    private var sessions: [URLSession] = []
}

// Use enum for:
// - Finite set of options
// - State machines
enum LoadingState {
    case idle
    case loading
    case success(Data)
    case failure(Error)
}
```

### Copy-on-Write (COW)

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

---

## Memory Management with ARC

### Strong Reference Cycles

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
    var tenant: Person?  // Creates cycle

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

### Breaking Cycles

```swift
class Apartment {
    let unit: String
    weak var tenant: Person?  // weak breaks the cycle

    init(unit: String) {
        self.unit = unit
    }
}

// Now both objects can be deallocated
john = nil  // "John is being deinitialized"
unit4A = nil  // "Apartment 4A is being deinitialized"
```

### weak vs unowned

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

### Closure Capture Lists

```swift
class NetworkClient {
    var onComplete: (() -> Void)?

    func fetchData() {
        // Strong reference cycle
        onComplete = {
            self.processResult()  // Captures self strongly
        }

        // Break cycle with capture list
        onComplete = { [weak self] in
            self?.processResult()  // Safe optional call
        }

        // Unowned when self outlives closure
        onComplete = { [unowned self] in
            self.processResult()  // No optional needed
        }
    }

    private func processResult() { }
}
```

---

## Error Handling Patterns

### Custom Error Types

```swift
enum NetworkError: Error {
    case invalidURL
    case noConnection
    case serverError(statusCode: Int)
    case decodingFailed
}

// LocalizedError for user-facing messages
extension NetworkError: LocalizedError {
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "The URL provided is invalid."
        case .noConnection:
            return "No internet connection."
        case .serverError(let code):
            return "Server error with status code: \(code)"
        case .decodingFailed:
            return "Failed to decode the response."
        }
    }
}
```

### Throwing Functions

```swift
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

### Result Type

```swift
func fetchUser(id: Int, completion: @escaping (Result<User, NetworkError>) -> Void) {
    guard let url = URL(string: "https://api.example.com/users/\(id)") else {
        completion(.failure(.invalidURL))
        return
    }

    URLSession.shared.dataTask(with: url) { data, response, error in
        if error != nil {
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

---

## Modern Concurrency

### Async Functions

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

### Parallel Execution

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

### Actors

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

### MainActor

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

---

## Testing Patterns

### Unit Test Structure

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

### Mock Objects

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

### Testing Async Code

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

### UI Testing

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

## SwiftUI Patterns

### MVVM Architecture

```swift
// Model
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModel
@MainActor
class UserListViewModel: ObservableObject {
    @Published var users: [User] = []
    @Published var isLoading = false
    @Published var error: Error?

    private let repository: UserRepository

    init(repository: UserRepository) {
        self.repository = repository
    }

    func loadUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await repository.fetchAll()
        } catch {
            self.error = error
        }
    }
}

// View
struct UserListView: View {
    @StateObject private var viewModel: UserListViewModel

    init(repository: UserRepository) {
        _viewModel = StateObject(wrappedValue: UserListViewModel(repository: repository))
    }

    var body: some View {
        List(viewModel.users) { user in
            Text(user.name)
        }
        .task {
            await viewModel.loadUsers()
        }
    }
}
```

### State Management

```swift
// @State for local view state
struct CounterView: View {
    @State private var count = 0

    var body: some View {
        Button("Count: \(count)") {
            count += 1
        }
    }
}

// @Binding for two-way data flow
struct ToggleRow: View {
    @Binding var isOn: Bool
    let title: String

    var body: some View {
        Toggle(title, isOn: $isOn)
    }
}

// @StateObject for owned observable objects
struct ParentView: View {
    @StateObject private var viewModel = ViewModel()

    var body: some View {
        ChildView(viewModel: viewModel)
    }
}

// @ObservedObject for passed observable objects
struct ChildView: View {
    @ObservedObject var viewModel: ViewModel

    var body: some View {
        Text(viewModel.title)
    }
}

// @EnvironmentObject for dependency injection
struct ContentView: View {
    @EnvironmentObject var settings: AppSettings

    var body: some View {
        Text("Theme: \(settings.theme)")
    }
}
```

---

## SwiftLint Configuration

```yaml
# .swiftlint.yml
included:
  - Sources
  - Tests

excluded:
  - Pods
  - .build
  - DerivedData

disabled_rules:
  - todo
  - trailing_whitespace

opt_in_rules:
  - array_init
  - closure_spacing
  - collection_alignment
  - contains_over_filter_count
  - contains_over_first_not_nil
  - empty_collection_literal
  - empty_count
  - empty_string
  - explicit_init
  - first_where
  - force_unwrapping
  - implicitly_unwrapped_optional
  - last_where
  - literal_expression_end_indentation
  - modifier_order
  - multiline_arguments
  - multiline_parameters
  - operator_usage_whitespace
  - overridden_super_call
  - prefer_self_type_over_type_of_self
  - prefer_zero_over_explicit_init
  - private_action
  - private_outlet
  - redundant_nil_coalescing
  - redundant_type_annotation
  - sorted_first_last
  - toggle_bool
  - trailing_closure
  - unneeded_parentheses_in_closure_argument
  - vertical_parameter_alignment_on_call
  - yoda_condition

line_length:
  warning: 120
  error: 150
  ignores_comments: true
  ignores_urls: true

type_body_length:
  warning: 300
  error: 500

file_length:
  warning: 500
  error: 1000

function_body_length:
  warning: 40
  error: 80

function_parameter_count:
  warning: 5
  error: 8

type_name:
  min_length: 3
  max_length: 50

identifier_name:
  min_length:
    warning: 2
    error: 1
  max_length:
    warning: 50
    error: 60
  excluded:
    - id
    - ok
    - or
    - x
    - y
    - z

nesting:
  type_level: 3
  function_level: 3

reporter: xcode
```

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

## Validation Checklist

Before considering Swift mastery complete:

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

## Additional Resources

### Books

- "Swift Programming: The Big Nerd Ranch Guide"
- "Advanced Swift" by objc.io
- "Thinking in SwiftUI"

### Video Courses

- Stanford CS193p (SwiftUI)
- Ray Wenderlich iOS & Swift tutorials
- WWDC session videos

### Community Resources

- [Swift by Sundell](https://www.swiftbysundell.com/) - Articles and podcasts
- [Hacking with Swift](https://www.hackingwithswift.com/) - Tutorials
- [Point-Free](https://www.pointfree.co/) - Advanced functional Swift
- [Swift Forums](https://forums.swift.org/) - Official discussions

---

**Current Version:** 1.0.0 (October 2025)
**Swift Version:** Swift 6.0, iOS 18, Xcode 16

For updates and contributions, see the [standards repository](https://github.com/williamzujkowski/standards).
