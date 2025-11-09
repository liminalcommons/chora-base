#!/bin/bash
#
# ============================================================================
# DEPRECATED: This script has been migrated to Python for cross-platform support
# ============================================================================
#
# Use: python scripts/merge-upstream-structure.py [--dry-run] [--no-backup]
# Or:  just merge-upstream
# Or:  just merge-upstream-dry-run
#
# Migration Guide: docs/user-docs/how-to/bash-to-python-migration.md
# Deprecated: v4.3.0 (2025-11-03)
# Removal: v5.0.0 (planned)
#
# Reason: Windows compatibility - this bash script:
#   - Requires 'yq' (YAML parser, separate installation)
#   - Uses Unicode emoji in output (✓✗⚠ℹ🔄)
#   - Uses complex bash string processing
#   - Uses eval for validation commands (security concern)
#
# ============================================================================
#
# merge-upstream-structure.sh - Merge structural updates from chora-base upstream
#
# Purpose: Safely merge structure-only files from chora-base upstream while preserving project content
# Usage: ./scripts/merge-upstream-structure.sh [--dry-run] [--no-backup]  (DEPRECATED)
#        python scripts/merge-upstream-structure.py [OPTIONS]             (RECOMMENDED)
#
# This script:
# 1. Reads .chorabase metadata to identify structure-only files
# 2. Fetches latest from upstream chora-base
# 3. Merges structure-only files using git checkout
# 4. Identifies hybrid files requiring manual merge
# 5. Creates backup and provides rollback mechanism
#
# Exit codes:
#   0 - Success
#   1 - Error (configuration, git operation, etc.)
#   2 - Invalid usage

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CHORABASE_FILE=".chorabase"
UPSTREAM_REMOTE="chora-base"
UPSTREAM_BRANCH="main"
BACKUP_DIR=""
DRY_RUN=false
NO_BACKUP=false

# Statistics
STRUCTURE_FILES_MERGED=0
HYBRID_FILES_FOUND=0
ERRORS=0

#############################################################################
# Helper Functions
#############################################################################

