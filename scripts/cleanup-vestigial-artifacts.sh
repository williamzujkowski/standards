#!/usr/bin/env bash
#
# Cleanup Vestigial Artifacts Script
#
# Purpose: Safely delete vestigial files with backup, logging, and validation.
# Features:
#   - Dry-run mode for preview
#   - Automatic backup before deletion
#   - Reference scanning and updating
#   - Post-deletion validation
#   - Comprehensive logging
#
# Usage:
#   ./cleanup-vestigial-artifacts.sh --input <file-list> [options]
#   ./cleanup-vestigial-artifacts.sh --dry-run --input files-to-delete.txt
#   ./cleanup-vestigial-artifacts.sh --input files-to-delete.txt --backup-dir /tmp/cleanup-backup

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
LOG_FILE="${REPO_ROOT}/reports/generated/cleanup-${TIMESTAMP}.log"
BACKUP_DIR="${REPO_ROOT}/.cleanup-backups/${TIMESTAMP}"
DRY_RUN=false
INPUT_FILE=""
VERBOSE=false
VALIDATE_AFTER=true

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp
    timestamp="$(date +'%Y-%m-%d %H:%M:%S')"

    echo "[${timestamp}] [${level}] ${message}" | tee -a "${LOG_FILE}"
}

log_info() { log "INFO" "$@"; }
log_warn() { log "WARN" "$@"; }
log_error() { log "ERROR" "$@"; }
log_success() { log "SUCCESS" "$@"; }

# Print colored output
print_color() {
    local color="$1"
    shift
    echo -e "${color}$*${NC}"
}

# Usage information
usage() {
    cat <<EOF
Usage: $0 --input <file-list> [options]

Safely delete vestigial files with backup and validation.

Required Arguments:
  --input FILE          File containing list of files to delete (one per line)

Options:
  --dry-run             Preview actions without executing
  --backup-dir DIR      Custom backup directory (default: .cleanup-backups/TIMESTAMP)
  --no-validate         Skip post-deletion validation
  --verbose             Enable verbose output
  --help                Show this help message

Examples:
  # Dry run to preview
  $0 --dry-run --input vestigial-files.txt

  # Execute cleanup with custom backup location
  $0 --input vestigial-files.txt --backup-dir /tmp/my-backup

  # Cleanup without validation (not recommended)
  $0 --input vestigial-files.txt --no-validate

File Format (vestigial-files.txt):
  One file path per line, relative to repository root:
    docs/old-guide.md
    examples/deprecated-example.py
    scripts/unused-script.sh
EOF
    exit 0
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --input)
            INPUT_FILE="$2"
            shift 2
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --backup-dir)
            BACKUP_DIR="$2"
            shift 2
            ;;
        --no-validate)
            VALIDATE_AFTER=false
            shift
            ;;
        --verbose)
            VERBOSE=true
            shift
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown option: $1"
            usage
            ;;
    esac
done

# Validate input
if [[ -z "${INPUT_FILE}" ]]; then
    print_color "${RED}" "Error: --input is required"
    usage
fi

if [[ ! -f "${INPUT_FILE}" ]]; then
    print_color "${RED}" "Error: Input file not found: ${INPUT_FILE}"
    exit 1
fi

# Initialize
mkdir -p "$(dirname "${LOG_FILE}")"
mkdir -p "${BACKUP_DIR}"

print_color "${BLUE}" "========================================="
print_color "${BLUE}" "Vestigial Artifacts Cleanup"
print_color "${BLUE}" "========================================="
echo ""
log_info "Starting cleanup process"
log_info "Repository root: ${REPO_ROOT}"
log_info "Input file: ${INPUT_FILE}"
log_info "Backup directory: ${BACKUP_DIR}"
log_info "Dry run: ${DRY_RUN}"
log_info "Log file: ${LOG_FILE}"
echo ""

# Read files to delete
mapfile -t FILES_TO_DELETE < <(grep -v '^#' "${INPUT_FILE}" | grep -v '^[[:space:]]*$' || true)

