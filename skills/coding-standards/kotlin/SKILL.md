---
name: kotlin-coding-standards
category: coding-standards
difficulty: intermediate
estimated_time: 45 minutes
tags: [kotlin, android, jvm, coroutines, null-safety]
description: Master Kotlin coding standards with null safety, coroutines, and idiomatic patterns
learning_objectives:
  - Apply Kotlin null safety and smart cast patterns
  - Implement coroutines for asynchronous programming
  - Use functional programming with collections and sequences
  - Write idiomatic Kotlin with delegation and extensions
  - Integrate static analysis with detekt and ktlint
prerequisites:
  - Basic JVM knowledge
  - Understanding of object-oriented programming
related_skills:
  - java-coding-standards
  - android-development
  - testing-standards
---

# Kotlin Coding Standards

## Level 1: Quick Reference

### Null Safety Cheat Sheet

**Safe Call Operator (?.)** - Returns null if receiver is null:

```kotlin
val length = user?.name?.length  // null if user or name is null
```

**Elvis Operator (?:)** - Provides default value:

```kotlin
val name = user?.name ?: "Unknown"
```

**Not-Null Assertion (!!)** - Throws NPE if null (use sparingly):

```kotlin
val length = user!!.name!!.length  // Throws if null
```

**Safe Cast (as?)** - Returns null on cast failure:

```kotlin
val employee = person as? Employee  // null if not Employee
```

**Scope Functions**:

- `let` - Execute lambda if not null, transform value
- `apply` - Configure object, return receiver
- `also` - Side effects, return receiver
- `run` - Execute lambda, return result
- `with` - Group calls, return result

```kotlin
user?.let { u ->
    println("Name: ${u.name}")
}

val user = User().apply {
    name = "Alice"
    email = "alice@example.com"
}
```

### Common Kotlin Patterns

**Data Classes** - Auto-generate equals, hashCode, toString, copy:

```kotlin
data class User(
    val id: String,
    val name: String,
    val email: String
)
```

**Sealed Classes** - Restricted class hierarchies:

```kotlin
sealed class Result<out T> {
    data class Success<T>(val data: T) : Result<T>()
    data class Error(val message: String) : Result<Nothing>()
    object Loading : Result<Nothing>()
}

when (result) {
    is Result.Success -> println(result.data)
    is Result.Error -> println(result.message)
    Result.Loading -> println("Loading...")
}
```

**Extension Functions** - Add methods to existing classes:

```kotlin
fun String.isValidEmail(): Boolean {
    return android.util.Patterns.EMAIL_ADDRESS.matcher(this).matches()
}
```

### Essential Checklist

- [ ] Configure detekt for static analysis
- [ ] Set up ktlint for code formatting
- [ ] Use nullable types (?) instead of !! operator
- [ ] Prefer immutable (val) over mutable (var)
- [ ] Use data classes for DTOs
- [ ] Implement sealed classes for state management
- [ ] Use extension functions for utility methods
- [ ] Apply scope functions appropriately
- [ ] Use trailing lambdas for readability
- [ ] Avoid platform types from Java interop

---

## Level 2: Implementation Guide

### 1. Null Safety and Smart Casts

**Nullable Types Declaration**:

```kotlin
// Explicit nullable types
var name: String? = null
val age: Int? = getAge()

// Non-null types (default)
val id: String = "123"
val count: Int = 0
```

**Smart Casts** - Compiler tracks null checks:

```kotlin
fun processUser(user: User?) {
    if (user != null) {
        // Smart cast to User
        println(user.name)
        user.updateProfile()
    }
}

// Smart cast with return
fun getUserName(user: User?): String {
    user ?: return "Unknown"
    // Smart cast after null check
    return user.name
}
```

**lateinit for Late Initialization** (non-nullable):

```kotlin
class MyActivity : Activity() {
    // Will be initialized in onCreate
    private lateinit var binding: ActivityMainBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)

        // Check initialization
        if (::binding.isInitialized) {
            setContentView(binding.root)
        }
    }
}
```

**Lazy Initialization** (thread-safe by default):

```kotlin
class DataRepository {
    // Initialized on first access
    private val database: AppDatabase by lazy {
        Room.databaseBuilder(
            context,
            AppDatabase::class.java,
            "app-db"
        ).build()
    }

    fun getUsers() = database.userDao().getAll()
}
```

