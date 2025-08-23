#!/usr/bin/env python3
"""
Setup Script for Standards Repository Monitoring System

This script sets up the complete monitoring infrastructure including:
- Directory structure
- Configuration files
- Cron jobs for automated reporting
- Dependencies installation
- Initial health check
"""

import json
import logging
import os
import subprocess
import sys


class MonitoringSetup:
    """Setup and configure the monitoring system"""

    def __init__(self, repo_path=None):
        self.repo_path = repo_path or os.getcwd()
        self.monitoring_dir = os.path.join(self.repo_path, "monitoring")

        # Setup logging
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        self.logger = logging.getLogger(__name__)

    def setup_directories(self):
        """Create necessary directory structure"""
        directories = [
            "monitoring",
            "monitoring/metrics",
            "monitoring/reports",
            "monitoring/health",
            "monitoring/logs",
            "monitoring/config",
        ]

        self.logger.info("Creating directory structure...")
        for dir_path in directories:
            full_path = os.path.join(self.repo_path, dir_path)
            os.makedirs(full_path, exist_ok=True)
            self.logger.info(f"✓ Created {dir_path}")

    def create_config_files(self):
        """Create configuration files"""
        self.logger.info("Creating configuration files...")

        # Main monitoring configuration
        monitoring_config = {
            "monitoring": {
                "enabled": True,
                "interval_minutes": 60,
                "retention_days": 30,
                "log_level": "INFO",
            },
            "health_checks": {
                "file_integrity": True,
                "dependency_validation": True,
                "link_validation": True,
                "standards_consistency": True,
                "git_health": True,
                "system_resources": True,
                "security_validation": True,
                "compliance_checking": True,
            },
            "performance_monitoring": {
                "enabled": True,
                "continuous_monitoring": False,
                "benchmark_scripts": True,
                "resource_tracking": True,
            },
            "analytics": {
                "enabled": True,
                "track_usage": True,
                "collect_metrics": True,
                "generate_insights": True,
            },
            "reporting": {
                "daily_summary": True,
                "weekly_analysis": True,
                "monthly_comprehensive": True,
                "alert_threshold": {
                    "health_score": 80,
                    "performance_degradation": 20,
                    "error_rate": 5,
                },
            },
            "notifications": {
                "email": {
                    "enabled": False,
                    "smtp_server": "smtp.gmail.com",
                    "smtp_port": 587,
                    "username": "",
                    "password": "",
                    "recipients": [],
                },
                "slack_webhook": "",
                "discord_webhook": "",
                "teams_webhook": "",
            },
            "dashboard": {
                "enabled": True,
                "port": 8080,
                "host": "localhost",
                "auto_refresh_minutes": 5,
            },
        }

        config_path = os.path.join(self.monitoring_dir, "config", "monitoring_config.json")
        with open(config_path, "w") as f:
            json.dump(monitoring_config, f, indent=2)

        self.logger.info(f"✓ Created monitoring configuration: {config_path}")

        # Performance thresholds configuration
        thresholds_config = {
            "performance_thresholds": {
                "git_operation_warning": 5.0,
                "git_operation_critical": 15.0,
                "file_read_warning": 1.0,
                "file_read_critical": 5.0,
                "script_execution_warning": 10.0,
                "script_execution_critical": 30.0,
                "memory_usage_warning": 80,
                "memory_usage_critical": 95,
                "cpu_usage_warning": 80,
                "cpu_usage_critical": 95,
            },
            "health_thresholds": {
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
            },
        }

        thresholds_path = os.path.join(self.monitoring_dir, "config", "thresholds.json")
        with open(thresholds_path, "w") as f:
            json.dump(thresholds_config, f, indent=2)

        self.logger.info(f"✓ Created thresholds configuration: {thresholds_path}")

    def create_wrapper_scripts(self):
        """Create wrapper scripts for easy execution"""
        self.logger.info("Creating wrapper scripts...")

        # Create run_monitoring.sh
        monitoring_script = f"""#!/bin/bash
# Standards Repository Monitoring Wrapper Script

set -e

REPO_PATH="{self.repo_path}"
MONITORING_DIR="$REPO_PATH/monitoring"

cd "$REPO_PATH"

echo "🔍 Running repository monitoring..."

# Run analytics collection
if [ -f "$MONITORING_DIR/analytics_collector.py" ]; then
    echo "📊 Collecting analytics..."
    python3 "$MONITORING_DIR/analytics_collector.py"
fi

# Run performance monitoring
if [ -f "$MONITORING_DIR/performance_monitor.py" ]; then
    echo "⚡ Running performance monitoring..."
    python3 "$MONITORING_DIR/performance_monitor.py"
fi

# Run health check
if [ -f "$MONITORING_DIR/health_monitor.py" ]; then
    echo "🏥 Running health check..."
    python3 "$MONITORING_DIR/health_monitor.py"
fi

# Generate automated reports
if [ -f "$MONITORING_DIR/automated_reports.py" ]; then
    echo "📝 Generating reports..."
    python3 "$MONITORING_DIR/automated_reports.py" --scheduled
fi

echo "✅ Monitoring completed successfully!"
"""

        script_path = os.path.join(self.monitoring_dir, "run_monitoring.sh")
        with open(script_path, "w") as f:
            f.write(monitoring_script)

        os.chmod(script_path, 0o755)
        self.logger.info(f"✓ Created monitoring script: {script_path}")

        # Create start_dashboard.sh
        dashboard_script = f"""#!/bin/bash
# Start Monitoring Dashboard

set -e

REPO_PATH="{self.repo_path}"
MONITORING_DIR="$REPO_PATH/monitoring"

cd "$REPO_PATH"

echo "🚀 Starting monitoring dashboard..."

if [ -f "$MONITORING_DIR/dashboard_server.py" ]; then
    python3 "$MONITORING_DIR/dashboard_server.py" --port 8080 --host localhost
else
    echo "❌ Dashboard server not found!"
    exit 1
fi
"""

        dashboard_script_path = os.path.join(self.monitoring_dir, "start_dashboard.sh")
        with open(dashboard_script_path, "w") as f:
            f.write(dashboard_script)

        os.chmod(dashboard_script_path, 0o755)
        self.logger.info(f"✓ Created dashboard script: {dashboard_script_path}")

    def check_dependencies(self):
        """Check and install required dependencies"""
        self.logger.info("Checking dependencies...")

        required_packages = ["psutil", "pyyaml"]
        missing_packages = []

        for package in required_packages:
            try:
                __import__(package)
                self.logger.info(f"✓ {package} is available")
            except ImportError:
                missing_packages.append(package)
                self.logger.warning(f"✗ {package} is missing")

        if missing_packages:
            self.logger.info(f"Installing missing packages: {', '.join(missing_packages)}")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install"] + missing_packages,
                    check=True,
                )
                self.logger.info("✓ Dependencies installed successfully")
            except subprocess.CalledProcessError as e:
                self.logger.error(f"Failed to install dependencies: {e}")
                self.logger.info("Please install manually: pip install " + " ".join(missing_packages))
        else:
            self.logger.info("✓ All dependencies are satisfied")

    def create_cron_jobs(self):
        """Create cron job suggestions for automated monitoring"""
        self.logger.info("Creating cron job configuration...")

        cron_config = f"""# Standards Repository Monitoring Cron Jobs
# Add these to your crontab with: crontab -e

# Run monitoring every hour
0 * * * * cd {self.repo_path} && ./monitoring/run_monitoring.sh >> ./monitoring/logs/cron.log 2>&1

# Generate daily report at 6 AM
0 6 * * * cd {self.repo_path} && python3 ./monitoring/automated_reports.py --daily >> ./monitoring/logs/daily_reports.log 2>&1

# Generate weekly report on Sundays at 7 AM
0 7 * * 0 cd {self.repo_path} && python3 ./monitoring/automated_reports.py --weekly >> ./monitoring/logs/weekly_reports.log 2>&1

# Generate monthly report on the 1st of each month at 8 AM
0 8 1 * * cd {self.repo_path} && python3 ./monitoring/automated_reports.py --monthly >> ./monitoring/logs/monthly_reports.log 2>&1

# Health check every 6 hours
0 */6 * * * cd {self.repo_path} && python3 ./monitoring/health_monitor.py >> ./monitoring/logs/health_check.log 2>&1
"""

        cron_path = os.path.join(self.monitoring_dir, "config", "cron_jobs.txt")
        with open(cron_path, "w") as f:
            f.write(cron_config)

        self.logger.info(f"✓ Created cron configuration: {cron_path}")
        self.logger.info("To enable automated monitoring, add the cron jobs with: crontab -e")

    def create_requirements_file(self):
        """Create requirements file for monitoring dependencies"""
        requirements = """# Standards Repository Monitoring Requirements
psutil>=5.8.0
pyyaml>=6.0
"""

        req_path = os.path.join(self.monitoring_dir, "requirements.txt")
        with open(req_path, "w") as f:
            f.write(requirements)

        self.logger.info(f"✓ Created requirements file: {req_path}")

    def create_readme(self):
        """Create README for the monitoring system"""
        readme_content = """# Standards Repository Monitoring System

This directory contains a comprehensive monitoring system for the standards repository that provides:

## Features

- **Analytics Collection**: Track standards usage patterns and repository metrics
- **Performance Monitoring**: Monitor Git operations, file access, and script execution performance
- **Health Monitoring**: Comprehensive health checks for repository integrity and compliance
- **Automated Reporting**: Daily, weekly, and monthly reports with trend analysis
- **Real-time Dashboard**: Web-based dashboard with visualizations and metrics
- **Alerting System**: Configurable alerts for performance and health issues

## Quick Start

### 1. Install Dependencies
```bash
pip install -r monitoring/requirements.txt
```

### 2. Run Initial Setup
```bash
python3 monitoring/setup_monitoring.py
```

### 3. Start Monitoring
```bash
# One-time monitoring run
./monitoring/run_monitoring.sh

# Start dashboard
./monitoring/start_dashboard.sh
```

### 4. Enable Automated Monitoring (Optional)
```bash
# Add cron jobs for automated monitoring
crontab -e
# Then copy the contents from monitoring/config/cron_jobs.txt
```

## Components

### Core Scripts

- `analytics_collector.py` - Collects repository usage and metrics data
- `performance_monitor.py` - Monitors system and operation performance
- `health_monitor.py` - Comprehensive repository health checks
- `automated_reports.py` - Generates automated reports and alerts
- `dashboard_server.py` - Web dashboard server with real-time data

### Dashboard

The web dashboard is available at `http://localhost:8080/dashboard` when running and provides:

- Real-time performance metrics
- Repository health status
- Usage analytics and trends
- Interactive charts and visualizations
- Alert notifications

### Configuration

Configuration files are located in `monitoring/config/`:

- `monitoring_config.json` - Main monitoring configuration
- `thresholds.json` - Performance and health thresholds
- `cron_jobs.txt` - Suggested cron job configuration

### Reports

Reports are automatically generated in `monitoring/reports/`:

- Daily summaries
- Weekly trend analysis
- Monthly comprehensive reports
- Health check results

### Logs

All monitoring logs are stored in `monitoring/logs/`:

- `analytics.log` - Analytics collection logs
- `performance.log` - Performance monitoring logs
- `health_monitor.log` - Health check logs
- `automated_reports.log` - Reporting system logs

## Manual Commands

### Generate Reports
```bash
# Daily summary
python3 monitoring/automated_reports.py --daily

# Weekly analysis
python3 monitoring/automated_reports.py --weekly

# Monthly comprehensive report
python3 monitoring/automated_reports.py --monthly
```

### Run Health Checks
```bash
# Full health check
python3 monitoring/health_monitor.py

# Performance monitoring
python3 monitoring/performance_monitor.py
```

### Collect Analytics
```bash
# Collect all metrics
python3 monitoring/analytics_collector.py
```

## Customization

### Thresholds
Edit `monitoring/config/thresholds.json` to adjust warning and critical thresholds for:
- Performance metrics
- Health checks
- Resource usage
- Error rates

### Notifications
Configure email, Slack, or other notifications in `monitoring/config/monitoring_config.json`:

```json
{
  "notifications": {
    "email": {
      "enabled": true,
      "smtp_server": "smtp.gmail.com",
      "username": "your-email@gmail.com",
      "recipients": ["team@company.com"]
    },
    "slack_webhook": "https://hooks.slack.com/..."
  }
}
```

### Dashboard
Customize dashboard settings:
- Port and host configuration
- Auto-refresh intervals
- Chart configurations

## Troubleshooting

### Common Issues

1. **Permission Errors**: Ensure scripts are executable (`chmod +x monitoring/*.sh`)
2. **Missing Dependencies**: Install with `pip install -r monitoring/requirements.txt`
3. **Port Conflicts**: Change dashboard port in configuration
4. **Cron Jobs Not Running**: Check cron logs and file paths

### Debug Mode
Enable debug logging by setting log level to "DEBUG" in configuration.

### Support
For issues or questions, check the logs in `monitoring/logs/` for detailed error information.
"""

        readme_path = os.path.join(self.monitoring_dir, "README.md")
        with open(readme_path, "w") as f:
            f.write(readme_content)

        self.logger.info(f"✓ Created README: {readme_path}")

    def run_initial_health_check(self):
        """Run initial health check to verify setup"""
        self.logger.info("Running initial health check...")

        try:
            # Import and run health monitor
            sys.path.append(self.monitoring_dir)
            from health_monitor import HealthMonitor

            monitor = HealthMonitor(self.repo_path)
            health_report = monitor.run_comprehensive_health_check()

            self.logger.info("✓ Initial health check completed")
            self.logger.info(f"  Overall Status: {health_report['overall_status']}")
            self.logger.info(f"  Health Score: {health_report['health_score']}/100")

            if health_report["alerts"]:
                self.logger.warning(f"  Issues found: {len(health_report['alerts'])}")
                for alert in health_report["alerts"][:3]:
                    self.logger.warning(f"    - {alert}")

        except Exception as e:
            self.logger.error(f"Initial health check failed: {e}")

    def setup_monitoring_system(self):
        """Run complete setup process"""
        self.logger.info("🚀 Setting up Standards Repository Monitoring System...")

        try:
            self.setup_directories()
            self.check_dependencies()
            self.create_config_files()
            self.create_wrapper_scripts()
            self.create_cron_jobs()
            self.create_requirements_file()
            self.create_readme()
            self.run_initial_health_check()

            self.logger.info("✅ Monitoring system setup completed successfully!")
            self.logger.info(f"📁 Monitoring directory: {self.monitoring_dir}")
            self.logger.info("📖 See monitoring/README.md for usage instructions")
            self.logger.info("🌐 Start dashboard with: ./monitoring/start_dashboard.sh")
            self.logger.info("⚙️  Enable automation with cron jobs from: monitoring/config/cron_jobs.txt")

        except Exception as e:
            self.logger.error(f"Setup failed: {e}")
            raise


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Setup Standards Repository Monitoring System")
    parser.add_argument("--repo-path", help="Path to repository (default: current directory)")
    parser.add_argument("--force", action="store_true", help="Force overwrite existing files")

    args = parser.parse_args()

    if args.repo_path and not os.path.exists(args.repo_path):
        print(f"❌ Repository path does not exist: {args.repo_path}")
        return 1

    setup = MonitoringSetup(repo_path=args.repo_path)

    try:
        setup.setup_monitoring_system()
        return 0
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
