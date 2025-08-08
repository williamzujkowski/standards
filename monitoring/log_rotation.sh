#!/bin/bash

# Log Rotation Script for Monitoring Data
# Rotates and cleans up old monitoring logs, metrics, and reports

set -e

# Configuration
LOG_RETENTION_DAYS=30
METRICS_RETENTION_DAYS=30
HEALTH_RETENTION_DAYS=7
REPORT_RETENTION_DAYS=60

# Base directory
MONITORING_DIR="/home/william/git/standards/monitoring"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "========================================="
echo "Monitoring Data Rotation and Cleanup"
echo "========================================="
echo ""

# Function to rotate logs
rotate_logs() {
    local dir="$1"
    local extension="$2"
    local retention_days="$3"
    local description="$4"
    
    if [ ! -d "$dir" ]; then
        echo -e "${YELLOW}⚠${NC} Directory $dir does not exist, skipping..."
        return
    fi
    
    echo "Processing $description in $dir..."
    
    # Count files before cleanup
    local before_count=$(find "$dir" -type f -name "*.$extension" 2>/dev/null | wc -l)
    
    # Find and remove old files
    local deleted_count=$(find "$dir" -type f -name "*.$extension" -mtime +$retention_days -delete -print 2>/dev/null | wc -l)
    
    # Compress files older than 1 day but within retention
    find "$dir" -type f -name "*.$extension" -mtime +1 -mtime -$retention_days 2>/dev/null | while read -r file; do
        if [[ ! "$file" =~ \.gz$ ]]; then
            gzip -9 "$file" 2>/dev/null && echo "  Compressed: $(basename "$file")"
        fi
    done
    
    # Count files after cleanup
    local after_count=$(find "$dir" -type f \( -name "*.$extension" -o -name "*.$extension.gz" \) 2>/dev/null | wc -l)
    
    echo -e "${GREEN}✓${NC} $description: Deleted $deleted_count old files (>$retention_days days)"
    echo "  Before: $before_count files | After: $after_count files"
    echo ""
}

# Function to keep latest files
keep_latest() {
    local dir="$1"
    local pattern="$2"
    
    if [ ! -d "$dir" ]; then
        return
    fi
    
    # Keep files matching "latest_*" pattern
    find "$dir" -type f -name "$pattern" -mtime +1 2>/dev/null | while read -r file; do
        touch "$file"  # Update timestamp to keep it
        echo "  Preserved: $(basename "$file")"
    done
}

# 1. Rotate log files
echo "1. Rotating log files..."
rotate_logs "$MONITORING_DIR/logs" "log" "$LOG_RETENTION_DAYS" "Log files"

# 2. Rotate metrics
echo "2. Rotating metrics..."
rotate_logs "$MONITORING_DIR/metrics" "json" "$METRICS_RETENTION_DAYS" "Metrics"
keep_latest "$MONITORING_DIR/metrics" "latest_*.json"

# 3. Rotate health reports
echo "3. Rotating health reports..."
rotate_logs "$MONITORING_DIR/health" "json" "$HEALTH_RETENTION_DAYS" "Health reports"
rotate_logs "$MONITORING_DIR/health" "txt" "$HEALTH_RETENTION_DAYS" "Health summaries"
keep_latest "$MONITORING_DIR/health" "latest_*.json"

# 4. Rotate reports
echo "4. Rotating reports..."
rotate_logs "$MONITORING_DIR/reports" "json" "$REPORT_RETENTION_DAYS" "JSON reports"
rotate_logs "$MONITORING_DIR/reports" "txt" "$REPORT_RETENTION_DAYS" "Text reports"

# 5. Clean up empty directories
echo "5. Cleaning up empty directories..."
find "$MONITORING_DIR" -type d -empty -delete 2>/dev/null || true
echo -e "${GREEN}✓${NC} Empty directories removed"
echo ""

# 6. Generate summary
echo "========================================="
echo "Rotation Summary"
echo "========================================="

# Calculate disk usage
if command -v du &> /dev/null; then
    DISK_USAGE=$(du -sh "$MONITORING_DIR" 2>/dev/null | cut -f1)
    echo "Total monitoring directory size: $DISK_USAGE"
fi

# Count remaining files
echo ""
echo "Remaining files by type:"
echo "  Logs: $(find "$MONITORING_DIR/logs" -type f 2>/dev/null | wc -l)"
echo "  Metrics: $(find "$MONITORING_DIR/metrics" -type f 2>/dev/null | wc -l)"
echo "  Health: $(find "$MONITORING_DIR/health" -type f 2>/dev/null | wc -l)"
echo "  Reports: $(find "$MONITORING_DIR/reports" -type f 2>/dev/null | wc -l)"

echo ""
echo -e "${GREEN}✓${NC} Log rotation completed successfully!"
echo ""
echo "Note: Add this script to crontab for automatic rotation:"
echo "  0 2 * * * $MONITORING_DIR/log_rotation.sh >> $MONITORING_DIR/logs/rotation.log 2>&1"