### 2. Coroutines for Asynchronous Programming

**Suspend Functions** - Async operations without blocking:

```kotlin
suspend fun fetchUser(id: String): User {
    return withContext(Dispatchers.IO) {
        apiService.getUser(id)
    }
}

suspend fun saveUser(user: User) {
    withContext(Dispatchers.IO) {
        database.userDao().insert(user)
    }
}
```

**Coroutine Builders**:

```kotlin
class UserRepository(
    private val apiService: ApiService,
    private val database: UserDao
) {
    // launch - Fire and forget
    fun refreshUsers() {
        CoroutineScope(Dispatchers.IO).launch {
            val users = apiService.getUsers()
            database.insertAll(users)
        }
    }

    // async - Return deferred result
    suspend fun getUserWithDetails(id: String): UserDetails {
        return coroutineScope {
            val userDeferred = async { apiService.getUser(id) }
            val postsDeferred = async { apiService.getUserPosts(id) }

            UserDetails(
                user = userDeferred.await(),
                posts = postsDeferred.await()
            )
        }
    }
}
```

**Flow for Reactive Streams**:

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

    // Combine flows
    fun getUsersWithStatus(
        usersFlow: Flow<List<User>>,
        statusFlow: Flow<NetworkStatus>
    ): Flow<Pair<List<User>, NetworkStatus>> {
        return combine(usersFlow, statusFlow) { users, status ->
            Pair(users, status)
        }
    }
}
```

**StateFlow and SharedFlow** - Hot flows for state management:

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

**Structured Concurrency** - Automatic cancellation:

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
                    throw e
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

### 3. Collections and Functional Programming

**Sequences for Large Collections** (lazy evaluation):

```kotlin
// List operations are eager (immediate)
val result = users
    .filter { it.isActive }
    .map { it.name.uppercase() }
    .take(10)

// Sequence operations are lazy (on-demand)
val result = users.asSequence()
    .filter { it.isActive }
    .map { it.name.uppercase() }
    .take(10)
    .toList()  // Terminal operation
```

**Common Collection Operations**:

```kotlin
// Transformation
val names = users.map { it.name }
val pairs = users.flatMap { user -> user.emails.map { user to it } }

// Filtering
val active = users.filter { it.isActive }
val (admins, regular) = users.partition { it.isAdmin }

// Aggregation
val count = users.count { it.isActive }
val total = orders.sumOf { it.amount }
val avgAge = users.map { it.age }.average()

// Grouping
val byRole = users.groupBy { it.role }
val byDept = users.associateBy { it.department }

// Searching
val admin = users.find { it.isAdmin }
val exists = users.any { it.email == target }
val allActive = users.all { it.isActive }
```

**Custom Collection Extensions**:

```kotlin
// Extension for chunked processing
fun <T> List<T>.chunkedProcess(
    chunkSize: Int,
    process: (List<T>) -> Unit
) {
    chunked(chunkSize).forEach { chunk ->
        process(chunk)
    }
}

// Extension for safe indexing
fun <T> List<T>.getOrNull(index: Int): T? {
    return if (index in indices) this[index] else null
}

// Extension for transforming with index
fun <T, R> List<T>.mapIndexedNotNull(
    transform: (index: Int, T) -> R?
): List<R> {
    return mapIndexedNotNull(transform)
}
```

### 4. Delegation Patterns

**Property Delegation** - Reusable property logic:

```kotlin
// Lazy initialization
class DataManager {
    val cache: Map<String, Data> by lazy {
        loadCacheFromDisk()
    }
}

// Observable properties
class User {
    var name: String by Delegates.observable("Unknown") { prop, old, new ->
        println("Name changed from $old to $new")
    }

    var email: String by Delegates.vetoable("") { _, _, newValue ->
        newValue.contains("@")  // Veto if invalid
    }
}

