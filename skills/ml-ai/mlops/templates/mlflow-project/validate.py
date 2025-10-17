"""
Model validation script for production readiness checks.
"""

import argparse

import great_expectations as ge
import mlflow
import pandas as pd
from sklearn.metrics import accuracy_score, roc_auc_score


def validate_model_performance(model, test_data, thresholds):
    """Validate model meets performance thresholds."""
    print("Validating model performance...")

    df = pd.read_csv(test_data)
    X_test = df.drop("target", axis=1)
    y_test = df["target"]

    # Load model
    model_loaded = mlflow.pyfunc.load_model(model)
    y_pred_proba = model_loaded.predict(X_test)

    # Calculate metrics
    auc = roc_auc_score(y_test, y_pred_proba)
    accuracy = accuracy_score(y_test, (y_pred_proba > 0.5).astype(int))

    print(f"  AUC: {auc:.4f} (threshold: {thresholds['auc']})")
    print(f"  Accuracy: {accuracy:.4f} (threshold: {thresholds['accuracy']})")

    # Check thresholds
    passed = auc >= thresholds["auc"] and accuracy >= thresholds["accuracy"]

    return passed, {"auc": auc, "accuracy": accuracy}


def validate_data_quality(test_data):
    """Validate test data quality using Great Expectations."""
    print("Validating data quality...")

    df = ge.read_csv(test_data)

    # Define expectations
    results = []
    results.append(df.expect_column_values_to_not_be_null("target"))
    results.append(df.expect_column_values_to_be_between("feature_1", -5, 5))

    # Check if all expectations passed
    passed = all(result.success for result in results)

    if passed:
        print("  ✓ All data quality checks passed")
    else:
        print("  ✗ Data quality checks failed")

    return passed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-uri", type=str, required=True)
    parser.add_argument("--test-data", type=str, required=True)
    parser.add_argument("--auc-threshold", type=float, default=0.85)
    parser.add_argument("--accuracy-threshold", type=float, default=0.80)
    args = parser.parse_args()

    thresholds = {"auc": args.auc_threshold, "accuracy": args.accuracy_threshold}

    # Run validation checks
    data_quality_passed = validate_data_quality(args.test_data)
    model_performance_passed, metrics = validate_model_performance(args.model_uri, args.test_data, thresholds)

    # Overall validation result
    if data_quality_passed and model_performance_passed:
        print("\n✓ Model validation PASSED - Ready for production")
        exit(0)
    else:
        print("\n✗ Model validation FAILED - Not ready for production")
        exit(1)


if __name__ == "__main__":
    main()
