# ML/AI Standards

> 📚 See also: [Unified Software Development Standards](./UNIFIED_STANDARDS.md)


**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** ML

---

## Table of Contents

1. [MLOps Principles](#1-mlops-principles)
2. [Model Development Lifecycle](#2-model-development-lifecycle)
3. [Model Deployment and Serving](#3-model-deployment-and-serving)
4. [Model Monitoring and Maintenance](#4-model-monitoring-and-maintenance)
5. [AI Ethics and Responsible AI](#5-ai-ethics-and-responsible-ai)
6. [Data Pipeline for ML](#6-data-pipeline-for-ml)
7. [Experimentation and Tracking](#7-experimentation-and-tracking)
8. [Implementation Checklist](#8-implementation-checklist)

---

## Overview

This standard provides comprehensive guidelines for machine learning and AI system development, deployment, and operations. It ensures reproducibility, scalability, and responsible AI practices across all ML/AI implementations.

## 1. MLOps Principles

### 1.1 Core Principles **[REQUIRED]**

```yaml
# MLOps configuration
mlops:
  principles:
    - reproducibility: "All experiments and models must be reproducible"
    - automation: "Automate training, testing, and deployment pipelines"
    - monitoring: "Continuous monitoring of model performance and drift"
    - versioning: "Version control for code, data, and models"
    - collaboration: "Enable cross-functional team collaboration"
```

### 1.2 Infrastructure as Code **[REQUIRED]**

```python
# Infrastructure setup using Terraform
resource "aws_sagemaker_model" "ml_model" {
  name               = "${var.model_name}-${var.environment}"
  execution_role_arn = aws_iam_role.sagemaker_role.arn

  primary_container {
    image          = var.container_image
    model_data_url = "s3://${var.model_bucket}/${var.model_path}"
    environment = {
      MODEL_SERVER_TIMEOUT = "3600"
      MODEL_SERVER_WORKERS = "4"
    }
  }
}
```

## 2. Model Development Lifecycle

### 2.1 Development Standards **[REQUIRED]**

```python
from dataclasses import dataclass
from typing import Dict, Any, Optional
import mlflow

@dataclass
class ModelConfig:
    """Standard model configuration."""
    name: str
    version: str
    framework: str
    hyperparameters: Dict[str, Any]
    metrics: Dict[str, float]

class MLModel:
    """Base class for all ML models."""

    def __init__(self, config: ModelConfig):
        self.config = config
        self.model = None
        mlflow.set_experiment(config.name)

    def train(self, X_train, y_train, X_val, y_val):
        """Standard training interface."""
        with mlflow.start_run():
            # Log parameters
            mlflow.log_params(self.config.hyperparameters)

            # Train model
            self.model = self._train_impl(X_train, y_train, X_val, y_val)

            # Evaluate and log metrics
            metrics = self.evaluate(X_val, y_val)
            mlflow.log_metrics(metrics)

            # Save model
            mlflow.sklearn.log_model(self.model, "model")

    def predict(self, X):
        """Standard prediction interface."""
        return self.model.predict(X)
```

### 2.2 Feature Engineering Pipeline **[RECOMMENDED]**

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest

def create_feature_pipeline():
    """Create standardized feature engineering pipeline."""
    return Pipeline([
        ('scaler', StandardScaler()),
        ('feature_selection', SelectKBest(k=20)),
        ('custom_transforms', CustomFeatureTransformer())
    ])

# Feature store integration
class FeatureStore:
    """Centralized feature management."""

    def register_feature(self, name: str, compute_fn, description: str):
        """Register a new feature computation."""
        return {
            'name': name,
            'version': self._get_next_version(name),
            'compute_fn': compute_fn,
            'description': description,
            'created_at': datetime.utcnow()
        }
```

## 3. Model Deployment and Serving

### 3.1 Deployment Patterns **[REQUIRED]**

```python
# Model serving with FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib

app = FastAPI(title="ML Model Service")

class PredictionRequest(BaseModel):
    features: List[float]

class PredictionResponse(BaseModel):
    prediction: float
    confidence: Optional[float]
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        model = load_model()
        prediction = model.predict([request.features])[0]

        return PredictionResponse(
            prediction=prediction,
            confidence=calculate_confidence(prediction),
            model_version=MODEL_VERSION
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 3.2 A/B Testing Framework **[RECOMMENDED]**

```python
class ABTestController:
    """Control A/B testing for model deployments."""

    def __init__(self, models: Dict[str, Any], traffic_split: Dict[str, float]):
        self.models = models
        self.traffic_split = traffic_split

    def route_request(self, request_id: str) -> str:
        """Route request to appropriate model version."""
        hash_value = hashlib.md5(request_id.encode()).hexdigest()
        bucket = int(hash_value[:8], 16) / (16**8)

        cumulative = 0
        for model_version, split in self.traffic_split.items():
            cumulative += split
            if bucket < cumulative:
                return model_version
        return list(self.models.keys())[-1]
```

## 4. Model Monitoring and Maintenance

### 4.1 Performance Monitoring **[REQUIRED]**

```python
from prometheus_client import Counter, Histogram, Gauge

# Define metrics
prediction_counter = Counter('ml_predictions_total', 'Total predictions', ['model', 'version'])
prediction_latency = Histogram('ml_prediction_duration_seconds', 'Prediction latency')
model_drift_score = Gauge('ml_model_drift_score', 'Model drift score', ['model'])

class ModelMonitor:
    """Monitor model performance in production."""

    def __init__(self, model_name: str, baseline_metrics: Dict[str, float]):
        self.model_name = model_name
        self.baseline_metrics = baseline_metrics

    def log_prediction(self, features, prediction, ground_truth=None):
        """Log prediction for monitoring."""
        prediction_counter.labels(model=self.model_name, version=MODEL_VERSION).inc()

        if ground_truth is not None:
            self._update_performance_metrics(prediction, ground_truth)

    def check_data_drift(self, current_data, reference_data):
        """Detect data drift using statistical tests."""
        from scipy.stats import ks_2samp

        drift_scores = {}
        for feature in current_data.columns:
            _, p_value = ks_2samp(
                reference_data[feature],
                current_data[feature]
            )
            drift_scores[feature] = 1 - p_value

        return drift_scores
```

## 5. AI Ethics and Responsible AI

### 5.1 Fairness and Bias Detection **[REQUIRED]**

```python
class FairnessAnalyzer:
    """Analyze model fairness across protected attributes."""

    def demographic_parity(self, y_pred, sensitive_attribute):
        """Check demographic parity."""
        groups = sensitive_attribute.unique()
        acceptance_rates = {}

        for group in groups:
            mask = sensitive_attribute == group
            acceptance_rates[group] = y_pred[mask].mean()

        return {
            'acceptance_rates': acceptance_rates,
            'max_difference': max(acceptance_rates.values()) - min(acceptance_rates.values())
        }

    def equal_opportunity(self, y_true, y_pred, sensitive_attribute):
        """Check equal opportunity (TPR equality)."""
        from sklearn.metrics import confusion_matrix

        tpr_by_group = {}
        for group in sensitive_attribute.unique():
            mask = sensitive_attribute == group
            tn, fp, fn, tp = confusion_matrix(y_true[mask], y_pred[mask]).ravel()
            tpr_by_group[group] = tp / (tp + fn) if (tp + fn) > 0 else 0

        return tpr_by_group
```

### 5.2 Model Interpretability **[RECOMMENDED]**

```python
import shap

class ModelInterpreter:
    """Provide model interpretability."""

    def __init__(self, model, X_train):
        self.model = model
        self.explainer = shap.Explainer(model, X_train)

    def explain_prediction(self, X_instance):
        """Explain individual prediction."""
        shap_values = self.explainer(X_instance)
        return {
            'base_value': self.explainer.expected_value,
            'shap_values': shap_values.values,
            'feature_names': X_instance.columns.tolist()
        }
```

## 6. Data Pipeline for ML

### 6.1 Data Validation **[REQUIRED]**

```python
from great_expectations import DataContext

class MLDataValidator:
    """Validate data for ML pipelines."""

    def __init__(self):
        self.context = DataContext()

    def validate_training_data(self, df, expectation_suite_name):
        """Validate training data against expectations."""
        batch = self.context.get_batch(df, expectation_suite_name)
        results = self.context.run_validation_operator(
            "action_list_operator",
            assets_to_validate=[batch]
        )
        return results

    def create_expectations(self, df):
        """Auto-generate data expectations."""
        suite = self.context.create_expectation_suite("ml_data_suite")

        # Add expectations
        suite.expect_table_row_count_to_be_between(min_value=1000)
        suite.expect_column_values_to_not_be_null("target")
        suite.expect_column_values_to_be_between("feature_1", 0, 100)

        return suite
```

## 7. Experimentation and Tracking

### 7.1 Experiment Tracking **[REQUIRED]**

```python
import wandb
from typing import Dict, Any

class ExperimentTracker:
    """Track ML experiments systematically."""

    def __init__(self, project_name: str):
        self.project_name = project_name
        wandb.init(project=project_name)

    def log_experiment(self, config: Dict[str, Any], metrics: Dict[str, float]):
        """Log experiment configuration and results."""
        # Log hyperparameters
        wandb.config.update(config)

        # Log metrics
        wandb.log(metrics)

        # Log model artifacts
        wandb.save('model.pkl')

    def log_dataset_info(self, dataset_stats: Dict[str, Any]):
        """Log dataset information."""
        wandb.log({
            "dataset/size": dataset_stats['size'],
            "dataset/features": dataset_stats['n_features'],
            "dataset/class_distribution": dataset_stats['class_distribution']
        })
```

### 7.2 Hyperparameter Optimization **[RECOMMENDED]**

```python
from optuna import create_study

def optimize_hyperparameters(objective_fn, n_trials=100):
    """Optimize hyperparameters using Bayesian optimization."""
    study = create_study(
        direction="maximize",
        pruner=optuna.pruners.MedianPruner()
    )

    study.optimize(objective_fn, n_trials=n_trials)

    return {
        'best_params': study.best_params,
        'best_value': study.best_value,
        'best_trial': study.best_trial
    }
```

## 8. Implementation Checklist

### ML Project Checklist

- [ ] **Data Pipeline**
  - [ ] Data validation implemented
  - [ ] Feature engineering pipeline defined
  - [ ] Data versioning in place

- [ ] **Model Development**
  - [ ] Experiment tracking configured
  - [ ] Model versioning implemented
  - [ ] Hyperparameter optimization setup

- [ ] **Model Deployment**
  - [ ] Model serving API created
  - [ ] A/B testing framework ready
  - [ ] Rollback strategy defined

- [ ] **Monitoring**
  - [ ] Performance metrics tracked
  - [ ] Data drift detection enabled
  - [ ] Alerting configured

- [ ] **Ethics & Compliance**
  - [ ] Bias detection implemented
  - [ ] Model interpretability available
  - [ ] Privacy requirements met

- [ ] **Documentation**
  - [ ] Model card created
  - [ ] API documentation complete
  - [ ] Training pipeline documented

### Best Practices Summary

1. **Always version** code, data, and models
2. **Automate** training and deployment pipelines
3. **Monitor** model performance and data drift continuously
4. **Document** experiments, decisions, and model behavior
5. **Test** model robustness and edge cases
6. **Ensure** fairness and interpretability
7. **Implement** gradual rollout strategies
8. **Maintain** reproducibility across environments

## Related Standards

### Core Dependencies

#### Data Engineering Standards

- **[DATA_ENGINEERING_STANDARDS.md](./DATA_ENGINEERING_STANDARDS.md)** - Data pipeline design for ML workflows
- **Cross-reference**: Use DE:pipelines section for ML data pipeline architecture
- **Integration**: Feature engineering and data quality standards for ML

#### Cloud Native Standards

- **[CLOUD_NATIVE_STANDARDS.md](./CLOUD_NATIVE_STANDARDS.md)** - Container orchestration for ML workloads
- **Cross-reference**: Use CN:kubernetes section for ML model serving infrastructure
- **Integration**: Scalable ML training and inference deployment patterns

#### Security Standards

- **[MODERN_SECURITY_STANDARDS.md](./MODERN_SECURITY_STANDARDS.md)** - ML model and data security
- **Cross-reference**: Use SEC:encryption section for model and data protection
- **Integration**: Privacy-preserving ML and secure model serving

#### Observability Standards

- **[OBSERVABILITY_STANDARDS.md](./OBSERVABILITY_STANDARDS.md)** - ML model monitoring and performance tracking
- **Cross-reference**: Use OBS:metrics section for ML performance monitoring setup
- **Integration**: Model drift detection and ML operations dashboards

### Supporting Standards

#### Testing Standards

- **[TESTING_STANDARDS.md](./TESTING_STANDARDS.md)** - ML model testing and validation
- **Cross-reference**: Use TS:integration section for ML pipeline testing patterns
- **Integration**: Model validation, A/B testing, and integration testing for ML

#### Coding Standards

- **[CODING_STANDARDS.md](./CODING_STANDARDS.md)** - ML code organization and quality
- **Cross-reference**: Use CS:patterns section for ML project structure
- **Integration**: Code quality and documentation standards for ML projects

#### Database Standards

- **[DATABASE_STANDARDS.md](./DATABASE_STANDARDS.md)** - Feature store and ML metadata management
- **Cross-reference**: Use DBS:data-modeling section for feature store design
- **Integration**: ML metadata storage and feature engineering data patterns

---

*This standard is maintained by the ML/AI Engineering team and reviewed quarterly.*
