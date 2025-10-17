---
name: advanced-kubernetes
category: cloud-native
difficulty: advanced
estimated_time: 60 minutes
prerequisites:
  - kubernetes
tags:
  - operators
  - crd
  - kubebuilder
  - controllers
  - webhooks
---

# Advanced Kubernetes: Operators & CRDs

## Level 1: Quick Reference

### Core Concepts at a Glance

**Custom Resource Definitions (CRDs)** extend Kubernetes API with custom object types. **Operators** are controllers that manage these custom resources using domain-specific logic.

**CRD vs ConfigMap Comparison:**

| Aspect | CRD | ConfigMap |
|--------|-----|-----------|
| **API Integration** | Full Kubernetes API support (CRUD, watch, RBAC) | Simple key-value storage |
| **Validation** | OpenAPI v3 schema validation, admission webhooks | No built-in validation |
| **Versioning** | Multiple versions with conversion webhooks | Single version only |
| **Use Case** | Complex application state, declarative APIs | Configuration data, environment variables |
| **Controller Support** | Reconciliation loops, status tracking | Manual polling required |
| **Example** | Database instances, ML workflows, backup policies | App config files, feature flags |

### Operator Pattern Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Kubernetes API Server                 │
│  (stores desired state in etcd)                         │
└────────────┬────────────────────────────┬───────────────┘
             │                            │
             │ Watch                      │ Update Status
             ↓                            ↑
    ┌────────────────┐         ┌─────────────────────┐
    │   Controller   │────────→│  External Resources │
    │  (Reconcile)   │  Manage │  (DBs, APIs, etc.)  │
    └────────────────┘         └─────────────────────┘
         ↑
         │ Compare
         │
    ┌────┴─────┐
    │ Desired  │
    │ vs Actual│
    └──────────┘
```

**Reconciliation Loop:**

1. **Watch** - Controller watches for changes to custom resources
2. **Compare** - Reconcile function compares desired vs actual state
3. **Act** - Controller takes actions to align actual state with desired
4. **Update Status** - Controller updates resource status with current state
5. **Requeue** - Schedule next reconciliation (periodic or event-driven)

### Controller Reconciliation Logic

```go
// Simplified reconciliation pattern
func (r *MyReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    // 1. Fetch the custom resource
    obj := &myapi.MyResource{}
    if err := r.Get(ctx, req.NamespacedName, obj); err != nil {
        return ctrl.Result{}, client.IgnoreNotFound(err)
    }

    // 2. Handle deletion (finalizers)
    if !obj.DeletionTimestamp.IsZero() {
        return r.handleDeletion(ctx, obj)
    }

    // 3. Reconcile external state
    if err := r.reconcileExternal(ctx, obj); err != nil {
        return ctrl.Result{}, err
    }

    // 4. Update status
    obj.Status.Ready = true
    if err := r.Status().Update(ctx, obj); err != nil {
        return ctrl.Result{}, err
    }

    return ctrl.Result{}, nil // Success, no requeue
}
```

### Essential Checklist

**Prerequisites:**

- [ ] Kubernetes cluster (v1.25+) - local (kind, minikube) or remote
- [ ] kubectl configured with admin access
- [ ] Go 1.21+ installed
- [ ] Docker/Podman for building operator images

**Development Tools:**

- [ ] `kubebuilder` (v3.12+) - scaffolding and code generation
- [ ] `operator-sdk` (optional) - alternative framework
- [ ] `controller-gen` - generates CRDs, RBACs, webhooks
- [ ] `kustomize` - manages Kubernetes manifests

**Testing Tools:**

- [ ] `envtest` - runs API server locally for unit tests
- [ ] `kind` - Kubernetes in Docker for integration tests
- [ ] `ginkgo` - BDD testing framework (optional)

**Key Files in Operator Project:**

```
my-operator/
├── api/v1/           # CRD definitions (Go structs)
├── config/
│   ├── crd/          # Generated CRD YAML
│   ├── rbac/         # Generated RBAC YAML
│   ├── manager/      # Operator deployment
│   └── webhook/      # Webhook configurations
├── controllers/      # Reconciliation logic
├── main.go           # Entrypoint (manager setup)
└── Dockerfile        # Container image build
```

**Quick Commands:**

```bash
# Initialize operator project
kubebuilder init --domain example.com --repo github.com/myorg/my-operator

# Create CRD + controller
kubebuilder create api --group apps --version v1 --kind MyApp

# Generate manifests
make manifests

# Run locally (connects to current kubeconfig cluster)
make install run

# Run tests
make test

# Build and deploy
make docker-build docker-push deploy IMG=myregistry/my-operator:v1.0.0
```

**Common Pitfalls:**

- ❌ Forgetting to update CRD when changing API structs → run `make manifests`
- ❌ Infinite reconciliation loops → use `ctrl.Result{RequeueAfter: time.Minute}`
- ❌ Not handling deletion properly → implement finalizers
- ❌ Blocking operations in reconcile → use background workers for long tasks
- ❌ Not setting owner references → orphaned resources on deletion

**When to Use Operators:**

- ✅ Managing complex stateful applications (databases, message queues)
- ✅ Automating operational tasks (backups, upgrades, scaling)
- ✅ Integrating with external systems (cloud APIs, SaaS platforms)
- ✅ Enforcing organizational policies (cost controls, security standards)
- ❌ Simple deployments (use Helm or plain manifests)
- ❌ One-time configuration changes (use Jobs or manual kubectl)

---

## Level 2: Implementation Guide

### 2.1 Custom Resource Definitions (CRDs)

CRDs extend the Kubernetes API with custom object types. They consist of:

- **Schema** - OpenAPI v3 validation rules
- **Versions** - Support multiple API versions with conversion
- **Scope** - Namespaced or cluster-scoped resources
- **Subresources** - Status, scale, and custom subresources

#### Defining a CRD with Kubebuilder

**Step 1: Create API types** (`api/v1/myapp_types.go`)

```go
package v1

