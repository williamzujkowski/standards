---
name: database-advanced-optimization
category: database
difficulty: advanced
estimated_time: 60 minutes
prerequisites:
  - Basic SQL knowledge
  - Database design fundamentals
  - Understanding of indexes and query execution
tags:
  - postgresql
  - mongodb
  - redis
  - performance
  - optimization
  - scaling
  - caching
  - sharding
learning_objectives:
  - Master database-specific optimization techniques
  - Implement effective caching strategies
  - Design scalable database architectures
  - Optimize query performance across multiple database systems
  - Configure connection pooling and monitoring
version: 1.0.0
last_updated: 2025-01-17
---

# Database Advanced Optimization

## Level 1: Quick Reference (5 minutes)

### Database Selection Guide

**Use SQL (PostgreSQL) when:**

- ACID compliance is critical
- Complex joins and transactions required
- Data has clear relational structure
- Strong consistency needed
- Rich query capabilities required

**Use NoSQL (MongoDB) when:**

- Flexible schema needed
- Horizontal scaling is priority
- Document-oriented data model fits
- High write throughput required
- Eventual consistency acceptable

**Use In-Memory (Redis) when:**

- Sub-millisecond latency required
- Caching layer needed
- Real-time features (pub/sub, streams)
- Session management
- Rate limiting or counters

### Common Optimization Patterns

```sql
-- PostgreSQL: Create covering index
CREATE INDEX idx_orders_user_date ON orders(user_id, created_at)
INCLUDE (status, total_amount);

-- PostgreSQL: Analyze query plan
EXPLAIN (ANALYZE, BUFFERS)
SELECT * FROM orders WHERE user_id = 123;
```

```javascript
// MongoDB: Create compound index
db.orders.createIndex({ userId: 1, createdAt: -1 }, { background: true });

// MongoDB: Use aggregation pipeline efficiently
db.orders.aggregate([
  { $match: { status: "pending" } },
  { $sort: { createdAt: -1 } },
  { $limit: 100 }
]);
```

```python
# Redis: Implement cache-aside pattern
def get_user(user_id):
    cache_key = f"user:{user_id}"
    user = redis.get(cache_key)

    if user is None:
        user = db.query("SELECT * FROM users WHERE id = %s", user_id)
        redis.setex(cache_key, 3600, json.dumps(user))

    return json.loads(user)
```

### Essential Optimization Checklist

#### PostgreSQL

- [ ] Create appropriate indexes (B-tree, GIN, GiST)
- [ ] Analyze query plans with EXPLAIN ANALYZE
- [ ] Configure autovacuum appropriately
- [ ] Set up connection pooling (PgBouncer)
- [ ] Monitor with pg_stat_statements
- [ ] Optimize shared_buffers and work_mem
- [ ] Configure appropriate WAL settings

#### MongoDB

- [ ] Design effective shard keys
- [ ] Create compound indexes for common queries
- [ ] Enable profiler for slow queries
- [ ] Configure replica sets for read scaling
- [ ] Optimize aggregation pipelines
- [ ] Set appropriate write concerns
- [ ] Monitor with MongoDB Compass/Atlas

#### Redis

- [ ] Implement appropriate caching strategy
- [ ] Configure maxmemory and eviction policies
- [ ] Use pipelining for bulk operations
- [ ] Set appropriate TTLs
- [ ] Monitor memory usage and hit rates
- [ ] Configure persistence (RDB/AOF) appropriately
- [ ] Use Redis Cluster for scaling

### Quick Wins

**Immediate Impact:**

1. Add indexes for frequently queried columns
2. Enable query result caching
3. Implement connection pooling
4. Add Redis cache layer for hot data
5. Optimize N+1 queries with batch loading

**Performance Monitoring:**

```bash
# PostgreSQL query stats
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC LIMIT 10;

# MongoDB profiler
db.setProfilingLevel(1, { slowms: 100 });
db.system.profile.find().sort({ ts: -1 }).limit(10);

# Redis stats
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses'
```

---

## Level 2: Implementation Guide (45 minutes)

### PostgreSQL Advanced Optimization

#### Index Strategies

PostgreSQL supports multiple index types, each optimized for specific use cases:

**B-tree Indexes (Default)**

```sql
-- Standard B-tree index for equality and range queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_orders_date ON orders(created_at DESC);

-- Composite index (column order matters!)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial index for specific conditions
CREATE INDEX idx_active_users ON users(email)
WHERE status = 'active';

-- Covering index (includes additional columns)
CREATE INDEX idx_orders_covering ON orders(user_id, created_at)
INCLUDE (status, total_amount, items_count);
```

