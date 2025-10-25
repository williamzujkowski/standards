#!/usr/bin/env python3
"""
Condense Advanced Kubernetes skill by replacing Level 2 sections with concise versions.
"""

CONDENSED_SECTIONS = """### 2.1 Custom Resource Definitions (CRDs)

CRDs extend Kubernetes API with custom object types validated by OpenAPI v3 schemas.

**Key Components:**
- **Spec** - Desired state (user input)
- **Status** - Observed state (controller output, separate subresource)
- **Validation** - Markers like `+kubebuilder:validation:Minimum=1`
- **Versions** - Support multiple API versions with conversion webhooks

**Essential Kubebuilder Markers:**
```go
// +kubebuilder:validation:Minimum=1
// +kubebuilder:validation:Maximum=10
Size int32 `json:"size"`

// +kubebuilder:validation:Pattern=`^[a-z0-9.-]+/[a-z0-9.-]+:[a-z0-9.-]+$`
Image string `json:"image"`

// +optional
Port int32 `json:"port,omitempty"`
```

**Printcolumns for `kubectl get`:**
```go
// +kubebuilder:printcolumn:name="Ready",type=integer,JSONPath=`.status.readyReplicas`
// +kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`
```

**Subresources:**
- `+kubebuilder:subresource:status` - Separate status endpoint
- `+kubebuilder:subresource:scale` - Enable `kubectl scale`

**Generate CRDs:** `make manifests` → outputs to `config/crd/bases/`

See [REFERENCE.md](./REFERENCE.md) for complete CRD definition, versioning, and conversion webhooks.

---

### 2.2 Operators and Controllers

**Reconciliation Loop:**
1. **Watch** - Controller watches for resource changes (via informers/caches)
2. **Compare** - Reconcile compares desired vs actual state
3. **Act** - Create/update/delete Kubernetes resources to match desired state
4. **Update Status** - Set status conditions (`Ready`, `Progressing`, `Degraded`)
5. **Requeue** - Schedule next reconciliation (event-driven or periodic)

**Controller Pattern:**
```go
func (r *Reconciler) Reconcile(ctx, req) (ctrl.Result, error) {
    // 1. Fetch custom resource
    obj := &MyResource{}
    if err := r.Get(ctx, req.NamespacedName, obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 2. Handle deletion (finalizers)
    if !obj.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, obj)
    }

    // 3. Reconcile external state
    if err := r.reconcileDeployment(ctx, obj); err != nil {
        return ctrl.Result{RequeueAfter: 30*time.Second}, err
    }

    // 4. Update status
    obj.Status.Ready = true
    return ctrl.Result{}, r.Status().Update(ctx, obj)
}
```

**Key Functions:**
- `controllerutil.CreateOrUpdate()` - Idempotent create/update
- `controllerutil.SetControllerReference()` - Automatic garbage collection
- `controllerutil.AddFinalizer()` - Cleanup before deletion

**Error Handling:**
- **Transient errors** - Requeue with delay: `ctrl.Result{RequeueAfter: 30s}`
- **Permanent errors** - Set degraded condition, don't requeue
- **Unknown errors** - Return error for exponential backoff

See [REFERENCE.md](./REFERENCE.md) for complete controller implementation with finalizers, owner references, and error handling.

---

### 2.3 Admission Webhooks

Webhooks intercept API requests before persistence for validation/mutation.

**Types:**
- **Validating** - Accept/reject requests (JWT validation, cross-field checks)
- **Mutating** - Modify requests (inject sidecars, set defaults)

**Implementation:**
```go
// Validating webhook
func (r *MyApp) ValidateCreate() (admission.Warnings, error) {
    if r.Spec.Size < 1 || r.Spec.Size > 100 {
        return nil, fmt.Errorf("size must be 1-100")
    }
    return nil, nil
}

// Mutating webhook (Defaulter)
func (r *MyApp) Default() {
    if r.Spec.Port == 0 {
        r.Spec.Port = 8080
    }
}
```

**Setup:**
1. Implement `webhook.Validator` or `webhook.Defaulter` interface
2. Add kubebuilder marker: `// +kubebuilder:webhook:path=/validate-...,mutating=false,...`
3. `make manifests` generates webhook config
4. Deploy with cert-manager for TLS certificates

**Requirements:**
- TLS certificates (use cert-manager)
- Service routing webhook traffic to operator
- `failurePolicy: fail` (default) - reject on webhook errors

See [REFERENCE.md](./REFERENCE.md) for complete webhook examples, cert-manager setup, and validation patterns.

---

### 2.4 Leader Election & High Availability

Leader election ensures only one controller instance reconciles at a time (prevents race conditions).

**Configuration:**
```go
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
    LeaderElection:          true,
    LeaderElectionID:        "myapp-controller.example.com",
    LeaderElectionNamespace: "myapp-system",
})
```

**How It Works:**
- Uses Kubernetes `Lease` resource for coordination
- One replica acquires lease, becomes leader
- Other replicas standby, ready to take over on leader failure
- Leader renews lease every 10s (default)

**Deployment:**
```yaml
spec:
  replicas: 3  # High availability
  containers:
  - args:
    - --leader-elect
```

See [REFERENCE.md](./REFERENCE.md) for RBAC requirements and lease configuration tuning.

---

### 2.5 Testing Operators

**Unit Testing with envtest:**
- Runs local API server (no kubelet, no containers)
- Fast tests (milliseconds per test)
- Full CRD validation

**Setup:**
```go
testEnv = &envtest.Environment{
    CRDDirectoryPaths: []string{filepath.Join("..", "config", "crd", "bases")},
}
cfg, _ := testEnv.Start()
k8sClient, _ = client.New(cfg, client.Options{Scheme: scheme.Scheme})
```

**Test Pattern:**
```go
It("Should create Deployment", func() {
    myApp := &MyApp{...}
    Expect(k8sClient.Create(ctx, myApp)).Should(Succeed())

    deployment := &Deployment{}
    Eventually(func() error {
        return k8sClient.Get(ctx, namespacedName, deployment)
    }, timeout, interval).Should(Succeed())

    Expect(*deployment.Spec.Replicas).To(Equal(int32(3)))
})
```

**Integration Testing with kind:**
```bash
kind create cluster
make docker-build docker-push deploy IMG=operator:test
kubectl wait --for=condition=available deployment/operator
kubectl apply -f test-cr.yaml
```

See [REFERENCE.md](./REFERENCE.md) for complete test suites, ginkgo patterns, and E2E test scripts.

---

### 2.6 Best Practices & Anti-Patterns

**✅ Best Practices:**
- **Idempotent reconciliation** - Same result on multiple calls
- **Use `CreateOrUpdate`** - Simplifies create/update logic
- **Set owner references** - Automatic garbage collection
- **Finalizers for cleanup** - External resources (cloud APIs, databases)
- **Status conditions** - `Ready`, `Progressing`, `Degraded` with detailed messages
- **Structured logging** - JSON format with consistent key-value pairs

**❌ Anti-Patterns:**
- **Blocking operations** - Don't make sync calls that block reconcile
- **Infinite loops** - Updating spec in reconcile triggers another reconcile
- **Hardcoded values** - Use env vars/ConfigMaps
- **Missing watches** - Ensure RBAC allows watching dependent resources
- **No health checks** - Implement `/healthz` and `/readyz` endpoints

**Requeue Strategies:**
```go
// Immediate requeue (rate-limited)
return ctrl.Result{Requeue: true}, nil

// Requeue after delay
return ctrl.Result{RequeueAfter: 30 * time.Second}, nil

// No requeue (wait for watch event)
return ctrl.Result{}, nil

// Error (exponential backoff)
return ctrl.Result{}, fmt.Errorf("transient error")
```

See [REFERENCE.md](./REFERENCE.md) for advanced patterns, multi-cluster operators, and OLM integration.

---
"""

