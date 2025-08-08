#!/bin/bash
# Standards Repository Monitoring Wrapper Script

set -e

REPO_PATH="/home/william/git/standards"
MONITORING_DIR="$REPO_PATH/monitoring"

cd "$REPO_PATH"

echo "🔍 Running repository monitoring..."

# Run analytics collection
if [ -f "$MONITORING_DIR/analytics_collector.py" ]; then
    echo "📊 Collecting analytics..."
    python3 "$MONITORING_DIR/analytics_collector.py"
fi

# Run performance monitoring
if [ -f "$MONITORING_DIR/performance_monitor.py" ]; then
    echo "⚡ Running performance monitoring..."
    python3 "$MONITORING_DIR/performance_monitor.py"
fi

# Run health check
if [ -f "$MONITORING_DIR/health_monitor.py" ]; then
    echo "🏥 Running health check..."
    python3 "$MONITORING_DIR/health_monitor.py"
fi

# Generate automated reports
if [ -f "$MONITORING_DIR/automated_reports.py" ]; then
    echo "📝 Generating reports..."
    python3 "$MONITORING_DIR/automated_reports.py" --scheduled
fi

echo "✅ Monitoring completed successfully!"