import (
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// MyAppSpec defines the desired state of MyApp
type MyAppSpec struct {
    // Size is the number of replicas
    // +kubebuilder:validation:Minimum=1
    // +kubebuilder:validation:Maximum=10
    Size int32 `json:"size"`

    // Image is the container image to run
    // +kubebuilder:validation:Pattern=`^[a-z0-9.-]+/[a-z0-9.-]+:[a-z0-9.-]+$`
    Image string `json:"image"`

    // Port is the application port
    // +kubebuilder:validation:Minimum=1024
    // +kubebuilder:validation:Maximum=65535
    // +optional
    Port int32 `json:"port,omitempty"`

    // Resources defines CPU/memory limits
    // +optional
    Resources *ResourceRequirements `json:"resources,omitempty"`
}

type ResourceRequirements struct {
    // CPULimit in millicores (e.g., "500m")
    // +kubebuilder:validation:Pattern=`^[0-9]+m$`
    CPULimit string `json:"cpuLimit,omitempty"`

    // MemoryLimit in megabytes (e.g., "512Mi")
    // +kubebuilder:validation:Pattern=`^[0-9]+Mi$`
    MemoryLimit string `json:"memoryLimit,omitempty"`
}

// MyAppStatus defines the observed state of MyApp
type MyAppStatus struct {
    // Conditions represent the latest available observations
    Conditions []metav1.Condition `json:"conditions,omitempty"`

    // ReadyReplicas is the number of ready pods
    ReadyReplicas int32 `json:"readyReplicas"`

    // Phase represents the current lifecycle phase
    // +kubebuilder:validation:Enum=Pending;Running;Failed;Succeeded
    Phase string `json:"phase,omitempty"`

    // LastUpdateTime is the last time the status was updated
    LastUpdateTime metav1.Time `json:"lastUpdateTime,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status
// +kubebuilder:subresource:scale:specpath=.spec.size,statuspath=.status.readyReplicas
// +kubebuilder:printcolumn:name="Size",type=integer,JSONPath=`.spec.size`
// +kubebuilder:printcolumn:name="Ready",type=integer,JSONPath=`.status.readyReplicas`
// +kubebuilder:printcolumn:name="Phase",type=string,JSONPath=`.status.phase`
// +kubebuilder:printcolumn:name="Age",type=date,JSONPath=`.metadata.creationTimestamp`
// +kubebuilder:resource:shortName=ma;myapps

// MyApp is the Schema for the myapps API
type MyApp struct {
    metav1.TypeMeta   `json:",inline"`
    metav1.ObjectMeta `json:"metadata,omitempty"`

    Spec   MyAppSpec   `json:"spec,omitempty"`
    Status MyAppStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// MyAppList contains a list of MyApp
type MyAppList struct {
    metav1.TypeMeta `json:",inline"`
    metav1.ListMeta `json:"metadata,omitempty"`
    Items           []MyApp `json:"items"`
}

func init() {
    SchemeBuilder.Register(&MyApp{}, &MyAppList{})
}
```

**Step 2: Generate CRD manifests**

```bash
make manifests  # Generates config/crd/bases/apps.example.com_myapps.yaml
```

**Key Kubebuilder Markers:**

| Marker | Purpose | Example |
|--------|---------|---------|
| `+kubebuilder:validation:Minimum` | Min value for numbers | `// +kubebuilder:validation:Minimum=0` |
| `+kubebuilder:validation:Maximum` | Max value for numbers | `// +kubebuilder:validation:Maximum=100` |
| `+kubebuilder:validation:Pattern` | Regex validation | `// +kubebuilder:validation:Pattern=^[a-z]+$` |
| `+kubebuilder:validation:Enum` | Allowed values | `// +kubebuilder:validation:Enum=A;B;C` |
| `+kubebuilder:validation:MinLength` | Min string length | `// +kubebuilder:validation:MinLength=3` |
| `+kubebuilder:validation:Required` | Field is required | `// +kubebuilder:validation:Required` |
| `+optional` | Field is optional | `// +optional` |
| `+kubebuilder:default` | Default value | `// +kubebuilder:default=8080` |
| `+kubebuilder:printcolumn` | kubectl column | `// +kubebuilder:printcolumn:name="Status",type=string` |
| `+kubebuilder:subresource:status` | Enable status subresource | Applied to type |
| `+kubebuilder:subresource:scale` | Enable scale subresource | Applied to type |

#### CRD Best Practices

**Versioning Strategy:**

```go
// api/v1alpha1/myapp_types.go - Initial version
type MyAppSpec struct {
    Size int32 `json:"size"`
}

// api/v1beta1/myapp_types.go - Beta version with new field
type MyAppSpec struct {
    Size     int32  `json:"size"`
    Strategy string `json:"strategy,omitempty"` // New field
}

// api/v1/myapp_types.go - Stable version
type MyAppSpec struct {
    Replicas int32  `json:"replicas"`           // Renamed from Size
    Strategy string `json:"strategy,omitempty"`
}
```

**Conversion Webhooks** (for version migrations):

```go
// api/v1/myapp_conversion.go
func (src *MyApp) ConvertTo(dstRaw conversion.Hub) error {
    dst := dstRaw.(*v1.MyApp)
    dst.ObjectMeta = src.ObjectMeta
    dst.Spec.Replicas = src.Spec.Size // Convert field name
    dst.Spec.Strategy = src.Spec.Strategy
    return nil
}

func (dst *MyApp) ConvertFrom(srcRaw conversion.Hub) error {
    src := srcRaw.(*v1.MyApp)
    dst.ObjectMeta = src.ObjectMeta
    dst.Spec.Size = src.Spec.Replicas // Convert field name
    dst.Spec.Strategy = src.Spec.Strategy
    return nil
}
```

---

### 2.2 Kubernetes Operators and Controllers

Operators automate operational tasks by implementing the reconciliation pattern. Controllers watch resources and ensure actual state matches desired state.

#### Controller Structure

**Main Components:**

1. **Manager** - Coordinates controllers, webhooks, and caches
2. **Reconciler** - Implements reconciliation logic
3. **Client** - Reads/writes Kubernetes resources
4. **Cache** - Local resource cache for efficient reads

**Initialization** (`main.go`):

```go
package main

import (
    "flag"
    "os"

    "k8s.io/apimachinery/pkg/runtime"
    utilruntime "k8s.io/apimachinery/pkg/util/runtime"
    clientgoscheme "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/healthz"
    "sigs.k8s.io/controller-runtime/pkg/log/zap"

    appsv1 "github.com/myorg/my-operator/api/v1"
    "github.com/myorg/my-operator/controllers"
)

var (
    scheme   = runtime.NewScheme()
    setupLog = ctrl.Log.WithName("setup")
)

func init() {
    utilruntime.Must(clientgoscheme.AddToScheme(scheme))
    utilruntime.Must(appsv1.AddToScheme(scheme))
}

func main() {
    var metricsAddr string
    var probeAddr string
    var enableLeaderElection bool

    flag.StringVar(&metricsAddr, "metrics-bind-address", ":8080", "Metrics endpoint")
    flag.StringVar(&probeAddr, "health-probe-bind-address", ":8081", "Health probe endpoint")
    flag.BoolVar(&enableLeaderElection, "leader-elect", false, "Enable leader election")

    opts := zap.Options{Development: true}
    opts.BindFlags(flag.CommandLine)
    flag.Parse()

    ctrl.SetLogger(zap.New(zap.UseFlagOptions(&opts)))

    mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
        Scheme:                 scheme,
        MetricsBindAddress:     metricsAddr,
        HealthProbeBindAddress: probeAddr,
        LeaderElection:         enableLeaderElection,
        LeaderElectionID:       "myapp.example.com",
    })
    if err != nil {
        setupLog.Error(err, "unable to start manager")
        os.Exit(1)
    }

    if err = (&controllers.MyAppReconciler{
        Client: mgr.GetClient(),
        Scheme: mgr.GetScheme(),
    }).SetupWithManager(mgr); err != nil {
        setupLog.Error(err, "unable to create controller", "controller", "MyApp")
        os.Exit(1)
    }

    if err := mgr.AddHealthzCheck("healthz", healthz.Ping); err != nil {
        setupLog.Error(err, "unable to set up health check")
        os.Exit(1)
    }
    if err := mgr.AddReadyzCheck("readyz", healthz.Ping); err != nil {
        setupLog.Error(err, "unable to set up ready check")
        os.Exit(1)
    }

    setupLog.Info("starting manager")
    if err := mgr.Start(ctrl.SetupSignalHandler()); err != nil {
        setupLog.Error(err, "problem running manager")
        os.Exit(1)
    }
}
```

#### Reconciliation Logic with Error Handling

**Full Reconciler Implementation** (`controllers/myapp_controller.go`):

```go
package controllers

import (
    "context"
    "fmt"
    "time"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    "k8s.io/apimachinery/pkg/api/meta"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
    "sigs.k8s.io/controller-runtime/pkg/log"

    myappsv1 "github.com/myorg/my-operator/api/v1"
)

const (
    finalizerName = "myapp.example.com/finalizer"

    // Condition types
    ConditionTypeReady      = "Ready"
    ConditionTypeProgressing = "Progressing"
    ConditionTypeDegraded    = "Degraded"
)

// MyAppReconciler reconciles a MyApp object
type MyAppReconciler struct {
    client.Client
    Scheme *runtime.Scheme
}

// +kubebuilder:rbac:groups=apps.example.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps/finalizers,verbs=update
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=events,verbs=create;patch

func (r *MyAppReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    // Fetch the MyApp instance
    myApp := &myappsv1.MyApp{}
    if err := r.Get(ctx, req.NamespacedName, myApp); err != nil {
        if errors.IsNotFound(err) {
            log.Info("MyApp resource not found. Ignoring since object must be deleted")
            return ctrl.Result{}, nil
        }
        log.Error(err, "Failed to get MyApp")
        return ctrl.Result{}, err
    }

    // Handle deletion with finalizers
    if !myApp.DeletionTimestamp.IsZero() {
        return r.reconcileDelete(ctx, myApp)
    }

    // Add finalizer if not present
    if !controllerutil.ContainsFinalizer(myApp, finalizerName) {
        controllerutil.AddFinalizer(myApp, finalizerName)
        if err := r.Update(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        log.Info("Added finalizer to MyApp")
    }

    // Set Progressing condition
    meta.SetStatusCondition(&myApp.Status.Conditions, metav1.Condition{
        Type:    ConditionTypeProgressing,
        Status:  metav1.ConditionTrue,
        Reason:  "Reconciling",
        Message: "Starting reconciliation",
    })

    // Reconcile Deployment
    if err := r.reconcileDeployment(ctx, myApp); err != nil {
        log.Error(err, "Failed to reconcile Deployment")
        r.setDegradedCondition(myApp, "DeploymentFailed", err.Error())
        if err := r.Status().Update(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        return ctrl.Result{RequeueAfter: 30 * time.Second}, err
    }

    // Reconcile Service
    if err := r.reconcileService(ctx, myApp); err != nil {
        log.Error(err, "Failed to reconcile Service")
        r.setDegradedCondition(myApp, "ServiceFailed", err.Error())
        if err := r.Status().Update(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        return ctrl.Result{RequeueAfter: 30 * time.Second}, err
    }

    // Update status based on Deployment readiness
    deployment := &appsv1.Deployment{}
    if err := r.Get(ctx, types.NamespacedName{
        Name:      myApp.Name,
        Namespace: myApp.Namespace,
    }, deployment); err != nil {
        return ctrl.Result{}, err
    }

    myApp.Status.ReadyReplicas = deployment.Status.ReadyReplicas
    myApp.Status.LastUpdateTime = metav1.Now()

    if deployment.Status.ReadyReplicas == myApp.Spec.Size {
        myApp.Status.Phase = "Running"
        meta.SetStatusCondition(&myApp.Status.Conditions, metav1.Condition{
            Type:    ConditionTypeReady,
            Status:  metav1.ConditionTrue,
            Reason:  "AllReplicasReady",
            Message: fmt.Sprintf("%d/%d replicas ready", myApp.Status.ReadyReplicas, myApp.Spec.Size),
        })
        meta.RemoveStatusCondition(&myApp.Status.Conditions, ConditionTypeProgressing)
    } else {
        myApp.Status.Phase = "Pending"
        meta.SetStatusCondition(&myApp.Status.Conditions, metav1.Condition{
            Type:    ConditionTypeProgressing,
            Status:  metav1.ConditionTrue,
            Reason:  "WaitingForReplicas",
            Message: fmt.Sprintf("%d/%d replicas ready", myApp.Status.ReadyReplicas, myApp.Spec.Size),
        })
    }

    if err := r.Status().Update(ctx, myApp); err != nil {
        log.Error(err, "Failed to update MyApp status")
        return ctrl.Result{}, err
    }

    log.Info("Successfully reconciled MyApp",
        "readyReplicas", myApp.Status.ReadyReplicas,
        "desiredReplicas", myApp.Spec.Size)

    return ctrl.Result{RequeueAfter: 5 * time.Minute}, nil
}

func (r *MyAppReconciler) reconcileDeployment(ctx context.Context, myApp *myappsv1.MyApp) error {
    log := log.FromContext(ctx)

    deployment := &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      myApp.Name,
            Namespace: myApp.Namespace,
        },
    }

    op, err := controllerutil.CreateOrUpdate(ctx, r.Client, deployment, func() error {
        // Set labels
        deployment.Labels = map[string]string{
            "app.kubernetes.io/name":       "myapp",
            "app.kubernetes.io/instance":   myApp.Name,
            "app.kubernetes.io/managed-by": "myapp-operator",
        }

        // Set spec
        replicas := myApp.Spec.Size
        deployment.Spec.Replicas = &replicas
        deployment.Spec.Selector = &metav1.LabelSelector{
            MatchLabels: map[string]string{
                "app.kubernetes.io/name":     "myapp",
                "app.kubernetes.io/instance": myApp.Name,
            },
        }

        deployment.Spec.Template = corev1.PodTemplateSpec{
            ObjectMeta: metav1.ObjectMeta{
                Labels: map[string]string{
                    "app.kubernetes.io/name":     "myapp",
                    "app.kubernetes.io/instance": myApp.Name,
                },
            },
            Spec: corev1.PodSpec{
                Containers: []corev1.Container{
                    {
                        Name:  "app",
                        Image: myApp.Spec.Image,
                        Ports: []corev1.ContainerPort{
                            {
                                Name:          "http",
                                ContainerPort: myApp.Spec.Port,
                                Protocol:      corev1.ProtocolTCP,
                            },
                        },
                    },
                },
            },
        }

        // Apply resource limits if specified
        if myApp.Spec.Resources != nil {
            deployment.Spec.Template.Spec.Containers[0].Resources = corev1.ResourceRequirements{
                Limits: corev1.ResourceList{
                    corev1.ResourceCPU:    parseQuantity(myApp.Spec.Resources.CPULimit),
                    corev1.ResourceMemory: parseQuantity(myApp.Spec.Resources.MemoryLimit),
                },
            }
        }

        // Set owner reference
        return controllerutil.SetControllerReference(myApp, deployment, r.Scheme)
    })

    if err != nil {
        return err
    }

    log.Info("Deployment reconciled", "operation", op)
    return nil
}

func (r *MyAppReconciler) reconcileService(ctx context.Context, myApp *myappsv1.MyApp) error {
    log := log.FromContext(ctx)

    service := &corev1.Service{
        ObjectMeta: metav1.ObjectMeta{
            Name:      myApp.Name,
            Namespace: myApp.Namespace,
        },
    }

    op, err := controllerutil.CreateOrUpdate(ctx, r.Client, service, func() error {
        service.Labels = map[string]string{
            "app.kubernetes.io/name":       "myapp",
            "app.kubernetes.io/instance":   myApp.Name,
            "app.kubernetes.io/managed-by": "myapp-operator",
        }

        service.Spec.Selector = map[string]string{
            "app.kubernetes.io/name":     "myapp",
            "app.kubernetes.io/instance": myApp.Name,
        }

        service.Spec.Ports = []corev1.ServicePort{
            {
                Name:     "http",
                Port:     80,
                TargetPort: intstr.FromInt(int(myApp.Spec.Port)),
                Protocol:   corev1.ProtocolTCP,
            },
        }

        service.Spec.Type = corev1.ServiceTypeClusterIP

        return controllerutil.SetControllerReference(myApp, service, r.Scheme)
    })

    if err != nil {
        return err
    }

    log.Info("Service reconciled", "operation", op)
    return nil
}

func (r *MyAppReconciler) reconcileDelete(ctx context.Context, myApp *myappsv1.MyApp) (ctrl.Result, error) {
    log := log.FromContext(ctx)

    if controllerutil.ContainsFinalizer(myApp, finalizerName) {
        // Perform cleanup (e.g., delete external resources)
        log.Info("Performing cleanup before deletion")

        // Example: Clean up external resources
        if err := r.cleanupExternalResources(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }

        // Remove finalizer
        controllerutil.RemoveFinalizer(myApp, finalizerName)
        if err := r.Update(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }
        log.Info("Removed finalizer from MyApp")
    }

    return ctrl.Result{}, nil
}

func (r *MyAppReconciler) cleanupExternalResources(ctx context.Context, myApp *myappsv1.MyApp) error {
    // Implement cleanup logic (e.g., delete cloud resources, notify external systems)
    // This is a placeholder
    return nil
}

func (r *MyAppReconciler) setDegradedCondition(myApp *myappsv1.MyApp, reason, message string) {
    meta.SetStatusCondition(&myApp.Status.Conditions, metav1.Condition{
        Type:    ConditionTypeDegraded,
        Status:  metav1.ConditionTrue,
        Reason:  reason,
        Message: message,
    })
    myApp.Status.Phase = "Failed"
}

func parseQuantity(s string) resource.Quantity {
    q, _ := resource.ParseQuantity(s)
    return q
}

// SetupWithManager sets up the controller with the Manager
func (r *MyAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
    return ctrl.NewControllerManagedBy(mgr).
        For(&myappsv1.MyApp{}).
        Owns(&appsv1.Deployment{}).
        Owns(&corev1.Service{}).
        Complete(r)
}
```

#### Error Handling Strategies

**Requeue Patterns:**

```go
// Immediate requeue (rate-limited by controller)
return ctrl.Result{Requeue: true}, nil

// Requeue after delay (e.g., waiting for external resource)
return ctrl.Result{RequeueAfter: 30 * time.Second}, nil

// No requeue (success, or waiting for watch event)
return ctrl.Result{}, nil

// Error with requeue (exponential backoff)
return ctrl.Result{}, fmt.Errorf("transient error: %w", err)
```

**Transient vs Permanent Errors:**

```go
func (r *MyAppReconciler) handleError(ctx context.Context, myApp *myappsv1.MyApp, err error) (ctrl.Result, error) {
    if isTransientError(err) {
        // Temporary issue (network timeout, API rate limit) - retry
        return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
    }

    if isPermanentError(err) {
        // Configuration issue - set error condition, don't requeue
        r.setDegradedCondition(myApp, "ConfigurationError", err.Error())
        r.Status().Update(ctx, myApp)
        return ctrl.Result{}, nil // Don't requeue until user fixes config
    }

    // Unknown error - let controller retry with exponential backoff
    return ctrl.Result{}, err
}

func isTransientError(err error) bool {
    // Check for network errors, timeouts, rate limits
    return errors.IsServiceUnavailable(err) ||
           errors.IsTimeout(err) ||
           errors.IsTooManyRequests(err)
}

func isPermanentError(err error) bool {
    // Check for validation errors, forbidden access
    return errors.IsInvalid(err) ||
           errors.IsForbidden(err) ||
           errors.IsUnauthorized(err)
}
```

---

### 2.3 Admission Webhooks

Webhooks intercept API requests to validate or mutate resources before they're persisted. They enable custom validation logic and policy enforcement.

#### Webhook Types

| Type | Purpose | Example Use Cases |
|------|---------|-------------------|
| **Validating** | Accept/reject requests | Enforce naming conventions, validate cross-field logic, check quotas |
| **Mutating** | Modify requests | Inject sidecars, set defaults, add labels/annotations |

#### Implementing Validating Webhook

**Step 1: Implement webhook interface** (`api/v1/myapp_webhook.go`):

```go
package v1

import (
    "fmt"
    "k8s.io/apimachinery/pkg/runtime"
    ctrl "sigs.k8s.io/controller-runtime"
    logf "sigs.k8s.io/controller-runtime/pkg/log"
    "sigs.k8s.io/controller-runtime/pkg/webhook"
    "sigs.k8s.io/controller-runtime/pkg/webhook/admission"
)

var myapplog = logf.Log.WithName("myapp-webhook")

func (r *MyApp) SetupWebhookWithManager(mgr ctrl.Manager) error {
    return ctrl.NewWebhookManagedBy(mgr).
        For(r).
        Complete()
}

// +kubebuilder:webhook:path=/validate-apps-example-com-v1-myapp,mutating=false,failurePolicy=fail,sideEffects=None,groups=apps.example.com,resources=myapps,verbs=create;update,versions=v1,name=vmyapp.kb.io,admissionReviewVersions=v1

var _ webhook.Validator = &MyApp{}

// ValidateCreate implements webhook.Validator
func (r *MyApp) ValidateCreate() (admission.Warnings, error) {
    myapplog.Info("validate create", "name", r.Name)

    return r.validateMyApp()
}

// ValidateUpdate implements webhook.Validator
func (r *MyApp) ValidateUpdate(old runtime.Object) (admission.Warnings, error) {
    myapplog.Info("validate update", "name", r.Name)

    oldMyApp := old.(*MyApp)

    // Prevent scaling down below 1 replica
    if r.Spec.Size < oldMyApp.Spec.Size && r.Spec.Size < 1 {
        return nil, fmt.Errorf("cannot scale below 1 replica")
    }

    // Prevent changing image registry
    oldRegistry := getRegistry(oldMyApp.Spec.Image)
    newRegistry := getRegistry(r.Spec.Image)
    if oldRegistry != newRegistry {
        return admission.Warnings{"Changing image registry may cause downtime"}, nil
    }

    return r.validateMyApp()
}

// ValidateDelete implements webhook.Validator
func (r *MyApp) ValidateDelete() (admission.Warnings, error) {
    myapplog.Info("validate delete", "name", r.Name)

    // Example: Prevent deletion of production instances
    if r.Labels["environment"] == "production" {
        return nil, fmt.Errorf("production instances cannot be deleted via API")
    }

    return nil, nil
}

func (r *MyApp) validateMyApp() (admission.Warnings, error) {
    var allWarnings admission.Warnings
    var allErrors []string

    // Validate size is within reasonable bounds
    if r.Spec.Size > 100 {
        allWarnings = append(allWarnings, "Large replica count may consume excessive resources")
    }

    // Validate image format
    if !isValidImageFormat(r.Spec.Image) {
        allErrors = append(allErrors, "image must be in format registry/name:tag")
    }

    // Validate port range
    if r.Spec.Port != 0 && (r.Spec.Port < 1024 || r.Spec.Port > 65535) {
        allErrors = append(allErrors, "port must be between 1024 and 65535")
    }

    // Cross-field validation
    if r.Spec.Resources != nil {
        if err := validateResources(r.Spec.Resources); err != nil {
            allErrors = append(allErrors, err.Error())
        }
    }

    if len(allErrors) > 0 {
        return allWarnings, fmt.Errorf("validation failed: %v", allErrors)
    }

    return allWarnings, nil
}

func isValidImageFormat(image string) bool {
    // Simplified validation - production should use regex
    return len(image) > 0 && contains(image, "/") && contains(image, ":")
}

func validateResources(res *ResourceRequirements) error {
    // Example: CPU limit must be at least 100m
    if res.CPULimit != "" {
        cpu := parseMillicores(res.CPULimit)
        if cpu < 100 {
            return fmt.Errorf("CPU limit must be at least 100m")
        }
    }

    // Example: Memory limit must be at least 64Mi
    if res.MemoryLimit != "" {
        mem := parseMegabytes(res.MemoryLimit)
        if mem < 64 {
            return fmt.Errorf("memory limit must be at least 64Mi")
        }
    }

    return nil
}

func getRegistry(image string) string {
    // Extract registry from image (simplified)
    parts := strings.Split(image, "/")
    if len(parts) > 0 {
        return parts[0]
    }
    return ""
}
```

#### Implementing Mutating Webhook

```go
// +kubebuilder:webhook:path=/mutate-apps-example-com-v1-myapp,mutating=true,failurePolicy=fail,sideEffects=None,groups=apps.example.com,resources=myapps,verbs=create;update,versions=v1,name=mmyapp.kb.io,admissionReviewVersions=v1

var _ webhook.Defaulter = &MyApp{}

// Default implements webhook.Defaulter
func (r *MyApp) Default() {
    myapplog.Info("default", "name", r.Name)

    // Set default port if not specified
    if r.Spec.Port == 0 {
        r.Spec.Port = 8080
    }

    // Set default resources if not specified
    if r.Spec.Resources == nil {
        r.Spec.Resources = &ResourceRequirements{
            CPULimit:    "500m",
            MemoryLimit: "512Mi",
        }
    }

    // Add standard labels
    if r.Labels == nil {
        r.Labels = make(map[string]string)
    }
    r.Labels["app.kubernetes.io/managed-by"] = "myapp-operator"

    // Set default size
    if r.Spec.Size == 0 {
        r.Spec.Size = 1
    }
}
```

**Step 2: Register webhook in main.go**:

```go
func main() {
    // ... manager setup ...

    if err = (&appsv1.MyApp{}).SetupWebhookWithManager(mgr); err != nil {
        setupLog.Error(err, "unable to create webhook", "webhook", "MyApp")
        os.Exit(1)
    }

    // ... start manager ...
}
```

**Step 3: Generate webhook manifests**:

```bash
make manifests  # Generates config/webhook/manifests.yaml
```

#### Webhook Deployment

Webhooks require TLS certificates. Use cert-manager:

```yaml
# config/default/kustomization.yaml
bases:
- ../webhook
- ../certmanager

replacements:
- source:
    kind: Certificate
    name: serving-cert
  targets:
  - select:
      kind: ValidatingWebhookConfiguration
    fieldPaths:
    - .webhooks[].clientConfig.caBundle
```

---

### 2.4 Leader Election for High Availability

Leader election ensures only one controller instance reconciles resources at a time, preventing conflicts in multi-replica deployments.

**Configuration** (`main.go`):

```go
mgr, err := ctrl.NewManager(ctrl.GetConfigOrDie(), ctrl.Options{
    // ... other options ...
    LeaderElection:          true,
    LeaderElectionID:        "myapp-controller-leader.example.com",
    LeaderElectionNamespace: "myapp-system",
    LeaseDuration:           &leaseDuration,    // 15s default
    RenewDeadline:           &renewDeadline,    // 10s default
    RetryPeriod:             &retryPeriod,      // 2s default
})
```

**Deployment with multiple replicas**:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp-controller
spec:
  replicas: 3  # High availability
  template:
    spec:
      containers:
      - name: manager
        args:
        - --leader-elect
        - --leader-election-id=myapp-controller-leader.example.com
```

**RBAC for leader election**:

```yaml
# Generated by kubebuilder
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: leader-election-role
rules:
- apiGroups: ["coordination.k8s.io"]
  resources: ["leases"]
  verbs: ["get", "create", "update"]
```

---

### 2.5 Testing Operators

#### Unit Testing with envtest

`envtest` runs a local API server for fast unit tests without a full cluster.

**Setup** (`controllers/suite_test.go`):

```go
package controllers

import (
    "path/filepath"
    "testing"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"

    "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/envtest"
    logf "sigs.k8s.io/controller-runtime/pkg/log"
    "sigs.k8s.io/controller-runtime/pkg/log/zap"

    appsv1 "github.com/myorg/my-operator/api/v1"
)

var (
    k8sClient client.Client
    testEnv   *envtest.Environment
    ctx       = ctrl.SetupSignalHandler()
)

func TestControllers(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Controller Suite")
}

var _ = BeforeSuite(func() {
    logf.SetLogger(zap.New(zap.WriteTo(GinkgoWriter), zap.UseDevMode(true)))

    By("bootstrapping test environment")
    testEnv = &envtest.Environment{
        CRDDirectoryPaths:     []string{filepath.Join("..", "config", "crd", "bases")},
        ErrorIfCRDPathMissing: true,
    }

    cfg, err := testEnv.Start()
    Expect(err).NotTo(HaveOccurred())
    Expect(cfg).NotTo(BeNil())

    err = appsv1.AddToScheme(scheme.Scheme)
    Expect(err).NotTo(HaveOccurred())

    k8sClient, err = client.New(cfg, client.Options{Scheme: scheme.Scheme})
    Expect(err).NotTo(HaveOccurred())
    Expect(k8sClient).NotTo(BeNil())
})

var _ = AfterSuite(func() {
    By("tearing down the test environment")
    err := testEnv.Stop()
    Expect(err).NotTo(HaveOccurred())
})
```

**Test Cases** (`controllers/myapp_controller_test.go`):

```go
package controllers

import (
    "context"
    "time"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/types"

    myappsv1 "github.com/myorg/my-operator/api/v1"
)

var _ = Describe("MyApp Controller", func() {
    const (
        timeout  = time.Second * 10
        interval = time.Millisecond * 250
    )

    Context("When creating MyApp", func() {
        It("Should create Deployment and Service", func() {
            ctx := context.Background()

            myApp := &myappsv1.MyApp{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "test-myapp",
                    Namespace: "default",
                },
                Spec: myappsv1.MyAppSpec{
                    Size:  3,
                    Image: "nginx:latest",
                    Port:  8080,
                },
            }

            Expect(k8sClient.Create(ctx, myApp)).Should(Succeed())

            // Wait for Deployment
            deployment := &appsv1.Deployment{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-myapp",
                    Namespace: "default",
                }, deployment)
            }, timeout, interval).Should(Succeed())

            Expect(*deployment.Spec.Replicas).To(Equal(int32(3)))
            Expect(deployment.Spec.Template.Spec.Containers[0].Image).To(Equal("nginx:latest"))

            // Wait for Service
            service := &corev1.Service{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-myapp",
                    Namespace: "default",
                }, service)
            }, timeout, interval).Should(Succeed())

            Expect(service.Spec.Ports[0].TargetPort.IntVal).To(Equal(int32(8080)))
        })

        It("Should update status when replicas are ready", func() {
            ctx := context.Background()

            // Simulate Deployment readiness
            deployment := &appsv1.Deployment{}
            Expect(k8sClient.Get(ctx, types.NamespacedName{
                Name:      "test-myapp",
                Namespace: "default",
            }, deployment)).Should(Succeed())

            deployment.Status.ReadyReplicas = 3
            Expect(k8sClient.Status().Update(ctx, deployment)).Should(Succeed())

            // Wait for MyApp status update
            myApp := &myappsv1.MyApp{}
            Eventually(func() int32 {
                k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-myapp",
                    Namespace: "default",
                }, myApp)
                return myApp.Status.ReadyReplicas
            }, timeout, interval).Should(Equal(int32(3)))

            Expect(myApp.Status.Phase).To(Equal("Running"))
        })
    })
})
```

#### Integration Testing with kind

**Test Script** (`test/e2e/e2e_test.sh`):

```bash
#!/bin/bash
set -e

