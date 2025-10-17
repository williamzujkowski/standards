"""
Redis Caching Patterns Implementation
Version: 1.0.0
Description: Production-ready Redis caching strategies
"""

import json
import logging
import time
from datetime import datetime
from functools import wraps
from typing import Any, Callable, List

import redis
from redis.cluster import RedisCluster

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RedisCache:
    """Redis cache manager with multiple caching strategies"""

    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        cluster_mode: bool = False,
        cluster_nodes: List[dict] = None,
    ):
        """
        Initialize Redis client

        Args:
            host: Redis host (single node)
            port: Redis port (single node)
            db: Redis database number
            cluster_mode: Enable Redis Cluster mode
            cluster_nodes: List of cluster nodes [{"host": "...", "port": ...}]
        """
        if cluster_mode and cluster_nodes:
            self.client = RedisCluster(
                startup_nodes=cluster_nodes, decode_responses=True, skip_full_coverage_check=True
            )
        else:
            self.client = redis.Redis(
                host=host,
                port=port,
                db=db,
                decode_responses=True,
                socket_keepalive=True,
                socket_keepalive_options={
                    redis.connection.socket.TCP_KEEPIDLE: 30,
                    redis.connection.socket.TCP_KEEPINTVL: 10,
                    redis.connection.socket.TCP_KEEPCNT: 3,
                },
            )

        self.stats = {"hits": 0, "misses": 0, "sets": 0, "deletes": 0}

    def _serialize(self, value: Any) -> str:
        """Serialize value for storage"""
        return json.dumps(value)

    def _deserialize(self, value: str) -> Any:
        """Deserialize value from storage"""
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    # ========================================================================
    # 1. CACHE-ASIDE (LAZY LOADING) PATTERN
    # ========================================================================

    def cache_aside_get(self, key: str, loader: Callable[[], Any], ttl: int = 3600) -> Any:
        """
        Cache-aside pattern: Check cache first, load from source on miss

        Args:
            key: Cache key
            loader: Function to load data on cache miss
            ttl: Time-to-live in seconds

        Returns:
            Cached or loaded value
        """
        # Try cache first
        cached = self.client.get(key)
        if cached:
            self.stats["hits"] += 1
            logger.info(f"Cache HIT: {key}")
            return self._deserialize(cached)

        # Cache miss: load from source
        self.stats["misses"] += 1
        logger.info(f"Cache MISS: {key}")

        value = loader()

        # Store in cache
        if value is not None:
            self.client.setex(key, ttl, self._serialize(value))
            self.stats["sets"] += 1

        return value

    def cache_aside_set(self, key: str, value: Any, ttl: int = 3600):
        """
        Store value in cache with TTL

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time-to-live in seconds
        """
        self.client.setex(key, ttl, self._serialize(value))
        self.stats["sets"] += 1

    def cache_aside_delete(self, key: str):
        """
        Invalidate cache entry

        Args:
            key: Cache key to delete
        """
        self.client.delete(key)
        self.stats["deletes"] += 1
        logger.info(f"Cache INVALIDATE: {key}")

    # ========================================================================
    # 2. WRITE-THROUGH CACHING PATTERN
    # ========================================================================

    def write_through(self, key: str, value: Any, writer: Callable[[Any], None], ttl: int = 3600):
        """
        Write-through pattern: Write to cache and database simultaneously

        Args:
            key: Cache key
            value: Value to write
            writer: Function to write to database
            ttl: Time-to-live in seconds
        """
        # Write to database first
        writer(value)

        # Write to cache
        self.client.setex(key, ttl, self._serialize(value))
        self.stats["sets"] += 1
        logger.info(f"Write-through: {key}")

    # ========================================================================
    # 3. WRITE-BEHIND (WRITE-BACK) PATTERN
    # ========================================================================

    def write_behind_enqueue(self, operation: str, data: dict):
        """
        Write-behind pattern: Queue database writes for async processing

        Args:
            operation: Operation type (insert, update, delete)
            data: Operation data
        """
        queue_key = "write_queue"
        payload = {"operation": operation, "data": data, "timestamp": datetime.utcnow().isoformat()}

        self.client.lpush(queue_key, self._serialize(payload))
        logger.info(f"Write-behind queued: {operation}")

    def write_behind_process(self, processor: Callable[[dict], None], batch_size: int = 10, timeout: int = 5):
        """
        Process write-behind queue

        Args:
            processor: Function to process queue items
            batch_size: Number of items to process per batch
            timeout: Block timeout in seconds
        """
        queue_key = "write_queue"

        while True:
            # Block and wait for items
            item = self.client.brpop(queue_key, timeout=timeout)

            if item:
                _, data = item
                operation = self._deserialize(data)

                try:
                    processor(operation)
                    logger.info(f"Write-behind processed: {operation['operation']}")
                except Exception as e:
                    logger.error(f"Write-behind error: {e}")
                    # Re-queue or handle error
                    self.client.lpush(f"{queue_key}:failed", data)

    # ========================================================================
    # 4. READ-THROUGH CACHING PATTERN
    # ========================================================================

    class ReadThrough:
        """Read-through cache proxy"""

        def __init__(self, cache: "RedisCache", ttl: int = 3600):
            self.cache = cache
            self.ttl = ttl

        def get(self, key: str, loader: Callable[[], Any]) -> Any:
            """
            Read-through: Transparently load and cache data

            Args:
                key: Cache key
                loader: Data loader function

            Returns:
                Cached or loaded value
            """
            return self.cache.cache_aside_get(key, loader, self.ttl)

    # ========================================================================
    # 5. CACHE DECORATORS
    # ========================================================================

    def cached(self, ttl: int = 3600, key_prefix: str = ""):
        """
        Decorator for caching function results

        Args:
            ttl: Cache TTL in seconds
            key_prefix: Prefix for cache keys

        Example:
            @cache.cached(ttl=300, key_prefix='user')
            def get_user(user_id):
                return db.query("SELECT * FROM users WHERE id = ?", user_id)
        """

        def decorator(func: Callable) -> Callable:
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key from function name and arguments
                key_parts = [key_prefix or func.__name__]
                key_parts.extend(str(arg) for arg in args)
                key_parts.extend(f"{k}:{v}" for k, v in sorted(kwargs.items()))
                cache_key = ":".join(key_parts)

                # Try cache
                cached = self.client.get(cache_key)
                if cached:
                    self.stats["hits"] += 1
                    return self._deserialize(cached)

                # Execute function
                self.stats["misses"] += 1
                result = func(*args, **kwargs)

                # Cache result
                if result is not None:
                    self.client.setex(cache_key, ttl, self._serialize(result))
                    self.stats["sets"] += 1

                return result

            return wrapper

        return decorator

    # ========================================================================
    # 6. ADVANCED PATTERNS
    # ========================================================================

    def get_with_stampede_protection(
        self, key: str, loader: Callable[[], Any], ttl: int = 3600, lock_timeout: int = 10
    ) -> Any:
        """
        Cache with stampede protection (single-flight pattern)

        Prevents multiple simultaneous cache refreshes for the same key

        Args:
            key: Cache key
            loader: Data loader function
            ttl: Cache TTL
            lock_timeout: Lock timeout in seconds
        """
        # Try cache
        cached = self.client.get(key)
        if cached:
            self.stats["hits"] += 1
            return self._deserialize(cached)

        # Acquire lock to prevent stampede
        lock_key = f"{key}:lock"
        lock = self.client.set(lock_key, "1", nx=True, ex=lock_timeout)

        if lock:
            try:
                # Load data
                value = loader()

                # Cache result
                if value is not None:
                    self.client.setex(key, ttl, self._serialize(value))
                    self.stats["sets"] += 1

                return value
            finally:
                # Release lock
                self.client.delete(lock_key)
        else:
            # Another process is loading, wait and retry
            time.sleep(0.1)
            return self.get_with_stampede_protection(key, loader, ttl, lock_timeout)

    def get_with_refresh_ahead(
        self, key: str, loader: Callable[[], Any], ttl: int = 3600, refresh_threshold: float = 0.8
    ) -> Any:
        """
        Cache with refresh-ahead strategy

        Refreshes cache before expiration to prevent cache misses

        Args:
            key: Cache key
            loader: Data loader function
            ttl: Cache TTL
            refresh_threshold: Refresh when TTL < threshold * ttl
        """
        # Get cached value and TTL
        cached = self.client.get(key)
        remaining_ttl = self.client.ttl(key)

        if cached and remaining_ttl > 0:
            self.stats["hits"] += 1

            # Check if refresh needed
            if remaining_ttl < (ttl * refresh_threshold):
                # Async refresh (in production, use background task)
                logger.info(f"Refresh-ahead triggered: {key}")
                try:
                    value = loader()
                    if value is not None:
                        self.client.setex(key, ttl, self._serialize(value))
                except Exception as e:
                    logger.error(f"Refresh-ahead failed: {e}")

            return self._deserialize(cached)

        # Cache miss
        self.stats["misses"] += 1
        value = loader()

        if value is not None:
            self.client.setex(key, ttl, self._serialize(value))
            self.stats["sets"] += 1

        return value

    # ========================================================================
    # 7. CACHE STATISTICS AND MONITORING
    # ========================================================================

    def get_stats(self) -> dict:
        """Get cache statistics"""
        total_requests = self.stats["hits"] + self.stats["misses"]
        hit_rate = self.stats["hits"] / total_requests if total_requests > 0 else 0

        # Get Redis info
        info = self.client.info()

        return {
            "hits": self.stats["hits"],
            "misses": self.stats["misses"],
            "sets": self.stats["sets"],
            "deletes": self.stats["deletes"],
            "hit_rate": f"{hit_rate:.2%}",
            "redis_used_memory": info.get("used_memory_human", "N/A"),
            "redis_connected_clients": info.get("connected_clients", 0),
            "redis_ops_per_sec": info.get("instantaneous_ops_per_sec", 0),
        }

    def reset_stats(self):
        """Reset statistics counters"""
        self.stats = {"hits": 0, "misses": 0, "sets": 0, "deletes": 0}


# ============================================================================
# USAGE EXAMPLES
# ============================================================================


def example_usage():
    """Example usage of Redis caching patterns"""

    # Initialize cache
    cache = RedisCache(host="localhost", port=6379)

    # Example 1: Cache-Aside Pattern
    def load_user(user_id: int):
        """Simulate database query"""
        logger.info(f"Loading user {user_id} from database")
        return {"id": user_id, "name": "John Doe", "email": "john@example.com"}

    user = cache.cache_aside_get(key=f"user:{1000}", loader=lambda: load_user(1000), ttl=3600)
    print(f"User: {user}")

    # Example 2: Using Decorator
    @cache.cached(ttl=300, key_prefix="product")
    def get_product(product_id: int):
        logger.info(f"Loading product {product_id} from database")
        return {"id": product_id, "name": "Widget", "price": 29.99}

    product = get_product(123)
    print(f"Product: {product}")

    # Example 3: Stampede Protection
    user_protected = cache.get_with_stampede_protection(key=f"user:{2000}", loader=lambda: load_user(2000), ttl=3600)

    # Print statistics
    stats = cache.get_stats()
    print(f"Cache Stats: {json.dumps(stats, indent=2)}")


if __name__ == "__main__":
    example_usage()
