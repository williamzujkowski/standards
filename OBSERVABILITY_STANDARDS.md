# Observability and Monitoring Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** OBS

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Observability Principles](#1-observability-principles)
2. [Metrics and Monitoring](#2-metrics-and-monitoring)
3. [Distributed Tracing](#3-distributed-tracing)
4. [Logging Standards](#4-logging-standards)
5. [Service Level Objectives (SLOs)](#5-service-level-objectives-slos)
6. [Alerting and Incident Response](#6-alerting-and-incident-response)
7. [Performance Monitoring](#7-performance-monitoring)
8. [Infrastructure Observability](#8-infrastructure-observability)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Observability Principles

<!-- @nist-controls: [au-2, au-3, au-4, au-5, au-6, au-9, si-4] -->

### 1.1 Three Pillars of Observability

#### Metrics, Logs, and Traces **[REQUIRED]**
```yaml
# Observability strategy configuration
observability:
  strategy: "three_pillars_plus_events"

  metrics:
    collection_interval: 15s
    retention:
      raw: 15d
      downsampled_5m: 90d
      downsampled_1h: 1y
    cardinality_limit: 1000000

  logs:
    retention: 30d  # @nist au-4 "Audit storage capacity"
    structured_format: json  # @nist au-3 "Content of audit records"
    compression: gzip
    log_level: info  # @nist au-2 "Audit events"

  traces:
    sampling_rate: 0.1  # 10% sampling
    retention: 7d
    max_trace_duration: 30s

  events:
    retention: 90d
    structured_format: json
```

#### OpenTelemetry Implementation **[REQUIRED]**
```python
# observability/telemetry.py
from opentelemetry import trace, metrics
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.auto_instrumentation import sitecustomize
import logging
import time
from typing import Dict, Any, Optional
from contextlib import contextmanager

class ObservabilityManager:
    # @nist au-2 "Comprehensive audit event generation"
    # @nist si-4 "System monitoring implementation"
    def __init__(self, service_name: str, service_version: str, environment: str):
        self.service_name = service_name
        self.service_version = service_version
        self.environment = environment

        # Configure resource attributes
        self.resource = Resource.create({
            "service.name": service_name,
            "service.version": service_version,
            "deployment.environment": environment,
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
        })

        self._setup_tracing()
        self._setup_metrics()
        self._setup_logging()

    def _setup_tracing(self):
        """Configure distributed tracing."""
        trace.set_tracer_provider(TracerProvider(resource=self.resource))

        # Jaeger exporter for traces
        jaeger_exporter = JaegerExporter(
            agent_host_name="jaeger-agent",
            agent_port=6831,
        )

        span_processor = BatchSpanProcessor(jaeger_exporter)
        trace.get_tracer_provider().add_span_processor(span_processor)

        self.tracer = trace.get_tracer(__name__)

    def _setup_metrics(self):
        """Configure metrics collection."""
        # Prometheus metrics reader
        prometheus_reader = PrometheusMetricReader()

        metrics.set_meter_provider(
            MeterProvider(resource=self.resource, metric_readers=[prometheus_reader])
        )

        self.meter = metrics.get_meter(__name__)

        # Standard application metrics
        self.request_counter = self.meter.create_counter(
            name="http_requests_total",
            description="Total number of HTTP requests",
            unit="1"
        )

        self.request_duration = self.meter.create_histogram(
            name="http_request_duration_seconds",
            description="HTTP request duration in seconds",
            unit="s"
        )

        self.error_counter = self.meter.create_counter(
            name="application_errors_total",
            description="Total number of application errors",
            unit="1"
        )

    def _setup_logging(self):
        """Configure structured logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "logger": "%(name)s", "message": "%(message)s", "service": "' + self.service_name + '"}',
            datefmt='%Y-%m-%dT%H:%M:%S'
        )

        self.logger = logging.getLogger(self.service_name)

    @contextmanager
    def trace_operation(self, operation_name: str, attributes: Optional[Dict[str, Any]] = None):
        """Context manager for tracing operations."""
        with self.tracer.start_as_current_span(operation_name) as span:
            start_time = time.time()

            # Add standard attributes
            span.set_attribute("operation.name", operation_name)
            span.set_attribute("service.name", self.service_name)

            # Add custom attributes
            if attributes:
                for key, value in attributes.items():
                    span.set_attribute(key, value)

            try:
                yield span
                span.set_status(trace.Status(trace.StatusCode.OK))
            except Exception as e:
                span.set_status(
                    trace.Status(trace.StatusCode.ERROR, str(e))
                )
                span.record_exception(e)
                self.error_counter.add(1, {"operation": operation_name, "error_type": type(e).__name__})
                raise
            finally:
                duration = time.time() - start_time
                span.set_attribute("operation.duration", duration)

    def record_http_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics."""
        labels = {
            "method": method,
            "endpoint": endpoint,
            "status_code": str(status_code)
        }

        self.request_counter.add(1, labels)
        self.request_duration.record(duration, labels)

        if status_code >= 400:
            self.error_counter.add(1, {**labels, "error_type": "http_error"})

    def log_structured(self, level: str, message: str, **kwargs):
        """Log structured data with context."""
        log_data = {
            "message": message,
            "service": self.service_name,
            "environment": self.environment,
            **kwargs
        }

        # Add trace context if available
        current_span = trace.get_current_span()
        if current_span:
            span_context = current_span.get_span_context()
            log_data["trace_id"] = format(span_context.trace_id, '032x')
            log_data["span_id"] = format(span_context.span_id, '016x')

        getattr(self.logger, level.lower())(str(log_data))

# Usage example
observability = ObservabilityManager(
    service_name="user-service",
    service_version="1.2.0",
    environment="production"
)

# Trace a database operation
with observability.trace_operation("user_lookup", {"user_id": "12345"}) as span:
    user = database.get_user("12345")
    span.set_attribute("user.found", user is not None)
    if user:
        span.set_attribute("user.segment", user.segment)

# Record HTTP metrics
observability.record_http_request("GET", "/users/12345", 200, 0.045)

# Structured logging
observability.log_structured("info", "User retrieved successfully",
                           user_id="12345", operation="user_lookup")
```

### 1.2 Observability Strategy

#### Service Instrumentation **[REQUIRED]**
```python
# observability/instrumentation.py
from functools import wraps
from typing import Callable, Any
import time
import asyncio

def instrument_function(operation_name: str = None):
    """Decorator to automatically instrument functions."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"

            with observability.trace_operation(op_name) as span:
                span.set_attribute("function.name", func.__name__)
                span.set_attribute("function.module", func.__module__)

                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("function.success", True)
                    return result
                except Exception as e:
                    span.set_attribute("function.success", False)
                    span.set_attribute("function.error", str(e))
                    raise
                finally:
                    duration = time.time() - start_time
                    span.set_attribute("function.duration", duration)

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            op_name = operation_name or f"{func.__module__}.{func.__name__}"

            with observability.trace_operation(op_name) as span:
                span.set_attribute("function.name", func.__name__)
                span.set_attribute("function.module", func.__module__)
                span.set_attribute("function.async", True)

                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    span.set_attribute("function.success", True)
                    return result
                except Exception as e:
                    span.set_attribute("function.success", False)
                    span.set_attribute("function.error", str(e))
                    raise
                finally:
                    duration = time.time() - start_time
                    span.set_attribute("function.duration", duration)

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Usage examples
@instrument_function("user_service.create_user")
def create_user(user_data: dict) -> dict:
    # Function implementation
    return {"user_id": "12345", "status": "created"}

@instrument_function()
async def fetch_user_preferences(user_id: str) -> dict:
    # Async function implementation
    await asyncio.sleep(0.1)  # Simulate async operation
    return {"theme": "dark", "language": "en"}
```

---

## 2. Metrics and Monitoring

### 2.1 Prometheus Configuration

#### Metrics Collection Setup **[REQUIRED]**
```yaml
# prometheus/prometheus.yml
global:
  scrape_interval: 15s
  evaluation_interval: 15s
  external_labels:
    cluster: 'production'
    region: 'us-east-1'

rule_files:
  - "alert_rules.yml"
  - "recording_rules.yml"

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

scrape_configs:
  - job_name: 'prometheus'
    static_configs:
      - targets: ['localhost:9090']

  - job_name: 'application-metrics'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__address__, __meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        regex: ([^:]+)(?::\d+)?;(\d+)
        replacement: $1:$2
        target_label: __address__
      - action: labelmap
        regex: __meta_kubernetes_pod_label_(.+)
      - source_labels: [__meta_kubernetes_namespace]
        action: replace
        target_label: kubernetes_namespace
      - source_labels: [__meta_kubernetes_pod_name]
        action: replace
        target_label: kubernetes_pod_name

  - job_name: 'node-exporter'
    kubernetes_sd_configs:
      - role: node
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/${1}/proxy/metrics

  - job_name: 'kube-state-metrics'
    static_configs:
      - targets: ['kube-state-metrics:8080']

  - job_name: 'cadvisor'
    kubernetes_sd_configs:
      - role: node
    scheme: https
    tls_config:
      ca_file: /var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    bearer_token_file: /var/run/secrets/kubernetes.io/serviceaccount/token
    relabel_configs:
      - action: labelmap
        regex: __meta_kubernetes_node_label_(.+)
      - target_label: __address__
        replacement: kubernetes.default.svc:443
      - source_labels: [__meta_kubernetes_node_name]
        regex: (.+)
        target_label: __metrics_path__
        replacement: /api/v1/nodes/${1}/proxy/metrics/cadvisor
```

#### Recording Rules **[REQUIRED]**
```yaml
# prometheus/recording_rules.yml
groups:
  - name: application_metrics
    interval: 30s
    rules:
      # Request rate by service
      - record: service:http_requests:rate5m
        expr: rate(http_requests_total[5m])

      # Error rate by service
      - record: service:http_errors:rate5m
        expr: rate(http_requests_total{status_code=~"5.."}[5m])

      # Error ratio
      - record: service:http_error_ratio:rate5m
        expr: |
          service:http_errors:rate5m / service:http_requests:rate5m

      # 95th percentile response time
      - record: service:http_request_duration:p95:5m
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

      # 99th percentile response time
      - record: service:http_request_duration:p99:5m
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m]))

  - name: infrastructure_metrics
    interval: 30s
    rules:
      # CPU utilization by node
      - record: node:cpu_utilization:avg5m
        expr: |
          1 - avg by (instance) (
            rate(node_cpu_seconds_total{mode="idle"}[5m])
          )

      # Memory utilization by node
      - record: node:memory_utilization:current
        expr: |
          1 - (
            node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes
          )

      # Disk utilization by device
      - record: node:disk_utilization:current
        expr: |
          1 - (
            node_filesystem_avail_bytes / node_filesystem_size_bytes
          )

  - name: business_metrics
    interval: 60s
    rules:
      # Active users in last hour
      - record: business:active_users:1h
        expr: |
          count by (service) (
            increase(user_activity_total[1h]) > 0
          )

      # Revenue per minute
      - record: business:revenue:rate1m
        expr: rate(order_value_total[1m])

      # Conversion rate
      - record: business:conversion_rate:5m
        expr: |
          rate(orders_completed_total[5m]) /
          rate(sessions_started_total[5m])
```

### 2.2 Custom Metrics Implementation

#### Application Metrics **[REQUIRED]**
```python
# metrics/application_metrics.py
from prometheus_client import Counter, Histogram, Gauge, Summary
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import time
from typing import Dict, List
from functools import wraps

class ApplicationMetrics:
    def __init__(self, service_name: str):
        self.service_name = service_name

        # HTTP metrics
        self.http_requests_total = Counter(
            'http_requests_total',
            'Total HTTP requests',
            ['method', 'endpoint', 'status_code', 'service']
        )

        self.http_request_duration = Histogram(
            'http_request_duration_seconds',
            'HTTP request duration',
            ['method', 'endpoint', 'service'],
            buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0)
        )

        # Database metrics
        self.db_operations_total = Counter(
            'database_operations_total',
            'Total database operations',
            ['operation', 'table', 'status', 'service']
        )

        self.db_operation_duration = Histogram(
            'database_operation_duration_seconds',
            'Database operation duration',
            ['operation', 'table', 'service'],
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0)
        )

        # Business metrics
        self.user_registrations_total = Counter(
            'user_registrations_total',
            'Total user registrations',
            ['source', 'service']
        )

        self.active_sessions = Gauge(
            'active_sessions_current',
            'Current number of active sessions',
            ['service']
        )

        self.order_value_total = Counter(
            'order_value_total',
            'Total order value',
            ['currency', 'service']
        )

        # System metrics
        self.memory_usage_bytes = Gauge(
            'process_memory_usage_bytes',
            'Process memory usage in bytes',
            ['service']
        )

        self.error_count = Counter(
            'application_errors_total',
            'Total application errors',
            ['error_type', 'component', 'service']
        )

    def record_http_request(self, method: str, endpoint: str, status_code: int, duration: float):
        """Record HTTP request metrics."""
        labels = {
            'method': method,
            'endpoint': endpoint,
            'status_code': str(status_code),
            'service': self.service_name
        }

        self.http_requests_total.labels(**labels).inc()
        self.http_request_duration.labels(
            method=method,
            endpoint=endpoint,
            service=self.service_name
        ).observe(duration)

    def record_db_operation(self, operation: str, table: str, duration: float, success: bool = True):
        """Record database operation metrics."""
        status = 'success' if success else 'error'

        self.db_operations_total.labels(
            operation=operation,
            table=table,
            status=status,
            service=self.service_name
        ).inc()

        self.db_operation_duration.labels(
            operation=operation,
            table=table,
            service=self.service_name
        ).observe(duration)

    def record_user_registration(self, source: str = 'web'):
        """Record user registration."""
        self.user_registrations_total.labels(
            source=source,
            service=self.service_name
        ).inc()

    def set_active_sessions(self, count: int):
        """Set current active session count."""
        self.active_sessions.labels(service=self.service_name).set(count)

    def record_order_value(self, value: float, currency: str = 'USD'):
        """Record order value."""
        self.order_value_total.labels(
            currency=currency,
            service=self.service_name
        ).inc(value)

    def record_error(self, error_type: str, component: str):
        """Record application error."""
        self.error_count.labels(
            error_type=error_type,
            component=component,
            service=self.service_name
        ).inc()

    def update_memory_usage(self, bytes_used: int):
        """Update memory usage metric."""
        self.memory_usage_bytes.labels(service=self.service_name).set(bytes_used)

# Decorator for automatic HTTP metrics
def record_http_metrics(metrics: ApplicationMetrics):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            start_time = time.time()

            try:
                response = func(request, *args, **kwargs)
                status_code = getattr(response, 'status_code', 200)
            except Exception as e:
                status_code = 500
                metrics.record_error(type(e).__name__, func.__name__)
                raise
            finally:
                duration = time.time() - start_time
                metrics.record_http_request(
                    method=request.method,
                    endpoint=request.path,
                    status_code=status_code,
                    duration=duration
                )

            return response
        return wrapper
    return decorator

# Usage
app_metrics = ApplicationMetrics("user-service")

@record_http_metrics(app_metrics)
def get_user(request, user_id):
    # Implementation
    return {"user_id": user_id, "name": "John Doe"}
```

---

## 3. Distributed Tracing

### 3.1 Jaeger Configuration

#### Tracing Setup **[REQUIRED]**
```yaml
# jaeger/jaeger.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: jaeger-configuration
data:
  span-storage-type: elasticsearch
  es-server-urls: http://elasticsearch:9200
  es-username: jaeger
  es-password: password
  es-num-shards: 5
  es-num-replicas: 1
  es-index-prefix: jaeger

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: jaeger-collector
spec:
  replicas: 3
  selector:
    matchLabels:
      app: jaeger-collector
  template:
    metadata:
      labels:
        app: jaeger-collector
    spec:
      containers:
      - name: jaeger-collector
        image: jaegertracing/jaeger-collector:1.50
        ports:
        - containerPort: 14269
        - containerPort: 14268
        - containerPort: 9411
        env:
        - name: SPAN_STORAGE_TYPE
          value: elasticsearch
        - name: ES_SERVER_URLS
          value: http://elasticsearch:9200
        - name: COLLECTOR_OTLP_ENABLED
          value: "true"
        resources:
          requests:
            memory: 256Mi
            cpu: 100m
          limits:
            memory: 512Mi
            cpu: 500m

---
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: jaeger-agent
spec:
  selector:
    matchLabels:
      app: jaeger-agent
  template:
    metadata:
      labels:
        app: jaeger-agent
    spec:
      containers:
      - name: jaeger-agent
        image: jaegertracing/jaeger-agent:1.50
        ports:
        - containerPort: 5775
          protocol: UDP
        - containerPort: 6831
          protocol: UDP
        - containerPort: 6832
          protocol: UDP
        - containerPort: 5778
          protocol: TCP
        env:
        - name: REPORTER_GRPC_HOST_PORT
          value: jaeger-collector:14250
        resources:
          requests:
            memory: 64Mi
            cpu: 50m
          limits:
            memory: 128Mi
            cpu: 100m
```

#### Advanced Tracing Patterns **[REQUIRED]**
```python
# tracing/advanced_patterns.py
from opentelemetry import trace
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry.semconv.trace import SpanAttributes
import asyncio
import time
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager

class AdvancedTracing:
    def __init__(self, tracer):
        self.tracer = tracer

    def trace_database_operation(self, operation: str, table: str, query: str = None):
        """Context manager for database operations."""
        return self.tracer.start_as_current_span(
            f"db.{operation}",
            attributes={
                SpanAttributes.DB_OPERATION: operation,
                SpanAttributes.DB_SQL_TABLE: table,
                SpanAttributes.DB_SYSTEM: "postgresql",
                SpanAttributes.DB_STATEMENT: query[:1000] if query else None,  # Truncate long queries
            }
        )

    def trace_http_client(self, method: str, url: str):
        """Context manager for HTTP client calls."""
        return self.tracer.start_as_current_span(
            f"http.client.{method.lower()}",
            attributes={
                SpanAttributes.HTTP_METHOD: method,
                SpanAttributes.HTTP_URL: url,
                SpanAttributes.HTTP_SCHEME: "https",
            }
        )

    def trace_message_producer(self, queue_name: str, message_id: str):
        """Context manager for message queue producers."""
        return self.tracer.start_as_current_span(
            f"message.send",
            kind=trace.SpanKind.PRODUCER,
            attributes={
                "messaging.system": "rabbitmq",
                "messaging.destination": queue_name,
                "messaging.message_id": message_id,
                "messaging.operation": "send",
            }
        )

    def trace_message_consumer(self, queue_name: str, message_id: str):
        """Context manager for message queue consumers."""
        return self.tracer.start_as_current_span(
            f"message.receive",
            kind=trace.SpanKind.CONSUMER,
            attributes={
                "messaging.system": "rabbitmq",
                "messaging.destination": queue_name,
                "messaging.message_id": message_id,
                "messaging.operation": "receive",
            }
        )

    @asynccontextmanager
    async def trace_async_operation(self, operation_name: str, **attributes):
        """Async context manager for tracing operations."""
        with self.tracer.start_as_current_span(operation_name) as span:
            # Add custom attributes
            for key, value in attributes.items():
                span.set_attribute(key, value)

            start_time = time.time()
            try:
                yield span
                span.set_status(Status(StatusCode.OK))
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, str(e)))
                span.record_exception(e)
                raise
            finally:
                duration = time.time() - start_time
                span.set_attribute("operation.duration", duration)

    def create_child_span(self, name: str, parent_span=None, **attributes):
        """Create a child span with custom parent."""
        if parent_span:
            ctx = trace.set_span_in_context(parent_span)
            return self.tracer.start_span(name, context=ctx, attributes=attributes)
        return self.tracer.start_span(name, attributes=attributes)

    def inject_trace_context(self, headers: Dict[str, str]) -> Dict[str, str]:
        """Inject trace context into HTTP headers."""
        from opentelemetry.propagate import inject
        inject(headers)
        return headers

    def extract_trace_context(self, headers: Dict[str, str]):
        """Extract trace context from HTTP headers."""
        from opentelemetry.propagate import extract
        return extract(headers)

# Usage examples
tracer = trace.get_tracer(__name__)
advanced_tracing = AdvancedTracing(tracer)

# Database operation tracing
async def fetch_user_data(user_id: str):
    with advanced_tracing.trace_database_operation("SELECT", "users", f"SELECT * FROM users WHERE id = {user_id}") as span:
        span.set_attribute("user.id", user_id)
        # Database operation
        await asyncio.sleep(0.01)  # Simulate DB call
        span.set_attribute("db.rows_affected", 1)
        return {"id": user_id, "name": "John Doe"}

# HTTP client tracing
async def call_external_api(endpoint: str):
    with advanced_tracing.trace_http_client("GET", f"https://api.example.com{endpoint}") as span:
        # HTTP client call
        await asyncio.sleep(0.1)  # Simulate HTTP call
        span.set_attribute(SpanAttributes.HTTP_STATUS_CODE, 200)
        span.set_attribute(SpanAttributes.HTTP_RESPONSE_SIZE, 1024)
        return {"status": "success"}

# Async operation tracing
async def process_user_order(user_id: str, order_data: Dict):
    async with advanced_tracing.trace_async_operation(
        "process_order",
        user_id=user_id,
        order_value=order_data.get("total", 0)
    ) as span:
        # Fetch user data
        user = await fetch_user_data(user_id)
        span.set_attribute("user.segment", user.get("segment", "standard"))

        # Call payment service
        payment_result = await call_external_api("/payment/process")
        span.set_attribute("payment.status", payment_result["status"])

        # Process order
        await asyncio.sleep(0.05)  # Simulate order processing
        span.set_attribute("order.processed", True)

        return {"order_id": "12345", "status": "completed"}
```

### 3.2 Trace Analysis and Optimization

#### Performance Analysis **[REQUIRED]**
```python
# tracing/analysis.py
import statistics
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class SpanSummary:
    operation_name: str
    service_name: str
    avg_duration: float
    p95_duration: float
    p99_duration: float
    error_rate: float
    call_count: int

@dataclass
class TraceAnalysis:
    trace_id: str
    total_duration: float
    span_count: int
    error_count: int
    critical_path: List[str]
    bottlenecks: List[str]
    services_involved: List[str]

class TraceAnalyzer:
    def __init__(self, jaeger_client):
        self.jaeger_client = jaeger_client

    def analyze_service_performance(self, service_name: str, time_range: timedelta) -> List[SpanSummary]:
        """Analyze performance metrics for a service."""
        end_time = datetime.now()
        start_time = end_time - time_range

        # Fetch spans from Jaeger
        spans = self.jaeger_client.get_spans(
            service_name=service_name,
            start_time=start_time,
            end_time=end_time
        )

        # Group spans by operation
        operations = {}
        for span in spans:
            op_name = span.operation_name
            if op_name not in operations:
                operations[op_name] = []
            operations[op_name].append(span)

        # Calculate metrics for each operation
        summaries = []
        for op_name, op_spans in operations.items():
            durations = [s.duration for s in op_spans]
            errors = [s for s in op_spans if s.has_error]

            summary = SpanSummary(
                operation_name=op_name,
                service_name=service_name,
                avg_duration=statistics.mean(durations),
                p95_duration=statistics.quantiles(durations, n=20)[18],  # 95th percentile
                p99_duration=statistics.quantiles(durations, n=100)[98],  # 99th percentile
                error_rate=len(errors) / len(op_spans),
                call_count=len(op_spans)
            )
            summaries.append(summary)

        return sorted(summaries, key=lambda s: s.p95_duration, reverse=True)

    def analyze_trace(self, trace_id: str) -> TraceAnalysis:
        """Analyze a specific trace for performance issues."""
        trace = self.jaeger_client.get_trace(trace_id)
        spans = trace.spans

        # Calculate total duration
        root_span = min(spans, key=lambda s: s.start_time)
        total_duration = max(s.start_time + s.duration for s in spans) - root_span.start_time

        # Find critical path (longest sequence of spans)
        critical_path = self._find_critical_path(spans)

        # Identify bottlenecks (spans that take >20% of total time)
        bottlenecks = [
            s.operation_name for s in spans
            if s.duration > total_duration * 0.2
        ]

        # Get involved services
        services_involved = list(set(s.service_name for s in spans))

        # Count errors
        error_count = len([s for s in spans if s.has_error])

        return TraceAnalysis(
            trace_id=trace_id,
            total_duration=total_duration,
            span_count=len(spans),
            error_count=error_count,
            critical_path=critical_path,
            bottlenecks=bottlenecks,
            services_involved=services_involved
        )

    def _find_critical_path(self, spans: List) -> List[str]:
        """Find the critical path through the trace."""
        # Build span hierarchy
        span_children = {}
        for span in spans:
            parent_id = span.parent_span_id
            if parent_id not in span_children:
                span_children[parent_id] = []
            span_children[parent_id].append(span)

        # Find path with maximum cumulative duration
        def calculate_path_duration(span_id, path):
            children = span_children.get(span_id, [])
            if not children:
                return path

            # Find child with maximum duration
            max_child = max(children, key=lambda s: s.duration)
            path.append(max_child.operation_name)
            return calculate_path_duration(max_child.span_id, path)

        root_span = next(s for s in spans if s.parent_span_id is None)
        return calculate_path_duration(root_span.span_id, [root_span.operation_name])

    def detect_anomalies(self, service_name: str) -> List[Dict[str, Any]]:
        """Detect performance anomalies in traces."""
        # Get recent performance baseline
        baseline_period = timedelta(hours=24)
        recent_period = timedelta(hours=1)

        baseline_summary = self.analyze_service_performance(service_name, baseline_period)
        recent_summary = self.analyze_service_performance(service_name, recent_period)

        anomalies = []

        for recent in recent_summary:
            # Find corresponding baseline operation
            baseline = next((b for b in baseline_summary if b.operation_name == recent.operation_name), None)
            if not baseline:
                continue

            # Check for duration anomalies (>2x baseline)
            if recent.p95_duration > baseline.p95_duration * 2:
                anomalies.append({
                    "type": "duration_anomaly",
                    "operation": recent.operation_name,
                    "baseline_p95": baseline.p95_duration,
                    "recent_p95": recent.p95_duration,
                    "increase_factor": recent.p95_duration / baseline.p95_duration
                })

            # Check for error rate anomalies (>5x baseline)
            if recent.error_rate > baseline.error_rate * 5:
                anomalies.append({
                    "type": "error_rate_anomaly",
                    "operation": recent.operation_name,
                    "baseline_error_rate": baseline.error_rate,
                    "recent_error_rate": recent.error_rate,
                    "increase_factor": recent.error_rate / baseline.error_rate if baseline.error_rate > 0 else "infinity"
                })

        return anomalies
```

---

## 4. Logging Standards

<!-- @nist-controls: [au-2, au-3, au-4, au-5, au-6, au-9] -->

### 4.1 Structured Logging

#### Log Format Standards **[REQUIRED]**
```python
# logging/structured_logging.py
import json
import logging
import time
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
import traceback
import threading

class StructuredLogger:
    # @nist au-3 "Structured audit record generation"
    # @nist au-9 "Protection of audit information"
    def __init__(self, service_name: str, version: str, environment: str):
        self.service_name = service_name
        self.version = version
        self.environment = environment
        self.correlation_id = None
        self._local = threading.local()

        # Configure base logger
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)

        # Remove default handlers
        self.logger.handlers.clear()

        # Add structured handler
        handler = logging.StreamHandler()
        handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(handler)

    def set_correlation_id(self, correlation_id: str):
        """Set correlation ID for request tracking."""
        self._local.correlation_id = correlation_id

    def get_correlation_id(self) -> Optional[str]:
        """Get current correlation ID."""
        return getattr(self._local, 'correlation_id', None)

    def _build_log_entry(self, level: str, message: str, **kwargs) -> Dict[str, Any]:
        """Build structured log entry.
        @nist au-3 "Content of audit records"
        @nist-implements au-3.1 "Additional audit information"
        """
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": level.upper(),
            "message": message,
            "service": self.service_name,
            "version": self.version,
            "environment": self.environment,
            "thread_id": threading.get_ident(),
            "process_id": os.getpid(),
        }

        # Add correlation ID if available
        correlation_id = self.get_correlation_id()
        if correlation_id:
            entry["correlation_id"] = correlation_id

        # Add trace context if available
        from opentelemetry import trace
        current_span = trace.get_current_span()
        if current_span and current_span.is_recording():
            span_context = current_span.get_span_context()
            entry["trace_id"] = format(span_context.trace_id, '032x')
            entry["span_id"] = format(span_context.span_id, '016x')

        # Add custom fields
        if kwargs:
            entry["fields"] = kwargs

        return entry

    def info(self, message: str, **kwargs):
        """Log info message."""
        entry = self._build_log_entry("info", message, **kwargs)
        self.logger.info(json.dumps(entry))

    def warning(self, message: str, **kwargs):
        """Log warning message."""
        entry = self._build_log_entry("warning", message, **kwargs)
        self.logger.warning(json.dumps(entry))

    def error(self, message: str, exception: Exception = None, **kwargs):
        """Log error message with optional exception.
        @nist si-11 "Error handling and logging"
        @nist au-2 "Log security-relevant errors"
        """
        if exception:
            kwargs.update({
                "exception_type": type(exception).__name__,
                "exception_message": str(exception),
                "stack_trace": traceback.format_exc()
            })

        entry = self._build_log_entry("error", message, **kwargs)
        self.logger.error(json.dumps(entry))

    def debug(self, message: str, **kwargs):
        """Log debug message."""
        entry = self._build_log_entry("debug", message, **kwargs)
        self.logger.debug(json.dumps(entry))

    def audit(self, action: str, user_id: str, resource: str, **kwargs):
        """Log audit event."""
        audit_data = {
            "action": action,
            "user_id": user_id,
            "resource": resource,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            **kwargs
        }

        entry = self._build_log_entry("audit", f"User {user_id} performed {action} on {resource}", **audit_data)
        self.logger.info(json.dumps(entry))

class StructuredFormatter(logging.Formatter):
    """Formatter for structured logs."""

    def format(self, record):
        # If the record message is already JSON, return as-is
        try:
            json.loads(record.getMessage())
            return record.getMessage()
        except (json.JSONDecodeError, ValueError):
            # Fall back to basic structured format
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
                "module": record.module,
                "function": record.funcName,
                "line": record.lineno,
            }

            if record.exc_info:
                log_entry["exception"] = self.formatException(record.exc_info)

            return json.dumps(log_entry)

# Usage example
import os

logger = StructuredLogger(
    service_name="user-service",
    version="1.2.0",
    environment=os.getenv("ENVIRONMENT", "development")
)

# Set correlation ID for request tracking
logger.set_correlation_id(str(uuid.uuid4()))

# Log structured messages
logger.info("User login attempt", user_id="12345", ip_address="192.168.1.1")
logger.warning("Rate limit approaching", user_id="12345", current_requests=45, limit=50)

try:
    # Some operation that might fail
    result = 1 / 0
except ZeroDivisionError as e:
    logger.error("Division by zero error", exception=e, operation="calculate_ratio")

# Audit logging
logger.audit("user_login", user_id="12345", resource="authentication_system",
            ip_address="192.168.1.1", success=True)
```

### 4.2 Log Aggregation and Analysis

#### ELK Stack Configuration **[REQUIRED]**
```yaml
# elk/elasticsearch.yml
cluster.name: "logging-cluster"
node.name: "logging-node-1"
network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node

# Index template for application logs
index_patterns: ["app-logs-*"]
template:
  settings:
    number_of_shards: 1
    number_of_replicas: 1
    index.refresh_interval: "5s"
    index.max_result_window: 50000
  mappings:
    properties:
      timestamp:
        type: date
        format: "strict_date_optional_time||epoch_millis"
      level:
        type: keyword
      message:
        type: text
        analyzer: standard
      service:
        type: keyword
      version:
        type: keyword
      environment:
        type: keyword
      correlation_id:
        type: keyword
      trace_id:
        type: keyword
      span_id:
        type: keyword
      fields:
        type: object
        dynamic: true

---
# logstash/pipeline.conf
input {
  beats {
    port => 5044
  }

  http {
    port => 8080
    codec => json
  }
}

filter {
  # Parse timestamp
  date {
    match => [ "timestamp", "ISO8601" ]
    target => "@timestamp"
  }

  # Extract log level
  if [level] {
    mutate {
      uppercase => [ "level" ]
    }
  }

  # Add index name based on service and date
  mutate {
    add_field => {
      "[@metadata][index]" => "app-logs-%{service}-%{+YYYY.MM.dd}"
    }
  }

  # Parse exception stack traces
  if [fields][exception_type] {
    mutate {
      add_tag => [ "exception" ]
    }
  }

  # Add geographical information for IP addresses
  if [fields][ip_address] {
    geoip {
      source => "[fields][ip_address]"
      target => "geoip"
    }
  }
}

output {
  elasticsearch {
    hosts => ["elasticsearch:9200"]
    index => "%{[@metadata][index]}"
    template_name => "app-logs"
    template_pattern => "app-logs-*"
    template_overwrite => true
  }

  # Output to stdout for debugging
  stdout {
    codec => rubydebug
  }
}

---
# kibana/kibana.yml
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://elasticsearch:9200"]
elasticsearch.username: "kibana_system"
elasticsearch.password: "password"

# Dashboard configuration
xpack.reporting.enabled: true
xpack.security.enabled: false
logging.level: info
```

#### Log Analysis Queries **[REQUIRED]**
```json
{
  "kibana_queries": {
    "error_rate_by_service": {
      "query": {
        "bool": {
          "must": [
            {"term": {"level": "ERROR"}},
            {"range": {"@timestamp": {"gte": "now-1h"}}}
          ]
        }
      },
      "aggs": {
        "services": {
          "terms": {"field": "service"},
          "aggs": {
            "error_count": {"value_count": {"field": "level"}}
          }
        }
      }
    },

    "slow_requests": {
      "query": {
        "bool": {
          "must": [
            {"exists": {"field": "fields.duration"}},
            {"range": {"fields.duration": {"gte": 1000}}},
            {"range": {"@timestamp": {"gte": "now-1h"}}}
          ]
        }
      },
      "sort": [{"fields.duration": {"order": "desc"}}]
    },

    "trace_analysis": {
      "query": {
        "bool": {
          "must": [
            {"term": {"trace_id": "TRACE_ID_HERE"}}
          ]
        }
      },
      "sort": [{"@timestamp": {"order": "asc"}}]
    },

    "user_activity_analysis": {
      "query": {
        "bool": {
          "must": [
            {"term": {"fields.user_id": "USER_ID_HERE"}},
            {"range": {"@timestamp": {"gte": "now-24h"}}}
          ]
        }
      },
      "aggs": {
        "activity_timeline": {
          "date_histogram": {
            "field": "@timestamp",
            "calendar_interval": "hour"
          }
        },
        "actions": {
          "terms": {"field": "fields.action"}
        }
      }
    }
  }
}
```

---

## 5. Service Level Objectives (SLOs)

### 5.1 SLO Definition Framework

#### SLO Configuration **[REQUIRED]**
```yaml
# slo/service_slos.yml
slos:
  user_service:
    availability:
      objective: 99.9%
      measurement_window: 30d
      error_budget: 0.1%
      sli_definition: |
        (sum(rate(http_requests_total{service="user-service",status_code!~"5.."}[5m])) /
         sum(rate(http_requests_total{service="user-service"}[5m]))) * 100
      alerting_threshold: 50%  # Alert when 50% of error budget is consumed

    latency:
      objective: 95%  # 95% of requests < 200ms
      threshold: 0.2  # 200ms
      measurement_window: 30d
      sli_definition: |
        histogram_quantile(0.95,
          rate(http_request_duration_seconds_bucket{service="user-service"}[5m])
        ) < 0.2
      alerting_threshold: 90%

    throughput:
      objective: 1000  # requests per second
      measurement_window: 1h
      sli_definition: |
        rate(http_requests_total{service="user-service"}[5m])
      alerting_threshold: 800  # Alert if below 800 RPS

  payment_service:
    availability:
      objective: 99.95%
      measurement_window: 30d
      error_budget: 0.05%
      sli_definition: |
        (sum(rate(http_requests_total{service="payment-service",status_code!~"5.."}[5m])) /
         sum(rate(http_requests_total{service="payment-service"}[5m]))) * 100

    latency:
      objective: 99%  # 99% of requests < 500ms
      threshold: 0.5
      measurement_window: 30d
      sli_definition: |
        histogram_quantile(0.99,
          rate(http_request_duration_seconds_bucket{service="payment-service"}[5m])
        ) < 0.5

business_slos:
  user_experience:
    page_load_time:
      objective: 95%  # 95% of page loads < 2s
      threshold: 2.0
      measurement_window: 24h
      sli_definition: |
        histogram_quantile(0.95,
          rate(page_load_duration_seconds_bucket[5m])
        ) < 2.0

    checkout_success_rate:
      objective: 99.5%
      measurement_window: 7d
      sli_definition: |
        (sum(rate(checkout_completed_total[5m])) /
         sum(rate(checkout_started_total[5m]))) * 100
```

#### SLO Monitoring Implementation **[REQUIRED]**
```python
# slo/slo_monitoring.py
import time
import statistics
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

class SLOStatus(Enum):
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    BREACH = "breach"

@dataclass
class SLOResult:
    name: str
    current_value: float
    objective: float
    status: SLOStatus
    error_budget_remaining: float
    measurement_window: timedelta
    last_updated: datetime

@dataclass
class ErrorBudget:
    total_budget: float
    consumed: float
    remaining: float
    burn_rate: float  # Current rate of consumption per hour

class SLOMonitor:
    def __init__(self, prometheus_client, config: Dict[str, Any]):
        self.prometheus = prometheus_client
        self.config = config
        self.slo_history = {}

    def evaluate_slo(self, service_name: str, slo_name: str) -> SLOResult:
        """Evaluate a specific SLO."""
        slo_config = self.config['slos'][service_name][slo_name]

        # Query Prometheus for SLI value
        query = slo_config['sli_definition']
        result = self.prometheus.query(query)

        if not result:
            raise Exception(f"No data available for SLO {service_name}.{slo_name}")

        current_value = float(result[0]['value'][1])
        objective = slo_config['objective']

        # Calculate error budget
        if slo_name == 'availability':
            error_budget = self._calculate_availability_error_budget(
                current_value, objective, slo_config['measurement_window']
            )
        elif slo_name == 'latency':
            error_budget = self._calculate_latency_error_budget(
                current_value, objective, slo_config['threshold']
            )
        else:
            error_budget = ErrorBudget(0, 0, 0, 0)  # Default for other SLO types

        # Determine status
        status = self._determine_slo_status(current_value, objective, error_budget, slo_config)

        return SLOResult(
            name=f"{service_name}.{slo_name}",
            current_value=current_value,
            objective=objective,
            status=status,
            error_budget_remaining=error_budget.remaining,
            measurement_window=timedelta(days=30),  # From config
            last_updated=datetime.utcnow()
        )

    def _calculate_availability_error_budget(self, current_availability: float,
                                           objective: float, window: str) -> ErrorBudget:
        """Calculate error budget for availability SLO."""
        # Convert window to hours
        window_hours = self._parse_time_window(window)

        # Calculate total error budget (time that can be unavailable)
        total_budget_hours = window_hours * (1 - objective / 100)

        # Calculate consumed budget
        consumed_hours = window_hours * (1 - current_availability / 100)

        # Calculate remaining budget
        remaining_hours = total_budget_hours - consumed_hours
        remaining_percentage = (remaining_hours / total_budget_hours) * 100 if total_budget_hours > 0 else 0

        # Calculate burn rate (simplified - would need historical data for accuracy)
        burn_rate = consumed_hours / window_hours if window_hours > 0 else 0

        return ErrorBudget(
            total_budget=total_budget_hours,
            consumed=consumed_hours,
            remaining=remaining_percentage,
            burn_rate=burn_rate
        )

    def _calculate_latency_error_budget(self, current_latency: float,
                                      objective: float, threshold: float) -> ErrorBudget:
        """Calculate error budget for latency SLO."""
        # For latency SLOs, error budget is based on percentage of requests above threshold
        if current_latency <= threshold:
            remaining = 100.0
            consumed = 0.0
        else:
            # Simplified calculation - would need more sophisticated logic in practice
            overage = (current_latency - threshold) / threshold
            consumed = min(overage * 100, 100)
            remaining = max(100 - consumed, 0)

        return ErrorBudget(
            total_budget=100.0,
            consumed=consumed,
            remaining=remaining,
            burn_rate=consumed  # Simplified
        )

    def _determine_slo_status(self, current_value: float, objective: float,
                            error_budget: ErrorBudget, config: Dict) -> SLOStatus:
        """Determine SLO status based on current performance and error budget."""

        # Check if SLO is breached
        if (config.get('type') == 'availability' and current_value < objective) or \
           (config.get('type') == 'latency' and current_value > config.get('threshold', 0)):
            return SLOStatus.BREACH

        # Check error budget consumption
        if error_budget.remaining <= 10:  # Less than 10% error budget remaining
            return SLOStatus.CRITICAL
        elif error_budget.remaining <= 25:  # Less than 25% error budget remaining
            return SLOStatus.WARNING
        else:
            return SLOStatus.HEALTHY

    def _parse_time_window(self, window: str) -> float:
        """Parse time window string to hours."""
        if window.endswith('d'):
            return float(window[:-1]) * 24
        elif window.endswith('h'):
            return float(window[:-1])
        elif window.endswith('m'):
            return float(window[:-1]) / 60
        else:
            return 24.0  # Default to 24 hours

    def evaluate_all_slos(self) -> List[SLOResult]:
        """Evaluate all configured SLOs."""
        results = []

        for service_name, service_slos in self.config['slos'].items():
            for slo_name in service_slos:
                try:
                    result = self.evaluate_slo(service_name, slo_name)
                    results.append(result)
                except Exception as e:
                    print(f"Failed to evaluate SLO {service_name}.{slo_name}: {e}")

        return results

    def generate_slo_report(self) -> Dict[str, Any]:
        """Generate comprehensive SLO report."""
        results = self.evaluate_all_slos()

        # Categorize by status
        status_counts = {status: 0 for status in SLOStatus}
        for result in results:
            status_counts[result.status] += 1

        # Find SLOs at risk
        at_risk = [r for r in results if r.status in [SLOStatus.WARNING, SLOStatus.CRITICAL]]
        breached = [r for r in results if r.status == SLOStatus.BREACH]

        return {
            "report_timestamp": datetime.utcnow().isoformat(),
            "total_slos": len(results),
            "status_summary": {status.value: count for status, count in status_counts.items()},
            "slos_at_risk": len(at_risk),
            "slos_breached": len(breached),
            "detailed_results": [
                {
                    "name": r.name,
                    "status": r.status.value,
                    "current_value": r.current_value,
                    "objective": r.objective,
                    "error_budget_remaining": r.error_budget_remaining
                }
                for r in results
            ],
            "recommendations": self._generate_recommendations(results)
        }

    def _generate_recommendations(self, results: List[SLOResult]) -> List[str]:
        """Generate recommendations based on SLO status."""
        recommendations = []

        breached = [r for r in results if r.status == SLOStatus.BREACH]
        critical = [r for r in results if r.status == SLOStatus.CRITICAL]

        if breached:
            recommendations.append(f"URGENT: {len(breached)} SLOs are breached. Immediate action required.")

        if critical:
            recommendations.append(f"WARNING: {len(critical)} SLOs are critical. Error budget nearly exhausted.")

        # Check for patterns
        availability_issues = [r for r in results if 'availability' in r.name and r.status != SLOStatus.HEALTHY]
        if len(availability_issues) > 1:
            recommendations.append("Multiple availability SLOs affected. Check for infrastructure issues.")

        latency_issues = [r for r in results if 'latency' in r.name and r.status != SLOStatus.HEALTHY]
        if len(latency_issues) > 1:
            recommendations.append("Multiple latency SLOs affected. Check for performance degradation.")

        return recommendations

# Usage
slo_monitor = SLOMonitor(prometheus_client, slo_config)
report = slo_monitor.generate_slo_report()
print(json.dumps(report, indent=2))
```

---

## 6. Alerting and Incident Response

### 6.1 Alert Configuration

#### Prometheus Alerting Rules **[REQUIRED]**
```yaml
# prometheus/alert_rules.yml
groups:
  - name: SLO_Alerts
    rules:
      # High Error Rate
      - alert: HighErrorRate
        expr: |
          (
            rate(http_requests_total{status_code=~"5.."}[5m]) /
            rate(http_requests_total[5m])
          ) * 100 > 1
        for: 2m
        labels:
          severity: critical
          team: platform
          service: "{{ $labels.service }}"
        annotations:
          summary: "High error rate detected for {{ $labels.service }}"
          description: |
            Error rate is {{ $value | humanizePercentage }} for service {{ $labels.service }}.
            This is above the 1% threshold for 2 minutes.
          runbook_url: "https://runbooks.company.com/high-error-rate"
          dashboard_url: "https://grafana.company.com/d/service-overview?var-service={{ $labels.service }}"

      # High Latency
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95,
            rate(http_request_duration_seconds_bucket[5m])
          ) > 0.5
        for: 5m
        labels:
          severity: warning
          team: platform
          service: "{{ $labels.service }}"
        annotations:
          summary: "High latency detected for {{ $labels.service }}"
          description: |
            95th percentile latency is {{ $value }}s for service {{ $labels.service }}.
            This is above the 500ms threshold for 5 minutes.

      # SLO Error Budget Consumption
      - alert: SLOErrorBudgetCritical
        expr: |
          (1 - slo_availability_ratio) * 100 > 0.05  # >50% of 0.1% error budget
        for: 1m
        labels:
          severity: critical
          team: platform
          slo_type: availability
        annotations:
          summary: "SLO error budget critically low"
          description: |
            Error budget consumption is {{ $value }}% for {{ $labels.service }}.
            At current rate, error budget will be exhausted in less than 1 day.

      # Service Down
      - alert: ServiceDown
        expr: up == 0
        for: 1m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Service {{ $labels.instance }} is down"
          description: |
            Service {{ $labels.instance }} has been down for more than 1 minute.

  - name: Infrastructure_Alerts
    rules:
      # High CPU Usage
      - alert: HighCPUUsage
        expr: |
          (1 - avg by(instance) (rate(node_cpu_seconds_total{mode="idle"}[5m]))) * 100 > 80
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "High CPU usage on {{ $labels.instance }}"
          description: |
            CPU usage is {{ $value | humanizePercentage }} on {{ $labels.instance }}.

      # High Memory Usage
      - alert: HighMemoryUsage
        expr: |
          (1 - (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes)) * 100 > 90
        for: 5m
        labels:
          severity: critical
          team: infrastructure
        annotations:
          summary: "High memory usage on {{ $labels.instance }}"
          description: |
            Memory usage is {{ $value | humanizePercentage }} on {{ $labels.instance }}.

      # Disk Space Low
      - alert: DiskSpaceLow
        expr: |
          (1 - (node_filesystem_avail_bytes / node_filesystem_size_bytes)) * 100 > 85
        for: 5m
        labels:
          severity: warning
          team: infrastructure
        annotations:
          summary: "Low disk space on {{ $labels.instance }}"
          description: |
            Disk usage is {{ $value | humanizePercentage }} on {{ $labels.instance }}:{{ $labels.mountpoint }}.

  - name: Business_Alerts
    rules:
      # Low Conversion Rate
      - alert: LowConversionRate
        expr: |
          (
            rate(orders_completed_total[5m]) /
            rate(sessions_started_total[5m])
          ) * 100 < 2
        for: 10m
        labels:
          severity: warning
          team: business
        annotations:
          summary: "Conversion rate is critically low"
          description: |
            Conversion rate is {{ $value | humanizePercentage }}, below 2% threshold.

      # Payment Failures
      - alert: HighPaymentFailureRate
        expr: |
          (
            rate(payment_failures_total[5m]) /
            rate(payment_attempts_total[5m])
          ) * 100 > 5
        for: 2m
        labels:
          severity: critical
          team: payments
        annotations:
          summary: "High payment failure rate"
          description: |
            Payment failure rate is {{ $value | humanizePercentage }}, above 5% threshold.
```

### 6.2 Incident Response Automation

#### AlertManager Configuration **[REQUIRED]**
```yaml
# alertmanager/alertmanager.yml
global:
  smtp_smarthost: 'localhost:587'
  smtp_from: 'alerts@company.com'
  slack_api_url: 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'

# Inhibition rules - suppress certain alerts when others are firing
inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service', 'instance']

# Routing rules
route:
  group_by: ['alertname', 'service']
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 4h
  receiver: 'default-receiver'

  routes:
    # Critical alerts go to on-call immediately
    - match:
        severity: critical
      receiver: 'critical-alerts'
      group_wait: 10s
      repeat_interval: 5m

    # SLO alerts
    - match:
        team: platform
      receiver: 'platform-team'

    # Business alerts
    - match:
        team: business
      receiver: 'business-team'

    # Infrastructure alerts
    - match:
        team: infrastructure
      receiver: 'infrastructure-team'

receivers:
  - name: 'default-receiver'
    email_configs:
      - to: 'team@company.com'
        subject: 'Alert: {{ .GroupLabels.alertname }}'
        body: |
          {{ range .Alerts }}
          Alert: {{ .Annotations.summary }}
          Description: {{ .Annotations.description }}
          {{ end }}

  - name: 'critical-alerts'
    slack_configs:
      - channel: '#critical-alerts'
        color: 'danger'
        title: 'CRITICAL: {{ .GroupLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          *Alert:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          *Runbook:* {{ .Annotations.runbook_url }}
          *Dashboard:* {{ .Annotations.dashboard_url }}
          {{ end }}
    pagerduty_configs:
      - service_key: 'YOUR_PAGERDUTY_SERVICE_KEY'
        description: '{{ .GroupLabels.alertname }}: {{ .CommonAnnotations.summary }}'

  - name: 'platform-team'
    slack_configs:
      - channel: '#platform-alerts'
        color: '{{ if eq .Status "firing" }}warning{{ else }}good{{ end }}'
        title: '{{ .GroupLabels.alertname }}'
        text: |
          {{ range .Alerts }}
          *Service:* {{ .Labels.service }}
          *Summary:* {{ .Annotations.summary }}
          *Description:* {{ .Annotations.description }}
          {{ end }}

  - name: 'business-team'
    slack_configs:
      - channel: '#business-alerts'
        color: 'warning'
        title: 'Business Metric Alert: {{ .GroupLabels.alertname }}'

  - name: 'infrastructure-team'
    email_configs:
      - to: 'infrastructure@company.com'
        subject: 'Infrastructure Alert: {{ .GroupLabels.alertname }}'
```

#### Incident Response Automation **[REQUIRED]**
```python
# incident/response_automation.py
import requests
import json
import time
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum

class IncidentSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class IncidentStatus(Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"

@dataclass
class Incident:
    id: str
    title: str
    description: str
    severity: IncidentSeverity
    status: IncidentStatus
    affected_services: List[str]
    created_at: datetime
    updated_at: datetime
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None

class IncidentManager:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.incidents = {}  # In practice, this would be a database
        self.notification_channels = {
            'slack': SlackNotifier(config['slack']),
            'pagerduty': PagerDutyNotifier(config['pagerduty']),
            'email': EmailNotifier(config['email'])
        }

    def create_incident(self, alert_data: Dict[str, Any]) -> Incident:
        """Create a new incident from alert data."""
        # Generate incident ID
        incident_id = f"INC-{int(time.time())}"

        # Determine severity from alert
        severity = self._map_alert_severity(alert_data.get('labels', {}).get('severity', 'warning'))

        # Extract affected services
        affected_services = [alert_data.get('labels', {}).get('service', 'unknown')]

        incident = Incident(
            id=incident_id,
            title=alert_data.get('annotations', {}).get('summary', 'Unknown Alert'),
            description=alert_data.get('annotations', {}).get('description', ''),
            severity=severity,
            status=IncidentStatus.OPEN,
            affected_services=affected_services,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        self.incidents[incident_id] = incident

        # Trigger automated response
        self._trigger_incident_response(incident, alert_data)

        return incident

    def _map_alert_severity(self, alert_severity: str) -> IncidentSeverity:
        """Map alert severity to incident severity."""
        mapping = {
            'critical': IncidentSeverity.CRITICAL,
            'warning': IncidentSeverity.MEDIUM,
            'info': IncidentSeverity.LOW
        }
        return mapping.get(alert_severity.lower(), IncidentSeverity.MEDIUM)

    def _trigger_incident_response(self, incident: Incident, alert_data: Dict[str, Any]):
        """Trigger automated incident response actions."""

        # 1. Send notifications based on severity
        if incident.severity == IncidentSeverity.CRITICAL:
            self._send_critical_notifications(incident, alert_data)
        else:
            self._send_standard_notifications(incident, alert_data)

        # 2. Auto-assign if possible
        assignee = self._determine_assignee(incident, alert_data)
        if assignee:
            self.assign_incident(incident.id, assignee)

        # 3. Create war room if critical
        if incident.severity == IncidentSeverity.CRITICAL:
            self._create_war_room(incident)

        # 4. Update status page if public-facing service
        if self._is_public_facing_service(incident.affected_services):
            self._update_status_page(incident)

        # 5. Trigger automated remediation if available
        self._attempt_auto_remediation(incident, alert_data)

    def _send_critical_notifications(self, incident: Incident, alert_data: Dict[str, Any]):
        """Send notifications for critical incidents."""
        # PagerDuty for immediate response
        self.notification_channels['pagerduty'].trigger_incident(
            incident_key=incident.id,
            description=incident.title,
            details=alert_data
        )

        # Slack to critical channel
        self.notification_channels['slack'].send_critical_alert(
            incident=incident,
            channel='#critical-incidents',
            alert_data=alert_data
        )

        # Email to leadership for SEV1
        if incident.severity == IncidentSeverity.CRITICAL:
            self.notification_channels['email'].send_incident_notification(
                incident=incident,
                recipients=['leadership@company.com'],
                template='critical_incident'
            )

    def _send_standard_notifications(self, incident: Incident, alert_data: Dict[str, Any]):
        """Send standard notifications for non-critical incidents."""
        # Slack to team channel
        team = alert_data.get('labels', {}).get('team', 'platform')
        channel = f"#{team}-alerts"

        self.notification_channels['slack'].send_alert(
            incident=incident,
            channel=channel,
            alert_data=alert_data
        )

    def _determine_assignee(self, incident: Incident, alert_data: Dict[str, Any]) -> Optional[str]:
        """Determine who should be assigned to the incident."""
        # Get team from alert labels
        team = alert_data.get('labels', {}).get('team')
        service = alert_data.get('labels', {}).get('service')

        # Lookup on-call engineer
        oncall_schedule = self.config.get('oncall_schedules', {})
        if team in oncall_schedule:
            return self._get_oncall_engineer(team)
        elif service in self.config.get('service_owners', {}):
            return self.config['service_owners'][service]

        return None

    def _get_oncall_engineer(self, team: str) -> Optional[str]:
        """Get current on-call engineer for team."""
        # In practice, this would integrate with PagerDuty or similar
        oncall_api = self.config.get('oncall_schedules', {}).get(team, {})
        if oncall_api:
            # Mock implementation
            return "oncall-engineer@company.com"
        return None

    def _create_war_room(self, incident: Incident):
        """Create war room for critical incident coordination."""
        # Create Slack channel
        channel_name = f"incident-{incident.id.lower()}"

        self.notification_channels['slack'].create_channel(
            name=channel_name,
            purpose=f"War room for {incident.title}",
            initial_members=['@incident-commander', '@on-call-engineer']
        )

        # Pin incident information
        incident_summary = f"""
        🚨 **INCIDENT {incident.id}** 🚨
        **Title:** {incident.title}
        **Severity:** {incident.severity.value.upper()}
        **Affected Services:** {', '.join(incident.affected_services)}
        **Created:** {incident.created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}

        **Next Steps:**
        1. Incident Commander: Assess impact and coordinate response
        2. On-call Engineer: Begin investigation and mitigation
        3. Communications: Prepare customer communications if needed
        """

        self.notification_channels['slack'].pin_message(
            channel=channel_name,
            message=incident_summary
        )

    def _is_public_facing_service(self, services: List[str]) -> bool:
        """Check if any affected services are public-facing."""
        public_services = self.config.get('public_services', [])
        return any(service in public_services for service in services)

    def _update_status_page(self, incident: Incident):
        """Update external status page for public incidents."""
        status_page_api = self.config.get('status_page', {})
        if not status_page_api:
            return

        # Map incident severity to status page impact
        impact_mapping = {
            IncidentSeverity.CRITICAL: 'critical',
            IncidentSeverity.HIGH: 'major',
            IncidentSeverity.MEDIUM: 'minor',
            IncidentSeverity.LOW: 'maintenance'
        }

        impact = impact_mapping[incident.severity]

        # Create status page incident
        status_incident = {
            'name': incident.title,
            'status': 'investigating',
            'impact': impact,
            'component_ids': self._get_component_ids(incident.affected_services),
            'body': incident.description or 'We are investigating reports of issues with our service.'
        }

        # Post to status page API (implementation would depend on provider)
        # self._post_to_status_page(status_incident)

    def _attempt_auto_remediation(self, incident: Incident, alert_data: Dict[str, Any]):
        """Attempt automated remediation based on alert type."""
        alert_name = alert_data.get('labels', {}).get('alertname', '')

        remediation_actions = {
            'HighMemoryUsage': self._restart_high_memory_pods,
            'ServiceDown': self._restart_failed_service,
            'HighErrorRate': self._enable_circuit_breaker,
            'HighLatency': self._scale_up_service
        }

        if alert_name in remediation_actions:
            action = remediation_actions[alert_name]
            try:
                result = action(incident, alert_data)
                if result:
                    self._add_incident_note(
                        incident.id,
                        f"Automated remediation attempted: {alert_name}"
                    )
            except Exception as e:
                self._add_incident_note(
                    incident.id,
                    f"Automated remediation failed: {str(e)}"
                )

    def _restart_high_memory_pods(self, incident: Incident, alert_data: Dict) -> bool:
        """Restart pods with high memory usage."""
        # Implementation would use Kubernetes API
        return True

    def _restart_failed_service(self, incident: Incident, alert_data: Dict) -> bool:
        """Restart failed service."""
        # Implementation would use orchestration system API
        return True

    def _enable_circuit_breaker(self, incident: Incident, alert_data: Dict) -> bool:
        """Enable circuit breaker for service with high error rate."""
        # Implementation would configure load balancer or service mesh
        return True

    def _scale_up_service(self, incident: Incident, alert_data: Dict) -> bool:
        """Scale up service experiencing high latency."""
        # Implementation would use auto-scaling API
        return True

    def assign_incident(self, incident_id: str, assignee: str):
        """Assign incident to a person."""
        if incident_id in self.incidents:
            self.incidents[incident_id].assigned_to = assignee
            self.incidents[incident_id].updated_at = datetime.utcnow()

    def update_incident_status(self, incident_id: str, status: IncidentStatus, notes: str = None):
        """Update incident status."""
        if incident_id in self.incidents:
            incident = self.incidents[incident_id]
            incident.status = status
            incident.updated_at = datetime.utcnow()
            if notes:
                incident.resolution_notes = notes

    def _add_incident_note(self, incident_id: str, note: str):
        """Add note to incident (simplified - would be in timeline in practice)."""
        if incident_id in self.incidents:
            incident = self.incidents[incident_id]
            current_notes = incident.resolution_notes or ""
            timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
            incident.resolution_notes = f"{current_notes}\n[{timestamp}] {note}"

# Notification channel implementations would be separate classes
class SlackNotifier:
    def __init__(self, config): pass
    def send_critical_alert(self, incident, channel, alert_data): pass
    def send_alert(self, incident, channel, alert_data): pass
    def create_channel(self, name, purpose, initial_members): pass
    def pin_message(self, channel, message): pass

class PagerDutyNotifier:
    def __init__(self, config): pass
    def trigger_incident(self, incident_key, description, details): pass

class EmailNotifier:
    def __init__(self, config): pass
    def send_incident_notification(self, incident, recipients, template): pass
```

---

## Implementation Checklist

### Observability Foundation
- [ ] OpenTelemetry instrumentation implemented
- [ ] Three pillars (metrics, logs, traces) configured
- [ ] Service instrumentation automated
- [ ] Context propagation working
- [ ] Resource attributes standardized

### Metrics and Monitoring
- [ ] Prometheus configured and running
- [ ] Application metrics implemented
- [ ] Recording rules defined
- [ ] Business metrics tracked
- [ ] Metric cardinality managed

### Distributed Tracing
- [ ] Jaeger deployed and configured
- [ ] Trace sampling configured
- [ ] Advanced tracing patterns implemented
- [ ] Trace analysis automated
- [ ] Performance bottlenecks identified

### Logging
- [ ] Structured logging implemented
- [ ] Log aggregation configured (ELK/EFK)
- [ ] Log retention policies defined
- [ ] Correlation IDs implemented
- [ ] Log analysis queries created

### SLOs and Error Budgets
- [ ] SLOs defined for critical services
- [ ] SLI queries implemented
- [ ] Error budget tracking automated
- [ ] SLO reporting dashboard created
- [ ] Alerting on SLO violations configured

### Alerting and Incident Response
- [ ] Alert rules comprehensive
- [ ] AlertManager configured
- [ ] Incident response automation implemented
- [ ] On-call schedules configured
- [ ] Runbooks created and linked

### Performance Monitoring
- [ ] Performance baselines established
- [ ] Anomaly detection configured
- [ ] Capacity planning metrics tracked
- [ ] Performance regression detection automated
- [ ] Optimization recommendations automated

### Infrastructure Observability
- [ ] Node exporter deployed
- [ ] Kubernetes metrics collected
- [ ] Container metrics monitored
- [ ] Network metrics tracked
- [ ] Storage metrics monitored

---

**End of Observability and Monitoring Standards**