# Create kind cluster
kind create cluster --name operator-test

# Build and load operator image
make docker-build IMG=myapp-operator:test
kind load docker-image myapp-operator:test --name operator-test

# Deploy operator
make deploy IMG=myapp-operator:test

# Wait for operator to be ready
kubectl wait --for=condition=available --timeout=60s \
  deployment/myapp-controller-manager -n myapp-system

# Create test MyApp
kubectl apply -f test/e2e/test-myapp.yaml

# Wait for MyApp to be ready
kubectl wait --for=condition=Ready --timeout=120s \
  myapp/test-myapp

# Verify Deployment and Service
kubectl get deployment test-myapp -o yaml
kubectl get service test-myapp -o yaml

# Cleanup
kind delete cluster --name operator-test
```

---

### 2.6 Deployment and RBAC

#### RBAC Configuration

Kubebuilder generates RBAC rules from controller markers:

```go
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
```

**Generated RBAC** (`config/rbac/role.yaml`):

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: manager-role
rules:
- apiGroups: ["apps.example.com"]
  resources: ["myapps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

#### Deployment Configuration

**Operator Deployment** (`config/manager/manager.yaml`):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: controller-manager
  namespace: system
spec:
  replicas: 1
  selector:
    matchLabels:
      control-plane: controller-manager
  template:
    metadata:
      labels:
        control-plane: controller-manager
    spec:
      serviceAccountName: controller-manager
      containers:
      - name: manager
        image: controller:latest
        command:
        - /manager
        args:
        - --leader-elect
        - --metrics-bind-address=:8080
        - --health-probe-bind-address=:8081
        env:
        - name: POD_NAMESPACE
          valueFrom:
            fieldRef:
              fieldPath: metadata.namespace
        livenessProbe:
          httpGet:
            path: /healthz
            port: 8081
          initialDelaySeconds: 15
          periodSeconds: 20
        readinessProbe:
          httpGet:
            path: /readyz
            port: 8081
          initialDelaySeconds: 5
          periodSeconds: 10
        resources:
          limits:
            cpu: 500m
            memory: 512Mi
          requests:
            cpu: 100m
            memory: 128Mi
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
      securityContext:
        runAsNonRoot: true
        seccompProfile:
          type: RuntimeDefault
```

