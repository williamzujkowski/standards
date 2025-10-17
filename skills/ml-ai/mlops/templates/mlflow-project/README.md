# MLflow Fraud Detection Project

Complete MLflow project template for fraud detection with tracking, validation, and serving.

## Structure

```
mlflow-project/
├── MLproject              # MLflow project definition
├── conda.yaml            # Conda environment
├── train.py              # Training script with MLflow tracking
├── validate.py           # Production validation script
├── data/                 # Data directory
├── models/               # Saved models
└── notebooks/            # Jupyter notebooks
```

## Usage

### 1. Train Model

```bash
mlflow run . -P data_path=data/train.csv -P learning_rate=0.01
```

### 2. Validate Model

```bash
mlflow run . -e validate -P model_uri=runs:/abc123/model -P test_data=data/test.csv
```

### 3. Serve Model

```bash
mlflow models serve -m runs:/abc123/model -p 5001
```

### 4. Make Predictions

```bash
curl -X POST http://localhost:5001/invocations \
  -H 'Content-Type: application/json' \
  -d '{"dataframe_split": {"columns": ["feature1", "feature2"], "data": [[0.5, 1.2]]}}'
```

## CI/CD Integration

This project can be integrated into CI/CD pipelines for automated training and deployment.
