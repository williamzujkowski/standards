#!/bin/bash
# Setup mTLS for Zero-Trust Architecture
# This script automates certificate generation and service mesh configuration

set -euo pipefail

# Configuration
CA_DIR="${CA_DIR:-/tmp/mtls-ca}"
CERT_VALIDITY_DAYS="${CERT_VALIDITY_DAYS:-365}"
NAMESPACE="${NAMESPACE:-production}"
SERVICE_MESH="${SERVICE_MESH:-istio}"  # istio or linkerd

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."

    local missing_tools=()

    for tool in openssl kubectl; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done

    if [ ${#missing_tools[@]} -ne 0 ]; then
        log_error "Missing required tools: ${missing_tools[*]}"
        exit 1
    fi

    if [ "$SERVICE_MESH" = "istio" ]; then
        if ! command -v istioctl &> /dev/null; then
            log_warn "istioctl not found. Install from: https://istio.io/latest/docs/setup/install/"
        fi
    elif [ "$SERVICE_MESH" = "linkerd" ]; then
        if ! command -v linkerd &> /dev/null; then
            log_warn "linkerd CLI not found. Install from: https://linkerd.io/2/getting-started/"
        fi
    fi

    log_info "Prerequisites check completed"
}

create_ca() {
    log_info "Creating Certificate Authority..."

    mkdir -p "$CA_DIR"
    cd "$CA_DIR"

    # Generate root CA private key
    openssl genrsa -out root-ca-key.pem 4096

    # Generate root CA certificate
    openssl req -new -x509 -days "$CERT_VALIDITY_DAYS" -key root-ca-key.pem \
        -out root-ca.pem \
        -subj "/CN=Zero Trust Root CA/O=Example Org/C=US"

    # Generate intermediate CA private key
    openssl genrsa -out intermediate-ca-key.pem 4096

    # Generate intermediate CA CSR
    openssl req -new -key intermediate-ca-key.pem \
        -out intermediate-ca.csr \
        -subj "/CN=Zero Trust Intermediate CA/O=Example Org/C=US"

    # Sign intermediate CA with root CA
    openssl x509 -req -days "$CERT_VALIDITY_DAYS" \
        -in intermediate-ca.csr \
        -CA root-ca.pem -CAkey root-ca-key.pem -CAcreateserial \
        -out intermediate-ca.pem \
        -extensions v3_ca \
        -extfile <(cat <<EOF
[v3_ca]
basicConstraints = CA:TRUE
keyUsage = critical,keyCertSign,cRLSign
subjectKeyIdentifier = hash
authorityKeyIdentifier = keyid:always,issuer
EOF
)

    # Create certificate chain
    cat intermediate-ca.pem root-ca.pem > cert-chain.pem

    log_info "Certificate Authority created in $CA_DIR"
}

generate_service_cert() {
    local service_name="$1"
    local san="${2:-$service_name.$NAMESPACE.svc.cluster.local}"

    log_info "Generating certificate for $service_name..."

    cd "$CA_DIR"

    # Generate service private key
    openssl genrsa -out "${service_name}-key.pem" 2048

    # Generate service CSR
    openssl req -new -key "${service_name}-key.pem" \
        -out "${service_name}.csr" \
        -subj "/CN=${san}/O=Example Org"

    # Create SAN extension file
    cat > "${service_name}-san.ext" <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = critical,digitalSignature,keyEncipherment
extendedKeyUsage = serverAuth,clientAuth
subjectAltName = @alt_names

[alt_names]
DNS.1 = ${san}
DNS.2 = ${service_name}
DNS.3 = ${service_name}.${NAMESPACE}
DNS.4 = ${service_name}.${NAMESPACE}.svc
DNS.5 = localhost
IP.1 = 127.0.0.1
EOF

    # Sign service certificate
    openssl x509 -req -days "$CERT_VALIDITY_DAYS" \
        -in "${service_name}.csr" \
        -CA intermediate-ca.pem -CAkey intermediate-ca-key.pem -CAcreateserial \
        -out "${service_name}-cert.pem" \
        -extfile "${service_name}-san.ext"

    # Verify certificate
    openssl verify -CAfile cert-chain.pem "${service_name}-cert.pem"

    log_info "Certificate generated for $service_name"
}

create_k8s_secret() {
    local service_name="$1"
    local secret_name="${service_name}-tls"

    log_info "Creating Kubernetes secret for $service_name..."

    cd "$CA_DIR"

    kubectl create secret generic "$secret_name" \
        --from-file=tls.crt="${service_name}-cert.pem" \
        --from-file=tls.key="${service_name}-key.pem" \
        --from-file=ca.crt=cert-chain.pem \
        -n "$NAMESPACE" \
        --dry-run=client -o yaml | kubectl apply -f -

    log_info "Secret $secret_name created in namespace $NAMESPACE"
}

setup_istio_mtls() {
    log_info "Setting up Istio mTLS..."

    # Create istio-system namespace if it doesn't exist
    kubectl create namespace istio-system --dry-run=client -o yaml | kubectl apply -f -

    # Create CA secret for Istio
    cd "$CA_DIR"
    kubectl create secret generic cacerts \
        --from-file=ca-cert.pem=intermediate-ca.pem \
        --from-file=ca-key.pem=intermediate-ca-key.pem \
        --from-file=root-cert.pem=root-ca.pem \
        --from-file=cert-chain.pem=cert-chain.pem \
        -n istio-system \
        --dry-run=client -o yaml | kubectl apply -f -

    # Apply global strict mTLS policy
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

    log_info "Istio mTLS configured with strict mode"
}

setup_linkerd_mtls() {
    log_info "Setting up Linkerd mTLS..."

    # Linkerd automatically provisions mTLS
    # Install trust anchor
    cd "$CA_DIR"

    kubectl create namespace linkerd --dry-run=client -o yaml | kubectl apply -f -

    kubectl create secret generic linkerd-trust-anchor \
        --from-file=ca.crt=root-ca.pem \
        -n linkerd \
        --dry-run=client -o yaml | kubectl apply -f -

    log_info "Linkerd trust anchor configured"
}

verify_mtls() {
    log_info "Verifying mTLS configuration..."

    if [ "$SERVICE_MESH" = "istio" ]; then
        log_info "Checking Istio mTLS status..."
        if command -v istioctl &> /dev/null; then
            istioctl proxy-status
        else
            log_warn "istioctl not available, skipping status check"
        fi
    elif [ "$SERVICE_MESH" = "linkerd" ]; then
        log_info "Checking Linkerd mTLS status..."
        if command -v linkerd &> /dev/null; then
            linkerd check --proxy
        else
            log_warn "linkerd CLI not available, skipping check"
        fi
    fi
}

rotate_certificates() {
    log_info "Rotating certificates..."

    local services=("$@")

    for service in "${services[@]}"; do
        log_info "Rotating certificate for $service..."
        generate_service_cert "$service"
        create_k8s_secret "$service"

        # Trigger pod restart to load new certificate
        kubectl rollout restart deployment "$service" -n "$NAMESPACE" || true
    done

    log_info "Certificate rotation completed"
}

display_cert_info() {
    local service_name="$1"

    cd "$CA_DIR"

    log_info "Certificate information for $service_name:"
    openssl x509 -in "${service_name}-cert.pem" -text -noout | grep -E "(Subject:|Issuer:|Not Before|Not After|DNS:)"
}

main() {
    log_info "Starting mTLS setup for Zero-Trust Architecture"

    case "${1:-setup}" in
        setup)
            check_prerequisites
            create_ca

            if [ "$SERVICE_MESH" = "istio" ]; then
                setup_istio_mtls
            elif [ "$SERVICE_MESH" = "linkerd" ]; then
                setup_linkerd_mtls
            else
                log_error "Unknown service mesh: $SERVICE_MESH"
                exit 1
            fi

            log_info "Basic mTLS setup completed"
            log_info "To generate service certificates, run:"
            log_info "  $0 generate-cert <service-name>"
            ;;

        generate-cert)
            if [ -z "${2:-}" ]; then
                log_error "Service name required"
                log_info "Usage: $0 generate-cert <service-name> [san]"
                exit 1
            fi

            generate_service_cert "$2" "${3:-}"
            create_k8s_secret "$2"
            display_cert_info "$2"
            ;;

        rotate)
            if [ -z "${2:-}" ]; then
                log_error "At least one service name required"
                log_info "Usage: $0 rotate <service1> [service2] ..."
                exit 1
            fi

            shift
            rotate_certificates "$@"
            ;;

        verify)
            verify_mtls
            ;;

        info)
            if [ -z "${2:-}" ]; then
                log_error "Service name required"
                log_info "Usage: $0 info <service-name>"
                exit 1
            fi

            display_cert_info "$2"
            ;;

        *)
            echo "Usage: $0 {setup|generate-cert|rotate|verify|info}"
            echo ""
            echo "Commands:"
            echo "  setup                         - Create CA and configure service mesh"
            echo "  generate-cert <service> [san] - Generate certificate for a service"
            echo "  rotate <service1> ...         - Rotate certificates for services"
            echo "  verify                        - Verify mTLS configuration"
            echo "  info <service>                - Display certificate information"
            echo ""
            echo "Environment variables:"
            echo "  CA_DIR               - Certificate directory (default: /tmp/mtls-ca)"
            echo "  CERT_VALIDITY_DAYS   - Certificate validity (default: 365)"
            echo "  NAMESPACE            - Kubernetes namespace (default: production)"
            echo "  SERVICE_MESH         - Service mesh type (default: istio)"
            exit 1
            ;;
    esac
}

main "$@"