**GIN Indexes (Full-text and Array Search)**

```sql
-- Full-text search
CREATE INDEX idx_products_search ON products
USING GIN(to_tsvector('english', name || ' ' || description));

-- Array containment
CREATE INDEX idx_posts_tags ON posts USING GIN(tags);

-- JSONB queries
CREATE INDEX idx_users_metadata ON users USING GIN(metadata jsonb_path_ops);

-- Query examples
SELECT * FROM products
WHERE to_tsvector('english', name || ' ' || description)
@@ to_tsquery('english', 'laptop');

SELECT * FROM posts WHERE tags @> ARRAY['postgresql', 'optimization'];
SELECT * FROM users WHERE metadata @> '{"plan": "premium"}';
```

**GiST Indexes (Geometric and Range Data)**

```sql
-- Range types
CREATE INDEX idx_bookings_dates ON bookings USING GiST(date_range);

-- Geometric data
CREATE INDEX idx_locations_point ON locations USING GiST(coordinates);

-- Full-text (alternative to GIN)
CREATE INDEX idx_documents_text ON documents USING GiST(content_tsvector);

-- Query examples
SELECT * FROM bookings
WHERE date_range && '[2025-01-01, 2025-01-31)'::daterange;
```

#### Query Optimization with EXPLAIN ANALYZE


```sql
-- Basic EXPLAIN
EXPLAIN SELECT * FROM orders WHERE user_id = 123;

-- EXPLAIN with execution statistics
EXPLAIN (ANALYZE, BUFFERS, VERBOSE)
SELECT o.*, u.email
FROM orders o
JOIN users u ON o.user_id = u.id
WHERE o.created_at > NOW() - INTERVAL '30 days'
ORDER BY o.created_at DESC
LIMIT 100;

-- Key metrics to analyze:
-- 1. Seq Scan → should be Index Scan for large tables
-- 2. Actual time vs Estimated rows (accuracy of statistics)
-- 3. Buffers: shared hit/read ratio (cache effectiveness)
-- 4. Execution time breakdown by node
```

**Understanding EXPLAIN Output:**

```
                                                    QUERY PLAN
-------------------------------------------------------------------------------------------------------------------
 Limit  (cost=0.56..45.23 rows=100 width=148) (actual time=0.032..1.234 rows=100 loops=1)
   ->  Nested Loop  (cost=0.56..8920.45 rows=19965 width=148) (actual time=0.031..1.189 rows=100 loops=1)
         ->  Index Scan Backward using idx_orders_created_at on orders o
             (cost=0.42..4567.89 rows=19965 width=120) (actual time=0.018..0.456 rows=100 loops=1)
               Index Cond: (created_at > (now() - '30 days'::interval))
               Buffers: shared hit=234
         ->  Index Scan using users_pkey on users u
             (cost=0.14..0.21 rows=1 width=28) (actual time=0.006..0.006 rows=1 loops=100)
               Index Cond: (id = o.user_id)
               Buffers: shared hit=300
 Planning Time: 0.234 ms
 Execution Time: 1.567 ms
```

**Optimization Decisions:**

- Index Scan = Good (using indexes)
- Buffers shared hit = Good (data in cache)
- Nested Loop = Appropriate for small result sets
- Hash Join = Better for large joins

#### VACUUM and Maintenance

```sql
-- Manual VACUUM (reclaim space, update statistics)
VACUUM ANALYZE orders;

-- Full VACUUM (locks table, reclaims more space)
VACUUM FULL orders;

-- Autovacuum tuning (postgresql.conf)
autovacuum = on
autovacuum_max_workers = 4
autovacuum_naptime = 10s
autovacuum_vacuum_threshold = 50
autovacuum_vacuum_scale_factor = 0.1
autovacuum_analyze_threshold = 50
autovacuum_analyze_scale_factor = 0.05

-- Per-table autovacuum settings
ALTER TABLE orders SET (
  autovacuum_vacuum_scale_factor = 0.05,
  autovacuum_analyze_scale_factor = 0.02
);

-- Monitor vacuum activity
SELECT schemaname, relname, last_vacuum, last_autovacuum,
       n_dead_tup, n_live_tup
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;

-- Check bloat
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size,
       n_dead_tup, n_live_tup,
       ROUND(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC;
```

#### Connection Pooling with PgBouncer

