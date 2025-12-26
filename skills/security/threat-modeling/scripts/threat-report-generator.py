#!/usr/bin/env python3
"""
Threat Modeling Report Generator

Generates comprehensive threat model reports from YAML threat definitions.
Supports STRIDE analysis, DREAD scoring, mitigation tracking, and NIST control mapping.

Usage:
    python threat-report-generator.py --input threats.yaml --output report.md
    python threat-report-generator.py --input threats.yaml --format html
    python threat-report-generator.py --input threats.yaml --summary-only
"""

import argparse
import sys
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

import yaml


class StrideCategory(Enum):
    """STRIDE threat categories."""

    SPOOFING = "Spoofing"
    TAMPERING = "Tampering"
    REPUDIATION = "Repudiation"
    INFORMATION_DISCLOSURE = "Information Disclosure"
    DENIAL_OF_SERVICE = "Denial of Service"
    ELEVATION_OF_PRIVILEGE = "Elevation of Privilege"


class Priority(Enum):
    """Threat priority levels based on DREAD score."""

    CRITICAL = "Critical"  # 8.0-10.0
    HIGH = "High"  # 6.0-7.9
    MEDIUM = "Medium"  # 4.0-5.9
    LOW = "Low"  # 0-3.9


@dataclass
class DreadScore:
    """DREAD scoring for threat prioritization."""

    damage: int  # 0-10
    reproducibility: int  # 0-10
    exploitability: int  # 0-10
    affected_users: int  # 0-10
    discoverability: int  # 0-10

    def calculate(self) -> float:
        """Calculate DREAD score."""
        return (
            self.damage + self.reproducibility + self.exploitability + self.affected_users + self.discoverability
        ) / 5

    def priority(self) -> Priority:
        """Determine priority from score."""
        score = self.calculate()
        if score >= 8.0:
            return Priority.CRITICAL
        if score >= 6.0:
            return Priority.HIGH
        if score >= 4.0:
            return Priority.MEDIUM
        return Priority.LOW


@dataclass
class Mitigation:
    """Threat mitigation control."""

    control: str
    nist_control: str
    status: str  # Planned, In Progress, Implemented, Not Applicable
    owner: str = ""
    target_date: str = ""


@dataclass
class Threat:
    """Threat definition."""

    id: str
    category: StrideCategory
    description: str
    attack_scenario: str
    component: str
    dread: DreadScore
    mitigations: list[Mitigation] = field(default_factory=list)
    impact_confidentiality: str = ""
    impact_integrity: str = ""
    impact_availability: str = ""


@dataclass
class ThreatModel:
    """Complete threat model."""

    system_name: str
    version: str
    date: str
    analyst: str
    threats: list[Threat] = field(default_factory=list)


