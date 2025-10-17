import Foundation

// MARK: - Protocol-Oriented Design Examples

// Example 1: Basic Protocol with Extension
protocol Drawable {
    var color: String { get set }
    func draw()
}

extension Drawable {
    // Default implementation
    func draw() {
        print("Drawing with color: \(color)")
    }

    // Additional functionality via extension
    func highlight() {
        print("Highlighting \(color)")
    }
}

// Example 2: Protocol Composition
protocol Identifiable {
    var id: UUID { get }
}

protocol Timestampable {
    var createdAt: Date { get }
    var updatedAt: Date { get set }
}

typealias Entity = Identifiable & Timestampable

struct User: Entity {
    let id: UUID
    let createdAt: Date
    var updatedAt: Date
    var name: String
}

// Example 3: Protocol with Associated Types
protocol Repository {
    associatedtype Item

    func fetchAll() async throws -> [Item]
    func save(_ item: Item) async throws
    func delete(_ item: Item) async throws
}

protocol Cache {
    associatedtype Key: Hashable
    associatedtype Value

    func get(_ key: Key) -> Value?
    func set(_ key: Key, value: Value)
    func clear()
}

// Example 4: Generic Protocol Implementation
struct InMemoryCache<K: Hashable, V>: Cache {
    typealias Key = K
    typealias Value = V

    private var storage: [K: V] = [:]

    func get(_ key: K) -> V? {
        storage[key]
    }

    mutating func set(_ key: K, value: V) {
        storage[key] = value
    }

    mutating func clear() {
        storage.removeAll()
    }
}

// Example 5: Protocol-Based Dependency Injection
protocol NetworkService {
    func request<T: Decodable>(_ endpoint: String) async throws -> T
}

protocol StorageService {
    func save<T: Codable>(_ value: T, key: String) throws
    func load<T: Codable>(key: String) throws -> T?
}

class UserManager {
    private let network: NetworkService
    private let storage: StorageService

    init(network: NetworkService, storage: StorageService) {
        self.network = network
        self.storage = storage
    }

    func fetchUser(id: String) async throws -> User {
        // Try cache first
        if let cached: User = try? storage.load(key: "user_\(id)") {
            return cached
        }

        // Fetch from network
        let user: User = try await network.request("/users/\(id)")

        // Cache result
        try? storage.save(user, key: "user_\(id)")

        return user
    }
}

// Example 6: Protocol with Conditional Conformance
extension Array: Drawable where Element: Drawable {
    var color: String {
        get { first?.color ?? "default" }
        set { forEach { var element = $0; element.color = newValue } }
    }

    func draw() {
        forEach { $0.draw() }
    }
}

// Example 7: Protocol Inheritance
protocol Animal {
    var name: String { get }
    func makeSound()
}

protocol Pet: Animal {
    var owner: String { get }
    func cuddle()
}

struct Dog: Pet {
    let name: String
    let owner: String

    func makeSound() {
        print("\(name) says: Woof!")
    }

    func cuddle() {
        print("\(name) cuddles with \(owner)")
    }
}

// Example 8: Protocol with Default Implementations
protocol Logger {
    func log(_ message: String)
    func logError(_ error: Error)
    func logWarning(_ message: String)
}

extension Logger {
    func logError(_ error: Error) {
        log("ERROR: \(error.localizedDescription)")
    }

    func logWarning(_ message: String) {
        log("WARNING: \(message)")
    }
}

struct ConsoleLogger: Logger {
    func log(_ message: String) {
        print(message)
    }
}

// Example 9: Protocol for Strategy Pattern
protocol SortStrategy {
    func sort<T: Comparable>(_ items: [T]) -> [T]
}

struct AscendingSort: SortStrategy {
    func sort<T: Comparable>(_ items: [T]) -> [T] {
        items.sorted(by: <)
    }
}

struct DescendingSort: SortStrategy {
    func sort<T: Comparable>(_ items: [T]) -> [T] {
        items.sorted(by: >)
    }
}

class DataSorter {
    private let strategy: SortStrategy

    init(strategy: SortStrategy) {
        self.strategy = strategy
    }

    func sort<T: Comparable>(_ items: [T]) -> [T] {
        strategy.sort(items)
    }
}

// Example 10: Protocol with @escaping Closures
protocol EventHandler {
    associatedtype Event

    func handle(_ event: Event, completion: @escaping (Result<Void, Error>) -> Void)
}

class AsyncEventHandler<E>: EventHandler {
    typealias Event = E

    private let handler: (E) async throws -> Void

    init(handler: @escaping (E) async throws -> Void) {
        self.handler = handler
    }

    func handle(_ event: E, completion: @escaping (Result<Void, Error>) -> Void) {
        Task {
            do {
                try await handler(event)
                completion(.success(()))
            } catch {
                completion(.failure(error))
            }
        }
    }
}
