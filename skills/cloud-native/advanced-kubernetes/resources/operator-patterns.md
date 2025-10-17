# Operator Patterns and Anti-Patterns

## Design Patterns

### 1. State Machine Pattern
Model complex workflows as finite state machines with explicit state transitions.

**When to use:**
- Multi-step provisioning workflows (e.g., database initialization)
- Resources with distinct lifecycle phases
- Operations requiring ordered steps

**Example:**
```go
type DatabasePhase string

const (
    PhaseInitializing DatabasePhase = "Initializing"
    PhaseProvisioning DatabasePhase = "Provisioning"
    PhaseConfiguring  DatabasePhase = "Configuring"
    PhaseReady        DatabasePhase = "Ready"
    PhaseFailed       DatabasePhase = "Failed"
)

func (r *DatabaseReconciler) reconcile(ctx context.Context, db *Database) error {
    switch db.Status.Phase {
    case PhaseInitializing:
        return r.initialize(ctx, db)
    case PhaseProvisioning:
        return r.provision(ctx, db)
    case PhaseConfiguring:
        return r.configure(ctx, db)
    case PhaseReady:
        return r.maintain(ctx, db)
    default:
        return r.handleUnknownPhase(ctx, db)
    }
}
```

### 2. External Resource Controller Pattern
Manage resources outside Kubernetes (cloud resources, databases, APIs).

**When to use:**
- Cloud resource management (S3 buckets, RDS instances)
- Integration with external SaaS platforms
- Managing on-premise infrastructure

**Best practices:**
- Use finalizers to prevent orphaned external resources
- Implement robust cleanup logic with timeouts
- Store external resource IDs in status
- Handle API rate limits and retries

### 3. Sidecar Injection Pattern
Automatically inject sidecar containers into pods.

**When to use:**
- Service mesh proxies (Istio, Linkerd)
- Logging/monitoring agents
- Security scanning containers

**Implementation:**
- Use mutating webhooks to modify pod specs
- Add containers, volumes, and init containers
- Respect existing pod configurations

### 4. Configuration Aggregation Pattern
Aggregate multiple configuration sources into a single resource.

**When to use:**
- Managing complex application configurations
- Merging environment-specific settings
- Inheriting from base configurations

**Example:**
```go
type AppConfig struct {
    Base      string `json:"base,omitempty"`      // Base config reference
    Overrides map[string]string `json:"overrides"` // Environment overrides
}

func (r *AppReconciler) aggregateConfig(ctx context.Context, app *App) (*Config, error) {
    // Load base config
    baseConfig := loadBaseConfig(app.Spec.Config.Base)
    
    // Apply overrides
    finalConfig := baseConfig.DeepCopy()
    for key, value := range app.Spec.Config.Overrides {
        finalConfig.Set(key, value)
    }
    
    return finalConfig, nil
}
```

### 5. Progressive Rollout Pattern
Implement canary or blue-green deployments for custom resources.

**When to use:**
- High-risk configuration changes
- Production database migrations
- Critical infrastructure updates

**Implementation:**
- Maintain multiple versions of resources
- Gradually shift traffic/load
- Implement automatic rollback on failures

---

## Anti-Patterns

### ❌ 1. Blocking Reconciliation
**Problem:** Long-running operations block the reconciliation loop.

**Example (BAD):**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // BAD: Blocks for minutes
    result := runLongMigration(ctx) // 10 minutes
    return ctrl.Result{}, nil
}
```

**Solution:**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    if !r.isMigrationComplete(ctx, obj) {
        // Start background job if not running
        if !r.isMigrationRunning(ctx, obj) {
            go r.runMigrationAsync(ctx, obj)
        }
        return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
    }
    return ctrl.Result{}, nil
}
```

### ❌ 2. Infinite Reconciliation Loops
**Problem:** Controller updates resource spec, triggering another reconciliation.

**Example (BAD):**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    obj.Spec.LastReconciled = time.Now() // BAD: Triggers another reconcile
    r.Update(ctx, obj)
    return ctrl.Result{}, nil
}
```

**Solution:**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    obj.Status.LastReconciled = time.Now() // GOOD: Update status only
    r.Status().Update(ctx, obj)
    return ctrl.Result{}, nil
}
```

### ❌ 3. Missing Finalizers
**Problem:** Deleting custom resource orphans external resources.

**Example (BAD):**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    createS3Bucket(obj.Name) // BAD: No cleanup on deletion
    return ctrl.Result{}, nil
}
```

**Solution:**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    if !obj.DeletionTimestamp.IsZero() {
        deleteS3Bucket(obj.Name)
        controllerutil.RemoveFinalizer(obj, finalizerName)
        r.Update(ctx, obj)
        return ctrl.Result{}, nil
    }
    
    controllerutil.AddFinalizer(obj, finalizerName)
    r.Update(ctx, obj)
    
    createS3Bucket(obj.Name)
    return ctrl.Result{}, nil
}
```

### ❌ 4. Hardcoded Configurations
**Problem:** Operator behavior hardcoded instead of configurable.

**Example (BAD):**
```go
func (r *Reconciler) reconcileDeployment(ctx context.Context, obj *MyApp) error {
    deployment.Namespace = "default" // BAD: Hardcoded
    deployment.Image = "myapp:1.0" // BAD: Hardcoded
}
```

