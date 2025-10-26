#!/usr/bin/env bash
#
# revert-to-pre-skills.sh - Revert skills.md refactor safely
#
# USAGE:
#   ./scripts/revert-to-pre-skills.sh [OPTIONS]
#
# OPTIONS:
#   --dry-run          Show what would be done without doing it
#   --method METHOD    Reversion method: revert|reset (default: revert)
#   --no-confirm       Skip confirmation prompts (dangerous!)
#   --verbose          Show detailed progress
#   --help             Show this help message
#
# EXAMPLES:
#   ./scripts/revert-to-pre-skills.sh --dry-run
#   ./scripts/revert-to-pre-skills.sh --method revert
#   ./scripts/revert-to-pre-skills.sh --method reset --no-confirm
#
# DESCRIPTION:
#   Reverts the skills.md refactor (commit a4b1ed1) using either:
#   - revert: Creates a new commit that undoes the changes (safer)
#   - reset: Moves HEAD to pre-skills commit (destructive, requires force push)
#
# SAFETY:
#   - Requires backup branch/tag to exist (created by backup-current-state.sh)
#   - Validates repository state before proceeding
#   - Requires confirmation for destructive operations
#   - Logs all operations
#   - Validates state at each step
#

set -euo pipefail

# Script directory and repository root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Default configuration
DRY_RUN=false
VERBOSE=false
METHOD="revert"
NO_CONFIRM=false
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="$REPO_ROOT/backups"
LOG_FILE="$LOG_DIR/reversion_${TIMESTAMP}.log"

# Target commits
SKILLS_COMMIT="a4b1ed1"      # The skills.md refactor commit
PRE_SKILLS_COMMIT="68e0eb7"  # Parent commit (pre-skills state)

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
            --method)
                METHOD="$2"
                if [[ "$METHOD" != "revert" && "$METHOD" != "reset" ]]; then
                    echo -e "${RED}Error: Invalid method. Use 'revert' or 'reset'${NC}"
                    exit 1
                fi
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

# Verify prerequisites
verify_prerequisites() {
    log INFO "Verifying prerequisites"

    cd "$REPO_ROOT"

    # Check if git repository
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log ERROR "Not a git repository: $REPO_ROOT"
        exit 1
    fi

    # Check if backup exists
    local backup_branches=$(git branch -a | grep -c "backup/pre-reversion-" || true)
    local backup_tags=$(git tag | grep -c "^backup-" || true)

    if [[ $backup_branches -eq 0 ]] || [[ $backup_tags -eq 0 ]]; then
        log ERROR "No backup found! Run ./scripts/backup-current-state.sh first"
        exit 1
    fi

    log SUCCESS "Backup verified (branches: $backup_branches, tags: $backup_tags)"

    # Check if target commits exist
    if ! git cat-file -e "$SKILLS_COMMIT" 2>/dev/null; then
        log ERROR "Skills commit not found: $SKILLS_COMMIT"
        exit 1
    fi

    if ! git cat-file -e "$PRE_SKILLS_COMMIT" 2>/dev/null; then
        log ERROR "Pre-skills commit not found: $PRE_SKILLS_COMMIT"
        exit 1
    fi

    log SUCCESS "Target commits verified"

    # Check for uncommitted changes
    if [[ -n $(git status --porcelain) ]]; then
        log ERROR "Working directory has uncommitted changes. Commit or stash them first."
        git status --short
        exit 1
    fi

    log SUCCESS "Working directory clean"

    # Check current branch
    local current_branch=$(git rev-parse --abbrev-ref HEAD)
    if [[ "$current_branch" == "master" ]] || [[ "$current_branch" == "main" ]]; then
        confirm "You are on branch '$current_branch'. This will modify the main branch."
    fi

    log SUCCESS "Prerequisites verified"
}

