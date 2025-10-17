import Foundation
import Combine

/// MVVM ViewModel Template with Modern Concurrency
/// Demonstrates async/await, @Published properties, and error handling
@MainActor
final class ExampleViewModel: ObservableObject {
    // MARK: - Published Properties

    @Published private(set) var items: [Item] = []
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?
    @Published var searchText = ""

    // MARK: - Private Properties

    private let repository: ItemRepository
    private var cancellables = Set<AnyCancellable>()

    // MARK: - Initialization

    init(repository: ItemRepository) {
        self.repository = repository
        setupSearchDebounce()
    }

    // MARK: - Public Methods

    func loadItems() async {
        isLoading = true
        error = nil

        do {
            items = try await repository.fetchItems()
        } catch {
            self.error = error
        }

        isLoading = false
    }

    func refreshItems() async {
        guard !isLoading else { return }
        await loadItems()
    }

    func addItem(_ item: Item) async {
        isLoading = true
        error = nil

        do {
            try await repository.saveItem(item)
            await loadItems()
        } catch {
            self.error = error
        }

        isLoading = false
    }

    func deleteItem(_ item: Item) async {
        guard let index = items.firstIndex(where: { $0.id == item.id }) else {
            return
        }

        items.remove(at: index)

        do {
            try await repository.deleteItem(item)
        } catch {
            // Revert on error
            items.insert(item, at: index)
            self.error = error
        }
    }

    // MARK: - Private Methods

    private func setupSearchDebounce() {
        $searchText
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .removeDuplicates()
            .sink { [weak self] query in
                Task {
                    await self?.performSearch(query: query)
                }
            }
            .store(in: &cancellables)
    }

    private func performSearch(query: String) async {
        guard !query.isEmpty else {
            await loadItems()
            return
        }

        isLoading = true
        error = nil

        do {
            items = try await repository.searchItems(query: query)
        } catch {
            self.error = error
        }

        isLoading = false
    }
}

// MARK: - Supporting Types

struct Item: Identifiable, Codable {
    let id: UUID
    var name: String
    var description: String
    let createdAt: Date
}

protocol ItemRepository {
    func fetchItems() async throws -> [Item]
    func saveItem(_ item: Item) async throws
    func deleteItem(_ item: Item) async throws
    func searchItems(query: String) async throws -> [Item]
}