// Custom delegates
class Preferences(private val prefs: SharedPreferences) {
    var username: String by StringPreference(prefs, "username", "")
    var userId: Int by IntPreference(prefs, "user_id", -1)
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
```

**Class Delegation** - Composition over inheritance:

```kotlin
interface Logger {
    fun log(message: String)
}

class ConsoleLogger : Logger {
    override fun log(message: String) {
        println("[LOG] $message")
    }
}

// Delegate Logger implementation
class UserService(logger: Logger) : Logger by logger {
    fun createUser(name: String) {
        log("Creating user: $name")
        // Create user logic
    }
}

// Multiple delegation
class CachedRepository(
    private val cache: Cache,
    private val api: ApiService
) : Cache by cache, ApiService by api {
    suspend fun getUserCached(id: String): User {
        return get(id) ?: run {
            val user = getUser(id)
            put(id, user)
            user
        }
    }
}
```

### 5. Java Interoperability

**Platform Types** - Avoid when possible:

```kotlin
// Java method returns String (platform type String!)
val name = javaObject.getName()  // Type is String!

// Make nullability explicit
val safeName: String = javaObject.getName() ?: "Unknown"
val nullableName: String? = javaObject.getName()
```

**Annotations for Java Compatibility**:

```kotlin
// JvmStatic for static methods
class StringUtils {
    companion object {
        @JvmStatic
        fun isBlank(value: String?): Boolean {
            return value.isNullOrBlank()
        }
    }
}
// Java: StringUtils.isBlank(str)

// JvmOverloads for default parameters
class User @JvmOverloads constructor(
    val name: String,
    val email: String = "",
    val age: Int = 0
)
// Java: new User("Alice"), new User("Bob", "bob@mail.com")

// JvmField for public fields
class Config {
    @JvmField
    val timeout = 30
}
// Java: config.timeout (not getTimeout())

// JvmName for method name conflicts
@file:JvmName("StringExtensions")
package com.example.utils

fun String.toSnakeCase(): String { /* ... */ }
// Java: StringExtensions.toSnakeCase(str)
```

**Handling Java Exceptions**:

```kotlin
// Checked exceptions require @Throws
@Throws(IOException::class)
fun readFile(path: String): String {
    return File(path).readText()
}

// Or use runCatching for Kotlin callers
fun readFileSafe(path: String): Result<String> {
    return runCatching {
        File(path).readText()
    }
}
```

### 6. Testing with JUnit 5 and MockK

**Basic Test Structure**:

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
}
```

**Testing Coroutines**:

```kotlin
@OptIn(ExperimentalCoroutinesApi::class)
class UserViewModelTest {
    private lateinit var viewModel: UserViewModel
    private lateinit var mockRepository: UserRepository

    // Test dispatcher for coroutines
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
}
```

**Testing Flows**:

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
}
```

**Parameterized Tests**:

```kotlin
class ValidationTest {
    @ParameterizedTest
    @ValueSource(strings = ["test@example.com", "user@domain.co.uk"])
    fun `valid emails pass validation`(email: String) {
        assertTrue(email.isValidEmail())
    }

    @ParameterizedTest
    @CsvSource(
        "Alice, 25, true",
        "Bob, 17, false",
        "Charlie, 18, true"
    )
    fun `age validation`(name: String, age: Int, expected: Boolean) {
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
            UserData("Bob", "bob@example.com")
        )
    }
}
```

**Mock Verification and Relaxed Mocks**:

```kotlin
@Test
fun `service calls repository with correct parameters`() {
    // Relaxed mock returns default values
    val mockRepo = mockk<UserRepository>(relaxed = true)
    val service = UserService(mockRepo)

    // When
    runBlocking {
        service.updateUser("123", "Alice")
    }

    // Verify call order
    coVerifyOrder {
        mockRepo.getUser("123")
        mockRepo.saveUser(any())
    }

    // Verify called at least once
    coVerify(atLeast = 1) { mockRepo.getUser("123") }

    // Verify not called
    coVerify(exactly = 0) { mockRepo.deleteUser(any()) }
}
```

### 7. Static Analysis and Code Quality

**Detekt Configuration** - See `config/detekt.yml`:

- Complexity limits (cyclomatic, cognitive)
- Naming conventions (classes, functions, variables)
- Code smells (long methods, large classes)
- Kotlin-specific rules (extension functions, coroutines)

**ktlint Integration**:

```kotlin
// Apply formatting rules
tasks.register("ktlintFormat", JavaExec::class) {
    group = "verification"
    description = "Fix Kotlin code style violations"
    classpath = configurations.ktlint
    main = "com.pinterest.ktlint.Main"
    args = listOf("-F", "src/**/*.kt")
}
```

**Custom Lint Rules**:

```kotlin
// Example: Detect usage of !! operator
class NotNullAssertionDetector : Detector(), SourceCodeScanner {
    override fun getApplicableUastTypes() = listOf(UCallExpression::class.java)

