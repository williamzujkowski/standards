#!/usr/bin/env python3
"""
Automated Reporting System for Standards Repository

This script generates automated reports including:
- Daily performance summaries
- Weekly trend analysis
- Monthly comprehensive reports
- Alert notifications
- Compliance tracking
"""

import json
import logging
import os
import smtplib
import statistics
import sys
from datetime import datetime, timedelta
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from analytics_collector import AnalyticsCollector
    from performance_monitor import PerformanceMonitor
except ImportError:
    print("Warning: Could not import monitoring modules")
    AnalyticsCollector = None
    PerformanceMonitor = None


class AutomatedReporter:
    """Generates and sends automated reports"""

    def __init__(self, repo_path=None, config_file=None):
        self.repo_path = repo_path or os.getcwd()
        self.config = self._load_config(config_file)

        # Setup directories
        self.reports_dir = os.path.join(self.repo_path, "monitoring", "reports")
        self.metrics_dir = os.path.join(self.repo_path, "monitoring", "metrics")
        self.logs_dir = os.path.join(self.repo_path, "monitoring", "logs")

        for dir_path in [self.reports_dir, self.metrics_dir, self.logs_dir]:
            os.makedirs(dir_path, exist_ok=True)

        # Setup logging
        logging.basicConfig(
            filename=os.path.join(self.logs_dir, "automated_reports.log"),
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger(__name__)

        # Initialize collectors
        self.analytics = AnalyticsCollector(self.repo_path) if AnalyticsCollector else None
        self.performance = PerformanceMonitor(self.repo_path) if PerformanceMonitor else None

    def _load_config(self, config_file):
        """Load reporting configuration"""
        default_config = {
            "email": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "username": "",
                "password": "",
                "recipients": [],
            },
            "reports": {
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
                "slack_webhook": "",
                "discord_webhook": "",
                "teams_webhook": "",
            },
        }

        if config_file and os.path.exists(config_file):
            try:
                with open(config_file) as f:
                    user_config = json.load(f)
                    # Merge with defaults
                    default_config.update(user_config)
            except Exception as e:
                self.logger.warning(f"Failed to load config file: {e}")

        return default_config

    def generate_daily_summary(self):
        """Generate daily performance summary"""
        try:
            today = datetime.now()
            report_data = {
                "date": today.isoformat(),
                "type": "daily_summary",
                "generated_at": today.isoformat(),
            }

            # Collect current metrics
            if self.analytics:
                git_metrics = self.analytics.collect_git_metrics()
                health_metrics = self.analytics.collect_repository_health_metrics()
                report_data["git_activity"] = git_metrics
                report_data["repository_health"] = health_metrics

            if self.performance:
                perf_report = self.performance.generate_performance_report()
                report_data["performance"] = perf_report

            # Generate summary text
            summary_text = self._format_daily_summary(report_data)

            # Save report
            report_filename = f"daily_summary_{today.strftime('%Y%m%d')}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2, default=str)

            # Save text version
            text_filename = f"daily_summary_{today.strftime('%Y%m%d')}.txt"
            text_path = os.path.join(self.reports_dir, text_filename)

            with open(text_path, "w") as f:
                f.write(summary_text)

            self.logger.info(f"Daily summary generated: {report_filename}")

            # Check for alerts
            alerts = self._check_daily_alerts(report_data)
            if alerts:
                self._send_alerts(alerts, "Daily Alert")

            return report_data

        except Exception as e:
            self.logger.error(f"Failed to generate daily summary: {e}")
            return None

    def generate_weekly_analysis(self):
        """Generate weekly trend analysis"""
        try:
            today = datetime.now()
            week_start = today - timedelta(days=7)

            report_data = {
                "week_ending": today.isoformat(),
                "week_starting": week_start.isoformat(),
                "type": "weekly_analysis",
                "generated_at": today.isoformat(),
            }

            # Collect weekly metrics
            weekly_metrics = self._collect_weekly_metrics(week_start, today)
            report_data.update(weekly_metrics)

            # Generate analysis text
            analysis_text = self._format_weekly_analysis(report_data)

            # Save report
            report_filename = f"weekly_analysis_{today.strftime('%Y%m%d')}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2, default=str)

            # Save text version
            text_filename = f"weekly_analysis_{today.strftime('%Y%m%d')}.txt"
            text_path = os.path.join(self.reports_dir, text_filename)

            with open(text_path, "w") as f:
                f.write(analysis_text)

            self.logger.info(f"Weekly analysis generated: {report_filename}")

            # Send weekly report if configured
            if self.config["email"]["enabled"]:
                self._send_email_report(
                    analysis_text,
                    f"Weekly Standards Repository Analysis - {today.strftime('%Y-%m-%d')}",
                )

            return report_data

        except Exception as e:
            self.logger.error(f"Failed to generate weekly analysis: {e}")
            return None

    def generate_monthly_comprehensive(self):
        """Generate comprehensive monthly report"""
        try:
            today = datetime.now()
            month_start = today.replace(day=1)

            report_data = {
                "month": today.strftime("%Y-%m"),
                "month_start": month_start.isoformat(),
                "month_end": today.isoformat(),
                "type": "monthly_comprehensive",
                "generated_at": today.isoformat(),
            }

            # Collect comprehensive monthly data
            monthly_data = self._collect_monthly_metrics(month_start, today)
            report_data.update(monthly_data)

            # Generate comprehensive report text
            comprehensive_text = self._format_monthly_comprehensive(report_data)

            # Save report
            report_filename = f"monthly_comprehensive_{today.strftime('%Y%m')}.json"
            report_path = os.path.join(self.reports_dir, report_filename)

            with open(report_path, "w") as f:
                json.dump(report_data, f, indent=2, default=str)

            # Save text version
            text_filename = f"monthly_comprehensive_{today.strftime('%Y%m')}.txt"
            text_path = os.path.join(self.reports_dir, text_filename)

            with open(text_path, "w") as f:
                f.write(comprehensive_text)

            self.logger.info(f"Monthly comprehensive report generated: {report_filename}")

            # Send monthly report if configured
            if self.config["email"]["enabled"]:
                self._send_email_report(
                    comprehensive_text,
                    f"Monthly Standards Repository Report - {today.strftime('%B %Y')}",
                    attach_file=report_path,
                )

            return report_data

        except Exception as e:
            self.logger.error(f"Failed to generate monthly comprehensive report: {e}")
            return None

    def _collect_weekly_metrics(self, start_date, end_date):
        """Collect metrics for the past week"""
        metrics = {
            "period_days": (end_date - start_date).days,
            "trends": {},
            "averages": {},
            "totals": {},
        }

        # Try to collect daily reports from the week
        daily_reports = []
        for i in range(7):
            date = start_date + timedelta(days=i)
            daily_file = os.path.join(self.reports_dir, f"daily_summary_{date.strftime('%Y%m%d')}.json")
            if os.path.exists(daily_file):
                try:
                    with open(daily_file) as f:
                        daily_data = json.load(f)
                        daily_reports.append(daily_data)
                except:
                    pass

        if daily_reports:
            # Calculate trends and averages
            health_scores = [r.get("performance", {}).get("health_score", {}).get("overall", 0) for r in daily_reports]
            git_commits = [r.get("git_activity", {}).get("commits", {}).get("today", 0) for r in daily_reports]

            metrics["averages"] = {
                "health_score": statistics.mean(health_scores) if health_scores else 0,
                "daily_commits": statistics.mean(git_commits) if git_commits else 0,
            }

            metrics["totals"] = {
                "total_commits": sum(git_commits),
                "reports_available": len(daily_reports),
            }

            # Trend analysis
            if len(health_scores) >= 2:
                trend = health_scores[-1] - health_scores[0]
                metrics["trends"]["health_score_trend"] = (
                    "improving" if trend > 0 else "declining" if trend < 0 else "stable"
                )

        return metrics

    def _collect_monthly_metrics(self, start_date, end_date):
        """Collect comprehensive metrics for the month"""
        metrics = {
            "period_days": (end_date - start_date).days,
            "summary": {},
            "trends": {},
            "performance_analysis": {},
            "repository_growth": {},
        }

        # Collect all available daily and weekly reports
        all_reports = []
        reports_dir = Path(self.reports_dir)

        for report_file in reports_dir.glob("daily_summary_*.json"):
            try:
                with open(report_file) as f:
                    data = json.load(f)
                    report_date = datetime.fromisoformat(data.get("date", ""))
                    if start_date <= report_date <= end_date:
                        all_reports.append(data)
            except:
                continue

        if all_reports:
            # Calculate comprehensive statistics
            health_scores = [r.get("performance", {}).get("health_score", {}).get("overall", 0) for r in all_reports]

            metrics["summary"] = {
                "average_health_score": (statistics.mean(health_scores) if health_scores else 0),
                "max_health_score": max(health_scores) if health_scores else 0,
                "min_health_score": min(health_scores) if health_scores else 0,
                "health_score_std_dev": (statistics.stdev(health_scores) if len(health_scores) > 1 else 0),
                "total_monitoring_days": len(all_reports),
            }

        # Add current repository state
        if self.analytics:
            current_metrics = self.analytics.collect_all_metrics()
            metrics["current_state"] = current_metrics

        return metrics

    def _format_daily_summary(self, data):
        """Format daily summary as readable text"""
        date = datetime.fromisoformat(data["date"]).strftime("%Y-%m-%d")

        text = f"""
DAILY STANDARDS REPOSITORY SUMMARY
==================================
Date: {date}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

PERFORMANCE OVERVIEW
-------------------
"""

        if "performance" in data:
            health = data["performance"].get("health_score", {})
            text += f"Overall Health Score: {health.get('overall', 'N/A')}/100\n"
            text += f"Git Operations: {health.get('git_operations', 'N/A')}/100\n"
            text += f"File Operations: {health.get('file_operations', 'N/A')}/100\n"
            text += f"System Efficiency: {health.get('cpu_efficiency', 'N/A')}/100\n"

        text += "\nGIT ACTIVITY\n------------\n"
        if "git_activity" in data:
            git = data["git_activity"]
            text += f"Commits today: {git.get('commits', {}).get('today', 0)}\n"
            text += f"Commits last 7 days: {git.get('commits', {}).get('last_7_days', 0)}\n"

            contributors = git.get("contributors", {})
            if contributors:
                text += f"Active contributors: {len(contributors)}\n"

        text += "\nREPOSITORY HEALTH\n-----------------\n"
        if "repository_health" in data:
            health = data["repository_health"]
            text += f"Documentation coverage: {health.get('documentation_coverage', 0):.1f}%\n"
            text += f"Link health: {health.get('link_health', {}).get('health_score', 0):.1f}%\n"

            file_counts = health.get("file_counts", {})
            text += f"Total files: {file_counts.get('total', 0)}\n"
            text += f"Markdown files: {file_counts.get('markdown', 0)}\n"

        return text

    def _format_weekly_analysis(self, data):
        """Format weekly analysis as readable text"""
        week_end = datetime.fromisoformat(data["week_ending"]).strftime("%Y-%m-%d")

        text = f"""
WEEKLY STANDARDS REPOSITORY ANALYSIS
=====================================
Week Ending: {week_end}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

WEEKLY SUMMARY
--------------
"""

        averages = data.get("averages", {})
        totals = data.get("totals", {})
        trends = data.get("trends", {})

        text += f"Average Health Score: {averages.get('health_score', 0):.1f}/100\n"
        text += f"Total Commits: {totals.get('total_commits', 0)}\n"
        text += f"Average Daily Commits: {averages.get('daily_commits', 0):.1f}\n"
        text += f"Days Monitored: {totals.get('reports_available', 0)}/7\n"

        text += "\nTREND ANALYSIS\n--------------\n"
        health_trend = trends.get("health_score_trend", "unknown")
        text += f"Health Score Trend: {health_trend.title()}\n"

        text += "\nRECOMMENDations\n---------------\n"
        if averages.get("health_score", 0) < 80:
            text += "• Consider investigating performance issues (health score below 80)\n"
        if totals.get("total_commits", 0) == 0:
            text += "• No commits detected this week - repository may be inactive\n"
        if totals.get("reports_available", 0) < 5:
            text += "• Limited monitoring data available - consider improving data collection\n"

        if averages.get("health_score", 0) >= 90:
            text += "• Excellent repository health - maintain current practices\n"

        return text

    def _format_monthly_comprehensive(self, data):
        """Format monthly comprehensive report as readable text"""
        month = data["month"]

        text = f"""
MONTHLY COMPREHENSIVE STANDARDS REPOSITORY REPORT
==================================================
Month: {month}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

EXECUTIVE SUMMARY
-----------------
"""

        summary = data.get("summary", {})
        text += f"Average Health Score: {summary.get('average_health_score', 0):.1f}/100\n"
        text += f"Best Performance: {summary.get('max_health_score', 0):.1f}/100\n"
        text += f"Worst Performance: {summary.get('min_health_score', 0):.1f}/100\n"
        text += f"Performance Stability: {summary.get('health_score_std_dev', 0):.1f} (std dev)\n"
        text += f"Monitoring Coverage: {summary.get('total_monitoring_days', 0)} days\n"

        text += "\nKEY METRICS\n-----------\n"

        current_state = data.get("current_state", {})
        if current_state:
            git_metrics = current_state.get("git_metrics", {})
            text += f"Total commits (30 days): {git_metrics.get('commits', {}).get('last_30_days', 0)}\n"

            standards_metrics = current_state.get("standards_metrics", {})
            text += f"Standards tracked: {len(standards_metrics)}\n"

            health_metrics = current_state.get("health_metrics", {})
            text += f"Repository size: {health_metrics.get('repository_size', 0) / (1024*1024):.1f} MB\n"

        text += "\nRECOMMENDATIONS FOR NEXT MONTH\n------------------------------\n"

        avg_health = summary.get("average_health_score", 0)
        if avg_health >= 90:
            text += "• Excellent performance - maintain current monitoring and practices\n"
        elif avg_health >= 80:
            text += "• Good performance - identify areas for optimization\n"
        elif avg_health >= 70:
            text += "• Moderate performance - investigate performance bottlenecks\n"
        else:
            text += "• Poor performance - urgent attention required\n"

        stability = summary.get("health_score_std_dev", 0)
        if stability > 10:
            text += "• High performance variability detected - investigate consistency issues\n"

        monitoring_days = summary.get("total_monitoring_days", 0)
        if monitoring_days < 20:
            text += "• Improve monitoring data collection for better insights\n"

        return text

    def _check_daily_alerts(self, data):
        """Check for conditions that require alerts"""
        alerts = []
        thresholds = self.config["reports"]["alert_threshold"]

        # Check health score
        if "performance" in data:
            health = data["performance"].get("health_score", {}).get("overall", 100)
            if health < thresholds["health_score"]:
                alerts.append(
                    {
                        "level": "warning",
                        "message": f"Health score dropped to {health:.1f}% (threshold: {thresholds['health_score']}%)",
                        "metric": "health_score",
                        "value": health,
                    }
                )

        # Check for performance issues
        if "performance" in data:
            git_ops = data["performance"].get("git_operations", {})
            failed_ops = sum(1 for op in git_ops.values() if not op.get("success", True))
            total_ops = len(git_ops)
            if total_ops > 0:
                error_rate = (failed_ops / total_ops) * 100
                if error_rate > thresholds["error_rate"]:
                    alerts.append(
                        {
                            "level": "critical",
                            "message": (
                                f"High error rate detected: {error_rate:.1f}% "
                                f"(threshold: {thresholds['error_rate']}%)"
                            ),
                            "metric": "error_rate",
                            "value": error_rate,
                        }
                    )

        return alerts

    def _send_alerts(self, alerts, subject_prefix="Alert"):
        """Send alerts via configured channels"""
        if not alerts:
            return

        alert_text = f"{subject_prefix}\n" + "=" * len(subject_prefix) + "\n\n"
        for alert in alerts:
            alert_text += f"[{alert['level'].upper()}] {alert['message']}\n"

        alert_text += f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

        # Send email if configured
        if self.config["email"]["enabled"]:
            self._send_email_report(alert_text, f"{subject_prefix} - Standards Repository")

        # Log alerts
        for alert in alerts:
            if alert["level"] == "critical":
                self.logger.critical(alert["message"])
            else:
                self.logger.warning(alert["message"])

    def _send_email_report(self, content, subject, attach_file=None):
        """Send email report"""
        try:
            email_config = self.config["email"]
            if not email_config["enabled"] or not email_config["recipients"]:
                return

            msg = MIMEMultipart()
            msg["From"] = email_config["username"]
            msg["To"] = ", ".join(email_config["recipients"])
            msg["Subject"] = subject

            msg.attach(MIMEText(content, "plain"))

            # Attach file if provided
            if attach_file and os.path.exists(attach_file):
                with open(attach_file, "rb") as attachment:
                    part = MIMEBase("application", "octet-stream")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {os.path.basename(attach_file)}",
                    )
                    msg.attach(part)

            # Send email
            server = smtplib.SMTP(email_config["smtp_server"], email_config["smtp_port"])
            server.starttls()
            server.login(email_config["username"], email_config["password"])
            server.send_message(msg)
            server.quit()

            self.logger.info(f"Email report sent: {subject}")

        except Exception as e:
            self.logger.error(f"Failed to send email report: {e}")

    def run_scheduled_reports(self):
        """Run all scheduled reports based on current time"""
        now = datetime.now()

        # Run daily summary every day
        if self.config["reports"]["daily_summary"]:
            self.generate_daily_summary()

        # Run weekly analysis on Sundays
        if self.config["reports"]["weekly_analysis"] and now.weekday() == 6:
            self.generate_weekly_analysis()

        # Run monthly comprehensive on the last day of the month
        if self.config["reports"]["monthly_comprehensive"]:
            tomorrow = now + timedelta(days=1)
            if tomorrow.month != now.month:  # Last day of month
                self.generate_monthly_comprehensive()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Automated Reporting System")
    parser.add_argument("--repo-path", help="Path to repository (default: current directory)")
    parser.add_argument("--config", help="Path to configuration file")
    parser.add_argument("--daily", action="store_true", help="Generate daily summary")
    parser.add_argument("--weekly", action="store_true", help="Generate weekly analysis")
    parser.add_argument("--monthly", action="store_true", help="Generate monthly comprehensive report")
    parser.add_argument(
        "--scheduled",
        action="store_true",
        help="Run scheduled reports based on current time",
    )

    args = parser.parse_args()

    reporter = AutomatedReporter(repo_path=args.repo_path, config_file=args.config)

    if args.daily:
        print("Generating daily summary...")
        report = reporter.generate_daily_summary()
        if report:
            print("✅ Daily summary generated successfully")
        else:
            print("❌ Failed to generate daily summary")

    elif args.weekly:
        print("Generating weekly analysis...")
        report = reporter.generate_weekly_analysis()
        if report:
            print("✅ Weekly analysis generated successfully")
        else:
            print("❌ Failed to generate weekly analysis")

    elif args.monthly:
        print("Generating monthly comprehensive report...")
        report = reporter.generate_monthly_comprehensive()
        if report:
            print("✅ Monthly comprehensive report generated successfully")
        else:
            print("❌ Failed to generate monthly comprehensive report")

    elif args.scheduled:
        print("Running scheduled reports...")
        reporter.run_scheduled_reports()
        print("✅ Scheduled reports completed")

    else:
        print("Generating all reports...")
        reporter.generate_daily_summary()
        reporter.generate_weekly_analysis()
        reporter.generate_monthly_comprehensive()
        print("✅ All reports generated")


if __name__ == "__main__":
    main()
