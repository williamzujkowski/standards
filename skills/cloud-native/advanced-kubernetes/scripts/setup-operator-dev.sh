#!/bin/bash
# Operator Development Environment Setup Script

set -e

OPERATOR_NAME="${1:-my-operator}"
OPERATOR_DOMAIN="${2:-example.com}"

echo "Setting up operator development environment..."
echo "Operator: ${OPERATOR_NAME}, Domain: ${OPERATOR_DOMAIN}"

# Install kubebuilder
if ! command -v kubebuilder &> /dev/null; then
    echo "Installing kubebuilder..."
    curl -L -o kubebuilder https://go.kubebuilder.io/dl/latest/$(go env GOOS)/$(go env GOARCH)
    chmod +x kubebuilder && sudo mv kubebuilder /usr/local/bin/
fi

# Install kind
if ! command -v kind &> /dev/null; then
    echo "Installing kind..."
    go install sigs.k8s.io/kind@latest
fi

# Create kind cluster
kind create cluster --name operator-dev 2>/dev/null || echo "Cluster already exists"

# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.2/cert-manager.yaml

echo "Environment setup complete!"