---

### 2.7 Best Practices and Anti-Patterns

#### Best Practices

✅ **Idempotent Reconciliation**

- Ensure reconcile function produces same result when called multiple times
- Use `CreateOrUpdate` instead of separate `Create`/`Update` logic

✅ **Status Conditions**

- Use standard condition types (`Ready`, `Progressing`, `Degraded`)
- Include detailed messages for debugging

✅ **Finalizers for Cleanup**

- Use finalizers to clean up external resources before deletion
- Implement robust cleanup logic with timeouts

✅ **Owner References**

- Set owner references for managed resources (automatic garbage collection)
- Use `controllerutil.SetControllerReference()`

✅ **Structured Logging**

- Use controller-runtime's logger with consistent key-value pairs
- Log important state transitions and errors

✅ **Resource Limits**

- Set CPU/memory limits for operator pods
- Monitor resource usage in production

✅ **Graceful Error Handling**

- Distinguish transient vs permanent errors
- Use appropriate requeue strategies

#### Anti-Patterns

❌ **Blocking Operations**

- Don't make synchronous API calls that block reconciliation
- Use background workers for long-running tasks

❌ **Infinite Loops**

- Don't update resource spec in reconcile (triggers another reconcile)
- Only update status subresource

❌ **Missing Watch Permissions**