**Solution:**
```go
func (r *Reconciler) reconcileDeployment(ctx context.Context, obj *MyApp) error {
    deployment.Namespace = obj.Namespace // GOOD: From resource
    deployment.Image = obj.Spec.Image // GOOD: Configurable
}
```

### ❌ 5. No Owner References
**Problem:** Managed resources not garbage collected when parent is deleted.

**Example (BAD):**
```go
func (r *Reconciler) createDeployment(ctx context.Context, obj *MyApp) error {
    deployment := &appsv1.Deployment{...}
    r.Create(ctx, deployment) // BAD: No owner reference
}
```

**Solution:**
```go
func (r *Reconciler) createDeployment(ctx context.Context, obj *MyApp) error {
    deployment := &appsv1.Deployment{...}
    controllerutil.SetControllerReference(obj, deployment, r.Scheme) // GOOD
    r.Create(ctx, deployment)
}
```

### ❌ 6. Ignoring Error Types
**Problem:** Treating all errors the same, causing unnecessary retries.

**Example (BAD):**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    if err := r.reconcile(ctx, obj); err != nil {
        return ctrl.Result{}, err // BAD: Always retries
    }
}
```

**Solution:**
```go
func (r *Reconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    if err := r.reconcile(ctx, obj); err != nil {
        if errors.IsInvalid(err) {
            // Permanent error - don't retry
            r.setErrorStatus(ctx, obj, err)
            return ctrl.Result{}, nil
        }
        if errors.IsServiceUnavailable(err) {
            // Transient error - retry with backoff
            return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
        }
        return ctrl.Result{}, err // Unknown error - exponential backoff
    }
}
```

### ❌ 7. Missing Health Checks
**Problem:** Kubernetes can't detect unhealthy controller.

**Example (BAD):**
```go
func main() {
    mgr, _ := ctrl.NewManager(...)
    mgr.Start(ctrl.SetupSignalHandler()) // BAD: No health checks
}
```

**Solution:**
```go
func main() {
    mgr, _ := ctrl.NewManager(...)
    mgr.AddHealthzCheck("healthz", healthz.Ping) // GOOD
    mgr.AddReadyzCheck("readyz", healthz.Ping) // GOOD
    mgr.Start(ctrl.SetupSignalHandler())
}
```

### ❌ 8. No RBAC Markers
**Problem:** Manual RBAC management is error-prone.

**Example (BAD):**
```go
// controllers/myapp_controller.go
// No RBAC markers - must manually maintain RBAC YAML
```

**Solution:**
```go
// controllers/myapp_controller.go
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
func (r *MyAppReconciler) Reconcile(...) {...}
```

---

## Performance Best Practices

### 1. Use Caching Effectively
```go
// GOOD: Use cached client for reads
obj := &MyApp{}
r.Get(ctx, req.NamespacedName, obj) // Uses cache

// GOOD: Use uncached client for writes
r.Update(ctx, obj) // Writes to API server
```

### 2. Batch Updates
```go
// BAD: Multiple status updates
r.Status().Update(ctx, obj) // Update 1
r.Status().Update(ctx, obj) // Update 2

// GOOD: Single status update
obj.Status.Field1 = value1
obj.Status.Field2 = value2
r.Status().Update(ctx, obj) // Single update
```

### 3. Use Predicates to Filter Events
```go
func (r *MyAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&MyApp{}).
        WithEventFilter(predicate.GenerationChangedPredicate{}). // Filter spec changes only
        Complete(r)
}
```

### 4. Implement Rate Limiting
```go
func (r *MyAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&MyApp{}).
        WithOptions(controller.Options{
            MaxConcurrentReconciles: 3,
            RateLimiter: workqueue.NewItemExponentialFailureRateLimiter(
                time.Second,
                5*time.Minute,
            ),
        }).
        Complete(r)
}
```

---

## Testing Patterns

### 1. Use Table-Driven Tests
```go
func TestReconcile(t *testing.T) {
    tests := []struct {
        name    string
        input   *MyApp
        want    ctrl.Result
        wantErr bool
    }{
        {name: "create", input: &MyApp{...}, want: ctrl.Result{}, wantErr: false},
        {name: "update", input: &MyApp{...}, want: ctrl.Result{}, wantErr: false},
        {name: "delete", input: &MyApp{...}, want: ctrl.Result{}, wantErr: false},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := reconciler.Reconcile(ctx, req)
            if (err != nil) != tt.wantErr {
                t.Errorf("wantErr %v, got %v", tt.wantErr, err)
            }
            if got != tt.want {
                t.Errorf("want %v, got %v", tt.want, got)
            }
        })
    }
}
```

### 2. Mock External Dependencies
```go
type MockCloudProvider struct {
    CreateBucketFunc func(name string) error
}

func TestReconcileWithMock(t *testing.T) {
    mock := &MockCloudProvider{
        CreateBucketFunc: func(name string) error {
            return nil // Controlled response
        },
    }
    
    reconciler := &MyAppReconciler{Cloud: mock}
    // Test reconciliation
}
```

---

## Summary

**DO:**
- ✅ Use finalizers for cleanup
- ✅ Set owner references
- ✅ Update status subresource only
- ✅ Implement health checks
- ✅ Handle errors appropriately
- ✅ Use RBAC markers
- ✅ Test thoroughly

**DON'T:**
- ❌ Block reconciliation
- ❌ Update spec in reconcile
- ❌ Hardcode configurations
- ❌ Ignore error types
- ❌ Skip finalizers
- ❌ Forget health checks
