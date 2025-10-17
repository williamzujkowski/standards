#!/usr/bin/env bash
# Setup Monitoring Stack with Docker Compose
# Includes: Prometheus, Grafana, Loki, Promtail, Jaeger, OpenTelemetry Collector

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${SCRIPT_DIR}/.."
STACK_NAME="${STACK_NAME:-monitoring}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $*"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $*"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $*"
}

check_dependencies() {
    log_info "Checking dependencies..."

    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi

    log_info "Dependencies check passed."
}

create_directories() {
    log_info "Creating necessary directories..."

    mkdir -p "${PROJECT_ROOT}/data/prometheus"
    mkdir -p "${PROJECT_ROOT}/data/grafana"
    mkdir -p "${PROJECT_ROOT}/data/loki"
    mkdir -p "${PROJECT_ROOT}/data/jaeger"
    mkdir -p "${PROJECT_ROOT}/data/alertmanager"
    mkdir -p "${PROJECT_ROOT}/logs"

    # Set permissions
    chmod -R 777 "${PROJECT_ROOT}/data"
    chmod -R 777 "${PROJECT_ROOT}/logs"
}

generate_docker_compose() {
    log_info "Generating docker-compose.yml..."

    cat > "${PROJECT_ROOT}/docker-compose.yml" << 'COMPOSE_EOF'
version: '3.8'

networks:
  monitoring:
    driver: bridge

volumes:
  prometheus-data:
  grafana-data:
  loki-data:
  jaeger-data:

services:
  # Prometheus - Metrics collection and storage
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "9090:9090"
    volumes:
      - ./config/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - ./templates/recording-rules.yml:/etc/prometheus/recording-rules.yml:ro
      - ./templates/alert-rules.yml:/etc/prometheus/alert-rules.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=15d'
      - '--web.console.libraries=/usr/share/prometheus/console_libraries'
      - '--web.console.templates=/usr/share/prometheus/consoles'
      - '--web.enable-lifecycle'
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:9090/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Node Exporter - System metrics
  node-exporter:
    image: prom/node-exporter:latest
    container_name: node-exporter
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "9100:9100"
    command:
      - '--path.procfs=/host/proc'
      - '--path.sysfs=/host/sys'
      - '--collector.filesystem.mount-points-exclude=^/(sys|proc|dev|host|etc)($$|/)'
    volumes:
      - /proc:/host/proc:ro
      - /sys:/host/sys:ro
      - /:/rootfs:ro

  # cAdvisor - Container metrics
  cadvisor:
    image: gcr.io/cadvisor/cadvisor:latest
    container_name: cadvisor
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "8080:8080"
    volumes:
      - /:/rootfs:ro
      - /var/run:/var/run:ro
      - /sys:/sys:ro
      - /var/lib/docker/:/var/lib/docker:ro
    privileged: true
    devices:
      - /dev/kmsg

  # Grafana - Visualization
  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
      - GF_INSTALL_PLUGINS=grafana-piechart-panel
    volumes:
      - grafana-data:/var/lib/grafana
      - ./templates/grafana-dashboard.json:/etc/grafana/provisioning/dashboards/api-service.json:ro
    depends_on:
      - prometheus
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Loki - Log aggregation
  loki:
    image: grafana/loki:latest
    container_name: loki
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "3100:3100"
    volumes:
      - loki-data:/loki
    command: -config.file=/etc/loki/local-config.yaml
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:3100/ready"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Promtail - Log shipper
  promtail:
    image: grafana/promtail:latest
    container_name: promtail
    restart: unless-stopped
    networks:
      - monitoring
    volumes:
      - /var/log:/var/log:ro
      - /var/lib/docker/containers:/var/lib/docker/containers:ro
    command: -config.file=/etc/promtail/config.yml
    depends_on:
      - loki

  # Jaeger - Distributed tracing
  jaeger:
    image: jaegertracing/all-in-one:latest
    container_name: jaeger
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "5775:5775/udp"  # zipkin.thrift compact
      - "6831:6831/udp"  # jaeger.thrift compact
      - "6832:6832/udp"  # jaeger.thrift binary
      - "5778:5778"      # serve configs
      - "16686:16686"    # frontend
      - "14268:14268"    # jaeger.thrift
      - "14250:14250"    # model.proto
      - "9411:9411"      # zipkin
    environment:
      - COLLECTOR_ZIPKIN_HOST_PORT=:9411
      - COLLECTOR_OTLP_ENABLED=true
    volumes:
      - jaeger-data:/badger
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:14269/"]
      interval: 30s
      timeout: 10s
      retries: 3

  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector-contrib:latest
    container_name: otel-collector
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "4317:4317"   # OTLP gRPC
      - "4318:4318"   # OTLP HTTP
      - "8888:8888"   # Metrics endpoint
      - "8889:8889"   # Prometheus exporter
      - "13133:13133" # Health check
    volumes:
      - ./templates/otel-collector.yaml:/etc/otel-collector-config.yaml:ro
    command: ["--config=/etc/otel-collector-config.yaml"]
    depends_on:
      - prometheus
      - jaeger
      - loki
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:13133"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Alertmanager - Alert routing
  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "9093:9093"
    volumes:
      - ./data/alertmanager:/alertmanager
    command:
      - '--config.file=/alertmanager/alertmanager.yml'
      - '--storage.path=/alertmanager'
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:9093/-/healthy"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Blackbox Exporter - Endpoint monitoring
  blackbox-exporter:
    image: prom/blackbox-exporter:latest
    container_name: blackbox-exporter
    restart: unless-stopped
    networks:
      - monitoring
    ports:
      - "9115:9115"
    command:
      - '--config.file=/etc/blackbox/blackbox.yml'
COMPOSE_EOF

    log_info "docker-compose.yml generated successfully."
}

