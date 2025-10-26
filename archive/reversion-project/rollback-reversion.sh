#!/usr/bin/env bash
#
# rollback-reversion.sh - Emergency rollback of failed reversion
#
# USAGE:
#   ./scripts/rollback-reversion.sh [OPTIONS]
#
# OPTIONS:
#   --dry-run          Show what would be done without doing it
#   --backup-tag TAG   Specific backup tag to restore (default: latest)
#   --no-confirm       Skip confirmation prompts (dangerous!)
#   --verbose          Show detailed progress
#   --help             Show this help message
#
# EXAMPLES:
#   ./scripts/rollback-reversion.sh --dry-run
#   ./scripts/rollback-reversion.sh --backup-tag backup-20251025_143022
#   ./scripts/rollback-reversion.sh --no-confirm --verbose
#
# DESCRIPTION:
#   Restores repository to the backup state created before reversion.
#   This is an emergency recovery tool to undo a failed reversion attempt.
#
# SAFETY:
#   - Requires backup tag to exist
#   - Creates rollback branch before restoration
#   - Requires confirmation before destructive operations
#   - Logs all operations
#   - Validates state after rollback
#

set -euo pipefail

# Script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default configuration
DRY_RUN=false
VERBOSE=false
NO_CONFIRM=false
BACKUP_TAG=""
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="$REPO_ROOT/backups"
LOG_FILE="$LOG_DIR/rollback_${TIMESTAMP}.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --backup-tag)
                BACKUP_TAG="$2"
                shift 2
                ;;
            --no-confirm)
                NO_CONFIRM=true
                shift
                ;;
            --verbose)
                VERBOSE=true
                shift
                ;;
            --help)
                grep '^#' "$0" | grep -v '#!/usr/bin/env' | sed 's/^# \?//'
                exit 0
                ;;
            *)
                echo -e "${RED}Error: Unknown option $1${NC}"
                exit 1
                ;;
        esac
    done
}

# Logging functions
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')

    # Create log directory if it doesn't exist
    [[ ! -d "$LOG_DIR" ]] && mkdir -p "$LOG_DIR"

    echo "[$timestamp] [$level] $message" | tee -a "$LOG_FILE"

    case $level in
        INFO)
            [[ "$VERBOSE" == "true" ]] && echo -e "${BLUE}INFO:${NC} $message" >&2
            ;;
        SUCCESS)
            echo -e "${GREEN}✓${NC} $message" >&2
            ;;
        WARNING)
            echo -e "${YELLOW}⚠${NC} $message" >&2
            ;;
        ERROR)
            echo -e "${RED}✗${NC} $message" >&2
            ;;
    esac
}

# Execute command with dry-run support
execute() {
    local cmd="$*"

    if [[ "$DRY_RUN" == "true" ]]; then
        log INFO "[DRY-RUN] Would execute: $cmd"
        return 0
    fi

    log INFO "Executing: $cmd"
    if eval "$cmd" >> "$LOG_FILE" 2>&1; then
        return 0
    else
        local exit_code=$?
        log ERROR "Command failed with exit code $exit_code: $cmd"
        return $exit_code
    fi
}

# Confirmation prompt
confirm() {
    local message="$1"

    if [[ "$NO_CONFIRM" == "true" ]]; then
        log WARNING "Auto-confirming (--no-confirm): $message"
        return 0
    fi

    echo -e "${YELLOW}⚠  $message${NC}"
    read -p "Continue? (yes/no): " response

    if [[ "$response" != "yes" ]]; then
        log WARNING "User cancelled operation"
        exit 1
    fi

    log INFO "User confirmed: $message"
}

# Find backup tag
find_backup_tag() {
    log INFO "Finding backup tag"

    cd "$REPO_ROOT"

    # If tag specified, verify it exists
    if [[ -n "$BACKUP_TAG" ]]; then
        if git rev-parse "$BACKUP_TAG" >/dev/null 2>&1; then
            log SUCCESS "Using specified backup tag: $BACKUP_TAG"
            echo "$BACKUP_TAG"
            return 0
        else
            log ERROR "Specified backup tag not found: $BACKUP_TAG"
            exit 1
        fi
    fi

    # Find latest backup tag
    local latest_tag=$(git tag -l "backup-*" | sort -r | head -1)

    if [[ -z "$latest_tag" ]]; then
        log ERROR "No backup tags found. Cannot rollback without backup."
        log INFO "Available tags:"
        git tag -l
        exit 1
    fi

    log SUCCESS "Found latest backup tag: $latest_tag"
    echo "$latest_tag"
}

