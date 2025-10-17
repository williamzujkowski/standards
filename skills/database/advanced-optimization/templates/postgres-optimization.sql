-- PostgreSQL Advanced Optimization Queries and Index Strategies
-- Version: 1.0.0
-- Description: Production-ready SQL queries for database optimization

-- ============================================================================
-- INDEX MANAGEMENT
-- ============================================================================

-- Create covering index with INCLUDE clause (PostgreSQL 11+)
CREATE INDEX CONCURRENTLY idx_orders_covering
ON orders(user_id, created_at DESC)
INCLUDE (status, total_amount, items_count);

-- Partial index for frequently filtered data
CREATE INDEX CONCURRENTLY idx_active_users
ON users(email)
WHERE status = 'active' AND deleted_at IS NULL;

-- Composite index (order matters: Equality, Sort, Range)
CREATE INDEX CONCURRENTLY idx_orders_esr
ON orders(status, created_at DESC, total_amount);

-- GIN index for full-text search
CREATE INDEX CONCURRENTLY idx_products_fts
ON products USING GIN(to_tsvector('english', name || ' ' || description));

-- GIN index for JSONB queries
CREATE INDEX CONCURRENTLY idx_users_metadata
ON users USING GIN(metadata jsonb_path_ops);

-- GiST index for range types
CREATE INDEX CONCURRENTLY idx_bookings_daterange
ON bookings USING GiST(date_range);

-- Find missing indexes (long sequential scans)
SELECT
    schemaname,
    tablename,
    seq_scan,
    seq_tup_read,
    idx_scan,
    seq_tup_read / NULLIF(seq_scan, 0) AS avg_seq_tup_read
FROM pg_stat_user_tables
WHERE seq_scan > 0
ORDER BY seq_tup_read DESC
LIMIT 20;

-- Find unused indexes (consider dropping)
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size
FROM pg_stat_user_indexes
WHERE idx_scan = 0
    AND indexrelname NOT LIKE '%_pkey'
ORDER BY pg_relation_size(indexrelid) DESC;

-- Check index bloat
SELECT
    schemaname,
    tablename,
    indexname,
    pg_size_pretty(pg_relation_size(indexrelid)) AS index_size,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY pg_relation_size(indexrelid) DESC
LIMIT 20;

-- ============================================================================
-- QUERY PERFORMANCE ANALYSIS
-- ============================================================================

