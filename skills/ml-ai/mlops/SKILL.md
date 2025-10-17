---
name: mlops
category: ml-ai
difficulty: advanced
estimated_time: 60 minutes
prerequisites:
  - machine-learning
  - docker-containers
  - kubernetes-basics
learning_outcomes:
  - Design end-to-end ML pipelines from training to production
  - Implement model versioning, experiment tracking, and monitoring
  - Deploy ML models with batch, real-time, and streaming strategies
  - Detect and respond to model drift in production
  - Build reproducible ML workflows with MLOps toolchains
related_skills:
  - data-engineering
  - ci-cd-pipelines
  - observability
tags:
  - mlops
  - machine-learning
  - model-deployment
  - ml-pipelines
  - model-monitoring
  - mlflow
  - kubeflow
version: 1.0.0
last_updated: 2025-01-17
---

# MLOps (Machine Learning Operations)

## Overview

MLOps brings DevOps principles to machine learning workflows, enabling reliable, scalable, and reproducible ML systems in production. It covers the entire ML lifecycle from experimentation to deployment and monitoring.

**Core Principles:**

- **Reproducibility**: Version everything (code, data, models, environments)
- **Automation**: Automate training, testing, deployment pipelines
- - **Monitoring**: Track model performance, data drift, system health
- **Collaboration**: Bridge data scientists, engineers, and operations
- **Governance**: Ensure model compliance, explainability, and auditing

---

## Level 1: Quick Reference

### ML Lifecycle Stages

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Data      │────▶│  Training   │────▶│ Deployment  │────▶│ Monitoring  │
│ Collection  │     │ & Experiment│     │  & Serving  │     │ & Retraining│
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │                    │
      │                    │                    │                    │
      ▼                    ▼                    ▼                    ▼
  Versioning        Tracking             Inference          Drift Detection
  Validation        Reproducibility      Scalability        Performance Decay
  Feature Eng.      Hyperparameters      A/B Testing        Alerts & Triggers
```

### MLOps vs Traditional DevOps

| Aspect | Traditional DevOps | MLOps |
|--------|-------------------|-------|
| **Artifacts** | Code, binaries | Code + Data + Models + Features |
| **Testing** | Unit, integration tests | Data validation + Model evaluation + Inference tests |
| **Deployment** | Deploy once, stable | Continuous retraining, model decay |
| **Monitoring** | Logs, metrics, traces | + Data drift, concept drift, model performance |
| **Versioning** | Git for code | Git + DVC for data + Model registry |
| **Reproducibility** | Dockerfile, env vars | + Data versions, random seeds, feature pipelines |

### Essential MLOps Checklist

**Experimentation & Development:**

- [ ] Experiment tracking (MLflow, Weights & Biases, Neptune.ai)
- [ ] Notebook versioning and parameterization (Papermill)
- [ ] Feature engineering pipelines with versioning
- [ ] Data quality checks (Great Expectations)
- [ ] Model versioning and registry

**Training Pipelines:**

- [ ] Automated data validation before training
- [ ] Reproducible training environments (Docker, Conda)
- [ ] Hyperparameter tuning (Optuna, Ray Tune)
- [ ] Distributed training support (Horovod, PyTorch DDP)
- [ ] Model evaluation metrics logged and tracked

**Deployment & Serving:**

- [ ] Model serving infrastructure (TorchServe, TensorFlow Serving, Seldon)
- [ ] Batch prediction pipelines for offline inference
- [ ] Real-time inference APIs with latency SLAs
- [ ] Canary deployments and A/B testing
- [ ] Shadow mode for model validation

**Monitoring & Maintenance:**

- [ ] Data drift detection (statistical tests, KL divergence)
- [ ] Concept drift detection (model performance degradation)
- [ ] Prediction monitoring and alerting
- [ ] Model performance dashboards
- [ ] Automated retraining triggers
- [ ] Model rollback procedures

### Quick Commands

```bash
# MLflow - Track experiments
mlflow ui --host 0.0.0.0 --port 5000
mlflow run . -P alpha=0.5

