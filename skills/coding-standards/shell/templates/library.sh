#!/usr/bin/env bash
#
# library.sh - Reusable bash function library
# Source this file in your scripts: source ./library.sh
#

#######################################
# STRING OPERATIONS
#######################################

# Trim whitespace from string
string_trim() {
  local str="$1"
  str="${str#"${str%%[![:space:]]*}"}"
  str="${str%"${str##*[![:space:]]}"}"
  echo "$str"
}

# Convert string to uppercase
string_upper() {
  echo "${1^^}"
}

# Convert string to lowercase
string_lower() {
  echo "${1,,}"
}

# Check if string contains substring
string_contains() {
  local string="$1"
  local substring="$2"
  [[ "$string" == *"$substring"* ]]
}

# Check if string starts with prefix
string_starts_with() {
  local string="$1"
  local prefix="$2"
  [[ "$string" == "$prefix"* ]]
}

# Check if string ends with suffix
string_ends_with() {
  local string="$1"
  local suffix="$2"
  [[ "$string" == *"$suffix" ]]
}

#######################################
# ARRAY OPERATIONS
#######################################

# Check if array contains element
array_contains() {
  local element="$1"
  shift
  local array=("$@")
  
  for item in "${array[@]}"; do
    if [[ "$item" == "$element" ]]; then
      return 0
    fi
  done
  return 1
}

# Get array length
array_length() {
  local -n arr=$1
  echo "${#arr[@]}"
}

# Join array elements with delimiter
array_join() {
  local delimiter="$1"
  shift
  local array=("$@")
  local result=""
  
  for item in "${array[@]}"; do
    if [[ -z "$result" ]]; then
      result="$item"
    else
      result="${result}${delimiter}${item}"
    fi
  done
  
  echo "$result"
}

#######################################
# FILE OPERATIONS
#######################################

# Get file size in bytes
file_size() {
  local file="$1"
  stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null
}

# Get file modification time
file_mtime() {
  local file="$1"
  stat -f%m "$file" 2>/dev/null || stat -c%Y "$file" 2>/dev/null
}

# Create directory if it doesn't exist
ensure_directory() {
  local dir="$1"
  if [[ ! -d "$dir" ]]; then
    mkdir -p "$dir"
  fi
}

# Backup file with timestamp
backup_file() {
  local file="$1"
  local timestamp
  timestamp="$(date '+%Y%m%d_%H%M%S')"
  local backup="${file}.backup.${timestamp}"
  
  if [[ -f "$file" ]]; then
    cp "$file" "$backup"
    echo "$backup"
  fi
}

# Count lines in file
count_lines() {
  local file="$1"
  wc -l < "$file" | tr -d ' '
}

#######################################
# VALIDATION
#######################################

# Validate email address
is_valid_email() {
  local email="$1"
  local regex='^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
  [[ "$email" =~ $regex ]]
}

# Validate IP address
is_valid_ip() {
  local ip="$1"
  local regex='^([0-9]{1,3}\.){3}[0-9]{1,3}$'
  
  if [[ ! "$ip" =~ $regex ]]; then
    return 1
  fi
  
  local -a octets
  IFS='.' read -ra octets <<< "$ip"
  
  for octet in "${octets[@]}"; do
    if ((octet > 255)); then
      return 1
    fi
  done
  
  return 0
}

# Validate URL
is_valid_url() {
  local url="$1"
  local regex='^https?://[a-zA-Z0-9.-]+(:[0-9]+)?(/.*)?$'
  [[ "$url" =~ $regex ]]
}

# Check if value is numeric
is_numeric() {
  local value="$1"
  [[ "$value" =~ ^[0-9]+$ ]]
}

# Check if value is integer (including negative)
is_integer() {
  local value="$1"
  [[ "$value" =~ ^-?[0-9]+$ ]]
}

#######################################
# DATE/TIME
#######################################

# Get current timestamp
timestamp() {
  date '+%Y-%m-%d %H:%M:%S'
}

# Get ISO 8601 timestamp
timestamp_iso() {
  date -u '+%Y-%m-%dT%H:%M:%SZ'
}

# Get Unix epoch timestamp
timestamp_epoch() {
  date '+%s'
}

# Format seconds as human-readable duration
format_duration() {
  local seconds=$1
  local hours=$((seconds / 3600))
  local minutes=$(((seconds % 3600) / 60))
  local secs=$((seconds % 60))
  
  printf "%02d:%02d:%02d" "$hours" "$minutes" "$secs"
}

#######################################
# SYSTEM
#######################################

# Get OS type
get_os() {
  case "$(uname -s)" in
    Linux*)   echo "linux" ;;
    Darwin*)  echo "macos" ;;
    CYGWIN*)  echo "windows" ;;
    MINGW*)   echo "windows" ;;
    *)        echo "unknown" ;;
  esac
}

# Get CPU count
get_cpu_count() {
  local os
  os=$(get_os)
  
  case "$os" in
    linux)  nproc ;;
    macos)  sysctl -n hw.ncpu ;;
    *)      echo "1" ;;
  esac
}