-- Enable pg_stat_statements extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 20 slowest queries by average execution time
SELECT
    substring(query, 1, 100) AS short_query,
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_time_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_time_ms,
    ROUND(max_exec_time::numeric, 2) AS max_time_ms,
    ROUND(stddev_exec_time::numeric, 2) AS stddev_time_ms,
    ROUND((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS pct_total_time
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Most frequently executed queries
SELECT
    substring(query, 1, 100) AS short_query,
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_time_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_time_ms,
    rows
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY calls DESC
LIMIT 20;

-- Queries consuming most total time
SELECT
    substring(query, 1, 100) AS short_query,
    calls,
    ROUND(total_exec_time::numeric, 2) AS total_time_ms,
    ROUND(mean_exec_time::numeric, 2) AS mean_time_ms,
    ROUND((100 * total_exec_time / sum(total_exec_time) OVER ())::numeric, 2) AS pct_total_time
FROM pg_stat_statements
WHERE query NOT LIKE '%pg_stat_statements%'
ORDER BY total_exec_time DESC
LIMIT 20;

-- Reset pg_stat_statements
SELECT pg_stat_statements_reset();

-- ============================================================================
-- MONITORING AND DIAGNOSTICS
-- ============================================================================

-- Cache hit ratio (should be > 90%)
SELECT
    'cache hit rate' AS metric,
    ROUND(
        sum(heap_blks_hit) * 100.0 / NULLIF(sum(heap_blks_hit) + sum(heap_blks_read), 0),
        2
    ) AS percentage
FROM pg_statio_user_tables
UNION ALL
SELECT
    'index hit rate' AS metric,
    ROUND(
        sum(idx_blks_hit) * 100.0 / NULLIF(sum(idx_blks_hit) + sum(idx_blks_read), 0),
        2
    ) AS percentage
FROM pg_statio_user_indexes;

-- Connection statistics
SELECT
    state,
    count(*) AS connections,
    max(now() - state_change) AS max_duration
FROM pg_stat_activity
WHERE pid != pg_backend_pid()
GROUP BY state
ORDER BY count(*) DESC;

-- Active queries (running > 30 seconds)
SELECT
    pid,
    now() - pg_stat_activity.query_start AS duration,
    state,
    query
FROM pg_stat_activity
WHERE state != 'idle'
    AND now() - pg_stat_activity.query_start > interval '30 seconds'
ORDER BY duration DESC;

-- Blocking queries
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement,
    blocked_activity.application_name AS blocked_application
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
    AND blocking_locks.page IS NOT DISTINCT FROM blocked_locks.page
    AND blocking_locks.tuple IS NOT DISTINCT FROM blocked_locks.tuple
    AND blocking_locks.virtualxid IS NOT DISTINCT FROM blocked_locks.virtualxid
    AND blocking_locks.transactionid IS NOT DISTINCT FROM blocked_locks.transactionid
    AND blocking_locks.classid IS NOT DISTINCT FROM blocked_locks.classid
    AND blocking_locks.objid IS NOT DISTINCT FROM blocked_locks.objid
    AND blocking_locks.objsubid IS NOT DISTINCT FROM blocked_locks.objsubid
    AND blocking_locks.pid != blocked_locks.pid
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;

-- ============================================================================
-- VACUUM AND MAINTENANCE
-- ============================================================================

-- Table bloat and dead tuples
SELECT
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio_pct,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Tables needing vacuum
SELECT
    schemaname || '.' || tablename AS table_name,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
    n_dead_tup,
    n_live_tup,
    ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup, 0), 2) AS dead_ratio_pct,
    last_autovacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
    AND ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup, 0), 2) > 10
ORDER BY n_dead_tup DESC;

-- Perform VACUUM ANALYZE on specific table
VACUUM (ANALYZE, VERBOSE) orders;

-- ============================================================================
-- DATABASE SIZE AND GROWTH
-- ============================================================================

-- Database sizes
SELECT
    datname AS database_name,
    pg_size_pretty(pg_database_size(datname)) AS size
FROM pg_database
ORDER BY pg_database_size(datname) DESC;

-- Largest tables
SELECT
    schemaname || '.' || tablename AS table_name,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
    pg_size_pretty(pg_relation_size(schemaname||'.'||tablename)) AS table_size,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS indexes_size
FROM pg_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;

-- Table growth over time (requires logging)
-- Create monitoring table
CREATE TABLE IF NOT EXISTS table_size_history (
    measured_at TIMESTAMP DEFAULT now(),
    table_name TEXT,
    total_size BIGINT,
    table_size BIGINT,
    indexes_size BIGINT
);

-- Populate monitoring data
INSERT INTO table_size_history (table_name, total_size, table_size, indexes_size)
SELECT
    schemaname || '.' || tablename,
    pg_total_relation_size(schemaname||'.'||tablename),
    pg_relation_size(schemaname||'.'||tablename),
    pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)
FROM pg_tables;

-- ============================================================================
-- CONFIGURATION RECOMMENDATIONS
-- ============================================================================

-- Show current configuration
SELECT name, setting, unit, context, source
FROM pg_settings
WHERE name IN (
    'shared_buffers',
    'effective_cache_size',
    'work_mem',
    'maintenance_work_mem',
    'max_connections',
    'max_parallel_workers_per_gather',
    'random_page_cost',
    'effective_io_concurrency',
    'wal_buffers',
    'checkpoint_completion_target'
)
ORDER BY name;

-- Recommended settings for typical web application (16GB RAM)
-- Add to postgresql.conf:
/*
shared_buffers = 4GB
effective_cache_size = 12GB
work_mem = 16MB
maintenance_work_mem = 512MB
max_connections = 200
max_parallel_workers_per_gather = 4
random_page_cost = 1.1
effective_io_concurrency = 200
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 2GB
min_wal_size = 512MB
*/
