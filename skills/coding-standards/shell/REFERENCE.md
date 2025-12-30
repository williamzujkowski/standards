# Shell Scripting Standards - Complete Reference

This document contains comprehensive examples, detailed configurations, and production-ready templates for shell scripting. For quick reference patterns, see [SKILL.md](./SKILL.md).

## Table of Contents

- [Complete Script Template](#complete-script-template)
- [Advanced Argument Parsing](#advanced-argument-parsing)
- [Comprehensive Logging System](#comprehensive-logging-system)
- [Input Validation Functions](#input-validation-functions)
- [Dependency Management](#dependency-management)
- [Testing with Bats](#testing-with-bats)
- [Security Best Practices](#security-best-practices)
- [Performance Optimization](#performance-optimization)
- [Debugging Techniques](#debugging-techniques)
- [Working with JSON](#working-with-json)
- [Working with APIs](#working-with-apis)
- [Configuration Management](#configuration-management)
- [Signal Handling](#signal-handling)
- [Process Management](#process-management)
- [Cross-Platform Compatibility](#cross-platform-compatibility)

---

## Complete Script Template

```bash
#!/usr/bin/env bash
#
# Script Name: backup-manager.sh
# Description: Manages automated backups with rotation
# Author: Your Name
# Version: 1.0.0
# Dependencies: rsync, gzip
#
# Usage: backup-manager.sh [-v] [-d DAYS] SOURCE DEST
#

# Strict error handling
set -euo pipefail

# Script metadata
readonly SCRIPT_NAME="${0##*/}"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly VERSION="1.0.0"

# Global configuration
readonly DEFAULT_RETENTION_DAYS=7
readonly LOG_FILE="/var/log/${SCRIPT_NAME%.sh}.log"

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_USAGE=2

# Color constants
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m'

# Main function at bottom
main() {
  parse_arguments "$@"
  validate_dependencies
  perform_backup
  rotate_old_backups
  log_info "Backup completed successfully"
}

# Run main if executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
```

---

## Advanced Argument Parsing

Complete argument parsing with long options support:

```bash
parse_arguments() {
  local verbose=false
  local output=""
  local retention_days=$DEFAULT_RETENTION_DAYS
  local dry_run=false

  # Parse options
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -v|--verbose)
        verbose=true
        log_level=$LOG_LEVEL_DEBUG
        shift
        ;;
      -o|--output)
        if [[ -z "${2:-}" ]]; then
          log_error "Option $1 requires an argument"
          usage
          exit "$EXIT_USAGE"
        fi
        output="$2"
        shift 2
        ;;
      -d|--days)
        if [[ ! "${2:-}" =~ ^[0-9]+$ ]]; then
          log_error "Option $1 requires a numeric argument"
          exit "$EXIT_USAGE"
        fi
        retention_days="$2"
        shift 2
        ;;
      -n|--dry-run)
        dry_run=true
        shift
        ;;
      -h|--help)
        usage
        exit "$EXIT_SUCCESS"
        ;;
      --version)
        echo "$SCRIPT_NAME version $VERSION"
        exit "$EXIT_SUCCESS"
        ;;
      --)
        shift
        break
        ;;
      -*)
        log_error "Unknown option: $1"
        usage
        exit "$EXIT_USAGE"
        ;;
      *)
        break
        ;;
    esac
  done

  # Validate positional arguments
  if [[ $# -lt 2 ]]; then
    log_error "Missing required arguments"
    usage
    exit "$EXIT_USAGE"
  fi

  readonly SOURCE="$1"
  readonly DEST="$2"
  readonly VERBOSE=$verbose
  readonly OUTPUT=$output
  readonly RETENTION_DAYS=$retention_days
  readonly DRY_RUN=$dry_run
}

usage() {
  cat << USAGE
${SCRIPT_NAME} - Automated backup manager

Usage:
  ${SCRIPT_NAME} [OPTIONS] SOURCE DEST

Arguments:
  SOURCE              Source directory to backup
  DEST                Destination directory for backups

Options:
  -v, --verbose       Enable verbose output
  -o, --output FILE   Write results to FILE
  -d, --days DAYS     Retention period (default: $DEFAULT_RETENTION_DAYS)
  -n, --dry-run       Show what would be done without doing it
  -h, --help          Show this help message
  --version           Show version information

Examples:
  ${SCRIPT_NAME} /home/user /backup
  ${SCRIPT_NAME} -v -d 14 /var/www /backup/www
  ${SCRIPT_NAME} --dry-run /data /mnt/backup

Exit Codes:
  0  Success
  1  General error
  2  Usage error

For more information, see the project documentation.
USAGE
}
```

---

## Comprehensive Logging System

```bash
# Logging levels
readonly LOG_LEVEL_DEBUG=0
readonly LOG_LEVEL_INFO=1
readonly LOG_LEVEL_WARN=2
readonly LOG_LEVEL_ERROR=3

# Current log level (set via -v flag)
log_level=$LOG_LEVEL_INFO

log_message() {
  local level=$1
  local color=$2
  local prefix=$3
  shift 3

  if ((level >= log_level)); then
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

    # Console output with color
    echo -e "${color}[${prefix}]${NC} $*" >&2

    # File output without color
    if [[ -w "$(dirname "$LOG_FILE")" ]]; then
      echo "[${timestamp}] [${prefix}] $*" >> "$LOG_FILE"
    fi
  fi
}

log_debug() {
  log_message "$LOG_LEVEL_DEBUG" "$BLUE" "DEBUG" "$@"
}

log_info() {
  log_message "$LOG_LEVEL_INFO" "$GREEN" "INFO" "$@"
}

log_warn() {
  log_message "$LOG_LEVEL_WARN" "$YELLOW" "WARN" "$@"
}

log_error() {
  log_message "$LOG_LEVEL_ERROR" "$RED" "ERROR" "$@"
}

# Usage
log_debug "Checking configuration..."
log_info "Starting backup process"
log_warn "Disk space is low"
log_error "Failed to connect to server"
```

---

## Input Validation Functions

### File and Directory Validation

```bash
# Validate file path
validate_file() {
  local file="$1"
  local description="${2:-File}"

  if [[ -z "$file" ]]; then
    log_error "$description path is empty"
    return 1
  fi

  if [[ ! -f "$file" ]]; then
    log_error "$description does not exist: $file"
    return 1
  fi

  if [[ ! -r "$file" ]]; then
    log_error "$description is not readable: $file"
    return 1
  fi

  return 0
}

# Validate directory
validate_directory() {
  local dir="$1"
  local description="${2:-Directory}"
  local must_be_writable="${3:-false}"

  if [[ -z "$dir" ]]; then
    log_error "$description path is empty"
    return 1
  fi

  if [[ ! -d "$dir" ]]; then
    log_error "$description does not exist: $dir"
    return 1
  fi

  if [[ "$must_be_writable" == "true" && ! -w "$dir" ]]; then
    log_error "$description is not writable: $dir"
    return 1
  fi

  return 0
}
```

### Numeric and Email Validation

```bash
# Validate numeric input
validate_number() {
  local value="$1"
  local description="${2:-Value}"
  local min="${3:-}"
  local max="${4:-}"

  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    log_error "$description must be a number: $value"
    return 1
  fi

  if [[ -n "$min" && "$value" -lt "$min" ]]; then
    log_error "$description must be >= $min: $value"
    return 1
  fi

  if [[ -n "$max" && "$value" -gt "$max" ]]; then
    log_error "$description must be <= $max: $value"
    return 1
  fi

  return 0
}

# Validate email
validate_email() {
  local email="$1"
  local regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

  if [[ ! "$email" =~ $regex ]]; then
    log_error "Invalid email format: $email"
    return 1
  fi

  return 0
}

# Sanitize user input
sanitize_input() {
  local input="$1"
  # Remove potentially dangerous characters
  input="${input//[^a-zA-Z0-9._-]/}"
  echo "$input"
}
```

---

## Dependency Management

```bash
# Check for required commands
validate_dependencies() {
  local missing_deps=()

  local required_commands=(
    rsync
    gzip
    tar
    date
    mktemp
  )

  for cmd in "${required_commands[@]}"; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      missing_deps+=("$cmd")
    fi
  done

  if ((${#missing_deps[@]} > 0)); then
    log_error "Missing required commands: ${missing_deps[*]}"
    log_info "Install with: apt-get install ${missing_deps[*]}"
    exit "$EXIT_ERROR"
  fi

  # Check versions if needed
  local rsync_version
  rsync_version="$(rsync --version | head -n1 | grep -oP '\d+\.\d+\.\d+')"

  if ! version_gt "$rsync_version" "3.0.0"; then
    log_error "rsync version must be >= 3.0.0 (found: $rsync_version)"
    exit "$EXIT_ERROR"
  fi
}

# Version comparison
version_gt() {
  local version1="$1"
  local version2="$2"
  printf '%s\n%s\n' "$version1" "$version2" | sort -V -C
  return $?
}

# Optional dependency handling
check_optional_tool() {
  local tool="$1"
  local fallback="$2"

  if command -v "$tool" >/dev/null 2>&1; then
    echo "$tool"
  else
    log_warn "$tool not found, using $fallback"
    echo "$fallback"
  fi
}

# Usage
compressor=$(check_optional_tool "pigz" "gzip")
```

---

## Testing with Bats

Complete Bats testing example:

```bash
# test-backup.bats
#!/usr/bin/env bats

# Setup function runs before each test
setup() {
  # Create test directory
  TEST_DIR="$(mktemp -d)"
  SOURCE_DIR="$TEST_DIR/source"
  DEST_DIR="$TEST_DIR/dest"

  mkdir -p "$SOURCE_DIR" "$DEST_DIR"
  echo "test content" > "$SOURCE_DIR/file.txt"

  # Source the script to test
  source ./backup-manager.sh
}

# Teardown runs after each test
teardown() {
  rm -rf "$TEST_DIR"
}

@test "validate_file succeeds for existing file" {
  touch "$TEST_DIR/test.txt"
  run validate_file "$TEST_DIR/test.txt"
  [ "$status" -eq 0 ]
}

@test "validate_file fails for missing file" {
  run validate_file "$TEST_DIR/missing.txt"
  [ "$status" -eq 1 ]
  [[ "$output" =~ "does not exist" ]]
}

@test "perform_backup creates backup directory" {
  run perform_backup "$SOURCE_DIR" "$DEST_DIR"
  [ "$status" -eq 0 ]
  [ -d "$DEST_DIR/backup_"* ]
}

@test "perform_backup preserves file content" {
  perform_backup "$SOURCE_DIR" "$DEST_DIR"

  local backup_dir
  backup_dir="$(find "$DEST_DIR" -maxdepth 1 -type d -name 'backup_*')"

  [ -f "$backup_dir/file.txt" ]
  [ "$(cat "$backup_dir/file.txt")" = "test content" ]
}

@test "parse_arguments handles verbose flag" {
  run parse_arguments -v "$SOURCE_DIR" "$DEST_DIR"
  [ "$status" -eq 0 ]
  [ "$VERBOSE" = "true" ]
}

@test "parse_arguments requires source and dest" {
  run parse_arguments
  [ "$status" -eq 2 ]
}

# Helper function for tests
create_test_file() {
  local file="$1"
  local content="${2:-test content}"
  echo "$content" > "$file"
}

@test "helper functions work" {
  create_test_file "$TEST_DIR/helper.txt" "custom content"
  [ -f "$TEST_DIR/helper.txt" ]
  [ "$(cat "$TEST_DIR/helper.txt")" = "custom content" ]
}
```

---

## Security Best Practices

### Complete Security Patterns

```bash
# 1. Never eval user input
bad_eval() {
  eval "$user_input"  # NEVER DO THIS
}

good_alternative() {
  case "$user_input" in
    start) start_service ;;
    stop) stop_service ;;
    *) log_error "Invalid command" ;;
  esac
}

# 2. Sanitize paths
sanitize_path() {
  local path="$1"

  # Remove .. and . components
  path="$(realpath -m "$path")"

  # Ensure path is within allowed directory
  local allowed_dir="/home/user/allowed"
  if [[ "$path" != "$allowed_dir"* ]]; then
    log_error "Path outside allowed directory: $path"
    return 1
  fi

  echo "$path"
}

# 3. Secure temporary files
create_secure_temp() {
  local temp_file
  temp_file="$(mktemp)" || {
    log_error "Failed to create temp file"
    return 1
  }

  # Set restrictive permissions
  chmod 600 "$temp_file"

  echo "$temp_file"
}

# 4. Avoid command injection
execute_safely() {
  local file="$1"

  # Bad: subject to injection
  # ls "$file"*.txt

  # Good: use arrays
  local -a files
  mapfile -t files < <(find . -name "${file}*.txt")

  for f in "${files[@]}"; do
    echo "$f"
  done
}

# 5. Handle sudo carefully
run_as_root() {
  if [[ $EUID -ne 0 ]]; then
    log_error "This function must be run as root"
    return 1
  fi

  # Drop privileges when possible
  sudo -u nobody some_command
}

# 6. Validate environment variables
validate_env() {
  # Set safe defaults
  : "${HOME:=/home/user}"
  : "${PATH:=/usr/local/bin:/usr/bin:/bin}"

  # Validate PATH doesn't include current directory
  if [[ "$PATH" =~ (^|:)\.(:|$) ]]; then
    log_error "PATH contains current directory"
    return 1
  fi
}

# 7. Secure password handling
read_password() {
  local password

  # Don't echo password
  read -rsp "Enter password: " password
  echo >&2

  # Use password
  some_command <<< "$password"

  # Clear password variable
  unset password
}

# 8. File descriptor leaks
prevent_fd_leak() {
  {
    # Operations here
    echo "data"
  } 3>&-  # Close FD 3 when done
}
```

---

## Performance Optimization

```bash
# 1. Use built-ins instead of external commands
# Slow
slow_dirname() {
  dirname "$file"  # Spawns process
}

# Fast
fast_dirname() {
  echo "${file%/*}"  # Built-in parameter expansion
}

# 2. Avoid unnecessary subshells
# Slow
count=$(cat file.txt | wc -l)

# Fast
count=$(wc -l < file.txt)

# 3. Use array operations
process_array() {
  local -a items=("$@")

  # Slow: loop with external commands
  # for item in "${items[@]}"; do
  #   result=$(echo "$item" | tr '[:lower:]' '[:upper:]')
  # done

  # Fast: bash built-ins
  for item in "${items[@]}"; do
    result="${item^^}"  # Bash 4+
  done
}

# 4. Batch operations
# Slow: multiple file operations
for file in *.txt; do
  cp "$file" /dest/
done

# Fast: single operation
cp *.txt /dest/

# 5. Use parallel processing (GNU parallel)
parallel_process() {
  # Process files in parallel
  find . -name "*.log" | parallel -j4 gzip

  # Or with bash
  for file in *.log; do
    gzip "$file" &
  done
  wait  # Wait for all background jobs
}
```

---

## Debugging Techniques

```bash
# Enable debug mode
set -x  # Print commands before executing
set -v  # Print script lines as read

# Disable debug mode
set +x
set +v

# Debug specific section
{
  set -x
  # Debug this code
  some_command
  another_command
  set +x
}

# Custom debug function
debug() {
  if [[ "${DEBUG:-false}" == "true" ]]; then
    echo "[DEBUG] $*" >&2
  fi
}

# Usage: DEBUG=true ./script.sh
debug "Current value: $variable"

# Trace function calls
trace() {
  echo "[TRACE] Entering ${FUNCNAME[1]}" >&2
}

my_function() {
  trace
  # function body
}

# Check syntax without running
bash -n script.sh

# Use shellcheck for static analysis
shellcheck script.sh

# Profile script execution time
PS4='+ $(date "+%s.%N ($LINENO) ")' bash -x script.sh
```

---

## Working with JSON

```bash
# Parse JSON with jq
parse_json() {
  local json_file="$1"

  # Extract value
  local name
  name=$(jq -r '.name' "$json_file")

  # Extract array
  local -a items
  mapfile -t items < <(jq -r '.items[]' "$json_file")

  # Complex query
  local version
  version=$(jq -r '.packages[] | select(.name=="mypackage") | .version' "$json_file")

  echo "Name: $name"
  echo "Items: ${items[*]}"
  echo "Version: $version"
}

# Generate JSON
generate_json() {
  local name="$1"
  local version="$2"

  jq -n \
    --arg name "$name" \
    --arg version "$version" \
    '{
      name: $name,
      version: $version,
      timestamp: now | todate
    }'
}

# Fallback without jq (basic parsing)
parse_json_basic() {
  local json="$1"
  local key="$2"

  # Extract simple string value
  echo "$json" | grep -o "\"$key\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" | cut -d'"' -f4
}
```

---

## Working with APIs

```bash
# Make HTTP requests with curl
api_request() {
  local method="$1"
  local endpoint="$2"
  local data="${3:-}"

  local base_url="https://api.example.com"
  local token="$API_TOKEN"

  local -a curl_args=(
    -X "$method"
    -H "Authorization: Bearer $token"
    -H "Content-Type: application/json"
    -H "Accept: application/json"
    --silent
    --show-error
    --fail
  )

  if [[ -n "$data" ]]; then
    curl_args+=(-d "$data")
  fi

  if ! response=$(curl "${curl_args[@]}" "$base_url$endpoint"); then
    log_error "API request failed: $method $endpoint"
    return 1
  fi

  echo "$response"
}

# Retry logic for API calls
api_request_with_retry() {
  local max_attempts=3
  local attempt=1
  local backoff=2

  while ((attempt <= max_attempts)); do
    if response=$(api_request "$@"); then
      echo "$response"
      return 0
    fi

    if ((attempt < max_attempts)); then
      log_warn "Request failed, retrying in ${backoff}s..."
      sleep "$backoff"
      backoff=$((backoff * 2))
    fi

    ((attempt++))
  done

  log_error "API request failed after $max_attempts attempts"
  return 1
}

# Upload file
upload_file() {
  local file="$1"
  local endpoint="$2"

  curl -X POST \
    -H "Authorization: Bearer $API_TOKEN" \
    -F "file=@$file" \
    "https://api.example.com$endpoint"
}
```

---

## Configuration Management

```bash
# Load configuration from file
load_config() {
  local config_file="${1:-config.conf}"

  if [[ ! -f "$config_file" ]]; then
    log_error "Config file not found: $config_file"
    return 1
  fi

  # Source config file in subshell for safety
  if ! (
    # Validate config file first
    bash -n "$config_file" || exit 1
    source "$config_file"
  ); then
    log_error "Invalid config file: $config_file"
    return 1
  fi

  # Now source it for real
  source "$config_file"
}

# Parse INI-style config
parse_ini() {
  local file="$1"
  local section="$2"
  local key="$3"

  # Extract value from [section]
  awk -F= -v section="$section" -v key="$key" '
    /^\[.*\]$/ { current_section = substr($0, 2, length($0)-2) }
    current_section == section && $1 ~ "^"key"$" { print $2 }
  ' "$file" | tr -d ' '
}

# Environment-specific config
load_env_config() {
  local env="${ENV:-development}"
  local config_dir="${CONFIG_DIR:-./config}"

  # Load base config
  if [[ -f "$config_dir/base.conf" ]]; then
    source "$config_dir/base.conf"
  fi

  # Override with environment-specific config
  if [[ -f "$config_dir/${env}.conf" ]]; then
    source "$config_dir/${env}.conf"
  fi

  log_info "Loaded configuration for environment: $env"
}
```

---

## Signal Handling

```bash
# Handle signals gracefully
setup_signal_handlers() {
  trap 'handle_sigint' INT
  trap 'handle_sigterm' TERM
  trap 'handle_sighup' HUP
}

handle_sigint() {
  log_info "Received SIGINT, shutting down gracefully..."
  cleanup
  exit 130
}

handle_sigterm() {
  log_info "Received SIGTERM, shutting down..."
  cleanup
  exit 143
}

handle_sighup() {
  log_info "Received SIGHUP, reloading configuration..."
  load_config
}

# Ignore signals during critical section
critical_section() {
  trap '' INT TERM  # Ignore signals

  # Critical operations
  important_operation

  trap - INT TERM  # Restore handlers
}
```

---

## Process Management

```bash
# Check if process is running
is_running() {
  local pid="$1"
  kill -0 "$pid" 2>/dev/null
}

# Wait for process with timeout
wait_for_process() {
  local pid="$1"
  local timeout="${2:-30}"
  local elapsed=0

  while is_running "$pid"; do
    if ((elapsed >= timeout)); then
      log_error "Timeout waiting for process $pid"
      return 1
    fi

    sleep 1
    ((elapsed++))
  done

  return 0
}

# Run command in background with monitoring
run_background() {
  local -a cmd=("$@")

  # Start process
  "${cmd[@]}" &
  local pid=$!

  # Store PID for cleanup
  echo "$pid" >> "$PID_FILE"

  log_info "Started background process: $pid"
  echo "$pid"
}

# Kill process tree
kill_tree() {
  local pid="$1"
  local signal="${2:-TERM}"

  # Kill all child processes
  pkill -"$signal" -P "$pid"

  # Kill parent process
  kill -"$signal" "$pid"
}
```

---

## Cross-Platform Compatibility

```bash
# Detect OS
detect_os() {
  case "$(uname -s)" in
    Linux*)   echo "linux" ;;
    Darwin*)  echo "macos" ;;
    CYGWIN*)  echo "windows" ;;
    MINGW*)   echo "windows" ;;
    *)        echo "unknown" ;;
  esac
}

# OS-specific commands
get_cpu_count() {
  local os
  os=$(detect_os)

  case "$os" in
    linux)
      nproc
      ;;
    macos)
      sysctl -n hw.ncpu
      ;;
    *)
      echo "1"
      ;;
  esac
}

# Portable sed command
portable_sed() {
  local os
  os=$(detect_os)

  if [[ "$os" == "macos" ]]; then
    sed -i '' "$@"  # macOS requires empty string
  else
    sed -i "$@"     # Linux
  fi
}

# Check bash version
require_bash_version() {
  local required_version="$1"

  if ! version_gt "$BASH_VERSION" "$required_version"; then
    log_error "Bash version $required_version or higher required (found: $BASH_VERSION)"
    exit 1
  fi
}
```

---

## Function Documentation Template

```bash
#######################################
# Performs incremental backup with rsync
# Globals:
#   BACKUP_DIR
#   LOG_FILE
# Arguments:
#   $1 - Source directory
#   $2 - Destination directory
# Returns:
#   0 on success, 1 on error
# Outputs:
#   Writes progress to stdout
#   Writes errors to stderr
#######################################
perform_backup() {
  local source="$1"
  local dest="$2"
  local timestamp
  timestamp="$(date '+%Y%m%d_%H%M%S')"
  local backup_path="${dest}/backup_${timestamp}"

  # Validate inputs
  if [[ ! -d "$source" ]]; then
    log_error "Source directory does not exist: $source"
    return 1
  fi

  if [[ ! -w "$dest" ]]; then
    log_error "Destination is not writable: $dest"
    return 1
  fi

  # Create backup directory
  if ! mkdir -p "$backup_path"; then
    log_error "Failed to create backup directory"
    return 1
  fi

  # Perform backup
  log_info "Backing up $source to $backup_path"

  if rsync -av --delete \
      --exclude='.git' \
      --exclude='node_modules' \
      "$source/" "$backup_path/"; then
    log_info "Backup completed: $backup_path"
    return 0
  else
    log_error "Backup failed"
    return 1
  fi
}
```

---

## External Resources

### Official Documentation

- [Bash Manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck Wiki](https://github.com/koalaman/shellcheck/wiki)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)

### Style Guides

- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Defensive Bash Programming](http://www.kfirlavi.com/blog/2012/11/14/defensive-bash-programming/)

### Testing Frameworks

- [Bats-core](https://github.com/bats-core/bats-core)
- [shUnit2](https://github.com/kward/shunit2)
- [ShellSpec](https://shellspec.info/)

### Static Analysis

- [ShellCheck](https://github.com/koalaman/shellcheck)
- [shfmt](https://github.com/mvdan/sh)

### Community Resources

- [Bash Pitfalls](https://mywiki.wooledge.org/BashPitfalls)
- [Bash FAQ](https://mywiki.wooledge.org/BashFAQ)
- [Process Substitution](https://mywiki.wooledge.org/ProcessSubstitution)

### Books

- *"Classic Shell Scripting"* by Arnold Robbins & Nelson H.F. Beebe
- *"Bash Cookbook"* by Carl Albing & JP Vossen
- *"Learning the bash Shell"* by Cameron Newham

---

*Last Updated: 2025-12-30*
*Reference Version: 1.0.0*
