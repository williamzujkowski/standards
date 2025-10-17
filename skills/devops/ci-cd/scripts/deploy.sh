#!/bin/bash
set -e

ENVIRONMENT=${1:-staging}
VERSION=${2:-latest}
NAMESPACE="myapp-${ENVIRONMENT}"

echo "Deploying version $VERSION to $ENVIRONMENT"

# Deploy to inactive environment (green)
kubectl set image deployment/myapp-green \
  myapp=registry.example.com/myapp:$VERSION \
  --namespace=$NAMESPACE

# Wait for green to be ready
kubectl rollout status deployment/myapp-green -n $NAMESPACE --timeout=5m

# Run smoke tests against green
echo "Running smoke tests..."
GREEN_URL=$(kubectl get service myapp-green -n $NAMESPACE -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')
curl -f "http://${GREEN_URL}/health" || exit 1

# Switch traffic to green
echo "Switching traffic to green..."
kubectl patch service myapp -n $NAMESPACE \
  -p '{"spec":{"selector":{"version":"green"}}}'

echo "Deployment successful! Old blue environment remains for rollback."
