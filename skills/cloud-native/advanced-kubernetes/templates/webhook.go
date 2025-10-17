// Validating and Mutating Admission Webhooks
// This file demonstrates both webhook types with production-ready validation

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

// SetupWebhookWithManager registers the webhook with the manager
func (r *MyApp) SetupWebhookWithManager(mgr ctrl.Manager) error {
	return ctrl.NewWebhookManagedBy(mgr).
		For(r).
		Complete()
}

// VALIDATING WEBHOOK IMPLEMENTATION

// +kubebuilder:webhook:path=/validate-apps-example-com-v1-myapp,mutating=false,failurePolicy=fail,sideEffects=None,groups=apps.example.com,resources=myapps,verbs=create;update,versions=v1,name=vmyapp.kb.io,admissionReviewVersions=v1

var _ webhook.Validator = &MyApp{}

// ValidateCreate implements webhook.Validator for create operations
func (r *MyApp) ValidateCreate() (admission.Warnings, error) {
	myapplog.Info("validate create", "name", r.Name)

	return r.validateMyApp()
}

// ValidateUpdate implements webhook.Validator for update operations
func (r *MyApp) ValidateUpdate(old runtime.Object) (admission.Warnings, error) {
	myapplog.Info("validate update", "name", r.Name)

	oldMyApp := old.(*MyApp)
	var warnings admission.Warnings

	// Prevent scaling down below 1 replica
	if r.Spec.Size < oldMyApp.Spec.Size && r.Spec.Size < 1 {
		return nil, fmt.Errorf("cannot scale below 1 replica")
	}

	// Warn about large scale-up operations
	if r.Spec.Size > oldMyApp.Spec.Size && (r.Spec.Size-oldMyApp.Spec.Size) > 5 {
		warnings = append(warnings, "Large scale-up operation may cause resource contention")
	}

	// Prevent changing image registry
	oldRegistry := getRegistry(oldMyApp.Spec.Image)
	newRegistry := getRegistry(r.Spec.Image)
	if oldRegistry != newRegistry {
		warnings = append(warnings, "Changing image registry may cause downtime during image pull")
	}

	// Prevent changing deployment strategy with running pods
	if r.Spec.Strategy != oldMyApp.Spec.Strategy && oldMyApp.Status.ReadyReplicas > 0 {
		warnings = append(warnings, "Changing deployment strategy requires pod restart")
	}

	return warnings, r.validateMyAppUpdate(oldMyApp)
}

// ValidateDelete implements webhook.Validator for delete operations
func (r *MyApp) ValidateDelete() (admission.Warnings, error) {
	myapplog.Info("validate delete", "name", r.Name)

	// Prevent deletion of production instances
	if r.Labels["environment"] == "production" {
		return nil, fmt.Errorf("production instances cannot be deleted via API; use manual confirmation")
	}

	// Warn about data loss
	if r.Status.ReadyReplicas > 0 {
		return admission.Warnings{
			"Deleting instance with running replicas will cause service disruption",
		}, nil
	}

	return nil, nil
}

// validateMyApp performs comprehensive validation on MyApp resource
func (r *MyApp) validateMyApp() (admission.Warnings, error) {
	var allWarnings admission.Warnings
	var allErrors []string

	// Validate size is within reasonable bounds
	if r.Spec.Size > 100 {
		allWarnings = append(allWarnings, "Large replica count may consume excessive cluster resources")
	}

	// Validate image format
	if !isValidImageFormat(r.Spec.Image) {
		allErrors = append(allErrors, "image must be in format registry/name:tag (e.g., docker.io/nginx:1.25.3)")
	}

	// Validate image tag is not 'latest'
	if strings.HasSuffix(r.Spec.Image, ":latest") {
		allWarnings = append(allWarnings, "Using 'latest' tag is not recommended for production; use specific version tags")
	}

	// Validate port range
	if r.Spec.Port != 0 && (r.Spec.Port < 1024 || r.Spec.Port > 65535) {
		allErrors = append(allErrors, "port must be between 1024 and 65535")
	}

	// Cross-field validation for resources
	if r.Spec.Resources != nil {
		if err := validateResources(r.Spec.Resources); err != nil {
			allErrors = append(allErrors, err.Error())
		}
	}

	// Validate environment variables
	envNames := make(map[string]bool)
	for _, env := range r.Spec.Env {
		if env.Name == "" {
			allErrors = append(allErrors, "environment variable name cannot be empty")
		}
		if envNames[env.Name] {
			allErrors = append(allErrors, fmt.Sprintf("duplicate environment variable: %s", env.Name))
		}
		envNames[env.Name] = true
	}

	// Validate deployment strategy
	if r.Spec.Strategy != "" && r.Spec.Strategy != "RollingUpdate" && r.Spec.Strategy != "Recreate" {
		allErrors = append(allErrors, "strategy must be 'RollingUpdate' or 'Recreate'")
	}

	if len(allErrors) > 0 {
		return allWarnings, fmt.Errorf("validation failed: %v", allErrors)
	}

	return allWarnings, nil
}

