package com.example.app.ui.user

import androidx.arch.core.executor.testing.InstantTaskExecutorRule
import com.example.app.data.repository.UserRepository
import com.example.app.model.User
import io.mockk.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.flowOf
import kotlinx.coroutines.test.*
import org.junit.jupiter.api.*
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.params.ParameterizedTest
import org.junit.jupiter.params.provider.CsvSource
import org.junit.jupiter.params.provider.ValueSource

/**
 * Test template for Kotlin with JUnit 5, MockK, and Coroutines
 */
@OptIn(ExperimentalCoroutinesApi::class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class UserViewModelTest {

    // Test dispatcher for coroutines
    private val testDispatcher = StandardTestDispatcher()

    // Mock repository
    private lateinit var mockRepository: UserRepository

    // System under test
    private lateinit var viewModel: UserViewModel

    @get:Rule
    val instantTaskExecutorRule = InstantTaskExecutorRule()

    @BeforeAll
    fun setupAll() {
        // Setup that runs once before all tests
        Dispatchers.setMain(testDispatcher)
    }

    @BeforeEach
    fun setup() {
        // Setup that runs before each test
        mockRepository = mockk(relaxed = false)
        viewModel = UserViewModel(mockRepository)
    }

    @AfterEach
    fun teardown() {
        // Cleanup after each test
        clearAllMocks()
    }

    @AfterAll
    fun teardownAll() {
        // Cleanup that runs once after all tests
        Dispatchers.resetMain()
    }

    // ========== Basic Tests ==========

    @Test
    fun `loadUsers updates state to Success with users`() = runTest {
        // Given
        val users = listOf(
            User("1", "Alice", "alice@example.com", true),
            User("2", "Bob", "bob@example.com", true)
        )
        coEvery { mockRepository.getUsers() } returns flowOf(users)

        // When
        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        val state = viewModel.uiState.value
        assertTrue(state is UiState.Success)
        assertEquals(users, (state as UiState.Success).users)
    }

    @Test
    fun `loadUsers updates state to Error on failure`() = runTest {
        // Given
        val errorMessage = "Network error"
        coEvery { mockRepository.getUsers() } returns flow {
            throw Exception(errorMessage)
        }

        // When
        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        val state = viewModel.uiState.value
        assertTrue(state is UiState.Error)
        assertEquals(errorMessage, (state as UiState.Error).message)
    }

    @Test
    fun `createUser emits UserCreated event on success`() = runTest {
        // Given
        val name = "Charlie"
        val email = "charlie@example.com"
        coEvery { mockRepository.saveUser(any()) } just Runs
        coEvery { mockRepository.getUsers() } returns flowOf(emptyList())

        // Collect events
        val events = mutableListOf<UserEvent>()
        val job = launch(UnconfinedTestDispatcher()) {
            viewModel.events.collect { events.add(it) }
        }

        // When
        viewModel.createUser(name, email)
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        assertTrue(events.any { it is UserEvent.UserCreated })
        val createdEvent = events.filterIsInstance<UserEvent.UserCreated>().first()
        assertEquals(name, createdEvent.user.name)
        assertEquals(email, createdEvent.user.email)

        job.cancel()
    }

    @Test
    fun `deleteUser calls repository and emits event`() = runTest {
        // Given
        val userId = "123"
        coEvery { mockRepository.deleteUser(userId) } just Runs
        coEvery { mockRepository.getUsers() } returns flowOf(emptyList())

        val events = mutableListOf<UserEvent>()
        val job = launch(UnconfinedTestDispatcher()) {
            viewModel.events.collect { events.add(it) }
        }

        // When
        viewModel.deleteUser(userId)
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        coVerify(exactly = 1) { mockRepository.deleteUser(userId) }
        assertTrue(events.any { it is UserEvent.UserDeleted })

        job.cancel()
    }

    // ========== Search Tests ==========

    @Test
    fun `updateSearchQuery filters users correctly`() = runTest {
        // Given
        val users = listOf(
            User("1", "Alice", "alice@example.com", true),
            User("2", "Bob", "bob@example.com", true),
            User("3", "Charlie", "charlie@example.com", true)
        )
        coEvery { mockRepository.getUsers() } returns flowOf(users)

        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // When
        viewModel.updateSearchQuery("alice")
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        val filteredUsers = viewModel.filteredUsers.value
        assertEquals(1, filteredUsers.size)
        assertEquals("Alice", filteredUsers[0].name)
    }

    @Test
    fun `search query is case insensitive`() = runTest {
        // Given
        val users = listOf(User("1", "Alice", "alice@example.com", true))
        coEvery { mockRepository.getUsers() } returns flowOf(users)

        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // When
        viewModel.updateSearchQuery("ALICE")
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        assertEquals(1, viewModel.filteredUsers.value.size)
    }

    // ========== Parameterized Tests ==========

    @ParameterizedTest
    @ValueSource(strings = ["alice@example.com", "bob@test.com", "user@domain.org"])
    fun `createUser accepts valid emails`(email: String) = runTest {
        // Given
        coEvery { mockRepository.saveUser(any()) } just Runs
        coEvery { mockRepository.getUsers() } returns flowOf(emptyList())

        // When
        viewModel.createUser("Test User", email)
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        coVerify { mockRepository.saveUser(match { it.email == email }) }
    }

    @ParameterizedTest
    @CsvSource(
        "Alice, 25, true",
        "Bob, 17, false",
        "Charlie, 18, true"
    )
    fun `user age validation`(name: String, age: Int, expectedValid: Boolean) {
        // Test business logic
        val isValid = age >= 18
        assertEquals(expectedValid, isValid)
    }

    // ========== Verification Tests ==========

    @Test
    fun `loadUsers is called exactly once on init`() = runTest {
        // Given
        coEvery { mockRepository.getUsers() } returns flowOf(emptyList())

        // When
        val newViewModel = UserViewModel(mockRepository)
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        coVerify(exactly = 1) { mockRepository.getUsers() }
    }

    @Test
    fun `updateUser verifies call order`() = runTest {
        // Given
        val userId = "123"
        val user = User(userId, "Alice", "alice@example.com", true)
        val users = listOf(user)

        coEvery { mockRepository.getUsers() } returns flowOf(users)
        coEvery { mockRepository.saveUser(any()) } just Runs

        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // When
        viewModel.updateUser(userId, "Alice Updated", "newemail@example.com")
        testDispatcher.scheduler.advanceUntilIdle()

        // Then - verify call order
        coVerifyOrder {
            mockRepository.saveUser(any())
            mockRepository.getUsers()
        }
    }

    @Test
    fun `toggleUserActiveStatus does not call deleteUser`() = runTest {
        // Given
        val user = User("1", "Alice", "alice@example.com", true)
        coEvery { mockRepository.getUsers() } returns flowOf(listOf(user))
        coEvery { mockRepository.saveUser(any()) } just Runs

        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // When
        viewModel.toggleUserActiveStatus("1")
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        coVerify(exactly = 0) { mockRepository.deleteUser(any()) }
    }

    // ========== Mock Slots ==========

    @Test
    fun `createUser passes correct user data to repository`() = runTest {
        // Given
        val slot = slot<User>()
        coEvery { mockRepository.saveUser(capture(slot)) } just Runs
        coEvery { mockRepository.getUsers() } returns flowOf(emptyList())

        // When
        viewModel.createUser("Alice", "alice@example.com")
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        val capturedUser = slot.captured
        assertEquals("Alice", capturedUser.name)
        assertEquals("alice@example.com", capturedUser.email)
        assertTrue(capturedUser.isActive)
        assertNotNull(capturedUser.id)
    }

    // ========== Exception Handling ==========

    @Test
    fun `repository exception is handled gracefully`() = runTest {
        // Given
        coEvery { mockRepository.getUsers() } throws RuntimeException("Database error")

        // When
        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // Then - should not crash, state should be Error
        val state = viewModel.uiState.value
        assertTrue(state is UiState.Error)
    }
}

/**
 * Extension for testing StateFlow
 */
suspend fun <T> kotlinx.coroutines.flow.StateFlow<T>.waitUntil(
    predicate: (T) -> Boolean
) = kotlinx.coroutines.withTimeout(1000) {
    this@waitUntil.first(predicate)
}
