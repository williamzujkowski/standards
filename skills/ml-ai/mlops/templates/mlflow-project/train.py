"""
MLflow training script with comprehensive tracking and model registry integration.
"""

import argparse
import os

import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn
import mlflow.xgboost
import numpy as np
import pandas as pd
import seaborn as sns
import shap
from mlflow.models.signature import infer_signature
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier


def set_seed(seed=42):
    """Set random seed for reproducibility."""
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)


def load_and_preprocess_data(data_path, test_size=0.2, random_state=42):
    """Load and preprocess data."""
    print(f"Loading data from {data_path}")
    df = pd.read_csv(data_path)

    # Separate features and target
    X = df.drop("target", axis=1)
    y = df["target"]

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Feature scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Log data statistics
    mlflow.log_param("n_samples", len(df))
    mlflow.log_param("n_features", X.shape[1])
    mlflow.log_param("class_balance", f"{y.mean():.3f}")

    return X_train_scaled, X_test_scaled, y_train, y_test, scaler, X.columns


def train_model(X_train, y_train, learning_rate, n_estimators, max_depth, random_state):
    """Train XGBoost model."""
    print("Training XGBoost model...")

    model = XGBClassifier(
        learning_rate=learning_rate,
        n_estimators=n_estimators,
        max_depth=max_depth,
        random_state=random_state,
        eval_metric="logloss",
    )

    # Log hyperparameters
    mlflow.log_params(
        {
            "learning_rate": learning_rate,
            "n_estimators": n_estimators,
            "max_depth": max_depth,
            "random_state": random_state,
        }
    )

    # Train with early stopping
    model.fit(X_train, y_train, eval_set=[(X_train, y_train)], verbose=False)

    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model and log metrics."""
    print("Evaluating model...")

    # Predictions
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]

    # Calculate metrics
    metrics = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1_score": f1_score(y_test, y_pred),
        "roc_auc": roc_auc_score(y_test, y_pred_proba),
    }

    # Log metrics
    mlflow.log_metrics(metrics)

    # Print metrics
    print("\nModel Performance:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print(f"\nConfusion Matrix:\n{cm}")

    # Classification report
    report = classification_report(y_test, y_pred)
    print(f"\nClassification Report:\n{report}")

    return metrics, y_pred, y_pred_proba


def create_visualizations(model, X_test, y_test, y_pred, y_pred_proba, feature_names):
    """Create and log visualizations."""
    print("Creating visualizations...")

    # Feature importance
    fig, ax = plt.subplots(figsize=(10, 6))
    feature_importance = (
        pd.DataFrame({"feature": feature_names, "importance": model.feature_importances_})
        .sort_values("importance", ascending=False)
        .head(20)
    )

    sns.barplot(data=feature_importance, x="importance", y="feature", ax=ax)
    ax.set_title("Top 20 Feature Importances")
    plt.tight_layout()
    mlflow.log_figure(fig, "feature_importance.png")
    plt.close()

    # Confusion matrix heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")
    plt.tight_layout()
    mlflow.log_figure(fig, "confusion_matrix.png")
    plt.close()

    # SHAP values (sample for performance)
    print("Computing SHAP values...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test[:100])

    fig, ax = plt.subplots(figsize=(10, 8))
    shap.summary_plot(shap_values, X_test[:100], feature_names=feature_names, show=False)
    plt.tight_layout()
    mlflow.log_figure(fig, "shap_summary.png")
    plt.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--test-size", type=float, default=0.2)
    parser.add_argument("--learning-rate", type=float, default=0.01)
    parser.add_argument("--n-estimators", type=int, default=100)
    parser.add_argument("--max-depth", type=int, default=6)
    parser.add_argument("--random-state", type=int, default=42)
    args = parser.parse_args()

    # Set seed
    set_seed(args.random_state)

    # Start MLflow run
    with mlflow.start_run():
        # Log environment info
        mlflow.log_param("python_version", os.sys.version)

        # Load and preprocess data
        X_train, X_test, y_train, y_test, scaler, feature_names = load_and_preprocess_data(
            args.data_path, args.test_size, args.random_state
        )

        # Train model
        model = train_model(X_train, y_train, args.learning_rate, args.n_estimators, args.max_depth, args.random_state)

        # Evaluate model
        metrics, y_pred, y_pred_proba = evaluate_model(model, X_test, y_test)

        # Create visualizations
        create_visualizations(model, X_test, y_test, y_pred, y_pred_proba, feature_names)

        # Infer model signature
        signature = infer_signature(X_train, model.predict(X_train))

        # Log model
        mlflow.xgboost.log_model(model, "model", signature=signature, registered_model_name="fraud_detection_model")

        # Log scaler as artifact
        import joblib

        joblib.dump(scaler, "scaler.pkl")
        mlflow.log_artifact("scaler.pkl")

        print(f"\nModel logged to MLflow. Run ID: {mlflow.active_run().info.run_id}")
        print(f"Model URI: runs:/{mlflow.active_run().info.run_id}/model")

        # Check if model meets production threshold
        if metrics["roc_auc"] >= 0.85:
            print(f"\n✓ Model meets production threshold (AUC: {metrics['roc_auc']:.4f})")
        else:
            print(f"\n✗ Model below production threshold (AUC: {metrics['roc_auc']:.4f})")


if __name__ == "__main__":
    main()
