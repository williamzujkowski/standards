//! Comprehensive test template
//!
//! Demonstrates:
//! - Unit tests
//! - Integration tests
//! - Property-based tests
//! - Test fixtures
//! - Async tests
//! - Benchmarks

use std::sync::Arc;
use tempfile::TempDir;

// Test subject
#[derive(Debug, Clone, PartialEq)]
pub struct Calculator {
    precision: u32,
}

impl Calculator {
    pub fn new(precision: u32) -> Self {
        Self { precision }
    }
    
    pub fn add(&self, a: f64, b: f64) -> f64 {
        let multiplier = 10_f64.powi(self.precision as i32);
        ((a + b) * multiplier).round() / multiplier
    }
    
    pub fn subtract(&self, a: f64, b: f64) -> f64 {
        self.add(a, -b)
    }
    
    pub fn multiply(&self, a: f64, b: f64) -> f64 {
        let multiplier = 10_f64.powi(self.precision as i32);
        ((a * b) * multiplier).round() / multiplier
    }
    
    pub fn divide(&self, a: f64, b: f64) -> Result<f64, String> {
        if b == 0.0 {
            return Err("Division by zero".to_string());
        }
        let multiplier = 10_f64.powi(self.precision as i32);
        Ok(((a / b) * multiplier).round() / multiplier)
    }
}

// Async function for testing
pub async fn async_operation(value: i32) -> Result<i32, String> {
    tokio::time::sleep(std::time::Duration::from_millis(10)).await;
    if value < 0 {
        Err("Negative value".to_string())
    } else {
        Ok(value * 2)
    }
}

#[cfg(test)]
mod unit_tests {
    use super::*;
    
    // Basic unit tests
    #[test]
    fn test_calculator_new() {
        let calc = Calculator::new(2);
        assert_eq!(calc.precision, 2);
    }
    
    #[test]
    fn test_add() {
        let calc = Calculator::new(2);
        assert_eq!(calc.add(1.5, 2.3), 3.8);
    }
    
    #[test]
    fn test_subtract() {
        let calc = Calculator::new(2);
        assert_eq!(calc.subtract(5.5, 2.3), 3.2);
    }
    
    #[test]
    fn test_multiply() {
        let calc = Calculator::new(2);
        assert_eq!(calc.multiply(2.5, 3.0), 7.5);
    }
    
    #[test]
    fn test_divide_success() {
        let calc = Calculator::new(2);
        let result = calc.divide(10.0, 2.0);
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), 5.0);
    }
    
    #[test]
    fn test_divide_by_zero() {
        let calc = Calculator::new(2);
        let result = calc.divide(10.0, 0.0);
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Division by zero");
    }
    
    #[test]
    #[should_panic(expected = "assertion failed")]
    fn test_should_panic() {
        assert_eq!(1, 2);
    }
    
    #[test]
    #[ignore]
    fn test_expensive_operation() {
        // Run only with: cargo test -- --ignored
        std::thread::sleep(std::time::Duration::from_secs(5));
    }
}

#[cfg(test)]
mod test_fixtures {
    use super::*;
    
    // Test fixture struct
    struct TestContext {
        temp_dir: TempDir,
        calculator: Calculator,
    }
    
    impl TestContext {
        fn new() -> Self {
            Self {
                temp_dir: TempDir::new().unwrap(),
                calculator: Calculator::new(2),
            }
        }
        
        fn temp_path(&self, filename: &str) -> std::path::PathBuf {
            self.temp_dir.path().join(filename)
        }
    }
    
    #[test]
    fn test_with_fixture() {
        let ctx = TestContext::new();
        
        // Use temporary directory
        let file_path = ctx.temp_path("test.txt");
        std::fs::write(&file_path, "test data").unwrap();
        assert!(file_path.exists());
        
        // Use calculator
        let result = ctx.calculator.add(1.0, 2.0);
        assert_eq!(result, 3.0);
    }
}

#[cfg(test)]
mod property_based_tests {
    use super::*;
    use proptest::prelude::*;
    