def main():
    skill_path = "/home/william/git/standards/skills/cloud-native/advanced-kubernetes/SKILL.md"

    with open(skill_path, 'r') as f:
        lines = f.readlines()

    # Find section boundaries
    level2_start = None
    level3_start = None

    for i, line in enumerate(lines):
        if line.startswith("## Level 2: Implementation Guide"):
            level2_start = i
        elif line.startswith("## Level 3: Deep Dive Resources"):
            level3_start = i
            break

    if level2_start is None or level3_start is None:
        print("Could not find section boundaries")
        return 1

    # Keep everything before Level 2, insert condensed content, keep Level 3 onwards
    new_content = (
        ''.join(lines[:level2_start]) +
        "## Level 2: Implementation Guide\n\n" +
        "> **📚 Complete Examples**: See [REFERENCE.md](./REFERENCE.md) for full controller implementations, webhook code, test suites, and production-ready patterns.\n\n" +
        CONDENSED_SECTIONS +
        '\n'.join(lines[level3_start:])
    )

    with open(skill_path, 'w') as f:
        f.write(new_content)

    print(f"✓ Condensed Level 2 from {level3_start - level2_start} to ~80 lines")
    print(f"✓ All detailed implementations moved to REFERENCE.md")

    return 0

if __name__ == "__main__":
    exit(main())
