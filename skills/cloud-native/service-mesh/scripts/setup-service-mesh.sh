#!/bin/bash
# Automated Istio Service Mesh Installation Script
# Usage: ./setup-service-mesh.sh [profile] [namespace]

set -e

# Configuration
PROFILE="${1:-default}"
NAMESPACE="${2:-default}"
ISTIO_VERSION="${ISTIO_VERSION:-1.20.0}"
INSTALL_ADDONS="${INSTALL_ADDONS:-true}"
ENABLE_MTLS="${ENABLE_MTLS:-true}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."

    # Check kubectl
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl not found. Please install kubectl."
        exit 1
    fi

    # Check cluster access
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot access Kubernetes cluster. Check your kubeconfig."
        exit 1
    fi

    # Check istioctl
    if ! command -v istioctl &> /dev/null; then
        log_warn "istioctl not found. Installing..."
        install_istioctl
    fi

    log_info "Prerequisites check passed."
}

# Install istioctl
install_istioctl() {
    log_info "Installing istioctl ${ISTIO_VERSION}..."

    curl -L https://istio.io/downloadIstio | ISTIO_VERSION=${ISTIO_VERSION} sh -

    cd "istio-${ISTIO_VERSION}"
    export PATH=$PWD/bin:$PATH
    cd ..

    log_info "istioctl installed successfully."
}

# Validate cluster resources
validate_cluster() {
    log_info "Validating cluster resources..."

    # Check node resources
    NODES=$(kubectl get nodes --no-headers | wc -l)
    if [ "$NODES" -lt 3 ]; then
        log_warn "Cluster has less than 3 nodes. High availability may be compromised."
    fi

    # Check available resources
    TOTAL_CPU=$(kubectl top nodes 2>/dev/null | awk 'NR>1 {sum+=$3} END {print sum}' || echo "0")
    if [ "$TOTAL_CPU" == "0" ]; then
        log_warn "Cannot determine cluster CPU resources. Ensure metrics-server is installed."
    fi

    log_info "Cluster validation completed."
}

# Install Istio
install_istio() {
    log_info "Installing Istio with profile: ${PROFILE}..."

    # Create istio-system namespace
    kubectl create namespace istio-system --dry-run=client -o yaml | kubectl apply -f -

    # Install Istio
    if [ "$PROFILE" == "production" ]; then
        istioctl install -y \
            --set profile=default \
            --set values.pilot.autoscaleEnabled=true \
            --set values.pilot.autoscaleMin=2 \
            --set values.pilot.autoscaleMax=5 \
            --set values.global.proxy.resources.requests.cpu=10m \
            --set values.global.proxy.resources.requests.memory=40Mi \
            --set values.global.proxy.resources.limits.cpu=2000m \
            --set values.global.proxy.resources.limits.memory=1024Mi
    else
        istioctl install --set profile="${PROFILE}" -y
    fi

    # Verify installation
    kubectl get pods -n istio-system

    log_info "Istio installed successfully."
}

# Enable sidecar injection
enable_sidecar_injection() {
    log_info "Enabling sidecar injection for namespace: ${NAMESPACE}..."

    kubectl create namespace "${NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -
    kubectl label namespace "${NAMESPACE}" istio-injection=enabled --overwrite

    log_info "Sidecar injection enabled for ${NAMESPACE}."
}

# Install observability addons
install_addons() {
    if [ "$INSTALL_ADDONS" != "true" ]; then
        log_info "Skipping addon installation."
        return
    fi

    log_info "Installing observability addons..."

    ISTIO_DIR="istio-${ISTIO_VERSION}"

    # Prometheus
    kubectl apply -f "${ISTIO_DIR}/samples/addons/prometheus.yaml" || true

    # Grafana
    kubectl apply -f "${ISTIO_DIR}/samples/addons/grafana.yaml" || true

    # Kiali
    kubectl apply -f "${ISTIO_DIR}/samples/addons/kiali.yaml" || true

    # Jaeger
    kubectl apply -f "${ISTIO_DIR}/samples/addons/jaeger.yaml" || true

    # Wait for addons to be ready
    log_info "Waiting for addons to be ready..."
    kubectl wait --for=condition=available --timeout=300s \
        deployment/prometheus -n istio-system 2>/dev/null || true
    kubectl wait --for=condition=available --timeout=300s \
        deployment/grafana -n istio-system 2>/dev/null || true
    kubectl wait --for=condition=available --timeout=300s \
        deployment/kiali -n istio-system 2>/dev/null || true
    kubectl wait --for=condition=available --timeout=300s \
        deployment/jaeger -n istio-system 2>/dev/null || true

    log_info "Addons installed successfully."
}

# Enable mTLS
enable_mtls() {
    if [ "$ENABLE_MTLS" != "true" ]; then
        log_info "Skipping mTLS configuration."
        return
    fi

    log_info "Enabling strict mTLS..."

    kubectl apply -f - <<EOF
apiVersion: security.istio.io/v1beta1
kind: PeerAuthentication
metadata:
  name: default
  namespace: istio-system
spec:
  mtls:
    mode: STRICT
EOF

    log_info "Strict mTLS enabled."
}

# Verify installation
verify_installation() {
    log_info "Verifying Istio installation..."

    # Check Istio components
    if ! kubectl get deployment -n istio-system istiod &> /dev/null; then
        log_error "Istiod deployment not found."
        exit 1
    fi

    # Run istioctl verify
    if istioctl verify-install &> /dev/null; then
        log_info "Istio installation verified successfully."
    else
        log_warn "Istio verification completed with warnings. Check the output."
    fi

    # Check proxy status
    log_info "Checking proxy status..."
    istioctl proxy-status || true
}

# Display access information
display_access_info() {
    log_info "=== Istio Dashboard Access ==="

    echo ""
    echo "To access dashboards, run these commands in separate terminals:"
    echo ""
    echo "  Kiali:      istioctl dashboard kiali"
    echo "  Prometheus: istioctl dashboard prometheus"
    echo "  Grafana:    istioctl dashboard grafana"
    echo "  Jaeger:     istioctl dashboard jaeger"
    echo ""

    log_info "=== Next Steps ==="
    echo ""
    echo "1. Deploy your application to namespace: ${NAMESPACE}"
    echo "2. Verify sidecar injection:"
    echo "   kubectl get pods -n ${NAMESPACE} -o jsonpath='{.items[*].spec.containers[*].name}'"
    echo ""
    echo "3. Create VirtualService and DestinationRule for traffic management"
    echo "4. Configure AuthorizationPolicy for security"
    echo ""
}

# Cleanup function
cleanup() {
    log_info "Cleaning up temporary files..."
    # Add cleanup logic if needed
}

# Main execution
main() {
    log_info "Starting Istio service mesh installation..."

    check_prerequisites
    validate_cluster
    install_istio
    enable_sidecar_injection
    install_addons
    enable_mtls
    verify_installation
    display_access_info
    cleanup

    log_info "Istio service mesh installation completed successfully!"
}

# Run main function
main

# Trap errors and cleanup
trap cleanup EXIT