- Ensure RBAC allows watching all dependent resources
- Missing watches cause stale cache reads

❌ **Hardcoded Values**

- Don't hardcode namespaces, names, or configurations
- Use environment variables or ConfigMaps

❌ **Ignoring Errors**

- Always handle and log errors
- Return errors to trigger exponential backoff

❌ **No Health Checks**

- Implement `/healthz` and `/readyz` endpoints
- Enable Kubernetes to detect unhealthy controllers

❌ **Testing Only in Production**

- Write unit tests with envtest
- Use integration tests with kind/minikube

---

## Level 3: Deep Dive Resources

### Advanced Operator Patterns

**State Machine Operators**

- Model complex workflows as finite state machines
- Use status phases to track progression through states
- Implement state transition validations and guards

**Multi-Tenancy Operators**

- Namespace isolation strategies
- Shared vs dedicated operator deployments
- RBAC scoping for tenant-specific resources

**GitOps Integration**

- Reconcile against Git repository state
- Implement drift detection and auto-remediation
- Use annotations to track source commits

**External Secret Management**

- Integrate with Vault, AWS Secrets Manager, or Azure Key Vault
- Implement secret rotation without downtime
- Use external-secrets operator pattern

### Multi-Cluster Operators

**Architecture Patterns:**

1. **Hub-Spoke Model** - Central operator manages multiple clusters
2. **Federated Model** - Operators in each cluster coordinate via shared state
3. **Active-Active** - Operators in multiple clusters handle same resources