# Kubeflow - Deploy pipeline
kfp pipeline create --pipeline-name my_pipeline pipeline.yaml
kfp run submit --experiment-name exp1 --pipeline-id <id>

# DVC - Version data
dvc add data/train.csv
dvc push
dvc pull

# Model serving - TorchServe
torch-model-archiver --model-name my_model --version 1.0 --serialized-file model.pt
torchserve --start --model-store ./model_store
curl -X POST http://localhost:8080/predictions/my_model -T input.json

# Feature store - Feast
feast apply
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

### Common Patterns

**1. Experiment Tracking**

```python
import mlflow

with mlflow.start_run():
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_metric("accuracy", 0.95)
    mlflow.sklearn.log_model(model, "model")
```

**2. Model Versioning**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
result = client.create_model_version(
    name="my_model",
    source="runs:/abc123/model",
    run_id="abc123"
)
```

**3. Model Serving**

```python
# Load model from registry
model = mlflow.pyfunc.load_model(f"models:/my_model/production")

# Inference
predictions = model.predict(input_data)
```

**4. Drift Detection**

```python
from scipy.stats import ks_2samp

# Compare training and production distributions
statistic, p_value = ks_2samp(train_distribution, production_distribution)
if p_value < 0.05:
    trigger_alert("Data drift detected")
```

---

## Level 2: Implementation Guide

### 1. ML Model Lifecycle Management

#### Training Phase

**Reproducible Training Environment:**

```python
# training/train.py
import os
import random
import numpy as np
import torch
import mlflow
from mlflow.models.signature import infer_signature