class ThreatReportGenerator:
    """Generate threat modeling reports."""

    def __init__(self, threat_model: ThreatModel):
        self.model = threat_model

    def generate_markdown(self) -> str:
        """Generate Markdown report."""
        sections = [
            self._header(),
            self._executive_summary(),
            self._threat_breakdown(),
            self._critical_threats(),
            self._mitigation_summary(),
            self._nist_control_mapping(),
            self._recommendations(),
        ]
        return "\n\n".join(sections)

    def _header(self) -> str:
        """Generate report header."""
        return f"""# Threat Model Report: {self.model.system_name}

**Version:** {self.model.version}
**Date:** {self.model.date}
**Analyst:** {self.model.analyst}
**Report Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---
"""

    def _executive_summary(self) -> str:
        """Generate executive summary."""
        total = len(self.model.threats)
        critical = sum(1 for t in self.model.threats if t.dread.priority() == Priority.CRITICAL)
        high = sum(1 for t in self.model.threats if t.dread.priority() == Priority.HIGH)
        medium = sum(1 for t in self.model.threats if t.dread.priority() == Priority.MEDIUM)
        low = sum(1 for t in self.model.threats if t.dread.priority() == Priority.LOW)

        mitigated = sum(1 for t in self.model.threats if any(m.status == "Implemented" for m in t.mitigations))

        return f"""## Executive Summary

**Total Threats Identified:** {total}

**Priority Breakdown:**
- 🔴 Critical (DREAD ≥ 8.0): {critical}
- 🟠 High (DREAD 6.0-7.9): {high}
- 🟡 Medium (DREAD 4.0-5.9): {medium}
- 🟢 Low (DREAD < 4.0): {low}

**Mitigation Status:**
- Threats with Implemented Mitigations: {mitigated} ({mitigated / total * 100:.1f}%)
- Threats Requiring Action: {total - mitigated} ({(total - mitigated) / total * 100:.1f}%)

**Risk Summary:**
{"⚠️ CRITICAL: Immediate action required for critical threats" if critical > 0 else "✅ No critical threats identified"}
"""

    def _threat_breakdown(self) -> str:
        """Generate threat breakdown by STRIDE category."""
        stride_counts = {}
        for threat in self.model.threats:
            cat = threat.category.value
            stride_counts[cat] = stride_counts.get(cat, 0) + 1

        rows = []
        for category in StrideCategory:
            count = stride_counts.get(category.value, 0)
            rows.append(f"| {category.value} | {count} |")

        return f"""## Threat Breakdown by STRIDE Category

| Category | Count |
|----------|-------|
{chr(10).join(rows)}
"""

    def _critical_threats(self) -> str:
        """Generate detailed section for critical and high threats."""
        critical_threats = [t for t in self.model.threats if t.dread.priority() in [Priority.CRITICAL, Priority.HIGH]]

        if not critical_threats:
            return "## Critical & High Priority Threats\n\n✅ No critical or high priority threats identified."

        sections = ["## Critical & High Priority Threats\n"]

        for threat in sorted(critical_threats, key=lambda t: t.dread.calculate(), reverse=True):
            priority = threat.dread.priority().value
            score = threat.dread.calculate()

            mitigation_rows = []
            for m in threat.mitigations:
                mitigation_rows.append(f"| {m.control} | {m.nist_control} | {m.status} | {m.owner} |")

            sections.append(
                f"""### {threat.id}: {threat.description}

**Priority:** {priority} (DREAD: {score:.1f})
**Category:** {threat.category.value}
**Affected Component:** {threat.component}

**Attack Scenario:**
{threat.attack_scenario}

**Impact:**
- Confidentiality: {threat.impact_confidentiality or "N/A"}
- Integrity: {threat.impact_integrity or "N/A"}
- Availability: {threat.impact_availability or "N/A"}

**DREAD Breakdown:**
- Damage Potential: {threat.dread.damage}/10
- Reproducibility: {threat.dread.reproducibility}/10
- Exploitability: {threat.dread.exploitability}/10
- Affected Users: {threat.dread.affected_users}/10
- Discoverability: {threat.dread.discoverability}/10

**Mitigations:**

| Control | NIST Control | Status | Owner |
|---------|--------------|--------|-------|
{chr(10).join(mitigation_rows) if mitigation_rows else "| No mitigations defined | - | - | - |"}

---
"""
            )

        return "\n".join(sections)

    def _mitigation_summary(self) -> str:
        """Generate mitigation status summary."""
        all_mitigations = [m for t in self.model.threats for m in t.mitigations]

        if not all_mitigations:
            return "## Mitigation Summary\n\nNo mitigations defined."

        implemented = sum(1 for m in all_mitigations if m.status == "Implemented")
        in_progress = sum(1 for m in all_mitigations if m.status == "In Progress")
        planned = sum(1 for m in all_mitigations if m.status == "Planned")

        return f"""## Mitigation Summary

**Total Mitigations:** {len(all_mitigations)}

**Status Breakdown:**
- ✅ Implemented: {implemented} ({implemented / len(all_mitigations) * 100:.1f}%)
- 🔄 In Progress: {in_progress} ({in_progress / len(all_mitigations) * 100:.1f}%)
- 📋 Planned: {planned} ({planned / len(all_mitigations) * 100:.1f}%)
"""

    def _nist_control_mapping(self) -> str:
        """Generate NIST control mapping."""
        nist_controls = {}
        for threat in self.model.threats:
            for mitigation in threat.mitigations:
                control = mitigation.nist_control
                if control not in nist_controls:
                    nist_controls[control] = []
                nist_controls[control].append((threat.id, mitigation.status))

        rows = []
        for control in sorted(nist_controls.keys()):
            threat_ids = ", ".join(t[0] for t in nist_controls[control])
            statuses = set(t[1] for t in nist_controls[control])
            status_summary = ", ".join(statuses)
            rows.append(f"| {control} | {threat_ids} | {status_summary} |")

        return f"""## NIST Control Mapping

| NIST Control | Threat IDs | Status |
|--------------|------------|--------|
{chr(10).join(rows) if rows else "| No NIST controls mapped | - | - |"}
"""

    def _recommendations(self) -> str:
        """Generate recommendations section."""
        critical_count = sum(1 for t in self.model.threats if t.dread.priority() == Priority.CRITICAL)
        high_count = sum(1 for t in self.model.threats if t.dread.priority() == Priority.HIGH)

        unmitigated = [t for t in self.model.threats if not any(m.status == "Implemented" for m in t.mitigations)]

        recommendations = ["## Recommendations\n"]

        if critical_count > 0:
            recommendations.append(
                f"### 🔴 IMMEDIATE ACTION REQUIRED\n\n"
                f"{critical_count} critical threat(s) identified. "
                f"Address these within 7 days:\n"
            )
            for threat in [t for t in self.model.threats if t.dread.priority() == Priority.CRITICAL]:
                recommendations.append(f"- {threat.id}: {threat.description}")

        if high_count > 0:
            recommendations.append(
                f"\n### 🟠 HIGH PRIORITY\n\n{high_count} high priority threat(s). Address within 30 days.\n"
            )

        if unmitigated:
            recommendations.append(
                f"\n### 📋 UNMITIGATED THREATS\n\n"
                f"{len(unmitigated)} threat(s) have no implemented mitigations. "
                f"Prioritize mitigation implementation.\n"
            )

        recommendations.append(
            "\n### 🔄 CONTINUOUS IMPROVEMENT\n\n"
            "- Schedule quarterly threat model reviews\n"
            "- Update threat model when architecture changes\n"
            "- Conduct penetration testing to validate mitigations\n"
            "- Track mitigation effectiveness metrics\n"
        )

        return "\n".join(recommendations)


