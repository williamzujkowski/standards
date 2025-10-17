//! Library crate template with best practices
//!
//! This template demonstrates:
//! - Public API design
//! - Error handling with thiserror
//! - Documentation with examples
//! - Unit testing

use std::fmt;
use thiserror::Error;

/// Custom error types for this library
#[derive(Error, Debug)]
pub enum LibError {
    #[error("Invalid input: {0}")]
    InvalidInput(String),

    #[error("Operation failed: {0}")]
    OperationFailed(String),

    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}

/// Type alias for Results in this library
pub type Result<T> = std::result::Result<T, LibError>;

/// Main library struct
///
/// # Examples
///
/// ```
/// use my_lib::MyLib;
///
/// let lib = MyLib::new("config");
/// assert!(lib.is_ok());
/// ```
#[derive(Debug, Clone)]
pub struct MyLib {
    config: String,
}

impl MyLib {
    /// Creates a new instance
    ///
    /// # Arguments
    ///
    /// * `config` - Configuration string
    ///
    /// # Examples
    ///
    /// ```
    /// use my_lib::MyLib;
    ///
    /// let lib = MyLib::new("default").unwrap();
    /// ```
    ///
    /// # Errors
    ///
    /// Returns `LibError::InvalidInput` if config is empty
    pub fn new(config: impl Into<String>) -> Result<Self> {
        let config = config.into();
        if config.is_empty() {
            return Err(LibError::InvalidInput("config cannot be empty".to_string()));
        }
        Ok(Self { config })
    }

    /// Processes input data
    ///
    /// # Arguments
    ///
    /// * `input` - Input string to process
    ///
    /// # Examples
    ///
    /// ```
    /// use my_lib::MyLib;
    ///
    /// let lib = MyLib::new("config").unwrap();
    /// let result = lib.process("test").unwrap();
    /// assert_eq!(result, "PROCESSED: test");
    /// ```
    pub fn process(&self, input: &str) -> Result<String> {
        if input.is_empty() {
            return Err(LibError::InvalidInput("input cannot be empty".to_string()));
        }
        Ok(format!("PROCESSED: {}", input))
    }

    /// Gets the configuration
    pub fn config(&self) -> &str {
        &self.config
    }
}

impl fmt::Display for MyLib {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "MyLib(config: {})", self.config)
    }
}

/// Trait for custom behavior
pub trait Processor {
    /// Process a value
    fn process(&self, input: &str) -> Result<String>;
}

impl Processor for MyLib {
    fn process(&self, input: &str) -> Result<String> {
        self.process(input)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_new_success() {
        let lib = MyLib::new("test");
        assert!(lib.is_ok());
        assert_eq!(lib.unwrap().config(), "test");
    }

    #[test]
    fn test_new_empty_config() {
        let lib = MyLib::new("");
        assert!(lib.is_err());
        match lib {
            Err(LibError::InvalidInput(_)) => (),
            _ => panic!("Expected InvalidInput error"),
        }
    }

    #[test]
    fn test_process_success() {
        let lib = MyLib::new("config").unwrap();
        let result = lib.process("hello");
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "PROCESSED: hello");
    }

    #[test]
    fn test_process_empty_input() {
        let lib = MyLib::new("config").unwrap();
        let result = lib.process("");
        assert!(result.is_err());
    }

    #[test]
    fn test_display() {
        let lib = MyLib::new("test").unwrap();
        assert_eq!(format!("{}", lib), "MyLib(config: test)");
    }

    #[test]
    fn test_trait_implementation() {
        let lib = MyLib::new("config").unwrap();
        let processor: &dyn Processor = &lib;
        let result = processor.process("trait");
        assert!(result.is_ok());
    }
}
