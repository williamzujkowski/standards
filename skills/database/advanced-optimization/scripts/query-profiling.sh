#!/bin/bash

# Database Query Profiling Automation Script
# Version: 1.0.0
# Description: Automated profiling for PostgreSQL and MongoDB

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
OUTPUT_DIR="${SCRIPT_DIR}/../reports"
SLOW_QUERY_THRESHOLD_MS=100

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Create output directory
mkdir -p "${OUTPUT_DIR}"

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# ============================================================================
# POSTGRESQL PROFILING
# ============================================================================

profile_postgresql() {
    local PG_HOST="${1:-localhost}"
    local PG_PORT="${2:-5432}"
    local PG_USER="${3:-postgres}"
    local PG_DB="${4:-postgres}"
    
    log_info "Starting PostgreSQL profiling on ${PG_HOST}:${PG_PORT}/${PG_DB}"
    
    local REPORT_FILE="${OUTPUT_DIR}/postgresql_profile_${TIMESTAMP}.txt"
    
    {
        echo "=================================================="
        echo "PostgreSQL Query Profile Report"
        echo "Generated: $(date)"
        echo "Host: ${PG_HOST}:${PG_PORT}"
        echo "Database: ${PG_DB}"
        echo "=================================================="
        echo ""
        
        # Check if pg_stat_statements is enabled
        echo "Checking pg_stat_statements extension..."
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -t -c \
            "SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements';" | grep -q 1 || {
            echo "WARNING: pg_stat_statements extension not found"
            echo "Run: CREATE EXTENSION pg_stat_statements;"
        }
        echo ""
        
        # Top 20 slowest queries
        echo "=================================================="
        echo "TOP 20 SLOWEST QUERIES BY AVERAGE TIME"
        echo "=================================================="
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -c "
            SELECT
                substring(query, 1, 80) AS short_query,
                calls,
                ROUND(mean_exec_time::numeric, 2) AS avg_ms,
                ROUND(total_exec_time::numeric, 2) AS total_ms,
                ROUND((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS pct
            FROM pg_stat_statements
            WHERE query NOT LIKE '%pg_stat_statements%'
            ORDER BY mean_exec_time DESC
            LIMIT 20;
        "
        echo ""
        
        # Most frequently called queries
        echo "=================================================="
        echo "TOP 20 MOST FREQUENTLY CALLED QUERIES"
        echo "=================================================="
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -c "
            SELECT
                substring(query, 1, 80) AS short_query,
                calls,
                ROUND(mean_exec_time::numeric, 2) AS avg_ms,
                ROUND(total_exec_time::numeric, 2) AS total_ms
            FROM pg_stat_statements
            WHERE query NOT LIKE '%pg_stat_statements%'
            ORDER BY calls DESC
            LIMIT 20;
        "
        echo ""
        
        # Cache hit ratio
        echo "=================================================="
        echo "CACHE HIT RATIO (should be > 90%)"
        echo "=================================================="
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -c "
            SELECT
                'Table Cache Hit Rate' AS metric,
                ROUND(sum(heap_blks_hit) * 100.0 / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0), 2) AS percentage
            FROM pg_statio_user_tables
            UNION ALL
            SELECT
                'Index Cache Hit Rate' AS metric,
                ROUND(sum(idx_blks_hit) * 100.0 / NULLIF(sum(idx_blks_hit) + sum(idx_blks_read), 0), 2) AS percentage
            FROM pg_statio_user_indexes;
        "
        echo ""
        
        # Missing indexes (sequential scans)
        echo "=================================================="
        echo "TABLES WITH HIGH SEQUENTIAL SCANS"
        echo "=================================================="
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -c "
            SELECT
                schemaname,
                tablename,
                seq_scan,
                idx_scan,
                seq_tup_read,
                ROUND(seq_tup_read::numeric / NULLIF(seq_scan, 0), 0) AS avg_seq_tup
            FROM pg_stat_user_tables
            WHERE seq_scan > 100
            ORDER BY seq_tup_read DESC
            LIMIT 20;
        "
        echo ""
        
        # Unused indexes
        echo "=================================================="
        echo "UNUSED INDEXES (consider dropping)"
        echo "=================================================="
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -c "
            SELECT
                schemaname,
                tablename,
                indexname,
                idx_scan,
                pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
            FROM pg_stat_user_indexes
            WHERE idx_scan = 0
                AND indexrelname NOT LIKE '%_pkey'
            ORDER BY pg_relation_size(indexrelid) DESC
            LIMIT 20;
        "
        echo ""
        
        # Table bloat
        echo "=================================================="
        echo "TABLE BLOAT (dead tuples)"
        echo "=================================================="
        psql -h "${PG_HOST}" -p "${PG_PORT}" -U "${PG_USER}" -d "${PG_DB}" -c "
            SELECT
                schemaname,
                tablename,
                n_live_tup,
                n_dead_tup,
                ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_pct,
                last_autovacuum
            FROM pg_stat_user_tables
            WHERE n_dead_tup > 1000
            ORDER BY n_dead_tup DESC
            LIMIT 20;
        "
        
    } | tee "${REPORT_FILE}"
    
    log_info "PostgreSQL profile saved to: ${REPORT_FILE}"
}

# ============================================================================
# MONGODB PROFILING
# ============================================================================

profile_mongodb() {
    local MONGO_HOST="${1:-localhost}"
    local MONGO_PORT="${2:-27017}"
    local MONGO_DB="${3:-test}"
    
    log_info "Starting MongoDB profiling on ${MONGO_HOST}:${MONGO_PORT}/${MONGO_DB}"
    
    local REPORT_FILE="${OUTPUT_DIR}/mongodb_profile_${TIMESTAMP}.txt"
    
    {
        echo "=================================================="
        echo "MongoDB Query Profile Report"
        echo "Generated: $(date)"
        echo "Host: ${MONGO_HOST}:${MONGO_PORT}"
        echo "Database: ${MONGO_DB}"
        echo "=================================================="
        echo ""
        
        # Enable profiler
        echo "Enabling profiler (slow queries > ${SLOW_QUERY_THRESHOLD_MS}ms)..."
        mongosh --host "${MONGO_HOST}" --port "${MONGO_PORT}" "${MONGO_DB}" --quiet --eval "
            db.setProfilingLevel(1, { slowms: ${SLOW_QUERY_THRESHOLD_MS} });
            print('Profiler enabled');
        "
        echo ""
        
        # Wait for some queries to be captured
        log_info "Collecting query samples (10 seconds)..."
        sleep 10
        
        # Recent slow queries
        echo "=================================================="
        echo "RECENT SLOW QUERIES (> ${SLOW_QUERY_THRESHOLD_MS}ms)"
        echo "=================================================="
        mongosh --host "${MONGO_HOST}" --port "${MONGO_PORT}" "${MONGO_DB}" --quiet --eval "
            db.system.profile.find({ millis: { \$gt: ${SLOW_QUERY_THRESHOLD_MS} } })
                .sort({ ts: -1 })
                .limit(20)
                .forEach(function(doc) {
                    print('Time: ' + doc.ts + ' | Duration: ' + doc.millis + 'ms');
                    print('Operation: ' + doc.op + ' | Namespace: ' + doc.ns);
                    print('Query: ' + JSON.stringify(doc.command).substring(0, 200));
                    print('---');
                });
        "
        echo ""
        
        # Queries without index usage (collection scans)
        echo "=================================================="
        echo "QUERIES WITHOUT INDEX USAGE (COLLSCAN)"
        echo "=================================================="
        mongosh --host "${MONGO_HOST}" --port "${MONGO_PORT}" "${MONGO_DB}" --quiet --eval "
            db.system.profile.find({ 'planSummary': /COLLSCAN/ })
                .limit(20)
                .forEach(function(doc) {
                    print('Collection: ' + doc.ns);
                    print('Query: ' + JSON.stringify(doc.command).substring(0, 200));
                    print('Duration: ' + doc.millis + 'ms');
                    print('---');
                });
        "
        echo ""
        
        # Index statistics
        echo "=================================================="
        echo "INDEX USAGE STATISTICS"
        echo "=================================================="
        mongosh --host "${MONGO_HOST}" --port "${MONGO_PORT}" "${MONGO_DB}" --quiet --eval "
            db.getCollectionNames().forEach(function(collName) {
                print('Collection: ' + collName);
                var stats = db[collName].aggregate([{ \$indexStats: {} }]).toArray();
                stats.forEach(function(index) {
                    print('  Index: ' + index.name + ' | Accesses: ' + index.accesses.ops);
                });
                print('');
            });
        "
        echo ""
        
        # Server status
        echo "=================================================="
        echo "SERVER STATUS"
        echo "=================================================="
        mongosh --host "${MONGO_HOST}" --port "${MONGO_PORT}" "${MONGO_DB}" --quiet --eval "
            var status = db.serverStatus();
            print('Connections: ' + status.connections.current + '/' + status.connections.available);
            print('Operations per second: ' + status.opcounters.query + ' queries, ' + status.opcounters.insert + ' inserts');
            print('Memory: ' + (status.mem.resident) + ' MB resident, ' + (status.mem.virtual) + ' MB virtual');
            print('Network: ' + (status.network.bytesIn / 1024 / 1024).toFixed(2) + ' MB in, ' + 
                  (status.network.bytesOut / 1024 / 1024).toFixed(2) + ' MB out');
        "
        echo ""
        
        # Database statistics
        echo "=================================================="
        echo "DATABASE STATISTICS"
        echo "=================================================="
        mongosh --host "${MONGO_HOST}" --port "${MONGO_PORT}" "${MONGO_DB}" --quiet --eval "
            var stats = db.stats();
            print('Collections: ' + stats.collections);
            print('Data Size: ' + (stats.dataSize / 1024 / 1024).toFixed(2) + ' MB');
            print('Index Size: ' + (stats.indexSize / 1024 / 1024).toFixed(2) + ' MB');
            print('Storage Size: ' + (stats.storageSize / 1024 / 1024).toFixed(2) + ' MB');
        "
        
    } | tee "${REPORT_FILE}"
    
    log_info "MongoDB profile saved to: ${REPORT_FILE}"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    echo "Database Query Profiling Tool"
    echo "=============================="
    echo ""
    
    # Parse arguments
    case "${1:-help}" in
        postgresql|pg)
            profile_postgresql "${2:-localhost}" "${3:-5432}" "${4:-postgres}" "${5:-postgres}"
            ;;
        mongodb|mongo)
            profile_mongodb "${2:-localhost}" "${3:-27017}" "${4:-test}"
            ;;
        both)
            profile_postgresql "${2:-localhost}" "${3:-5432}" "${4:-postgres}" "${5:-postgres}"
            profile_mongodb "${6:-localhost}" "${7:-27017}" "${8:-test}"
            ;;
        help|*)
            echo "Usage:"
            echo "  $0 postgresql [host] [port] [user] [database]"
            echo "  $0 mongodb [host] [port] [database]"
            echo "  $0 both [pg_host] [pg_port] [pg_user] [pg_db] [mongo_host] [mongo_port] [mongo_db]"
            echo ""
            echo "Examples:"
            echo "  $0 postgresql localhost 5432 postgres myapp"
            echo "  $0 mongodb localhost 27017 myapp"
            echo "  $0 both"
            exit 0
            ;;
    esac
    
    echo ""
    log_info "Profiling complete. Reports saved to: ${OUTPUT_DIR}"
}

main "$@"
