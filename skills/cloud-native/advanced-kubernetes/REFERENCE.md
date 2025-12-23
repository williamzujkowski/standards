# Advanced Kubernetes - Reference Implementation

This document contains detailed code examples, complete controller implementations, and advanced patterns extracted from the main skill guide.

## Table of Contents

- [Complete CRD Definition](#complete-crd-definition)
- [Full Controller Implementation](#full-controller-implementation)
- [Admission Webhooks](#admission-webhooks)
- [Testing Examples](#testing-examples)
- [RBAC and Deployment](#rbac-and-deployment)
- [Advanced Patterns](#advanced-patterns)

---

## Complete CRD Definition

### CRD API Types (api/v1/myapp_types.go)

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

### Kubebuilder Validation Markers Reference

| Marker | Purpose | Example |
|--------|---------|---------|
| `+kubebuilder:validation:Minimum` | Min value | `// +kubebuilder:validation:Minimum=0` |
| `+kubebuilder:validation:Maximum` | Max value | `// +kubebuilder:validation:Maximum=100` |
| `+kubebuilder:validation:Pattern` | Regex | `// +kubebuilder:validation:Pattern=^[a-z]+$` |
| `+kubebuilder:validation:Enum` | Allowed values | `// +kubebuilder:validation:Enum=A;B;C` |
| `+kubebuilder:validation:MinLength` | Min string length | `// +kubebuilder:validation:MinLength=3` |
| `+kubebuilder:validation:Required` | Field required | `// +kubebuilder:validation:Required` |
| `+optional` | Field optional | `// +optional` |
| `+kubebuilder:default` | Default value | `// +kubebuilder:default=8080` |

---

## Full Controller Implementation

### Complete Reconciler (controllers/myapp_controller.go)

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
    "k8s.io/apimachinery/pkg/util/intstr"
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
        deployment.Labels = map[string]string{
            "app.kubernetes.io/name":       "myapp",
            "app.kubernetes.io/instance":   myApp.Name,
            "app.kubernetes.io/managed-by": "myapp-operator",
        }

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

        if myApp.Spec.Resources != nil {
            deployment.Spec.Template.Spec.Containers[0].Resources = corev1.ResourceRequirements{
                Limits: corev1.ResourceList{
                    corev1.ResourceCPU:    parseQuantity(myApp.Spec.Resources.CPULimit),
                    corev1.ResourceMemory: parseQuantity(myApp.Spec.Resources.MemoryLimit),
                },
            }
        }

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
                Name:       "http",
                Port:       80,
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
        log.Info("Performing cleanup before deletion")

        if err := r.cleanupExternalResources(ctx, myApp); err != nil {
            return ctrl.Result{}, err
        }

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

---

## Admission Webhooks

### Validating Webhook (api/v1/myapp_webhook.go)

```go
package v1

import (
    "fmt"
    "strings"
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

func (r *MyApp) ValidateCreate() (admission.Warnings, error) {
    myapplog.Info("validate create", "name", r.Name)
    return r.validateMyApp()
}

func (r *MyApp) ValidateUpdate(old runtime.Object) (admission.Warnings, error) {
    myapplog.Info("validate update", "name", r.Name)

    oldMyApp := old.(*MyApp)

    if r.Spec.Size < oldMyApp.Spec.Size && r.Spec.Size < 1 {
        return nil, fmt.Errorf("cannot scale below 1 replica")
    }

    oldRegistry := getRegistry(oldMyApp.Spec.Image)
    newRegistry := getRegistry(r.Spec.Image)
    if oldRegistry != newRegistry {
        return admission.Warnings{"Changing image registry may cause downtime"}, nil
    }

    return r.validateMyApp()
}

func (r *MyApp) ValidateDelete() (admission.Warnings, error) {
    myapplog.Info("validate delete", "name", r.Name)

    if r.Labels["environment"] == "production" {
        return nil, fmt.Errorf("production instances cannot be deleted via API")
    }

    return nil, nil
}

func (r *MyApp) validateMyApp() (admission.Warnings, error) {
    var allWarnings admission.Warnings
    var allErrors []string

    if r.Spec.Size > 100 {
        allWarnings = append(allWarnings, "Large replica count may consume excessive resources")
    }

    if !isValidImageFormat(r.Spec.Image) {
        allErrors = append(allErrors, "image must be in format registry/name:tag")
    }

    if r.Spec.Port != 0 && (r.Spec.Port < 1024 || r.Spec.Port > 65535) {
        allErrors = append(allErrors, "port must be between 1024 and 65535")
    }

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
    return len(image) > 0 && strings.Contains(image, "/") && strings.Contains(image, ":")
}

func validateResources(res *ResourceRequirements) error {
    if res.CPULimit != "" {
        cpu := parseMillicores(res.CPULimit)
        if cpu < 100 {
            return fmt.Errorf("CPU limit must be at least 100m")
        }
    }

    if res.MemoryLimit != "" {
        mem := parseMegabytes(res.MemoryLimit)
        if mem < 64 {
            return fmt.Errorf("memory limit must be at least 64Mi")
        }
    }

    return nil
}

func getRegistry(image string) string {
    parts := strings.Split(image, "/")
    if len(parts) > 0 {
        return parts[0]
    }
    return ""
}
```

### Mutating Webhook (Defaulter)

```go
// +kubebuilder:webhook:path=/mutate-apps-example-com-v1-myapp,mutating=true,failurePolicy=fail,sideEffects=None,groups=apps.example.com,resources=myapps,verbs=create;update,versions=v1,name=mmyapp.kb.io,admissionReviewVersions=v1

var _ webhook.Defaulter = &MyApp{}

func (r *MyApp) Default() {
    myapplog.Info("default", "name", r.Name)

    if r.Spec.Port == 0 {
        r.Spec.Port = 8080
    }

    if r.Spec.Resources == nil {
        r.Spec.Resources = &ResourceRequirements{
            CPULimit:    "500m",
            MemoryLimit: "512Mi",
        }
    }

    if r.Labels == nil {
        r.Labels = make(map[string]string)
    }
    r.Labels["app.kubernetes.io/managed-by"] = "myapp-operator"

    if r.Spec.Size == 0 {
        r.Spec.Size = 1
    }
}
```

---

## Testing Examples

### envtest Setup (controllers/suite_test.go)

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

### Controller Tests (controllers/myapp_controller_test.go)

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

            deployment := &appsv1.Deployment{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-myapp",
                    Namespace: "default",
                }, deployment)
            }, timeout, interval).Should(Succeed())

            Expect(*deployment.Spec.Replicas).To(Equal(int32(3)))
            Expect(deployment.Spec.Template.Spec.Containers[0].Image).To(Equal("nginx:latest"))

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

            deployment := &appsv1.Deployment{}
            Expect(k8sClient.Get(ctx, types.NamespacedName{
                Name:      "test-myapp",
                Namespace: "default",
            }, deployment)).Should(Succeed())

            deployment.Status.ReadyReplicas = 3
            Expect(k8sClient.Status().Update(ctx, deployment)).Should(Succeed())

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

---

## RBAC and Deployment

### Generated RBAC (config/rbac/role.yaml)

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: manager-role
rules:
- apiGroups: ["apps.example.com"]
  resources: ["myapps"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: ["apps.example.com"]
  resources: ["myapps/status"]
  verbs: ["get", "update", "patch"]
- apiGroups: ["apps.example.com"]
  resources: ["myapps/finalizers"]
  verbs: ["update"]
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["services"]
  verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
- apiGroups: [""]
  resources: ["events"]
  verbs: ["create", "patch"]
```

### Operator Deployment (config/manager/manager.yaml)

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

## Advanced Patterns

### Error Handling Strategies

```go
func (r *MyAppReconciler) handleError(ctx context.Context, myApp *myappsv1.MyApp, err error) (ctrl.Result, error) {
    if isTransientError(err) {
        // Temporary issue - retry with backoff
        return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
    }

    if isPermanentError(err) {
        // Configuration issue - set error condition, don't requeue
        r.setDegradedCondition(myApp, "ConfigurationError", err.Error())
        r.Status().Update(ctx, myApp)
        return ctrl.Result{}, nil
    }

    // Unknown error - let controller retry with exponential backoff
    return ctrl.Result{}, err
}

func isTransientError(err error) bool {
    return errors.IsServiceUnavailable(err) ||
           errors.IsTimeout(err) ||
           errors.IsTooManyRequests(err)
}

func isPermanentError(err error) bool {
    return errors.IsInvalid(err) ||
           errors.IsForbidden(err) ||
           errors.IsUnauthorized(err)
}
```

### CRD Versioning and Conversion

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
    dst.Spec.Size = src.Spec.Replicas
    dst.Spec.Strategy = src.Spec.Strategy
    return nil
}
```

### Integration Testing Script

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

# Wait for operator
kubectl wait --for=condition=available --timeout=60s \
  deployment/myapp-controller-manager -n myapp-system

# Create test MyApp
kubectl apply -f test/e2e/test-myapp.yaml

# Wait for MyApp
kubectl wait --for=condition=Ready --timeout=120s myapp/test-myapp

# Verify resources
kubectl get deployment test-myapp -o yaml
kubectl get service test-myapp -o yaml

# Cleanup
kind delete cluster --name operator-test
```

---

## Additional Resources

### Official Documentation

- [Kubebuilder Book](https://book.kubebuilder.io/)
- [Operator SDK](https://sdk.operatorframework.io/)
- [Controller Runtime](https://github.com/kubernetes-sigs/controller-runtime)

### Production Operator Examples

- [etcd-operator](https://github.com/coreos/etcd-operator)
- [prometheus-operator](https://github.com/prometheus-operator/prometheus-operator)
- [cert-manager](https://github.com/cert-manager/cert-manager)
- [strimzi-kafka-operator](https://github.com/strimzi/strimzi-kafka-operator)
