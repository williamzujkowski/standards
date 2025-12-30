# Rust Coding Standards - Complete Reference

> **Note**: This is the Level 3 reference document for the Rust Coding Standards skill.
> For the core skill content, see [SKILL.md](./SKILL.md).

## Table of Contents

- [Ownership Deep Dive](#ownership-deep-dive)
- [Lifetime Annotations](#lifetime-annotations)
- [Traits & Generics](#traits--generics)
- [Advanced Error Handling](#advanced-error-handling)
- [Concurrency Patterns](#concurrency-patterns)
- [Testing Strategies](#testing-strategies)
- [Documentation Standards](#documentation-standards)
- [Performance Optimization](#performance-optimization)
- [Advanced Patterns](#advanced-patterns)
- [Unsafe Code Guidelines](#unsafe-code-guidelines)
- [Configuration Files](#configuration-files)

---

## Ownership Deep Dive

### Move Semantics

```rust
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 moved to s2

    // println!("{}", s1); // Error: value borrowed after move
    println!("{}", s2); // OK
}

// Clone for deep copy
let s1 = String::from("hello");
let s2 = s1.clone(); // explicit deep copy
println!("s1 = {}, s2 = {}", s1, s2); // Both valid

// Copy trait for stack-only data
let x = 5;
let y = x; // x is copied (not moved)
println!("x = {}, y = {}", x, y); // Both valid

// Types implementing Copy: integers, floats, bool, char, tuples of Copy types
```

### Ownership in Functions

```rust
fn takes_ownership(s: String) {
    println!("{}", s);
} // s dropped here

fn makes_copy(x: i32) {
    println!("{}", x);
} // x goes out of scope, nothing special

fn main() {
    let s = String::from("hello");
    takes_ownership(s); // s moved into function
    // println!("{}", s); // Error

    let x = 5;
    makes_copy(x); // x copied
    println!("{}", x); // Still valid
}

// Return ownership
fn gives_ownership() -> String {
    String::from("hello")
}

fn takes_and_gives_back(s: String) -> String {
    s // return ownership to caller
}
```

### Dangling References Prevention

```rust
// This won't compile
fn dangle() -> &String {
    let s = String::from("hello");
    &s // returns reference to value that will be dropped
} // s goes out of scope and is dropped

// Return owned value instead
fn no_dangle() -> String {
    String::from("hello")
}
```

---

## Lifetime Annotations

### Why Lifetimes?

```rust
// Compiler needs to know relationship between input and output lifetimes
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// The signature tells compiler:
// - Returned reference lives at least as long as both parameters
// - Both parameters must have the same lifetime

fn main() {
    let string1 = String::from("long string");
    let result;
    {
        let string2 = String::from("short");
        result = longest(string1.as_str(), string2.as_str());
        println!("{}", result); // OK: used within string2's lifetime
    }
    // println!("{}", result); // Error: string2 dropped
}
```

### Lifetime Elision Rules

```rust
// Rule 1: Each parameter gets its own lifetime
fn first_word(s: &str) -> &str { // actually: fn first_word<'a>(s: &'a str) -> &'a str

// Rule 2: If exactly one input lifetime, it's assigned to all outputs
fn parse(s: &str) -> &str { // fn parse<'a>(s: &'a str) -> &'a str

// Rule 3: If multiple inputs and one is &self or &mut self,
// the lifetime of self is assigned to all outputs
impl<'a> ImportantExcerpt<'a> {
    fn level(&self) -> i32 { // no lifetime annotation needed
        3
    }

    fn announce_and_return_part(&self, announcement: &str) -> &str {
        println!("Attention: {}", announcement);
        self.part // returns with lifetime of self
    }
}
```

### Struct Lifetimes

```rust
// Struct holding references needs lifetime parameters
struct ImportantExcerpt<'a> {
    part: &'a str,
}

impl<'a> ImportantExcerpt<'a> {
    fn new(text: &'a str, start: usize, end: usize) -> Self {
        ImportantExcerpt {
            part: &text[start..end],
        }
    }

    fn get_part(&self) -> &str {
        self.part
    }
}

fn main() {
    let novel = String::from("Call me Ishmael. Some years ago...");
    let first_sentence = novel.split('.').next().unwrap();
    let excerpt = ImportantExcerpt::new(&novel, 0, first_sentence.len());
    // novel must outlive excerpt
}
```

### Multiple Lifetimes

```rust
// Different lifetimes for different parameters
struct Context<'a>(&'a str);

struct Parser<'a, 'b> {
    context: &'a Context<'a>,
    input: &'b str,
}

impl<'a, 'b> Parser<'a, 'b> {
    fn parse(&self) -> Result<(), &'b str> {
        // Can return error referencing input
        Err(&self.input[1..])
    }
}
```

---

## Traits & Generics

### Defining Traits

```rust
pub trait Summary {
    // Required method
    fn summarize(&self) -> String;

    // Default implementation
    fn summarize_author(&self) -> String {
        String::from("Anonymous")
    }

    // Method using other trait methods
    fn full_summary(&self) -> String {
        format!("{} by {}", self.summarize(), self.summarize_author())
    }
}

// Implementing traits
pub struct NewsArticle {
    pub headline: String,
    pub location: String,
    pub author: String,
    pub content: String,
}

impl Summary for NewsArticle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.headline, self.author, self.location)
    }

    fn summarize_author(&self) -> String {
        self.author.clone()
    }
}

pub struct Tweet {
    pub username: String,
    pub content: String,
    pub reply: bool,
    pub retweet: bool,
}

impl Summary for Tweet {
    fn summarize(&self) -> String {
        format!("{}: {}", self.username, self.content)
    }

    fn summarize_author(&self) -> String {
        format!("@{}", self.username)
    }
}
```

### Trait Bounds

```rust
// Function accepting any type implementing Summary
pub fn notify(item: &impl Summary) {
    println!("Breaking news! {}", item.summarize());
}

// Trait bound syntax (equivalent)
pub fn notify<T: Summary>(item: &T) {
    println!("Breaking news! {}", item.summarize());
}

// Multiple trait bounds
pub fn compare<T: Summary + Display>(a: &T, b: &T) {
    println!("Comparing: {} vs {}", a, b);
}

// where clause for readability
pub fn complex_function<T, U>(t: &T, u: &U) -> String
where
    T: Display + Clone,
    U: Clone + Debug,
{
    format!("{:?}", u)
}

// Returning trait types
fn returns_summarizable() -> impl Summary {
    Tweet {
        username: String::from("user"),
        content: String::from("content"),
        reply: false,
        retweet: false,
    }
}
```

### Blanket Implementations

```rust
// Implement trait for any type satisfying bounds
use std::fmt::Display;

trait ToJson {
    fn to_json(&self) -> String;
}

impl<T: Display> ToJson for T {
    fn to_json(&self) -> String {
        format!("\"{}\"", self)
    }
}

// Now any type implementing Display automatically gets ToJson
```

### Common Traits Reference

```rust
// Debug: formatted with {:?}
#[derive(Debug)]
struct Point { x: i32, y: i32 }

// Clone: explicit copying
#[derive(Clone)]
struct Data { content: Vec<u8> }

// Copy: implicit copying (requires Clone)
#[derive(Copy, Clone)]
struct Point2D { x: f64, y: f64 }

// PartialEq, Eq: equality comparison
#[derive(PartialEq, Eq)]
struct UserId(u32);

// PartialOrd, Ord: ordering
#[derive(PartialOrd, Ord, PartialEq, Eq)]
enum Priority { Low, Medium, High }

// Hash: use in HashMap/HashSet
#[derive(Hash, PartialEq, Eq)]
struct CacheKey(String);

// Default: default value
#[derive(Default)]
struct Config {
    timeout: u32, // 0
    retries: u32, // 0
}
```

---

## Advanced Error Handling

### Custom Error Types with thiserror

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataStoreError {
    #[error("Connection failed: {0}")]
    ConnectionFailed(String),

    #[error("Query failed: {query}")]
    QueryFailed {
        query: String,
        #[source]
        source: sqlx::Error,
    },

    #[error("Record not found: {0}")]
    NotFound(String),

    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("I/O error")]
    Io(#[from] std::io::Error),

    #[error("Database error")]
    Database(#[from] sqlx::Error),
}

pub type Result<T> = std::result::Result<T, DataStoreError>;
```

### Error Context with anyhow

```rust
use anyhow::{Context, Result};

fn read_config() -> Result<Config> {
    let path = "config.toml";
    let content = fs::read_to_string(path)
        .context(format!("Failed to read config file: {}", path))?;

    toml::from_str(&content)
        .context("Failed to parse config as TOML")
}

fn main() -> Result<()> {
    let config = read_config()
        .context("Application initialization failed")?;

    process(&config)?;

    Ok(())
}
```

### Error Conversion Chain

```rust
#[derive(Error, Debug)]
pub enum AppError {
    #[error("Configuration error: {0}")]
    Config(#[from] ConfigError),

    #[error("Database error: {0}")]
    Database(#[from] DbError),
}

#[derive(Error, Debug)]
pub enum ConfigError {
    #[error("Parse error: {0}")]
    Parse(#[from] toml::de::Error),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

// Automatic conversion chain: toml::de::Error -> ConfigError -> AppError
fn load_app() -> Result<App, AppError> {
    let config = load_config()?; // toml::de::Error auto-converted
    let db = connect_db(&config)?; // DbError auto-converted
    Ok(App { config, db })
}
```

---

## Concurrency Patterns

### Async/Await Basics

```rust
use tokio;

#[tokio::main]
async fn main() -> Result<()> {
    let result = fetch_data().await?;
    process(result).await?;
    Ok(())
}

async fn fetch_data() -> Result<Data> {
    let response = reqwest::get("https://api.example.com/data").await?;
    let data = response.json().await?;
    Ok(data)
}

async fn process(data: Data) -> Result<()> {
    // Async processing
    tokio::time::sleep(Duration::from_secs(1)).await;
    Ok(())
}
```

### Concurrent Tasks

```rust
use tokio;

async fn fetch_all() -> Result<Vec<Data>> {
    let urls = vec![
        "https://api.example.com/1",
        "https://api.example.com/2",
        "https://api.example.com/3",
    ];

    // Sequential (slow)
    let mut results = Vec::new();
    for url in urls {
        results.push(fetch_url(url).await?);
    }

    // Concurrent with join_all
    let futures = urls.iter().map(|url| fetch_url(url));
    let results: Vec<_> = futures::future::join_all(futures).await;

    // Concurrent with tokio::spawn
    let mut handles = Vec::new();
    for url in urls {
        let handle = tokio::spawn(async move {
            fetch_url(&url).await
        });
        handles.push(handle);
    }

    let mut results = Vec::new();
    for handle in handles {
        results.push(handle.await??);
    }

    Ok(results)
}
```

### Channel Patterns

```rust
use tokio::sync::{mpsc, oneshot};

// Multi-producer, single-consumer
async fn worker_pool() {
    let (tx, mut rx) = mpsc::channel(32);

    // Spawn workers
    for i in 0..4 {
        let tx = tx.clone();
        tokio::spawn(async move {
            loop {
                let work = generate_work(i).await;
                if tx.send(work).await.is_err() {
                    break;
                }
            }
        });
    }
    drop(tx); // Close channel when all senders dropped

    // Consume results
    while let Some(result) = rx.recv().await {
        process_result(result).await;
    }
}

// One-shot channel for single value
async fn compute_async(x: i32) -> Result<i32> {
    let (tx, rx) = oneshot::channel();

    tokio::spawn(async move {
        let result = expensive_computation(x);
        let _ = tx.send(result);
    });

    rx.await.map_err(|_| anyhow::anyhow!("Computation failed"))
}
```

### Shared State Patterns

```rust
use std::sync::Arc;
use tokio::sync::{Mutex, RwLock};

// Arc for shared ownership across threads
#[derive(Clone)]
struct AppState {
    counter: Arc<Mutex<u64>>,
    cache: Arc<RwLock<HashMap<String, String>>>,
}

async fn increment(state: AppState) {
    let mut counter = state.counter.lock().await;
    *counter += 1;
}

async fn read_cache(state: AppState, key: &str) -> Option<String> {
    let cache = state.cache.read().await;
    cache.get(key).cloned()
}

async fn write_cache(state: AppState, key: String, value: String) {
    let mut cache = state.cache.write().await;
    cache.insert(key, value);
}
```

---

## Testing Strategies

### Unit Tests

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_addition() {
        assert_eq!(2 + 2, 4);
    }

    #[test]
    fn test_string_contains() {
        let s = "hello world";
        assert!(s.contains("world"));
        assert!(!s.contains("goodbye"));
    }

    #[test]
    #[should_panic(expected = "divide by zero")]
    fn test_division_by_zero() {
        divide(10, 0);
    }

    #[test]
    fn test_result() -> Result<()> {
        let result = parse_number("42")?;
        assert_eq!(result, 42);
        Ok(())
    }
}
```

### Integration Tests

```rust
// tests/integration_test.rs
use my_crate::{Config, App};

#[test]
fn test_full_workflow() {
    let config = Config::default();
    let app = App::new(config);

    let result = app.process_data("input.txt");
    assert!(result.is_ok());

    let output = result.unwrap();
    assert_eq!(output.len(), 100);
}

#[tokio::test]
async fn test_async_operation() {
    let result = fetch_and_process().await;
    assert!(result.is_ok());
}
```

### Property-Based Testing with proptest

```rust
use proptest::prelude::*;

proptest! {
    #[test]
    fn test_reverse_twice(s in ".*") {
        let reversed_twice: String = s.chars().rev().collect::<String>()
            .chars().rev().collect();
        assert_eq!(s, reversed_twice);
    }

    #[test]
    fn test_addition_commutative(a in 0..1000i32, b in 0..1000i32) {
        assert_eq!(a + b, b + a);
    }
}
```

### Test Fixtures & Helpers

```rust
#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    struct TestContext {
        temp_dir: TempDir,
        db: Database,
    }

    impl TestContext {
        fn new() -> Self {
            let temp_dir = TempDir::new().unwrap();
            let db = Database::connect_memory().unwrap();
            Self { temp_dir, db }
        }

        fn create_test_user(&self) -> User {
            User {
                id: 1,
                name: "Test User".to_string(),
                email: "test@example.com".to_string(),
            }
        }
    }

    #[test]
    fn test_with_context() {
        let ctx = TestContext::new();
        let user = ctx.create_test_user();

        let result = ctx.db.insert_user(&user);
        assert!(result.is_ok());
    }
}
```

### Mocking with mockall

```rust
use mockall::{automock, predicate::*};

#[automock]
trait Database {
    fn get_user(&self, id: u32) -> Result<User>;
    fn save_user(&mut self, user: &User) -> Result<()>;
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_with_mock() {
        let mut mock_db = MockDatabase::new();

        mock_db
            .expect_get_user()
            .with(eq(1))
            .times(1)
            .returning(|_| Ok(User::default()));

        let user = mock_db.get_user(1).unwrap();
        assert_eq!(user.id, 0);
    }
}
```

---

## Documentation Standards

### Doc Comments

```rust
/// Calculates the sum of two numbers.
///
/// # Examples
///
/// ```
/// let result = my_crate::add(2, 3);
/// assert_eq!(result, 5);
/// ```
///
/// # Panics
///
/// This function will panic if the sum overflows.
///
/// # Errors
///
/// Returns an error if...
///
/// # Safety
///
/// This function is unsafe because...
pub fn add(a: i32, b: i32) -> i32 {
    a + b
}

/// A user in the system.
///
/// # Examples
///
/// ```
/// use my_crate::User;
///
/// let user = User::new("Alice", "alice@example.com");
/// assert_eq!(user.name, "Alice");
/// ```
pub struct User {
    /// The user's unique identifier
    pub id: u32,
    /// The user's display name
    pub name: String,
    /// The user's email address
    pub email: String,
}
```

### Module Documentation

```rust
//! This module provides utilities for working with users.
//!
//! # Examples
//!
//! ```
//! use my_crate::user::{User, UserRepository};
//!
//! let repo = UserRepository::new();
//! let user = repo.find_by_email("user@example.com")?;
//! ```

/// User management functionality
pub mod user {
    // ...
}
```

---

## Performance Optimization

### Zero-Cost Abstractions

```rust
// Iterators compile to equivalent loops
let sum: i32 = (1..=100)
    .filter(|x| x % 2 == 0)
    .map(|x| x * 2)
    .sum();

// Generic functions monomorphized (no runtime cost)
fn print<T: Display>(value: T) {
    println!("{}", value);
}

print(42);        // Compiles to version for i32
print("hello");   // Compiles to version for &str
```

### Avoiding Allocations

```rust
// Prefer slices over owned strings
fn count_words(text: &str) -> usize {  // Not String
    text.split_whitespace().count()
}

// Use Cow for conditional cloning
use std::borrow::Cow;

fn process_text(text: &str) -> Cow<str> {
    if text.contains("bad") {
        Cow::Owned(text.replace("bad", "good"))
    } else {
        Cow::Borrowed(text)
    }
}

// Reuse buffers
let mut buffer = String::with_capacity(1024);
for item in items {
    buffer.clear();
    write!(&mut buffer, "{}", item)?;
    send(&buffer)?;
}
```

### Inlining Hints

```rust
#[inline]
pub fn small_function() -> i32 {
    42
}

#[inline(always)]
pub fn always_inline() -> i32 {
    100
}

#[inline(never)]
pub fn never_inline() {
    // Complex function
}
```

### Profiling

```bash
# CPU profiling with cargo-flamegraph
cargo install flamegraph
cargo flamegraph --bin my-app

# Memory profiling with valgrind
cargo build --release
valgrind --tool=massif target/release/my-app

# Benchmarking with criterion
cargo bench
```

### Compiler Optimizations

```toml
# Cargo.toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = 'abort'
```

---

## Advanced Patterns

### Newtype Pattern

```rust
// Strong typing prevents mix-ups
struct UserId(u32);
struct ProductId(u32);

fn get_user(id: UserId) -> User { /* ... */ }
// get_user(ProductId(1)); // Compile error

// Add methods to newtypes
impl UserId {
    fn new(id: u32) -> Self {
        UserId(id)
    }

    fn value(&self) -> u32 {
        self.0
    }
}

// Derive common traits
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
struct Email(String);

impl Email {
    fn parse(s: &str) -> Result<Self, ValidationError> {
        if s.contains('@') {
            Ok(Email(s.to_string()))
        } else {
            Err(ValidationError::InvalidEmail)
        }
    }
}
```

### Typestate Pattern

```rust
use std::marker::PhantomData;

// States as zero-sized types
struct Locked;
struct Unlocked;

struct Door<State> {
    _state: PhantomData<State>,
}

impl Door<Locked> {
    fn new() -> Self {
        Door { _state: PhantomData }
    }

    fn unlock(self, key: &Key) -> Result<Door<Unlocked>, Error> {
        if key.is_valid() {
            Ok(Door { _state: PhantomData })
        } else {
            Err(Error::InvalidKey)
        }
    }
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> {
        Door { _state: PhantomData }
    }

    fn open(&mut self) {
        println!("Door opened");
    }
}

// Usage - compile-time guarantees
let door = Door::new(); // Locked
let door = door.unlock(&key)?; // Unlocked
// door.lock(); // Can't call lock on locked door - compile error
```

### Builder Pattern

```rust
#[derive(Default)]
pub struct RequestBuilder {
    url: Option<String>,
    method: Method,
    headers: HashMap<String, String>,
    body: Option<Vec<u8>>,
    timeout: Duration,
}

impl RequestBuilder {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn url(mut self, url: impl Into<String>) -> Self {
        self.url = Some(url.into());
        self
    }

    pub fn method(mut self, method: Method) -> Self {
        self.method = method;
        self
    }

    pub fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.insert(key.into(), value.into());
        self
    }

    pub fn body(mut self, body: impl Into<Vec<u8>>) -> Self {
        self.body = Some(body.into());
        self
    }

    pub fn timeout(mut self, timeout: Duration) -> Self {
        self.timeout = timeout;
        self
    }

    pub fn build(self) -> Result<Request, BuildError> {
        let url = self.url.ok_or(BuildError::MissingUrl)?;
        Ok(Request {
            url,
            method: self.method,
            headers: self.headers,
            body: self.body,
            timeout: self.timeout,
        })
    }
}

// Usage
let request = RequestBuilder::new()
    .url("https://api.example.com")
    .method(Method::POST)
    .header("Content-Type", "application/json")
    .body(json_bytes)
    .timeout(Duration::from_secs(30))
    .build()?;
```

---

## Unsafe Code Guidelines

### When Unsafe is Necessary

- FFI (Foreign Function Interface)
- Raw pointer manipulation
- Implementing unsafe traits (Send, Sync)
- Performance-critical code after profiling

### Safety Documentation

```rust
/// # Safety
///
/// - `ptr` must be valid for reads of `len` bytes
/// - Memory must be initialized
/// - No mutable aliases during lifetime 'a
unsafe fn from_raw_parts<'a>(ptr: *const u8, len: usize) -> &'a [u8] {
    std::slice::from_raw_parts(ptr, len)
}
```

### Minimizing Unsafe Scope

```rust
// Bad: large unsafe block
unsafe {
    let ptr = allocate(size);
    // ... many lines of code ...
    deallocate(ptr);
}

// Good: minimal unsafe, safe wrapper
fn safe_allocate(size: usize) -> Box<[u8]> {
    let ptr = unsafe { allocate(size) };
    // Safe operations with ptr
    unsafe { Box::from_raw(std::slice::from_raw_parts_mut(ptr, size)) }
}
```

### Testing with Miri

```bash
# Install Miri
rustup +nightly component add miri

# Run tests with Miri (detects undefined behavior)
cargo +nightly miri test
```

---

## Configuration Files

### rustfmt.toml

```toml
# Rust formatter configuration
edition = "2021"
max_width = 100
tab_spaces = 4
newline_style = "Unix"
use_small_heuristics = "Default"
reorder_imports = true
reorder_modules = true
remove_nested_parens = true
format_strings = false
format_macro_matchers = false
format_macro_bodies = true
merge_derives = true
use_try_shorthand = true
use_field_init_shorthand = true
force_explicit_abi = true
```

### clippy.toml

```toml
# Clippy linter configuration
avoid-breaking-exported-api = false
cognitive-complexity-threshold = 25
disallowed-methods = []
disallowed-types = []
doc-valid-idents = ["GitHub", "GitLab", "JavaScript", "TypeScript"]
msrv = "1.70.0"
too-many-arguments-threshold = 7
type-complexity-threshold = 250
```

### Cargo.toml Best Practices

```toml
[package]
name = "my-project"
version = "0.1.0"
edition = "2021"
rust-version = "1.70"
authors = ["Your Name <you@example.com>"]
description = "A brief description"
license = "MIT OR Apache-2.0"
repository = "https://github.com/user/repo"
documentation = "https://docs.rs/my-project"
keywords = ["rust", "example"]
categories = ["development-tools"]

[dependencies]
tokio = { version = "1.0", features = ["full"] }
serde = { version = "1.0", features = ["derive"] }
thiserror = "1.0"
anyhow = "1.0"

[dev-dependencies]
criterion = "0.5"
proptest = "1.0"
mockall = "0.11"
tempfile = "3.0"

[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = 'abort'

[profile.dev]
opt-level = 0
debug = true

[profile.test]
opt-level = 0
debug = true

[[bench]]
name = "benchmarks"
harness = false
```

---

## Learning Resources

### Official Resources

- [The Rust Book](https://doc.rust-lang.org/book/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/) (unsafe Rust)
- [Async Book](https://rust-lang.github.io/async-book/)

### Practice

- [Rustlings](https://github.com/rust-lang/rustlings)
- [Exercism Rust Track](https://exercism.org/tracks/rust)
- [Advent of Code in Rust](https://adventofcode.com/)

### Advanced

- [Rust Design Patterns](https://rust-unofficial.github.io/patterns/)
- [Rust for Rustaceans](https://nostarch.com/rust-rustaceans) (book)
- [Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/)

### Async/Concurrency

- [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
- [Async Rust](https://rust-lang.github.io/async-book/)

---

## Quick Reference Card

### Ownership Rules

| Rule | Description |
|------|-------------|
| Single owner | Each value has exactly one owner |
| Move semantics | Assignment moves by default |
| Drop on scope exit | Values cleaned up when owner exits scope |
| Clone for deep copy | Use `.clone()` for explicit copies |
| Copy for stack types | Primitives implement Copy trait |

### Borrowing Rules

| Rule | Description |
|------|-------------|
| `&T` | Immutable borrow (multiple allowed) |
| `&mut T` | Mutable borrow (exclusive) |
| No mixing | Cannot have `&mut T` and `&T` simultaneously |
| NLL | Non-lexical lifetimes - borrows end at last use |

### Common Patterns

| Pattern | Use Case |
|---------|----------|
| Newtype | Type safety, semantic meaning |
| Typestate | Compile-time state machine validation |
| Builder | Complex object construction |
| RAII | Resource management via Drop |

### Error Handling

| Crate | Use Case |
|-------|----------|
| `thiserror` | Library error types |
| `anyhow` | Application error handling |
| `?` operator | Early return on error |
| `Result<T, E>` | Fallible operations |
| `Option<T>` | Optional values |

---

*Last updated: 2024*
