---
name: rust-coding-standards
category: coding-standards
difficulty: intermediate
estimated_time: 45 minutes
version: 1.0.0
tags:
- rust
- ownership
- borrowing
- memory-safety
- performance
dependencies: []
description: // Immutable borrow (multiple allowed) let s = String::from("hello");
  let r1 = &s; let r2 = &s; println!("{} and {}", r1, r2); // ✓ OK
---


# Rust Coding Standards

> **Purpose**: Master Rust's ownership system, type safety, and zero-cost abstractions for building safe, concurrent, and performant systems.

## Level 1: Quick Reference

### Core Principles

- **Ownership**: Each value has exactly one owner
- **Borrowing**: References allow multiple readers XOR one writer
- **Zero-cost abstractions**: High-level code compiles to optimal machine code
- **Explicit over implicit**: No hidden allocations or control flow

### Ownership & Borrowing Cheat Sheet

```rust
// Ownership transfer (move)
let s1 = String::from("hello");
let s2 = s1; // s1 is now invalid

// Immutable borrow (multiple allowed)
let s = String::from("hello");
let r1 = &s;
let r2 = &s;
println!("{} and {}", r1, r2); // ✓ OK

// Mutable borrow (exclusive)
let mut s = String::from("hello");
let r1 = &mut s;
r1.push_str(" world");
// let r2 = &s; // ✗ Error: cannot borrow while mutable borrow exists

// Copy types (stack-only)
let x = 5;
let y = x; // x is still valid (i32 implements Copy)
```

### Common Patterns

#### Result & Option

```rust
// Option: value may be absent
match find_user(42) {
    Some(user) => println!("Found: {}", user.name),
    None => println!("Not found"),
}

// Combinators
let name = find_user(42).map(|u| u.name).unwrap_or("Anonymous".into());

// Early return with ?
fn process() -> Result<(), Error> {
    let config = parse_config("app.toml")?;
    Ok(())
}
```

#### Iterators

```rust
// Transformation pipeline
let sum: i32 = vec![1, 2, 3, 4, 5]
    .iter()
    .filter(|&x| x % 2 == 0)
    .map(|x| x * 2)
    .sum();

// Collect into different types
let doubled: Vec<i32> = numbers.iter().map(|x| x * 2).collect();
let set: HashSet<i32> = numbers.into_iter().collect();
```

#### Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),

    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),

    #[error("Invalid configuration: {0}")]
    Config(String),

    #[error("Not found: {0}")]
    NotFound(String),
}

pub type Result<T> = std::result::Result<T, AppError>;
```

### Essential Checklist

- [ ] **Clippy passes**: `cargo clippy -- -D warnings`
- [ ] **Format enforced**: `cargo fmt -- --check`
- [ ] **No compiler warnings**: `cargo check --all-targets`
- [ ] **Tests pass**: `cargo test`
- [ ] **Documentation builds**: `cargo doc --no-deps`
- [ ] **No unsafe without justification**: Document all `unsafe` blocks
- [ ] **Dependencies audited**: `cargo audit`
- [ ] **Error types are descriptive**: Use thiserror or custom types

### Quick Wins

```rust
// Use Result for fallible operations
fn read_config() -> Result<Config> {
    let content = fs::read_to_string("config.toml")?;
    Ok(toml::from_str(&content)?)
}

// Derive common traits
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct User {
    pub id: u32,
    pub name: String,
}

// Use iterators over loops
// ✗ Avoid
let mut sum = 0;
for x in numbers {
    sum += x;
}

// ✓ Prefer
let sum: i32 = numbers.iter().sum();
```

### Lifetimes

```rust
// Specify reference relationships
fn longest<'a>(x: &'a str, y: &'a str) -> &'a str {
    if x.len() > y.len() { x } else { y }
}

// Struct with lifetime
struct Excerpt<'a> { part: &'a str }