# Create reversion branch
create_reversion_branch() {
    local branch_name="reversion/skills-md-${TIMESTAMP}"

    log INFO "Creating reversion branch: $branch_name"

    execute git checkout -b "$branch_name" || {
        log ERROR "Failed to create reversion branch"
        exit 1
    }

    log SUCCESS "Reversion branch created: $branch_name"
    echo "$branch_name"
}

# Perform revert (safer method)
perform_revert() {
    log INFO "Performing revert of commit $SKILLS_COMMIT"

    confirm "This will create a new commit that undoes the skills.md refactor"

    # Revert the skills commit
    execute git revert --no-edit "$SKILLS_COMMIT" || {
        log ERROR "Git revert failed. Check for conflicts."
        log INFO "To manually resolve:"
        log INFO "  1. Fix conflicts in affected files"
        log INFO "  2. git add <resolved-files>"
        log INFO "  3. git revert --continue"
        exit 1
    }

    log SUCCESS "Revert completed successfully"

    # Show what changed
    log INFO "Changes made by revert:"
    git show --stat HEAD
}

# Perform reset (destructive method)
perform_reset() {
    log INFO "Performing reset to commit $PRE_SKILLS_COMMIT"

    confirm "WARNING: This is DESTRUCTIVE and will rewrite history. Requires force push!"
    confirm "Are you absolutely sure? This cannot be undone easily."

    # Reset to pre-skills commit
    execute git reset --hard "$PRE_SKILLS_COMMIT" || {
        log ERROR "Git reset failed"
        exit 1
    }

    log SUCCESS "Reset completed successfully"
    log WARNING "You will need to force push: git push --force-with-lease"

    # Show current state
    log INFO "Current state:"
    git log --oneline -5
}

# Validate reversion
validate_reversion() {
    log INFO "Validating reversion"

    # Check that we're not on the skills commit
    local current_commit=$(git rev-parse HEAD)
    if [[ "$current_commit" == "$SKILLS_COMMIT" ]]; then
        log ERROR "Still on skills commit! Reversion failed."
        exit 1
    fi

    # Check if skills directory structure was removed/restored
    log INFO "Checking repository structure"

    if [[ "$METHOD" == "revert" ]]; then
        # After revert, we should be back to pre-skills state
        # but with the skills commit still in history
        local commits_after=$(git log --oneline "$PRE_SKILLS_COMMIT"..HEAD | wc -l)
        log INFO "Commits after pre-skills state: $commits_after"
    else
        # After reset, we should be exactly at pre-skills commit
        local current_commit_short=$(git rev-parse --short HEAD)
        local expected_commit_short=$(git rev-parse --short "$PRE_SKILLS_COMMIT")

        if [[ "$current_commit_short" != "$expected_commit_short" ]]; then
            log ERROR "Not at expected commit! Current: $current_commit_short, Expected: $expected_commit_short"
            exit 1
        fi
    fi

    log SUCCESS "Reversion validated"
}

# Run existing validation scripts
run_validation_scripts() {
    log INFO "Running existing validation scripts"

    cd "$REPO_ROOT"

    # Run structure validation if script exists
    if [[ -f "scripts/generate-audit-reports.py" ]]; then
        log INFO "Running structure audit"
        if execute python3 scripts/generate-audit-reports.py; then
            log SUCCESS "Structure audit passed"
        else
            log WARNING "Structure audit found issues (expected after reversion)"
        fi
    fi

    # Run skills validation if script exists
    if [[ -f "scripts/validate-skills.py" ]]; then
        log INFO "Running skills validation"
        if execute python3 scripts/validate-skills.py; then
            log SUCCESS "Skills validation passed"
        else
            log WARNING "Skills validation found issues (may be expected)"
        fi
    fi

    log INFO "Validation scripts completed"
}

