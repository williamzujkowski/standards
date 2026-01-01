# Kotlin Coding Standards - Complete Reference

This document contains detailed examples and advanced patterns for the Kotlin coding standards skill.

## Table of Contents

1. [Advanced Coroutines](#advanced-coroutines)
2. [Complete Flow Patterns](#complete-flow-patterns)
3. [Advanced Delegation](#advanced-delegation)
4. [Comprehensive Testing](#comprehensive-testing)
5. [Static Analysis Configuration](#static-analysis-configuration)
6. [Spring Boot Integration](#spring-boot-integration)

---

## Advanced Coroutines

### StateFlow and SharedFlow

```kotlin
class UserViewModel : ViewModel() {
    // StateFlow - Always has value, replays last
    private val _uiState = MutableStateFlow<UiState>(UiState.Loading)
    val uiState: StateFlow<UiState> = _uiState.asStateFlow()

    // SharedFlow - Events without initial value
    private val _events = MutableSharedFlow<UserEvent>()
    val events: SharedFlow<UserEvent> = _events.asSharedFlow()

    fun loadUsers() {
        viewModelScope.launch {
            _uiState.value = UiState.Loading

            try {
                val users = repository.getUsers()
                _uiState.value = UiState.Success(users)
            } catch (e: Exception) {
                _uiState.value = UiState.Error(e.message ?: "Unknown error")
                _events.emit(UserEvent.ShowError(e.message))
            }
        }
    }
}
```

### Structured Concurrency

```kotlin
class UserService {
    private val scope = CoroutineScope(SupervisorJob() + Dispatchers.Default)

    fun startPeriodicSync() {
        scope.launch {
            while (isActive) {
                try {
                    syncUsers()
                    delay(30_000) // 30 seconds
                } catch (e: CancellationException) {
                    throw e  // Re-throw cancellation
                } catch (e: Exception) {
                    Log.e("UserService", "Sync failed", e)
                }
            }
        }
    }

    fun cleanup() {
        scope.cancel()
    }
}
```

### Combining Multiple Flows

```kotlin
fun getUsersWithStatus(
    usersFlow: Flow<List<User>>,
    statusFlow: Flow<NetworkStatus>
): Flow<Pair<List<User>, NetworkStatus>> {
    return combine(usersFlow, statusFlow) { users, status ->
        Pair(users, status)
    }
}

// Zip - pairs elements one-to-one
fun pairFlows(): Flow<Pair<Int, String>> {
    val numbers = flowOf(1, 2, 3)
    val letters = flowOf("A", "B", "C")
    return numbers.zip(letters) { num, letter -> Pair(num, letter) }
}
```

---

## Complete Flow Patterns

### Cold Flow Creation

```kotlin
class UserRepository(private val database: UserDao) {
    // Cold flow - Emits on collection
    fun getUsers(): Flow<List<User>> {
        return database.getUsersFlow()
    }

    // Transform flows
    fun getActiveUsers(): Flow<List<User>> {
        return database.getUsersFlow()
            .map { users -> users.filter { it.isActive } }
            .distinctUntilChanged()
    }

    // Flow builder
    fun fetchUsersWithProgress(): Flow<FetchState> = flow {
        emit(FetchState.Loading)
        try {
            val users = apiService.getUsers()
            emit(FetchState.Success(users))
        } catch (e: Exception) {
            emit(FetchState.Error(e.message))
        }
    }
}
```

### Flow Operators

```kotlin
// Debounce for search
fun searchUsers(query: Flow<String>): Flow<List<User>> {
    return query
        .debounce(300)
        .distinctUntilChanged()
        .flatMapLatest { searchQuery ->
            if (searchQuery.isEmpty()) {
                flowOf(emptyList())
            } else {
                repository.searchUsers(searchQuery)
            }
        }
}

// Retry with exponential backoff
fun fetchWithRetry(): Flow<Result<Data>> = flow {
    emit(apiService.fetchData())
}.retryWhen { cause, attempt ->
    if (cause is IOException && attempt < 3) {
        delay((2.0.pow(attempt.toDouble()) * 1000).toLong())
        true
    } else {
        false
    }
}
```

---

## Advanced Delegation

### Observable Properties

```kotlin
class User {
    var name: String by Delegates.observable("Unknown") { prop, old, new ->
        println("Name changed from $old to $new")
    }

    var email: String by Delegates.vetoable("") { _, _, newValue ->
        newValue.contains("@")  // Veto if invalid
    }
}
```

### SharedPreferences Delegate

```kotlin
class Preferences(private val prefs: SharedPreferences) {
    var username: String by StringPreference(prefs, "username", "")
    var userId: Int by IntPreference(prefs, "user_id", -1)
    var isLoggedIn: Boolean by BooleanPreference(prefs, "logged_in", false)
}

class StringPreference(
    private val prefs: SharedPreferences,
    private val key: String,
    private val default: String
) : ReadWriteProperty<Any?, String> {
    override fun getValue(thisRef: Any?, property: KProperty<*>): String {
        return prefs.getString(key, default) ?: default
    }

    override fun setValue(thisRef: Any?, property: KProperty<*>, value: String) {
        prefs.edit().putString(key, value).apply()
    }
}

class IntPreference(
    private val prefs: SharedPreferences,
    private val key: String,
    private val default: Int
) : ReadWriteProperty<Any?, Int> {
    override fun getValue(thisRef: Any?, property: KProperty<*>): Int {
        return prefs.getInt(key, default)
    }

    override fun setValue(thisRef: Any?, property: KProperty<*>, value: Int) {
        prefs.edit().putInt(key, value).apply()
    }
}

class BooleanPreference(
    private val prefs: SharedPreferences,
    private val key: String,
    private val default: Boolean
) : ReadWriteProperty<Any?, Boolean> {
    override fun getValue(thisRef: Any?, property: KProperty<*>): Boolean {
        return prefs.getBoolean(key, default)
    }

    override fun setValue(thisRef: Any?, property: KProperty<*>, value: Boolean) {
        prefs.edit().putBoolean(key, value).apply()
    }
}
```

### Multiple Interface Delegation

```kotlin
interface Cache {
    fun get(key: String): Any?
    fun put(key: String, value: Any)
}

interface ApiService {
    suspend fun getUser(id: String): User
}

class CachedRepository(
    private val cache: Cache,
    private val api: ApiService
) : Cache by cache, ApiService by api {
    suspend fun getUserCached(id: String): User {
        return get(id) as? User ?: run {
            val user = getUser(id)
            put(id, user)
            user
        }
    }
}
```

---

## Comprehensive Testing

### Basic Test Structure with JUnit 5 and MockK

```kotlin
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class UserRepositoryTest {
    private lateinit var repository: UserRepository
    private lateinit var mockApi: ApiService
    private lateinit var mockDatabase: UserDao

    @BeforeEach
    fun setup() {
        mockApi = mockk()
        mockDatabase = mockk()
        repository = UserRepository(mockApi, mockDatabase)
    }

    @AfterEach
    fun teardown() {
        clearAllMocks()
    }

    @Test
    fun `getUser returns user from API`() = runTest {
        // Given
        val userId = "123"
        val expectedUser = User(userId, "Alice")
        coEvery { mockApi.getUser(userId) } returns expectedUser

        // When
        val result = repository.getUser(userId)

        // Then
        assertEquals(expectedUser, result)
        coVerify(exactly = 1) { mockApi.getUser(userId) }
    }

    @Test
    fun `getUser throws exception when API fails`() = runTest {
        // Given
        val userId = "123"
        coEvery { mockApi.getUser(userId) } throws IOException("Network error")

        // When/Then
        assertThrows<IOException> {
            repository.getUser(userId)
        }
    }
}
```

### Testing Coroutines with TestDispatcher

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {
    private lateinit var viewModel: UserViewModel
    private lateinit var mockRepository: UserRepository
    private val testDispatcher = StandardTestDispatcher()

    @BeforeEach
    fun setup() {
        Dispatchers.setMain(testDispatcher)
        mockRepository = mockk()
        viewModel = UserViewModel(mockRepository)
    }

    @AfterEach
    fun teardown() {
        Dispatchers.resetMain()
    }

    @Test
    fun `loadUsers updates state to Success`() = runTest {
        // Given
        val users = listOf(User("1", "Alice"))
        coEvery { mockRepository.getUsers() } returns users

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
        coEvery { mockRepository.getUsers() } throws Exception("API Error")

        // When
        viewModel.loadUsers()
        testDispatcher.scheduler.advanceUntilIdle()

        // Then
        val state = viewModel.uiState.value
        assertTrue(state is UiState.Error)
        assertEquals("API Error", (state as UiState.Error).message)
    }
}
```

### Testing Flows with Turbine

```kotlin
class UserRepositoryTest {
    @Test
    fun `getUsers flow emits users`() = runTest {
        // Given
        val users = listOf(User("1", "Alice"))
        val flow = flow { emit(users) }
        every { mockDatabase.getUsersFlow() } returns flow

        // When/Then
        repository.getUsers().test {
            assertEquals(users, awaitItem())
            awaitComplete()
        }
    }

    @Test
    fun `getActiveUsers filters inactive users`() = runTest {
        // Given
        val users = listOf(
            User("1", "Alice", isActive = true),
            User("2", "Bob", isActive = false)
        )
        every { mockDatabase.getUsersFlow() } returns flowOf(users)

        // When/Then
        repository.getActiveUsers().test {
            val result = awaitItem()
            assertEquals(1, result.size)
            assertEquals("Alice", result[0].name)
            awaitComplete()
        }
    }

    @Test
    fun `flow emits loading then success`() = runTest {
        // Given
        val users = listOf(User("1", "Alice"))
        coEvery { mockApi.getUsers() } returns users

        // When/Then
        repository.fetchUsersWithProgress().test {
            assertEquals(FetchState.Loading, awaitItem())
            assertEquals(FetchState.Success(users), awaitItem())
            awaitComplete()
        }
    }
}
```

### Parameterized Tests

```kotlin
class ValidationTest {
    @ParameterizedTest
    @ValueSource(strings = ["test@example.com", "user@domain.co.uk", "a@b.io"])
    fun `valid emails pass validation`(email: String) {
        assertTrue(email.isValidEmail())
    }

    @ParameterizedTest
    @ValueSource(strings = ["invalid", "@example.com", "test@", ""])
    fun `invalid emails fail validation`(email: String) {
        assertFalse(email.isValidEmail())
    }

    @ParameterizedTest
    @CsvSource(
        "Alice, 25, true",
        "Bob, 17, false",
        "Charlie, 18, true",
        "Diana, 0, false"
    )
    fun `age validation returns expected result`(name: String, age: Int, expected: Boolean) {
        val user = User(name, age)
        assertEquals(expected, user.isAdult())
    }

    @ParameterizedTest
    @MethodSource("provideUserData")
    fun `user creation with various inputs`(data: UserData) {
        val user = User(data.name, data.email)
        assertNotNull(user.id)
        assertEquals(data.name, user.name)
    }

    companion object {
        @JvmStatic
        fun provideUserData() = listOf(
            UserData("Alice", "alice@example.com"),
            UserData("Bob", "bob@example.com"),
            UserData("Charlie", "charlie@test.org")
        )
    }
}

data class UserData(val name: String, val email: String)
```

### Mock Verification Patterns

```kotlin
@Test
fun `service calls repository with correct parameters`() = runTest {
    // Relaxed mock returns default values
    val mockRepo = mockk<UserRepository>(relaxed = true)
    val service = UserService(mockRepo)

    // When
    service.updateUser("123", "Alice")

    // Verify call order
    coVerifyOrder {
        mockRepo.getUser("123")
        mockRepo.saveUser(any())
    }

    // Verify called at least once
    coVerify(atLeast = 1) { mockRepo.getUser("123") }

    // Verify not called
    coVerify(exactly = 0) { mockRepo.deleteUser(any()) }

    // Capture arguments
    val slot = slot<User>()
    coVerify { mockRepo.saveUser(capture(slot)) }
    assertEquals("Alice", slot.captured.name)
}

@Test
fun `verify all interactions`() = runTest {
    val mockRepo = mockk<UserRepository>()
    coEvery { mockRepo.getUser(any()) } returns User("1", "Test")

    // When
    service.processUser("123")

    // Verify all expected calls happened
    coVerifyAll {
        mockRepo.getUser("123")
    }

    // Confirm no unverified calls
    confirmVerified(mockRepo)
}
```

---

## Static Analysis Configuration

### Detekt Configuration (detekt.yml)

```yaml
build:
  maxIssues: 0
  weights:
    complexity: 2
    formatting: 1
    style: 1

complexity:
  ComplexCondition:
    active: true
    threshold: 4
  ComplexMethod:
    active: true
    threshold: 15
  LongMethod:
    active: true
    threshold: 60
  LongParameterList:
    active: true
    functionThreshold: 6
    constructorThreshold: 7
  NestedBlockDepth:
    active: true
    threshold: 4
  TooManyFunctions:
    active: true
    thresholdInFiles: 11
    thresholdInClasses: 11
    thresholdInInterfaces: 11

naming:
  ClassNaming:
    active: true
    classPattern: '[A-Z][a-zA-Z0-9]*'
  FunctionNaming:
    active: true
    functionPattern: '[a-z][a-zA-Z0-9]*'
    ignoreAnnotated: ['Composable']
  VariableNaming:
    active: true
    variablePattern: '[a-z][a-zA-Z0-9]*'

style:
  ForbiddenComment:
    active: true
    values: ['TODO:', 'FIXME:', 'STOPSHIP:']
  MagicNumber:
    active: true
    ignoreNumbers: ['-1', '0', '1', '2']
    ignoreAnnotation: true
  MaxLineLength:
    active: true
    maxLineLength: 120
  WildcardImport:
    active: true

coroutines:
  GlobalCoroutineUsage:
    active: true
  RedundantSuspendModifier:
    active: true
  SuspendFunWithFlowReturnType:
    active: true

exceptions:
  SwallowedException:
    active: true
  TooGenericExceptionCaught:
    active: true
  TooGenericExceptionThrown:
    active: true
```

### ktlint Integration (build.gradle.kts)

```kotlin
plugins {
    id("org.jlleitschuh.gradle.ktlint") version "11.6.1"
}

ktlint {
    version.set("1.0.1")
    android.set(true)
    outputToConsole.set(true)
    outputColorName.set("RED")
    ignoreFailures.set(false)
    enableExperimentalRules.set(true)
    filter {
        exclude("**/generated/**")
        include("**/kotlin/**")
    }
}

tasks.register("ktlintFormat", JavaExec::class) {
    group = "verification"
    description = "Fix Kotlin code style violations"
    classpath = configurations.ktlint.get()
    mainClass.set("com.pinterest.ktlint.Main")
    args = listOf("-F", "src/**/*.kt")
}
```

### Custom Lint Rule Example

```kotlin
class NotNullAssertionDetector : Detector(), SourceCodeScanner {
    companion object {
        val ISSUE = Issue.create(
            id = "NotNullAssertion",
            briefDescription = "Avoid using !! operator",
            explanation = "The not-null assertion (!!) can cause NullPointerException. " +
                "Use safe call (?.) or elvis operator (?:) instead.",
            category = Category.CORRECTNESS,
            priority = 6,
            severity = Severity.WARNING,
            implementation = Implementation(
                NotNullAssertionDetector::class.java,
                Scope.JAVA_FILE_SCOPE
            )
        )
    }

    override fun getApplicableUastTypes() = listOf(UPostfixExpression::class.java)

    override fun createUastHandler(context: JavaContext): UElementHandler {
        return object : UElementHandler() {
            override fun visitPostfixExpression(node: UPostfixExpression) {
                if (node.operator.text == "!!") {
                    context.report(
                        ISSUE,
                        node,
                        context.getLocation(node),
                        "Avoid using !! operator. Use safe call (?.) or elvis (?:) instead."
                    )
                }
            }
        }
    }
}
```

---

## Spring Boot Integration

### Repository Pattern

```kotlin
@Repository
class UserRepository(private val jdbcTemplate: JdbcTemplate) {

    fun findById(id: String): User? {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE id = ?",
            UserRowMapper(),
            id
        )
    }

    fun findAll(): List<User> {
        return jdbcTemplate.query("SELECT * FROM users", UserRowMapper())
    }

    fun save(user: User): User {
        jdbcTemplate.update(
            "INSERT INTO users (id, name, email) VALUES (?, ?, ?) " +
                "ON CONFLICT (id) DO UPDATE SET name = ?, email = ?",
            user.id, user.name, user.email, user.name, user.email
        )
        return user
    }
}

class UserRowMapper : RowMapper<User> {
    override fun mapRow(rs: ResultSet, rowNum: Int): User {
        return User(
            id = rs.getString("id"),
            name = rs.getString("name"),
            email = rs.getString("email")
        )
    }
}
```

### REST Controller with Coroutines

```kotlin
@RestController
@RequestMapping("/api/users")
class UserController(private val userService: UserService) {

    @GetMapping
    suspend fun getAllUsers(): ResponseEntity<List<User>> {
        return ResponseEntity.ok(userService.getAll())
    }

    @GetMapping("/{id}")
    suspend fun getUser(@PathVariable id: String): ResponseEntity<User> {
        return userService.findById(id)
            ?.let { ResponseEntity.ok(it) }
            ?: ResponseEntity.notFound().build()
    }

    @PostMapping
    suspend fun createUser(@RequestBody @Valid user: CreateUserRequest): ResponseEntity<User> {
        val created = userService.create(user)
        return ResponseEntity.created(URI("/api/users/${created.id}")).body(created)
    }

    @PutMapping("/{id}")
    suspend fun updateUser(
        @PathVariable id: String,
        @RequestBody @Valid user: UpdateUserRequest
    ): ResponseEntity<User> {
        return userService.update(id, user)
            ?.let { ResponseEntity.ok(it) }
            ?: ResponseEntity.notFound().build()
    }

    @DeleteMapping("/{id}")
    suspend fun deleteUser(@PathVariable id: String): ResponseEntity<Unit> {
        userService.delete(id)
        return ResponseEntity.noContent().build()
    }

    @ExceptionHandler(ValidationException::class)
    fun handleValidation(e: ValidationException): ResponseEntity<ErrorResponse> {
        return ResponseEntity.badRequest().body(ErrorResponse(e.message ?: "Validation failed"))
    }
}

data class CreateUserRequest(
    @field:NotBlank val name: String,
    @field:Email val email: String
)

data class UpdateUserRequest(
    @field:NotBlank val name: String?,
    @field:Email val email: String?
)

data class ErrorResponse(val message: String)
```

### WebFlux with Flow Integration

```kotlin
@Configuration
class RouterConfiguration {
    @Bean
    fun userRoutes(handler: UserHandler) = coRouter {
        "/api/users".nest {
            GET("", handler::getAll)
            GET("/{id}", handler::getById)
            POST("", handler::create)
            PUT("/{id}", handler::update)
            DELETE("/{id}", handler::delete)
        }
    }
}

@Component
class UserHandler(private val repository: UserRepository) {

    suspend fun getAll(request: ServerRequest): ServerResponse {
        return repository.findAll()
            .let { ServerResponse.ok().bodyValueAndAwait(it) }
    }

    suspend fun getById(request: ServerRequest): ServerResponse {
        val id = request.pathVariable("id")
        return repository.findById(id)
            ?.let { ServerResponse.ok().bodyValueAndAwait(it) }
            ?: ServerResponse.notFound().buildAndAwait()
    }

    suspend fun create(request: ServerRequest): ServerResponse {
        val user = request.awaitBody<User>()
        val saved = repository.save(user)
        return ServerResponse.created(URI("/api/users/${saved.id}"))
            .bodyValueAndAwait(saved)
    }

    suspend fun update(request: ServerRequest): ServerResponse {
        val id = request.pathVariable("id")
        val update = request.awaitBody<User>()
        return repository.update(id, update)
            ?.let { ServerResponse.ok().bodyValueAndAwait(it) }
            ?: ServerResponse.notFound().buildAndAwait()
    }

    suspend fun delete(request: ServerRequest): ServerResponse {
        val id = request.pathVariable("id")
        repository.delete(id)
        return ServerResponse.noContent().buildAndAwait()
    }
}
```

---

## Related Resources

- [Kotlin Language Reference](https://kotlinlang.org/docs/reference/)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [Kotlin Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin for Java Developers](https://kotlinlang.org/docs/java-to-kotlin-interop.html)
- [Detekt Documentation](https://detekt.dev/)
- [ktlint Documentation](https://ktlint.github.io/)
- [MockK Documentation](https://mockk.io/)
- [Turbine Flow Testing](https://github.com/cashapp/turbine)

### Books

- **"Kotlin in Action"** by Dmitry Jemerov & Svetlana Isakova
- **"Effective Kotlin"** by Marcin Moskała
- **"Kotlin Coroutines"** by Marcin Moskała

---

*Last updated: 2025-01-01*