// Static lifetime
const CONFIG: &'static str = "default";
```

### Memory Safety Rules

1. **No data races**: Compiler enforces at compile time
2. **No null pointers**: Use `Option<T>` instead
3. **No dangling pointers**: Borrow checker prevents
4. **No use-after-free**: Ownership system prevents
5. **No buffer overflows**: Bounds checking (can be optimized away)


## Level 2: Implementation Guide

### Ownership System Deep Dive

#### The Three Rules

1. Each value in Rust has a variable that's called its owner
2. There can only be one owner at a time
3. When the owner goes out of scope, the value will be dropped

```rust
// Move semantics
fn main() {
    let s1 = String::from("hello");
    let s2 = s1; // s1 moved to s2

    // println!("{}", s1); // ✗ Error: value borrowed after move
    println!("{}", s2); // ✓ OK
}

// Clone for deep copy
let s1 = String::from("hello");
let s2 = s1.clone(); // explicit deep copy
println!("s1 = {}, s2 = {}", s1, s2); // ✓ Both valid

// Copy trait for stack-only data
let x = 5;
let y = x; // x is copied (not moved)
println!("x = {}, y = {}", x, y); // ✓ Both valid

// Types implementing Copy: integers, floats, bool, char, tuples of Copy types
```

#### Ownership in Functions

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
    // println!("{}", s); // ✗ Error

    let x = 5;
    makes_copy(x); // x copied
    println!("{}", x); // ✓ Still valid
}

// Return ownership
fn gives_ownership() -> String {
    String::from("hello")
}

fn takes_and_gives_back(s: String) -> String {
    s // return ownership to caller
}
```

### Borrowing & References

#### Immutable References

```rust
// Multiple immutable borrows allowed
fn calculate_length(s: &String) -> usize {
    s.len()
} // s goes out of scope, but doesn't own the data

fn main() {
    let s1 = String::from("hello");
    let len = calculate_length(&s1); // borrow s1
    println!("Length of '{}' is {}", s1, len); // s1 still valid
}

// Multiple simultaneous immutable borrows
let s = String::from("hello");
let r1 = &s;
let r2 = &s;
let r3 = &s;
println!("{}, {}, {}", r1, r2, r3); // ✓ OK
```

#### Mutable References

```rust
// Only one mutable borrow allowed
fn change(s: &mut String) {
    s.push_str(", world");
}

fn main() {
    let mut s = String::from("hello");
    change(&mut s);
    println!("{}", s); // "hello, world"
}

// Cannot mix mutable and immutable borrows
let mut s = String::from("hello");
let r1 = &s; // ✓ OK
let r2 = &s; // ✓ OK
// let r3 = &mut s; // ✗ Error: cannot borrow as mutable
println!("{} and {}", r1, r2);

// But this works (non-lexical lifetimes)
let mut s = String::from("hello");
let r1 = &s;
let r2 = &s;
println!("{} and {}", r1, r2); // last use of r1 and r2
let r3 = &mut s; // ✓ OK: r1 and r2 no longer used
r3.push_str(" world");
```

#### Dangling References Prevention

```rust
// ✗ This won't compile
fn dangle() -> &String {
    let s = String::from("hello");
    &s // returns reference to value that will be dropped
} // s goes out of scope and is dropped

// ✓ Return owned value instead
fn no_dangle() -> String {
    String::from("hello")
}
```

### Lifetime Annotations

#### Why Lifetimes?

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
        println!("{}", result); // ✓ OK: used within string2's lifetime
    }
    // println!("{}", result); // ✗ Error: string2 dropped
}
```

#### Lifetime Elision Rules

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

#### Struct Lifetimes

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

#### Multiple Lifetimes

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

### Traits & Generics

#### Defining Traits

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

#### Trait Bounds

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

#### Blanket Implementations

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

#### Common Traits

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

### Advanced Error Handling

#### Custom Error Types with thiserror

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

#### Error Context with anyhow

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

#### Error Conversion Chain

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

### Concurrency

#### Async/Await Basics

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

#### Concurrent Tasks

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

#### Channels

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

#### Shared State

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

### Testing

#### Unit Tests

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

#### Integration Tests

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

#### Property-Based Testing with proptest

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

#### Test Fixtures & Helpers

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

#### Mocking with mockall

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

### Documentation

#### Doc Comments

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

#### Module Documentation

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

### Performance Optimization

#### Zero-Cost Abstractions

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

#### Avoiding Allocations

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

#### Inlining

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


## Level 3: Deep Dive Resources

### Advanced Patterns

#### Newtype Pattern

Encapsulate types for type safety and semantic clarity:

```rust
// Strong typing prevents mix-ups
struct UserId(u32);
struct ProductId(u32);