**Implementation Considerations:**

- Use cluster-api for cluster lifecycle management
- Implement cross-cluster service discovery (e.g., Submariner)
- Handle network partitions and split-brain scenarios
- Use consensus protocols for distributed state

**Tools:**

- **KubeFed** (deprecated) - Kubernetes Federation v2
- **OCM (Open Cluster Management)** - CNCF sandbox project
- **Argo CD ApplicationSet** - Multi-cluster GitOps
- **Crossplane** - Universal control plane for multi-cloud

### Operator Lifecycle Manager (OLM)

**What is OLM?**

- Package manager for Kubernetes operators
- Handles installation, upgrades, and dependency management
- Used by OpenShift and available as CNCF project

**OLM Components:**

- **Catalog** - Repository of operator metadata (CSV, CRD)
- **Subscription** - Declarative operator installation
- **InstallPlan** - Execution plan for operator installation
- **ClusterServiceVersion (CSV)** - Operator metadata and deployment info

**Creating an OLM Bundle:**

```bash
# Generate bundle manifests
operator-sdk generate bundle --version 1.0.0

# Validate bundle
operator-sdk bundle validate ./bundle

# Build and push bundle image
docker build -f bundle.Dockerfile -t myregistry/myapp-operator-bundle:v1.0.0 .
docker push myregistry/myapp-operator-bundle:v1.0.0

# Add to catalog
opm index add --bundles myregistry/myapp-operator-bundle:v1.0.0 \
  --tag myregistry/myapp-catalog:latest
```

