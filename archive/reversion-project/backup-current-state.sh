#!/usr/bin/env bash
#
# backup-current-state.sh - Create comprehensive backup before reversion
#
# USAGE:
#   ./scripts/backup-current-state.sh [OPTIONS]
#
# OPTIONS:
#   --dry-run          Show what would be done without doing it
#   --backup-dir DIR   Custom backup directory (default: backups/)
#   --verbose          Show detailed progress
#   --help             Show this help message
#
# EXAMPLES:
#   ./scripts/backup-current-state.sh
#   ./scripts/backup-current-state.sh --dry-run
#   ./scripts/backup-current-state.sh --verbose --backup-dir /tmp/backups
#
# DESCRIPTION:
#   Creates timestamped backup branch, tags current HEAD, and exports
#   metadata for safe reversion tracking. All operations are logged.
#
# SAFETY:
#   - Idempotent: Can be run multiple times safely
#   - Non-destructive: Only creates new branches/tags
#   - Logged: All operations recorded to backup.log
#

set -euo pipefail

# Script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default configuration
DRY_RUN=false
VERBOSE=false
BACKUP_DIR="$REPO_ROOT/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$BACKUP_DIR/backup_${TIMESTAMP}.log"

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
            --backup-dir)
                BACKUP_DIR="$2"
                shift 2
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

# Initialize backup directory
init_backup_dir() {
    log INFO "Initializing backup directory: $BACKUP_DIR"

    if [[ ! -d "$BACKUP_DIR" ]] && [[ "$DRY_RUN" == "false" ]]; then
        mkdir -p "$BACKUP_DIR"
    fi

    if [[ "$DRY_RUN" == "false" ]]; then
        # Initialize log file
        echo "=== Backup Process Started at $(date) ===" > "$LOG_FILE"
    fi

    log SUCCESS "Backup directory ready: $BACKUP_DIR"
}

# Verify git repository
verify_git_repo() {
    log INFO "Verifying git repository"

    cd "$REPO_ROOT"

    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log ERROR "Not a git repository: $REPO_ROOT"
        exit 1
    fi

    log SUCCESS "Git repository verified"
}

# Get current state metadata
get_current_state() {
    log INFO "Collecting current state metadata"

    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    local current_commit=$(git rev-parse HEAD)
    local current_commit_short=$(git rev-parse --short HEAD)
    local commit_message=$(git log -1 --pretty=%s)
    local commit_date=$(git log -1 --pretty=%ci)

    cat <<EOF
Current State Metadata
=====================
Timestamp: $TIMESTAMP
Branch: $current_branch
Commit: $current_commit
Commit (short): $current_commit_short
Message: $commit_message
Date: $commit_date
Working Dir: $REPO_ROOT
EOF

    log SUCCESS "State metadata collected"
}

# Create backup branch
create_backup_branch() {
    local branch_name="backup/pre-reversion-${TIMESTAMP}"

    log INFO "Creating backup branch: $branch_name"

    execute git checkout -b "$branch_name" || {
        log WARNING "Branch may already exist, attempting to use existing"
        execute git checkout "$branch_name"
    }

    log SUCCESS "Backup branch created: $branch_name"
    echo "$branch_name"
}

# Create backup tag
create_backup_tag() {
    local current_commit=$(git rev-parse HEAD)
    local tag_name="backup-${TIMESTAMP}"

    log INFO "Creating backup tag: $tag_name"

    execute git tag -a "$tag_name" -m "Backup before skills.md reversion at $TIMESTAMP" || {
        log WARNING "Tag creation failed, may already exist"
    }

    log SUCCESS "Backup tag created: $tag_name at $current_commit"
    echo "$tag_name"
}

# Export state metadata
export_state_metadata() {
    local metadata_file="$BACKUP_DIR/state_${TIMESTAMP}.json"

    log INFO "Exporting state metadata to: $metadata_file"

    if [[ "$DRY_RUN" == "false" ]]; then
        cat > "$metadata_file" <<EOF
{
  "timestamp": "$TIMESTAMP",
  "backup_date": "$(date -Iseconds)",
  "branch": "$(git rev-parse --abbrev-ref HEAD)",
  "commit": "$(git rev-parse HEAD)",
  "commit_short": "$(git rev-parse --short HEAD)",
  "commit_message": $(git log -1 --pretty=%s | jq -R .),
  "commit_date": "$(git log -1 --pretty=%ci)",
  "repository_root": "$REPO_ROOT",
  "backup_directory": "$BACKUP_DIR",
  "git_status": $(git status --porcelain | jq -R . | jq -s .),
  "branch_list": $(git branch -a | jq -R . | jq -s .),
  "tag_list": $(git tag | jq -R . | jq -s .),
  "remote_list": $(git remote -v | jq -R . | jq -s .)
}
EOF
    fi

    log SUCCESS "State metadata exported: $metadata_file"
    echo "$metadata_file"
}

