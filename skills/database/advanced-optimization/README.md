# Database Advanced Optimization Skill

Production-ready skill for mastering database optimization across PostgreSQL, MongoDB, and Redis.

## Overview

This skill provides comprehensive guidance on database performance optimization, covering:

- PostgreSQL advanced indexing, query optimization, and VACUUM tuning
- MongoDB sharding strategies, aggregation pipeline optimization, and replica sets
- Redis caching patterns, pub/sub, and cluster configuration
- Query optimization techniques including N+1 problem resolution
- Database scaling strategies (vertical, horizontal, read replicas, sharding)
- Connection pooling best practices
- Monitoring and profiling tools
- Backup and recovery strategies

## Structure

```
skills/database/advanced-optimization/
├── SKILL.md                           # Main skill document (1,406 lines)
├── templates/
│   ├── postgres-optimization.sql      # PostgreSQL optimization queries
│   ├── mongodb-sharding.yaml          # MongoDB sharding configuration
│   ├── redis-caching.py               # Redis caching pattern implementations
│   └── monitoring-dashboard.json      # Grafana monitoring dashboard
├── scripts/
│   └── query-profiling.sh             # Automated database profiling
├── config/
│   └── pgbouncer.ini                  # PgBouncer connection pooling config
└── README.md                          # This file
```

## Quick Start

### 1. Review the Skill

Start with the SKILL.md file:

- Level 1 (5 min): Quick reference and essential checklists
- Level 2 (45 min): Comprehensive implementation guide
- Level 3 (10 min): Deep dive resources and practice exercises

### 2. Use the Templates

All templates are production-ready and can be adapted to your environment:

```bash
# PostgreSQL optimization
psql -U postgres -d myapp -f templates/postgres-optimization.sql

# MongoDB sharding setup
# Review and adapt mongodb-sharding.yaml to your cluster

# Redis caching
python3 templates/redis-caching.py

# Database profiling
./scripts/query-profiling.sh postgresql localhost 5432 postgres myapp
./scripts/query-profiling.sh mongodb localhost 27017 myapp

# PgBouncer setup
cp config/pgbouncer.ini /etc/pgbouncer/
systemctl restart pgbouncer
```

### 3. Import Monitoring Dashboard

Import the Grafana dashboard:

```bash
# Import to Grafana
curl -X POST http://localhost:3000/api/dashboards/db \
  -H "Content-Type: application/json" \
  -d @templates/monitoring-dashboard.json
```

## Key Topics Covered

### PostgreSQL

- B-tree, GIN, and GiST indexes
- EXPLAIN ANALYZE query optimization
- VACUUM and autovacuum tuning
- pg_stat_statements monitoring
- PgBouncer connection pooling
- Performance configuration tuning

### MongoDB

- Shard key selection strategies
- Compound and partial indexes
- Aggregation pipeline optimization
- Replica set configuration
- Zone sharding for geographic distribution
- Profiler and index usage analysis

### Redis

- Cache-aside (lazy loading) pattern
- Write-through and write-behind caching
- Read-through pattern
- Pub/sub and Redis Streams
- Cluster configuration
- Data structures and use cases

### Query Optimization

- N+1 query problem solutions
- Batch loading techniques
- Join optimization
- Connection pooling strategies
- Query profiling and analysis

### Scaling & Monitoring

- Vertical vs horizontal scaling
- Read replicas and sharding
- Monitoring with pg_stat_statements, MongoDB profiler, Redis INFO
- Backup and recovery strategies
- Performance metrics and alerting

## Prerequisites

- Basic SQL knowledge
- Understanding of database design fundamentals
- Familiarity with indexes and query execution
- Command-line experience

## Estimated Time

- **Level 1 Quick Reference**: 5 minutes
- **Level 2 Implementation**: 45 minutes
- **Level 3 Deep Dive**: 10 minutes
- **Total**: 60 minutes

## Related Skills

- Database Design Fundamentals
- API Performance Optimization
- System Architecture Patterns
- Monitoring and Observability

## Version

- **Version**: 1.0.0
- **Last Updated**: 2025-01-17
- **Total Lines**: 3,576 lines (including all templates and scripts)

## License

Part of the Standards Repository - See repository license for details.