def load_threat_model(yaml_file: str) -> ThreatModel:
    """Load threat model from YAML file."""
    with open(yaml_file) as f:
        data = yaml.safe_load(f)

    threats = []
    for threat_data in data.get("threats", []):
        dread_data = threat_data["dread"]
        dread = DreadScore(
            damage=dread_data["damage"],
            reproducibility=dread_data["reproducibility"],
            exploitability=dread_data["exploitability"],
            affected_users=dread_data["affected_users"],
            discoverability=dread_data["discoverability"],
        )

        mitigations = [
            Mitigation(
                control=m["control"],
                nist_control=m["nist_control"],
                status=m["status"],
                owner=m.get("owner", ""),
                target_date=m.get("target_date", ""),
            )
            for m in threat_data.get("mitigations", [])
        ]

        threat = Threat(
            id=threat_data["id"],
            category=StrideCategory[threat_data["category"].upper().replace(" ", "_")],
            description=threat_data["description"],
            attack_scenario=threat_data["attack_scenario"],
            component=threat_data["component"],
            dread=dread,
            mitigations=mitigations,
            impact_confidentiality=threat_data.get("impact_confidentiality", ""),
            impact_integrity=threat_data.get("impact_integrity", ""),
            impact_availability=threat_data.get("impact_availability", ""),
        )
        threats.append(threat)

    return ThreatModel(
        system_name=data["system_name"],
        version=data["version"],
        date=data["date"],
        analyst=data["analyst"],
        threats=threats,
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate threat modeling reports from YAML definitions")
    parser.add_argument("--input", "-i", required=True, help="Input YAML file with threat definitions")
    parser.add_argument("--output", "-o", help="Output file (default: stdout)")
    parser.add_argument(
        "--format", "-f", choices=["markdown", "md"], default="markdown", help="Output format (default: markdown)"
    )
    parser.add_argument(
        "--summary-only", action="store_true", help="Generate summary only (no detailed threat listings)"
    )

    args = parser.parse_args()

    try:
        # Load threat model
        model = load_threat_model(args.input)

        # Generate report
        generator = ThreatReportGenerator(model)
        report = generator.generate_markdown()

        # Output
        if args.output:
            with open(args.output, "w") as f:
                f.write(report)
            print(f"✅ Report generated: {args.output}")
        else:
            print(report)

    except FileNotFoundError:
        print(f"❌ Error: File not found: {args.input}", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
