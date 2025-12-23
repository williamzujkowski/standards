#!/usr/bin/env python3
"""
Fix Documentation Accuracy Script

Purpose: Scan documentation for exaggerations and replace with evidence-based claims.
Features:
  - Pattern detection for vague/exaggerated language
  - Evidence-based replacement suggestions
  - Dry-run mode for preview
  - Link validation after updates
  - Automated claim verification

Usage:
  python3 fix-documentation-accuracy.py --dry-run
  python3 fix-documentation-accuracy.py --fix --verbose
  python3 fix-documentation-accuracy.py --target CLAUDE.md --check-links
"""

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configuration
REPO_ROOT = Path(__file__).parent.parent
REPORTS_DIR = REPO_ROOT / "reports" / "generated"
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE = REPORTS_DIR / f"accuracy-fixes-{TIMESTAMP}.log"

# Prohibited language patterns (regex, description, replacement strategy)
PROHIBITED_PATTERNS = [
    # Vague quantifiers
    (r"\b(significantly|dramatically|vastly|substantially)\s+(\w+)", "Vague quantifier", "Use specific metrics"),
    (
        r"\b(numerous|many|several|various)\s+(agents?|tools?|features?)",
        "Vague count",
        "Specify exact count with verification",
    ),
    (r"\b(best|optimal|perfect|ideal)\s+", "Unverifiable superlative", "Use qualified statements"),
    # Marketing language
    (
        r"\b(game-changer|revolutionary|cutting-edge|state-of-the-art)\b",
        "Marketing hyperbole",
        "Use factual descriptions",
    ),
    (r"\b(seamless|effortless|automatic)\b", "Oversimplification", "Describe actual mechanism"),
    (r"\b(unlimited|infinite|endless)\b", "Impossible claim", "State actual limits"),
    # Unqualified claims
    (r"\b(always|never|all|none)\s+(works?|succeeds?|fails?)", "Absolute claim", "Add qualifying context"),
    (r"\b(guaranteed|ensures?|promises?)\b", "Unverifiable guarantee", "Use 'aims to' or 'designed to'"),
    # Temporal vagueness
    (r"\b(recently|soon|upcoming|planned)\b", "Temporal vagueness", "Use specific dates/versions"),
    (r"\b(latest|newest|modern)\b", "Relative temporal claim", "Specify version or date"),
]

# Required evidence patterns (claim type, required evidence)
EVIDENCE_REQUIREMENTS = {
    "performance_claim": ["measurement method", "test conditions", "actual metrics"],
    "count_claim": ["verification command", "file path", "timestamp"],
    "feature_claim": ["implementation file", "test coverage", "documentation"],
    "compliance_claim": ["validation script", "audit report", "timestamp"],
}


@dataclass
class DocumentIssue:
    """Represents an accuracy issue found in documentation."""

    file_path: Path
    line_number: int
    issue_type: str
    original_text: str
    suggested_fix: Optional[str] = None
    evidence_required: List[str] = field(default_factory=list)
    severity: str = "warning"  # error, warning, info


@dataclass
class FixResult:
    """Result of applying a fix."""

    file_path: Path
    original_text: str
    fixed_text: str
    success: bool
    message: str = ""


