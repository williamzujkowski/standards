#!/bin/bash
# Setup test database and run integration tests

set -euo pipefail

# Configuration
COMPOSE_FILE="${COMPOSE_FILE:-docker-compose.test.yml}"
TEST_PATH="${TEST_PATH:-tests/integration/}"
TIMEOUT="${TIMEOUT:-60}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $*"
}

error() {
    echo -e "${RED}[ERROR]${NC} $*" >&2
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

cleanup() {
    log "Cleaning up test environment..."
    docker-compose -f "$COMPOSE_FILE" down -v --remove-orphans
}

# Trap to ensure cleanup on exit
trap cleanup EXIT INT TERM

# Start test environment
log "Starting test environment..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for services to be healthy
log "Waiting for services to be ready..."
end=$((SECONDS + TIMEOUT))

while [ $SECONDS -lt $end ]; do
    if docker-compose -f "$COMPOSE_FILE" ps | grep -q "healthy"; then
        log "Services are healthy"
        break
    fi
    sleep 2
done

if [ $SECONDS -ge $end ]; then
    error "Services failed to become healthy within ${TIMEOUT}s"
    docker-compose -f "$COMPOSE_FILE" logs
    exit 1
fi

# Run database migrations
log "Running database migrations..."
if ! docker-compose -f "$COMPOSE_FILE" exec -T app python manage.py migrate; then
    error "Migration failed"
    exit 1
fi

# Seed test data if needed
if [ -f "tests/fixtures/seed.sql" ]; then
    log "Seeding test data..."
    docker-compose -f "$COMPOSE_FILE" exec -T postgres \
        psql -U test -d testdb < tests/fixtures/seed.sql
fi

# Run integration tests
log "Running integration tests..."
if docker-compose -f "$COMPOSE_FILE" exec -T app pytest "$TEST_PATH" -v --tb=short; then
    log "Integration tests passed!"
    exit 0
else
    error "Integration tests failed"
    docker-compose -f "$COMPOSE_FILE" logs app
    exit 1
fi