```ini
# pgbouncer.ini basic configuration
[databases]
myapp = host=localhost dbname=myapp_production

[pgbouncer]
listen_addr = 0.0.0.0
listen_port = 6432
auth_type = md5
auth_file = /etc/pgbouncer/userlist.txt

# Pool modes
pool_mode = transaction  # or session, statement

# Connection limits
max_client_conn = 1000
default_pool_size = 25
min_pool_size = 5
reserve_pool_size = 5
reserve_pool_timeout = 3

# Timeouts
server_idle_timeout = 600
server_lifetime = 3600
server_connect_timeout = 15
query_timeout = 0
query_wait_timeout = 120

# Logging
admin_users = postgres
stats_users = postgres
log_connections = 0
log_disconnections = 0
log_pooler_errors = 1
```

**Connection Pooling Best Practices:**

- Use `transaction` mode for most applications
- Set `default_pool_size` = (CPU cores × 2) + effective_spindle_count
- Monitor pool usage: `SHOW POOLS;` in PgBouncer console
- Application connection string: `postgresql://user:pass@pgbouncer:6432/myapp`

#### PostgreSQL Performance Tuning

```sql
-- postgresql.conf critical settings
shared_buffers = 4GB              # 25% of RAM
effective_cache_size = 12GB       # 75% of RAM
work_mem = 16MB                   # Per operation memory
maintenance_work_mem = 512MB      # For VACUUM, CREATE INDEX
max_connections = 200
max_parallel_workers_per_gather = 4

-- WAL settings for write-heavy workloads
wal_buffers = 16MB
checkpoint_completion_target = 0.9
max_wal_size = 2GB
min_wal_size = 512MB

-- Query planner settings
random_page_cost = 1.1           # For SSD storage
effective_io_concurrency = 200   # For SSD storage
default_statistics_target = 100

-- Enable query monitoring
shared_preload_libraries = 'pg_stat_statements'
pg_stat_statements.track = all
pg_stat_statements.max = 10000
```

### MongoDB Advanced Optimization

#### Sharding Strategies

**Shard Key Selection:**

```javascript
// Good shard key: high cardinality, even distribution
// Example: user_id for multi-tenant application
sh.enableSharding("myapp")
sh.shardCollection("myapp.orders", { "userId": 1 })

// Compound shard key for better distribution
sh.shardCollection("myapp.events", { "tenantId": 1, "timestamp": 1 })

// Hashed shard key for random distribution
sh.shardCollection("myapp.logs", { "_id": "hashed" })
```

**Shard Key Patterns:**

1. **Range-based Sharding** (ordered data):

```javascript
// Good for time-series data
sh.shardCollection("analytics.events", { "date": 1, "userId": 1 })

// Queries benefit from targeted routing
db.events.find({ date: ISODate("2025-01-17"), userId: 123 })
```

2. **Hash-based Sharding** (random distribution):

```javascript
// Good for even distribution, poor for range queries
sh.shardCollection("users.profiles", { "_id": "hashed" })

// All shards queried for range
db.profiles.find({ _id: { $gt: 1000, $lt: 2000 } })
```

3. **Zone Sharding** (geographic distribution):

```javascript
// Configure zones for data locality
sh.addShardTag("shard0000", "US-EAST")
sh.addShardTag("shard0001", "EU-WEST")

sh.addTagRange(
  "myapp.users",
  { region: "us-east", userId: MinKey },
  { region: "us-east", userId: MaxKey },
  "US-EAST"
)
```

#### Index Optimization

```javascript
// Compound index design (ESR rule: Equality, Sort, Range)
db.orders.createIndex(
  { status: 1, createdAt: -1, totalAmount: 1 },
  { background: true, name: "idx_orders_esr" }
)

// Covering index (includes projected fields)
db.users.createIndex(
  { email: 1 },
  { unique: true, partialFilterExpression: { active: true } }
)

// Text index for search
db.products.createIndex(
  { name: "text", description: "text" },
  { weights: { name: 10, description: 5 } }
)

// Geospatial index
db.stores.createIndex({ location: "2dsphere" })

// TTL index for automatic cleanup
db.sessions.createIndex(
  { createdAt: 1 },
  { expireAfterSeconds: 3600 }
)

// Partial index (smaller, faster)
db.orders.createIndex(
  { userId: 1, createdAt: -1 },
  { partialFilterExpression: { status: "pending" } }
)
```

**Index Analysis:**

```javascript
// Explain query execution
db.orders.find({ userId: 123 }).sort({ createdAt: -1 }).explain("executionStats")

// Check index usage
db.orders.aggregate([
  { $indexStats: {} }
])

// Find unused indexes
db.orders.aggregate([
  { $indexStats: {} },
  { $match: { "accesses.ops": { $lt: 100 } } }
])
```

#### Aggregation Pipeline Optimization

