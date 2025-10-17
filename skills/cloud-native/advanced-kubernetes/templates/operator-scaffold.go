// Kubebuilder Controller Scaffold with Complete Reconcile Logic
// This file demonstrates a production-ready controller implementation

package controllers

import (
	"context"
	"fmt"
	"time"

	appsv1 "k8s.io/api/apps/v1"
	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/api/errors"
	"k8s.io/apimachinery/pkg/api/meta"
	"k8s.io/apimachinery/pkg/api/resource"
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
	finalizerName           = "myapp.example.com/finalizer"
	ConditionTypeReady      = "Ready"
	ConditionTypeProgressing = "Progressing"
	ConditionTypeDegraded    = "Degraded"
)

// MyAppReconciler reconciles a MyApp object
type MyAppReconciler struct {
	client.Client
	Scheme *runtime.Scheme
}

// RBAC permissions for the controller
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps/status,verbs=get;update;patch
// +kubebuilder:rbac:groups=apps.example.com,resources=myapps/finalizers,verbs=update
// +kubebuilder:rbac:groups=apps,resources=deployments,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=services,verbs=get;list;watch;create;update;patch;delete
// +kubebuilder:rbac:groups=core,resources=events,verbs=create;patch

// Reconcile is the main reconciliation loop
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
		log.Info("Adding finalizer to MyApp")
		controllerutil.AddFinalizer(myApp, finalizerName)
		if err := r.Update(ctx, myApp); err != nil {
			return ctrl.Result{}, err
		}
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
		return r.handleError(ctx, myApp, err)
	}

	// Reconcile Service
	if err := r.reconcileService(ctx, myApp); err != nil {
		log.Error(err, "Failed to reconcile Service")
		r.setDegradedCondition(myApp, "ServiceFailed", err.Error())
		if err := r.Status().Update(ctx, myApp); err != nil {
			return ctrl.Result{}, err
		}
		return r.handleError(ctx, myApp, err)
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

	// Requeue after 5 minutes for periodic reconciliation
	return ctrl.Result{RequeueAfter: 5 * time.Minute}, nil
}

// reconcileDeployment ensures the Deployment exists and matches the spec
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

		// Build container spec
		container := corev1.Container{
			Name:  "app",
			Image: myApp.Spec.Image,
			Ports: []corev1.ContainerPort{
				{
					Name:          "http",
					ContainerPort: myApp.Spec.Port,
					Protocol:      corev1.ProtocolTCP,
				},
			},
			Env: buildEnvVars(myApp.Spec.Env),
		}

		// Apply resource limits if specified
		if myApp.Spec.Resources != nil {
			container.Resources = corev1.ResourceRequirements{
				Limits: corev1.ResourceList{},
			}
			if myApp.Spec.Resources.CPULimit != "" {
				container.Resources.Limits[corev1.ResourceCPU] = resource.MustParse(myApp.Spec.Resources.CPULimit)
			}
			if myApp.Spec.Resources.MemoryLimit != "" {
				container.Resources.Limits[corev1.ResourceMemory] = resource.MustParse(myApp.Spec.Resources.MemoryLimit)
			}
		}

		deployment.Spec.Template = corev1.PodTemplateSpec{
			ObjectMeta: metav1.ObjectMeta{
				Labels: map[string]string{
					"app.kubernetes.io/name":     "myapp",
					"app.kubernetes.io/instance": myApp.Name,
				},
			},
			Spec: corev1.PodSpec{
				Containers: []corev1.Container{container},
			},
		}

		// Set deployment strategy
		if myApp.Spec.Strategy == "Recreate" {
			deployment.Spec.Strategy = appsv1.DeploymentStrategy{
				Type: appsv1.RecreateDeploymentStrategyType,
			}
		} else {
			deployment.Spec.Strategy = appsv1.DeploymentStrategy{
				Type: appsv1.RollingUpdateDeploymentStrategyType,
				RollingUpdate: &appsv1.RollingUpdateDeployment{
					MaxUnavailable: &intstr.IntOrString{Type: intstr.String, StrVal: "25%"},
					MaxSurge:       &intstr.IntOrString{Type: intstr.String, StrVal: "25%"},
				},
			}
		}

		// Set owner reference for garbage collection
		return controllerutil.SetControllerReference(myApp, deployment, r.Scheme)
	})

	if err != nil {
		return err
	}

	log.Info("Deployment reconciled", "operation", op)
	return nil
}

