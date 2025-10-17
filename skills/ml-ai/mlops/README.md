# MLOps Skill

Comprehensive MLOps skill covering the complete ML lifecycle from training to production deployment, monitoring, and continuous improvement.

## Contents

- `SKILL.md` - Complete skill documentation with 3 levels
- `templates/` - Production-ready templates
  - `mlflow-project/` - Complete MLflow project with tracking, validation, and serving
  - `kubeflow-pipeline.yaml` - End-to-end Kubeflow pipeline definition
  - `model-serving-config.yaml` - TorchServe and TensorFlow Serving configurations
  - `feature-store.py` - Feast feature store implementation
  - `ab-testing-framework.py` - Multi-Armed Bandit A/B testing framework
- `scripts/` - Utility scripts
  - `drift-detection.py` - Comprehensive drift detection system

## Quick Start

### 1. MLflow Project

```bash
cd templates/mlflow-project
mlflow run . -P data_path=data/train.csv
```

### 2. Feature Store

```python
from templates.feature_store import FeatureStoreManager

fs = FeatureStoreManager()
features = fs.get_online_features(
    entity_rows=[{"user_id": 123}],
    feature_refs=["user_features:transaction_count_7d"]
)
```

### 3. Drift Detection

```python
from scripts.drift_detection import DriftDetector

detector = DriftDetector(reference_data, feature_types)
drift_results = detector.detect_drift(production_data)
```

### 4. A/B Testing

```python
from templates.ab_testing_framework import ABTestingFramework

framework = ABTestingFramework(
    model_ids=['model_v1', 'model_v2'],
    strategy='thompson'
)
selected_model = framework.select_model()
```

## Key Concepts

### ML Lifecycle

1. **Data Collection & Validation** - Version data, validate quality
2. **Feature Engineering** - Feature stores, transformations
3. **Model Training** - Experiment tracking, hyperparameter tuning
4. **Model Evaluation** - Metrics, validation gates
5. **Model Deployment** - Batch, real-time, streaming inference
6. **Model Monitoring** - Drift detection, performance tracking
7. **Model Retraining** - Automated triggers, continuous improvement

### MLOps Tools

- **Experiment Tracking**: MLflow, Weights & Biases
- **Pipelines**: Kubeflow, Apache Airflow
- **Feature Stores**: Feast, Tecton
- **Model Serving**: TorchServe, TensorFlow Serving
- **Monitoring**: Evidently AI, WhyLabs
- **Data Versioning**: DVC, LakeFS

## Integration Patterns

### CI/CD for ML

```yaml
# GitHub Actions example
- name: Train Model
  run: mlflow run . --experiment-name ci-training

- name: Validate Model
  run: python validate.py --threshold 0.90

- name: Deploy to Staging
  if: success()
  run: kubectl apply -f deployment-staging.yaml
```

### Production Monitoring

```python
# Prometheus metrics
from prometheus_client import Gauge

MODEL_ACCURACY = Gauge('model_accuracy', 'Current model accuracy')
DATA_DRIFT_SCORE = Gauge('data_drift_score', 'Drift severity')

# Update metrics
MODEL_ACCURACY.set(current_accuracy)
DATA_DRIFT_SCORE.set(drift_score)
```

## Best Practices

1. **Version Everything**: Code, data, models, configurations
2. **Automate Testing**: Data validation, model evaluation, integration tests
3. **Monitor Continuously**: Performance, drift, system health
4. **Document Thoroughly**: Model cards, experiment logs, deployment guides
5. **Enable Rollback**: Quick rollback to previous model versions
6. **Implement Gates**: Performance thresholds before production deployment

## Resources

- MLflow Documentation: https://mlflow.org/docs/
- Kubeflow: https://www.kubeflow.org/docs/
- Feast: https://docs.feast.dev/
- "Designing Machine Learning Systems" by Chip Huyen

## Next Steps

1. Complete the Level 1 Quick Reference
2. Work through Level 2 Implementation Guide examples
3. Build end-to-end pipeline with provided templates
4. Implement monitoring and drift detection
5. Set up A/B testing for model comparison

---

**License**: MIT
**Version**: 1.0.0
**Last Updated**: 2025-01-17
