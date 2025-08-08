#!/bin/bash
# Start Monitoring Dashboard

set -e

REPO_PATH="/home/william/git/standards"
MONITORING_DIR="$REPO_PATH/monitoring"

cd "$REPO_PATH"

echo "🚀 Starting monitoring dashboard..."

if [ -f "$MONITORING_DIR/dashboard_server.py" ]; then
    python3 "$MONITORING_DIR/dashboard_server.py" --port 8080 --host localhost
else
    echo "❌ Dashboard server not found!"
    exit 1
fi