print_header() {
    echo -e "${BLUE}=======================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}=======================================${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

#############################################################################
# Validation Functions
#############################################################################

check_prerequisites() {
    print_header "Checking Prerequisites"

    # Check if in git repository
    if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
        print_error "Not in a git repository"
        exit 1
    fi
    print_success "Git repository detected"

    # Check if .chorabase exists
    if [ ! -f "$CHORABASE_FILE" ]; then
        print_error ".chorabase file not found in repository root"
        print_info "Expected: $CHORABASE_FILE"
        exit 1
    fi
    print_success ".chorabase metadata found"

    # Check if yq is available for YAML parsing
    if ! command -v yq &> /dev/null; then
        print_error "yq is required for YAML parsing"
        print_info "Install: brew install yq (macOS) or apt-get install yq (Linux)"
        exit 1
    fi
    print_success "yq available for YAML parsing"

    echo ""
}

check_upstream_remote() {
    print_header "Checking Upstream Remote"

    # Check if upstream remote exists
    if ! git remote get-url "$UPSTREAM_REMOTE" > /dev/null 2>&1; then
        print_warning "Upstream remote '$UPSTREAM_REMOTE' not found"
        print_info "Adding upstream remote..."

        # Get upstream URL from .chorabase
        UPSTREAM_URL=$(yq eval '.merge.upstream_url' "$CHORABASE_FILE")

        if [ "$UPSTREAM_URL" = "null" ] || [ -z "$UPSTREAM_URL" ]; then
            print_error "No upstream_url found in .chorabase"
            exit 1
        fi

        if [ "$DRY_RUN" = false ]; then
            git remote add "$UPSTREAM_REMOTE" "$UPSTREAM_URL"
            print_success "Added upstream remote: $UPSTREAM_URL"
        else
            print_info "[DRY RUN] Would add remote: $UPSTREAM_URL"
        fi
    else
        UPSTREAM_URL=$(git remote get-url "$UPSTREAM_REMOTE")
        print_success "Upstream remote found: $UPSTREAM_URL"
    fi

    echo ""
}

fetch_upstream() {
    print_header "Fetching Upstream Changes"

    if [ "$DRY_RUN" = false ]; then
        print_info "Fetching from $UPSTREAM_REMOTE..."
        if git fetch "$UPSTREAM_REMOTE" "$UPSTREAM_BRANCH"; then
            print_success "Fetched latest from $UPSTREAM_REMOTE/$UPSTREAM_BRANCH"
        else
            print_error "Failed to fetch from upstream"
            exit 1
        fi
    else
        print_info "[DRY RUN] Would fetch from $UPSTREAM_REMOTE/$UPSTREAM_BRANCH"
    fi

    echo ""
}

#############################################################################
# Backup Functions
#############################################################################

create_backup() {
    if [ "$NO_BACKUP" = true ]; then
        print_info "Skipping backup (--no-backup specified)"
        echo ""
        return
    fi

    print_header "Creating Backup"

    TIMESTAMP=$(date +%Y%m%d-%H%M%S)
    BACKUP_DIR=".chora-backup-$TIMESTAMP"

    if [ "$DRY_RUN" = false ]; then
        mkdir -p "$BACKUP_DIR"

        # Get current git commit
        CURRENT_COMMIT=$(git rev-parse HEAD)
        echo "$CURRENT_COMMIT" > "$BACKUP_DIR/commit.txt"

        # Save current branch
        CURRENT_BRANCH=$(git branch --show-current)
        echo "$CURRENT_BRANCH" > "$BACKUP_DIR/branch.txt"

        print_success "Backup created: $BACKUP_DIR"
        print_info "Current commit: $CURRENT_COMMIT"
        print_info "Current branch: $CURRENT_BRANCH"
    else
        print_info "[DRY RUN] Would create backup: .chora-backup-$TIMESTAMP"
    fi

    echo ""
}

#############################################################################
# Merge Functions
#############################################################################

parse_structure_files() {
    print_header "Parsing Structure-Only Files"

    # Extract structure_only files from .chorabase
    # This handles both file paths and glob patterns
    STRUCTURE_FILES=$(yq eval '.structure_only[]' "$CHORABASE_FILE" | grep -v '^null$' || true)

    if [ -z "$STRUCTURE_FILES" ]; then
        print_warning "No structure_only files found in .chorabase"
        return 1
    fi

    # Count files (for reporting)
    FILE_COUNT=$(echo "$STRUCTURE_FILES" | wc -l | xargs)
    print_success "Found $FILE_COUNT structure-only file patterns"

    echo ""
    return 0
}

expand_glob_patterns() {
    local pattern="$1"

    # Check if pattern contains glob characters
    if [[ "$pattern" == *"*"* ]] || [[ "$pattern" == *"?"* ]]; then
        # Use git ls-tree to expand pattern from upstream
        git ls-tree -r --name-only "$UPSTREAM_REMOTE/$UPSTREAM_BRANCH" "$pattern" 2>/dev/null || true
    else
        # Plain file path
        echo "$pattern"
    fi
}

merge_structure_files() {
    print_header "Merging Structure-Only Files"

    if ! parse_structure_files; then
        return
    fi

    # Process each structure file pattern
    while IFS= read -r pattern; do
        # Skip empty lines and comments
        if [ -z "$pattern" ] || [[ "$pattern" == \#* ]]; then
            continue
        fi

        # Expand glob patterns
        FILES_TO_MERGE=$(expand_glob_patterns "$pattern")

        if [ -z "$FILES_TO_MERGE" ]; then
            print_warning "No files match pattern: $pattern"
            continue
        fi

        # Merge each file
        while IFS= read -r file; do
            if [ -z "$file" ]; then
                continue
            fi

            # Check if file exists in upstream
            if ! git cat-file -e "$UPSTREAM_REMOTE/$UPSTREAM_BRANCH:$file" 2>/dev/null; then
                print_warning "File not in upstream: $file"
                continue
            fi

            if [ "$DRY_RUN" = false ]; then
                # Merge file from upstream
                if git checkout "$UPSTREAM_REMOTE/$UPSTREAM_BRANCH" -- "$file" 2>/dev/null; then
                    print_success "Merged: $file"
                    ((STRUCTURE_FILES_MERGED++))
                else
                    print_error "Failed to merge: $file"
                    ((ERRORS++))
                fi
            else
                print_info "[DRY RUN] Would merge: $file"
                ((STRUCTURE_FILES_MERGED++))
            fi
        done <<< "$FILES_TO_MERGE"

    done <<< "$STRUCTURE_FILES"

    echo ""
}

#############################################################################
# Hybrid File Detection
#############################################################################

detect_hybrid_files() {
    print_header "Detecting Hybrid Files"

    # Extract hybrid file keys from .chorabase
    HYBRID_FILES=$(yq eval '.hybrid | keys | .[]' "$CHORABASE_FILE" 2>/dev/null || true)

    if [ -z "$HYBRID_FILES" ]; then
        print_info "No hybrid files defined in .chorabase"
        echo ""
        return
    fi

    print_warning "The following files require manual merge:"
    echo ""

    while IFS= read -r file; do
        if [ -z "$file" ]; then
            continue
        fi

        # Get merge strategy for this file
        MERGE_STRATEGY=$(yq eval ".hybrid[\"$file\"].merge_strategy" "$CHORABASE_FILE" 2>/dev/null || echo "manual")

        print_info "  $file (strategy: $MERGE_STRATEGY)"
        ((HYBRID_FILES_FOUND++))

    done <<< "$HYBRID_FILES"

    echo ""
    print_info "Hybrid files were NOT automatically merged"
    print_info "Use specialized merge tools in scripts/ directory:"
    echo ""
    print_info "  ./scripts/merge-agents-md.py      # For AGENTS.md"
    print_info "  ./scripts/merge-readme-md.py      # For README.md"
    print_info "  ./scripts/merge-index-md.py       # For INDEX.md"
    echo ""
}

#############################################################################
# Validation
#############################################################################

run_validation() {
    print_header "Running Validation"

    # Check if validation is enabled
    VALIDATE=$(yq eval '.merge.validate_after_merge' "$CHORABASE_FILE" 2>/dev/null || echo "false")

    if [ "$VALIDATE" != "true" ]; then
        print_info "Validation disabled in .chorabase"
        echo ""
        return
    fi

    if [ "$DRY_RUN" = true ]; then
        print_info "[DRY RUN] Would run validation commands"
        echo ""
        return
    fi

    # Get validation commands
    VALIDATION_COMMANDS=$(yq eval '.merge.validation_commands[]' "$CHORABASE_FILE" 2>/dev/null || true)

    if [ -z "$VALIDATION_COMMANDS" ]; then
        print_info "No validation commands defined"
        echo ""
        return
    fi

    print_info "Running validation commands..."
    echo ""

    VALIDATION_FAILED=false

    while IFS= read -r cmd; do
        if [ -z "$cmd" ]; then
            continue
        fi

        print_info "Running: $cmd"

        if eval "$cmd"; then
            print_success "Passed"
        else
            print_error "Failed: $cmd"
            VALIDATION_FAILED=true
        fi
        echo ""
    done <<< "$VALIDATION_COMMANDS"

    if [ "$VALIDATION_FAILED" = true ]; then
        print_warning "Some validation checks failed"
        print_info "Review errors above and fix before committing"
        echo ""
    else
        print_success "All validation checks passed"
        echo ""
    fi
}

#############################################################################
# Summary
#############################################################################

print_summary() {
    print_header "Merge Summary"

    echo -e "${GREEN}Structure files merged:${NC} $STRUCTURE_FILES_MERGED"
    echo -e "${YELLOW}Hybrid files requiring manual merge:${NC} $HYBRID_FILES_FOUND"
    echo -e "${RED}Errors:${NC} $ERRORS"
    echo ""

    if [ "$DRY_RUN" = true ]; then
        print_info "DRY RUN - No changes were made"
        echo ""
        print_info "To apply changes, run without --dry-run:"
        print_info "  ./scripts/merge-upstream-structure.sh"
        echo ""
    else
        if [ -n "$BACKUP_DIR" ]; then
            print_info "Backup created: $BACKUP_DIR"
            echo ""
            print_info "To rollback, run:"
            print_info "  git reset --hard \$(cat $BACKUP_DIR/commit.txt)"
            echo ""
        fi

        if [ $STRUCTURE_FILES_MERGED -gt 0 ]; then
            print_info "Next steps:"
            print_info "  1. Review merged changes: git status"
            print_info "  2. Handle hybrid files (see above)"
            print_info "  3. Run tests: just test"
            print_info "  4. Commit changes: git add . && git commit -m 'chore: Merge structural updates from upstream'"
            echo ""
        fi
    fi

    if [ $ERRORS -gt 0 ]; then
        print_warning "Merge completed with errors - review above"
        exit 1
    fi
}

#############################################################################
# Main
#############################################################################

show_usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Merge structural updates from chora-base upstream while preserving project content.

OPTIONS:
    --dry-run       Show what would be merged without making changes
    --no-backup     Skip creating backup before merge
    -h, --help      Show this help message

EXAMPLES:
    # Preview what would be merged
    $0 --dry-run

    # Merge structural updates
    $0

    # Merge without backup (not recommended)
    $0 --no-backup

DESCRIPTION:
    This script reads .chorabase metadata to identify structure-only files,
    fetches the latest from upstream chora-base, and merges those files while
    preserving your project-specific content.

    Hybrid files (AGENTS.md, README.md, etc.) are detected but NOT automatically
    merged. Use specialized merge tools for those files.

SAFETY FEATURES:
    - Creates backup before merge (with commit hash)
    - Dry-run mode to preview changes
    - Validation after merge (if configured in .chorabase)
    - Clear rollback instructions

MORE INFO:
    See: docs/user-docs/how-to/upgrade-structure-from-upstream.md

EOF
}

main() {
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --dry-run)
                DRY_RUN=true
                shift
                ;;
            --no-backup)
                NO_BACKUP=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                echo "Unknown option: $1"
                show_usage
                exit 2
                ;;
        esac
    done

    print_header "Merge Upstream Structure"

    if [ "$DRY_RUN" = true ]; then
        print_warning "DRY RUN MODE - No changes will be made"
        echo ""
    fi

    # Run merge workflow
    check_prerequisites
    check_upstream_remote
    fetch_upstream
    create_backup
    merge_structure_files
    detect_hybrid_files
    run_validation
    print_summary

    print_success "Merge workflow completed successfully"
}

# Run main function
main "$@"
