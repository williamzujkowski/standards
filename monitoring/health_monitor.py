#!/usr/bin/env python3
"""
Repository Health Monitor

This script provides comprehensive health monitoring for the standards repository,
including file integrity, dependency tracking, validation status, and automated
health checks with alerting.
"""

import json
import logging
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path

import psutil
import yaml


class HealthMonitor:
    """Comprehensive repository health monitoring system"""

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        self.monitoring_dir = os.path.join(self.repo_path, "monitoring")
        self.health_dir = os.path.join(self.monitoring_dir, "health")
        self.logs_dir = os.path.join(self.monitoring_dir, "logs")

        # Ensure directories exist
        for dir_path in [self.health_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename=os.path.join(self.logs_dir, "health_monitor.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # Health check configuration
        self.health_checks = {
            "file_integrity": True,
            "dependency_validation": True,
            "link_validation": True,
            "standards_consistency": True,
            "git_health": True,
            "system_resources": True,
            "security_validation": True,
            "compliance_checking": True,
        }

        # Health thresholds
        self.thresholds = {
            "critical": {
                "broken_links_percent": 10,
                "missing_files_percent": 5,
                "dependency_errors_percent": 15,
                "system_cpu_percent": 95,
                "system_memory_percent": 95,
                "disk_usage_percent": 95,
            },
            "warning": {
                "broken_links_percent": 5,
                "missing_files_percent": 2,
                "dependency_errors_percent": 5,
                "system_cpu_percent": 80,
                "system_memory_percent": 80,
                "disk_usage_percent": 85,
            },
        }

    def run_comprehensive_health_check(self):
        """Run all health checks and generate comprehensive report"""
        self.logger.info("Starting comprehensive health check")

        health_report = {
            "timestamp": datetime.now().isoformat(),
            "overall_status": "healthy",
            "health_score": 100,
            "checks": {},
            "alerts": [],
            "recommendations": [],
        }

        # Run individual health checks
        if self.health_checks["file_integrity"]:
            health_report["checks"]["file_integrity"] = self._check_file_integrity()

        if self.health_checks["dependency_validation"]:
            health_report["checks"]["dependency_validation"] = self._check_dependencies()

        if self.health_checks["link_validation"]:
            health_report["checks"]["link_validation"] = self._check_links()

        if self.health_checks["standards_consistency"]:
            health_report["checks"]["standards_consistency"] = self._check_standards_consistency()

        if self.health_checks["git_health"]:
            health_report["checks"]["git_health"] = self._check_git_health()

        if self.health_checks["system_resources"]:
            health_report["checks"]["system_resources"] = self._check_system_resources()

        if self.health_checks["security_validation"]:
            health_report["checks"]["security_validation"] = self._check_security()

        if self.health_checks["compliance_checking"]:
            health_report["checks"]["compliance_checking"] = self._check_compliance()

        # Calculate overall health score and status
        health_report = self._calculate_overall_health(health_report)

        # Save health report
        self._save_health_report(health_report)

        self.logger.info(
            f"Health check completed. Overall status: {health_report['overall_status']}, "
            f"Score: {health_report['health_score']}"
        )

        return health_report

    def _check_file_integrity(self):
        """Check integrity of critical files"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        # Critical files that must exist
        critical_files = [
            "README.md",
            "config/MANIFEST.yaml",
            "docs/standards/CODING_STANDARDS.md",
            "docs/standards/MODERN_SECURITY_STANDARDS.md",
            "docs/standards/UNIFIED_STANDARDS.md",
        ]

        missing_files = []
        corrupted_files = []

        for file_path in critical_files:
            full_path = os.path.join(self.repo_path, file_path)

            if not os.path.exists(full_path):
                missing_files.append(file_path)
                continue

            try:
                # Check if file is readable and has content
                with open(full_path, encoding="utf-8") as f:
                    content = f.read()
                    if len(content) < 100:  # Files should have substantial content
                        corrupted_files.append(f"{file_path} (too small)")

                    # Basic format validation for key files
                    if file_path.endswith(".md") and not content.startswith("#"):
                        corrupted_files.append(f"{file_path} (invalid markdown format)")

                    if file_path.endswith(".yaml") or file_path.endswith(".yml"):
                        try:
                            yaml.safe_load(content)
                        except yaml.YAMLError:
                            corrupted_files.append(f"{file_path} (invalid YAML)")

            except Exception as e:
                corrupted_files.append(f"{file_path} (read error: {e!s})")

        # Calculate score
        total_files = len(critical_files)
        issues_count = len(missing_files) + len(corrupted_files)

        if issues_count > 0:
            check_result["score"] = max(0, 100 - (issues_count / total_files * 100))

            if issues_count / total_files > 0.1:  # More than 10% issues
                check_result["status"] = "critical"
            elif issues_count / total_files > 0.05:  # More than 5% issues
                check_result["status"] = "warning"

        check_result["details"] = {
            "total_critical_files": total_files,
            "missing_files": missing_files,
            "corrupted_files": corrupted_files,
            "healthy_files": total_files - issues_count,
        }

        if missing_files:
            check_result["issues"].append(f"Missing critical files: {', '.join(missing_files)}")

        if corrupted_files:
            check_result["issues"].append(f"Corrupted/invalid files: {', '.join(corrupted_files)}")

        return check_result

    def _check_dependencies(self):
        """Check for dependency issues in the repository"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        dependency_issues = []

        # Check Python dependencies
        python_files = list(Path(self.repo_path).rglob("*.py"))
        requirements_files = list(Path(self.repo_path).rglob("requirements*.txt"))

        if python_files and not requirements_files:
            dependency_issues.append("Python files found but no requirements.txt")

        # Check for common import issues in Python files
        import_errors = []
        for py_file in python_files[:10]:  # Check first 10 Python files
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                # Look for common problematic imports
                problematic_imports = re.findall(r"import\s+(\w+)", content)
                for imp in problematic_imports:
                    if imp in ["requests", "pandas", "numpy"] and not requirements_files:
                        import_errors.append(f"{py_file.name} imports {imp} but no requirements.txt")

            except Exception:
                continue

        # Check Node.js dependencies if applicable
        package_json_files = list(Path(self.repo_path).rglob("package.json"))
        js_files = list(Path(self.repo_path).rglob("*.js")) + list(Path(self.repo_path).rglob("*.ts"))

        if js_files and not package_json_files:
            dependency_issues.append("JavaScript/TypeScript files found but no package.json")

        # Check for missing node_modules if package.json exists
        for package_json in package_json_files:
            node_modules = package_json.parent / "node_modules"
            if not node_modules.exists():
                dependency_issues.append(f"Missing node_modules for {package_json}")

        # Calculate score
        total_issues = len(dependency_issues) + len(import_errors)
        if total_issues > 0:
            check_result["score"] = max(0, 100 - (total_issues * 10))

            if total_issues > 5:
                check_result["status"] = "critical"
            elif total_issues > 2:
                check_result["status"] = "warning"

        check_result["details"] = {
            "python_files": len(python_files),
            "requirements_files": len(requirements_files),
            "js_files": len(js_files),
            "package_json_files": len(package_json_files),
            "dependency_issues": dependency_issues,
            "import_errors": import_errors[:5],  # First 5 import errors
        }

        check_result["issues"] = dependency_issues + import_errors[:5]

        return check_result

    def _check_links(self):
        """Check for broken internal links"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        markdown_files = list(Path(self.repo_path).rglob("*.md"))
        total_links = 0
        broken_links = []

        for md_file in markdown_files:
            try:
                with open(md_file, encoding="utf-8") as f:
                    content = f.read()

                # Find markdown links
                link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
                links = re.findall(link_pattern, content)

                for link_text, link_url in links:
                    total_links += 1

                    # Check internal links (relative paths)
                    if link_url.startswith("./") or link_url.startswith("../") or not link_url.startswith("http"):
                        # Convert to absolute path
                        if link_url.startswith("./"):
                            link_path = md_file.parent / link_url[2:]
                        elif link_url.startswith("../"):
                            link_path = md_file.parent / link_url
                        else:
                            link_path = Path(self.repo_path) / link_url

                        # Remove anchor if present
                        if "#" in str(link_path):
                            link_path = Path(str(link_path).split("#")[0])

                        if not link_path.exists():
                            broken_links.append(
                                {
                                    "file": str(md_file.relative_to(self.repo_path)),
                                    "link": link_url,
                                    "text": link_text,
                                }
                            )

            except Exception as e:
                check_result["issues"].append(f"Error checking links in {md_file}: {e!s}")

        # Calculate score
        if total_links > 0:
            broken_percentage = len(broken_links) / total_links * 100
            check_result["score"] = max(0, 100 - broken_percentage * 2)  # 2 points per broken link percentage

            if broken_percentage > self.thresholds["critical"]["broken_links_percent"]:
                check_result["status"] = "critical"
            elif broken_percentage > self.thresholds["warning"]["broken_links_percent"]:
                check_result["status"] = "warning"

        check_result["details"] = {
            "total_links": total_links,
            "broken_links": len(broken_links),
            "broken_percentage": (len(broken_links) / total_links * 100 if total_links > 0 else 0),
            "broken_link_details": broken_links[:10],  # First 10 broken links
        }

        if broken_links:
            check_result["issues"].append(f"{len(broken_links)} broken internal links found")

        return check_result

    def _check_standards_consistency(self):
        """Check consistency across standards files"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        try:
            # Load MANIFEST.yaml for reference
            manifest_path = os.path.join(self.repo_path, "config", "MANIFEST.yaml")
            if not os.path.exists(manifest_path):
                check_result["issues"].append("MANIFEST.yaml not found")
                check_result["status"] = "critical"
                check_result["score"] = 0
                return check_result

            with open(manifest_path) as f:
                manifest = yaml.safe_load(f)

            standards = manifest.get("standards", {})
            consistency_issues = []

            # Check if all standards files referenced in manifest exist
            missing_standards = []
            for _std_id, std_info in standards.items():
                file_path = os.path.join(self.repo_path, "docs", "standards", std_info["full_name"])
                if not os.path.exists(file_path):
                    missing_standards.append(std_info["full_name"])

            # Check for standards files not in manifest
            standards_dir = os.path.join(self.repo_path, "docs", "standards")
            if os.path.exists(standards_dir):
                actual_files = [f for f in os.listdir(standards_dir) if f.endswith(".md")]
                manifest_files = [info["full_name"] for info in standards.values()]

                orphaned_files = set(actual_files) - set(manifest_files)
                if orphaned_files:
                    consistency_issues.append(f"Files not in manifest: {', '.join(orphaned_files)}")

            # Check for inconsistent section structure
            inconsistent_structures = []
            for _std_id, std_info in standards.items():
                file_path = os.path.join(self.repo_path, "docs", "standards", std_info["full_name"])
                if os.path.exists(file_path):
                    try:
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()

                        # Check for required sections
                        required_sections = [
                            "## Overview",
                            "## Implementation",
                            "## Examples",
                        ]
                        missing_sections = []
                        for section in required_sections:
                            if section not in content:
                                missing_sections.append(section)

                        if missing_sections:
                            inconsistent_structures.append(
                                f"{std_info['full_name']}: missing {', '.join(missing_sections)}"
                            )

                    except Exception:
                        continue

            # Calculate score
            total_issues = len(missing_standards) + len(consistency_issues) + len(inconsistent_structures)
            if total_issues > 0:
                check_result["score"] = max(0, 100 - (total_issues * 5))

                if total_issues > 10:
                    check_result["status"] = "critical"
                elif total_issues > 5:
                    check_result["status"] = "warning"

            check_result["details"] = {
                "total_standards": len(standards),
                "missing_standards": missing_standards,
                "consistency_issues": consistency_issues,
                "inconsistent_structures": inconsistent_structures,
            }

            check_result["issues"] = (
                [f"Missing standards files: {', '.join(missing_standards)}"]
                if missing_standards
                else [] + consistency_issues + inconsistent_structures
            )

        except Exception as e:
            check_result["status"] = "critical"
            check_result["score"] = 0
            check_result["issues"].append(f"Error checking standards consistency: {e!s}")

        return check_result

    def _check_git_health(self):
        """Check Git repository health"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        try:
            # Check if we're in a git repository
            result = subprocess.run(["git", "status"], check=False, capture_output=True, text=True, cwd=self.repo_path)
            if result.returncode != 0:
                check_result["status"] = "critical"
                check_result["score"] = 0
                check_result["issues"].append("Not a valid Git repository")
                return check_result

            # Check for uncommitted changes
            uncommitted_files = []
            if result.stdout:
                lines = result.stdout.split("\n")
                in_changes_section = False
                for line in lines:
                    if "Changes not staged for commit:" in line or "Changes to be committed:" in line:
                        in_changes_section = True
                    elif in_changes_section and line.strip() and not line.startswith("\t"):
                        in_changes_section = False
                    elif in_changes_section and line.strip():
                        file_match = re.search(r"\s+(?:modified|new file|deleted):\s+(.+)", line)
                        if file_match:
                            uncommitted_files.append(file_match.group(1))

            # Check recent commit activity
            recent_commits = subprocess.run(
                ["git", "log", "--oneline", "--since=30 days ago"],
                check=False,
                capture_output=True,
                text=True,
                cwd=self.repo_path,
            )
            commit_count = len(recent_commits.stdout.strip().split("\n")) if recent_commits.stdout.strip() else 0

            # Check for large files
            large_files = []
            try:
                find_result = subprocess.run(
                    ["find", self.repo_path, "-type", "f", "-size", "+10M"],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                if find_result.stdout:
                    large_files = [f.replace(self.repo_path + "/", "") for f in find_result.stdout.strip().split("\n")]
                    # Filter out .git directory files
                    large_files = [f for f in large_files if not f.startswith(".git/")]
            except:
                pass

            # Calculate score based on findings
            score_deductions = 0

            if len(uncommitted_files) > 10:
                score_deductions += 20
                check_result["issues"].append(f"Many uncommitted files: {len(uncommitted_files)}")
            elif len(uncommitted_files) > 5:
                score_deductions += 10

            if commit_count == 0:
                score_deductions += 30
                check_result["issues"].append("No commits in last 30 days")
            elif commit_count < 5:
                score_deductions += 10

            if large_files:
                score_deductions += 15
                check_result["issues"].append(f"Large files detected: {', '.join(large_files[:3])}")

            check_result["score"] = max(0, 100 - score_deductions)

            if score_deductions > 40:
                check_result["status"] = "critical"
            elif score_deductions > 20:
                check_result["status"] = "warning"

            check_result["details"] = {
                "uncommitted_files": len(uncommitted_files),
                "recent_commits_30_days": commit_count,
                "large_files": large_files,
                "repository_status": "clean" if not uncommitted_files else "dirty",
            }

        except Exception as e:
            check_result["status"] = "critical"
            check_result["score"] = 0
            check_result["issues"].append(f"Error checking Git health: {e!s}")

        return check_result

    def _check_system_resources(self):
        """Check system resource usage"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        try:
            # CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)

            # Memory usage
            memory = psutil.virtual_memory()
            memory_percent = memory.percent

            # Disk usage for repository
            disk_usage = psutil.disk_usage(self.repo_path)
            disk_percent = disk_usage.used / disk_usage.total * 100

            # Check thresholds
            score_deductions = 0

            if cpu_percent > self.thresholds["critical"]["system_cpu_percent"]:
                score_deductions += 30
                check_result["issues"].append(f"Critical CPU usage: {cpu_percent:.1f}%")
            elif cpu_percent > self.thresholds["warning"]["system_cpu_percent"]:
                score_deductions += 15
                check_result["issues"].append(f"High CPU usage: {cpu_percent:.1f}%")

            if memory_percent > self.thresholds["critical"]["system_memory_percent"]:
                score_deductions += 30
                check_result["issues"].append(f"Critical memory usage: {memory_percent:.1f}%")
            elif memory_percent > self.thresholds["warning"]["system_memory_percent"]:
                score_deductions += 15
                check_result["issues"].append(f"High memory usage: {memory_percent:.1f}%")

            if disk_percent > self.thresholds["critical"]["disk_usage_percent"]:
                score_deductions += 25
                check_result["issues"].append(f"Critical disk usage: {disk_percent:.1f}%")
            elif disk_percent > self.thresholds["warning"]["disk_usage_percent"]:
                score_deductions += 10
                check_result["issues"].append(f"High disk usage: {disk_percent:.1f}%")

            check_result["score"] = max(0, 100 - score_deductions)

            if score_deductions > 50:
                check_result["status"] = "critical"
            elif score_deductions > 20:
                check_result["status"] = "warning"

            check_result["details"] = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory_percent,
                "memory_available_gb": memory.available / (1024**3),
                "disk_percent": disk_percent,
                "disk_free_gb": disk_usage.free / (1024**3),
            }

        except Exception as e:
            check_result["status"] = "warning"
            check_result["score"] = 80
            check_result["issues"].append(f"Error checking system resources: {e!s}")

        return check_result

    def _check_security(self):
        """Check for security issues"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        security_issues = []

        # Check for sensitive files
        sensitive_patterns = [
            "*.key",
            "*.pem",
            "*password*",
            "*secret*",
            ".env*",
            "id_rsa*",
        ]

        sensitive_files = []
        for pattern in sensitive_patterns:
            files = list(Path(self.repo_path).rglob(pattern))
            # Filter out .git directory
            files = [f for f in files if ".git" not in str(f)]
            sensitive_files.extend(files)

        if sensitive_files:
            security_issues.append(f"Potential sensitive files: {', '.join([f.name for f in sensitive_files[:5]])}")

        # Check for hardcoded secrets in code files
        code_files = (
            list(Path(self.repo_path).rglob("*.py"))
            + list(Path(self.repo_path).rglob("*.js"))
            + list(Path(self.repo_path).rglob("*.ts"))
            + list(Path(self.repo_path).rglob("*.md"))
        )

        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]

        files_with_secrets = []
        for code_file in code_files[:20]:  # Check first 20 files
            try:
                with open(code_file, encoding="utf-8") as f:
                    content = f.read()
                    for pattern in secret_patterns:
                        if re.search(pattern, content, re.IGNORECASE):
                            files_with_secrets.append(code_file.name)
                            break
            except:
                continue

        if files_with_secrets:
            security_issues.append(f"Potential hardcoded secrets in: {', '.join(files_with_secrets[:3])}")

        # Check file permissions (Unix systems)
        if os.name != "nt":
            executable_files = []
            for root, dirs, files in os.walk(self.repo_path):
                # Skip .git directory
                if ".git" in dirs:
                    dirs.remove(".git")

                for file in files:
                    file_path = os.path.join(root, file)
                    if os.access(file_path, os.X_OK) and not file.endswith((".sh", ".py")):
                        executable_files.append(file)

            if executable_files:
                security_issues.append(f"Unexpected executable files: {', '.join(executable_files[:3])}")

        # Calculate score
        score_deduction = len(security_issues) * 15
        check_result["score"] = max(0, 100 - score_deduction)

        if len(security_issues) > 3:
            check_result["status"] = "critical"
        elif len(security_issues) > 1:
            check_result["status"] = "warning"

        check_result["details"] = {
            "sensitive_files": len(sensitive_files),
            "files_with_potential_secrets": len(files_with_secrets),
            "security_issues_found": len(security_issues),
        }

        check_result["issues"] = security_issues

        return check_result

    def _check_compliance(self):
        """Check compliance with repository standards"""
        check_result = {"status": "healthy", "score": 100, "details": {}, "issues": []}

        try:
            # Try to run compliance score calculation
            compliance_script = os.path.join(self.repo_path, "scripts", "calculate_compliance_score.py")
            if os.path.exists(compliance_script):
                result = subprocess.run(
                    ["python3", compliance_script],
                    check=False,
                    capture_output=True,
                    text=True,
                    cwd=self.repo_path,
                )

                if result.returncode == 0:
                    # Parse compliance score from output
                    for line in result.stdout.split("\n"):
                        if "Compliance Score:" in line:
                            score_match = re.search(r"(\d+\.?\d*)%", line)
                            if score_match:
                                compliance_score = float(score_match.group(1))
                                check_result["score"] = compliance_score

                                if compliance_score < 70:
                                    check_result["status"] = "critical"
                                    check_result["issues"].append(f"Low compliance score: {compliance_score:.1f}%")
                                elif compliance_score < 85:
                                    check_result["status"] = "warning"
                                    check_result["issues"].append(f"Moderate compliance score: {compliance_score:.1f}%")

                                check_result["details"]["compliance_score"] = compliance_score
                                break
                else:
                    check_result["issues"].append("Compliance script failed to run")
                    check_result["score"] = 80
            else:
                check_result["issues"].append("Compliance calculation script not found")
                check_result["score"] = 90

            # Check for required documentation
            required_docs = [
                "README.md",
                "docs/core/CONTRIBUTING.md",
                "docs/core/CODE_OF_CONDUCT.md",
                "LICENSE",
            ]

            missing_docs = []
            for doc in required_docs:
                if not os.path.exists(os.path.join(self.repo_path, doc)):
                    missing_docs.append(doc)

            if missing_docs:
                check_result["issues"].append(f"Missing required documentation: {', '.join(missing_docs)}")
                check_result["score"] = max(0, check_result["score"] - len(missing_docs) * 5)

            check_result["details"]["missing_documentation"] = missing_docs

        except Exception as e:
            check_result["status"] = "warning"
            check_result["score"] = 75
            check_result["issues"].append(f"Error checking compliance: {e!s}")

        return check_result

    def _calculate_overall_health(self, health_report):
        """Calculate overall health score and status"""
        checks = health_report["checks"]

        if not checks:
            health_report["overall_status"] = "unknown"
            health_report["health_score"] = 0
            return health_report

        # Calculate weighted average score
        weights = {
            "file_integrity": 0.2,
            "dependency_validation": 0.15,
            "link_validation": 0.1,
            "standards_consistency": 0.2,
            "git_health": 0.15,
            "system_resources": 0.1,
            "security_validation": 0.05,
            "compliance_checking": 0.05,
        }

        total_score = 0
        total_weight = 0

        for check_name, check_result in checks.items():
            weight = weights.get(check_name, 0.1)
            score = check_result.get("score", 0)
            total_score += score * weight
            total_weight += weight

        overall_score = total_score / total_weight if total_weight > 0 else 0
        health_report["health_score"] = round(overall_score, 2)

        # Determine overall status
        critical_checks = [check for check in checks.values() if check.get("status") == "critical"]
        warning_checks = [check for check in checks.values() if check.get("status") == "warning"]

        if critical_checks or overall_score < 60:
            health_report["overall_status"] = "critical"
        elif warning_checks or overall_score < 80:
            health_report["overall_status"] = "warning"
        else:
            health_report["overall_status"] = "healthy"

        # Collect all alerts and recommendations
        all_issues = []
        for check_result in checks.values():
            all_issues.extend(check_result.get("issues", []))

        health_report["alerts"] = all_issues

        # Generate recommendations
        recommendations = []
        if overall_score < 80:
            recommendations.append("Consider running individual health checks to identify specific issues")

        if any(check.get("status") == "critical" for check in checks.values()):
            recommendations.append("Critical issues detected - immediate attention required")

        if len(all_issues) > 10:
            recommendations.append("Multiple issues detected - prioritize fixes based on severity")

        health_report["recommendations"] = recommendations

        return health_report

    def _save_health_report(self, health_report):
        """Save health report to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save detailed JSON report
        json_filename = f"health_report_{timestamp}.json"
        json_path = os.path.join(self.health_dir, json_filename)

        with open(json_path, "w") as f:
            json.dump(health_report, f, indent=2, default=str)

        # Save latest report
        latest_path = os.path.join(self.health_dir, "latest_health_report.json")
        with open(latest_path, "w") as f:
            json.dump(health_report, f, indent=2, default=str)

        # Save summary text report
        summary_text = self._format_health_summary(health_report)
        text_filename = f"health_summary_{timestamp}.txt"
        text_path = os.path.join(self.health_dir, text_filename)

        with open(text_path, "w") as f:
            f.write(summary_text)

        self.logger.info(f"Health report saved: {json_filename}")

    def _format_health_summary(self, health_report):
        """Format health report as readable text summary"""
        timestamp = datetime.fromisoformat(health_report["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")

        text = f"""
REPOSITORY HEALTH REPORT
========================
Generated: {timestamp}
Overall Status: {health_report["overall_status"].upper()}
Health Score: {health_report["health_score"]}/100

HEALTH CHECK RESULTS
-------------------
"""

        for check_name, check_result in health_report["checks"].items():
            status = check_result["status"].upper()
            score = check_result["score"]
            text += f"{check_name.replace('_', ' ').title()}: {status} ({score}/100)\n"

            if check_result.get("issues"):
                for issue in check_result["issues"][:3]:  # First 3 issues
                    text += f"  - {issue}\n"

        if health_report["alerts"]:
            text += "\nALERTS\n------\n"
            for alert in health_report["alerts"][:10]:  # First 10 alerts
                text += f"• {alert}\n"

        if health_report["recommendations"]:
            text += "\nRECOMMENDATIONS\n---------------\n"
            for rec in health_report["recommendations"]:
                text += f"• {rec}\n"

        return text


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Repository Health Monitor")
    parser.add_argument("--repo-path", help="Path to repository (default: current directory)")
    parser.add_argument(
        "--output",
        choices=["json", "text", "both"],
        default="both",
        help="Output format (default: both)",
    )

    args = parser.parse_args()

    monitor = HealthMonitor(repo_path=args.repo_path)

    print("🔍 Running comprehensive health check...")
    health_report = monitor.run_comprehensive_health_check()

    print("\n📊 Health Check Results:")
    print(f"Overall Status: {health_report['overall_status'].upper()}")
    print(f"Health Score: {health_report['health_score']}/100")

    if health_report["alerts"]:
        print(f"\n⚠️  Issues Found: {len(health_report['alerts'])}")
        for alert in health_report["alerts"][:5]:
            print(f"  • {alert}")

    if health_report["recommendations"]:
        print("\n💡 Recommendations:")
        for rec in health_report["recommendations"]:
            print(f"  • {rec}")

    print(f"\n📁 Detailed reports saved to: {monitor.health_dir}")


if __name__ == "__main__":
    main()