// validateMyAppUpdate performs validation specific to update operations
func (r *MyApp) validateMyAppUpdate(old *MyApp) error {
	// Prevent changing immutable fields
	if r.Namespace != old.Namespace {
		return fmt.Errorf("namespace is immutable")
	}

	return nil
}

// MUTATING WEBHOOK IMPLEMENTATION

// +kubebuilder:webhook:path=/mutate-apps-example-com-v1-myapp,mutating=true,failurePolicy=fail,sideEffects=None,groups=apps.example.com,resources=myapps,verbs=create;update,versions=v1,name=mmyapp.kb.io,admissionReviewVersions=v1

var _ webhook.Defaulter = &MyApp{}

// Default implements webhook.Defaulter for setting default values
func (r *MyApp) Default() {
	myapplog.Info("default", "name", r.Name)

	// Set default port if not specified
	if r.Spec.Port == 0 {
		r.Spec.Port = 8080
		myapplog.Info("set default port", "port", 8080)
	}

	// Set default resources if not specified
	if r.Spec.Resources == nil {
		r.Spec.Resources = &ResourceRequirements{
			CPULimit:    "500m",
			MemoryLimit: "512Mi",
		}
		myapplog.Info("set default resources", "cpu", "500m", "memory", "512Mi")
	}

	// Set default deployment strategy
	if r.Spec.Strategy == "" {
		r.Spec.Strategy = "RollingUpdate"
		myapplog.Info("set default strategy", "strategy", "RollingUpdate")
	}

	// Add standard labels if not present
	if r.Labels == nil {
		r.Labels = make(map[string]string)
	}
	if _, exists := r.Labels["app.kubernetes.io/managed-by"]; !exists {
		r.Labels["app.kubernetes.io/managed-by"] = "myapp-operator"
	}
	if _, exists := r.Labels["app.kubernetes.io/name"]; !exists {
		r.Labels["app.kubernetes.io/name"] = "myapp"
	}

	// Set default size if zero
	if r.Spec.Size == 0 {
		r.Spec.Size = 1
		myapplog.Info("set default size", "size", 1)
	}

	// Add standard annotations
	if r.Annotations == nil {
		r.Annotations = make(map[string]string)
	}
	if _, exists := r.Annotations["myapp.example.com/version"]; !exists {
		r.Annotations["myapp.example.com/version"] = "v1"
	}
}

// VALIDATION HELPER FUNCTIONS

// isValidImageFormat validates container image format
func isValidImageFormat(image string) bool {
	if image == "" {
		return false
	}

	// Must contain registry/repo:tag format
	if !strings.Contains(image, "/") {
		return false
	}
	if !strings.Contains(image, ":") {
		return false
	}

	// Basic format check: registry/name:tag
	parts := strings.Split(image, "/")
	if len(parts) < 2 {
		return false
	}

	// Check tag part
	lastPart := parts[len(parts)-1]
	if !strings.Contains(lastPart, ":") {
		return false
	}

	tagParts := strings.Split(lastPart, ":")
	if len(tagParts) != 2 {
		return false
	}

	// Tag should not be empty
	if tagParts[1] == "" {
		return false
	}

	return true
}

// validateResources validates CPU and memory limits
func validateResources(res *ResourceRequirements) error {
	// Validate CPU limit format and minimum
	if res.CPULimit != "" {
		if !strings.HasSuffix(res.CPULimit, "m") {
			return fmt.Errorf("CPU limit must be in millicores format (e.g., '500m')")
		}
		cpu := strings.TrimSuffix(res.CPULimit, "m")
		var cpuVal int
		if _, err := fmt.Sscanf(cpu, "%d", &cpuVal); err != nil {
			return fmt.Errorf("invalid CPU limit format: %s", res.CPULimit)
		}
		if cpuVal < 100 {
			return fmt.Errorf("CPU limit must be at least 100m")
		}
		if cpuVal > 8000 {
			return fmt.Errorf("CPU limit exceeds maximum of 8000m (8 cores)")
		}
	}

	// Validate memory limit format and minimum
	if res.MemoryLimit != "" {
		if !strings.HasSuffix(res.MemoryLimit, "Mi") {
			return fmt.Errorf("memory limit must be in megabytes format (e.g., '512Mi')")
		}
		mem := strings.TrimSuffix(res.MemoryLimit, "Mi")
		var memVal int
		if _, err := fmt.Sscanf(mem, "%d", &memVal); err != nil {
			return fmt.Errorf("invalid memory limit format: %s", res.MemoryLimit)
		}
		if memVal < 64 {
			return fmt.Errorf("memory limit must be at least 64Mi")
		}
		if memVal > 16384 {
			return fmt.Errorf("memory limit exceeds maximum of 16384Mi (16Gi)")
		}
	}

	return nil
}

// getRegistry extracts registry from image string
func getRegistry(image string) string {
	parts := strings.Split(image, "/")
	if len(parts) > 0 {
		return parts[0]
	}
	return ""
}