# Find backup branch
find_backup_branch() {
    log INFO "Finding backup branch"

    cd "$REPO_ROOT"

    # Find latest backup branch
    local latest_branch=$(git branch -a | grep "backup/pre-reversion-" | sed 's/^[* ]*//' | sort -r | head -1)

    if [[ -z "$latest_branch" ]]; then
        log WARNING "No backup branch found"
        return 1
    fi

    log SUCCESS "Found backup branch: $latest_branch"
    echo "$latest_branch"
}

# Verify backup state
verify_backup() {
    local backup_tag="$1"

    log INFO "Verifying backup state"

    cd "$REPO_ROOT"

    # Check if tag exists
    if ! git rev-parse "$backup_tag" >/dev/null 2>&1; then
        log ERROR "Backup tag does not exist: $backup_tag"
        exit 1
    fi

    # Get backup commit info
    local backup_commit=$(git rev-parse "$backup_tag")
    local backup_commit_short=$(git rev-parse --short "$backup_tag")
    local backup_message=$(git log -1 --pretty=%s "$backup_tag")
    local backup_date=$(git log -1 --pretty=%ci "$backup_tag")

    log INFO "Backup details:"
    log INFO "  Tag: $backup_tag"
    log INFO "  Commit: $backup_commit_short"
    log INFO "  Message: $backup_message"
    log INFO "  Date: $backup_date"

    log SUCCESS "Backup verified"
}

# Check current state
check_current_state() {
    log INFO "Checking current repository state"

    cd "$REPO_ROOT"

    # Check for uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        log WARNING "Working directory has uncommitted changes:"
        git status --short

        confirm "Uncommitted changes will be lost. Continue with rollback?"
    fi

    # Get current state info
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    local current_commit=$(git rev-parse --short HEAD)

    log INFO "Current state:"
    log INFO "  Branch: $current_branch"
    log INFO "  Commit: $current_commit"

    log SUCCESS "Current state checked"
}

# Create rollback branch
create_rollback_branch() {
    local branch_name="rollback/from-reversion-${TIMESTAMP}"

    log INFO "Creating rollback branch: $branch_name"

    # Save current state in a branch (for reference)
    execute git branch "$branch_name" || {
        log WARNING "Failed to create rollback reference branch (may already exist)"
    }

    log SUCCESS "Rollback reference branch created: $branch_name"
    echo "$branch_name"
}

# Perform rollback to backup
perform_rollback() {
    local backup_tag="$1"

    log INFO "Performing rollback to backup: $backup_tag"

    confirm "This will restore repository to backup state. Current work will be lost."

    # Reset to backup tag
    execute git reset --hard "$backup_tag" || {
        log ERROR "Failed to reset to backup tag"
        exit 1
    }

    log SUCCESS "Rollback completed - restored to $backup_tag"

    # Show current state
    log INFO "Current state after rollback:"
    git log --oneline -5
}

# Clean up reversion artifacts
cleanup_reversion_artifacts() {
    log INFO "Cleaning up reversion artifacts"

    cd "$REPO_ROOT"

    # List reversion branches
    local reversion_branches=$(git branch | grep "reversion/skills-md-" || true)

    if [[ -n "$reversion_branches" ]]; then
        log INFO "Found reversion branches:"
        echo "$reversion_branches" | while read -r branch; do
            log INFO "  $branch"
        done

        if confirm "Delete reversion branches?"; then
            echo "$reversion_branches" | while read -r branch; do
                execute git branch -D "$branch" || log WARNING "Failed to delete branch: $branch"
            done
        fi
    else
        log INFO "No reversion branches to clean up"
    fi

    log SUCCESS "Cleanup completed"
}

# Validate rollback
validate_rollback() {
    local backup_tag="$1"

    log INFO "Validating rollback"

    cd "$REPO_ROOT"

    # Verify we're at the backup commit
    local current_commit=$(git rev-parse HEAD)
    local backup_commit=$(git rev-parse "$backup_tag")

    if [[ "$current_commit" != "$backup_commit" ]]; then
        log ERROR "Rollback validation failed: not at backup commit"
        log ERROR "  Current:  $current_commit"
        log ERROR "  Expected: $backup_commit"
        exit 1
    fi

    log SUCCESS "Rollback validated - at backup commit"

    # Check repository integrity
    if git fsck --full > /dev/null 2>&1; then
        log SUCCESS "Repository integrity verified"
    else
        log WARNING "Repository integrity check found issues (usually harmless)"
    fi
}