# Get available memory in MB
get_memory_mb() {
  local os
  os=$(get_os)
  
  case "$os" in
    linux)
      free -m | awk '/^Mem:/ {print $7}'
      ;;
    macos)
      vm_stat | awk '/Pages free/ {print int($3 * 4096 / 1048576)}'
      ;;
    *)
      echo "0"
      ;;
  esac
}

#######################################
# NETWORK
#######################################

# Check if host is reachable
is_host_reachable() {
  local host="$1"
  local timeout="${2:-5}"
  
  ping -c 1 -W "$timeout" "$host" >/dev/null 2>&1
}

# Check if port is open
is_port_open() {
  local host="$1"
  local port="$2"
  local timeout="${3:-5}"
  
  timeout "$timeout" bash -c "cat < /dev/null > /dev/tcp/${host}/${port}" 2>/dev/null
}

# Get public IP address
get_public_ip() {
  curl -s https://api.ipify.org 2>/dev/null || \
    curl -s https://ifconfig.me 2>/dev/null || \
    echo "unavailable"
}

#######################################
# PROCESS MANAGEMENT
#######################################

# Check if process is running by PID
is_process_running() {
  local pid="$1"
  kill -0 "$pid" 2>/dev/null
}

# Wait for process to finish
wait_for_process() {
  local pid="$1"
  local timeout="${2:-0}"
  local elapsed=0
  
  while is_process_running "$pid"; do
    if ((timeout > 0 && elapsed >= timeout)); then
      return 1
    fi
    sleep 1
    ((elapsed++))
  done
  
  return 0
}

# Get process name by PID
get_process_name() {
  local pid="$1"
  ps -p "$pid" -o comm= 2>/dev/null
}

#######################################
# RETRY LOGIC
#######################################

# Retry command with exponential backoff
retry() {
  local max_attempts="${1:-3}"
  local initial_delay="${2:-1}"
  shift 2
  local -a cmd=("$@")
  
  local attempt=1
  local delay=$initial_delay
  
  while ((attempt <= max_attempts)); do
    if "${cmd[@]}"; then
      return 0
    fi
    
    if ((attempt < max_attempts)); then
      sleep "$delay"
      delay=$((delay * 2))
    fi
    
    ((attempt++))
  done
  
  return 1
}

#######################################
# LOGGING HELPERS
#######################################

# Log with timestamp
log_with_timestamp() {
  local message="$1"
  echo "[$(timestamp)] $message"
}

# Log to file
log_to_file() {
  local file="$1"
  local message="$2"
  echo "[$(timestamp)] $message" >> "$file"
}

#######################################
# PROGRESS INDICATORS
#######################################

# Show spinner while command runs
spinner() {
  local pid=$1
  local spin='⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏'
  local i=0
  
  while is_process_running "$pid"; do
    printf "\r[%s] Processing..." "${spin:i++%${#spin}:1}"
    sleep 0.1
  done
  
  printf "\r[✓] Done!         \n"
}

# Progress bar
progress_bar() {
  local current=$1
  local total=$2
  local width=50
  
  local percentage=$((current * 100 / total))
  local filled=$((width * current / total))
  local empty=$((width - filled))
  
  printf "\r["
  printf "%${filled}s" | tr ' ' '='
  printf "%${empty}s" | tr ' ' ' '
  printf "] %d%%" "$percentage"
}

#######################################
# CLEANUP HELPERS
#######################################

# Register cleanup function
register_cleanup() {
  local func="$1"
  trap "$func" EXIT INT TERM
}

# Remove file on exit
cleanup_file() {
  local file="$1"
  trap "rm -f '$file'" EXIT INT TERM
}

# Remove directory on exit
cleanup_dir() {
  local dir="$1"
  trap "rm -rf '$dir'" EXIT INT TERM
}

#######################################
# COLOR OUTPUT
#######################################

# Color codes
readonly COLOR_RED='\033[0;31m'
readonly COLOR_GREEN='\033[0;32m'
readonly COLOR_YELLOW='\033[1;33m'
readonly COLOR_BLUE='\033[0;34m'
readonly COLOR_MAGENTA='\033[0;35m'
readonly COLOR_CYAN='\033[0;36m'
readonly COLOR_NC='\033[0m'

# Print colored text
print_color() {
  local color="$1"
  shift
  echo -e "${color}$*${COLOR_NC}"
}

print_red() { print_color "$COLOR_RED" "$@"; }
print_green() { print_color "$COLOR_GREEN" "$@"; }
print_yellow() { print_color "$COLOR_YELLOW" "$@"; }
print_blue() { print_color "$COLOR_BLUE" "$@"; }

#######################################
# VERSION COMPARISON
#######################################

# Compare versions (returns 0 if v1 >= v2)
version_gte() {
  local v1="$1"
  local v2="$2"
  
  printf '%s\n%s\n' "$v1" "$v2" | sort -V -C
}
