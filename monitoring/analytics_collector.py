#!/usr/bin/env python3
"""
Standards Repository Analytics Collector

This script collects analytics on standards usage patterns, file access,
and repository health metrics for the standards repository.
"""

import json
import os
import subprocess
import time
from datetime import datetime, timedelta
from pathlib import Path
import logging
import hashlib
import yaml


class AnalyticsCollector:
    """Collects analytics on standards repository usage"""

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        self.metrics_dir = os.path.join(self.repo_path, "monitoring", "metrics")
        self.logs_dir = os.path.join(self.repo_path, "monitoring", "logs")

        # Ensure directories exist
        os.makedirs(self.metrics_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename=os.path.join(self.logs_dir, "analytics.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

    def collect_git_metrics(self):
        """Collect Git repository metrics"""
        try:
            # Get commit history metrics
            commits_last_30_days = self._get_git_commits_count(30)
            commits_last_7_days = self._get_git_commits_count(7)

            # Get file change frequency
            file_changes = self._get_file_change_frequency()

            # Get contributor metrics
            contributors = self._get_contributor_metrics()

            # Get branch metrics
            branch_info = self._get_branch_metrics()

            metrics = {
                "timestamp": datetime.now().isoformat(),
                "commits": {
                    "last_30_days": commits_last_30_days,
                    "last_7_days": commits_last_7_days,
                    "today": self._get_git_commits_count(1),
                },
                "file_changes": file_changes,
                "contributors": contributors,
                "branches": branch_info,
            }

            self.logger.info(
                f"Collected Git metrics: {commits_last_7_days} commits in last 7 days"
            )
            return metrics

        except Exception as e:
            self.logger.error(f"Error collecting Git metrics: {e}")
            return {}

    def collect_standards_usage_metrics(self):
        """Collect metrics on standards document usage and access patterns"""
        try:
            manifest_path = os.path.join(self.repo_path, "config", "MANIFEST.yaml")
            if not os.path.exists(manifest_path):
                self.logger.warning("MANIFEST.yaml not found")
                return {}

            with open(manifest_path, "r") as f:
                manifest = yaml.safe_load(f)

            standards_metrics = {}

            for std_id, std_info in manifest.get("standards", {}).items():
                file_path = os.path.join(
                    self.repo_path, "docs", "standards", std_info["full_name"]
                )

                if os.path.exists(file_path):
                    metrics = self._analyze_standard_file(file_path, std_info)
                    standards_metrics[std_id] = metrics

            self.logger.info(
                f"Collected metrics for {len(standards_metrics)} standards"
            )
            return standards_metrics

        except Exception as e:
            self.logger.error(f"Error collecting standards metrics: {e}")
            return {}

    def collect_repository_health_metrics(self):
        """Collect repository health and quality metrics"""
        try:
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "repository_size": self._get_repository_size(),
                "file_counts": self._get_file_counts(),
                "documentation_coverage": self._calculate_documentation_coverage(),
                "link_health": self._check_link_health(),
                "compliance_scores": self._get_compliance_scores(),
                "disk_usage": self._get_disk_usage(),
            }

            self.logger.info("Collected repository health metrics")
            return metrics

        except Exception as e:
            self.logger.error(f"Error collecting health metrics: {e}")
            return {}

    def collect_performance_metrics(self):
        """Collect performance metrics for repository operations"""
        try:
            metrics = {
                "timestamp": datetime.now().isoformat(),
                "script_performance": self._benchmark_scripts(),
                "file_access_times": self._measure_file_access_times(),
                "search_performance": self._benchmark_search_operations(),
                "validation_times": self._measure_validation_performance(),
            }

            self.logger.info("Collected performance metrics")
            return metrics

        except Exception as e:
            self.logger.error(f"Error collecting performance metrics: {e}")
            return {}

    def _get_git_commits_count(self, days):
        """Get number of commits in the last N days"""
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cmd = f"git log --since='{since_date}' --oneline | wc -l"
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=self.repo_path
        )
        return int(result.stdout.strip()) if result.stdout.strip() else 0

    def _get_file_change_frequency(self):
        """Get file change frequency over last 30 days"""
        cmd = "git log --since='30 days ago' --name-only --pretty=format: | sort | uniq -c | sort -nr"
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=self.repo_path
        )

        file_changes = {}
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    count = int(parts[0])
                    filename = " ".join(parts[1:])
                    if filename.endswith(".md"):
                        file_changes[filename] = count

        return dict(list(file_changes.items())[:20])  # Top 20 most changed files

    def _get_contributor_metrics(self):
        """Get contributor metrics"""
        cmd = "git log --since='30 days ago' --pretty=format:'%an' | sort | uniq -c | sort -nr"
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, cwd=self.repo_path
        )

        contributors = {}
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                parts = line.strip().split(None, 1)
                if len(parts) >= 2:
                    count = int(parts[0])
                    name = parts[1]
                    contributors[name] = count

        return contributors

    def _get_branch_metrics(self):
        """Get branch information"""
        try:
            # Get current branch
            current_branch = subprocess.run(
                "git branch --show-current",
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            ).stdout.strip()

            # Get total branches
            branches = subprocess.run(
                "git branch -a | wc -l",
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            ).stdout.strip()

            return {
                "current": current_branch,
                "total_branches": int(branches) if branches else 0,
            }
        except:
            return {"current": "unknown", "total_branches": 0}

    def _analyze_standard_file(self, file_path, std_info):
        """Analyze a standards file for metrics"""
        try:
            stat = os.stat(file_path)

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Calculate content hash for change detection
            content_hash = hashlib.md5(content.encode()).hexdigest()

            metrics = {
                "file_size": stat.st_size,
                "last_modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "content_hash": content_hash,
                "estimated_tokens": std_info.get("token_estimate", 0),
                "line_count": len(content.split("\n")),
                "word_count": len(content.split()),
                "sections": len(
                    [line for line in content.split("\n") if line.startswith("#")]
                ),
                "code_blocks": content.count("```"),
                "links": content.count("["),  # Rough link count
            }

            return metrics

        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return {}

    def _get_repository_size(self):
        """Get total repository size"""
        try:
            cmd = f"du -sb {self.repo_path}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return int(result.stdout.split()[0]) if result.stdout else 0
        except:
            return 0

    def _get_file_counts(self):
        """Get counts of different file types"""
        file_counts = {
            "markdown": 0,
            "python": 0,
            "javascript": 0,
            "yaml": 0,
            "json": 0,
            "shell": 0,
            "total": 0,
        }

        for root, dirs, files in os.walk(self.repo_path):
            # Skip .git directory
            if ".git" in dirs:
                dirs.remove(".git")

            for file in files:
                file_counts["total"] += 1

                if file.endswith(".md"):
                    file_counts["markdown"] += 1
                elif file.endswith(".py"):
                    file_counts["python"] += 1
                elif file.endswith((".js", ".ts")):
                    file_counts["javascript"] += 1
                elif file.endswith((".yml", ".yaml")):
                    file_counts["yaml"] += 1
                elif file.endswith(".json"):
                    file_counts["json"] += 1
                elif file.endswith(".sh"):
                    file_counts["shell"] += 1

        return file_counts

    def _calculate_documentation_coverage(self):
        """Calculate documentation coverage metrics"""
        docs_dir = os.path.join(self.repo_path, "docs")
        if not os.path.exists(docs_dir):
            return 0

        total_md_files = 0
        documented_features = 0

        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith(".md"):
                    total_md_files += 1
                    # Simple heuristic: files with substantial content are "documented"
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                            if len(content) > 1000:  # More than 1000 chars
                                documented_features += 1
                    except:
                        pass

        return (documented_features / total_md_files * 100) if total_md_files > 0 else 0

    def _check_link_health(self):
        """Check health of internal links"""
        # This is a simplified version - in production you'd want more sophisticated checking
        broken_links = 0
        total_links = 0

        docs_dir = os.path.join(self.repo_path, "docs")
        if os.path.exists(docs_dir):
            for root, dirs, files in os.walk(docs_dir):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, "r", encoding="utf-8") as f:
                                content = f.read()
                                # Simple regex to find markdown links
                                import re

                                links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", content)
                                total_links += len(links)

                                for _, link in links:
                                    if link.startswith("./") or link.startswith("../"):
                                        # Check if local file exists
                                        link_path = os.path.join(
                                            os.path.dirname(file_path), link
                                        )
                                        if not os.path.exists(link_path):
                                            broken_links += 1
                        except:
                            pass

        health_score = (
            ((total_links - broken_links) / total_links * 100)
            if total_links > 0
            else 100
        )
        return {
            "total_links": total_links,
            "broken_links": broken_links,
            "health_score": health_score,
        }

    def _get_compliance_scores(self):
        """Get compliance scores if available"""
        try:
            # Try to run the compliance score script
            script_path = os.path.join(
                self.repo_path, "scripts", "calculate_compliance_score.py"
            )
            if os.path.exists(script_path):
                result = subprocess.run(
                    ["python3", script_path],
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                )

                if result.returncode == 0:
                    lines = result.stdout.strip().split("\n")
                    scores = {}
                    for line in lines:
                        if "Score:" in line:
                            scores["compliance_score"] = float(
                                line.split(":")[1].strip().rstrip("%")
                            )
                        elif "Total Rules:" in line:
                            scores["total_rules"] = int(line.split(":")[1].strip())
                        elif "Required Rules:" in line:
                            scores["required_rules"] = int(line.split(":")[1].strip())
                    return scores
        except:
            pass

        return {}

    def _get_disk_usage(self):
        """Get disk usage breakdown"""
        usage = {}

        subdirs = ["docs", "scripts", "config", "examples", "tests", "monitoring"]
        for subdir in subdirs:
            subdir_path = os.path.join(self.repo_path, subdir)
            if os.path.exists(subdir_path):
                try:
                    cmd = f"du -sb {subdir_path}"
                    result = subprocess.run(
                        cmd, shell=True, capture_output=True, text=True
                    )
                    usage[subdir] = (
                        int(result.stdout.split()[0]) if result.stdout else 0
                    )
                except:
                    usage[subdir] = 0

        return usage

    def _benchmark_scripts(self):
        """Benchmark key repository scripts"""
        scripts_dir = os.path.join(self.repo_path, "scripts")
        benchmarks = {}

        if os.path.exists(scripts_dir):
            test_scripts = [
                "generate_summary.py",
                "generate_digest.py",
                "calculate_compliance_score.py",
            ]

            for script in test_scripts:
                script_path = os.path.join(scripts_dir, script)
                if os.path.exists(script_path):
                    try:
                        start_time = time.time()
                        result = subprocess.run(
                            ["python3", script_path],
                            capture_output=True,
                            text=True,
                            cwd=self.repo_path,
                            timeout=30,  # 30 second timeout
                        )
                        end_time = time.time()

                        benchmarks[script] = {
                            "execution_time": end_time - start_time,
                            "success": result.returncode == 0,
                            "output_size": len(result.stdout) + len(result.stderr),
                        }
                    except subprocess.TimeoutExpired:
                        benchmarks[script] = {
                            "execution_time": 30,
                            "success": False,
                            "error": "timeout",
                        }
                    except Exception as e:
                        benchmarks[script] = {
                            "execution_time": 0,
                            "success": False,
                            "error": str(e),
                        }

        return benchmarks

    def _measure_file_access_times(self):
        """Measure file access times for key files"""
        key_files = [
            "config/MANIFEST.yaml",
            "docs/standards/CODING_STANDARDS.md",
            "docs/standards/SECURITY_STANDARDS.md",
            "README.md",
        ]

        access_times = {}

        for file_path in key_files:
            full_path = os.path.join(self.repo_path, file_path)
            if os.path.exists(full_path):
                try:
                    start_time = time.time()
                    with open(full_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    end_time = time.time()

                    access_times[file_path] = {
                        "read_time": end_time - start_time,
                        "file_size": len(content),
                        "read_speed_mb_per_sec": len(content)
                        / (end_time - start_time)
                        / (1024 * 1024),
                    }
                except Exception as e:
                    access_times[file_path] = {"error": str(e)}

        return access_times

    def _benchmark_search_operations(self):
        """Benchmark search operations"""
        benchmarks = {}

        # Test grep operations
        search_terms = ["TODO", "FIXME", "security", "authentication"]

        for term in search_terms:
            try:
                start_time = time.time()
                cmd = f"grep -r '{term}' docs/ --include='*.md' | wc -l"
                result = subprocess.run(
                    cmd, shell=True, capture_output=True, text=True, cwd=self.repo_path
                )
                end_time = time.time()

                benchmarks[f"grep_{term}"] = {
                    "search_time": end_time - start_time,
                    "results_count": (
                        int(result.stdout.strip()) if result.stdout.strip() else 0
                    ),
                }
            except Exception as e:
                benchmarks[f"grep_{term}"] = {"error": str(e)}

        return benchmarks

    def _measure_validation_performance(self):
        """Measure validation script performance"""
        validation_scripts = [
            "validate_markdown_links.py",
            "validate_standards_consistency.py",
        ]

        performance = {}
        scripts_dir = os.path.join(self.repo_path, "scripts")

        for script in validation_scripts:
            script_path = os.path.join(scripts_dir, script)
            if os.path.exists(script_path):
                try:
                    start_time = time.time()
                    result = subprocess.run(
                        ["python3", script_path],
                        capture_output=True,
                        text=True,
                        cwd=self.repo_path,
                        timeout=60,  # 60 second timeout
                    )
                    end_time = time.time()

                    performance[script] = {
                        "validation_time": end_time - start_time,
                        "success": result.returncode == 0,
                        "issues_found": result.stdout.count("ERROR")
                        + result.stdout.count("WARNING"),
                    }
                except subprocess.TimeoutExpired:
                    performance[script] = {
                        "validation_time": 60,
                        "success": False,
                        "error": "timeout",
                    }
                except Exception as e:
                    performance[script] = {
                        "validation_time": 0,
                        "success": False,
                        "error": str(e),
                    }

        return performance

    def save_metrics(self, metrics, filename):
        """Save metrics to JSON file"""
        filepath = os.path.join(self.metrics_dir, filename)
        try:
            with open(filepath, "w") as f:
                json.dump(metrics, f, indent=2, default=str)
            self.logger.info(f"Metrics saved to {filepath}")
        except Exception as e:
            self.logger.error(f"Error saving metrics to {filepath}: {e}")

    def collect_all_metrics(self):
        """Collect all metrics and save them"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Collect all metrics
        git_metrics = self.collect_git_metrics()
        standards_metrics = self.collect_standards_usage_metrics()
        health_metrics = self.collect_repository_health_metrics()
        performance_metrics = self.collect_performance_metrics()

        # Combine all metrics
        all_metrics = {
            "collection_timestamp": datetime.now().isoformat(),
            "git_metrics": git_metrics,
            "standards_metrics": standards_metrics,
            "health_metrics": health_metrics,
            "performance_metrics": performance_metrics,
        }

        # Save metrics
        self.save_metrics(all_metrics, f"metrics_{timestamp}.json")

        # Also save as latest
        self.save_metrics(all_metrics, "latest_metrics.json")

        self.logger.info("All metrics collection completed")
        return all_metrics


if __name__ == "__main__":
    collector = AnalyticsCollector()
    metrics = collector.collect_all_metrics()

    print("Analytics collection completed!")
    print(f"Metrics saved to: {collector.metrics_dir}")

    # Print summary
    if metrics.get("git_metrics"):
        git = metrics["git_metrics"]
        print(f"\nGit Summary:")
        print(
            f"  - Commits last 7 days: {git.get('commits', {}).get('last_7_days', 0)}"
        )
        print(f"  - Contributors: {len(git.get('contributors', {}))}")

    if metrics.get("health_metrics"):
        health = metrics["health_metrics"]
        print(f"\nRepository Health:")
        print(f"  - Total files: {health.get('file_counts', {}).get('total', 0)}")
        print(
            f"  - Documentation coverage: {health.get('documentation_coverage', 0):.1f}%"
        )

    if metrics.get("standards_metrics"):
        print(f"  - Standards tracked: {len(metrics['standards_metrics'])}")