```javascript
// Optimize pipeline order: $match early, $project late
db.orders.aggregate([
  // 1. Filter early (uses indexes)
  { $match: {
    status: "completed",
    createdAt: { $gte: ISODate("2025-01-01") }
  }},

  // 2. Sort (can use index if immediately after $match)
  { $sort: { createdAt: -1 } },

  // 3. Limit early to reduce documents processed
  { $limit: 1000 },

  // 4. Lookup (expensive, do after filtering)
  { $lookup: {
    from: "users",
    localField: "userId",
    foreignField: "_id",
    as: "user"
  }},

  // 5. Unwind after lookup
  { $unwind: "$user" },

  // 6. Group (after filtering and limiting)
  { $group: {
    _id: "$user.country",
    totalRevenue: { $sum: "$totalAmount" },
    orderCount: { $sum: 1 }
  }},

  // 7. Project last (remove unnecessary fields)
  { $project: {
    _id: 0,
    country: "$_id",
    totalRevenue: 1,
    orderCount: 1
  }}
])

// Use $facet for multiple aggregations in one query
db.orders.aggregate([
  { $match: { status: "completed" } },
  { $facet: {
    "byStatus": [
      { $group: { _id: "$status", count: { $sum: 1 } } }
    ],
    "byCountry": [
      { $group: { _id: "$shippingCountry", total: { $sum: "$totalAmount" } } }
    ],
    "totalStats": [
      { $group: { _id: null, total: { $sum: "$totalAmount" }, avg: { $avg: "$totalAmount" } } }
    ]
  }}
])
```

#### Replica Set Configuration

```javascript
// Configure replica set for read scaling
rs.initiate({
  _id: "myReplicaSet",
  members: [
    { _id: 0, host: "mongo1:27017", priority: 3 },
    { _id: 1, host: "mongo2:27017", priority: 2 },
    { _id: 2, host: "mongo3:27017", priority: 1 }
  ]
})

// Read preferences for load distribution
// Application connection string:
mongodb://mongo1:27017,mongo2:27017,mongo3:27017/myapp?replicaSet=myReplicaSet&readPreference=secondaryPreferred

// Write concern for durability
db.orders.insertOne(
  { userId: 123, total: 99.99 },
  { writeConcern: { w: "majority", j: true, wtimeout: 5000 } }
)

// Read concern for consistency
db.orders.find({ userId: 123 })
  .readConcern("majority")
  .toArray()
```


### Redis Advanced Patterns

#### Caching Strategies

**1. Cache-Aside (Lazy Loading)**

```python
import redis
import json
from typing import Optional

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def get_user(user_id: int) -> Optional[dict]:
    """Cache-aside pattern: check cache first, then database"""
    cache_key = f"user:{user_id}"

    # Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Cache miss: query database
    user = db.query("SELECT * FROM users WHERE id = %s", user_id)
    if user:
        # Store in cache with TTL
        redis_client.setex(cache_key, 3600, json.dumps(user))

    return user

def update_user(user_id: int, data: dict):
    """Update database and invalidate cache"""
    db.execute("UPDATE users SET ... WHERE id = %s", user_id)
    redis_client.delete(f"user:{user_id}")
```

**2. Write-Through Caching**

```python
def save_user(user_id: int, data: dict):
    """Write to cache and database simultaneously"""
    cache_key = f"user:{user_id}"

    # Write to database
    db.execute("INSERT INTO users ... VALUES ...", data)

    # Write to cache
    redis_client.setex(cache_key, 3600, json.dumps(data))
```

**3. Write-Behind (Write-Back) Caching**

```python
def save_user_async(user_id: int, data: dict):
    """Write to cache immediately, database asynchronously"""
    cache_key = f"user:{user_id}"

    # Write to cache immediately
    redis_client.setex(cache_key, 3600, json.dumps(data))

    # Queue database write
    redis_client.lpush("write_queue", json.dumps({
        "operation": "update_user",
        "user_id": user_id,
        "data": data
    }))

# Background worker processes write_queue
def process_write_queue():
    while True:
        item = redis_client.brpop("write_queue", timeout=5)
        if item:
            operation = json.loads(item[1])
            db.execute(operation)
```

**4. Read-Through Caching**

```python
class CacheProxy:
    """Transparent caching layer"""

    def get_user(self, user_id: int) -> dict:
        cache_key = f"user:{user_id}"

        # Check cache
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        # Load from source
        user = self._load_from_database(user_id)

        # Populate cache
        if user:
            redis_client.setex(cache_key, 3600, json.dumps(user))

        return user
```

#### Redis Data Structures and Use Cases