fn get_user(id: UserId) -> User { /* ... */ }
// get_user(ProductId(1)); // ✗ Compile error
```

See: `resources/newtype-pattern.md`

#### Typestate Pattern

Encode state machines in the type system:

```rust
struct Locked;
struct Unlocked;

struct Door<State> {
    _state: PhantomData<State>,
}

impl Door<Locked> {
    fn unlock(self) -> Door<Unlocked> { /* ... */ }
}

impl Door<Unlocked> {
    fn lock(self) -> Door<Locked> { /* ... */ }
    fn open(&mut self) { /* ... */ }
}
```

See: `resources/typestate-pattern.md`

### Unsafe Code Guidelines

When `unsafe` is necessary:

- **Document invariants**: Explain what must be true for safety
- **Minimize scope**: Keep unsafe blocks small
- **Encapsulate**: Wrap unsafe in safe APIs
- **Test extensively**: Include miri in CI

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

See: `resources/unsafe-guidelines.md`

### Performance Optimization

#### Profiling

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

#### Compiler Optimizations

```toml
# Cargo.toml
[profile.release]
opt-level = 3
lto = true
codegen-units = 1
panic = 'abort'
```

See: `resources/performance-guide.md`

### Learning Path

1. **Start**: Rust Book (<https://doc.rust-lang.org/book/>)
2. **Practice**: Rustlings (<https://github.com/rust-lang/rustlings>)
3. **Patterns**: Rust Design Patterns (<https://rust-unofficial.github.io/patterns/>)
4. **Advanced**: Rust for Rustaceans (book)
5. **Async**: Tokio Tutorial (<https://tokio.rs/tokio/tutorial>)

### Bundled Resources

This skill includes ready-to-use configuration files and templates in the skill directory:

- `config/rustfmt.toml` - Rust code formatter configuration
- `config/clippy.toml` - Clippy linter rules
- `templates/lib-template.rs` - Library crate skeleton
- `templates/main-template.rs` - Binary crate with error handling
- `templates/test-template.rs` - Comprehensive test suite template
- `scripts/setup-rust-project.sh` - Project initialization script

### Quick Setup

```bash
# Copy formatter config to your project
cp config/rustfmt.toml .

# Copy linter config
cp config/clippy.toml .

# Initialize new project with best practices
bash scripts/setup-rust-project.sh my-project
```

### Common Pitfalls to Avoid

1. **Fighting the borrow checker**: Design with ownership in mind
2. **Over-using `.clone()`**: Profile before optimizing
3. **Ignoring Clippy warnings**: They're usually right
4. **Not using `?` operator**: Makes error handling cleaner
5. **Premature unsafe**: Try safe abstractions first
6. **String vs &str confusion**: Prefer &str for parameters
7. **Not leveraging iterators**: More idiomatic and often faster

### Next Steps

- Master the ownership system through practice
- Contribute to open-source Rust projects
- Learn async/await for concurrent applications
- Explore procedural macros for code generation
- Study the standard library source code
- Join the Rust community (users.rust-lang.org)

## Examples

### Basic Usage

```rust
// TODO: Add basic example for rust
// This example demonstrates core functionality
```

### Advanced Usage

```rust
// TODO: Add advanced example for rust
// This example shows production-ready patterns
```

### Integration Example

```rust
// TODO: Add integration example showing how rust
// works with other systems and services
```

See `examples/rust/` for complete working examples.

## Integration Points

This skill integrates with:

### Upstream Dependencies

- **Tools**: Common development tools and frameworks
- **Prerequisites**: Basic understanding of general concepts

### Downstream Consumers

- **Applications**: Production systems requiring rust functionality
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

- Follow established patterns and conventions for rust
- Keep dependencies up to date and scan for vulnerabilities
- Write comprehensive documentation and inline comments
- Use linting and formatting tools consistently
- Implement proper error handling and logging
- Regular code reviews and pair programming
- Monitor production metrics and set up alerts

---

---

**Skill Complete**: You now have comprehensive Rust coding standards covering ownership, traits, error handling, concurrency, testing, and performance optimization. Use the bundled resources to kickstart your Rust projects with best practices built-in.
