#!/usr/bin/env bash
#
# install-shell-tools.sh - Install shell scripting development tools
# Installs: shellcheck, shfmt, bats-core
#

set -euo pipefail

readonly SCRIPT_NAME="${0##*/}"
readonly GREEN='\033[0;32m'
readonly RED='\033[0;31m'
readonly YELLOW='\033[1;33m'
readonly NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $*" >&2; }
log_error() { echo -e "${RED}[ERROR]${NC} $*" >&2; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $*" >&2; }

command_exists() {
  command -v "$1" >/dev/null 2>&1
}

detect_os() {
  case "$(uname -s)" in
    Linux*)   echo "linux" ;;
    Darwin*)  echo "macos" ;;
    *)        echo "unknown" ;;
  esac
}

install_shellcheck() {
  log_info "Installing ShellCheck..."
  
  local os
  os=$(detect_os)
  
  case "$os" in
    linux)
      if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install -y shellcheck
      elif command_exists dnf; then
        sudo dnf install -y ShellCheck
      elif command_exists yum; then
        sudo yum install -y ShellCheck
      elif command_exists pacman; then
        sudo pacman -S --noconfirm shellcheck
      else
        log_warn "Package manager not detected, installing from binary..."
        install_shellcheck_binary
      fi
      ;;
    macos)
      if command_exists brew; then
        brew install shellcheck
      else
        log_error "Homebrew not found. Install from: https://brew.sh/"
        return 1
      fi
      ;;
    *)
      log_error "Unsupported OS: $os"
      return 1
      ;;
  esac
  
  log_info "ShellCheck installed successfully"
}

install_shellcheck_binary() {
  local version="v0.9.0"
  local arch
  arch="$(uname -m)"
  
  case "$arch" in
    x86_64)  arch="x86_64" ;;
    aarch64) arch="aarch64" ;;
    *)
      log_error "Unsupported architecture: $arch"
      return 1
      ;;
  esac
  
  local url="https://github.com/koalaman/shellcheck/releases/download/${version}/shellcheck-${version}.linux.${arch}.tar.xz"
  local temp_dir
  temp_dir="$(mktemp -d)"
  
  log_info "Downloading ShellCheck from $url"
  curl -L "$url" -o "$temp_dir/shellcheck.tar.xz"
  
  tar -xf "$temp_dir/shellcheck.tar.xz" -C "$temp_dir"
  sudo mv "$temp_dir/shellcheck-${version}/shellcheck" /usr/local/bin/
  sudo chmod +x /usr/local/bin/shellcheck
  
  rm -rf "$temp_dir"
}

install_shfmt() {
  log_info "Installing shfmt..."
  
  local os
  os=$(detect_os)
  
  case "$os" in
    linux)
      if command_exists apt-get; then
        # Not in default repos, install from binary
        install_shfmt_binary
      elif command_exists brew; then
        brew install shfmt
      else
        install_shfmt_binary
      fi
      ;;
    macos)
      if command_exists brew; then
        brew install shfmt
      else
        log_error "Homebrew not found. Install from: https://brew.sh/"
        return 1
      fi
      ;;
    *)
      log_error "Unsupported OS: $os"
      return 1
      ;;
  esac
  
  log_info "shfmt installed successfully"
}

install_shfmt_binary() {
  local version="v3.7.0"
  local arch
  arch="$(uname -m)"
  
  case "$arch" in
    x86_64)  arch="amd64" ;;
    aarch64) arch="arm64" ;;
    *)
      log_error "Unsupported architecture: $arch"
      return 1
      ;;
  esac
  
  local url="https://github.com/mvdan/sh/releases/download/${version}/shfmt_${version}_linux_${arch}"
  
  log_info "Downloading shfmt from $url"
  sudo curl -L "$url" -o /usr/local/bin/shfmt
  sudo chmod +x /usr/local/bin/shfmt
}

install_bats() {
  log_info "Installing bats-core..."
  
  local os
  os=$(detect_os)
  
  case "$os" in
    linux)
      if command_exists apt-get; then
        # Try package manager first
        if sudo apt-get install -y bats 2>/dev/null; then
          log_info "Installed bats from package manager"
        else
          install_bats_from_source
        fi
      else
        install_bats_from_source
      fi
      ;;
    macos)
      if command_exists brew; then
        brew install bats-core
      else
        log_error "Homebrew not found. Install from: https://brew.sh/"
        return 1
      fi
      ;;
    *)
      log_error "Unsupported OS: $os"
      return 1
      ;;
  esac
  
  log_info "bats-core installed successfully"
}

install_bats_from_source() {
  local version="v1.10.0"
  local temp_dir
  temp_dir="$(mktemp -d)"
  
  log_info "Installing bats-core from source..."
  
  if ! command_exists git; then
    log_error "Git is required to install bats from source"
    return 1
  fi
  
  git clone --depth 1 --branch "$version" https://github.com/bats-core/bats-core.git "$temp_dir"
  cd "$temp_dir"
  sudo ./install.sh /usr/local
  
  rm -rf "$temp_dir"
}

verify_installation() {
  log_info "Verifying installations..."
  
  local all_installed=true
  
  if command_exists shellcheck; then
    log_info "✓ ShellCheck: $(shellcheck --version | head -n2 | tail -n1)"
  else
    log_error "✗ ShellCheck not found"
    all_installed=false
  fi
  
  if command_exists shfmt; then
    log_info "✓ shfmt: $(shfmt --version)"
  else
    log_error "✗ shfmt not found"
    all_installed=false
  fi
  
  if command_exists bats; then
    log_info "✓ bats: $(bats --version)"
  else
    log_error "✗ bats not found"
    all_installed=false
  fi
  
  if $all_installed; then
    log_info "All tools installed successfully!"
    return 0
  else
    log_error "Some tools failed to install"
    return 1
  fi
}

usage() {
  cat << USAGE
${SCRIPT_NAME} - Install shell scripting development tools

Usage:
  ${SCRIPT_NAME} [OPTIONS]

Options:
  --shellcheck    Install only ShellCheck
  --shfmt         Install only shfmt
  --bats          Install only bats-core
  --all           Install all tools (default)
  -h, --help      Show this help message

Examples:
  ${SCRIPT_NAME}                  # Install all tools
  ${SCRIPT_NAME} --shellcheck     # Install only ShellCheck
  ${SCRIPT_NAME} --shfmt --bats   # Install shfmt and bats

USAGE
}

main() {
  local install_shellcheck=false
  local install_shfmt_flag=false
  local install_bats_flag=false
  local install_all=true
  
  # Parse arguments
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --shellcheck)
        install_shellcheck=true
        install_all=false
        shift
        ;;
      --shfmt)
        install_shfmt_flag=true
        install_all=false
        shift
        ;;
      --bats)
        install_bats_flag=true
        install_all=false
        shift
        ;;
      --all)
        install_all=true
        shift
        ;;
      -h|--help)
        usage
        exit 0
        ;;
      *)
        log_error "Unknown option: $1"
        usage
        exit 1
        ;;
    esac
  done
  
  # Install tools
  if $install_all; then
    install_shellcheck || log_warn "ShellCheck installation failed"
    install_shfmt || log_warn "shfmt installation failed"
    install_bats || log_warn "bats installation failed"
  else
    $install_shellcheck && (install_shellcheck || log_warn "ShellCheck installation failed")
    $install_shfmt_flag && (install_shfmt || log_warn "shfmt installation failed")
    $install_bats_flag && (install_bats || log_warn "bats installation failed")
  fi
  
  echo
  verify_installation
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
  main "$@"
fi