# Create rollback report
create_rollback_report() {
    local backup_tag="$1"
    local rollback_branch="$2"
    local report_file="$LOG_DIR/rollback_report_${TIMESTAMP}.txt"

    log INFO "Creating rollback report"

    if [[ "$DRY_RUN" == "false" ]]; then
        cat > "$report_file" <<EOF
=================================================================
ROLLBACK REPORT
=================================================================

Rollback Timestamp: $TIMESTAMP
Rollback Date: $(date)

ROLLBACK DETAILS
----------------
Backup Tag: $backup_tag
Rollback Branch (reference): $rollback_branch

CURRENT STATE (AFTER ROLLBACK)
-------------------------------
Current Branch: $(git rev-parse --abbrev-ref HEAD)
Current Commit: $(git rev-parse HEAD)
Current Commit (short): $(git rev-parse --short HEAD)

REPOSITORY STATUS
-----------------
$(git status)

RECENT COMMITS (last 10)
------------------------
$(git log --oneline -10)

VERIFICATION COMMANDS
---------------------
# Verify current state
git log --oneline -10

# Check what was rolled back from
git log --oneline "$rollback_branch" -5

# View all backups
git tag -l "backup-*"
git branch -a | grep backup

RECOVERY NOTES
--------------
If you need to restore the reversion attempt:
1. Find the rollback reference branch: git log "$rollback_branch"
2. Create new branch from it: git checkout -b restore-reversion "$rollback_branch"
3. Review and decide next steps

NEXT STEPS
----------
1. Review this report: cat $report_file
2. Verify repository state: git status
3. If needed, re-attempt reversion with fixes:
   - Create new backup: ./scripts/backup-current-state.sh
   - Try reversion again: ./scripts/revert-to-pre-skills.sh
4. Clean up old backup artifacts if desired

=================================================================
EOF
    fi

    log SUCCESS "Rollback report created: $report_file"
    echo "$report_file"
}

# Main execution
main() {
    parse_args "$@"

    echo -e "${RED}==================================================================${NC}"
    echo -e "${RED}EMERGENCY ROLLBACK - Undoing Failed Reversion${NC}"
    echo -e "${RED}==================================================================${NC}"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}DRY-RUN MODE: No changes will be made${NC}"
        echo ""
    fi

    # Find and verify backup
    local backup_tag=$(find_backup_tag)
    verify_backup "$backup_tag"

    echo ""
    echo -e "${YELLOW}⚠  WARNING: This will restore repository to backup state${NC}"
    echo -e "${YELLOW}⚠  All changes since backup will be lost${NC}"
    echo ""
    echo -e "Backup Tag: ${BLUE}$backup_tag${NC}"
    echo ""

    # Check current state
    check_current_state

    # Confirm major operation
    confirm "Proceed with emergency rollback?"

    # Create rollback reference branch
    local rollback_branch=$(create_rollback_branch)

    # Perform rollback
    perform_rollback "$backup_tag"

    # Validate rollback
    validate_rollback "$backup_tag"

    # Optional cleanup
    cleanup_reversion_artifacts

    # Create report
    local report_file=$(create_rollback_report "$backup_tag" "$rollback_branch")

    # Final output
    echo ""
    echo -e "${GREEN}==================================================================${NC}"
    echo -e "${GREEN}ROLLBACK COMPLETED${NC}"
    echo -e "${GREEN}==================================================================${NC}"
    echo ""
    echo -e "Restored to:   ${BLUE}$backup_tag${NC}"
    echo -e "Reference:     ${BLUE}$rollback_branch${NC}"
    echo -e "Report:        ${BLUE}$report_file${NC}"
    echo ""

    if [[ "$DRY_RUN" == "false" ]]; then
        echo -e "${YELLOW}Repository has been restored to backup state${NC}"
        echo ""
        echo -e "${YELLOW}Next steps:${NC}"
        echo "  1. Review report: cat $report_file"
        echo "  2. Verify state: git status && git log --oneline -10"
        echo "  3. If needed, re-attempt reversion with corrections"
    fi

    log INFO "Rollback process completed"
}

# Run main function
main "$@"