    proptest! {
        #[test]
        fn test_add_commutative(a in -1000.0..1000.0, b in -1000.0..1000.0) {
            let calc = Calculator::new(2);
            let result1 = calc.add(a, b);
            let result2 = calc.add(b, a);
            // Use approximate equality due to floating point
            prop_assert!((result1 - result2).abs() < 0.01);
        }
        
        #[test]
        fn test_add_associative(a in -100.0..100.0, b in -100.0..100.0, c in -100.0..100.0) {
            let calc = Calculator::new(2);
            let result1 = calc.add(calc.add(a, b), c);
            let result2 = calc.add(a, calc.add(b, c));
            prop_assert!((result1 - result2).abs() < 0.01);
        }
        
        #[test]
        fn test_multiply_by_zero(x in -1000.0..1000.0) {
            let calc = Calculator::new(2);
            let result = calc.multiply(x, 0.0);
            prop_assert_eq!(result, 0.0);
        }
        
        #[test]
        fn test_divide_multiply_inverse(x in -1000.0..1000.0, y in 1.0..1000.0) {
            let calc = Calculator::new(2);
            let divided = calc.divide(x, y).unwrap();
            let multiplied = calc.multiply(divided, y);
            prop_assert!((x - multiplied).abs() < 0.1);
        }
    }
}

#[cfg(test)]
mod async_tests {
    use super::*;
    
    #[tokio::test]
    async fn test_async_operation_success() {
        let result = async_operation(5).await;
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), 10);
    }
    
    #[tokio::test]
    async fn test_async_operation_error() {
        let result = async_operation(-1).await;
        assert!(result.is_err());
        assert_eq!(result.unwrap_err(), "Negative value");
    }
    
    #[tokio::test]
    async fn test_concurrent_operations() {
        let handles: Vec<_> = (0..10)
            .map(|i| tokio::spawn(async move { async_operation(i).await }))
            .collect();
        
        let results: Vec<_> = futures::future::join_all(handles)
            .await
            .into_iter()
            .map(|h| h.unwrap())
            .collect();
        
        assert_eq!(results.len(), 10);
        for (i, result) in results.iter().enumerate() {
            assert!(result.is_ok());
            assert_eq!(result.as_ref().unwrap(), &((i as i32) * 2));
        }
    }
}

#[cfg(test)]
mod parameterized_tests {
    use super::*;
    
    #[test]
    fn test_multiple_precisions() {
        let test_cases = vec![
            (0, 1.5, 2.5, 4.0),
            (1, 1.55, 2.55, 4.1),
            (2, 1.555, 2.555, 4.11),
        ];
        
        for (precision, a, b, expected) in test_cases {
            let calc = Calculator::new(precision);
            let result = calc.add(a, b);
            assert_eq!(result, expected, "Failed for precision {}", precision);
        }
    }
}

#[cfg(test)]
mod mock_tests {
    use super::*;
    use std::sync::Mutex;
    
    // Simple mock trait
    trait DataStore {
        fn get(&self, key: &str) -> Option<String>;
        fn set(&mut self, key: &str, value: String);
    }
    
    // Mock implementation
    struct MockDataStore {
        data: Arc<Mutex<std::collections::HashMap<String, String>>>,
    }
    
    impl MockDataStore {
        fn new() -> Self {
            Self {
                data: Arc::new(Mutex::new(std::collections::HashMap::new())),
            }
        }
    }
    
    impl DataStore for MockDataStore {
        fn get(&self, key: &str) -> Option<String> {
            self.data.lock().unwrap().get(key).cloned()
        }
        
        fn set(&mut self, key: &str, value: String) {
            self.data.lock().unwrap().insert(key.to_string(), value);
        }
    }
    
    #[test]
    fn test_with_mock() {
        let mut store = MockDataStore::new();
        
        store.set("key", "value".to_string());
        assert_eq!(store.get("key"), Some("value".to_string()));
        assert_eq!(store.get("missing"), None);
    }
}

// Benchmarks (requires nightly and criterion)
// Add to Cargo.toml:
// [dev-dependencies]
// criterion = "0.5"
//
// [[bench]]
// name = "calculator_bench"
// harness = false

/*
#[cfg(test)]
mod benchmarks {
    use super::*;
    use criterion::{black_box, criterion_group, criterion_main, Criterion};
    
    fn bench_add(c: &mut Criterion) {
        let calc = Calculator::new(2);
        c.bench_function("add", |b| {
            b.iter(|| calc.add(black_box(1.5), black_box(2.5)))
        });
    }
    
    fn bench_multiply(c: &mut Criterion) {
        let calc = Calculator::new(2);
        c.bench_function("multiply", |b| {
            b.iter(|| calc.multiply(black_box(1.5), black_box(2.5)))
        });
    }
    
    criterion_group!(benches, bench_add, bench_multiply);
    criterion_main!(benches);
}
*/
