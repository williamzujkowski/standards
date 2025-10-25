---
skill_id: data-engineering/data-quality
version: 1.0.0
category: data-engineering
complexity: advanced
prerequisites:
- database/sql
- coding-standards/python
estimated_time: 6-8 hours
standards_alignment:
- DE:data-quality
- OBS:monitoring
- LEG:data-retention
token_cost:
  level_1: ~150
  level_2: ~2000
  level_3: 0 (filesystem)
name: data-quality
description: 'Core Principles:'
---


# Data Quality

## Level 1: Quick Start (5 min)

**Core Principles**:

- Completeness - no missing critical data
- Accuracy - data reflects reality
- Consistency - data aligns across systems
- Timeliness - data is current and available

**Quick Reference**:

```python
# Great Expectations validation
import great_expectations as gx
context = gx.get_context()
validator = context.sources.pandas_default.read_csv("data.csv")
validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_between("age", 0, 120)
```

**Essential Checklist**:

- [ ] Define data quality rules and SLAs
- [ ] Implement automated validation checks
- [ ] Monitor data quality metrics
- [ ] Set up alerting for quality degradation
- [ ] Document data quality expectations

**Common Pitfalls**: See [Common Pitfalls](#common-pitfalls)

## Level 2: Implementation (30 min)

### Data Quality Dimensions

**Completeness Checks**:

```python
def check_completeness(df, required_columns):
    """Validate no missing values in critical columns"""
    missing = df[required_columns].isnull().sum()
    completeness = (1 - missing / len(df)) * 100
    return completeness

# Example
required = ['user_id', 'transaction_date', 'amount']
scores = check_completeness(df, required)
assert all(scores > 99), f"Completeness below threshold: {scores}"
```

**Accuracy Validation**:

```python
# Range checks
def validate_ranges(df):
    assert df['age'].between(0, 120).all(), "Age out of range"
    assert (df['amount'] >= 0).all(), "Negative amount found"
    assert df['email'].str.contains('@').all(), "Invalid email"
```

**Consistency Rules**:

```python
# Cross-field validation
def check_consistency(df):
    # End date must be after start date
    assert (df['end_date'] >= df['start_date']).all()

    # Total should equal sum of parts
    assert np.isclose(
        df['total'],
        df[['part1', 'part2', 'part3']].sum(axis=1)
    ).all()
```

### Data Quality Framework Implementation

**Great Expectations Setup**:

```python
# Create expectation suite
suite = context.create_expectation_suite("transactions_suite")

# Add expectations
validator = context.get_validator(
    batch_request=batch_request,
    expectation_suite_name="transactions_suite"
)

# Schema expectations
validator.expect_table_columns_to_match_ordered_list([
    "id", "user_id", "amount", "timestamp"
])

# Business rule expectations
validator.expect_column_values_to_be_unique("id")
validator.expect_column_values_to_not_be_null("user_id")
validator.expect_column_values_to_be_between("amount", 0, 1000000)

# Save suite
validator.save_expectation_suite(discard_failed_expectations=False)
```

**Automated Validation Pipeline**:

```python
# In data pipeline
def validate_data(df, suite_name):
    validator = context.get_validator(
        batch_request=create_batch_request(df),
        expectation_suite_name=suite_name
    )

    results = validator.validate()

    if not results.success:
        failed = [r for r in results.results if not r.success]
        raise DataQualityException(f"Validation failed: {failed}")

    return results

# Run validation
try:
    results = validate_data(df, "transactions_suite")
    logger.info(f"Data quality check passed: {results.statistics}")
except DataQualityException as e:
    alert_data_team(e)
    raise
```

### Quality Metrics and Monitoring

**Data Quality Score**:

```python
def calculate_dq_score(df, expectations):
    """Calculate overall data quality score"""
    scores = {
        'completeness': check_completeness(df),
        'accuracy': check_accuracy(df),
        'consistency': check_consistency(df),
        'timeliness': check_timeliness(df)
    }

    # Weighted average
    weights = {'completeness': 0.3, 'accuracy': 0.4,
               'consistency': 0.2, 'timeliness': 0.1}

    total_score = sum(scores[k] * weights[k] for k in scores)
    return total_score, scores
```

**Quality Dashboards**:

```python
# Export metrics for visualization
import pandas as pd

def export_quality_metrics(results):
    metrics = {
        'timestamp': datetime.now(),
        'suite_name': results.suite_name,
        'success_rate': results.statistics['success_percent'],
        'evaluated_expectations': results.statistics['evaluated_expectations'],
        'successful_expectations': results.statistics['successful_expectations']
    }

    # Send to time-series DB
    influxdb_client.write_point('data_quality', metrics)
```

**Integration Points**: See [Integration Points](#integration-points)

## Level 3: Mastery

**Advanced Topics**:

- See `docs/data-engineering/data-quality/advanced-anomaly-detection.md`
- See `docs/data-engineering/data-quality/ml-based-validation.md`
- See `docs/data-engineering/data-quality/data-lineage-tracking.md`

**Resources**:

- [Great Expectations Documentation](https://docs.greatexpectations.io/)
- [Data Quality Framework](https://tdwi.org/articles/2017/01/10/data-quality-framework.aspx)
- [Deequ (AWS)](https://github.com/awslabs/deequ)

**Templates**:

- `templates/data-engineering/data-quality/expectation-suite.json`
- `templates/data-engineering/data-quality/quality-dashboard.yaml`

**Scripts**:

- `scripts/data-engineering/data-quality/validate-pipeline.py`
- `scripts/data-engineering/data-quality/generate-profile.py`
- `scripts/data-engineering/data-quality/quality-report.py`

## Examples

### Basic Validation Pipeline

```python
# validate.py
import great_expectations as gx

def validate_dataset(file_path, suite_name):
    context = gx.get_context()

    # Create batch request
    batch_request = {
        "datasource_name": "my_datasource",
        "data_connector_name": "default_inferred_data_connector_name",
        "data_asset_name": file_path
    }

    # Validate
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )

    results = validator.validate()

    # Generate data docs
    context.build_data_docs()

    return results.success

if __name__ == "__main__":
    success = validate_dataset("data/transactions.csv", "transactions_suite")
    sys.exit(0 if success else 1)
```

### Production Pipeline Integration

```python
# airflow_dag.py
from airflow import DAG
from airflow.operators.python import PythonOperator

def run_quality_checks(**context):
    df = context['ti'].xcom_pull(task_ids='extract_data')

    # Run validation
    results = validate_data(df, "production_suite")

    # Push metrics
    context['ti'].xcom_push(key='quality_score', value=results.statistics)

    if not results.success:
        raise AirflowFailException("Data quality check failed")

with DAG('data_pipeline', schedule_interval='@daily') as dag:
    quality_check = PythonOperator(
        task_id='quality_check',
        python_callable=run_quality_checks
    )
```

### Real-Time Validation

```python
# Kafka stream validation
from confluent_kafka import Consumer
import great_expectations as gx

consumer = Consumer({'bootstrap.servers': 'localhost:9092'})
context = gx.get_context()

while True:
    msg = consumer.poll(1.0)
    if msg:
        data = json.loads(msg.value())

        # Convert to DataFrame
        df = pd.DataFrame([data])

        # Validate
        try:
            validate_data(df, "realtime_suite")
            process_message(data)
        except DataQualityException:
            send_to_dead_letter_queue(msg)
```

## Integration Points

### Upstream Dependencies

- **Data Sources**: Databases, APIs, file systems, streams
- **ETL Tools**: Airflow, Prefect, Dagster, dbt
- **Data Catalogs**: DataHub, Amundsen, Atlan

### Downstream Consumers

- **BI Tools**: Tableau, Looker, Power BI
- **ML Platforms**: MLflow, Kubeflow, SageMaker
- **Data Warehouses**: Snowflake, BigQuery, Redshift

### Related Skills

- [Orchestration](../orchestration/SKILL.md)
- [SQL](../../database/sql/SKILL.md)
- [Python Coding Standards](../../coding-standards/python/SKILL.md)
- [Monitoring](../../devops/monitoring/SKILL.md)

## Common Pitfalls

### Pitfall 1: No Data Quality SLAs

**Problem**: Quality issues go unnoticed until impacting business
**Solution**: Define measurable quality targets and monitor continuously
**Prevention**: Establish data quality SLAs in data contracts

### Pitfall 2: Manual Validation

**Problem**: Inconsistent checks, human error, doesn't scale
**Solution**: Automate validation in data pipelines
**Prevention**: Make automated quality checks mandatory for production

### Pitfall 3: Ignoring Data Drift

**Problem**: Models degrade, reports become inaccurate
**Solution**: Monitor data distributions and schema changes over time
**Prevention**: Implement statistical drift detection and alerting

### Pitfall 4: Validation Without Context

**Problem**: False positives, alert fatigue
**Solution**: Set business-relevant thresholds and validation rules
**Prevention**: Involve domain experts in defining quality expectations

### Pitfall 5: No Quality Lineage

**Problem**: Unable to trace quality issues to source
**Solution**: Track data lineage and quality at each transformation
**Prevention**: Implement end-to-end lineage tracking with quality metadata