**OLM Best Practices:**

- Define proper upgrade paths in CSV
- Test upgrade scenarios (skip versions, downgrades)
- Use semantic versioning
- Document breaking changes in release notes

### Advanced Testing Strategies

**Property-Based Testing:**

- Use tools like `gopter` for property-based tests
- Test invariants across state transitions
- Generate random valid/invalid inputs

**Chaos Testing:**

- Use Chaos Mesh or Litmus to inject failures
- Test operator resilience to node failures, network partitions
- Verify recovery from partial updates

**Performance Testing:**

- Benchmark reconciliation loop latency
- Test with 1000+ custom resources
- Measure memory/CPU usage under load
- Use profiling tools (pprof) for bottleneck analysis

### Production Readiness Checklist

**Observability:**

- [ ] Metrics exported via Prometheus endpoint
- [ ] Structured logging with levels (info, warn, error)
- [ ] Distributed tracing (OpenTelemetry)
- [ ] Custom metrics for business logic (e.g., backup success rate)

**Security:**

- [ ] RBAC follows least-privilege principle
- [ ] Secrets encrypted at rest and in transit
- [ ] Pod Security Standards enforced
- [ ] Network policies restrict traffic
- [ ] Image vulnerability scanning in CI/CD

**Reliability:**

- [ ] Leader election enabled for HA
- [ ] Graceful shutdown with finalizers
- [ ] Rate limiting to prevent API server overload
- [ ] Circuit breakers for external dependencies
- [ ] Backup/restore procedures documented