```python
# 1. String: Simple key-value, counters
redis_client.set("user:1000:name", "John Doe")
redis_client.incr("page:views:home")
redis_client.setex("session:abc123", 1800, json.dumps(session_data))

# 2. Hash: Object storage
redis_client.hset("user:1000", mapping={
    "name": "John Doe",
    "email": "john@example.com",
    "plan": "premium"
})
redis_client.hincrby("user:1000", "login_count", 1)

# 3. List: Queues, activity feeds
redis_client.lpush("queue:tasks", task_id)
redis_client.rpop("queue:tasks")
redis_client.ltrim("feed:user:1000", 0, 99)  # Keep last 100 items

# 4. Set: Unique collections, tags
redis_client.sadd("tags:post:123", "python", "redis", "database")
redis_client.sismember("tags:post:123", "python")
redis_client.sinter("tags:post:123", "tags:post:456")  # Common tags

# 5. Sorted Set: Leaderboards, time-series
redis_client.zadd("leaderboard", {"player1": 100, "player2": 95})
redis_client.zincrby("leaderboard", 10, "player1")
redis_client.zrevrange("leaderboard", 0, 9, withscores=True)  # Top 10

# 6. HyperLogLog: Cardinality estimation
redis_client.pfadd("unique:visitors:2025-01-17", "user1", "user2")
redis_client.pfcount("unique:visitors:2025-01-17")
```

#### Pub/Sub and Streams

**Pub/Sub Pattern:**

```python
import redis

# Publisher
pub = redis.Redis()
pub.publish("notifications", json.dumps({
    "type": "new_order",
    "order_id": 12345
}))

# Subscriber
sub = redis.Redis()
pubsub = sub.pubsub()
pubsub.subscribe("notifications")

for message in pubsub.listen():
    if message["type"] == "message":
        data = json.loads(message["data"])
        process_notification(data)
```

**Redis Streams (Preferred for Reliable Messaging):**

```python
# Producer
stream_key = "events:orders"
redis_client.xadd(stream_key, {
    "order_id": 12345,
    "user_id": 1000,
    "total": 99.99
})

# Consumer Group
group_name = "order-processors"
redis_client.xgroup_create(stream_key, group_name, id="0", mkstream=True)

# Consumer
consumer_name = "worker-1"
while True:
    messages = redis_client.xreadgroup(
        group_name, consumer_name, {stream_key: ">"}, count=10, block=5000
    )

    for stream, message_list in messages:
        for message_id, data in message_list:
            try:
                process_order(data)
                redis_client.xack(stream_key, group_name, message_id)
            except Exception as e:
                logger.error(f"Failed to process {message_id}: {e}")
```

#### Redis Cluster Configuration

```python
from redis.cluster import RedisCluster

# Connect to Redis Cluster
cluster = RedisCluster(
    startup_nodes=[
        {"host": "redis-node-1", "port": 6379},
        {"host": "redis-node-2", "port": 6379},
        {"host": "redis-node-3", "port": 6379}
    ],
    decode_responses=True,
    skip_full_coverage_check=True
)

# Use hash tags for multi-key operations
cluster.set("{user:1000}:profile", profile_data)
cluster.set("{user:1000}:settings", settings_data)
# Both keys on same shard due to {user:1000} hash tag
```

**Redis Configuration (redis.conf):**

```ini
# Memory management
maxmemory 2gb
maxmemory-policy allkeys-lru

# Persistence
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec

# Performance
tcp-backlog 511
timeout 300
tcp-keepalive 60
```

### Query Optimization Techniques

#### Solving the N+1 Problem

**Bad: N+1 Queries**

```python
# 1 query to get orders
orders = db.query("SELECT * FROM orders WHERE user_id = ?", user_id)

# N queries to get user details for each order
for order in orders:
    user = db.query("SELECT * FROM users WHERE id = ?", order.user_id)
    order.user = user
```

**Good: Join or Batch Loading**

```python
# Single query with join
orders = db.query("""
    SELECT o.*, u.name, u.email
    FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE o.user_id = ?
""", user_id)

# Or batch loading
order_ids = [1, 2, 3, 4, 5]
orders = db.query("SELECT * FROM orders WHERE id IN (?)", order_ids)
user_ids = [o.user_id for o in orders]
users = db.query("SELECT * FROM users WHERE id IN (?)", user_ids)
users_map = {u.id: u for u in users}
for order in orders:
    order.user = users_map[order.user_id]
```

#### Database Scaling Strategies

**1. Vertical Scaling (Scale Up)**

- Increase CPU, RAM, storage
- Simple but has limits
- Good for initial growth

**2. Horizontal Scaling (Scale Out)**

