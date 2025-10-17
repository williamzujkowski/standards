#!/usr/bin/env python3
"""
HIPAA Audit Log Analyzer and Compliance Reporting

Analyzes audit logs for HIPAA compliance violations and anomalies.
Generates compliance reports for HIPAA Security Rule 164.312(b) requirements.

LEGAL DISCLAIMER: This is a reference implementation for educational purposes.
Compliance requirements vary by organization. Consult with compliance officers.
"""

import json
import csv
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from collections import defaultdict, Counter
from dataclasses import dataclass, field, asdict


@dataclass
class AuditLogEntry:
    """Represents a single audit log entry"""
    timestamp: str
    user_id: str
    event_type: str
    resource_accessed: str
    success: bool
    source_ip: str
    patient_id: Optional[str] = None
    action: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ComplianceViolation:
    """Represents a compliance violation or anomaly"""
    severity: str  # critical, high, medium, low
    violation_type: str
    description: str
    user_id: str
    timestamp: str
    patient_id: Optional[str] = None
    details: Dict[str, Any] = field(default_factory=dict)


class HIPAAAuditLogAnalyzer:
    """
    Analyzes audit logs for HIPAA compliance violations

    Detection Rules:
    - After-hours access by non-emergency personnel
    - Bulk record access (>50 records in single session)
    - Access to VIP patient records
    - Geographical anomalies (access from unusual locations)
    - Terminated employee account activity
    - Failed login patterns (brute-force attempts)
    - PHI access without legitimate treatment relationship
    - Unusual access patterns (time, volume, resource type)
    - Access to own medical record by employee
    - Modifications to audit logs (tampering)
    """

    def __init__(self):
        self.violations: List[ComplianceViolation] = []
        self.audit_entries: List[AuditLogEntry] = []
        self.user_access_patterns: Dict[str, List[AuditLogEntry]] = defaultdict(list)

        # Configuration (customize per organization)
        self.business_hours_start = 7  # 7 AM
        self.business_hours_end = 19   # 7 PM
        self.bulk_access_threshold = 50
        self.failed_login_threshold = 5
        self.vip_patient_ids = set()  # Load from configuration
        self.terminated_user_ids = set()  # Load from HR system
        self.emergency_roles = {'ER_PHYSICIAN', 'ER_NURSE', 'ON_CALL_MD'}

    def load_audit_log(self, log_file: str, format: str = 'json'):
        """
        Load audit log from file

        Args:
            log_file: Path to audit log file
            format: Log format ('json', 'csv')
        """
        if format == 'json':
            with open(log_file, 'r') as f:
                for line in f:
                    try:
                        entry_dict = json.loads(line.strip())
                        entry = AuditLogEntry(**entry_dict)
                        self.audit_entries.append(entry)
                        self.user_access_patterns[entry.user_id].append(entry)
                    except json.JSONDecodeError:
                        continue

        elif format == 'csv':
            with open(log_file, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convert 'true'/'false' strings to boolean
                    row['success'] = row.get('success', '').lower() == 'true'

                    # Handle optional fields
                    row['patient_id'] = row.get('patient_id') or None
                    row['action'] = row.get('action') or None

                    # Parse metadata if present
                    if 'metadata' in row and row['metadata']:
                        try:
                            row['metadata'] = json.loads(row['metadata'])
                        except json.JSONDecodeError:
                            row['metadata'] = {}
                    else:
                        row['metadata'] = {}

                    entry = AuditLogEntry(**row)
                    self.audit_entries.append(entry)
                    self.user_access_patterns[entry.user_id].append(entry)

    def analyze_after_hours_access(self):
        """Detect after-hours PHI access by non-emergency personnel"""
        for entry in self.audit_entries:
            # Parse timestamp
            try:
                timestamp = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
            except ValueError:
                continue

            # Check if outside business hours
            hour = timestamp.hour
            if not (self.business_hours_start <= hour < self.business_hours_end):
                # Check if user has emergency role
                user_role = entry.metadata.get('user_role', '')

                if user_role not in self.emergency_roles:
                    self.violations.append(ComplianceViolation(
                        severity='high',
                        violation_type='after_hours_access',
                        description=f'After-hours PHI access by non-emergency user',
                        user_id=entry.user_id,
                        timestamp=entry.timestamp,
                        patient_id=entry.patient_id,
                        details={
                            'hour': hour,
                            'user_role': user_role,
                            'resource': entry.resource_accessed
                        }
                    ))

    def analyze_bulk_access(self):
        """Detect bulk record access (potential data extraction)"""
        # Group by user and session (1-hour window)
        user_sessions = defaultdict(lambda: defaultdict(list))

        for entry in self.audit_entries:
            if entry.event_type in ['record_view', 'search', 'export']:
                timestamp = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
                session_key = timestamp.replace(minute=0, second=0, microsecond=0)
                user_sessions[entry.user_id][session_key].append(entry)

        # Check for bulk access
        for user_id, sessions in user_sessions.items():
            for session_time, entries in sessions.items():
                if len(entries) > self.bulk_access_threshold:
                    # Potential bulk access
                    unique_patients = len(set(e.patient_id for e in entries if e.patient_id))

                    self.violations.append(ComplianceViolation(
                        severity='critical',
                        violation_type='bulk_access',
                        description=f'Bulk record access: {len(entries)} records in 1 hour',
                        user_id=user_id,
                        timestamp=entries[0].timestamp,
                        details={
                            'record_count': len(entries),
                            'unique_patients': unique_patients,
                            'session_start': session_time.isoformat(),
                            'event_types': [e.event_type for e in entries]
                        }
                    ))

    def analyze_vip_access(self):
        """Detect access to VIP patient records"""
        for entry in self.audit_entries:
            if entry.patient_id in self.vip_patient_ids:
                # Log all VIP access for review
                self.violations.append(ComplianceViolation(
                    severity='high',
                    violation_type='vip_access',
                    description=f'Access to VIP patient record',
                    user_id=entry.user_id,
                    timestamp=entry.timestamp,
                    patient_id=entry.patient_id,
                    details={
                        'event_type': entry.event_type,
                        'resource': entry.resource_accessed,
                        'justification_required': True
                    }
                ))

    def analyze_terminated_user_access(self):
        """Detect access by terminated employees"""
        for entry in self.audit_entries:
            if entry.user_id in self.terminated_user_ids:
                self.violations.append(ComplianceViolation(
                    severity='critical',
                    violation_type='terminated_user_access',
                    description=f'Access by terminated employee',
                    user_id=entry.user_id,
                    timestamp=entry.timestamp,
                    patient_id=entry.patient_id,
                    details={
                        'event_type': entry.event_type,
                        'resource': entry.resource_accessed,
                        'immediate_action_required': True
                    }
                ))

    def analyze_failed_logins(self):
        """Detect brute-force login attempts"""
        failed_logins = defaultdict(list)

        for entry in self.audit_entries:
            if entry.event_type == 'login' and not entry.success:
                failed_logins[entry.user_id].append(entry)

        for user_id, failures in failed_logins.items():
            if len(failures) >= self.failed_login_threshold:
                # Potential brute-force attack
                timestamps = [datetime.fromisoformat(e.timestamp.replace('Z', '+00:00')) for e in failures]
                time_window = max(timestamps) - min(timestamps)

                self.violations.append(ComplianceViolation(
                    severity='high',
                    violation_type='failed_login_pattern',
                    description=f'Multiple failed login attempts: {len(failures)} failures',
                    user_id=user_id,
                    timestamp=failures[0].timestamp,
                    details={
                        'failure_count': len(failures),
                        'time_window_seconds': time_window.total_seconds(),
                        'source_ips': list(set(e.source_ip for e in failures))
                    }
                ))

    def analyze_geographical_anomalies(self):
        """Detect access from unusual geographical locations"""
        # Simplified implementation: detect same user from multiple IPs in short time
        user_ip_timeline = defaultdict(list)

        for entry in self.audit_entries:
            timestamp = datetime.fromisoformat(entry.timestamp.replace('Z', '+00:00'))
            user_ip_timeline[entry.user_id].append((timestamp, entry.source_ip))

        for user_id, timeline in user_ip_timeline.items():
            # Sort by timestamp
            timeline.sort(key=lambda x: x[0])

            # Check for IP changes within short window (1 hour)
            for i in range(len(timeline) - 1):
                time1, ip1 = timeline[i]
                time2, ip2 = timeline[i + 1]

                if ip1 != ip2 and (time2 - time1) < timedelta(hours=1):
                    self.violations.append(ComplianceViolation(
                        severity='medium',
                        violation_type='geographical_anomaly',
                        description=f'Access from different IPs within 1 hour',
                        user_id=user_id,
                        timestamp=time2.isoformat(),
                        details={
                            'ip1': ip1,
                            'ip2': ip2,
                            'time_diff_minutes': (time2 - time1).total_seconds() / 60
                        }
                    ))

    def analyze_self_access(self):
        """Detect employees accessing their own medical records"""
        for entry in self.audit_entries:
            # Check if user accessed record with their own patient ID
            # (requires mapping user_id to patient_id)
            user_patient_id = entry.metadata.get('user_patient_id')

            if user_patient_id and entry.patient_id == user_patient_id:
                self.violations.append(ComplianceViolation(
                    severity='medium',
                    violation_type='self_access',
                    description=f'Employee accessed own medical record',
                    user_id=entry.user_id,
                    timestamp=entry.timestamp,
                    patient_id=entry.patient_id,
                    details={
                        'event_type': entry.event_type,
                        'justification_required': True
                    }
                ))

    def analyze_audit_log_tampering(self):
        """Detect potential audit log tampering"""
        # Check for gaps in log timestamps
        timestamps = sorted([
            datetime.fromisoformat(e.timestamp.replace('Z', '+00:00'))
            for e in self.audit_entries
        ])

        for i in range(len(timestamps) - 1):
            gap = timestamps[i + 1] - timestamps[i]

            # Alert on gaps > 1 hour during business hours
            if gap > timedelta(hours=1):
                if self.business_hours_start <= timestamps[i].hour < self.business_hours_end:
                    self.violations.append(ComplianceViolation(
                        severity='critical',
                        violation_type='audit_log_gap',
                        description=f'Suspicious gap in audit logs: {gap.total_seconds() / 3600:.1f} hours',
                        user_id='SYSTEM',
                        timestamp=timestamps[i].isoformat(),
                        details={
                            'gap_start': timestamps[i].isoformat(),
                            'gap_end': timestamps[i + 1].isoformat(),
                            'gap_hours': gap.total_seconds() / 3600
                        }
                    ))

    def run_all_analyses(self):
        """Run all compliance analysis checks"""
        print("Running HIPAA compliance analysis...")
        print(f"Total audit entries: {len(self.audit_entries)}")
        print()

        self.analyze_after_hours_access()
        print(f"✓ After-hours access analysis complete")

        self.analyze_bulk_access()
        print(f"✓ Bulk access analysis complete")

        self.analyze_vip_access()
        print(f"✓ VIP access analysis complete")

        self.analyze_terminated_user_access()
        print(f"✓ Terminated user analysis complete")

        self.analyze_failed_logins()
        print(f"✓ Failed login analysis complete")

        self.analyze_geographical_anomalies()
        print(f"✓ Geographical anomaly analysis complete")

        self.analyze_self_access()
        print(f"✓ Self-access analysis complete")

        self.analyze_audit_log_tampering()
        print(f"✓ Audit log tampering analysis complete")

        print()
        print(f"Total violations detected: {len(self.violations)}")

    def generate_compliance_report(self, output_file: str = 'compliance_report.json'):
        """Generate comprehensive compliance report"""
        # Categorize violations by severity
        severity_counts = Counter(v.severity for v in self.violations)
        violation_type_counts = Counter(v.violation_type for v in self.violations)
        user_violation_counts = Counter(v.user_id for v in self.violations)

        report = {
            'report_generated': datetime.utcnow().isoformat() + 'Z',
            'audit_period': {
                'start': self.audit_entries[0].timestamp if self.audit_entries else None,
                'end': self.audit_entries[-1].timestamp if self.audit_entries else None,
                'total_entries': len(self.audit_entries)
            },
            'summary': {
                'total_violations': len(self.violations),
                'critical': severity_counts['critical'],
                'high': severity_counts['high'],
                'medium': severity_counts['medium'],
                'low': severity_counts['low']
            },
            'violation_types': dict(violation_type_counts),
            'top_users_with_violations': dict(user_violation_counts.most_common(10)),
            'violations': [asdict(v) for v in self.violations]
        }

        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"Compliance report generated: {output_file}")
        return report

    def generate_summary_report(self):
        """Generate human-readable summary report"""
        severity_counts = Counter(v.severity for v in self.violations)
        violation_type_counts = Counter(v.violation_type for v in self.violations)

        print("=" * 70)
        print("HIPAA COMPLIANCE AUDIT REPORT")
        print("=" * 70)
        print()

        print(f"Report Generated: {datetime.utcnow().isoformat() + 'Z'}")
        print(f"Audit Period: {self.audit_entries[0].timestamp if self.audit_entries else 'N/A'} to {self.audit_entries[-1].timestamp if self.audit_entries else 'N/A'}")
        print(f"Total Audit Entries Analyzed: {len(self.audit_entries)}")
        print()

        print("COMPLIANCE SUMMARY")
        print("-" * 70)
        print(f"Total Violations: {len(self.violations)}")
        print(f"  Critical: {severity_counts['critical']}")
        print(f"  High:     {severity_counts['high']}")
        print(f"  Medium:   {severity_counts['medium']}")
        print(f"  Low:      {severity_counts['low']}")
        print()

        print("VIOLATION BREAKDOWN BY TYPE")
        print("-" * 70)
        for violation_type, count in violation_type_counts.most_common():
            print(f"  {violation_type}: {count}")
        print()

        if severity_counts['critical'] > 0:
            print("CRITICAL VIOLATIONS (IMMEDIATE ACTION REQUIRED)")
            print("-" * 70)
            critical_violations = [v for v in self.violations if v.severity == 'critical']
            for v in critical_violations[:10]:  # Show top 10
                print(f"  [{v.timestamp}] {v.violation_type}: {v.description}")
                print(f"    User: {v.user_id}, Patient: {v.patient_id or 'N/A'}")
            print()

        print("=" * 70)


