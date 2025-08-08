#!/usr/bin/env python3
"""
Dashboard Server for Standards Repository Monitoring

This script serves the monitoring dashboard and provides real-time data
from the analytics collector and performance monitor.
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import threading
import time

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from analytics_collector import AnalyticsCollector
    from performance_monitor import PerformanceMonitor
except ImportError:
    print("Warning: Could not import analytics modules. Dashboard will serve static content only.")
    AnalyticsCollector = None
    PerformanceMonitor = None

class DashboardHandler(SimpleHTTPRequestHandler):
    """Custom HTTP handler for the dashboard"""
    
    def __init__(self, *args, repo_path=None, **kwargs):
        self.repo_path = repo_path or os.getcwd()
        self.analytics_collector = AnalyticsCollector(self.repo_path) if AnalyticsCollector else None
        self.performance_monitor = PerformanceMonitor(self.repo_path) if PerformanceMonitor else None
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # API endpoints
        if parsed_path.path.startswith('/api/'):
            self.handle_api_request(parsed_path)
        elif parsed_path.path == '/' or parsed_path.path == '/dashboard':
            self.serve_dashboard()
        else:
            # Serve static files
            super().do_GET()
    
    def handle_api_request(self, parsed_path):
        """Handle API requests for dashboard data"""
        try:
            if parsed_path.path == '/api/metrics/latest':
                self.serve_latest_metrics()
            elif parsed_path.path == '/api/performance/latest':
                self.serve_performance_data()
            elif parsed_path.path == '/api/usage/standards':
                self.serve_usage_stats()
            elif parsed_path.path == '/api/health/status':
                self.serve_health_status()
            elif parsed_path.path == '/api/git/activity':
                self.serve_git_activity()
            else:
                self.send_error(404, "API endpoint not found")
        except Exception as e:
            self.send_error(500, f"Internal server error: {str(e)}")
    
    def serve_dashboard(self):
        """Serve the main dashboard HTML"""
        dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.html')
        try:
            with open(dashboard_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace mock data endpoints with real API calls
            content = content.replace(
                '// In a real implementation, these would be API calls',
                '// Real API calls enabled'
            )
            
            # Inject real API calls
            api_injection = """
                // Real API implementation
                async function fetchMetrics() {
                    const response = await fetch('/api/metrics/latest');
                    return await response.json();
                }
                
                async function fetchPerformanceData() {
                    const response = await fetch('/api/performance/latest');
                    return await response.json();
                }
                
                async function fetchUsageStats() {
                    const response = await fetch('/api/usage/standards');
                    return await response.json();
                }
                
                async function fetchHealthStatus() {
                    const response = await fetch('/api/health/status');
                    return await response.json();
                }
                
                async function fetchGitActivity() {
                    const response = await fetch('/api/git/activity');
                    return await response.json();
                }
            """
            
            content = content.replace('</script>', api_injection + '</script>')
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(content.encode()))
            self.end_headers()
            self.wfile.write(content.encode())
            
        except FileNotFoundError:
            self.send_error(404, "Dashboard file not found")
        except Exception as e:
            self.send_error(500, f"Error serving dashboard: {str(e)}")
    
    def serve_latest_metrics(self):
        """Serve the latest collected metrics"""
        if not self.analytics_collector:
            self.send_json_response({"error": "Analytics collector not available"})
            return
        
        try:
            metrics = self.analytics_collector.collect_all_metrics()
            self.send_json_response(metrics)
        except Exception as e:
            self.send_json_response({"error": f"Failed to collect metrics: {str(e)}"})
    
    def serve_performance_data(self):
        """Serve performance monitoring data"""
        if not self.performance_monitor:
            self.send_json_response(self._get_mock_performance_data())
            return
        
        try:
            # Try to load latest performance report
            latest_file = os.path.join(self.performance_monitor.metrics_dir, 'latest_performance_report.json')
            if os.path.exists(latest_file):
                with open(latest_file, 'r') as f:
                    data = json.load(f)
                self.send_json_response(data)
            else:
                # Generate new performance report
                report = self.performance_monitor.generate_performance_report()
                self.send_json_response(report)
        except Exception as e:
            self.send_json_response({"error": f"Failed to get performance data: {str(e)}"})
    
    def serve_usage_stats(self):
        """Serve standards usage statistics"""
        try:
            if self.analytics_collector:
                standards_metrics = self.analytics_collector.collect_standards_usage_metrics()
                
                # Process for dashboard display
                usage_data = {
                    'standards': [],
                    'usage_counts': [],
                    'file_sizes': [],
                    'last_modified': []
                }
                
                for std_id, metrics in standards_metrics.items():
                    usage_data['standards'].append(std_id)
                    usage_data['usage_counts'].append(metrics.get('line_count', 0))
                    usage_data['file_sizes'].append(metrics.get('file_size', 0))
                    usage_data['last_modified'].append(metrics.get('last_modified', ''))
                
                self.send_json_response(usage_data)
            else:
                self.send_json_response(self._get_mock_usage_data())
                
        except Exception as e:
            self.send_json_response({"error": f"Failed to get usage stats: {str(e)}"})
    
    def serve_health_status(self):
        """Serve repository health status"""
        try:
            if self.analytics_collector:
                health_metrics = self.analytics_collector.collect_repository_health_metrics()
                
                # Calculate overall health score
                health_score = 100
                alerts = []
                
                # Check documentation coverage
                doc_coverage = health_metrics.get('documentation_coverage', 0)
                if doc_coverage < 80:
                    health_score -= 10
                    alerts.append({
                        'type': 'warning',
                        'message': f'Documentation coverage is {doc_coverage:.1f}% - consider improving'
                    })
                
                # Check link health
                link_health = health_metrics.get('link_health', {})
                if link_health.get('broken_links', 0) > 0:
                    health_score -= 5
                    alerts.append({
                        'type': 'warning',
                        'message': f'{link_health.get("broken_links", 0)} broken links detected'
                    })
                
                # Check compliance scores
                compliance = health_metrics.get('compliance_scores', {})
                if compliance.get('compliance_score', 100) < 90:
                    health_score -= 15
                    alerts.append({
                        'type': 'warning',
                        'message': f'Compliance score is {compliance.get("compliance_score", "unknown")}%'
                    })
                
                if health_score >= 90:
                    alerts.insert(0, {
                        'type': 'success',
                        'message': 'All systems operational - repository health excellent'
                    })
                
                health_data = {
                    'overall_health': max(health_score, 0),
                    'documentation_coverage': doc_coverage,
                    'link_health': link_health.get('health_score', 100),
                    'compliance_score': compliance.get('compliance_score', 100),
                    'alerts': alerts,
                    'last_updated': datetime.now().isoformat()
                }
                
                self.send_json_response(health_data)
            else:
                self.send_json_response(self._get_mock_health_data())
                
        except Exception as e:
            self.send_json_response({"error": f"Failed to get health status: {str(e)}"})
    
    def serve_git_activity(self):
        """Serve Git activity data"""
        try:
            if self.analytics_collector:
                git_metrics = self.analytics_collector.collect_git_metrics()
                
                # Format for dashboard
                activity_data = {
                    'commits_7_days': git_metrics.get('commits', {}).get('last_7_days', 0),
                    'commits_30_days': git_metrics.get('commits', {}).get('last_30_days', 0),
                    'contributors': git_metrics.get('contributors', {}),
                    'file_changes': git_metrics.get('file_changes', {}),
                    'branches': git_metrics.get('branches', {})
                }
                
                self.send_json_response(activity_data)
            else:
                self.send_json_response(self._get_mock_git_data())
                
        except Exception as e:
            self.send_json_response({"error": f"Failed to get git activity: {str(e)}"})
    
    def send_json_response(self, data):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2, default=str)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Length', len(json_data.encode()))
        self.end_headers()
        self.wfile.write(json_data.encode())
    
    def _get_mock_performance_data(self):
        """Return mock performance data when real collector is not available"""
        return {
            'health_score': {
                'overall': 87.5,
                'git_operations': 92.3,
                'file_operations': 88.7,
                'script_performance': 85.2,
                'cpu_efficiency': 76.5,
                'memory_efficiency': 82.1,
                'search_performance': 94.6
            },
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_mock_usage_data(self):
        """Return mock usage data"""
        return {
            'standards': ['Coding Standards', 'Security Standards', 'Testing Standards', 'DevOps Standards', 'Frontend Standards'],
            'usage_counts': [45, 38, 32, 28, 25],
            'file_sizes': [45000, 78000, 52000, 58000, 68000]
        }
    
    def _get_mock_health_data(self):
        """Return mock health data"""
        return {
            'overall_health': 87.5,
            'documentation_coverage': 94.2,
            'link_health': 98.1,
            'compliance_score': 92.3,
            'alerts': [
                {'type': 'success', 'message': 'All systems operational'},
                {'type': 'warning', 'message': 'Consider updating 2 standards files'}
            ],
            'last_updated': datetime.now().isoformat()
        }
    
    def _get_mock_git_data(self):
        """Return mock git activity data"""
        return {
            'commits_7_days': 12,
            'commits_30_days': 47,
            'contributors': {'Developer 1': 8, 'Developer 2': 4},
            'file_changes': {'docs/standards/CODING_STANDARDS.md': 3, 'README.md': 2},
            'branches': {'current': 'main', 'total_branches': 3}
        }

class DashboardServer:
    """Main dashboard server class"""
    
    def __init__(self, repo_path=None, port=8080, host='localhost'):
        self.repo_path = repo_path or os.getcwd()
        self.port = port
        self.host = host
        self.httpd = None
        self.monitoring_thread = None
        self.stop_monitoring = False
        
    def start(self):
        """Start the dashboard server"""
        # Change to the monitoring directory to serve static files
        monitoring_dir = os.path.join(self.repo_path, 'monitoring')
        os.chdir(monitoring_dir)
        
        # Create custom handler with repo path
        handler_class = lambda *args, **kwargs: DashboardHandler(*args, repo_path=self.repo_path, **kwargs)
        
        # Start HTTP server
        self.httpd = HTTPServer((self.host, self.port), handler_class)
        
        print(f"🚀 Dashboard server starting on http://{self.host}:{self.port}")
        print(f"📊 Dashboard available at: http://{self.host}:{self.port}/dashboard")
        print(f"🔗 API endpoints available at: http://{self.host}:{self.port}/api/")
        print("Press Ctrl+C to stop the server")
        
        # Start background monitoring
        self.start_background_monitoring()
        
        try:
            self.httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Stopping dashboard server...")
            self.stop()
    
    def stop(self):
        """Stop the dashboard server"""
        self.stop_monitoring = True
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=5)
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
        print("✅ Dashboard server stopped")
    
    def start_background_monitoring(self):
        """Start background monitoring thread"""
        if AnalyticsCollector and PerformanceMonitor:
            self.monitoring_thread = threading.Thread(target=self._background_monitoring)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
            print("📈 Background monitoring started")
    
    def _background_monitoring(self):
        """Background monitoring loop"""
        analytics = AnalyticsCollector(self.repo_path)
        performance = PerformanceMonitor(self.repo_path)
        
        while not self.stop_monitoring:
            try:
                # Collect metrics every 5 minutes
                analytics.collect_all_metrics()
                performance.generate_performance_report()
                
                print(f"📊 Metrics updated at {datetime.now().strftime('%H:%M:%S')}")
                
                # Wait 5 minutes
                for _ in range(300):  # 5 minutes = 300 seconds
                    if self.stop_monitoring:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                print(f"⚠️ Error in background monitoring: {e}")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Standards Repository Dashboard Server')
    parser.add_argument('--port', type=int, default=8080, help='Port to serve on (default: 8080)')
    parser.add_argument('--host', default='localhost', help='Host to bind to (default: localhost)')
    parser.add_argument('--repo-path', help='Path to repository (default: current directory)')
    
    args = parser.parse_args()
    
    server = DashboardServer(
        repo_path=args.repo_path,
        port=args.port,
        host=args.host
    )
    
    try:
        server.start()
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())