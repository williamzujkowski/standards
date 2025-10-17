"""
A/B Testing Framework for ML Models with Multi-Armed Bandit algorithms.
Supports Thompson Sampling, Epsilon-Greedy, and UCB strategies.
"""

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional, Tuple

import numpy as np


@dataclass
class ModelMetrics:
    """Metrics for a single model variant."""

    model_id: str
    total_requests: int = 0
    successful_predictions: int = 0
    failed_predictions: int = 0
    total_reward: float = 0.0
    avg_latency_ms: float = 0.0

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_predictions / self.total_requests

    @property
    def avg_reward(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.total_reward / self.total_requests


class BanditStrategy(ABC):
    """Abstract base class for bandit algorithms."""

    @abstractmethod
    def select_model(self, metrics: Dict[str, ModelMetrics]) -> str:
        """Select which model to use."""
        pass

    @abstractmethod
    def update(self, model_id: str, reward: float):
        """Update algorithm state after receiving reward."""
        pass


class ThompsonSampling(BanditStrategy):
    """Thompson Sampling algorithm using Beta distribution."""

    def __init__(self, model_ids: List[str], prior_alpha: float = 1.0, prior_beta: float = 1.0):
        self.model_ids = model_ids
        # Beta distribution parameters (successes, failures)
        self.alpha = {model_id: prior_alpha for model_id in model_ids}
        self.beta = {model_id: prior_beta for model_id in model_ids}

    def select_model(self, metrics: Dict[str, ModelMetrics]) -> str:
        """Select model by sampling from Beta distributions."""
        samples = {model_id: np.random.beta(self.alpha[model_id], self.beta[model_id]) for model_id in self.model_ids}
        return max(samples, key=samples.get)

    def update(self, model_id: str, reward: float):
        """Update Beta distribution parameters."""
        if reward > 0.5:  # Success
            self.alpha[model_id] += 1
        else:  # Failure
            self.beta[model_id] += 1

    def get_statistics(self) -> Dict:
        """Get current statistics for each model."""
        return {
            model_id: {
                "alpha": self.alpha[model_id],
                "beta": self.beta[model_id],
                "expected_reward": self.alpha[model_id] / (self.alpha[model_id] + self.beta[model_id]),
                "confidence_interval": self._compute_ci(model_id),
            }
            for model_id in self.model_ids
        }

    def _compute_ci(self, model_id: str, confidence: float = 0.95) -> Tuple[float, float]:
        """Compute confidence interval for model's success rate."""
        from scipy.stats import beta

        alpha, beta_val = self.alpha[model_id], self.beta[model_id]
        lower = beta.ppf((1 - confidence) / 2, alpha, beta_val)
        upper = beta.ppf(1 - (1 - confidence) / 2, alpha, beta_val)
        return (lower, upper)


class EpsilonGreedy(BanditStrategy):
    """Epsilon-Greedy algorithm."""

    def __init__(self, model_ids: List[str], epsilon: float = 0.1, decay: float = 0.999):
        self.model_ids = model_ids
        self.epsilon = epsilon
        self.initial_epsilon = epsilon
        self.decay = decay
        self.rewards = {model_id: [] for model_id in model_ids}

    def select_model(self, metrics: Dict[str, ModelMetrics]) -> str:
        """Select model using epsilon-greedy strategy."""
        # Exploration
        if np.random.random() < self.epsilon:
            return np.random.choice(self.model_ids)

        # Exploitation
        avg_rewards = {
            model_id: np.mean(self.rewards[model_id]) if self.rewards[model_id] else 0 for model_id in self.model_ids
        }
        return max(avg_rewards, key=avg_rewards.get)

    def update(self, model_id: str, reward: float):
        """Update rewards and decay epsilon."""
        self.rewards[model_id].append(reward)
        self.epsilon *= self.decay

    def get_statistics(self) -> Dict:
        """Get current statistics."""
        return {
            model_id: {
                "avg_reward": np.mean(self.rewards[model_id]) if self.rewards[model_id] else 0,
                "total_samples": len(self.rewards[model_id]),
            }
            for model_id in self.model_ids
        } | {"current_epsilon": self.epsilon}


class UCB(BanditStrategy):
    """Upper Confidence Bound algorithm."""

    def __init__(self, model_ids: List[str], exploration_factor: float = 2.0):
        self.model_ids = model_ids
        self.exploration_factor = exploration_factor
        self.counts = {model_id: 0 for model_id in model_ids}
        self.values = {model_id: 0.0 for model_id in model_ids}
        self.total_counts = 0

    def select_model(self, metrics: Dict[str, ModelMetrics]) -> str:
        """Select model using UCB formula."""
        # Ensure all models tried at least once
        for model_id in self.model_ids:
            if self.counts[model_id] == 0:
                return model_id

        # UCB calculation
        ucb_values = {}
        for model_id in self.model_ids:
            avg_value = self.values[model_id] / self.counts[model_id]
            exploration_bonus = self.exploration_factor * np.sqrt(np.log(self.total_counts) / self.counts[model_id])
            ucb_values[model_id] = avg_value + exploration_bonus

        return max(ucb_values, key=ucb_values.get)

    def update(self, model_id: str, reward: float):
        """Update counts and values."""
        self.counts[model_id] += 1
        self.values[model_id] += reward
        self.total_counts += 1

    def get_statistics(self) -> Dict:
        """Get current statistics."""
        return {
            model_id: {
                "avg_reward": self.values[model_id] / self.counts[model_id] if self.counts[model_id] > 0 else 0,
                "count": self.counts[model_id],
                "ucb_value": self.values[model_id] / self.counts[model_id]
                + self.exploration_factor * np.sqrt(np.log(self.total_counts) / (self.counts[model_id] + 1)),
            }
            for model_id in self.model_ids
        }


class ABTestingFramework:
    """Complete A/B testing framework for ML models."""

    def __init__(self, model_ids: List[str], strategy: str = "thompson", strategy_params: Optional[Dict] = None):
        self.model_ids = model_ids
        self.metrics = {model_id: ModelMetrics(model_id) for model_id in model_ids}

        # Initialize bandit strategy
        strategy_params = strategy_params or {}
        if strategy == "thompson":
            self.bandit = ThompsonSampling(model_ids, **strategy_params)
        elif strategy == "epsilon_greedy":
            self.bandit = EpsilonGreedy(model_ids, **strategy_params)
        elif strategy == "ucb":
            self.bandit = UCB(model_ids, **strategy_params)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

        self.experiment_log = []

    def select_model(self) -> str:
        """Select model for serving."""
        return self.bandit.select_model(self.metrics)

    def record_result(
        self, model_id: str, reward: float, success: bool, latency_ms: float, metadata: Optional[Dict] = None
    ):
        """Record result of model prediction."""
        # Update metrics
        metrics = self.metrics[model_id]
        metrics.total_requests += 1
        metrics.total_reward += reward

        if success:
            metrics.successful_predictions += 1
        else:
            metrics.failed_predictions += 1

        # Update average latency (running average)
        metrics.avg_latency_ms = (
            metrics.avg_latency_ms * (metrics.total_requests - 1) + latency_ms
        ) / metrics.total_requests

        # Update bandit
        self.bandit.update(model_id, reward)

        # Log experiment
        self.experiment_log.append(
            {
                "timestamp": datetime.now().isoformat(),
                "model_id": model_id,
                "reward": reward,
                "success": success,
                "latency_ms": latency_ms,
                "metadata": metadata or {},
            }
        )

    def get_metrics(self) -> Dict[str, ModelMetrics]:
        """Get current metrics for all models."""
        return self.metrics

    def get_statistics(self) -> Dict:
        """Get comprehensive statistics."""
        model_stats = {
            model_id: {
                "total_requests": metrics.total_requests,
                "success_rate": metrics.success_rate,
                "avg_reward": metrics.avg_reward,
                "avg_latency_ms": metrics.avg_latency_ms,
            }
            for model_id, metrics in self.metrics.items()
        }

        bandit_stats = self.bandit.get_statistics()

        return {
            "model_metrics": model_stats,
            "bandit_statistics": bandit_stats,
            "total_requests": sum(m.total_requests for m in self.metrics.values()),
        }

    def determine_winner(self, confidence: float = 0.95, min_samples: int = 100) -> Optional[str]:
        """
        Determine if there's a statistically significant winner.

        Returns:
            model_id of winner, or None if no clear winner
        """
        # Check minimum sample size
        if any(m.total_requests < min_samples for m in self.metrics.values()):
            return None

        # Statistical test for winner (simplified)
        success_rates = {model_id: metrics.success_rate for model_id, metrics in self.metrics.items()}

        best_model = max(success_rates, key=success_rates.get)
        best_rate = success_rates[best_model]

        # Check if best model is significantly better
        for model_id, rate in success_rates.items():
            if model_id != best_model:
                # Simple threshold: best must be X% better
                if best_rate < rate * 1.1:  # 10% better threshold
                    return None

        return best_model

    def export_results(self, filepath: str):
        """Export experiment results to JSON."""
        results = {
            "statistics": self.get_statistics(),
            "experiment_log": self.experiment_log[-1000:],  # Last 1000 entries
        }

        with open(filepath, "w") as f:
            json.dump(results, f, indent=2)

    def generate_report(self) -> str:
        """Generate human-readable report."""
        stats = self.get_statistics()

        report = ["=" * 80]
        report.append("A/B TESTING REPORT")
        report.append("=" * 80)
        report.append(f"\nTotal Requests: {stats['total_requests']}")

        report.append("\n" + "-" * 80)
        report.append("MODEL PERFORMANCE")
        report.append("-" * 80)

        for model_id, metrics in stats["model_metrics"].items():
            report.append(f"\nModel: {model_id}")
            report.append(f"  Requests: {metrics['total_requests']}")
            report.append(f"  Success Rate: {metrics['success_rate']:.2%}")
            report.append(f"  Avg Reward: {metrics['avg_reward']:.4f}")
            report.append(f"  Avg Latency: {metrics['avg_latency_ms']:.2f}ms")

        report.append("\n" + "-" * 80)
        report.append("BANDIT STATISTICS")
        report.append("-" * 80)
        report.append(json.dumps(stats["bandit_statistics"], indent=2))

        # Determine winner
        winner = self.determine_winner()
        if winner:
            report.append(f"\n🏆 WINNER: {winner}")
        else:
            report.append("\n⏳ No clear winner yet - continue testing")

        report.append("\n" + "=" * 80)

        return "\n".join(report)


# Example Usage
if __name__ == "__main__":
    # Initialize A/B testing framework
    framework = ABTestingFramework(
        model_ids=["model_v1", "model_v2", "model_v3"],
        strategy="thompson",
        strategy_params={"prior_alpha": 1.0, "prior_beta": 1.0},
    )

    # Simulate requests
    np.random.seed(42)

    # Model v2 is best (80% success), v1 is 70%, v3 is 60%
    true_success_rates = {"model_v1": 0.70, "model_v2": 0.80, "model_v3": 0.60}

    print("Running A/B test simulation...\n")

    for i in range(1000):
        # Select model using bandit
        selected_model = framework.select_model()

        # Simulate prediction
        success = np.random.random() < true_success_rates[selected_model]
        reward = 1.0 if success else 0.0
        latency_ms = np.random.normal(50, 10)  # Simulated latency

        # Record result
        framework.record_result(model_id=selected_model, reward=reward, success=success, latency_ms=latency_ms)

        # Print progress
        if (i + 1) % 200 == 0:
            print(f"Iteration {i + 1}:")
            stats = framework.get_statistics()
            for model_id, metrics in stats["model_metrics"].items():
                print(f"  {model_id}: {metrics['total_requests']} requests, {metrics['success_rate']:.2%} success")
            print()

    # Generate final report
    print("\n" + framework.generate_report())

    # Export results
    framework.export_results("ab_test_results.json")
    print("\nResults exported to ab_test_results.json")
