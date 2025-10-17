import XCTest
@testable import YourModule

// MARK: - XCTest Template with Mocking and Async Testing

final class ExampleServiceTests: XCTestCase {
    // MARK: - System Under Test
    
    var sut: ExampleService!
    
    // MARK: - Mock Dependencies
    
    var mockNetworkService: MockNetworkService!
    var mockStorageService: MockStorageService!
    
    // MARK: - Setup & Teardown
    
    override func setUp() {
        super.setUp()
        
        mockNetworkService = MockNetworkService()
        mockStorageService = MockStorageService()
        
        sut = ExampleService(
            network: mockNetworkService,
            storage: mockStorageService
        )
    }
    
    override func tearDown() {
        sut = nil
        mockNetworkService = nil
        mockStorageService = nil
        
        super.tearDown()
    }
    
    // MARK: - Tests
    
    func testFetchUser_Success() async throws {
        // Arrange
        let expectedUser = User(id: UUID(), name: "John Doe", email: "john@example.com")
        mockNetworkService.userToReturn = expectedUser
        
        // Act
        let result = try await sut.fetchUser(id: expectedUser.id)
        
        // Assert
        XCTAssertEqual(result.id, expectedUser.id)
        XCTAssertEqual(result.name, expectedUser.name)
        XCTAssertEqual(result.email, expectedUser.email)
        XCTAssertTrue(mockNetworkService.fetchUserCalled)
        XCTAssertEqual(mockNetworkService.fetchUserCallCount, 1)
    }
    
    func testFetchUser_NetworkError() async {
        // Arrange
        mockNetworkService.errorToThrow = NetworkError.noConnection
        
        // Act & Assert
        do {
            _ = try await sut.fetchUser(id: UUID())
            XCTFail("Expected error to be thrown")
        } catch let error as NetworkError {
            XCTAssertEqual(error, NetworkError.noConnection)
        } catch {
            XCTFail("Unexpected error type: \(error)")
        }
    }
    
    func testCacheUser_Success() async throws {
        // Arrange
        let user = User(id: UUID(), name: "Jane Doe", email: "jane@example.com")
        
        // Act
        try await sut.cacheUser(user)
        
        // Assert
        XCTAssertTrue(mockStorageService.saveUserCalled)
        XCTAssertEqual(mockStorageService.savedUser?.id, user.id)
    }
    
    func testLoadCachedUser_Success() async throws {
        // Arrange
        let user = User(id: UUID(), name: "Bob", email: "bob@example.com")
        mockStorageService.userToReturn = user
        
        // Act
        let result = try await sut.loadCachedUser(id: user.id)
        
        // Assert
        XCTAssertEqual(result?.id, user.id)
        XCTAssertTrue(mockStorageService.loadUserCalled)
    }
    
    func testLoadCachedUser_NotFound() async throws {
        // Arrange
        mockStorageService.userToReturn = nil
        
        // Act
        let result = try await sut.loadCachedUser(id: UUID())
        
        // Assert
        XCTAssertNil(result)
    }
    
    // MARK: - Performance Tests
    
    func testFetchUserPerformance() {
        let user = User(id: UUID(), name: "Test", email: "test@example.com")
        mockNetworkService.userToReturn = user
        
        measure {
            let expectation = expectation(description: "Fetch completes")
            
            Task {
                _ = try? await sut.fetchUser(id: user.id)
                expectation.fulfill()
            }
            
            waitForExpectations(timeout: 1.0)
        }
    }
    
    // MARK: - Edge Cases
    
    func testFetchUser_EmptyResponse() async {
        // Arrange
        mockNetworkService.userToReturn = nil
        
        // Act & Assert
        do {
            _ = try await sut.fetchUser(id: UUID())
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is ServiceError)
        }
    }
}

// MARK: - Mock Network Service

class MockNetworkService: NetworkService {
    var userToReturn: User?
    var errorToThrow: Error?
    var fetchUserCalled = false
    var fetchUserCallCount = 0
    
    func fetchUser(id: UUID) async throws -> User {
        fetchUserCalled = true
        fetchUserCallCount += 1
        
        if let error = errorToThrow {
            throw error
        }
        
        guard let user = userToReturn else {
            throw ServiceError.userNotFound
        }
        
        return user
    }
}

// MARK: - Mock Storage Service

class MockStorageService: StorageService {
    var userToReturn: User?
    var errorToThrow: Error?
    var saveUserCalled = false
    var loadUserCalled = false
    var savedUser: User?
    
    func saveUser(_ user: User) async throws {
        saveUserCalled = true
        savedUser = user
        
        if let error = errorToThrow {
            throw error
        }
    }
    
    func loadUser(id: UUID) async throws -> User? {
        loadUserCalled = true
        
        if let error = errorToThrow {
            throw error
        }
        
        return userToReturn
    }
    
    func deleteUser(id: UUID) async throws {
        if let error = errorToThrow {
            throw error
        }
    }
}

// MARK: - Test Helpers

extension XCTestCase {
    func wait(for duration: TimeInterval) async {
        try? await Task.sleep(nanoseconds: UInt64(duration * 1_000_000_000))
    }
}

// MARK: - Supporting Types

struct User: Codable, Equatable {
    let id: UUID
    var name: String
    var email: String
}

enum NetworkError: Error, Equatable {
    case noConnection
    case timeout
    case serverError
}

enum ServiceError: Error {
    case userNotFound
    case invalidData
}

protocol NetworkService {
    func fetchUser(id: UUID) async throws -> User
}

protocol StorageService {
    func saveUser(_ user: User) async throws
    func loadUser(id: UUID) async throws -> User?
    func deleteUser(id: UUID) async throws
}

class ExampleService {
    private let network: NetworkService
    private let storage: StorageService
    
    init(network: NetworkService, storage: StorageService) {
        self.network = network
        self.storage = storage
    }
    
    func fetchUser(id: UUID) async throws -> User {
        // Try cache first
        if let cached = try? await storage.loadUser(id: id) {
            return cached
        }
        
        // Fetch from network
        let user = try await network.fetchUser(id: id)
        
        // Cache result
        try? await storage.saveUser(user)
        
        return user
    }
    
    func cacheUser(_ user: User) async throws {
        try await storage.saveUser(user)
    }
    
    func loadCachedUser(id: UUID) async throws -> User? {
        try await storage.loadUser(id: id)
    }
}
