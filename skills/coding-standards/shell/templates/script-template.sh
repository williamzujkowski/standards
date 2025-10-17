#!/usr/bin/env bash
#
# Script Name: script-template.sh
# Description: Production-ready bash script template with best practices
# Author: Your Name <your.email@example.com>
# Version: 1.0.0
# License: MIT
#
# Usage: script-template.sh [OPTIONS] ARGUMENTS
#
# Dependencies:
#   - bash >= 4.0
#   - Standard Unix utilities (grep, sed, awk)
#

#######################################
# STRICT ERROR HANDLING
#######################################

set -euo pipefail
IFS=$'\n\t'

#######################################
# SCRIPT METADATA
#######################################

readonly SCRIPT_NAME="${0##*/}"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_VERSION="1.0.0"
readonly SCRIPT_AUTHOR="Your Name"

#######################################
# CONFIGURATION
#######################################

# Exit codes
readonly EXIT_SUCCESS=0
readonly EXIT_ERROR=1
readonly EXIT_USAGE=2
readonly EXIT_DEPENDENCY=3

# Defaults
readonly DEFAULT_LOG_LEVEL="INFO"
readonly DEFAULT_TIMEOUT=30

# Colors
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly MAGENTA='\033[0;35m'
readonly CYAN='\033[0;36m'
readonly NC='\033[0m' # No Color

# Global variables (set by parse_arguments)
VERBOSE=false
DRY_RUN=false
LOG_LEVEL="$DEFAULT_LOG_LEVEL"
LOG_FILE=""
CONFIG_FILE=""

#######################################
# LOGGING
#######################################

# Log levels
readonly LOG_LEVEL_DEBUG=0
readonly LOG_LEVEL_INFO=1
readonly LOG_LEVEL_WARN=2
readonly LOG_LEVEL_ERROR=3

# Current log level number
log_level_num=$LOG_LEVEL_INFO

#######################################
# Log a message with level and color
# Globals:
#   log_level_num
#   LOG_FILE
# Arguments:
#   $1 - Level number
#   $2 - Color code
#   $3 - Level name
#   $@ - Message
#######################################
log_message() {
  local level=$1
  local color=$2
  local prefix=$3
  shift 3

  if ((level >= log_level_num)); then
    local timestamp
    timestamp="$(date '+%Y-%m-%d %H:%M:%S')"

    # Console output with color
    echo -e "${color}[${prefix}]${NC} $*" >&2

    # File output without color
    if [[ -n "$LOG_FILE" && -w "$(dirname "$LOG_FILE")" ]]; then
      echo "[${timestamp}] [${prefix}] $*" >> "$LOG_FILE"
    fi
  fi
}

log_debug() { log_message "$LOG_LEVEL_DEBUG" "$BLUE" "DEBUG" "$@"; }
log_info() { log_message "$LOG_LEVEL_INFO" "$GREEN" "INFO" "$@"; }
log_warn() { log_message "$LOG_LEVEL_WARN" "$YELLOW" "WARN" "$@"; }
log_error() { log_message "$LOG_LEVEL_ERROR" "$RED" "ERROR" "$@"; }

#######################################
# CLEANUP AND ERROR HANDLING
#######################################

# Temporary files tracking
declare -a TEMP_FILES=()
declare -a TEMP_DIRS=()

#######################################
# Cleanup function called on exit
# Globals:
#   TEMP_FILES
#   TEMP_DIRS
#######################################
cleanup() {
  local exit_code=$?

  # Remove temporary files
  for file in "${TEMP_FILES[@]}"; do
    if [[ -f "$file" ]]; then
      rm -f "$file"
      log_debug "Removed temp file: $file"
    fi
  done

  # Remove temporary directories
  for dir in "${TEMP_DIRS[@]}"; do
    if [[ -d "$dir" ]]; then
      rm -rf "$dir"
      log_debug "Removed temp dir: $dir"
    fi
  done

  if ((exit_code != 0)); then
    log_error "Script exited with code: $exit_code"
  fi

  exit "$exit_code"
}

#######################################
# Error handler for trapped errors
# Arguments:
#   $1 - Line number where error occurred
#   $2 - Error code
#######################################
error_handler() {
  local line_no=$1
  local error_code=$2
  log_error "Error on line $line_no: exit code $error_code"
}

# Set up traps
trap cleanup EXIT INT TERM
trap 'error_handler ${LINENO} $?' ERR

#######################################
# UTILITY FUNCTIONS
#######################################

#######################################
# Check if command exists
# Arguments:
#   $1 - Command name
# Returns:
#   0 if command exists, 1 otherwise
#######################################
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

#######################################
# Create a secure temporary file
# Returns:
#   Path to temporary file
#######################################
create_temp_file() {
  local temp_file
  temp_file="$(mktemp)" || {
    log_error "Failed to create temporary file"
    exit "$EXIT_ERROR"
  }
  chmod 600 "$temp_file"
  TEMP_FILES+=("$temp_file")
  echo "$temp_file"
}

#######################################
# Create a temporary directory
# Returns:
#   Path to temporary directory
#######################################
create_temp_dir() {
  local temp_dir
  temp_dir="$(mktemp -d)" || {
    log_error "Failed to create temporary directory"
    exit "$EXIT_ERROR"
  }
  chmod 700 "$temp_dir"
  TEMP_DIRS+=("$temp_dir")
  echo "$temp_dir"
}