generate_alertmanager_config() {
    log_info "Generating alertmanager configuration..."

    mkdir -p "${PROJECT_ROOT}/data/alertmanager"

    cat > "${PROJECT_ROOT}/data/alertmanager/alertmanager.yml" << 'ALERTMANAGER_EOF'
global:
  resolve_timeout: 5m
  slack_api_url: 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 12h

  routes:
    - match:
        severity: critical
      receiver: 'pagerduty'
      continue: true

    - match:
        severity: warning
      receiver: 'slack-warnings'

receivers:
  - name: 'default'
    webhook_configs:
      - url: 'http://localhost:5001/'

  - name: 'slack-warnings'
    slack_configs:
      - channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'
        text: '{{ range .Alerts }}{{ .Annotations.description }}{{ end }}'

  - name: 'pagerduty'
    webhook_configs:
      - url: 'http://localhost:5001/pagerduty'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'instance']
ALERTMANAGER_EOF

    log_info "Alertmanager configuration generated."
}

start_stack() {
    log_info "Starting monitoring stack..."

    cd "${PROJECT_ROOT}"
    docker-compose up -d

    log_info "Waiting for services to be healthy..."
    sleep 10

    log_info "Monitoring stack started successfully!"
}

print_access_info() {
    echo ""
    echo "========================================="
    echo "  Monitoring Stack Access Information"
    echo "========================================="
    echo ""
    echo "Prometheus:      http://localhost:9090"
    echo "Grafana:         http://localhost:3000 (admin/admin)"
    echo "Jaeger UI:       http://localhost:16686"
    echo "Alertmanager:    http://localhost:9093"
    echo "Loki:            http://localhost:3100"
    echo "Node Exporter:   http://localhost:9100"
    echo "cAdvisor:        http://localhost:8080"
    echo "OTel Collector:  http://localhost:8888/metrics"
    echo ""
    echo "========================================="
    echo ""
}

stop_stack() {
    log_info "Stopping monitoring stack..."
    cd "${PROJECT_ROOT}"
    docker-compose down
    log_info "Monitoring stack stopped."
}

cleanup_stack() {
    log_warn "This will remove all monitoring data. Are you sure? (yes/no)"
    read -r response
    if [[ "$response" == "yes" ]]; then
        log_info "Cleaning up monitoring stack..."
        cd "${PROJECT_ROOT}"
        docker-compose down -v
        rm -rf "${PROJECT_ROOT}/data"
        rm -rf "${PROJECT_ROOT}/logs"
        rm -f "${PROJECT_ROOT}/docker-compose.yml"
        log_info "Cleanup complete."
    else
        log_info "Cleanup cancelled."
    fi
}

show_logs() {
    local service="${1:-}"
    if [[ -z "$service" ]]; then
        docker-compose logs -f
    else
        docker-compose logs -f "$service"
    fi
}

main() {
    case "${1:-start}" in
        start)
            check_dependencies
            create_directories
            generate_docker_compose
            generate_alertmanager_config
            start_stack
            print_access_info
            ;;
        stop)
            stop_stack
            ;;
        restart)
            stop_stack
            sleep 2
            start_stack
            print_access_info
            ;;
        cleanup)
            cleanup_stack
            ;;
        logs)
            show_logs "${2:-}"
            ;;
        status)
            docker-compose ps
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|cleanup|logs [service]|status}"
            exit 1
            ;;
    esac
}

main "$@"
