import Foundation

// MARK: - Network Service with Modern Async/Await

/// A protocol-oriented network layer using async/await
protocol NetworkService {
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T
    func request(_ endpoint: Endpoint) async throws -> Data
}

// MARK: - Endpoint Definition

struct Endpoint {
    let path: String
    let method: HTTPMethod
    let headers: [String: String]?
    let body: Data?
    
    enum HTTPMethod: String {
        case get = "GET"
        case post = "POST"
        case put = "PUT"
        case delete = "DELETE"
        case patch = "PATCH"
    }
    
    init(
        path: String,
        method: HTTPMethod = .get,
        headers: [String: String]? = nil,
        body: Data? = nil
    ) {
        self.path = path
        self.method = method
        self.headers = headers
        self.body = body
    }
}

// MARK: - Network Errors

enum NetworkError: LocalizedError {
    case invalidURL
    case noData
    case decodingFailed
    case serverError(statusCode: Int)
    case unauthorized
    case timeout
    case noConnection
    
    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "The URL provided was invalid"
        case .noData:
            return "No data received from server"
        case .decodingFailed:
            return "Failed to decode server response"
        case .serverError(let code):
            return "Server error with status code: \(code)"
        case .unauthorized:
            return "Unauthorized access"
        case .timeout:
            return "Request timed out"
        case .noConnection:
            return "No internet connection"
        }
    }
}

// MARK: - Default Implementation

final class DefaultNetworkService: NetworkService {
    private let baseURL: String
    private let session: URLSession
    private let decoder: JSONDecoder
    
    init(
        baseURL: String,
        session: URLSession = .shared,
        decoder: JSONDecoder = JSONDecoder()
    ) {
        self.baseURL = baseURL
        self.session = session
        self.decoder = decoder
        
        // Configure decoder
        decoder.dateDecodingStrategy = .iso8601
        decoder.keyDecodingStrategy = .convertFromSnakeCase
    }
    
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let data = try await request(endpoint)
        
        do {
            return try decoder.decode(T.self, from: data)
        } catch {
            throw NetworkError.decodingFailed
        }
    }
    
    func request(_ endpoint: Endpoint) async throws -> Data {
        guard let url = URL(string: baseURL + endpoint.path) else {
            throw NetworkError.invalidURL
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = endpoint.method.rawValue
        request.httpBody = endpoint.body
        
        // Add headers
        endpoint.headers?.forEach { key, value in
            request.setValue(value, forHTTPHeaderField: key)
        }
        
        // Default headers
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")
        
        do {
            let (data, response) = try await session.data(for: request)
            
            guard let httpResponse = response as? HTTPURLResponse else {
                throw NetworkError.noConnection
            }
            
            switch httpResponse.statusCode {
            case 200...299:
                return data
            case 401:
                throw NetworkError.unauthorized
            case 408:
                throw NetworkError.timeout
            default:
                throw NetworkError.serverError(statusCode: httpResponse.statusCode)
            }
        } catch let error as NetworkError {
            throw error
        } catch {
            throw NetworkError.noConnection
        }
    }
}

// MARK: - Authenticated Network Service

final class AuthenticatedNetworkService: NetworkService {
    private let baseService: NetworkService
    private let tokenProvider: TokenProvider
    
    init(baseService: NetworkService, tokenProvider: TokenProvider) {
        self.baseService = baseService
        self.tokenProvider = tokenProvider
    }
    
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let authenticatedEndpoint = try await addAuthentication(to: endpoint)
        return try await baseService.request(authenticatedEndpoint)
    }
    
    func request(_ endpoint: Endpoint) async throws -> Data {
        let authenticatedEndpoint = try await addAuthentication(to: endpoint)
        return try await baseService.request(authenticatedEndpoint)
    }
    
    private func addAuthentication(to endpoint: Endpoint) async throws -> Endpoint {
        let token = try await tokenProvider.getToken()
        
        var headers = endpoint.headers ?? [:]
        headers["Authorization"] = "Bearer \(token)"
        
        return Endpoint(
            path: endpoint.path,
            method: endpoint.method,
            headers: headers,
            body: endpoint.body
        )
    }
}

// MARK: - Token Provider Protocol

protocol TokenProvider {
    func getToken() async throws -> String
    func refreshToken() async throws -> String
}

// MARK: - Response Caching

actor NetworkCache {
    private var cache: [String: CachedResponse] = [:]
    
    struct CachedResponse {
        let data: Data
        let expiresAt: Date
    }
    
    func get(for key: String) -> Data? {
        guard let cached = cache[key],
              cached.expiresAt > Date() else {
            cache.removeValue(forKey: key)
            return nil
        }
        return cached.data
    }
    
    func set(_ data: Data, for key: String, ttl: TimeInterval = 300) {
        let cached = CachedResponse(
            data: data,
            expiresAt: Date().addingTimeInterval(ttl)
        )
        cache[key] = cached
    }
    
    func clear() {
        cache.removeAll()
    }
}

// MARK: - Cached Network Service

final class CachedNetworkService: NetworkService {
    private let baseService: NetworkService
    private let cache: NetworkCache
    
    init(baseService: NetworkService, cache: NetworkCache = NetworkCache()) {
        self.baseService = baseService
        self.cache = cache
    }
    
    func request<T: Decodable>(_ endpoint: Endpoint) async throws -> T {
        let cacheKey = endpoint.path
        
        // Try cache first for GET requests
        if endpoint.method == .get,
           let cachedData = await cache.get(for: cacheKey) {
            return try JSONDecoder().decode(T.self, from: cachedData)
        }
        
        // Fetch from network
        let result: T = try await baseService.request(endpoint)
        
        // Cache the result
        if endpoint.method == .get,
           let data = try? JSONEncoder().encode(result) {
            await cache.set(data, for: cacheKey)
        }
        
        return result
    }
    
    func request(_ endpoint: Endpoint) async throws -> Data {
        let cacheKey = endpoint.path
        
        if endpoint.method == .get,
           let cachedData = await cache.get(for: cacheKey) {
            return cachedData
        }
        
        let data = try await baseService.request(endpoint)
        
        if endpoint.method == .get {
            await cache.set(data, for: cacheKey)
        }
        
        return data
    }
}

// MARK: - Usage Example

/*
// Create service
let networkService = DefaultNetworkService(baseURL: "https://api.example.com")

// Wrap with authentication
let tokenProvider = MyTokenProvider()
let authService = AuthenticatedNetworkService(
    baseService: networkService,
    tokenProvider: tokenProvider
)

// Add caching
let cachedService = CachedNetworkService(baseService: authService)

// Make request
let endpoint = Endpoint(path: "/users/123", method: .get)
let user: User = try await cachedService.request(endpoint)
*/