#######################################
# Validate file exists and is readable
# Arguments:
#   $1 - File path
#   $2 - Description (optional)
# Returns:
#   0 on success, 1 on failure
#######################################
validate_file() {
  local file="$1"
  local desc="${2:-File}"

  if [[ -z "$file" ]]; then
    log_error "$desc path is empty"
    return 1
  fi

  if [[ ! -f "$file" ]]; then
    log_error "$desc does not exist: $file"
    return 1
  fi

  if [[ ! -r "$file" ]]; then
    log_error "$desc is not readable: $file"
    return 1
  fi

  return 0
}

#######################################
# Validate directory exists
# Arguments:
#   $1 - Directory path
#   $2 - Description (optional)
#   $3 - Must be writable (true/false, optional)
# Returns:
#   0 on success, 1 on failure
#######################################
validate_directory() {
  local dir="$1"
  local desc="${2:-Directory}"
  local writable="${3:-false}"

  if [[ -z "$dir" ]]; then
    log_error "$desc path is empty"
    return 1
  fi

  if [[ ! -d "$dir" ]]; then
    log_error "$desc does not exist: $dir"
    return 1
  fi

  if [[ "$writable" == "true" && ! -w "$dir" ]]; then
    log_error "$desc is not writable: $dir"
    return 1
  fi

  return 0
}

#######################################
# Ask user for confirmation
# Arguments:
#   $1 - Prompt message (optional)
# Returns:
#   0 if confirmed, 1 otherwise
#######################################
confirm() {
  local prompt="${1:-Are you sure?}"
  local response

  read -rp "$prompt [y/N] " response
  [[ "$response" =~ ^[Yy]$ ]]
}

#######################################
# DEPENDENCY CHECKING
#######################################

#######################################
# Validate all required dependencies
# Returns:
#   0 on success, exits on failure
#######################################
validate_dependencies() {
  local -a missing_deps=()

  local -a required_commands=(
    grep
    sed
    awk
  )

  for cmd in "${required_commands[@]}"; do
    if ! command_exists "$cmd"; then
      missing_deps+=("$cmd")
    fi
  done

  if ((${#missing_deps[@]} > 0)); then
    log_error "Missing required commands: ${missing_deps[*]}"
    exit "$EXIT_DEPENDENCY"
  fi

  log_debug "All dependencies satisfied"
}

#######################################
# ARGUMENT PARSING
#######################################

#######################################
# Display usage information
#######################################
usage() {
  cat << USAGE
${SCRIPT_NAME} - Script description here

Usage:
  ${SCRIPT_NAME} [OPTIONS] ARGUMENTS

Options:
  -v, --verbose       Enable verbose output (debug logging)
  -n, --dry-run       Show what would be done without doing it
  -l, --log-file FILE Write logs to FILE
  -c, --config FILE   Use configuration file
  -h, --help          Show this help message
  --version           Show version information

Arguments:
  (Define your positional arguments here)

Examples:
  ${SCRIPT_NAME} -v argument1 argument2
  ${SCRIPT_NAME} --dry-run --log-file output.log

Exit Codes:
  0  Success
  1  General error
  2  Usage error
  3  Missing dependency

Environment Variables:
  LOG_LEVEL    Set log level (DEBUG, INFO, WARN, ERROR)
  CONFIG_FILE  Default configuration file path

For more information, see: https://example.com/docs
USAGE
}

#######################################
# Parse command line arguments
# Arguments:
#   $@ - All command line arguments
#######################################
parse_arguments() {
  # Parse options
  while [[ $# -gt 0 ]]; do
    case "$1" in
      -v|--verbose)
        VERBOSE=true
        log_level_num=$LOG_LEVEL_DEBUG
        shift
        ;;
      -n|--dry-run)
        DRY_RUN=true
        shift
        ;;
      -l|--log-file)
        if [[ -z "${2:-}" ]]; then
          log_error "Option $1 requires an argument"
          usage
          exit "$EXIT_USAGE"
        fi
        LOG_FILE="$2"
        shift 2
        ;;
      -c|--config)
        if [[ -z "${2:-}" ]]; then
          log_error "Option $1 requires an argument"
          usage
          exit "$EXIT_USAGE"
        fi
        CONFIG_FILE="$2"
        shift 2
        ;;
      -h|--help)
        usage
        exit "$EXIT_SUCCESS"
        ;;
      --version)
        echo "${SCRIPT_NAME} version ${SCRIPT_VERSION}"
        echo "Author: ${SCRIPT_AUTHOR}"
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

  # Parse positional arguments
  # TODO: Add your positional argument handling here

  # Example validation
  # if [[ $# -lt 1 ]]; then
  #   log_error "Missing required argument"
  #   usage
  #   exit "$EXIT_USAGE"
  # fi
}

#######################################
# MAIN LOGIC
#######################################

#######################################
# Main function
# Arguments:
#   $@ - All command line arguments
#######################################
main() {
  log_info "Starting ${SCRIPT_NAME} v${SCRIPT_VERSION}"

  # Parse arguments
  parse_arguments "$@"

  # Validate dependencies
  validate_dependencies

  # Load configuration if specified
  if [[ -n "$CONFIG_FILE" ]]; then
    if validate_file "$CONFIG_FILE" "Config file"; then
      log_info "Loading configuration from: $CONFIG_FILE"
      # TODO: Load configuration
    else
      exit "$EXIT_ERROR"
    fi
  fi

  # TODO: Implement your main logic here

  log_info "Script completed successfully"
}

#######################################
# SCRIPT EXECUTION
#######################################

# Only run main if script is executed directly
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