// reconcileService ensures the Service exists and matches the spec
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

// reconcileDelete handles resource cleanup before deletion
func (r *MyAppReconciler) reconcileDelete(ctx context.Context, myApp *myappsv1.MyApp) (ctrl.Result, error) {
	log := log.FromContext(ctx)

	if controllerutil.ContainsFinalizer(myApp, finalizerName) {
		log.Info("Performing cleanup before deletion")

		// Clean up external resources (e.g., cloud resources, external APIs)
		if err := r.cleanupExternalResources(ctx, myApp); err != nil {
			log.Error(err, "Failed to clean up external resources")
			return ctrl.Result{}, err
		}

		// Remove finalizer to allow deletion
		controllerutil.RemoveFinalizer(myApp, finalizerName)
		if err := r.Update(ctx, myApp); err != nil {
			return ctrl.Result{}, err
		}
		log.Info("Removed finalizer from MyApp")
	}

	return ctrl.Result{}, nil
}

// cleanupExternalResources handles cleanup of external resources
func (r *MyAppReconciler) cleanupExternalResources(ctx context.Context, myApp *myappsv1.MyApp) error {
	// Implement cleanup logic here
	// Examples:
	// - Delete S3 buckets
	// - Revoke cloud IAM roles
	// - Notify external monitoring systems
	// - Delete DNS records
	return nil
}

// handleError determines if error is transient and sets appropriate requeue
func (r *MyAppReconciler) handleError(ctx context.Context, myApp *myappsv1.MyApp, err error) (ctrl.Result, error) {
	if isTransientError(err) {
		// Temporary issue - retry after delay
		return ctrl.Result{RequeueAfter: 30 * time.Second}, nil
	}

	if isPermanentError(err) {
		// Configuration issue - don't requeue
		return ctrl.Result{}, nil
	}

	// Unknown error - let controller retry with exponential backoff
	return ctrl.Result{}, err
}

// isTransientError checks if error is temporary
func isTransientError(err error) bool {
	return errors.IsServiceUnavailable(err) ||
		errors.IsTimeout(err) ||
		errors.IsTooManyRequests(err)
}

// isPermanentError checks if error requires user intervention
func isPermanentError(err error) bool {
	return errors.IsInvalid(err) ||
		errors.IsForbidden(err) ||
		errors.IsUnauthorized(err)
}

// setDegradedCondition sets the Degraded condition
func (r *MyAppReconciler) setDegradedCondition(myApp *myappsv1.MyApp, reason, message string) {
	meta.SetStatusCondition(&myApp.Status.Conditions, metav1.Condition{
		Type:    ConditionTypeDegraded,
		Status:  metav1.ConditionTrue,
		Reason:  reason,
		Message: message,
	})
	myApp.Status.Phase = "Failed"
}

// buildEnvVars converts spec env vars to corev1.EnvVar
func buildEnvVars(envVars []myappsv1.EnvVar) []corev1.EnvVar {
	result := make([]corev1.EnvVar, len(envVars))
	for i, env := range envVars {
		result[i] = corev1.EnvVar{
			Name:  env.Name,
			Value: env.Value,
		}
	}
	return result
}

// SetupWithManager sets up the controller with the Manager
func (r *MyAppReconciler) SetupWithManager(mgr ctrl.Manager) error {
	return ctrl.NewControllerManagedBy(mgr).
		For(&myappsv1.MyApp{}).
		Owns(&appsv1.Deployment{}).
		Owns(&corev1.Service{}).
		Complete(r)
}
