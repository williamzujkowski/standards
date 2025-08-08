# Standards Repository Monitoring System

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
