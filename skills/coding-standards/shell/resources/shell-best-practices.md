# Shell Scripting Best Practices

Comprehensive guide to writing production-quality bash scripts.

## Table of Contents

- [Script Structure](#script-structure)
- [Error Handling](#error-handling)
- [Variable Management](#variable-management)
- [Functions](#functions)
- [Testing](#testing)
- [Security](#security)
- [Performance](#performance)
- [Portability](#portability)

## Script Structure

### Standard Template

```bash
#!/usr/bin/env bash
#
# Script description
# Author and version info
#

set -euo pipefail

# Constants
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="${0##*/}"

# Configuration
CONFIG_VAR="default"

# Functions (in logical order)
usage() { ... }
parse_arguments() { ... }
validate_dependencies() { ... }
main() { ... }

# Cleanup
cleanup() { ... }
trap cleanup EXIT

# Entry point
main "$@"
```

### Organization Principles

1. **Shebang First**: Always use `#!/usr/bin/env bash`
2. **Documentation**: Add header with description, author, usage
3. **Error Handling**: Set immediately after shebang
4. **Constants**: Define before variables
5. **Functions**: Group related functions together
6. **Main Last**: Entry point at bottom
7. **Size Limit**: Keep scripts under 500 lines; split larger ones

## Error Handling

### Essential Settings

```bash
# Exit on error
set -e

# Exit on undefined variable
set -u

# Exit on pipe failure
set -o pipefail

# Combine all three
set -euo pipefail
```

### Trap for Cleanup

```bash
cleanup() {
  local exit_code=$?
  # Cleanup logic here
  rm -f "${temp_files[@]}"
  exit "$exit_code"
}

trap cleanup EXIT INT TERM
trap 'echo "Error on line $LINENO"' ERR
```

### Error Messages

```bash
# Always write errors to stderr
echo "Error: something failed" >&2

# Include context
echo "Error: Failed to process $file at line $LINENO" >&2

# Use exit codes meaningfully
exit 1  # General error
exit 2  # Usage error
exit 3  # Dependency error
```

## Variable Management

### Naming Conventions

```bash
# Constants: UPPER_SNAKE_CASE
readonly MAX_RETRIES=3
readonly DEFAULT_TIMEOUT=30

# Global variables: lower_snake_case
script_dir="/path/to/dir"
user_input=""

# Local variables: always declare local
my_function() {
  local temp_var="value"
  local -r readonly_var="constant"
}

# Environment variables: UPPER_CASE (existing convention)
export PATH="/usr/local/bin:$PATH"
```

### Quoting Rules

```bash
# ALWAYS quote variables
echo "$variable"           # ✓ Correct
echo $variable             # ✗ Wrong

# Quote command substitution
current_dir="$(pwd)"       # ✓ Correct
current_dir=$(pwd)         # ✗ Wrong (but works)

# Arrays need special quoting
files=("file1" "file2")
for file in "${files[@]}"; do  # ✓ Preserves elements
  echo "$file"
done

# Don't quote arithmetic
count=$((count + 1))       # ✓ Correct
count="$((count + 1))"     # ✗ Unnecessary
```

### Default Values

```bash
# Parameter expansion for defaults
value="${1:-default}"              # Use default if $1 empty
value="${1-default}"               # Use default if $1 unset
required="${1:?Error: arg required}"  # Exit if empty

# Multiple fallbacks
config_file="${CONFIG_FILE:-${HOME}/.config/app.conf}"
```

## Functions

### Design Principles

```bash
#######################################
# Function description
# Globals:
#   GLOBAL_VAR - description
# Arguments:
#   $1 - description
#   $2 - description (optional)
# Returns:
#   0 on success, 1 on error
# Outputs:
#   Writes result to stdout
#   Writes errors to stderr
#######################################
my_function() {
  local arg1="$1"
  local arg2="${2:-default}"

  # Validate inputs
  if [[ -z "$arg1" ]]; then
    echo "Error: arg1 required" >&2
    return 1
  fi

  # Do work
  local result="processed $arg1"

  # Return value via stdout
  echo "$result"
  return 0
}
```

### Best Practices

1. **Single Responsibility**: One function, one job
2. **Local Variables**: Always use `local`
3. **Error Handling**: Return non-zero on error
4. **Documentation**: Use header comment format
5. **Output**: Results to stdout, errors to stderr
6. **Size Limit**: Keep under 50 lines

### Return Values

```bash
# Return via exit code
is_valid() {
  [[ "$1" =~ ^[0-9]+$ ]]
  # Returns 0 (true) or 1 (false)
}

# Return via stdout
get_value() {
  echo "result"
}

# Combine both
process() {
  local result="processed"
  echo "$result"
  return 0
}

# Usage
if is_valid "$input"; then
  result=$(get_value)
fi
```

## Testing

### Test Structure (Bats)

```bash
#!/usr/bin/env bats

setup() {
  export TEST_DIR="$(mktemp -d)"
}

teardown() {
  rm -rf "$TEST_DIR"
}

@test "function returns expected value" {
  source ./script.sh
  result=$(my_function "input")
  [ "$result" = "expected" ]
}

@test "function fails on invalid input" {
  source ./script.sh
  run my_function ""
  [ "$status" -ne 0 ]
}
```

### Testing Strategies

1. **Unit Tests**: Test individual functions
2. **Integration Tests**: Test script as whole
3. **Edge Cases**: Empty input, special chars, large input
4. **Error Cases**: Missing files, invalid input
5. **Mocking**: Mock external commands
6. **Coverage**: Aim for >80% coverage

### Test Helpers

```bash
# In tests
create_test_file() {
  local file="$1"
  local content="${2:-test}"
  echo "$content" > "$file"
}

assert_file_exists() {
  [ -f "$1" ]
}

assert_file_contains() {
  grep -q "$2" "$1"
}
```

## Security

### Input Validation

```bash
# Sanitize user input
sanitize() {
  local input="$1"
  # Remove dangerous characters
  input="${input//[^a-zA-Z0-9._-]/}"
  echo "$input"
}

# Validate paths
validate_path() {
  local path="$1"
  local allowed_dir="/home/user/allowed"

  # Resolve to absolute path
  path="$(realpath -m "$path")"

  # Check if within allowed directory
  if [[ "$path" != "$allowed_dir"* ]]; then
    echo "Error: Path outside allowed directory" >&2
    return 1
  fi

  echo "$path"
}
```

### Command Injection Prevention

```bash
# BAD: Never eval user input
eval "$user_input"  # ✗ DANGEROUS

# BAD: Unquoted variables in commands
ls $user_path  # ✗ Word splitting

# GOOD: Quote everything
ls "$user_path"  # ✓ Safe

# GOOD: Use arrays for complex commands
local -a cmd=(
  docker run
  --name "$container_name"
  --volume "$volume"
  "$image"
)
"${cmd[@]}"
```

### Secrets Management

```bash
# Never hardcode secrets
PASSWORD="secret123"  # ✗ WRONG

# Use environment variables
if [[ -z "$API_TOKEN" ]]; then
  echo "Error: API_TOKEN not set" >&2
  exit 1
fi

# Read from secure file
if [[ -f "$HOME/.secrets/token" ]]; then
  API_TOKEN="$(cat "$HOME/.secrets/token")"
fi

# Read password securely
read -rsp "Enter password: " password
echo >&2
```

### File Operations

```bash
# Use secure temp files
temp_file="$(mktemp)"
chmod 600 "$temp_file"

# Check before removing
if [[ -f "$file" ]]; then
  rm "$file"
fi

# Never remove with unquoted variables
rm -rf "$dir"/*  # ✓ Safe
rm -rf $dir/*    # ✗ Dangerous if $dir is empty
```

## Performance

### Optimization Strategies

```bash
# Use built-ins over external commands
# Slow
dirname "$file"
basename "$file"

# Fast
echo "${file%/*}"   # dirname
echo "${file##*/}"  # basename

# Avoid unnecessary subshells
# Slow
result=$(cat file | grep pattern)

# Fast
result=$(grep pattern file)

# Even faster
result=$(grep pattern < file)
```

### Parallel Processing

```bash
# Process in parallel
for file in *.txt; do
  process_file "$file" &
done
wait

# GNU parallel (if available)
find . -name "*.log" | parallel gzip

# Limit concurrent jobs
for file in *.txt; do
  while (($(jobs -r | wc -l) >= 4)); do
    sleep 0.1
  done
  process_file "$file" &
done
wait
```

### Caching

```bash
# Cache expensive operations
declare -A cache

cached_function() {
  local key="$1"

  if [[ -n "${cache[$key]:-}" ]]; then
    echo "${cache[$key]}"
    return 0
  fi

  local result
  result=$(expensive_operation "$key")
  cache[$key]="$result"

  echo "$result"
}
```

## Portability

### OS Detection

```bash
detect_os() {
  case "$(uname -s)" in
    Linux*)   echo "linux" ;;
    Darwin*)  echo "macos" ;;
    CYGWIN*)  echo "windows" ;;
    *)        echo "unknown" ;;
  esac
}

# Use OS-specific commands
get_cpu_count() {
  case "$(detect_os)" in
    linux)  nproc ;;
    macos)  sysctl -n hw.ncpu ;;
    *)      echo "1" ;;
  esac
}
```

### Portable Commands

```bash
# Use command -v instead of which
if command -v docker >/dev/null 2>&1; then
  echo "Docker found"
fi

# Portable sed
# macOS requires -i ''
sed_inplace() {
  if [[ "$(uname)" == "Darwin" ]]; then
    sed -i '' "$@"
  else
    sed -i "$@"
  fi
}

# Portable date
# GNU date: date -d "2 days ago"
# BSD date: date -v-2d
```

### Bash Version Compatibility

```bash
# Check bash version
require_bash_4() {
  if ((BASH_VERSINFO[0] < 4)); then
    echo "Error: Bash 4.0+ required" >&2
    exit 1
  fi
}

# Avoid bash 4+ features if targeting older systems
# Avoid: associative arrays, ${var^^}, ${var,,}
# Use: indexed arrays, tr for case conversion
```

## Common Patterns

### Argument Parsing

```bash
while [[ $# -gt 0 ]]; do
  case "$1" in
    -v|--verbose)
      verbose=true
      shift
      ;;
    -o|--output)
      output="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
    *)
      break
      ;;
  esac
done
```

### File Processing

```bash
# Read file line by line
while IFS= read -r line; do
  echo "Line: $line"
done < "$file"

# Process CSV
while IFS=, read -r col1 col2 col3; do
  echo "$col1 | $col2 | $col3"
done < data.csv

# Skip header
tail -n +2 data.csv | while IFS=, read -r col1 col2; do
  echo "$col1: $col2"
done
```

### Retry Logic

```bash
retry() {
  local max_attempts=3
  local attempt=1
  local delay=2

  while ((attempt <= max_attempts)); do
    if "$@"; then
      return 0
    fi

    if ((attempt < max_attempts)); then
      echo "Attempt $attempt failed, retrying..." >&2
      sleep "$delay"
      delay=$((delay * 2))
    fi

    ((attempt++))
  done

  return 1
}

# Usage
retry curl -f https://api.example.com/data
```

## Quick Reference

### ShellCheck Top Errors

- **SC2086**: Quote variables to prevent word splitting
- **SC2046**: Quote command substitution
- **SC2006**: Use `$()` instead of backticks
- **SC2155**: Declare and assign separately
- **SC2164**: Use `cd ... || exit` for safety

### Common Mistakes

```bash
# ✗ Wrong
if [ $var == "test" ]; then        # Unquoted variable
  cd $dir && ls                     # No error handling
  result=`command`                   # Backticks
fi

# ✓ Correct
if [[ "$var" == "test" ]]; then    # Quoted, [[
  cd "$dir" || exit 1               # Error handling
  result="$(command)"               # Modern syntax
fi
```

### Style Checklist

- [ ] Shebang: `#!/usr/bin/env bash`
- [ ] Error handling: `set -euo pipefail`
- [ ] Cleanup trap: `trap cleanup EXIT`
- [ ] Quote all variables: `"$var"`
- [ ] Use `[[` for tests
- [ ] Local variables in functions
- [ ] Meaningful exit codes
- [ ] Comments for complex logic
- [ ] ShellCheck passes with no warnings

---

*Last Updated: 2025-10-17*
