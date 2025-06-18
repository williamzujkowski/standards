# Data Engineering Standards

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active
**Standard Code:** DE

---

**Version:** 1.0.0
**Last Updated:** January 2025
**Status:** Active

## Table of Contents

1. [Data Pipeline Standards](#1-data-pipeline-standards)
2. [Data Quality and Governance](#2-data-quality-and-governance)
3. [Data Storage and Modeling](#3-data-storage-and-modeling)
4. [Streaming Data Processing](#4-streaming-data-processing)
5. [Analytics Engineering](#5-analytics-engineering)
6. [Data Security and Privacy](#6-data-security-and-privacy)
7. [MLOps and Data Science](#7-mlops-and-data-science)
8. [Data Operations](#8-data-operations)

---

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## 1. Data Pipeline Standards

### 1.1 ETL/ELT Design Principles

#### Pipeline Architecture **[REQUIRED]**
```python
# Data pipeline structure
class DataPipeline:
    """Base class for all data pipelines."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.metrics = MetricsCollector()

    def extract(self) -> DataSet:
        """Extract data from source systems."""
        with self.metrics.timer('extract_duration'):
            try:
                data = self._extract_implementation()
                self.logger.info(f"Extracted {len(data)} records")
                return data
            except Exception as e:
                self.logger.error(f"Extract failed: {e}")
                self.metrics.increment('extract_failures')
                raise

    def transform(self, data: DataSet) -> DataSet:
        """Transform extracted data."""
        with self.metrics.timer('transform_duration'):
            # Data quality checks
            self._validate_input_data(data)

            # Apply transformations
            transformed = self._transform_implementation(data)

            # Validate output
            self._validate_output_data(transformed)

            return transformed

    def load(self, data: DataSet) -> LoadResult:
        """Load transformed data to destination."""
        with self.metrics.timer('load_duration'):
            return self._load_implementation(data)

    def run(self) -> PipelineResult:
        """Execute the complete pipeline."""
        pipeline_id = generate_pipeline_id()
        start_time = datetime.utcnow()

        try:
            self.logger.info(f"Starting pipeline {pipeline_id}")

            # Execute ETL steps
            raw_data = self.extract()
            clean_data = self.transform(raw_data)
            result = self.load(clean_data)

            # Record success metrics
            duration = (datetime.utcnow() - start_time).total_seconds()
            self.metrics.histogram('pipeline_duration', duration)
            self.metrics.increment('pipeline_success')

            return PipelineResult(
                pipeline_id=pipeline_id,
                status='success',
                records_processed=len(clean_data),
                duration=duration
            )

        except Exception as e:
            self.logger.error(f"Pipeline {pipeline_id} failed: {e}")
            self.metrics.increment('pipeline_failures')
            raise
```

#### Configuration Management **[REQUIRED]**
```yaml
# pipeline-config.yml
pipeline:
  name: "customer_data_etl"
  version: "1.2.0"
  schedule: "0 2 * * *"  # Daily at 2 AM
  timeout_minutes: 60
  retry_policy:
    max_retries: 3
    retry_delay_seconds: 300
    backoff_multiplier: 2

sources:
  - name: "customer_db"
    type: "postgresql"
    connection: "${CUSTOMER_DB_CONNECTION}"
    query_file: "sql/customer_extract.sql"
    incremental_column: "updated_at"

  - name: "orders_api"
    type: "rest_api"
    base_url: "${ORDERS_API_URL}"
    auth_type: "bearer_token"
    rate_limit: 100  # requests per minute

destinations:
  - name: "data_warehouse"
    type: "snowflake"
    connection: "${SNOWFLAKE_CONNECTION}"
    schema: "analytics"
    table: "dim_customers"
    write_mode: "upsert"
    partition_by: ["created_date"]

data_quality:
  rules:
    - column: "customer_id"
      type: "not_null"
      severity: "error"
    - column: "email"
      type: "unique"
      severity: "warning"
    - column: "created_at"
      type: "range"
      min_value: "2020-01-01"
      max_value: "{{ today }}"

monitoring:
  alerts:
    - metric: "pipeline_failure_rate"
      threshold: 0.1
      window: "1h"
    - metric: "data_freshness"
      threshold: "2h"
```

### 1.2 Data Orchestration

#### Airflow DAG Standards **[REQUIRED]**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor
from datetime import datetime, timedelta

# Default arguments for all tasks
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2025, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
}

# DAG definition
dag = DAG(
    'customer_data_pipeline',
    default_args=default_args,
    description='Customer data ETL pipeline',
    schedule_interval='@daily',
    catchup=False,  # Don't run for historical dates
    max_active_runs=1,  # Prevent overlapping runs
    tags=['etl', 'customer', 'daily'],
    doc_md=__doc__,
)

# Task definitions
def extract_customer_data(**context):
    """Extract customer data from source systems."""
    execution_date = context['execution_date']

    # Use Airflow's XCom to pass data between tasks
    extracted_records = extract_customers_since(execution_date)
    return len(extracted_records)

def validate_data_quality(**context):
    """Validate data quality before processing."""
    # Get record count from previous task
    record_count = context['task_instance'].xcom_pull(
        task_ids='extract_customer_data'
    )

    if record_count == 0:
        raise ValueError("No records extracted - check source system")

    # Additional quality checks
    run_data_quality_tests()

# Define tasks
extract_task = PythonOperator(
    task_id='extract_customer_data',
    python_callable=extract_customer_data,
    dag=dag,
)

quality_check = PythonOperator(
    task_id='validate_data_quality',
    python_callable=validate_data_quality,
    dag=dag,
)

transform_task = BashOperator(
    task_id='transform_data',
    bash_command='dbt run --models customer_models',
    dag=dag,
)

load_task = PythonOperator(
    task_id='load_to_warehouse',
    python_callable=load_customer_data,
    dag=dag,
)

# Define dependencies
extract_task >> quality_check >> transform_task >> load_task
```

#### dbt Configuration **[REQUIRED]**
```yaml
# dbt_project.yml
name: 'analytics'
version: '1.0.0'
config-version: 2

model-paths: ["models"]
analysis-paths: ["analysis"]
test-paths: ["tests"]
seed-paths: ["data"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  analytics:
    # Staging models
    staging:
      +materialized: view
      +docs:
        node_color: "lightblue"

    # Intermediate models
    intermediate:
      +materialized: ephemeral
      +docs:
        node_color: "orange"

    # Mart models
    marts:
      +materialized: table
      +docs:
        node_color: "green"
      core:
        +materialized: table
        +post-hook: "{{ grant_select('analytics_users') }}"

vars:
  # Date range for incremental models
  start_date: '2020-01-01'

  # Feature flags
  enable_experimental_features: false

on-run-start:
  - "{{ create_audit_log_entry() }}"

on-run-end:
  - "{{ update_data_freshness() }}"
```

### 1.3 Error Handling and Recovery

#### Retry Logic **[REQUIRED]**
```python
import backoff
from typing import Any, Callable
import logging

logger = logging.getLogger(__name__)

@backoff.on_exception(
    backoff.expo,
    (ConnectionError, TimeoutError),
    max_tries=5,
    max_time=300,  # 5 minutes
    on_backoff=lambda details: logger.warning(
        f"Retry {details['tries']}/{details['max_tries']} "
        f"after {details['wait']:.1f}s: {details['exception']}"
    )
)
def robust_data_operation(operation: Callable, *args, **kwargs) -> Any:
    """Execute data operation with retry logic."""
    try:
        return operation(*args, **kwargs)
    except Exception as e:
        logger.error(f"Operation failed: {e}")
        raise

# Circuit breaker pattern
class CircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN

    def call(self, func: Callable, *args, **kwargs) -> Any:
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = 'HALF_OPEN'
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.record_failure()
            raise

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

    def reset(self):
        self.failure_count = 0
        self.state = 'CLOSED'
```

---

## 2. Data Quality and Governance

### 2.1 Data Quality Framework

#### Quality Rules Engine **[REQUIRED]**
```python
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd

@dataclass
class DataQualityResult:
    rule_name: str
    passed: bool
    failed_records: int
    total_records: int
    error_message: str = None
    severity: str = "error"  # error, warning, info

class DataQualityRule(ABC):
    """Base class for data quality rules."""

    def __init__(self, name: str, severity: str = "error"):
        self.name = name
        self.severity = severity

    @abstractmethod
    def validate(self, data: pd.DataFrame) -> DataQualityResult:
        pass

class NotNullRule(DataQualityRule):
    def __init__(self, column: str, **kwargs):
        super().__init__(f"not_null_{column}", **kwargs)
        self.column = column

    def validate(self, data: pd.DataFrame) -> DataQualityResult:
        null_count = data[self.column].isnull().sum()
        passed = null_count == 0

        return DataQualityResult(
            rule_name=self.name,
            passed=passed,
            failed_records=null_count,
            total_records=len(data),
            error_message=f"Found {null_count} null values in {self.column}" if not passed else None,
            severity=self.severity
        )

class UniqueRule(DataQualityRule):
    def __init__(self, column: str, **kwargs):
        super().__init__(f"unique_{column}", **kwargs)
        self.column = column

    def validate(self, data: pd.DataFrame) -> DataQualityResult:
        duplicate_count = data[self.column].duplicated().sum()
        passed = duplicate_count == 0

        return DataQualityResult(
            rule_name=self.name,
            passed=passed,
            failed_records=duplicate_count,
            total_records=len(data),
            error_message=f"Found {duplicate_count} duplicate values in {self.column}" if not passed else None,
            severity=self.severity
        )

class DataQualityValidator:
    def __init__(self, rules: List[DataQualityRule]):
        self.rules = rules
        self.results = []

    def validate(self, data: pd.DataFrame) -> List[DataQualityResult]:
        self.results = []

        for rule in self.rules:
            try:
                result = rule.validate(data)
                self.results.append(result)

                # Log results
                if not result.passed:
                    if result.severity == "error":
                        logger.error(f"Data quality check failed: {result.error_message}")
                    else:
                        logger.warning(f"Data quality warning: {result.error_message}")

            except Exception as e:
                logger.error(f"Data quality rule {rule.name} failed to execute: {e}")
                self.results.append(DataQualityResult(
                    rule_name=rule.name,
                    passed=False,
                    failed_records=0,
                    total_records=len(data),
                    error_message=str(e),
                    severity="error"
                ))

        return self.results

    def has_errors(self) -> bool:
        return any(not r.passed and r.severity == "error" for r in self.results)

    def generate_report(self) -> Dict[str, Any]:
        return {
            "total_rules": len(self.rules),
            "passed_rules": sum(1 for r in self.results if r.passed),
            "failed_rules": sum(1 for r in self.results if not r.passed),
            "error_count": sum(1 for r in self.results if not r.passed and r.severity == "error"),
            "warning_count": sum(1 for r in self.results if not r.passed and r.severity == "warning"),
            "results": [
                {
                    "rule": r.rule_name,
                    "status": "passed" if r.passed else "failed",
                    "severity": r.severity,
                    "failed_records": r.failed_records,
                    "failure_rate": r.failed_records / r.total_records if r.total_records > 0 else 0,
                    "message": r.error_message
                }
                for r in self.results
            ]
        }
```

#### Great Expectations Integration **[RECOMMENDED]**
```python
# great_expectations/expectations/custom_dataset.py
import great_expectations as ge
from great_expectations.core.expectation_configuration import ExpectationConfiguration

def create_data_quality_suite(df_name: str) -> ge.core.ExpectationSuite:
    """Create a comprehensive data quality suite."""

    suite = ge.core.ExpectationSuite(expectation_suite_name=f"{df_name}_quality_suite")

    # Basic data integrity expectations
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_table_row_count_to_be_between",
            kwargs={"min_value": 1, "max_value": 10000000}
        )
    )

    # Column-specific expectations
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_not_be_null",
            kwargs={"column": "id"}
        )
    )

    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_unique",
            kwargs={"column": "id"}
        )
    )

    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_match_regex",
            kwargs={
                "column": "email",
                "regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            }
        )
    )

    # Custom business rule expectations
    suite.add_expectation(
        ExpectationConfiguration(
            expectation_type="expect_column_values_to_be_between",
            kwargs={
                "column": "age",
                "min_value": 0,
                "max_value": 150
            }
        )
    )

    return suite

# Usage in pipeline
def validate_with_great_expectations(df: pd.DataFrame, suite_name: str) -> bool:
    """Validate DataFrame using Great Expectations."""

    # Convert to Great Expectations DataFrame
    ge_df = ge.from_pandas(df)

    # Load or create expectation suite
    suite = create_data_quality_suite(suite_name)

    # Validate
    validation_result = ge_df.validate(expectation_suite=suite)

    # Process results
    if not validation_result.success:
        failed_expectations = [
            exp for exp in validation_result.results
            if not exp.success
        ]

        for failure in failed_expectations:
            logger.error(f"Expectation failed: {failure.expectation_config.expectation_type}")

    return validation_result.success
```

### 2.2 Data Lineage and Catalog

#### Data Lineage Tracking **[REQUIRED]**
```python
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import json

@dataclass
class DataAsset:
    name: str
    type: str  # table, view, file, api
    location: str
    schema: Dict[str, str]
    owner: str
    description: str
    created_at: datetime
    updated_at: datetime

@dataclass
class DataLineage:
    asset_id: str
    parent_assets: List[str]
    transformation: str
    transformation_code: Optional[str]
    created_by: str
    created_at: datetime

class DataCatalog:
    def __init__(self, backend_type: str = "postgres"):
        self.backend = self._init_backend(backend_type)

    def register_asset(self, asset: DataAsset) -> str:
        """Register a new data asset in the catalog."""
        asset_id = self._generate_asset_id(asset)

        self.backend.execute("""
            INSERT INTO data_assets (
                id, name, type, location, schema, owner,
                description, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                updated_at = EXCLUDED.updated_at,
                schema = EXCLUDED.schema
        """, (
            asset_id, asset.name, asset.type, asset.location,
            json.dumps(asset.schema), asset.owner, asset.description,
            asset.created_at, asset.updated_at
        ))

        return asset_id

    def record_lineage(self, lineage: DataLineage):
        """Record data lineage information."""
        self.backend.execute("""
            INSERT INTO data_lineage (
                asset_id, parent_assets, transformation,
                transformation_code, created_by, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            lineage.asset_id, json.dumps(lineage.parent_assets),
            lineage.transformation, lineage.transformation_code,
            lineage.created_by, lineage.created_at
        ))

    def get_lineage(self, asset_id: str, depth: int = 3) -> Dict:
        """Get lineage graph for an asset."""
        # Recursive query to build lineage graph
        query = """
        WITH RECURSIVE lineage_tree AS (
            SELECT asset_id, parent_assets, transformation, 0 as level
            FROM data_lineage
            WHERE asset_id = %s

            UNION ALL

            SELECT l.asset_id, l.parent_assets, l.transformation, lt.level + 1
            FROM data_lineage l
            JOIN lineage_tree lt ON l.asset_id = ANY(
                SELECT json_array_elements_text(lt.parent_assets::json)
            )
            WHERE lt.level < %s
        )
        SELECT * FROM lineage_tree
        """

        results = self.backend.fetch_all(query, (asset_id, depth))
        return self._build_lineage_graph(results)

# Usage in dbt models
def track_dbt_lineage():
    """Track lineage for dbt models."""
    # This would be called in dbt post-hooks
    catalog = DataCatalog()

    # Register the current model
    asset = DataAsset(
        name="{{ this.name }}",
        type="table",
        location="{{ this }}",
        schema="{{ get_column_schema() }}",
        owner="{{ var('owner') }}",
        description="{{ model.description }}",
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    asset_id = catalog.register_asset(asset)

    # Record lineage to parent models
    lineage = DataLineage(
        asset_id=asset_id,
        parent_assets="{{ get_parent_models() }}",
        transformation="dbt_model",
        transformation_code="{{ get_compiled_sql() }}",
        created_by="dbt",
        created_at=datetime.utcnow()
    )

    catalog.record_lineage(lineage)
```

### 2.3 Data Governance Framework

#### Data Classification **[REQUIRED]**
```python
from enum import Enum
from typing import List, Dict

class DataClassification(Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"
    PII = "pii"
    PHI = "phi"  # Protected Health Information

class DataGovernancePolicy:
    def __init__(self):
        self.policies = {
            DataClassification.PII: {
                "encryption_required": True,
                "access_log_required": True,
                "retention_days": 2555,  # 7 years
                "allowed_regions": ["us-east-1", "us-west-2"],
                "approval_required": True,
                "anonymization_required": True
            },
            DataClassification.PHI: {
                "encryption_required": True,
                "access_log_required": True,
                "retention_days": 2555,
                "allowed_regions": ["us-east-1"],
                "approval_required": True,
                "anonymization_required": True,
                "audit_required": True
            },
            DataClassification.CONFIDENTIAL: {
                "encryption_required": True,
                "access_log_required": True,
                "retention_days": 1825,  # 5 years
                "approval_required": False,
                "anonymization_required": False
            }
        }

    def validate_compliance(self, asset: DataAsset, classification: DataClassification) -> List[str]:
        """Validate that an asset complies with governance policies."""
        violations = []
        policy = self.policies.get(classification, {})

        # Check encryption requirement
        if policy.get("encryption_required") and not asset.is_encrypted:
            violations.append("Encryption required but not enabled")

        # Check access logging
        if policy.get("access_log_required") and not asset.has_access_logging:
            violations.append("Access logging required but not enabled")

        # Check region restrictions
        allowed_regions = policy.get("allowed_regions", [])
        if allowed_regions and asset.region not in allowed_regions:
            violations.append(f"Asset in {asset.region} but only {allowed_regions} allowed")

        return violations

# Data masking utilities
class DataMasking:
    @staticmethod
    def mask_email(email: str) -> str:
        """Mask email address for privacy."""
        local, domain = email.split('@')
        masked_local = local[0] + '*' * (len(local) - 2) + local[-1] if len(local) > 2 else '*' * len(local)
        return f"{masked_local}@{domain}"

    @staticmethod
    def mask_phone(phone: str) -> str:
        """Mask phone number."""
        if len(phone) >= 4:
            return '*' * (len(phone) - 4) + phone[-4:]
        return '*' * len(phone)

    @staticmethod
    def mask_ssn(ssn: str) -> str:
        """Mask Social Security Number."""
        return "XXX-XX-" + ssn[-4:] if len(ssn) >= 4 else "XXX-XX-XXXX"
```

---

## 3. Data Storage and Modeling

### 3.1 Data Warehouse Design

#### Dimensional Modeling **[REQUIRED]**
```sql
-- Dimension table example
CREATE TABLE dim_customers (
    customer_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(200) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    address_line_1 VARCHAR(255),
    address_line_2 VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    postal_code VARCHAR(20),
    country VARCHAR(50),
    customer_segment VARCHAR(50),
    customer_status VARCHAR(20),

    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current BOOLEAN DEFAULT TRUE,

    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by VARCHAR(100),
    updated_by VARCHAR(100),

    -- Data quality fields
    data_source VARCHAR(100),
    data_quality_score DECIMAL(3,2),

    UNIQUE(customer_id, effective_date)
);

-- Fact table example
CREATE TABLE fact_orders (
    order_key BIGINT IDENTITY(1,1) PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,

    -- Foreign keys to dimensions
    customer_key BIGINT NOT NULL,
    product_key BIGINT NOT NULL,
    date_key INTEGER NOT NULL,
    store_key BIGINT,

    -- Degenerate dimensions
    order_number VARCHAR(50),
    line_item_number INTEGER,

    -- Measures
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    total_amount DECIMAL(10,2) NOT NULL,
    cost_amount DECIMAL(10,2),
    profit_amount DECIMAL(10,2),

    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (customer_key) REFERENCES dim_customers(customer_key),
    FOREIGN KEY (product_key) REFERENCES dim_products(product_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key),
    FOREIGN KEY (store_key) REFERENCES dim_stores(store_key)
);

-- Indexes for performance
CREATE INDEX idx_fact_orders_customer ON fact_orders(customer_key);
CREATE INDEX idx_fact_orders_product ON fact_orders(product_key);
CREATE INDEX idx_fact_orders_date ON fact_orders(date_key);
CREATE INDEX idx_fact_orders_composite ON fact_orders(date_key, customer_key, product_key);
```

#### Data Vault Modeling **[RECOMMENDED]**
```sql
-- Hub: Business keys
CREATE TABLE hub_customer (
    customer_hash_key CHAR(32) PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL
);

-- Satellite: Descriptive attributes
CREATE TABLE sat_customer_details (
    customer_hash_key CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    load_end_date TIMESTAMP,
    customer_name VARCHAR(200),
    email VARCHAR(255),
    phone VARCHAR(50),
    address TEXT,
    customer_segment VARCHAR(50),
    record_source VARCHAR(100) NOT NULL,
    hash_diff CHAR(32) NOT NULL,

    PRIMARY KEY (customer_hash_key, load_date),
    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key)
);

-- Link: Relationships between business entities
CREATE TABLE link_customer_order (
    customer_order_hash_key CHAR(32) PRIMARY KEY,
    customer_hash_key CHAR(32) NOT NULL,
    order_hash_key CHAR(32) NOT NULL,
    load_date TIMESTAMP NOT NULL,
    record_source VARCHAR(100) NOT NULL,

    FOREIGN KEY (customer_hash_key) REFERENCES hub_customer(customer_hash_key),
    FOREIGN KEY (order_hash_key) REFERENCES hub_order(order_hash_key)
);
```

### 3.2 Data Lake Architecture

#### Data Lake Organization **[REQUIRED]**
```
data-lake/
├── raw/                          # Raw, unprocessed data
│   ├── year=2025/
│   │   ├── month=01/
│   │   │   ├── day=15/
│   │   │   │   ├── hour=14/
│   │   │   │   │   └── source_system_data.parquet
├── bronze/                       # Cleaned, validated data
│   ├── source_system/
│   │   ├── table_name/
│   │   │   └── year=2025/month=01/day=15/
├── silver/                       # Enriched, conformed data
│   ├── domain_area/
│   │   ├── entity_name/
│   │   │   └── year=2025/month=01/day=15/
└── gold/                        # Analytics-ready data
    ├── business_area/
    │   ├── aggregated_metrics/
    │   └── dimensional_models/
```

#### Data Lake Processing **[REQUIRED]**
```python
import boto3
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

class DataLakeProcessor:
    def __init__(self, spark_config: Dict[str, str]):
        self.spark = SparkSession.builder \
            .appName("DataLakeProcessor") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
            .getOrCreate()

        # Configure for optimal performance
        self.spark.conf.set("spark.sql.adaptive.advisoryPartitionSizeInBytes", "256MB")
        self.spark.conf.set("spark.sql.adaptive.coalescePartitions.minPartitionNum", "1")

    def process_raw_to_bronze(self, source_path: str, target_path: str, schema: StructType):
        """Process raw data to bronze layer with basic cleaning."""

        # Read raw data
        df = self.spark.read.schema(schema).parquet(source_path)

        # Basic data cleaning
        df_clean = df \
            .dropDuplicates() \
            .withColumn("processed_at", current_timestamp()) \
            .withColumn("data_source", lit("source_system")) \
            .filter(col("id").isNotNull())  # Remove records without key

        # Data quality checks
        total_records = df.count()
        clean_records = df_clean.count()
        quality_score = clean_records / total_records if total_records > 0 else 0

        if quality_score < 0.95:  # Less than 95% clean data
            logger.warning(f"Data quality below threshold: {quality_score:.2%}")

        # Write to bronze layer with partitioning
        df_clean.write \
            .mode("overwrite") \
            .partitionBy("year", "month", "day") \
            .parquet(target_path)

        return {
            "total_records": total_records,
            "clean_records": clean_records,
            "quality_score": quality_score
        }

    def process_bronze_to_silver(self, bronze_path: str, silver_path: str):
        """Process bronze data to silver layer with enrichment."""

        # Read bronze data
        df = self.spark.read.parquet(bronze_path)

        # Apply business rules and enrichment
        df_enriched = df \
            .withColumn("customer_segment",
                when(col("total_spent") > 1000, "premium")
                .when(col("total_spent") > 500, "standard")
                .otherwise("basic")) \
            .withColumn("customer_lifetime_months",
                months_between(current_date(), col("first_purchase_date"))) \
            .withColumn("is_active",
                col("last_purchase_date") > date_sub(current_date(), 90))

        # Write to silver layer
        df_enriched.write \
            .mode("overwrite") \
            .option("mergeSchema", "true") \
            .partitionBy("customer_segment", "year", "month") \
            .parquet(silver_path)

    def create_gold_aggregations(self, silver_path: str, gold_path: str):
        """Create analytics-ready aggregations in gold layer."""

        df = self.spark.read.parquet(silver_path)

        # Customer metrics aggregation
        customer_metrics = df.groupBy("customer_id", "customer_segment") \
            .agg(
                sum("order_amount").alias("total_spent"),
                count("order_id").alias("order_count"),
                avg("order_amount").alias("avg_order_value"),
                max("order_date").alias("last_order_date"),
                min("order_date").alias("first_order_date")
            ) \
            .withColumn("calculated_at", current_timestamp())

        # Write aggregated metrics
        customer_metrics.write \
            .mode("overwrite") \
            .partitionBy("customer_segment") \
            .parquet(f"{gold_path}/customer_metrics")
```

### 3.3 NoSQL Data Modeling

#### Document Store Design **[REQUIRED]**
```json
// MongoDB customer document
{
  "_id": ObjectId("..."),
  "customer_id": "CUST-12345",
  "personal_info": {
    "name": {
      "first": "John",
      "last": "Doe",
      "full": "John Doe"
    },
    "email": "john.doe@example.com",
    "phone": "+1-555-123-4567",
    "date_of_birth": ISODate("1985-03-15"),
    "address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "postal_code": "10001",
      "country": "US"
    }
  },
  "account_info": {
    "status": "active",
    "segment": "premium",
    "created_at": ISODate("2020-01-15"),
    "last_login": ISODate("2025-01-15T10:30:00Z"),
    "preferences": {
      "marketing_emails": true,
      "sms_notifications": false,
      "currency": "USD",
      "language": "en"
    }
  },
  "order_summary": {
    "total_orders": 15,
    "total_spent": 2450.50,
    "avg_order_value": 163.37,
    "first_order_date": ISODate("2020-02-01"),
    "last_order_date": ISODate("2025-01-10")
  },
  "tags": ["premium", "loyal", "electronics"],
  "metadata": {
    "created_at": ISODate("2020-01-15"),
    "updated_at": ISODate("2025-01-15"),
    "version": 3,
    "data_source": "customer_service"
  }
}
```

#### Key-Value Store Design **[REQUIRED]**
```python
# Redis data modeling for caching and real-time features
import redis
import json
from typing import Dict, Any
from datetime import timedelta

class CustomerCacheManager:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client
        self.default_ttl = timedelta(hours=24)

    def cache_customer_profile(self, customer_id: str, profile: Dict[str, Any]):
        """Cache customer profile with structured keys."""
        key = f"customer:profile:{customer_id}"

        # Store as hash for efficient field access
        pipeline = self.redis.pipeline()
        pipeline.hset(key, mapping={
            "name": profile["name"],
            "email": profile["email"],
            "segment": profile["segment"],
            "last_login": profile["last_login"].isoformat()
        })
        pipeline.expire(key, self.default_ttl)
        pipeline.execute()

    def cache_customer_preferences(self, customer_id: str, preferences: Dict[str, Any]):
        """Cache customer preferences."""
        key = f"customer:preferences:{customer_id}"

        self.redis.setex(
            key,
            self.default_ttl,
            json.dumps(preferences)
        )

    def increment_page_views(self, customer_id: str, page: str):
        """Track customer page views."""
        key = f"customer:pageviews:{customer_id}:{page}"

        pipeline = self.redis.pipeline()
        pipeline.incr(key)
        pipeline.expire(key, timedelta(days=30))
        pipeline.execute()

    def get_recent_activity(self, customer_id: str, limit: int = 10) -> List[Dict]:
        """Get recent customer activity from sorted set."""
        key = f"customer:activity:{customer_id}"

        # Get recent activities (stored with timestamp scores)
        activities = self.redis.zrevrange(key, 0, limit-1, withscores=True)

        return [
            {
                "activity": activity.decode(),
                "timestamp": score
            }
            for activity, score in activities
        ]
```

---

## 4. Streaming Data Processing

### 4.1 Apache Kafka Standards

#### Topic Design **[REQUIRED]**
```yaml
# kafka-topics.yml
topics:
  - name: "customer.events.v1"
    partitions: 12
    replication_factor: 3
    config:
      retention.ms: 2592000000  # 30 days
      cleanup.policy: "delete"
      compression.type: "snappy"
      min.insync.replicas: 2

  - name: "order.events.v1"
    partitions: 24
    replication_factor: 3
    config:
      retention.ms: 7776000000  # 90 days
      cleanup.policy: "delete"
      compression.type: "lz4"
      min.insync.replicas: 2

  - name: "customer.snapshots.v1"
    partitions: 6
    replication_factor: 3
    config:
      cleanup.policy: "compact"
      compression.type: "snappy"
      min.insync.replicas: 2
```

#### Schema Registry Configuration **[REQUIRED]**
```json
// Customer event schema (Avro)
{
  "type": "record",
  "name": "CustomerEvent",
  "namespace": "com.company.events",
  "fields": [
    {
      "name": "event_id",
      "type": "string",
      "doc": "Unique identifier for the event"
    },
    {
      "name": "customer_id",
      "type": "string",
      "doc": "Customer identifier"
    },
    {
      "name": "event_type",
      "type": {
        "type": "enum",
        "name": "EventType",
        "symbols": ["CREATED", "UPDATED", "DELETED", "LOGIN", "LOGOUT", "PURCHASE"]
      }
    },
    {
      "name": "event_time",
      "type": {
        "type": "long",
        "logicalType": "timestamp-millis"
      }
    },
    {
      "name": "event_data",
      "type": [
        "null",
        {
          "type": "map",
          "values": "string"
        }
      ],
      "default": null
    },
    {
      "name": "metadata",
      "type": {
        "type": "record",
        "name": "EventMetadata",
        "fields": [
          {"name": "source", "type": "string"},
          {"name": "version", "type": "string"},
          {"name": "correlation_id", "type": ["null", "string"], "default": null}
        ]
      }
    }
  ]
}
```

#### Kafka Streams Processing **[REQUIRED]**
```java
import org.apache.kafka.streams.KafkaStreams;
import org.apache.kafka.streams.StreamsBuilder;
import org.apache.kafka.streams.kstream.*;
import org.apache.kafka.streams.state.Stores;
import java.time.Duration;

public class CustomerEventProcessor {

    public static void main(String[] args) {
        StreamsBuilder builder = new StreamsBuilder();

        // Input stream
        KStream<String, CustomerEvent> customerEvents = builder
            .stream("customer.events.v1");

        // Filter and transform events
        KStream<String, CustomerEvent> validEvents = customerEvents
            .filter((key, event) -> event.getCustomerId() != null)
            .filter((key, event) -> isValidEvent(event));

        // Aggregate customer activity
        KTable<String, CustomerActivity> customerActivity = validEvents
            .groupByKey()
            .aggregate(
                CustomerActivity::new,
                (key, event, activity) -> activity.addEvent(event),
                Materialized.<String, CustomerActivity>as(
                    Stores.persistentKeyValueStore("customer-activity-store"))
                    .withValueSerde(customerActivitySerde())
            );

        // Create windowed aggregations for real-time metrics
        KTable<Windowed<String>, Long> eventCounts = validEvents
            .groupByKey()
            .windowedBy(TimeWindows.of(Duration.ofMinutes(5)))
            .count(Materialized.as("event-counts-store"));

        // Detect anomalies (high activity)
        KStream<String, Alert> anomalies = eventCounts
            .toStream()
            .filter((window, count) -> count > 100)  // More than 100 events in 5 minutes
            .map((window, count) -> KeyValue.pair(
                window.key(),
                new Alert("HIGH_ACTIVITY", window.key(), count, window.window().start())
            ));

        // Output streams
        customerActivity.toStream().to("customer.activity.v1");
        anomalies.to("customer.alerts.v1");

        // Start the application
        KafkaStreams streams = new KafkaStreams(builder.build(), getStreamsConfig());
        streams.start();

        // Graceful shutdown
        Runtime.getRuntime().addShutdownHook(new Thread(streams::close));
    }

    private static boolean isValidEvent(CustomerEvent event) {
        // Validate event structure and business rules
        return event.getEventTime() != null &&
               event.getEventType() != null &&
               event.getEventTime() > System.currentTimeMillis() - Duration.ofDays(1).toMillis();
    }
}
```

### 4.2 Real-time Analytics

#### Apache Flink Processing **[RECOMMENDED]**
```scala
import org.apache.flink.streaming.api.scala._
import org.apache.flink.streaming.api.windowing.time.Time
import org.apache.flink.streaming.api.windowing.windows.TimeWindow
import org.apache.flink.connector.kafka.source.KafkaSource
import org.apache.flink.api.common.serialization.SimpleStringSchema

object CustomerEventAnalytics {
  def main(args: Array[String]): Unit = {
    val env = StreamExecutionEnvironment.getExecutionEnvironment

    // Configure Kafka source
    val kafkaSource = KafkaSource.builder[String]()
      .setBootstrapServers("localhost:9092")
      .setTopics("customer.events.v1")
      .setGroupId("customer-analytics")
      .setValueOnlyDeserializer(new SimpleStringSchema())
      .build()

    // Create data stream
    val customerEvents = env
      .fromSource(kafkaSource, WatermarkStrategy.noWatermarks(), "Customer Events")
      .map(parseCustomerEvent)
      .assignTimestampsAndWatermarks(
        WatermarkStrategy
          .forBoundedOutOfOrderness[CustomerEvent](Duration.ofSeconds(10))
          .withTimestampAssigner((event, _) => event.eventTime)
      )

    // Real-time aggregations
    val customerMetrics = customerEvents
      .keyBy(_.customerId)
      .window(TumblingEventTimeWindows.of(Time.minutes(5)))
      .aggregate(new CustomerMetricsAggregator)

    // Anomaly detection
    val anomalies = customerEvents
      .keyBy(_.customerId)
      .window(SlidingEventTimeWindows.of(Time.minutes(10), Time.minutes(1)))
      .process(new AnomalyDetector)

    // Output to various sinks
    customerMetrics.addSink(createElasticsearchSink())
    anomalies.addSink(createAlertSink())

    env.execute("Customer Event Analytics")
  }
}

class CustomerMetricsAggregator extends AggregateFunction[CustomerEvent, CustomerMetrics, CustomerMetrics] {
  override def createAccumulator(): CustomerMetrics = new CustomerMetrics()

  override def add(event: CustomerEvent, acc: CustomerMetrics): CustomerMetrics = {
    acc.eventCount += 1
    acc.lastEventTime = event.eventTime
    event.eventType match {
      case "PURCHASE" => acc.purchaseCount += 1
      case "LOGIN" => acc.loginCount += 1
      case _ =>
    }
    acc
  }

  override def getResult(acc: CustomerMetrics): CustomerMetrics = acc

  override def merge(acc1: CustomerMetrics, acc2: CustomerMetrics): CustomerMetrics = {
    acc1.eventCount += acc2.eventCount
    acc1.purchaseCount += acc2.purchaseCount
    acc1.loginCount += acc2.loginCount
    acc1.lastEventTime = Math.max(acc1.lastEventTime, acc2.lastEventTime)
    acc1
  }
}
```

---

## 5. Analytics Engineering

### 5.1 dbt Best Practices

#### Project Structure **[REQUIRED]**
```
analytics/
├── dbt_project.yml
├── packages.yml
├── models/
│   ├── staging/
│   │   ├── _staging.yml
│   │   ├── _sources.yml
│   │   └── stg_customers.sql
│   ├── intermediate/
│   │   ├── _intermediate.yml
│   │   └── int_customer_orders.sql
│   ├── marts/
│   │   ├── core/
│   │   │   ├── _core.yml
│   │   │   ├── dim_customers.sql
│   │   │   └── fct_orders.sql
│   │   └── finance/
│   │       ├── _finance.yml
│   │       └── revenue_metrics.sql
├── macros/
│   ├── generate_schema_name.sql
│   └── test_helpers.sql
├── tests/
│   ├── generic/
│   └── singular/
├── analysis/
├── seeds/
└── snapshots/
```

#### Model Development Standards **[REQUIRED]**
```sql
-- models/staging/stg_customers.sql
{{ config(
    materialized='view',
    tags=['staging', 'customer']
) }}

with source as (
    select * from {{ source('raw_data', 'customers') }}
),

renamed as (
    select
        customer_id,
        customer_name,
        email_address as email,
        phone_number as phone,
        registration_date,
        customer_status,

        -- Standardize dates
        registration_date::date as registration_date_clean,

        -- Clean and validate email
        case
            when email_address ~ '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
            then lower(email_address)
            else null
        end as email_clean,

        -- Audit fields
        _loaded_at,
        _source_file

    from source

    -- Filter out test data
    where customer_id is not null
      and customer_name not ilike '%test%'
      and registration_date >= '2020-01-01'
)

select * from renamed

-- Add tests in schema.yml
```

```yaml
# models/staging/_staging.yml
version: 2

sources:
  - name: raw_data
    description: Raw data from operational systems
    tables:
      - name: customers
        description: Customer master data
        columns:
          - name: customer_id
            description: Unique identifier for customer
            tests:
              - not_null
              - unique
          - name: email_address
            description: Customer email address
            tests:
              - not_null
          - name: registration_date
            description: Date customer registered
            tests:
              - not_null

models:
  - name: stg_customers
    description: Staging model for customer data
    columns:
      - name: customer_id
        description: Unique identifier for customer
        tests:
          - not_null
          - unique
      - name: email_clean
        description: Cleaned and validated email address
        tests:
          - not_null
          - unique
      - name: registration_date_clean
        description: Cleaned registration date
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: '2020-01-01'
              max_value: "{{ var('max_date') }}"
```

#### Macro Development **[REQUIRED]**
```sql
-- macros/generate_surrogate_key.sql
{% macro generate_surrogate_key(columns) %}
    {{ dbt_utils.surrogate_key(columns) }}
{% endmacro %}

-- macros/test_data_freshness.sql
{% macro test_data_freshness(model, timestamp_column, threshold_hours=24) %}
    select count(*)
    from {{ model }}
    where {{ timestamp_column }} < current_timestamp - interval '{{ threshold_hours }} hours'
{% endmacro %}

-- macros/safe_divide.sql
{% macro safe_divide(numerator, denominator) %}
    case
        when {{ denominator }} = 0 then null
        else {{ numerator }} / {{ denominator }}
    end
{% endmacro %}

-- macros/pivot_table.sql
{% macro pivot_table(table_name, group_by_column, pivot_column, value_column, agg_func='sum') %}
    select
        {{ group_by_column }},
        {% for value in dbt_utils.get_column_values(table=table_name, column=pivot_column) %}
        {{ agg_func }}(case when {{ pivot_column }} = '{{ value }}' then {{ value_column }} end) as {{ value }}
        {%- if not loop.last -%},{%- endif -%}
        {% endfor %}
    from {{ table_name }}
    group by {{ group_by_column }}
{% endmacro %}
```

### 5.2 Metrics and KPIs Framework

#### Metrics Definition **[REQUIRED]**
```yaml
# metrics/customer_metrics.yml
version: 2

metrics:
  - name: monthly_active_customers
    label: Monthly Active Customers
    model: ref('fct_customer_activity')
    description: Number of unique customers active in the last 30 days
    type: count_distinct
    sql: customer_id
    timestamp: activity_date
    time_grains: [day, week, month]
    filters:
      - field: activity_date
        operator: '>='
        value: "current_date - 30"
    dimensions:
      - customer_segment
      - acquisition_channel
      - geographic_region

  - name: customer_lifetime_value
    label: Customer Lifetime Value
    model: ref('fct_orders')
    description: Average revenue per customer over their lifetime
    type: average
    sql: total_order_value
    timestamp: order_date
    time_grains: [month, quarter, year]
    dimensions:
      - customer_segment
      - acquisition_channel

  - name: customer_churn_rate
    label: Customer Churn Rate
    model: ref('customer_cohorts')
    description: Percentage of customers who stop purchasing
    type: ratio
    numerator: churned_customers
    denominator: total_customers
    timestamp: cohort_month
    time_grains: [month, quarter]
```

#### Business Logic Layer **[REQUIRED]**
```sql
-- models/marts/core/customer_metrics.sql
{{ config(
    materialized='table',
    indexes=[
        {'columns': ['metric_date'], 'type': 'btree'},
        {'columns': ['customer_segment', 'metric_date'], 'type': 'btree'}
    ]
) }}

with daily_metrics as (
    select
        date_trunc('day', activity_date) as metric_date,
        customer_segment,

        -- Activity metrics
        count(distinct customer_id) as active_customers,
        count(*) as total_activities,

        -- Engagement metrics
        avg(session_duration_minutes) as avg_session_duration,
        sum(page_views) as total_page_views,

        -- Revenue metrics
        sum(order_value) as total_revenue,
        count(distinct case when order_value > 0 then customer_id end) as purchasing_customers,

        -- Calculated metrics
        {{ safe_divide('sum(order_value)', 'count(distinct customer_id)') }} as revenue_per_customer,
        {{ safe_divide(
            'count(distinct case when order_value > 0 then customer_id end)',
            'count(distinct customer_id)'
        ) }} as conversion_rate

    from {{ ref('fct_customer_activity') }}
    where activity_date >= current_date - 90  -- Last 90 days
    group by 1, 2
),

weekly_metrics as (
    select
        date_trunc('week', metric_date) as metric_week,
        customer_segment,

        avg(active_customers) as avg_daily_active_customers,
        sum(total_revenue) as weekly_revenue,
        avg(conversion_rate) as avg_conversion_rate

    from daily_metrics
    group by 1, 2
),

final as (
    select
        metric_date,
        'daily' as metric_grain,
        customer_segment,
        active_customers as metric_value,
        'active_customers' as metric_name,
        current_timestamp as calculated_at
    from daily_metrics

    union all

    select
        metric_week as metric_date,
        'weekly' as metric_grain,
        customer_segment,
        avg_daily_active_customers as metric_value,
        'avg_daily_active_customers' as metric_name,
        current_timestamp as calculated_at
    from weekly_metrics
)

select * from final
```

### 5.3 Data Contracts

#### Schema Contracts **[REQUIRED]**
```yaml
# contracts/customer_data_contract.yml
version: 1.0.0
contract_name: customer_master_data
description: Customer master data contract between systems

provider:
  system: customer_service
  team: customer_experience
  contact: customer-team@company.com

consumer:
  system: analytics_warehouse
  team: data_platform
  contact: data-team@company.com

data_schema:
  table_name: customers
  fields:
    - name: customer_id
      type: string
      required: true
      unique: true
      description: Unique identifier for customer

    - name: email
      type: string
      required: true
      unique: true
      format: email
      description: Customer email address

    - name: created_at
      type: timestamp
      required: true
      description: Customer creation timestamp

    - name: status
      type: string
      required: true
      enum: [active, inactive, suspended]
      description: Customer account status

quality_requirements:
  completeness: 99.5%
  uniqueness: 100%
  validity: 99%
  freshness: 1 hour

sla:
  availability: 99.9%
  max_downtime: 4 hours
  response_time: < 100ms

change_management:
  notification_period: 30 days
  breaking_changes: major version bump
  backward_compatibility: 2 versions
```

#### Contract Testing **[REQUIRED]**
```python
import pandas as pd
from typing import Dict, List
import jsonschema
from dataclasses import dataclass

@dataclass
class ContractViolation:
    field: str
    violation_type: str
    description: str
    severity: str

class DataContractValidator:
    def __init__(self, contract_config: Dict):
        self.contract = contract_config
        self.violations = []

    def validate_schema(self, df: pd.DataFrame) -> List[ContractViolation]:
        """Validate DataFrame against contract schema."""
        violations = []

        # Check required fields
        required_fields = [
            field['name'] for field in self.contract['data_schema']['fields']
            if field.get('required', False)
        ]

        missing_fields = set(required_fields) - set(df.columns)
        for field in missing_fields:
            violations.append(ContractViolation(
                field=field,
                violation_type="missing_required_field",
                description=f"Required field {field} is missing",
                severity="error"
            ))

        # Check data types
        for field_config in self.contract['data_schema']['fields']:
            field_name = field_config['name']
            if field_name not in df.columns:
                continue

            expected_type = field_config['type']
            if not self._validate_field_type(df[field_name], expected_type):
                violations.append(ContractViolation(
                    field=field_name,
                    violation_type="invalid_type",
                    description=f"Field {field_name} has invalid type, expected {expected_type}",
                    severity="error"
                ))

        return violations

    def validate_quality_requirements(self, df: pd.DataFrame) -> List[ContractViolation]:
        """Validate data quality requirements."""
        violations = []
        quality_reqs = self.contract.get('quality_requirements', {})

        # Check completeness
        if 'completeness' in quality_reqs:
            required_completeness = quality_reqs['completeness'] / 100
            actual_completeness = (len(df) - df.isnull().sum().sum()) / (len(df) * len(df.columns))

            if actual_completeness < required_completeness:
                violations.append(ContractViolation(
                    field="overall",
                    violation_type="completeness_violation",
                    description=f"Completeness {actual_completeness:.2%} below required {required_completeness:.2%}",
                    severity="warning"
                ))

        # Check uniqueness for unique fields
        for field_config in self.contract['data_schema']['fields']:
            if field_config.get('unique', False):
                field_name = field_config['name']
                if field_name in df.columns:
                    duplicate_count = df[field_name].duplicated().sum()
                    if duplicate_count > 0:
                        violations.append(ContractViolation(
                            field=field_name,
                            violation_type="uniqueness_violation",
                            description=f"Found {duplicate_count} duplicate values in unique field {field_name}",
                            severity="error"
                        ))

        return violations

    def generate_contract_report(self, df: pd.DataFrame) -> Dict:
        """Generate comprehensive contract validation report."""
        schema_violations = self.validate_schema(df)
        quality_violations = self.validate_quality_requirements(df)

        all_violations = schema_violations + quality_violations

        return {
            "contract_name": self.contract['contract_name'],
            "validation_timestamp": pd.Timestamp.now().isoformat(),
            "total_records": len(df),
            "schema_valid": len(schema_violations) == 0,
            "quality_valid": len(quality_violations) == 0,
            "violations": [
                {
                    "field": v.field,
                    "type": v.violation_type,
                    "description": v.description,
                    "severity": v.severity
                }
                for v in all_violations
            ],
            "summary": {
                "total_violations": len(all_violations),
                "error_count": len([v for v in all_violations if v.severity == "error"]),
                "warning_count": len([v for v in all_violations if v.severity == "warning"])
            }
        }
```

---

## Implementation Checklist

### Pipeline Development
- [ ] ETL/ELT pipelines follow standard structure
- [ ] Error handling and retry logic implemented
- [ ] Data quality checks integrated
- [ ] Monitoring and alerting configured
- [ ] Configuration externalized

### Data Quality
- [ ] Quality rules defined and automated
- [ ] Data profiling implemented
- [ ] Anomaly detection configured
- [ ] Quality metrics tracked
- [ ] Remediation processes defined

### Data Governance
- [ ] Data catalog implemented
- [ ] Lineage tracking automated
- [ ] Classification system defined
- [ ] Access controls implemented
- [ ] Compliance monitoring active

### Streaming Processing
- [ ] Event schemas defined
- [ ] Stream processing topology designed
- [ ] State management configured
- [ ] Error handling implemented
- [ ] Monitoring and alerting setup

### Analytics Engineering
- [ ] dbt project structured properly
- [ ] Models follow layered approach
- [ ] Tests comprehensive
- [ ] Documentation complete
- [ ] CI/CD pipeline configured

### Data Contracts
- [ ] Contracts defined for critical datasets
- [ ] Validation automated
- [ ] Change management process established
- [ ] Monitoring implemented
- [ ] Violation handling defined

---

**End of Data Engineering Standards**