    override fun createUastHandler(context: JavaContext): UElementHandler {
        return object : UElementHandler() {
            override fun visitCallExpression(node: UCallExpression) {
                if (node.methodName == "not null assertion") {
                    context.report(
                        ISSUE,
                        node,
                        context.getLocation(node),
                        "Avoid using !! operator, use safe call or elvis instead"
                    )
                }
            }
        }
    }
}
```

---

## Level 3: Deep Dive Resources

### Official Documentation

- [Kotlin Language Reference](https://kotlinlang.org/docs/reference/)
- [Kotlin Coroutines Guide](https://kotlinlang.org/docs/coroutines-guide.html)
- [Kotlin Style Guide](https://kotlinlang.org/docs/coding-conventions.html)
- [Kotlin for Java Developers](https://kotlinlang.org/docs/java-to-kotlin-interop.html)

### Books

- **"Kotlin in Action"** by Dmitry Jemerov & Svetlana Isakova
- **"Effective Kotlin"** by Marcin Moskała
- **"Kotlin Coroutines"** by Marcin Moskała

### Tools

- [Detekt](https://detekt.dev/) - Static code analysis
- [ktlint](https://ktlint.github.io/) - Code formatter
- [MockK](https://mockk.io/) - Mocking library
- [Turbine](https://github.com/cashapp/turbine) - Flow testing

### Community

- [Kotlin Slack](https://kotlinlang.slack.com/)
- [r/Kotlin](https://www.reddit.com/r/Kotlin/)
- [Kotlin Blog](https://blog.jetbrains.com/kotlin/)

### Related Skills

- `android-development` - Android app development
- `java-coding-standards` - Java interop patterns
- `testing-standards` - Comprehensive testing guide

---

## Bundled Resources

1. **config/detekt.yml** - Detekt static analysis configuration
2. **templates/ViewModel.kt** - Android ViewModel with coroutines
3. **templates/Repository.kt** - Repository pattern with Flow
4. **templates/sealed-class.kt** - Sealed class for state management
5. **templates/test-template.kt** - JUnit 5 + MockK test template
6. **scripts/setup-kotlin-project.sh** - Gradle Kotlin project setup

## Examples

### Basic Usage

```python
// TODO: Add basic example for kotlin
// This example demonstrates core functionality
```

### Advanced Usage

```python
// TODO: Add advanced example for kotlin
// This example shows production-ready patterns
```

### Integration Example

```python
// TODO: Add integration example showing how kotlin
// works with other systems and services
```

See `examples/kotlin/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring kotlin functionality
- **CI/CD Pipelines**: Automated testing and deployment workflows
- **Monitoring Systems**: Observability and logging platforms

### Related Skills

- See other skills in this category

### Common Integration Patterns

1. **Development Workflow**: How this skill fits into daily development
2. **Production Deployment**: Integration with production systems
3. **Monitoring & Alerting**: Observability integration points

## Common Pitfalls

### Pitfall 1: Insufficient Testing

**Problem:** Not testing edge cases and error conditions leads to production bugs

**Solution:** Implement comprehensive test coverage including:

- Happy path scenarios
- Error handling and edge cases
- Integration points with external systems

**Prevention:** Enforce minimum code coverage (80%+) in CI/CD pipeline

### Pitfall 2: Hardcoded Configuration

**Problem:** Hardcoding values makes applications inflexible and environment-dependent

**Solution:** Use environment variables and configuration management:

- Separate config from code
- Use environment-specific configuration files
- Never commit secrets to version control

**Prevention:** Use tools like dotenv, config validators, and secret scanners

### Pitfall 3: Ignoring Security Best Practices

**Problem:** Security vulnerabilities from not following established security patterns

**Solution:** Follow security guidelines:

- Input validation and sanitization
- Proper authentication and authorization
- Encrypted data transmission (TLS/SSL)
- Regular security audits and updates

**Prevention:** Use security linters, SAST tools, and regular dependency updates

**Best Practices:**

- Follow established patterns and conventions for kotlin
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

---

*Last updated: 2025-10-17*