**Read Replicas:**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Master for writes
master_engine = create_engine("postgresql://master:5432/myapp")

# Replicas for reads
replica_engines = [
    create_engine("postgresql://replica1:5432/myapp"),
    create_engine("postgresql://replica2:5432/myapp")
]

def get_session(write=False):
    if write:
        return sessionmaker(bind=master_engine)()
    else:
        # Round-robin replica selection
        engine = random.choice(replica_engines)
        return sessionmaker(bind=engine)()

# Usage
read_session = get_session(write=False)
users = read_session.query(User).all()

write_session = get_session(write=True)
write_session.add(User(name="John"))
write_session.commit()
```

**Sharding:**

```python
def get_shard(user_id: int) -> int:
    """Distribute users across 4 shards"""
    return user_id % 4

def get_connection(user_id: int):
    shard_id = get_shard(user_id)
    return shard_connections[shard_id]

# Query specific shard
conn = get_connection(user_id=1234)
user = conn.query("SELECT * FROM users WHERE id = ?", 1234)

# Query all shards (expensive!)
results = []
for conn in shard_connections:
    results.extend(conn.query("SELECT * FROM users WHERE status = 'active'"))
```

#### Connection Pooling Best Practices

**HikariCP (Java):**

```java
HikariConfig config = new HikariConfig();
config.setJdbcUrl("jdbc:postgresql://localhost:5432/myapp");
config.setUsername("user");
config.setPassword("password");
config.setMaximumPoolSize(20);
config.setMinimumIdle(5);
config.setConnectionTimeout(30000);
config.setIdleTimeout(600000);
config.setMaxLifetime(1800000);

HikariDataSource ds = new HikariDataSource(config);
```

**Python (SQLAlchemy):**

```python
from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://user:pass@localhost/myapp",
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True
)
```

**Node.js (pg-pool):**

```javascript
const { Pool } = require('pg');

const pool = new Pool({
  host: 'localhost',
  database: 'myapp',
  user: 'user',
  password: 'password',
  max: 20,                // Maximum pool size
  min: 5,                 // Minimum pool size
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});
```


### Database Monitoring and Profiling

#### PostgreSQL Monitoring

**pg_stat_statements Extension:**

```sql
-- Enable extension
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Top 10 slowest queries by average time
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    max_exec_time,
    stddev_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- Most frequently called queries
SELECT
    query,
    calls,
    total_exec_time,
    rows
FROM pg_stat_statements
ORDER BY calls DESC
LIMIT 10;

-- Queries with most total time
SELECT
    query,
    calls,
    total_exec_time,
    mean_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;

-- Reset statistics
SELECT pg_stat_statements_reset();
```

**Key Metrics to Monitor:**

```sql
-- Connection statistics
SELECT count(*), state
FROM pg_stat_activity
GROUP BY state;

-- Cache hit ratio (should be > 90%)
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit)  as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;

-- Table bloat and dead tuples
SELECT
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    last_vacuum,
    last_autovacuum
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;

-- Index usage
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Blocking queries
SELECT
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS blocking_statement
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks
    ON blocking_locks.locktype = blocked_locks.locktype
    AND blocking_locks.database IS NOT DISTINCT FROM blocked_locks.database
    AND blocking_locks.relation IS NOT DISTINCT FROM blocked_locks.relation
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

#### MongoDB Profiling

**Enable Profiler:**

```javascript
// Enable profiler for slow queries (>100ms)
db.setProfilingLevel(1, { slowms: 100 })

// Profile all operations
db.setProfilingLevel(2)

// Disable profiler
db.setProfilingLevel(0)

// Check profiler status
db.getProfilingStatus()
```

**Analyze Slow Queries:**

```javascript
// Recent slow queries
db.system.profile.find({
  millis: { $gt: 100 }
}).sort({ ts: -1 }).limit(10).pretty()

// Slow queries by operation type
db.system.profile.aggregate([
  { $match: { millis: { $gt: 100 } } },
  { $group: {
    _id: "$op",
    count: { $sum: 1 },
    avgMs: { $avg: "$millis" },
    maxMs: { $max: "$millis" }
  }},
  { $sort: { avgMs: -1 } }
])

// Queries without index usage
db.system.profile.find({
  "planSummary": { $regex: /COLLSCAN/ }
}).limit(10)
```

**Server Status Metrics:**

```javascript
// Overall server status
db.serverStatus()

// Connection metrics
db.serverStatus().connections

// Operation counters
db.serverStatus().opcounters

// Memory usage
db.serverStatus().mem

// Network metrics
db.serverStatus().network

// Current operations
db.currentOp()

// Database statistics
db.stats()
```

