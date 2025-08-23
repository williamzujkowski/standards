#!/usr/bin/env python3
"""
Repository Performance Monitor

This script monitors performance of repository operations including:
- Git operations
- File system operations
- Script execution times
- Memory and CPU usage
- Validation and processing times
"""

import json
import logging
import os
import statistics
import subprocess
import time
from datetime import datetime, timedelta

import psutil


class PerformanceMonitor:
    """Monitor and track repository operation performance"""

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        self.metrics_dir = os.path.join(self.repo_path, "monitoring", "metrics")
        self.logs_dir = os.path.join(self.repo_path, "monitoring", "logs")

        # Ensure directories exist
        os.makedirs(self.metrics_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename=os.path.join(self.logs_dir, "performance.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # Performance thresholds
        self.thresholds = {
            "git_operation_warning": 5.0,  # seconds
            "git_operation_critical": 15.0,  # seconds
            "file_read_warning": 1.0,  # seconds
            "file_read_critical": 5.0,  # seconds
            "script_execution_warning": 10.0,  # seconds
            "script_execution_critical": 30.0,  # seconds
            "memory_usage_warning": 80,  # percentage
            "memory_usage_critical": 95,  # percentage
            "cpu_usage_warning": 80,  # percentage
            "cpu_usage_critical": 95,  # percentage
        }

    def monitor_git_operations(self):
        """Monitor Git operation performance"""
        operations = [
            ("status", ["git", "status", "--porcelain"]),
            ("log", ["git", "log", "--oneline", "-10"]),
            ("diff", ["git", "diff", "--stat"]),
            ("branch", ["git", "branch", "-a"]),
            ("remote", ["git", "remote", "-v"]),
        ]

        git_metrics = {}

        for op_name, cmd in operations:
            try:
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

                result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.repo_path, timeout=30)

                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024  # MB

                execution_time = end_time - start_time
                memory_used = end_memory - start_memory

                git_metrics[op_name] = {
                    "execution_time": execution_time,
                    "memory_used_mb": memory_used,
                    "success": result.returncode == 0,
                    "output_size": len(result.stdout) + len(result.stderr),
                    "status": self._get_performance_status("git_operation", execution_time),
                }

                if execution_time > self.thresholds["git_operation_warning"]:
                    self.logger.warning(f"Git {op_name} operation slow: {execution_time:.2f}s")

            except subprocess.TimeoutExpired:
                git_metrics[op_name] = {
                    "execution_time": 30,
                    "success": False,
                    "error": "timeout",
                    "status": "critical",
                }
                self.logger.error(f"Git {op_name} operation timed out")

            except Exception as e:
                git_metrics[op_name] = {
                    "execution_time": 0,
                    "success": False,
                    "error": str(e),
                    "status": "error",
                }
                self.logger.error(f"Git {op_name} operation failed: {e}")

        return git_metrics

    def monitor_file_operations(self):
        """Monitor file system operation performance"""
        test_files = [
            "README.md",
            "config/MANIFEST.yaml",
            "docs/standards/CODING_STANDARDS.md",
            "docs/standards/MODERN_SECURITY_STANDARDS.md",
            "docs/standards/UNIFIED_STANDARDS.md",
        ]

        file_metrics = {}

        for file_path in test_files:
            full_path = os.path.join(self.repo_path, file_path)
            if not os.path.exists(full_path):
                continue

            try:
                # Test file read performance
                start_time = time.time()
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()
                read_time = time.time() - start_time

                # Test file stat performance
                start_time = time.time()
                os.stat(full_path)
                stat_time = time.time() - start_time

                file_size = len(content)
                read_speed = file_size / read_time if read_time > 0 else 0

                file_metrics[file_path] = {
                    "read_time": read_time,
                    "stat_time": stat_time,
                    "file_size": file_size,
                    "read_speed_bytes_per_sec": read_speed,
                    "read_speed_mb_per_sec": read_speed / (1024 * 1024),
                    "status": self._get_performance_status("file_read", read_time),
                }

                if read_time > self.thresholds["file_read_warning"]:
                    self.logger.warning(f"Slow file read for {file_path}: {read_time:.3f}s")

            except Exception as e:
                file_metrics[file_path] = {"error": str(e), "status": "error"}
                self.logger.error(f"File operation failed for {file_path}: {e}")

        return file_metrics

    def monitor_script_performance(self):
        """Monitor repository script execution performance"""
        scripts_dir = os.path.join(self.repo_path, "scripts")
        test_scripts = []

        if os.path.exists(scripts_dir):
            # Find Python scripts to test
            for script in os.listdir(scripts_dir):
                if script.endswith(".py") and script not in ["__pycache__"]:
                    test_scripts.append(script)

        script_metrics = {}

        for script in test_scripts[:10]:  # Limit to first 10 scripts
            script_path = os.path.join(scripts_dir, script)

            try:
                start_time = time.time()
                start_memory = psutil.Process().memory_info().rss / 1024 / 1024
                start_cpu = psutil.cpu_percent()

                result = subprocess.run(
                    ["python3", script_path],
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                    timeout=60,  # 60 second timeout
                )

                end_time = time.time()
                end_memory = psutil.Process().memory_info().rss / 1024 / 1024
                end_cpu = psutil.cpu_percent()

                execution_time = end_time - start_time
                memory_used = end_memory - start_memory
                cpu_used = end_cpu - start_cpu

                script_metrics[script] = {
                    "execution_time": execution_time,
                    "memory_used_mb": memory_used,
                    "cpu_usage_percent": cpu_used,
                    "success": result.returncode == 0,
                    "output_size": len(result.stdout) + len(result.stderr),
                    "status": self._get_performance_status("script_execution", execution_time),
                }

                if execution_time > self.thresholds["script_execution_warning"]:
                    self.logger.warning(f"Script {script} execution slow: {execution_time:.2f}s")

            except subprocess.TimeoutExpired:
                script_metrics[script] = {
                    "execution_time": 60,
                    "success": False,
                    "error": "timeout",
                    "status": "critical",
                }
                self.logger.error(f"Script {script} timed out")

            except Exception as e:
                script_metrics[script] = {
                    "execution_time": 0,
                    "success": False,
                    "error": str(e),
                    "status": "error",
                }
                self.logger.error(f"Script {script} failed: {e}")

        return script_metrics

    def monitor_system_resources(self):
        """Monitor system resource usage during operations"""
        # Collect resource usage over a 30-second period
        cpu_samples = []
        memory_samples = []
        disk_io_start = psutil.disk_io_counters()

        sample_count = 30
        for _i in range(sample_count):
            cpu_samples.append(psutil.cpu_percent(interval=1))
            memory_samples.append(psutil.virtual_memory().percent)

        disk_io_end = psutil.disk_io_counters()

        # Calculate disk I/O
        disk_read_bytes = disk_io_end.read_bytes - disk_io_start.read_bytes
        disk_write_bytes = disk_io_end.write_bytes - disk_io_start.write_bytes

        system_metrics = {
            "cpu_usage": {
                "average": statistics.mean(cpu_samples),
                "max": max(cpu_samples),
                "min": min(cpu_samples),
                "samples": cpu_samples,
                "status": self._get_performance_status("cpu_usage", max(cpu_samples)),
            },
            "memory_usage": {
                "average": statistics.mean(memory_samples),
                "max": max(memory_samples),
                "min": min(memory_samples),
                "samples": memory_samples,
                "status": self._get_performance_status("memory_usage", max(memory_samples)),
            },
            "disk_io": {
                "read_bytes": disk_read_bytes,
                "write_bytes": disk_write_bytes,
                "read_mb": disk_read_bytes / (1024 * 1024),
                "write_mb": disk_write_bytes / (1024 * 1024),
            },
            "disk_usage": psutil.disk_usage(self.repo_path)._asdict(),
        }

        # Log warnings for high resource usage
        if max(cpu_samples) > self.thresholds["cpu_usage_warning"]:
            self.logger.warning(f"High CPU usage detected: {max(cpu_samples):.1f}%")

        if max(memory_samples) > self.thresholds["memory_usage_warning"]:
            self.logger.warning(f"High memory usage detected: {max(memory_samples):.1f}%")

        return system_metrics

    def benchmark_search_operations(self):
        """Benchmark various search operations"""
        search_benchmarks = {}

        # Test different search patterns
        search_tests = [
            ("simple_grep", "grep -r 'TODO' docs/ --include='*.md'"),
            (
                "complex_grep",
                "grep -r -E '(security|authentication|authorization)' docs/ --include='*.md'",
            ),
            ("find_files", "find docs/ -name '*.md' -type f"),
            ("file_count", "find docs/ -name '*.md' -type f | wc -l"),
            ("word_count", "find docs/ -name '*.md' -exec wc -w {} + | tail -1"),
        ]

        for test_name, command in search_tests:
            try:
                start_time = time.time()
                result = subprocess.run(
                    command,
                    shell=True,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                    timeout=30,
                )
                end_time = time.time()

                search_benchmarks[test_name] = {
                    "execution_time": end_time - start_time,
                    "success": result.returncode == 0,
                    "output_lines": (len(result.stdout.split("\n")) if result.stdout else 0),
                    "command": command,
                }

            except subprocess.TimeoutExpired:
                search_benchmarks[test_name] = {
                    "execution_time": 30,
                    "success": False,
                    "error": "timeout",
                    "command": command,
                }
            except Exception as e:
                search_benchmarks[test_name] = {
                    "execution_time": 0,
                    "success": False,
                    "error": str(e),
                    "command": command,
                }

        return search_benchmarks

    def _get_performance_status(self, operation_type, value):
        """Get performance status based on thresholds"""
        warning_threshold = self.thresholds.get(f"{operation_type}_warning")
        critical_threshold = self.thresholds.get(f"{operation_type}_critical")

        if warning_threshold is None or critical_threshold is None:
            return "unknown"

        if value >= critical_threshold:
            return "critical"
        elif value >= warning_threshold:
            return "warning"
        else:
            return "ok"

    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        self.logger.info("Starting comprehensive performance monitoring")

        report = {
            "timestamp": datetime.now().isoformat(),
            "monitoring_duration": "30_seconds",
            "git_operations": self.monitor_git_operations(),
            "file_operations": self.monitor_file_operations(),
            "script_performance": self.monitor_script_performance(),
            "system_resources": self.monitor_system_resources(),
            "search_benchmarks": self.benchmark_search_operations(),
            "thresholds": self.thresholds,
        }

        # Calculate overall health score
        report["health_score"] = self._calculate_health_score(report)

        # Save the report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(self.metrics_dir, f"performance_report_{timestamp}.json")

        try:
            with open(report_file, "w") as f:
                json.dump(report, f, indent=2, default=str)
            self.logger.info(f"Performance report saved to {report_file}")
        except Exception as e:
            self.logger.error(f"Failed to save performance report: {e}")

        # Also save as latest
        latest_file = os.path.join(self.metrics_dir, "latest_performance_report.json")
        try:
            with open(latest_file, "w") as f:
                json.dump(report, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"Failed to save latest performance report: {e}")

        return report

    def _calculate_health_score(self, report):
        """Calculate overall repository health score based on performance metrics"""
        scores = []

        # Git operations score
        git_ops = report.get("git_operations", {})
        git_success_rate = (
            sum(1 for op in git_ops.values() if op.get("success", False)) / len(git_ops) if git_ops else 0
        )
        scores.append(git_success_rate * 100)

        # File operations score
        file_ops = report.get("file_operations", {})
        file_success_rate = sum(1 for op in file_ops.values() if "error" not in op) / len(file_ops) if file_ops else 0
        scores.append(file_success_rate * 100)

        # Script performance score
        script_perf = report.get("script_performance", {})
        script_success_rate = (
            sum(1 for op in script_perf.values() if op.get("success", False)) / len(script_perf) if script_perf else 0
        )
        scores.append(script_success_rate * 100)

        # System resources score (inverse of usage)
        sys_resources = report.get("system_resources", {})
        cpu_score = max(0, 100 - sys_resources.get("cpu_usage", {}).get("max", 0))
        memory_score = max(0, 100 - sys_resources.get("memory_usage", {}).get("max", 0))
        scores.extend([cpu_score, memory_score])

        # Search performance score
        search_benchmarks = report.get("search_benchmarks", {})
        search_success_rate = (
            sum(1 for op in search_benchmarks.values() if op.get("success", False)) / len(search_benchmarks)
            if search_benchmarks
            else 0
        )
        scores.append(search_success_rate * 100)

        overall_score = statistics.mean(scores) if scores else 0

        return {
            "overall": round(overall_score, 2),
            "git_operations": round(git_success_rate * 100, 2),
            "file_operations": round(file_success_rate * 100, 2),
            "script_performance": round(script_success_rate * 100, 2),
            "cpu_efficiency": round(cpu_score, 2),
            "memory_efficiency": round(memory_score, 2),
            "search_performance": round(search_success_rate * 100, 2),
        }

    def continuous_monitoring(self, duration_minutes=60, interval_minutes=5):
        """Run continuous monitoring for specified duration"""
        self.logger.info(f"Starting continuous monitoring for {duration_minutes} minutes")

        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        reports = []

        while datetime.now() < end_time:
            try:
                report = self.generate_performance_report()
                reports.append(report)

                self.logger.info(
                    f"Monitoring cycle completed. Health score: {report.get('health_score', {}).get('overall', 'N/A')}"
                )

                # Wait for next interval
                time.sleep(interval_minutes * 60)

            except KeyboardInterrupt:
                self.logger.info("Continuous monitoring interrupted by user")
                break
            except Exception as e:
                self.logger.error(f"Error during continuous monitoring: {e}")
                time.sleep(60)  # Wait a minute before retrying

        # Save summary of continuous monitoring
        summary = {
            "monitoring_period": {
                "start": (datetime.now() - timedelta(minutes=duration_minutes)).isoformat(),
                "end": datetime.now().isoformat(),
                "duration_minutes": duration_minutes,
                "interval_minutes": interval_minutes,
            },
            "total_reports": len(reports),
            "average_health_score": (
                statistics.mean([r.get("health_score", {}).get("overall", 0) for r in reports]) if reports else 0
            ),
            "reports": reports,
        }

        summary_file = os.path.join(
            self.metrics_dir,
            f'continuous_monitoring_summary_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
        )
        try:
            with open(summary_file, "w") as f:
                json.dump(summary, f, indent=2, default=str)
            self.logger.info(f"Continuous monitoring summary saved to {summary_file}")
        except Exception as e:
            self.logger.error(f"Failed to save monitoring summary: {e}")

        return summary


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Repository Performance Monitor")
    parser.add_argument("--continuous", action="store_true", help="Run continuous monitoring")
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Duration for continuous monitoring (minutes)",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Interval between monitoring cycles (minutes)",
    )

    args = parser.parse_args()

    monitor = PerformanceMonitor()

    if args.continuous:
        print(f"Starting continuous monitoring for {args.duration} minutes...")
        summary = monitor.continuous_monitoring(args.duration, args.interval)
        print(
            f"Continuous monitoring completed. Average health score: {summary.get('average_health_score', 'N/A'):.2f}"
        )
    else:
        print("Running single performance monitoring cycle...")
        report = monitor.generate_performance_report()

        # Print summary
        health_score = report.get("health_score", {})
        print("\nPerformance Report Summary:")
        print(f"  Overall Health Score: {health_score.get('overall', 'N/A'):.2f}/100")
        print(f"  Git Operations: {health_score.get('git_operations', 'N/A'):.2f}/100")
        print(f"  File Operations: {health_score.get('file_operations', 'N/A'):.2f}/100")
        print(f"  Script Performance: {health_score.get('script_performance', 'N/A'):.2f}/100")
        print(f"  CPU Efficiency: {health_score.get('cpu_efficiency', 'N/A'):.2f}/100")
        print(f"  Memory Efficiency: {health_score.get('memory_efficiency', 'N/A'):.2f}/100")
        print(f"  Search Performance: {health_score.get('search_performance', 'N/A'):.2f}/100")

        print(f"\nDetailed report saved to: {monitor.metrics_dir}")
