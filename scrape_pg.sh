#!/bin/bash

# scrape_pg.sh: Scrapes Paul Graham essays using the fabric utility
# Reads URLs from pg_data.json and saves content as Markdown files

set -euo pipefail

# Configuration
readonly POSTS_DIR="posts"
readonly LOG_FILE="scrape_log.txt"
readonly JSON_FILE="pg_data.json"
readonly FABRIC_CMD="$HOME/util/fabric"
readonly DELAY=2

# Colors for output
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly BLUE='\033[0;34m'
readonly NC='\033[0m' # No Color

log() {
    echo "[$(date '+%H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}Error: $*${NC}" >&2
    exit 1
}

success() {
    echo -e "${GREEN}$*${NC}"
}

info() {
    echo -e "${BLUE}$*${NC}"
}

# Validate prerequisites
check_requirements() {
    command -v jq >/dev/null || error "jq is required. Install with: brew install jq"
    [[ -x "$FABRIC_CMD" ]] || error "fabric not found at $FABRIC_CMD"
    [[ -f "$JSON_FILE" ]] || error "Data file $JSON_FILE not found"
    jq empty "$JSON_FILE" 2>/dev/null || error "Invalid JSON in $JSON_FILE"
}

# Sanitize filename by replacing problematic characters
sanitize_filename() {
    echo "$1" | sed 's/[^a-zA-Z0-9 -]/_/g' | sed 's/__*/_/g' | cut -c1-80
}

# Main scraping function
scrape_essay() {
    local url="$1"
    local title="$2"
    local index="$3"
    local total="$4"

    local filename="$(sanitize_filename "$title").md"
    local filepath="$POSTS_DIR/$filename"

    printf "[%d/%d] %s\n" "$index" "$total" "$title"

    if "$FABRIC_CMD" -u "$url" > "$filepath" 2>/dev/null; then
        local size=$(stat -f%z "$filepath" 2>/dev/null || echo "0")
        if [[ $size -gt 0 ]]; then
            success "  ✓ Saved ($size bytes)"
            log "SUCCESS: $title -> $filename ($size bytes)"
            return 0
        else
            rm -f "$filepath"
            error "  ✗ Empty content"
            log "ERROR: Empty content for $title"
            return 1
        fi
    else
        rm -f "$filepath"
        error "  ✗ Failed to scrape"
        log "ERROR: Failed to scrape $title from $url"
        return 1
    fi
}

# Main execution
main() {
    info "Paul Graham Essay Scraper"
    info "========================"

    check_requirements

    local total_entries=$(jq length "$JSON_FILE")
    local success_count=0
    local error_count=0

    # Setup
    mkdir -p "$POSTS_DIR"
    echo "Scraping started at $(date)" > "$LOG_FILE"
    log "Processing $total_entries entries"

    # Process each entry
    for i in $(seq 0 $((total_entries - 1))); do
        local url=$(jq -r ".[$i].url" "$JSON_FILE")
        local title=$(jq -r ".[$i].title" "$JSON_FILE")

        if scrape_essay "$url" "$title" $((i + 1)) "$total_entries"; then
            ((success_count++))
        else
            ((error_count++))
        fi

        # Rate limiting (skip delay on last item)
        if [[ $((i + 1)) -lt $total_entries ]]; then
            sleep "$DELAY"
        fi
    done

    # Summary
    echo
    info "Summary:"
    info "  Total: $total_entries"
    success "  Success: $success_count"
    [[ $error_count -gt 0 ]] && error "  Failed: $error_count" || true
    info "  Files saved to: $POSTS_DIR"

    log "COMPLETE: $success_count successful, $error_count failed"
}

main "$@"