class DocumentationAccuracyFixer:
    """Fixes documentation accuracy issues."""

    def __init__(self, dry_run: bool = True, verbose: bool = False):
        self.dry_run = dry_run
        self.verbose = verbose
        self.issues: List[DocumentIssue] = []
        self.fixes: List[FixResult] = []

        # Ensure reports directory exists
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Initialize logging
        self.log_file = open(LOG_FILE, "w", encoding="utf-8")
        self._log(f"Documentation Accuracy Fixer - {datetime.now()}")
        self._log(f"Mode: {'DRY RUN' if dry_run else 'FIX'}")
        self._log("-" * 80)

    def _log(self, message: str) -> None:
        """Write to log file and optionally print."""
        self.log_file.write(f"{message}\n")
        if self.verbose:
            print(message)

    def scan_file(self, file_path: Path) -> List[DocumentIssue]:
        """Scan a file for accuracy issues."""
        issues = []

        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            for line_num, line in enumerate(lines, start=1):
                # Check prohibited patterns
                for pattern, issue_desc, fix_strategy in PROHIBITED_PATTERNS:
                    if re.search(pattern, line, re.IGNORECASE):
                        issues.append(
                            DocumentIssue(
                                file_path=file_path,
                                line_number=line_num,
                                issue_type=issue_desc,
                                original_text=line.strip(),
                                suggested_fix=fix_strategy,
                                severity="warning",
                            )
                        )

                # Check for claims without evidence
                issues.extend(self._check_evidence_requirements(file_path, line_num, line))

        except Exception as e:
            self._log(f"Error scanning {file_path}: {e}")

        return issues

    def _check_evidence_requirements(self, file_path: Path, line_num: int, line: str) -> List[DocumentIssue]:
        """Check if claims have required evidence."""
        issues = []

        # Performance claims
        perf_pattern = r"(\d+)([%x])\s+(faster|slower|reduction|improvement|increase)"
        if re.search(perf_pattern, line, re.IGNORECASE):
            # Check if evidence is nearby (within 3 lines)
            if not self._has_nearby_evidence(file_path, line_num, ["test", "benchmark", "measurement", "verified"]):
                issues.append(
                    DocumentIssue(
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="Performance claim without evidence",
                        original_text=line.strip(),
                        evidence_required=EVIDENCE_REQUIREMENTS["performance_claim"],
                        severity="error",
                    )
                )

        # Count claims (e.g., "48 agents available")
        count_pattern = r"(\d+)\s+(agents?|tools?|skills?|files?)\s+(available|exist|present)"
        if re.search(count_pattern, line, re.IGNORECASE):
            if not self._has_nearby_evidence(file_path, line_num, ["verified", "see", "check", "run", "find"]):
                issues.append(
                    DocumentIssue(
                        file_path=file_path,
                        line_number=line_num,
                        issue_type="Count claim without verification",
                        original_text=line.strip(),
                        evidence_required=EVIDENCE_REQUIREMENTS["count_claim"],
                        severity="error",
                    )
                )

        return issues

    def _has_nearby_evidence(self, file_path: Path, line_num: int, keywords: List[str], window: int = 3) -> bool:
        """Check if evidence keywords appear near a claim."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")

            start = max(0, line_num - window - 1)
            end = min(len(lines), line_num + window)

            nearby_text = " ".join(lines[start:end]).lower()

            return any(keyword.lower() in nearby_text for keyword in keywords)

        except Exception:
            return False

    def suggest_fix(self, issue: DocumentIssue) -> Optional[str]:
        """Generate a suggested fix for an issue."""
        original = issue.original_text

        # Handle prohibited patterns
        for pattern, desc, fix_strategy in PROHIBITED_PATTERNS:
            if re.search(pattern, original, re.IGNORECASE):
                # Generate context-aware suggestions
                if "significantly" in original.lower():
                    return re.sub(r"\bsignificantly\b", "[SPECIFY METRIC]", original, flags=re.IGNORECASE)
                elif "numerous" in original.lower():
                    return re.sub(r"\bnumerous\b", "[EXACT COUNT]", original, flags=re.IGNORECASE)
                elif "best" in original.lower():
                    return re.sub(r"\bbest\b", "recommended", original, flags=re.IGNORECASE)

        return None

    def apply_safe_fixes(self, file_path: Path) -> List[FixResult]:
        """Apply safe automated fixes to a file."""
        results = []

        try:
            content = file_path.read_text(encoding="utf-8")
            original_content = content

            # Safe replacements (conservative)
            safe_replacements = [
                (r"\b(game-changer|revolutionary)\b", "innovative", re.IGNORECASE),
                (r"\bcutting-edge\b", "modern", re.IGNORECASE),
                (r"\bseamless(?:ly)?\b", "integrated", re.IGNORECASE),
                (r"\beffortless(?:ly)?\b", "streamlined", re.IGNORECASE),
                (r"\bguaranteed?\b", "designed to", re.IGNORECASE),
                (r"\b(always|never)\s+(works?|fails?)", r"typically \2", re.IGNORECASE),
            ]

            for pattern, replacement, flags in safe_replacements:
                if re.search(pattern, content, flags):
                    new_content = re.sub(pattern, replacement, content, flags=flags)
                    if new_content != content:
                        results.append(
                            FixResult(
                                file_path=file_path,
                                original_text=pattern,
                                fixed_text=replacement,
                                success=True,
                                message=f"Replaced marketing language: {pattern} -> {replacement}",
                            )
                        )
                        content = new_content

            # Write changes if not dry run
            if content != original_content:
                if not self.dry_run:
                    file_path.write_text(content, encoding="utf-8")
                    self._log(f"Fixed: {file_path}")
                else:
                    self._log(f"Would fix: {file_path}")

        except Exception as e:
            results.append(
                FixResult(
                    file_path=file_path,
                    original_text="",
                    fixed_text="",
                    success=False,
                    message=f"Error applying fixes: {e}",
                )
            )

        return results

    def validate_links_after_fix(self, file_path: Path) -> bool:
        """Validate that links still work after fixes."""
        self._log(f"Validating links in {file_path}...")

        try:
            # Run link checker
            subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts" / "generate-audit-reports.py")],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=60,
            )

            # Check for broken links
            audit_file = REPORTS_DIR / "structure-audit.json"
            if audit_file.exists():
                with open(audit_file) as f:
                    audit_data = json.load(f)
                    broken_links = audit_data.get("broken_links", 0)

                    if broken_links == 0:
                        self._log("✅ No broken links found")
                        return True
                    else:
                        self._log(f"⚠️  Found {broken_links} broken links")
                        return False

        except Exception as e:
            self._log(f"Error validating links: {e}")
            return False

        return True

    def scan_all_docs(self, target_files: Optional[List[Path]] = None) -> None:
        """Scan all documentation files for accuracy issues."""
        if target_files:
            files_to_scan = target_files
        else:
            # Scan key documentation files
            files_to_scan = [
                REPO_ROOT / "CLAUDE.md",
                REPO_ROOT / "README.md",
                REPO_ROOT / "docs" / "guides" / "KICKSTART_PROMPT.md",
            ]

            # Add all files in docs/
            if (REPO_ROOT / "docs").exists():
                files_to_scan.extend((REPO_ROOT / "docs").rglob("*.md"))

        self._log(f"\nScanning {len(files_to_scan)} files for accuracy issues...")

        for file_path in files_to_scan:
            if not file_path.exists():
                continue

            self._log(f"\nScanning: {file_path.relative_to(REPO_ROOT)}")
            issues = self.scan_file(file_path)

            if issues:
                self._log(f"  Found {len(issues)} issues")
                for issue in issues:
                    self._log(f"    Line {issue.line_number}: {issue.issue_type}")
                    self._log(f"      {issue.original_text}")
                    if issue.suggested_fix:
                        self._log(f"      Fix: {issue.suggested_fix}")

            self.issues.extend(issues)

    def generate_report(self) -> str:
        """Generate accuracy report."""
        report_lines = [
            "# Documentation Accuracy Report",
            f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Mode: {'DRY RUN' if self.dry_run else 'FIX'}",
            "\n## Summary\n",
            f"- Total issues found: {len(self.issues)}",
            f"- Errors: {len([i for i in self.issues if i.severity == 'error'])}",
            f"- Warnings: {len([i for i in self.issues if i.severity == 'warning'])}",
            f"- Fixes applied: {len(self.fixes)}",
        ]

        # Group by file
        issues_by_file: Dict[Path, List[DocumentIssue]] = {}
        for issue in self.issues:
            issues_by_file.setdefault(issue.file_path, []).append(issue)

        report_lines.append("\n## Issues by File\n")
        for file_path, file_issues in sorted(issues_by_file.items()):
            report_lines.append(f"\n### {file_path.relative_to(REPO_ROOT)}\n")
            for issue in file_issues:
                report_lines.append(f"- **Line {issue.line_number}**: {issue.issue_type}")
                report_lines.append(f"  - Original: `{issue.original_text[:100]}`")
                if issue.suggested_fix:
                    report_lines.append(f"  - Suggestion: {issue.suggested_fix}")
                if issue.evidence_required:
                    report_lines.append(f"  - Evidence needed: {', '.join(issue.evidence_required)}")

        if self.fixes:
            report_lines.append("\n## Fixes Applied\n")
            for fix in self.fixes:
                report_lines.append(f"- {fix.file_path.relative_to(REPO_ROOT)}: {fix.message}")

        return "\n".join(report_lines)

    def close(self) -> None:
        """Close resources."""
        self.log_file.close()


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Fix documentation accuracy issues",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (preview only)
  python3 fix-documentation-accuracy.py --dry-run

  # Fix issues
  python3 fix-documentation-accuracy.py --fix

  # Fix specific file
  python3 fix-documentation-accuracy.py --fix --target CLAUDE.md

  # Fix and validate links
  python3 fix-documentation-accuracy.py --fix --check-links --verbose
        """,
    )

    parser.add_argument("--dry-run", action="store_true", help="Preview changes without applying")
    parser.add_argument("--fix", action="store_true", help="Apply safe automated fixes")
    parser.add_argument("--target", type=Path, help="Target specific file")
    parser.add_argument("--check-links", action="store_true", help="Validate links after fixes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Determine mode
    if not args.fix and not args.dry_run:
        args.dry_run = True  # Default to dry run

    # Initialize fixer
    fixer = DocumentationAccuracyFixer(dry_run=args.dry_run, verbose=args.verbose)

    try:
        # Scan documentation
        target_files = [REPO_ROOT / args.target] if args.target else None
        fixer.scan_all_docs(target_files)

        # Apply fixes if requested
        if args.fix and not args.dry_run:
            print("\nApplying fixes...")
            for file_path in set(issue.file_path for issue in fixer.issues):
                results = fixer.apply_safe_fixes(file_path)
                fixer.fixes.extend(results)

            # Validate links if requested
            if args.check_links:
                print("\nValidating links...")
                for file_path in set(fix.file_path for fix in fixer.fixes if fix.success):
                    fixer.validate_links_after_fix(file_path)

        # Generate report
        report = fixer.generate_report()
        report_file = REPORTS_DIR / f"accuracy-report-{TIMESTAMP}.md"
        report_file.write_text(report + "\n", encoding="utf-8")

        print("\n" + "=" * 80)
        print("DOCUMENTATION ACCURACY REPORT")
        print("=" * 80)
        print(f"\nTotal issues: {len(fixer.issues)}")
        print(f"Errors: {len([i for i in fixer.issues if i.severity == 'error'])}")
        print(f"Warnings: {len([i for i in fixer.issues if i.severity == 'warning'])}")

        if args.fix and not args.dry_run:
            print(f"\nFixes applied: {len(fixer.fixes)}")
            print(f"Successful: {len([f for f in fixer.fixes if f.success])}")
            print(f"Failed: {len([f for f in fixer.fixes if not f.success])}")

        print(f"\nReport saved: {report_file}")
        print(f"Log saved: {LOG_FILE}")

        # Exit code based on severity
        has_errors = any(i.severity == "error" for i in fixer.issues)
        sys.exit(1 if has_errors else 0)

    finally:
        fixer.close()


if __name__ == "__main__":
    main()