# Export diff with pre-skills state
export_skills_diff() {
    local diff_file="$BACKUP_DIR/skills_refactor_diff_${TIMESTAMP}.patch"
    local pre_skills_commit="68e0eb7"  # Parent of skills refactor commit

    log INFO "Exporting diff with pre-skills state (from $pre_skills_commit)"

    if [[ "$DRY_RUN" == "false" ]]; then
        git diff "$pre_skills_commit" HEAD > "$diff_file" 2>> "$LOG_FILE"
    fi

    log SUCCESS "Skills refactor diff exported: $diff_file"
    echo "$diff_file"
}

# Create backup summary
create_backup_summary() {
    local branch_name="$1"
    local tag_name="$2"
    local metadata_file="$3"
    local diff_file="$4"
    local summary_file="$BACKUP_DIR/backup_summary_${TIMESTAMP}.txt"

    log INFO "Creating backup summary"

    if [[ "$DRY_RUN" == "false" ]]; then
        cat > "$summary_file" <<EOF
=================================================================
BACKUP SUMMARY
=================================================================

Backup Timestamp: $TIMESTAMP
Backup Date: $(date)

BACKUP ARTIFACTS
----------------
Backup Branch: $branch_name
Backup Tag: $tag_name
Metadata File: $metadata_file
Diff File: $diff_file
Log File: $LOG_FILE

CURRENT STATE
-------------
$(get_current_state)

REPOSITORY STATUS
-----------------
$(git status)

RECENT COMMITS (last 10)
------------------------
$(git log --oneline -10)

VERIFICATION COMMANDS
---------------------
# View backup branch
git checkout $branch_name

# View backup tag
git show $tag_name

# View metadata
cat $metadata_file | jq .

# View diff with pre-skills state
less $diff_file

# Restore to this backup (if needed)
git checkout $branch_name
git checkout -b restored-from-backup-$TIMESTAMP

NEXT STEPS
----------
1. Review this summary: cat $summary_file
2. Verify backup artifacts exist
3. Proceed with reversion: ./scripts/revert-to-pre-skills.sh
4. If reversion fails: ./scripts/rollback-reversion.sh

=================================================================
EOF
    fi

    log SUCCESS "Backup summary created: $summary_file"
    echo "$summary_file"
}

# Main execution
main() {
    parse_args "$@"

    echo -e "${BLUE}==================================================================${NC}"
    echo -e "${BLUE}Standards Repository - State Backup${NC}"
    echo -e "${BLUE}==================================================================${NC}"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}DRY-RUN MODE: No changes will be made${NC}"
        echo ""
    fi

    # Initialize
    init_backup_dir
    verify_git_repo

    # Create backups
    local branch_name=$(create_backup_branch)
    local tag_name=$(create_backup_tag)
    local metadata_file=$(export_state_metadata)
    local diff_file=$(export_skills_diff)

    # Create summary
    local summary_file=$(create_backup_summary "$branch_name" "$tag_name" "$metadata_file" "$diff_file")

    # Final output
    echo ""
    echo -e "${GREEN}==================================================================${NC}"
    echo -e "${GREEN}BACKUP COMPLETED SUCCESSFULLY${NC}"
    echo -e "${GREEN}==================================================================${NC}"
    echo ""
    echo -e "Backup Branch: ${BLUE}$branch_name${NC}"
    echo -e "Backup Tag:    ${BLUE}$tag_name${NC}"
    echo -e "Summary File:  ${BLUE}$summary_file${NC}"
    echo ""

    if [[ "$DRY_RUN" == "false" ]]; then
        echo -e "${YELLOW}Next steps:${NC}"
        echo "  1. Review backup summary: cat $summary_file"
        echo "  2. Proceed with reversion: ./scripts/revert-to-pre-skills.sh"
        echo "  3. If needed, rollback: ./scripts/rollback-reversion.sh"
    fi

    log INFO "Backup process completed"
}

# Run main function
main "$@"