if [[ ${#FILES_TO_DELETE[@]} -eq 0 ]]; then
    print_color "${YELLOW}" "No files to delete found in ${INPUT_FILE}"
    exit 0
fi

print_color "${BLUE}" "Files to process: ${#FILES_TO_DELETE[@]}"
echo ""

# Function to check if file exists
check_file_exists() {
    local file="$1"
    local full_path="${REPO_ROOT}/${file}"

    if [[ ! -f "${full_path}" ]]; then
        log_warn "File not found: ${file}"
        return 1
    fi
    return 0
}

# Function to scan for references
scan_references() {
    local file="$1"
    local filename
    filename="$(basename "${file}")"
    local references=()

    log_info "Scanning for references to: ${file}"

    # Search for references in markdown files
    while IFS= read -r ref_file; do
        if grep -q "${filename}" "${ref_file}" 2>/dev/null; then
            references+=("${ref_file}")
        fi
    done < <(find "${REPO_ROOT}" -name "*.md" -type f ! -path "*/\.git/*" ! -path "*/.cleanup-backups/*" ! -path "*/reports/generated/*")

    # Search for references in config files
    while IFS= read -r ref_file; do
        if grep -q "${file}" "${ref_file}" 2>/dev/null; then
            references+=("${ref_file}")
        fi
    done < <(find "${REPO_ROOT}/config" -type f 2>/dev/null || true)

    if [[ ${#references[@]} -gt 0 ]]; then
        log_warn "Found ${#references[@]} references to ${file}:"
        for ref in "${references[@]}"; do
            log_warn "  - ${ref}"
        done
    else
        log_info "No references found for ${file}"
    fi

    echo "${#references[@]}"
}

# Function to backup file
backup_file() {
    local file="$1"
    local full_path="${REPO_ROOT}/${file}"
    local backup_path="${BACKUP_DIR}/${file}"

    mkdir -p "$(dirname "${backup_path}")"

    if cp -p "${full_path}" "${backup_path}"; then
        log_info "Backed up: ${file} -> ${backup_path}"
        return 0
    else
        log_error "Failed to backup: ${file}"
        return 1
    fi
}

# Function to delete file
delete_file() {
    local file="$1"
    local full_path="${REPO_ROOT}/${file}"

    if rm "${full_path}"; then
        log_success "Deleted: ${file}"
        return 0
    else
        log_error "Failed to delete: ${file}"
        return 1
    fi
}

# Function to update references
update_references() {
    local deleted_file="$1"
    local filename
    filename="$(basename "${deleted_file}")"

    log_info "Checking for references to update: ${deleted_file}"

    # Find and update references in markdown files
    local updated_count=0
    while IFS= read -r ref_file; do
        if grep -q "${filename}" "${ref_file}" 2>/dev/null; then
            log_warn "Found reference in: ${ref_file}"
            log_warn "  Manual review recommended for: ${ref_file}"
            ((updated_count++))
        fi
    done < <(find "${REPO_ROOT}" -name "*.md" -type f ! -path "*/\.git/*" ! -path "*/.cleanup-backups/*" ! -path "*/reports/generated/*")

    if [[ ${updated_count} -gt 0 ]]; then
        log_warn "Found ${updated_count} files that may need manual updates"
    fi
}

# Main cleanup process
print_color "${BLUE}" "Phase 1: Validation"
echo ""

VALID_FILES=()
MISSING_FILES=()
FILE_REFERENCES=()

for file in "${FILES_TO_DELETE[@]}"; do
    if check_file_exists "${file}"; then
        VALID_FILES+=("${file}")
        ref_count=$(scan_references "${file}")
        FILE_REFERENCES+=("${ref_count}")
    else
        MISSING_FILES+=("${file}")
    fi
done

echo ""
print_color "${GREEN}" "Valid files: ${#VALID_FILES[@]}"
print_color "${YELLOW}" "Missing files: ${#MISSING_FILES[@]}"
echo ""

if [[ ${#MISSING_FILES[@]} -gt 0 ]]; then
    log_warn "The following files were not found:"
    for missing in "${MISSING_FILES[@]}"; do
        log_warn "  - ${missing}"
    done
    echo ""
fi

if [[ ${#VALID_FILES[@]} -eq 0 ]]; then
    print_color "${YELLOW}" "No valid files to delete"
    exit 0
fi

# Check for references
TOTAL_REFERENCES=0
for ref_count in "${FILE_REFERENCES[@]}"; do
    TOTAL_REFERENCES=$((TOTAL_REFERENCES + ref_count))
done

if [[ ${TOTAL_REFERENCES} -gt 0 ]]; then
    print_color "${YELLOW}" "Warning: Found ${TOTAL_REFERENCES} total references to files being deleted"
    print_color "${YELLOW}" "Manual review may be required after cleanup"
    echo ""
fi

if [[ "${DRY_RUN}" == "true" ]]; then
    print_color "${YELLOW}" "DRY RUN MODE - No files will be deleted"
    echo ""
    print_color "${BLUE}" "Would delete the following files:"
    for file in "${VALID_FILES[@]}"; do
        echo "  - ${file}"
    done
    echo ""
    log_info "Dry run completed - no changes made"
    exit 0
fi

# Confirm deletion
print_color "${YELLOW}" "Ready to delete ${#VALID_FILES[@]} files"
read -p "Continue? (yes/no): " -r
echo ""

if [[ ! "${REPLY}" =~ ^[Yy][Ee][Ss]$ ]]; then
    print_color "${YELLOW}" "Cleanup cancelled"
    log_info "Cleanup cancelled by user"
    exit 0
fi

# Phase 2: Backup
print_color "${BLUE}" "Phase 2: Backup"
echo ""

BACKUP_FAILURES=0
for file in "${VALID_FILES[@]}"; do
    if ! backup_file "${file}"; then
        ((BACKUP_FAILURES++))
    fi
done

if [[ ${BACKUP_FAILURES} -gt 0 ]]; then
    print_color "${RED}" "Backup failures: ${BACKUP_FAILURES}"
    log_error "Aborting cleanup due to backup failures"
    exit 1
fi

echo ""
log_success "All files backed up successfully"
echo ""

# Phase 3: Deletion
print_color "${BLUE}" "Phase 3: Deletion"
echo ""

DELETED_FILES=()
DELETION_FAILURES=()

for file in "${VALID_FILES[@]}"; do
    if delete_file "${file}"; then
        DELETED_FILES+=("${file}")
    else
        DELETION_FAILURES+=("${file}")
    fi
done

echo ""
print_color "${GREEN}" "Deleted: ${#DELETED_FILES[@]} files"
if [[ ${#DELETION_FAILURES[@]} -gt 0 ]]; then
    print_color "${RED}" "Failed: ${#DELETION_FAILURES[@]} files"
    for failed in "${DELETION_FAILURES[@]}"; do
        log_error "  - ${failed}"
    done
fi
echo ""

# Phase 4: Update references
print_color "${BLUE}" "Phase 4: Reference Check"
echo ""

for file in "${DELETED_FILES[@]}"; do
    update_references "${file}"
done

echo ""

# Phase 5: Validation
if [[ "${VALIDATE_AFTER}" == "true" ]]; then
    print_color "${BLUE}" "Phase 5: Validation"
    echo ""

    log_info "Running validation scripts..."

    # Run audit reports
    if [[ -x "${SCRIPT_DIR}/generate-audit-reports.py" ]]; then
        if python3 "${SCRIPT_DIR}/generate-audit-reports.py" >> "${LOG_FILE}" 2>&1; then
            log_success "Audit reports generated successfully"
        else
            log_warn "Audit report generation had issues (check log)"
        fi
    fi

    # Run validation
    if [[ -x "${SCRIPT_DIR}/validate-claims.py" ]]; then
        if python3 "${SCRIPT_DIR}/validate-claims.py" >> "${LOG_FILE}" 2>&1; then
            log_success "Validation passed"
        else
            log_warn "Validation found issues (check log)"
        fi
    fi

    echo ""
fi

# Summary
print_color "${BLUE}" "========================================="
print_color "${BLUE}" "Cleanup Summary"
print_color "${BLUE}" "========================================="
echo ""
print_color "${GREEN}" "Successfully deleted: ${#DELETED_FILES[@]} files"
if [[ ${#DELETION_FAILURES[@]} -gt 0 ]]; then
    print_color "${RED}" "Failed deletions: ${#DELETION_FAILURES[@]}"
fi
print_color "${BLUE}" "Backup location: ${BACKUP_DIR}"
print_color "${BLUE}" "Log file: ${LOG_FILE}"
echo ""

if [[ ${TOTAL_REFERENCES} -gt 0 ]]; then
    print_color "${YELLOW}" "⚠️  Manual review recommended for ${TOTAL_REFERENCES} reference(s)"
    echo ""
    echo "Next steps:"
    echo "1. Review log file: ${LOG_FILE}"
    echo "2. Check for broken links: python3 scripts/generate-audit-reports.py"
    echo "3. Update documentation as needed"
    echo "4. Run validation: python3 scripts/validate-claims.py"
fi

log_success "Cleanup completed successfully"

# Rollback instructions
cat >> "${LOG_FILE}" <<EOF

ROLLBACK INSTRUCTIONS
=====================
To restore deleted files:
  cd ${BACKUP_DIR}
  cp -r . ${REPO_ROOT}/

To restore individual files:
  cp ${BACKUP_DIR}/<file> ${REPO_ROOT}/<file>
EOF

echo ""
print_color "${GREEN}" "✅ Cleanup complete!"
echo ""

exit 0
