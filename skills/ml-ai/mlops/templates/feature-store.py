"""
Feature Store implementation using Feast for online and offline feature serving.
"""

from datetime import datetime, timedelta

import pandas as pd
from feast import Entity, Feature, FeatureStore, FeatureView, FileSource, ValueType
from feast.types import Float32, Int64, String


# Feature Repository Configuration
# Save as: feature_repo/feature_store.yaml
FEATURE_STORE_YAML = """
project: fraud_detection
registry: data/registry.db
provider: local
online_store:
  type: sqlite
  path: data/online_store.db
offline_store:
  type: file
entity_key_serialization_version: 2
"""

# Define Entities
user = Entity(name="user_id", value_type=ValueType.INT64, description="User identifier")

merchant = Entity(name="merchant_id", value_type=ValueType.INT64, description="Merchant identifier")

transaction = Entity(name="transaction_id", value_type=ValueType.STRING, description="Transaction identifier")

# Define Feature Sources
user_features_source = FileSource(
    path="data/user_features.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp",
)

transaction_features_source = FileSource(
    path="data/transaction_features.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp",
)

merchant_features_source = FileSource(
    path="data/merchant_features.parquet",
    event_timestamp_column="event_timestamp",
    created_timestamp_column="created_timestamp",
)

# Define Feature Views
user_features = FeatureView(
    name="user_features",
    entities=["user_id"],
    ttl=timedelta(days=7),
    features=[
        Feature(name="transaction_count_7d", dtype=Int64),
        Feature(name="transaction_count_30d", dtype=Int64),
        Feature(name="avg_transaction_amount", dtype=Float32),
        Feature(name="max_transaction_amount", dtype=Float32),
        Feature(name="account_age_days", dtype=Int64),
        Feature(name="failed_login_attempts", dtype=Int64),
        Feature(name="device_change_frequency", dtype=Float32),
    ],
    online=True,
    source=user_features_source,
    tags={"team": "fraud_detection", "priority": "high"},
)

transaction_features = FeatureView(
    name="transaction_features",
    entities=["transaction_id"],
    ttl=timedelta(hours=24),
    features=[
        Feature(name="amount", dtype=Float32),
        Feature(name="hour_of_day", dtype=Int64),
        Feature(name="day_of_week", dtype=Int64),
        Feature(name="is_international", dtype=Int64),
        Feature(name="distance_from_last_transaction_km", dtype=Float32),
        Feature(name="time_since_last_transaction_minutes", dtype=Float32),
    ],
    online=True,
    source=transaction_features_source,
    tags={"team": "fraud_detection"},
)

merchant_features = FeatureView(
    name="merchant_features",
    entities=["merchant_id"],
    ttl=timedelta(days=30),
    features=[
        Feature(name="fraud_rate_7d", dtype=Float32),
        Feature(name="fraud_rate_30d", dtype=Float32),
        Feature(name="avg_transaction_amount", dtype=Float32),
        Feature(name="merchant_age_days", dtype=Int64),
        Feature(name="category", dtype=String),
        Feature(name="risk_score", dtype=Float32),
    ],
    online=True,
    source=merchant_features_source,
    tags={"team": "fraud_detection"},
)


class FeatureStoreManager:
    """Manager for feature engineering and serving."""

    def __init__(self, repo_path: str = "feature_repo/"):
        self.store = FeatureStore(repo_path=repo_path)

    def apply_feature_definitions(self):
        """Apply feature definitions to the feature store."""
        # This would be done via: feast apply

    def generate_training_features(self, entity_df: pd.DataFrame, feature_refs: list[str]) -> pd.DataFrame:
        """
        Generate features for model training (historical/offline features).

        Args:
            entity_df: DataFrame with entity keys and timestamps
            feature_refs: List of feature references (e.g., "user_features:transaction_count_7d")

        Returns:
            DataFrame with features joined
        """
        training_df = self.store.get_historical_features(entity_df=entity_df, features=feature_refs).to_df()

        return training_df

    def get_online_features(self, entity_rows: list[dict], feature_refs: list[str]) -> dict:
        """
        Get online features for real-time inference.

        Args:
            entity_rows: List of entity dictionaries
            feature_refs: List of feature references

        Returns:
            Dictionary of features
        """
        features = self.store.get_online_features(features=feature_refs, entity_rows=entity_rows).to_dict()

        return features

    def materialize_features(self, start_date: datetime, end_date: datetime, feature_views: list[str] = None):
        """
        Materialize features from offline to online store.

        Args:
            start_date: Start of time range
            end_date: End of time range
            feature_views: Specific feature views to materialize (None = all)
        """
        self.store.materialize(start_date=start_date, end_date=end_date, feature_views=feature_views)

    def materialize_incremental(self, end_date: datetime):
        """Incrementally materialize new features."""
        self.store.materialize_incremental(end_date=end_date)


