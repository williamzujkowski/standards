//! Binary crate template with error handling
//!
//! Demonstrates:
//! - CLI argument parsing with clap
//! - Structured logging with tracing
//! - Error handling with anyhow
//! - Clean main function

use anyhow::{Context, Result};
use clap::Parser;
use tracing::{info, warn, error};
use tracing_subscriber;

/// CLI application
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Input file path
    #[arg(short, long)]
    input: String,
    
    /// Output file path
    #[arg(short, long)]
    output: Option<String>,
    
    /// Verbose mode
    #[arg(short, long)]
    verbose: bool,
    
    /// Configuration file
    #[arg(short, long, default_value = "config.toml")]
    config: String,
}

/// Application configuration
#[derive(Debug)]
struct Config {
    input: String,
    output: Option<String>,
    config_path: String,
}

impl Config {
    fn from_args(args: Args) -> Self {
        Self {
            input: args.input,
            output: args.output,
            config_path: args.config,
        }
    }
}

/// Main application logic
struct App {
    config: Config,
}

impl App {
    fn new(config: Config) -> Self {
        Self { config }
    }
    
    /// Run the application
    fn run(&self) -> Result<()> {
        info!("Starting application");
        
        // Read input
        let input = self.read_input()
            .context("Failed to read input file")?;
        
        info!("Read {} bytes from input", input.len());
        
        // Process data
        let output = self.process(&input)
            .context("Failed to process data")?;
        
        // Write output
        self.write_output(&output)
            .context("Failed to write output")?;
        
        info!("Application completed successfully");
        Ok(())
    }
    
    fn read_input(&self) -> Result<String> {
        info!("Reading from: {}", self.config.input);
        std::fs::read_to_string(&self.config.input)
            .context(format!("Cannot read file: {}", self.config.input))
    }
    
    fn process(&self, input: &str) -> Result<String> {
        info!("Processing input");
        
        if input.is_empty() {
            warn!("Input is empty, returning unchanged");
            return Ok(input.to_string());
        }
        
        // Example processing: convert to uppercase
        let output = input.to_uppercase();
        
        info!("Processed {} bytes", output.len());
        Ok(output)
    }
    
    fn write_output(&self, data: &str) -> Result<()> {
        match &self.config.output {
            Some(path) => {
                info!("Writing to: {}", path);
                std::fs::write(path, data)
                    .context(format!("Cannot write file: {}", path))?;
            }
            None => {
                info!("Writing to stdout");
                println!("{}", data);
            }
        }
        Ok(())
    }
}

fn main() -> Result<()> {
    // Parse command line arguments
    let args = Args::parse();
    
    // Setup logging
    let log_level = if args.verbose {
        tracing::Level::DEBUG
    } else {
        tracing::Level::INFO
    };
    
    tracing_subscriber::fmt()
        .with_max_level(log_level)
        .with_target(false)
        .with_thread_ids(false)
        .with_file(true)
        .with_line_number(true)
        .init();
    
    info!("Application started");
    
    // Create configuration
    let config = Config::from_args(args);
    
    // Run application
    let app = App::new(config);
    app.run().context("Application execution failed")?;
    
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use tempfile::NamedTempFile;
    use std::io::Write;
    
    #[test]
    fn test_process_empty_input() {
        let config = Config {
            input: "test.txt".to_string(),
            output: None,
            config_path: "config.toml".to_string(),
        };
        let app = App::new(config);
        
        let result = app.process("");
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "");
    }
    
    #[test]
    fn test_process_uppercase() {
        let config = Config {
            input: "test.txt".to_string(),
            output: None,
            config_path: "config.toml".to_string(),
        };
        let app = App::new(config);
        
        let result = app.process("hello world");
        assert!(result.is_ok());
        assert_eq!(result.unwrap(), "HELLO WORLD");
    }
    
    #[test]
    fn test_read_write_integration() -> Result<()> {
        // Create temporary input file
        let mut input_file = NamedTempFile::new()?;
        writeln!(input_file, "test content")?;
        
        // Create temporary output file
        let output_file = NamedTempFile::new()?;
        
        let config = Config {
            input: input_file.path().to_string_lossy().to_string(),
            output: Some(output_file.path().to_string_lossy().to_string()),
            config_path: "config.toml".to_string(),
        };
        
        let app = App::new(config);
        let result = app.run();
        
        assert!(result.is_ok());
        
        // Verify output
        let output = std::fs::read_to_string(output_file.path())?;
        assert_eq!(output, "TEST CONTENT\n");
        
        Ok(())
    }
}