#### Redis Monitoring

**INFO Command:**

```bash
# All stats
redis-cli INFO

# Specific sections
redis-cli INFO server
redis-cli INFO memory
redis-cli INFO stats
redis-cli INFO replication
redis-cli INFO cpu

# Key metrics
redis-cli INFO stats | grep -E 'keyspace_hits|keyspace_misses|evicted_keys'
redis-cli INFO memory | grep -E 'used_memory_human|maxmemory_human'
```

**Key Metrics:**

```python
import redis

client = redis.Redis()

# Get all info
info = client.info()

# Cache hit rate
hits = info['keyspace_hits']
misses = info['keyspace_misses']
hit_rate = hits / (hits + misses) if (hits + misses) > 0 else 0
print(f"Cache hit rate: {hit_rate:.2%}")

# Memory usage
used_memory = info['used_memory_human']
max_memory = info['maxmemory_human']
print(f"Memory: {used_memory} / {max_memory}")

# Connected clients
connected_clients = info['connected_clients']
print(f"Connected clients: {connected_clients}")

# Operations per second
ops_per_sec = info['instantaneous_ops_per_sec']
print(f"Operations/sec: {ops_per_sec}")

# Evicted keys
evicted_keys = info['evicted_keys']
print(f"Evicted keys: {evicted_keys}")
```

**Slow Log:**

```bash
# Configure slow log (microseconds)
redis-cli CONFIG SET slowlog-log-slower-than 10000
redis-cli CONFIG SET slowlog-max-len 128

# View slow log
redis-cli SLOWLOG GET 10

# Reset slow log
redis-cli SLOWLOG RESET
```

### Backup and Recovery Strategies

#### PostgreSQL Backup

**Physical Backup (pg_basebackup):**

```bash
# Full backup
pg_basebackup -h localhost -U postgres -D /backup/pg_data -Fp -Xs -P

# Compressed backup
pg_basebackup -h localhost -U postgres -D /backup/pg_data -Ft -z -P
```

**Logical Backup (pg_dump):**

```bash
# Single database
pg_dump -h localhost -U postgres -d myapp -F c -f /backup/myapp.dump

# All databases
pg_dumpall -h localhost -U postgres -f /backup/all_databases.sql

# Schema only
pg_dump -h localhost -U postgres -d myapp -s -f /backup/schema.sql

# Data only
pg_dump -h localhost -U postgres -d myapp -a -f /backup/data.sql

# Specific tables
pg_dump -h localhost -U postgres -d myapp -t users -t orders -F c -f /backup/tables.dump
```

**Restore:**

```bash
# Restore custom format dump
pg_restore -h localhost -U postgres -d myapp -v /backup/myapp.dump

# Restore SQL dump
psql -h localhost -U postgres -d myapp -f /backup/myapp.sql

# Parallel restore (faster)
pg_restore -h localhost -U postgres -d myapp -j 4 -v /backup/myapp.dump
```

**Point-in-Time Recovery (PITR):**

```bash
# Enable WAL archiving (postgresql.conf)
wal_level = replica
archive_mode = on
archive_command = 'cp %p /archive/%f'

# Take base backup
pg_basebackup -h localhost -U postgres -D /backup/base -Fp -Xs -P

# Restore to specific time
# 1. Stop PostgreSQL
# 2. Restore base backup
# 3. Create recovery.conf
restore_command = 'cp /archive/%f %p'
recovery_target_time = '2025-01-17 10:30:00'
# 4. Start PostgreSQL
```

#### MongoDB Backup

**mongodump:**

```bash
# Full backup
mongodump --host localhost --port 27017 --out /backup/mongo

# Specific database
mongodump --host localhost --port 27017 --db myapp --out /backup/mongo

# Specific collection
mongodump --host localhost --db myapp --collection orders --out /backup/mongo

# Compressed backup
mongodump --host localhost --gzip --out /backup/mongo

# Replica set backup
mongodump --host "rs0/mongo1:27017,mongo2:27017,mongo3:27017" --out /backup/mongo
```

**mongorestore:**

```bash
# Restore full backup
mongorestore --host localhost --port 27017 /backup/mongo

# Restore specific database
mongorestore --host localhost --db myapp /backup/mongo/myapp

# Drop existing data before restore
mongorestore --host localhost --drop /backup/mongo

# Restore from compressed backup
mongorestore --host localhost --gzip /backup/mongo
```

**Filesystem Snapshots (Replica Set):**