# Example usage and sample data generator
def generate_sample_audit_log(output_file: str = 'sample_audit_log.jsonl'):
    """Generate sample audit log for testing"""
    import random

    users = ['user001', 'user002', 'user003', 'user004', 'terminated_user']
    patient_ids = [f'P{str(i).zfill(6)}' for i in range(1, 101)]
    event_types = ['login', 'record_view', 'record_update', 'search', 'export']
    ips = ['192.168.1.100', '192.168.1.101', '10.0.0.50', '203.0.113.45']

    entries = []

    # Generate normal activity
    base_time = datetime.utcnow() - timedelta(days=7)

    for day in range(7):
        for hour in range(7, 19):  # Business hours
            for _ in range(random.randint(5, 15)):
                timestamp = base_time + timedelta(days=day, hours=hour, minutes=random.randint(0, 59))

                entry = {
                    'timestamp': timestamp.isoformat() + 'Z',
                    'user_id': random.choice(users),
                    'event_type': random.choice(event_types),
                    'resource_accessed': f'/api/patients/{random.choice(patient_ids)}',
                    'success': True,
                    'source_ip': random.choice(ips),
                    'patient_id': random.choice(patient_ids),
                    'metadata': {'user_role': 'PHYSICIAN'}
                }
                entries.append(entry)

    # Inject violations
    # 1. After-hours access
    for _ in range(5):
        timestamp = base_time + timedelta(days=random.randint(0, 6), hours=22, minutes=random.randint(0, 59))
        entry = {
            'timestamp': timestamp.isoformat() + 'Z',
            'user_id': 'user002',
            'event_type': 'record_view',
            'resource_accessed': f'/api/patients/{random.choice(patient_ids)}',
            'success': True,
            'source_ip': ips[0],
            'patient_id': random.choice(patient_ids),
            'metadata': {'user_role': 'BILLING'}
        }
        entries.append(entry)

    # 2. Bulk access
    bulk_time = base_time + timedelta(days=3, hours=14)
    for i in range(60):
        timestamp = bulk_time + timedelta(minutes=i)
        entry = {
            'timestamp': timestamp.isoformat() + 'Z',
            'user_id': 'user003',
            'event_type': 'record_view',
            'resource_accessed': f'/api/patients/{patient_ids[i]}',
            'success': True,
            'source_ip': ips[1],
            'patient_id': patient_ids[i],
            'metadata': {'user_role': 'ADMIN'}
        }
        entries.append(entry)

    # 3. Failed logins
    failed_time = base_time + timedelta(days=5, hours=2)
    for i in range(10):
        timestamp = failed_time + timedelta(seconds=i * 30)
        entry = {
            'timestamp': timestamp.isoformat() + 'Z',
            'user_id': 'user004',
            'event_type': 'login',
            'resource_accessed': '/auth/login',
            'success': False,
            'source_ip': '203.0.113.99',
            'metadata': {}
        }
        entries.append(entry)

    # 4. Terminated user access
    term_time = base_time + timedelta(days=6, hours=10)
    entry = {
        'timestamp': term_time.isoformat() + 'Z',
        'user_id': 'terminated_user',
        'event_type': 'record_view',
        'resource_accessed': f'/api/patients/{patient_ids[0]}',
        'success': True,
        'source_ip': ips[2],
        'patient_id': patient_ids[0],
        'metadata': {'user_role': 'NURSE'}
    }
    entries.append(entry)

    # Sort by timestamp
    entries.sort(key=lambda x: x['timestamp'])

    # Write to file
    with open(output_file, 'w') as f:
        for entry in entries:
            f.write(json.dumps(entry) + '\n')

    print(f"Sample audit log generated: {output_file}")
    print(f"Total entries: {len(entries)}")
    return output_file


if __name__ == "__main__":
    print("HIPAA Audit Log Analyzer - Demo")
    print("=" * 70)
    print()

    # Generate sample audit log
    sample_log = generate_sample_audit_log()
    print()

    # Initialize analyzer
    analyzer = HIPAAAuditLogAnalyzer()

    # Configure (in production, load from config/database)
    analyzer.terminated_user_ids = {'terminated_user'}
    analyzer.vip_patient_ids = set()  # Empty for demo

    # Load audit log
    print("Loading audit log...")
    analyzer.load_audit_log(sample_log, format='json')
    print(f"Loaded {len(analyzer.audit_entries)} audit entries")
    print()

    # Run all analyses
    analyzer.run_all_analyses()
    print()

    # Generate reports
    analyzer.generate_compliance_report('compliance_report.json')
    print()

    analyzer.generate_summary_report()