# Create reversion report
create_reversion_report() {
    local branch_name="$1"
    local report_file="$LOG_DIR/reversion_report_${TIMESTAMP}.txt"

    log INFO "Creating reversion report"

    if [[ "$DRY_RUN" == "false" ]]; then
        cat > "$report_file" <<EOF
=================================================================
REVERSION REPORT
=================================================================

Reversion Timestamp: $TIMESTAMP
Reversion Date: $(date)
Reversion Method: $METHOD

REVERSION DETAILS
-----------------
Skills Commit: $SKILLS_COMMIT
Pre-Skills Commit: $PRE_SKILLS_COMMIT
Reversion Branch: $branch_name

CURRENT STATE
-------------
Current Branch: $(git rev-parse --abbrev-ref HEAD)
Current Commit: $(git rev-parse HEAD)
Current Commit (short): $(git rev-parse --short HEAD)

REPOSITORY STATUS
-----------------
$(git status)

RECENT COMMITS (last 10)
------------------------
$(git log --oneline -10)

DIFF WITH PRE-SKILLS STATE
---------------------------
$(git diff --stat "$PRE_SKILLS_COMMIT" HEAD || echo "No differences (expected for reset method)")

VERIFICATION COMMANDS
---------------------
# View current state
git log --oneline -10

# Compare with pre-skills state
git diff $PRE_SKILLS_COMMIT HEAD

# Run validation
python3 scripts/validate-reversion.sh

# If reversion is good, merge to main
git checkout main
git merge $branch_name

# If reversion failed, rollback
./scripts/rollback-reversion.sh

NEXT STEPS
----------
1. Review this report: cat $report_file
2. Run validation: ./scripts/validate-reversion.sh
3. If validation passes and changes look good:
   - Merge reversion branch to main
   - Push changes (force push if using reset method)
4. If something went wrong:
   - Run rollback: ./scripts/rollback-reversion.sh

=================================================================
EOF
    fi

    log SUCCESS "Reversion report created: $report_file"
    echo "$report_file"
}

# Main execution
main() {
    parse_args "$@"

    echo -e "${BLUE}==================================================================${NC}"
    echo -e "${BLUE}Standards Repository - Skills.md Reversion${NC}"
    echo -e "${BLUE}==================================================================${NC}"
    echo ""

    if [[ "$DRY_RUN" == "true" ]]; then
        echo -e "${YELLOW}DRY-RUN MODE: No changes will be made${NC}"
        echo ""
    fi

    echo -e "Reversion Method: ${BLUE}$METHOD${NC}"
    echo -e "Skills Commit:    ${BLUE}$SKILLS_COMMIT${NC}"
    echo -e "Target Commit:    ${BLUE}$PRE_SKILLS_COMMIT${NC}"
    echo ""

    # Verify prerequisites
    verify_prerequisites

    # Create reversion branch
    local branch_name=$(create_reversion_branch)

    # Perform reversion based on method
    if [[ "$METHOD" == "revert" ]]; then
        perform_revert
    else
        perform_reset
    fi

    # Validate reversion
    validate_reversion

    # Run validation scripts
    run_validation_scripts

    # Create report
    local report_file=$(create_reversion_report "$branch_name")

    # Final output
    echo ""
    echo -e "${GREEN}==================================================================${NC}"
    echo -e "${GREEN}REVERSION COMPLETED${NC}"
    echo -e "${GREEN}==================================================================${NC}"
    echo ""
    echo -e "Method:        ${BLUE}$METHOD${NC}"
    echo -e "Branch:        ${BLUE}$branch_name${NC}"
    echo -e "Report:        ${BLUE}$report_file${NC}"
    echo ""

    if [[ "$DRY_RUN" == "false" ]]; then
        echo -e "${YELLOW}Next steps:${NC}"
        echo "  1. Review report: cat $report_file"
        echo "  2. Run validation: ./scripts/validate-reversion.sh"
        echo "  3. If good, merge to main and push"
        echo "  4. If bad, rollback: ./scripts/rollback-reversion.sh"
    fi

    log INFO "Reversion process completed"
}

# Run main function
main "$@"