```javascript
// 1. Stop balancer (if sharded)
sh.stopBalancer()

// 2. Lock secondary member
db.fsyncLock()

// 3. Take filesystem snapshot (LVM, ZFS, EBS snapshot)

// 4. Unlock
db.fsyncUnlock()

// 5. Start balancer
sh.startBalancer()
```

#### Redis Backup

**RDB (Snapshot):**

```bash
# Manual snapshot
redis-cli BGSAVE

# Configure automatic snapshots (redis.conf)
save 900 1      # After 900 sec if 1 key changed
save 300 10     # After 300 sec if 10 keys changed
save 60 10000   # After 60 sec if 10000 keys changed

# Backup RDB file
cp /var/lib/redis/dump.rdb /backup/dump-$(date +%Y%m%d).rdb
```

**AOF (Append-Only File):**

```bash
# Enable AOF (redis.conf)
appendonly yes
appendfsync everysec

# Rewrite AOF
redis-cli BGREWRITEAOF

# Backup AOF file
cp /var/lib/redis/appendonly.aof /backup/appendonly-$(date +%Y%m%d).aof
```

**Restore:**

```bash
# Stop Redis
systemctl stop redis

# Restore RDB or AOF
cp /backup/dump.rdb /var/lib/redis/
# or
cp /backup/appendonly.aof /var/lib/redis/

# Start Redis
systemctl start redis
```

---

## Level 3: Deep Dive Resources (10 minutes)

### Official Documentation

**PostgreSQL:**

- [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html)
- [pg_stat_statements](https://www.postgresql.org/docs/current/pgstatstatements.html)
- [EXPLAIN Documentation](https://www.postgresql.org/docs/current/sql-explain.html)
- [PgBouncer Documentation](https://www.pgbouncer.org/usage.html)

**MongoDB:**

- [MongoDB Performance Best Practices](https://www.mongodb.com/docs/manual/administration/analyzing-mongodb-performance/)
- [Sharding Guide](https://www.mongodb.com/docs/manual/sharding/)
- [Index Strategies](https://www.mongodb.com/docs/manual/applications/indexes/)
- [Aggregation Pipeline Optimization](https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/)

**Redis:**

- [Redis Documentation](https://redis.io/documentation)
- [Redis Cluster Tutorial](https://redis.io/docs/manual/scaling/)
- [Redis Persistence](https://redis.io/docs/manual/persistence/)
- [Redis Best Practices](https://redis.io/docs/manual/patterns/)

### Books and Courses

- "High Performance PostgreSQL" by Gregory Smith
- "PostgreSQL Query Optimization" by Henrietta Dombrovskaya
- "MongoDB: The Definitive Guide" by Shannon Bradshaw
- "Redis in Action" by Josiah Carlson
- "Designing Data-Intensive Applications" by Martin Kleppmann

### Tools and Utilities

**PostgreSQL:**

- pgAdmin 4 - Database management
- pg_top - Real-time monitoring
- pgBadger - Log analyzer
- pgtune - Configuration generator

**MongoDB:**

- MongoDB Compass - GUI client
- MongoDB Atlas - Managed service
- mongostat/mongotop - Command-line monitoring
- Studio 3T - Advanced GUI

**Redis:**

- RedisInsight - GUI client
- redis-cli - Command-line interface
- redis-stat - Real-time monitoring
- redis-rdb-tools - RDB file analysis

### Practice Exercises

1. **Index Optimization Challenge**: Given a slow query, design optimal indexes
2. **Sharding Strategy**: Design shard key for multi-tenant application
3. **Cache Implementation**: Build cache-aside pattern with TTL and invalidation
4. **Query Analysis**: Use EXPLAIN to optimize complex join queries
5. **Backup Strategy**: Design comprehensive backup/recovery plan

### Related Skills

- [Database Design Fundamentals](../design-fundamentals/SKILL.md)
- [API Performance Optimization](../../backend/api-performance/SKILL.md)
- [System Architecture Patterns](../../architecture/system-patterns/SKILL.md)
- [Monitoring and Observability](../../devops/monitoring/SKILL.md)

---

## Bundled Resources

This skill includes 6 production-ready templates and scripts:

1. **templates/postgres-optimization.sql** - PostgreSQL optimization queries and index strategies
2. **templates/mongodb-sharding.yaml** - MongoDB sharding configuration
3. **templates/redis-caching.py** - Redis caching pattern implementations
4. **scripts/query-profiling.sh** - Automated database query profiling
5. **config/pgbouncer.ini** - PgBouncer connection pooling configuration
6. **templates/monitoring-dashboard.json** - Grafana dashboard for database metrics

All resources are located in the `skills/database/advanced-optimization/` directory.