def set_seed(seed=42):
    """Ensure reproducibility across runs."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)

def train_model(config):
    set_seed(config.get('seed', 42))

    # Log environment
    mlflow.log_param("python_version", os.sys.version)
    mlflow.log_param("pytorch_version", torch.__version__)

    # Data versioning reference
    mlflow.log_param("data_version", config['data_version'])

    # Training loop
    for epoch in range(config['epochs']):
        train_loss = train_epoch(model, train_loader)
        val_loss, val_metrics = validate(model, val_loader)

        # Log metrics per epoch
        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "val_accuracy": val_metrics['accuracy']
        }, step=epoch)

        # Checkpoint best model
        if val_loss < best_loss:
            best_loss = val_loss
            torch.save(model.state_dict(), "best_model.pth")

    # Log final model with signature
    signature = infer_signature(sample_input, model(sample_input))
    mlflow.pytorch.log_model(
        model,
        "model",
        signature=signature,
        registered_model_name="my_model"
    )
```

**Hyperparameter Optimization:**

```python
import optuna
from optuna.integration.mlflow import MLflowCallback

def objective(trial):
    # Suggest hyperparameters
    lr = trial.suggest_loguniform('lr', 1e-5, 1e-1)
    batch_size = trial.suggest_categorical('batch_size', [16, 32, 64])

    with mlflow.start_run(nested=True):
        model = train_model(lr=lr, batch_size=batch_size)
        val_accuracy = evaluate(model)

        mlflow.log_params(trial.params)
        mlflow.log_metric("val_accuracy", val_accuracy)

        return val_accuracy

# Run optimization
study = optuna.create_study(direction="maximize")
mlflc = MLflowCallback(tracking_uri="http://localhost:5000")
study.optimize(objective, n_trials=50, callbacks=[mlflc])
```

#### Model Versioning

**Model Registry Pattern:**

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model
model_uri = f"runs:/{run_id}/model"
mv = client.create_model_version(
    name="fraud_detection_model",
    source=model_uri,
    run_id=run_id,
    description="XGBoost model trained on 2025-01 data"
)

# Transition to staging
client.transition_model_version_stage(
    name="fraud_detection_model",
    version=mv.version,
    stage="Staging"
)

# Add metadata
client.set_model_version_tag(
    name="fraud_detection_model",
    version=mv.version,
    key="validation_status",
    value="passed"
)

# Promote to production after validation
client.transition_model_version_stage(
    name="fraud_detection_model",
    version=mv.version,
    stage="Production",
    archive_existing_versions=True
)
```

### 2. Feature Engineering & Feature Stores

**Feature Store with Feast:**

```python
# feature_repo/features.py
from feast import Entity, Feature, FeatureView, FileSource, ValueType
from feast.types import Float32, Int64
from datetime import timedelta

# Define entity
user = Entity(
    name="user_id",
    value_type=ValueType.INT64,
    description="User identifier"
)

# Define data source
user_features_source = FileSource(
    path="data/user_features.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp"
)

# Define feature view
user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=7),
    features=[
        Feature(name="transaction_count_7d", dtype=Int64),
        Feature(name="avg_transaction_amount", dtype=Float32),
        Feature(name="account_age_days", dtype=Int64)
    ],
    online=True,
    source=user_features_source,
    tags={"team": "fraud_detection"}
)
```

**Feature Retrieval in Training:**

```python
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo/")

# Historical features for training
entity_df = pd.DataFrame({
    "user_id": [1, 2, 3],
    "event_timestamp": [
        datetime(2025, 1, 1),
        datetime(2025, 1, 2),
        datetime(2025, 1, 3)
    ]
})

training_df = store.get_historical_features(
    entity_df=entity_df,
    features=[
        "user_features:transaction_count_7d",
        "user_features:avg_transaction_amount",
        "user_features:account_age_days"
    ]
).to_df()

# Online features for inference
online_features = store.get_online_features(
    features=[
        "user_features:transaction_count_7d",
        "user_features:avg_transaction_amount"
    ],
    entity_rows=[{"user_id": 123}]
).to_dict()
```

### 3. Model Serving Strategies

#### Batch Prediction Pipeline

**Apache Airflow DAG:**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import mlflow

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

def load_model():
    """Load production model from registry."""
    mlflow.set_tracking_uri("http://mlflow:5000")
    model = mlflow.pyfunc.load_model("models:/my_model/Production")
    return model

def batch_predict(**context):
    """Run batch predictions on S3 data."""
    model = load_model()

    # Load data from S3
    s3_hook = S3Hook(aws_conn_id='aws_default')
    data = s3_hook.read_key(
        key=f"input/data_{context['ds']}.parquet",
        bucket_name="ml-batch-data"
    )
    df = pd.read_parquet(io.BytesIO(data))

    # Predict
    predictions = model.predict(df)
    df['prediction'] = predictions

    # Write results back to S3
    output_buffer = io.BytesIO()
    df.to_parquet(output_buffer, index=False)
    s3_hook.load_bytes(
        output_buffer.getvalue(),
        key=f"output/predictions_{context['ds']}.parquet",
        bucket_name="ml-batch-data",
        replace=True
    )

with DAG(
    'batch_prediction_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False
) as dag:

    predict_task = PythonOperator(
        task_id='batch_predict',
        python_callable=batch_predict,
        provide_context=True
    )
```

#### Real-Time Inference API

**FastAPI Model Serving:**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow
import numpy as np
from prometheus_client import Counter, Histogram, generate_latest
import time

app = FastAPI(title="Model Inference API")

# Metrics
PREDICTION_COUNTER = Counter('predictions_total', 'Total predictions')
PREDICTION_LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
ERROR_COUNTER = Counter('prediction_errors_total', 'Total prediction errors')

# Load model at startup
model = None

@app.on_event("startup")
async def load_model():
    global model
    mlflow.set_tracking_uri("http://mlflow:5000")
    model = mlflow.pyfunc.load_model("models:/my_model/Production")

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    prediction: float
    model_version: str
    latency_ms: float

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    start_time = time.time()

    try:
        # Convert to numpy array
        input_data = np.array(request.features).reshape(1, -1)

        # Predict
        prediction = model.predict(input_data)[0]

        # Metrics
        latency = (time.time() - start_time) * 1000
        PREDICTION_COUNTER.inc()
        PREDICTION_LATENCY.observe(latency / 1000)

        return PredictionResponse(
            prediction=float(prediction),
            model_version="1.0",
            latency_ms=latency
        )
    except Exception as e:
        ERROR_COUNTER.inc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

#### Streaming Inference

**Kafka Consumer with Model:**

```python
from kafka import KafkaConsumer, KafkaProducer
import json
import mlflow

# Load model
model = mlflow.pyfunc.load_model("models:/my_model/Production")

# Kafka setup
consumer = KafkaConsumer(
    'input_events',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    group_id='ml_inference_group'
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Process stream
for message in consumer:
    event = message.value

    try:
        # Extract features
        features = extract_features(event)

        # Predict
        prediction = model.predict(features)

        # Publish result
        result = {
            'event_id': event['id'],
            'prediction': float(prediction[0]),
            'timestamp': time.time()
        }
        producer.send('predictions', value=result)

    except Exception as e:
        logger.error(f"Prediction error: {e}")
        continue
```

### 4. Model Monitoring & Drift Detection

#### Data Drift Detection

**Statistical Testing Approach:**

```python
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency
from typing import Dict, Tuple

class DriftDetector:
    def __init__(self, reference_data: np.ndarray, threshold: float = 0.05):
        self.reference_data = reference_data
        self.threshold = threshold

    def detect_numerical_drift(self, current_data: np.ndarray) -> Dict:
        """Detect drift in numerical features using KS test."""
        drifts = {}

        for col_idx in range(self.reference_data.shape[1]):
            ref_col = self.reference_data[:, col_idx]
            curr_col = current_data[:, col_idx]

            # Kolmogorov-Smirnov test
            statistic, p_value = ks_2samp(ref_col, curr_col)

            drifts[f'feature_{col_idx}'] = {
                'statistic': statistic,
                'p_value': p_value,
                'drift_detected': p_value < self.threshold,
                'severity': self._compute_severity(statistic)
            }

        return drifts

    def detect_categorical_drift(self,
                                 ref_counts: Dict,
                                 curr_counts: Dict) -> Dict:
        """Detect drift in categorical features using Chi-square test."""
        # Align categories
        all_categories = set(ref_counts.keys()) | set(curr_counts.keys())
        ref_freq = [ref_counts.get(cat, 0) for cat in all_categories]
        curr_freq = [curr_counts.get(cat, 0) for cat in all_categories]

        # Chi-square test
        contingency_table = [ref_freq, curr_freq]
        chi2, p_value, dof, expected = chi2_contingency(contingency_table)

        return {
            'chi2_statistic': chi2,
            'p_value': p_value,
            'drift_detected': p_value < self.threshold,
            'new_categories': list(set(curr_counts.keys()) - set(ref_counts.keys()))
        }

    def _compute_severity(self, statistic: float) -> str:
        if statistic < 0.1:
            return "low"
        elif statistic < 0.3:
            return "medium"
        else:
            return "high"
```

#### Concept Drift Detection

**Performance-Based Monitoring:**

```python
from collections import deque
import numpy as np

class ConceptDriftDetector:
    def __init__(self, window_size: int = 1000, sensitivity: float = 2.0):
        self.window_size = window_size
        self.sensitivity = sensitivity
        self.performance_history = deque(maxlen=window_size)
        self.baseline_mean = None
        self.baseline_std = None

    def set_baseline(self, baseline_performance: list):
        """Set baseline from historical performance."""
        self.baseline_mean = np.mean(baseline_performance)
        self.baseline_std = np.std(baseline_performance)

    def update(self, current_performance: float) -> Dict:
        """Update with new performance and detect drift."""
        self.performance_history.append(current_performance)

        if len(self.performance_history) < 100:
            return {'drift_detected': False, 'message': 'Collecting data'}

        # Compute current statistics
        current_mean = np.mean(self.performance_history)
        current_std = np.std(self.performance_history)

        # Z-score based detection
        if self.baseline_mean is not None:
            z_score = (current_mean - self.baseline_mean) / self.baseline_std
            drift_detected = abs(z_score) > self.sensitivity

            return {
                'drift_detected': drift_detected,
                'current_mean': current_mean,
                'baseline_mean': self.baseline_mean,
                'z_score': z_score,
                'performance_drop': ((self.baseline_mean - current_mean) /
                                    self.baseline_mean * 100)
            }

        return {'drift_detected': False}
```

#### Production Monitoring Dashboard

**Prometheus Metrics + Grafana:**

```python
from prometheus_client import Gauge, Counter, Histogram, start_http_server
import threading

# Define metrics
MODEL_ACCURACY = Gauge('model_accuracy', 'Current model accuracy')
PREDICTION_DISTRIBUTION = Histogram('prediction_distribution',
                                   'Distribution of predictions')
DATA_DRIFT_SCORE = Gauge('data_drift_score', 'Data drift severity score')
CONCEPT_DRIFT_ALERT = Gauge('concept_drift_alert', 'Concept drift detected (0/1)')

class ModelMonitor:
    def __init__(self, drift_detector: DriftDetector,
                 concept_detector: ConceptDriftDetector):
        self.drift_detector = drift_detector
        self.concept_detector = concept_detector

        # Start Prometheus server
        start_http_server(8000)

    def monitor_batch(self, predictions: np.ndarray,
                     actual: np.ndarray,
                     features: np.ndarray):
        """Monitor a batch of predictions."""

        # Accuracy
        accuracy = (predictions == actual).mean()
        MODEL_ACCURACY.set(accuracy)

        # Prediction distribution
        for pred in predictions:
            PREDICTION_DISTRIBUTION.observe(pred)

        # Data drift
        drift_results = self.drift_detector.detect_numerical_drift(features)
        max_drift = max(d['statistic'] for d in drift_results.values())
        DATA_DRIFT_SCORE.set(max_drift)

        # Concept drift
        concept_result = self.concept_detector.update(accuracy)
        if concept_result['drift_detected']:
            CONCEPT_DRIFT_ALERT.set(1)
            self._trigger_retraining_alert(concept_result)
        else:
            CONCEPT_DRIFT_ALERT.set(0)

    def _trigger_retraining_alert(self, drift_info: Dict):
        """Send alert for model retraining."""
        # Integrate with alerting system (PagerDuty, Slack, etc.)
        alert_message = f"""
        ⚠️ Concept Drift Detected!

        Current Accuracy: {drift_info['current_mean']:.3f}
        Baseline Accuracy: {drift_info['baseline_mean']:.3f}
        Performance Drop: {drift_info['performance_drop']:.2f}%

        Action Required: Trigger model retraining pipeline.
        """
        # send_alert(alert_message)
```

### 5. ML Pipelines & Orchestration

#### Kubeflow Pipelines

**Pipeline Definition:**

```python
from kfp import dsl
from kfp import compiler

@dsl.component
def load_data(data_path: str) -> dsl.OutputPath(str):
    """Load and validate data."""
    import pandas as pd
    from great_expectations.dataset import PandasDataset

    # Load data
    df = pd.read_parquet(data_path)

    # Validate with Great Expectations
    dataset = PandasDataset(df)
    assert dataset.expect_column_values_to_not_be_null('target').success
    assert dataset.expect_column_values_to_be_between('feature1', 0, 100).success

    output_path = '/tmp/validated_data.parquet'
    df.to_parquet(output_path)
    return output_path

@dsl.component
def train_model(data_path: str,
                learning_rate: float,
                epochs: int) -> dsl.OutputPath(str):
    """Train model with MLflow tracking."""
    import mlflow
    import torch

    mlflow.set_tracking_uri("http://mlflow-service:5000")

    with mlflow.start_run():
        model = create_model()
        train_model(model, data_path, learning_rate, epochs)

        # Log model
        mlflow.pytorch.log_model(model, "model")

        # Return model URI
        return mlflow.get_artifact_uri("model")

@dsl.component
def evaluate_model(model_path: str, test_data_path: str) -> dict:
    """Evaluate model on test set."""
    import mlflow

    model = mlflow.pytorch.load_model(model_path)
    test_data = load_data(test_data_path)

    metrics = evaluate(model, test_data)
    return metrics

@dsl.component
def deploy_model(model_path: str, metrics: dict, threshold: float = 0.90):
    """Deploy model if metrics meet threshold."""
    if metrics['accuracy'] >= threshold:
        # Register and promote model
        client = mlflow.tracking.MlflowClient()
        model_version = client.create_model_version(
            name="production_model",
            source=model_path,
            run_id=mlflow.active_run().info.run_id
        )

        client.transition_model_version_stage(
            name="production_model",
            version=model_version.version,
            stage="Production"
        )
        print(f"Deployed model version {model_version.version}")
    else:
        raise ValueError(f"Model accuracy {metrics['accuracy']} below threshold {threshold}")

@dsl.pipeline(name='ml-training-pipeline')
def ml_pipeline(data_path: str, learning_rate: float = 0.001, epochs: int = 10):
    """Complete ML pipeline."""

    # Load and validate data
    data_task = load_data(data_path=data_path)

    # Train model
    train_task = train_model(
        data_path=data_task.output,
        learning_rate=learning_rate,
        epochs=epochs
    )

    # Evaluate
    eval_task = evaluate_model(
        model_path=train_task.output,
        test_data_path=f"{data_path}/test"
    )

    # Deploy if passing
    deploy_task = deploy_model(
        model_path=train_task.output,
        metrics=eval_task.output
    )

# Compile pipeline
compiler.Compiler().compile(ml_pipeline, 'ml_pipeline.yaml')
```

### 6. A/B Testing & Canary Deployments

**Multi-Armed Bandit for Model Selection:**

```python
import numpy as np
from typing import List, Dict

class ThompsonSamplingBandit:
    """Thompson Sampling for A/B testing models."""

    def __init__(self, model_ids: List[str]):
        self.model_ids = model_ids
        # Beta distribution parameters (successes, failures)
        self.alpha = {model_id: 1 for model_id in model_ids}
        self.beta = {model_id: 1 for model_id in model_ids}

    def select_model(self) -> str:
        """Select model using Thompson Sampling."""
        samples = {
            model_id: np.random.beta(self.alpha[model_id], self.beta[model_id])
            for model_id in self.model_ids
        }
        return max(samples, key=samples.get)

    def update(self, model_id: str, reward: float):
        """Update model statistics based on reward (1=success, 0=failure)."""
        if reward > 0.5:  # Success
            self.alpha[model_id] += 1
        else:  # Failure
            self.beta[model_id] += 1

    def get_statistics(self) -> Dict:
        """Get current model statistics."""
        return {
            model_id: {
                'alpha': self.alpha[model_id],
                'beta': self.beta[model_id],
                'expected_reward': self.alpha[model_id] /
                                  (self.alpha[model_id] + self.beta[model_id]),
                'total_trials': self.alpha[model_id] + self.beta[model_id] - 2
            }
            for model_id in self.model_ids
        }

# Usage in production
bandit = ThompsonSamplingBandit(['model_v1', 'model_v2'])

def serve_prediction(input_data):
    """Serve prediction with A/B testing."""

    # Select model
    selected_model = bandit.select_model()
    model = load_model(selected_model)

    # Predict
    prediction = model.predict(input_data)

    # Track for later reward update
    log_prediction(
        model_id=selected_model,
        prediction=prediction,
        input_data=input_data
    )

    return prediction

def update_rewards():
    """Batch update rewards based on actual outcomes."""
    outcomes = fetch_outcomes()  # Get actual labels

    for outcome in outcomes:
        model_id = outcome['model_id']
        correct = outcome['prediction'] == outcome['actual']
        bandit.update(model_id, reward=1 if correct else 0)
```

### 7. Production Best Practices

#### Model Governance

**Model Card Documentation:**

```python
# model_card.yaml
model_details:
  name: "Fraud Detection XGBoost v2.1"
  version: "2.1.0"
  date: "2025-01-15"
  owners: ["ml-team@company.com"]
  license: "Proprietary"

intended_use:
  primary_uses:
    - "Real-time fraud detection for transactions >$1000"
    - "Batch scoring for daily transaction reviews"
  out_of_scope:
    - "Not intended for cryptocurrency transactions"
    - "Not calibrated for international transactions outside US/EU"

training_data:
  source: "Internal transaction database"
  date_range: "2023-01-01 to 2024-12-31"
  size: "50M transactions"
  preprocessing:
    - "Feature engineering: transaction velocity, account age"
    - "SMOTE oversampling for fraud class"
    - "StandardScaler normalization"

metrics:
  - name: "AUC-ROC"
    value: 0.94
    threshold: 0.85
  - name: "Precision @ 5% FPR"
    value: 0.89
  - name: "Recall"
    value: 0.82

ethical_considerations:
  - "Bias analysis performed across demographic groups"
  - "No protected attributes used as features"
  - "Quarterly fairness audits required"

monitoring:
  - "Data drift: Weekly statistical tests"
  - "Performance: Daily accuracy tracking"
  - "Retraining trigger: AUC drop >5%"
```

#### CI/CD for ML

**GitHub Actions Workflow:**

```yaml
# .github/workflows/ml-pipeline.yml
name: ML Pipeline CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  data-validation:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          pip install great-expectations dvc

      - name: Pull data with DVC
        run: dvc pull

      - name: Validate data
        run: |
          great_expectations checkpoint run data_validation_checkpoint

  model-training:
    needs: data-validation
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Train model
        run: |
          python training/train.py --config config/train_config.yaml

      - name: Log to MLflow
        env:
          MLFLOW_TRACKING_URI: ${{ secrets.MLFLOW_URI }}
        run: |
          mlflow run . --experiment-name ci-training

  model-evaluation:
    needs: model-training
    runs-on: ubuntu-latest
    steps:
      - name: Load model from MLflow
        run: |
          MODEL_URI=$(mlflow models list --max-results 1 --json | jq -r '.[0].source')
          python evaluation/evaluate.py --model-uri $MODEL_URI

      - name: Check performance gate
        run: |
          python scripts/performance_gate.py --threshold 0.90

  deploy-staging:
    needs: model-evaluation
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to staging
        run: |
          kubectl set image deployment/model-server \
            model=gcr.io/project/model:${{ github.sha }} \
            -n staging

  canary-test:
    needs: deploy-staging
    runs-on: ubuntu-latest
    steps:
      - name: Run canary tests
        run: |
          python tests/canary_test.py --endpoint https://staging.example.com/predict

      - name: Monitor metrics
        run: |
          python monitoring/check_metrics.py --duration 300 --threshold 0.95

  deploy-production:
    needs: canary-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Gradual rollout
        run: |
          # 10% traffic
          kubectl set image deployment/model-server model=gcr.io/project/model:${{ github.sha }}
          kubectl scale deployment/model-server-new --replicas=1
          sleep 600

          # 50% traffic
          kubectl scale deployment/model-server-new --replicas=5
          sleep 600

          # 100% traffic
          kubectl scale deployment/model-server-new --replicas=10
          kubectl scale deployment/model-server-old --replicas=0
```

---

## Level 3: Deep Dive Resources

### Advanced Topics

1. **Distributed Training**
   - Horovod for data parallelism
   - PyTorch DistributedDataParallel
   - Model parallelism with Megatron-LM
   - Gradient compression techniques

2. **Advanced Monitoring**
   - Explainable AI monitoring (SHAP, LIME)
   - Adversarial robustness testing
   - Model interpretability dashboards
   - Automated root cause analysis

3. **AutoML & Meta-Learning**
   - AutoML platforms (H2O AutoML, Auto-sklearn)
   - Neural architecture search (NAS)
   - Transfer learning pipelines
   - Few-shot learning for rapid adaptation

4. **Edge ML & Model Optimization**
   - Model quantization (INT8, mixed precision)
   - Knowledge distillation
   - Pruning and compression
   - ONNX for cross-platform deployment

### Official Documentation

- **MLflow**: https://mlflow.org/docs/latest/index.html
- **Kubeflow**: https://www.kubeflow.org/docs/
- **Feast Feature Store**: https://docs.feast.dev/
- **DVC (Data Version Control)**: https://dvc.org/doc
- **Great Expectations**: https://docs.greatexpectations.io/
- **TorchServe**: https://pytorch.org/serve/
- **TensorFlow Serving**: https://www.tensorflow.org/tfx/guide/serving
- **Seldon Core**: https://docs.seldon.io/projects/seldon-core/en/latest/

### Books

- "Machine Learning Design Patterns" by Lakshmanan, Robinson, Munn
- "Building Machine Learning Powered Applications" by Emmanuel Ameisen
- "Designing Machine Learning Systems" by Chip Huyen
- "Machine Learning Engineering" by Andriy Burkov

### Courses

- Google Cloud Professional ML Engineer Certification
- AWS Certified Machine Learning – Specialty
- Coursera: MLOps Specialization (DeepLearning.AI)
- Full Stack Deep Learning (Berkeley)

### Tools & Platforms

- **Experiment Tracking**: MLflow, Weights & Biases, Neptune.ai, Comet.ml
- **Pipeline Orchestration**: Kubeflow, Apache Airflow, Metaflow, Prefect
- **Feature Stores**: Feast, Tecton, Hopsworks
- **Model Serving**: TorchServe, TensorFlow Serving, Seldon Core, KServe
- **Monitoring**: Evidently AI, WhyLabs, Arize AI, Fiddler
- **Data Versioning**: DVC, LakeFS, Pachyderm

### Community Resources

- MLOps Community: https://mlops.community/
- Made With ML: https://madewithml.com/
- Papers with Code: https://paperswithcode.com/
- MLOps Subreddit: r/mlops

---

## Practice Exercises

### Exercise 1: End-to-End Pipeline

Build a complete MLOps pipeline:

1. Version dataset with DVC
2. Train model with MLflow tracking
3. Register model in MLflow Model Registry
4. Create Kubeflow pipeline for retraining
5. Deploy with FastAPI + Docker
6. Monitor with Prometheus + Grafana

### Exercise 2: Drift Detection System

Implement comprehensive drift detection:

1. Collect baseline statistics from training data
2. Implement KS test for numerical features
3. Implement Chi-square test for categorical features
4. Create concept drift detector tracking model performance
5. Set up alerts for drift detection
6. Build automated retraining trigger

### Exercise 3: A/B Testing Framework

Build an A/B testing system for models:

1. Deploy two model versions
2. Implement Thompson Sampling for traffic routing
3. Collect feedback and update reward statistics
4. Create dashboard showing model performance comparison
5. Implement automated winner selection
6. Gradual rollout of winning model

### Exercise 4: Feature Store

Set up a production feature store:

1. Define entities and feature views in Feast
2. Materialize historical features for training
3. Set up online feature serving
4. Implement feature freshness monitoring
5. Create feature lineage tracking
6. Build feature validation pipeline

---

**Next Steps:** Explore [data-engineering](../data-engineering/SKILL.md) for upstream data pipelines or [observability](../../devops/observability/SKILL.md) for production monitoring integration.