# Feature Engineering Pipeline
class FeatureEngineer:
    """Feature engineering transformations."""

    @staticmethod
    def engineer_user_features(user_transactions: pd.DataFrame) -> pd.DataFrame:
        """Engineer user-level features."""

        # Time-based aggregations
        user_features = (
            user_transactions.groupby("user_id")
            .agg({"transaction_id": "count", "amount": ["mean", "max", "std"], "is_fraud": "mean"})
            .reset_index()
        )

        user_features.columns = [
            "user_id",
            "transaction_count",
            "avg_transaction_amount",
            "max_transaction_amount",
            "transaction_amount_std",
            "fraud_rate",
        ]

        # Account age
        user_features["account_creation_date"] = pd.to_datetime(user_transactions.groupby("user_id")["timestamp"].min())
        user_features["account_age_days"] = (datetime.now() - user_features["account_creation_date"]).dt.days

        # Timestamps for Feast
        user_features["event_timestamp"] = datetime.now()
        user_features["created_timestamp"] = datetime.now()

        return user_features

    @staticmethod
    def engineer_transaction_features(current_transaction: dict, user_history: pd.DataFrame) -> dict:
        """Engineer transaction-level features."""

        features = {}

        # Time-based features
        current_time = pd.to_datetime(current_transaction["timestamp"])
        features["hour_of_day"] = current_time.hour
        features["day_of_week"] = current_time.dayofweek
        features["is_weekend"] = int(current_time.dayofweek >= 5)

        # Velocity features
        if not user_history.empty:
            last_transaction = user_history.iloc[-1]
            time_diff = (current_time - pd.to_datetime(last_transaction["timestamp"])).total_seconds() / 60
            features["time_since_last_transaction_minutes"] = time_diff

            # Location features
            if "latitude" in current_transaction and "longitude" in current_transaction:
                distance = FeatureEngineer._haversine_distance(
                    current_transaction["latitude"],
                    current_transaction["longitude"],
                    last_transaction["latitude"],
                    last_transaction["longitude"],
                )
                features["distance_from_last_transaction_km"] = distance
        else:
            features["time_since_last_transaction_minutes"] = 0
            features["distance_from_last_transaction_km"] = 0

        # Amount features
        features["amount"] = current_transaction["amount"]
        features["is_round_amount"] = int(current_transaction["amount"] % 1 == 0)

        # International transaction
        features["is_international"] = int(
            current_transaction.get("country") != current_transaction.get("merchant_country")
        )

        return features

    @staticmethod
    def _haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two points in km."""
        from math import asin, cos, radians, sin, sqrt

        # Convert to radians
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        km = 6371 * c

        return km


# Example Usage
if __name__ == "__main__":
    # Initialize feature store manager
    fs_manager = FeatureStoreManager()

    # Example 1: Generate training features
    print("Example 1: Historical features for training")
    entity_df = pd.DataFrame(
        {
            "user_id": [1, 2, 3],
            "merchant_id": [101, 102, 103],
            "event_timestamp": [datetime(2025, 1, 1), datetime(2025, 1, 2), datetime(2025, 1, 3)],
        }
    )

    feature_refs = [
        "user_features:transaction_count_7d",
        "user_features:avg_transaction_amount",
        "merchant_features:fraud_rate_7d",
        "merchant_features:risk_score",
    ]

    training_features = fs_manager.generate_training_features(entity_df, feature_refs)
    print(training_features.head())

    # Example 2: Online features for inference
    print("\nExample 2: Online features for real-time prediction")
    entity_rows = [{"user_id": 1, "merchant_id": 101}]

    online_features = fs_manager.get_online_features(entity_rows, feature_refs)
    print(online_features)

    # Example 3: Feature engineering
    print("\nExample 3: Feature engineering")
    engineer = FeatureEngineer()

    # Sample transaction history
    user_transactions = pd.DataFrame(
        {
            "user_id": [1, 1, 1, 2, 2],
            "transaction_id": ["t1", "t2", "t3", "t4", "t5"],
            "amount": [100, 50, 200, 75, 300],
            "is_fraud": [0, 0, 0, 1, 0],
            "timestamp": pd.date_range("2025-01-01", periods=5, freq="D"),
        }
    )

    user_features = engineer.engineer_user_features(user_transactions)
    print("\nEngineered user features:")
    print(user_features)

    # Example 4: Materialize features
    print("\nExample 4: Materializing features to online store")
    fs_manager.materialize_incremental(end_date=datetime.now())
    print("Features materialized successfully")
