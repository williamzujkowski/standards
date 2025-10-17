"""
Comprehensive drift detection system for production ML models.
Includes statistical tests, distribution comparisons, and alerting.
"""
import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import jensenshannon
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')

class DriftDetector:
    """
    Multi-method drift detection for numerical and categorical features.
    
    Methods:
    - Kolmogorov-Smirnov test (numerical)
    - Population Stability Index (numerical)
    - Jensen-Shannon divergence (numerical)
    - Chi-square test (categorical)
    - Total Variation Distance (categorical)
    """
    
    def __init__(
        self,
        reference_data: pd.DataFrame,
        feature_types: Dict[str, str],
        significance_level: float = 0.05,
        psi_threshold: float = 0.1,
        js_threshold: float = 0.1
    ):
        """
        Initialize drift detector with reference data.
        
        Args:
            reference_data: Training/baseline data
            feature_types: Dict mapping feature names to types ('numerical' or 'categorical')
            significance_level: P-value threshold for statistical tests
            psi_threshold: PSI threshold for drift detection
            js_threshold: Jensen-Shannon divergence threshold
        """
        self.reference_data = reference_data
        self.feature_types = feature_types
        self.significance_level = significance_level
        self.psi_threshold = psi_threshold
        self.js_threshold = js_threshold
        
        # Precompute reference statistics
        self.reference_stats = self._compute_reference_statistics()
    
    def _compute_reference_statistics(self) -> Dict:
        """Precompute statistics from reference data."""
        stats_dict = {}
        
        for feature, ftype in self.feature_types.items():
            if feature not in self.reference_data.columns:
                continue
            
            if ftype == 'numerical':
                values = self.reference_data[feature].dropna()
                stats_dict[feature] = {
                    'type': 'numerical',
                    'mean': values.mean(),
                    'std': values.std(),
                    'quantiles': np.percentile(values, [0, 25, 50, 75, 100]),
                    'distribution': values.values
                }
            elif ftype == 'categorical':
                value_counts = self.reference_data[feature].value_counts(normalize=True)
                stats_dict[feature] = {
                    'type': 'categorical',
                    'categories': value_counts.index.tolist(),
                    'frequencies': value_counts.values,
                    'value_counts': value_counts.to_dict()
                }
        
        return stats_dict
    
    def detect_drift(self, current_data: pd.DataFrame) -> Dict:
        """
        Detect drift in all features.
        
        Args:
            current_data: Production data to compare against reference
        
        Returns:
            Dictionary containing drift detection results per feature
        """
        results = {
            'overall_drift': False,
            'features_with_drift': [],
            'feature_results': {}
        }
        
        for feature, ref_stats in self.reference_stats.items():
            if feature not in current_data.columns:
                continue
            
            if ref_stats['type'] == 'numerical':
                feature_result = self._detect_numerical_drift(
                    feature,
                    current_data[feature].dropna().values,
                    ref_stats
                )
            else:
                feature_result = self._detect_categorical_drift(
                    feature,
                    current_data[feature],
                    ref_stats
                )
            
            results['feature_results'][feature] = feature_result
            
            if feature_result['drift_detected']:
                results['features_with_drift'].append(feature)
                results['overall_drift'] = True
        
        return results
    
    def _detect_numerical_drift(
        self,
        feature: str,
        current_values: np.ndarray,
        ref_stats: Dict
    ) -> Dict:
        """Detect drift in numerical features using multiple methods."""
        
        ref_values = ref_stats['distribution']
        
        # 1. Kolmogorov-Smirnov Test
        ks_stat, ks_pvalue = stats.ks_2samp(ref_values, current_values)
        ks_drift = ks_pvalue < self.significance_level
        
        # 2. Population Stability Index (PSI)
        psi = self._calculate_psi(ref_values, current_values)
        psi_drift = psi > self.psi_threshold
        
        # 3. Jensen-Shannon Divergence
        js_div = self._calculate_jensen_shannon(ref_values, current_values)
        js_drift = js_div > self.js_threshold
        
        # 4. Statistical summary comparison
        current_mean = np.mean(current_values)
        current_std = np.std(current_values)
        mean_shift = abs(current_mean - ref_stats['mean']) / (ref_stats['std'] + 1e-6)
        
        # Overall drift decision (any method triggers)
        drift_detected = ks_drift or psi_drift or js_drift
        
        return {
            'feature': feature,
            'type': 'numerical',
            'drift_detected': drift_detected,
            'methods': {
                'kolmogorov_smirnov': {
                    'statistic': float(ks_stat),
                    'p_value': float(ks_pvalue),
                    'drift': ks_drift
                },
                'psi': {
                    'value': float(psi),
                    'threshold': self.psi_threshold,
                    'drift': psi_drift
                },
                'jensen_shannon': {
                    'value': float(js_div),
                    'threshold': self.js_threshold,
                    'drift': js_drift
                }
            },
            'statistics': {
                'reference_mean': float(ref_stats['mean']),
                'current_mean': float(current_mean),
                'reference_std': float(ref_stats['std']),
                'current_std': float(current_std),
                'mean_shift_magnitude': float(mean_shift)
            },
            'severity': self._compute_severity(max(ks_stat, psi, js_div))
        }
    
    def _detect_categorical_drift(
        self,
        feature: str,
        current_series: pd.Series,
        ref_stats: Dict
    ) -> Dict:
        """Detect drift in categorical features."""
        
        # Current value counts
        current_value_counts = current_series.value_counts(normalize=True)
        
        # Align categories
        all_categories = set(ref_stats['categories']) | set(current_value_counts.index)
        ref_freq = [ref_stats['value_counts'].get(cat, 0) for cat in all_categories]
        curr_freq = [current_value_counts.get(cat, 0) for cat in all_categories]
        
        # 1. Chi-square test
        # Add small constant to avoid zero frequencies
        ref_freq_adj = [f + 1e-6 for f in ref_freq]
        curr_freq_adj = [f + 1e-6 for f in curr_freq]
        
        chi2_stat, chi2_pvalue = stats.chisquare(curr_freq_adj, ref_freq_adj)
        chi2_drift = chi2_pvalue < self.significance_level
        
        # 2. Total Variation Distance
        tvd = 0.5 * sum(abs(r - c) for r, c in zip(ref_freq, curr_freq))
        tvd_drift = tvd > 0.1  # Typical threshold
        
        # 3. Category changes
        new_categories = set(current_value_counts.index) - set(ref_stats['categories'])
        missing_categories = set(ref_stats['categories']) - set(current_value_counts.index)
        
        drift_detected = chi2_drift or tvd_drift or len(new_categories) > 0
        
        return {
            'feature': feature,
            'type': 'categorical',
            'drift_detected': drift_detected,
            'methods': {
                'chi_square': {
                    'statistic': float(chi2_stat),
                    'p_value': float(chi2_pvalue),
                    'drift': chi2_drift
                },
                'total_variation_distance': {
                    'value': float(tvd),
                    'drift': tvd_drift
                }
            },
            'category_changes': {
                'new_categories': list(new_categories),
                'missing_categories': list(missing_categories)
            },
            'severity': self._compute_severity(tvd)
        }
    
    def _calculate_psi(
        self,
        reference: np.ndarray,
        current: np.ndarray,
        bins: int = 10
    ) -> float:
        """Calculate Population Stability Index."""
        
        # Create bins based on reference distribution
        bin_edges = np.percentile(reference, np.linspace(0, 100, bins + 1))
        bin_edges = np.unique(bin_edges)  # Remove duplicates
        
        # Histogram counts
        ref_counts, _ = np.histogram(reference, bins=bin_edges)
        curr_counts, _ = np.histogram(current, bins=bin_edges)
        
        # Convert to proportions
        ref_props = ref_counts / len(reference)
        curr_props = curr_counts / len(current)
        
        # Avoid log(0)
        ref_props = np.where(ref_props == 0, 0.0001, ref_props)
        curr_props = np.where(curr_props == 0, 0.0001, curr_props)
        
        # PSI calculation
        psi = np.sum((curr_props - ref_props) * np.log(curr_props / ref_props))
        
        return psi
    
    def _calculate_jensen_shannon(
        self,
        reference: np.ndarray,
        current: np.ndarray,
        bins: int = 50
    ) -> float:
        """Calculate Jensen-Shannon divergence."""
        
        # Create common bins
        all_data = np.concatenate([reference, current])
        bin_edges = np.histogram_bin_edges(all_data, bins=bins)
        
        # Histograms
        ref_hist, _ = np.histogram(reference, bins=bin_edges, density=True)
        curr_hist, _ = np.histogram(current, bins=bin_edges, density=True)
        
        # Normalize to probability distributions
        ref_hist = ref_hist / (np.sum(ref_hist) + 1e-10)
        curr_hist = curr_hist / (np.sum(curr_hist) + 1e-10)
        
        # Jensen-Shannon divergence
        js_div = jensenshannon(ref_hist, curr_hist)
        
        return js_div
    
    def _compute_severity(self, score: float) -> str:
        """Compute drift severity level."""
        if score < 0.1:
            return "low"
        elif score < 0.25:
            return "medium"
        elif score < 0.5:
            return "high"
        else:
            return "critical"
    
    def generate_report(self, drift_results: Dict) -> str:
        """Generate human-readable drift report."""
        
        report = ["=" * 80]
        report.append("DRIFT DETECTION REPORT")
        report.append("=" * 80)
        
        if drift_results['overall_drift']:
            report.append(f"\n⚠️  DRIFT DETECTED in {len(drift_results['features_with_drift'])} feature(s)")
            report.append(f"Features: {', '.join(drift_results['features_with_drift'])}")
        else:
            report.append("\n✓ No significant drift detected")
        
        report.append("\n" + "-" * 80)
        report.append("FEATURE-LEVEL RESULTS")
        report.append("-" * 80)
        
        for feature, result in drift_results['feature_results'].items():
            report.append(f"\nFeature: {feature}")
            report.append(f"  Type: {result['type']}")
            report.append(f"  Drift: {'YES' if result['drift_detected'] else 'NO'}")
            
            if result['drift_detected']:
                report.append(f"  Severity: {result['severity'].upper()}")
            
            report.append("  Methods:")
            for method_name, method_result in result['methods'].items():
                drift_status = "DRIFT" if method_result.get('drift', False) else "OK"
                report.append(f"    - {method_name}: {drift_status}")
                if 'value' in method_result:
                    report.append(f"      Value: {method_result['value']:.4f}")
                if 'p_value' in method_result:
                    report.append(f"      P-value: {method_result['p_value']:.4f}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)


# Example usage
if __name__ == "__main__":
    # Generate sample data
    np.random.seed(42)
    
    # Reference (training) data
    ref_df = pd.DataFrame({
        'numerical_1': np.random.normal(0, 1, 10000),
        'numerical_2': np.random.exponential(2, 10000),
        'categorical_1': np.random.choice(['A', 'B', 'C'], 10000, p=[0.5, 0.3, 0.2])
    })
    
    # Current (production) data with drift
    curr_df = pd.DataFrame({
        'numerical_1': np.random.normal(0.5, 1.2, 1000),  # Shifted mean and variance
        'numerical_2': np.random.exponential(2.5, 1000),  # Changed distribution
        'categorical_1': np.random.choice(['A', 'B', 'C', 'D'], 1000, p=[0.4, 0.3, 0.2, 0.1])  # New category
    })
    
    # Define feature types
    feature_types = {
        'numerical_1': 'numerical',
        'numerical_2': 'numerical',
        'categorical_1': 'categorical'
    }
    
    # Initialize detector
    detector = DriftDetector(
        reference_data=ref_df,
        feature_types=feature_types,
        significance_level=0.05,
        psi_threshold=0.1,
        js_threshold=0.1
    )
    
    # Detect drift
    drift_results = detector.detect_drift(curr_df)
    
    # Generate report
    report = detector.generate_report(drift_results)
    print(report)
    
    # Example: Integration with monitoring
    if drift_results['overall_drift']:
        print("\n🚨 Triggering retraining pipeline...")
        # send_alert_to_slack(drift_results)
        # trigger_retraining_job()