**Operational:**

- [ ] Runbooks for common failure scenarios
- [ ] SLO/SLI definitions (e.g., 99.9% reconciliation success)
- [ ] Alerting rules for critical conditions
- [ ] Upgrade/rollback procedures tested
- [ ] Capacity planning documented

### Resources and Further Learning

**Official Documentation:**

- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Operator SDK Documentation](https://sdk.operatorframework.io/)
- [Kubernetes Controller Runtime](https://github.com/kubernetes-sigs/controller-runtime)

**Bundled Resources in This Directory:**

1. `templates/crd-definition.yaml` - Complete CRD with OpenAPI schema
2. `templates/operator-scaffold.go` - Controller with reconcile logic
3. `templates/webhook.go` - Validating and mutating webhooks
4. `templates/rbac.yaml` - RBAC manifests for operator deployment
5. `scripts/setup-operator-dev.sh` - Development environment setup
6. `resources/operator-patterns.md` - Common patterns and anti-patterns

**Community Resources:**

- [CNCF Operator White Paper](https://github.com/cncf/tag-app-delivery/blob/main/operator-wg/whitepaper/Operator-WhitePaper_v1-0.md)
- [Awesome Operators](https://github.com/operator-framework/awesome-operators)
- [Kubernetes Slack #kubebuilder](https://kubernetes.slack.com/)

**Example Production Operators:**

- [etcd-operator](https://github.com/coreos/etcd-operator)
- [prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
- [cert-manager](https://github.com/cert-manager/cert-manager)
- [strimzi-kafka-operator](https://github.com/strimzi/strimzi-kafka-operator)

### Next Steps

1. **Build a Simple Operator** - Start with a basic CRD and controller
2. **Add Validation** - Implement admission webhooks
3. **Test Thoroughly** - Write unit tests with envtest, integration tests with kind
4. **Observe in Production** - Deploy with metrics, logging, and tracing
5. **Iterate** - Add features based on operational experience

**Advanced Topics to Explore:**

- Custom admission plugins
- API aggregation and extension API servers
- Operator Hub and OLM
- Multi-cluster federation
- Operator performance optimization

---

**End of Advanced Kubernetes Skill**
