#!/usr/bin/env python3
"""
Standards Repository Linter
Comprehensive linting for markdown standards based on KNOWLEDGE_MANAGEMENT_STANDARDS.md
"""

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass
class LintIssue:
    """Represents a linting issue"""

    file: str
    line: int
    column: int
    rule: str
    severity: str  # error, warning, info
    message: str
    fix_suggestion: str | None = None


class StandardsLinter:
    """Comprehensive linter for standards documents"""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.issues: list[LintIssue] = []
        self.manifest = self._load_manifest()
        self.standards_files = list(self.root.glob("*_STANDARDS.md"))
        self.standards_files.extend(self.root.glob("UNIFIED_STANDARDS.md"))

    def _load_manifest(self) -> dict:
        """Load MANIFEST.yaml"""
        manifest_path = self.root / "MANIFEST.yaml"
        if manifest_path.exists():
            with open(manifest_path) as f:
                return yaml.safe_load(f)
        return {}

    def lint_all(self) -> list[LintIssue]:
        """Run all linting rules"""
        for std_file in self.standards_files:
            self._lint_file(std_file)

        # Also check cross-file rules
        self._check_manifest_completeness()
        self._check_index_coverage()
        self._check_graph_relationships()

        return self.issues

    def _lint_file(self, file_path: Path):
        """Lint a single file"""
        with open(file_path) as f:
            content = f.read()
            lines = content.split("\n")

        # Run all file-level checks
        self._check_metadata(file_path, lines)
        self._check_structure(file_path, content, lines)
        self._check_cross_references(file_path, content, lines)
        self._check_requirement_tags(file_path, content, lines)
        self._check_token_efficiency(file_path, content)
        self._check_formatting(file_path, lines)
        self._check_code_examples(file_path, content, lines)

    def _check_metadata(self, file_path: Path, lines: list[str]):
        """Check for required metadata headers"""
        "\n".join(lines[:20])

        # Version check with semantic versioning pattern
        version_pattern = r"^\*\*Version:\*\*\s+\d+\.\d+\.\d+\s*$"
        if not any(re.match(version_pattern, line) for line in lines[:20]):
            self._add_issue(
                file_path,
                1,
                1,
                "metadata-version",
                "error",
                "Missing or invalid version metadata",
                "Add: **Version:** X.Y.Z",
            )

        # Last Updated check
        date_pattern = r"^\*\*Last Updated:\*\*\s+\d{4}-\d{2}-\d{2}\s*$"
        if not any(re.match(date_pattern, line) for line in lines[:20]):
            self._add_issue(
                file_path,
                1,
                1,
                "metadata-date",
                "error",
                "Missing or invalid Last Updated metadata",
                "Add: **Last Updated:** YYYY-MM-DD",
            )

        # Status check
        status_pattern = r"^\*\*Status:\*\*\s+(Draft|Active|Deprecated)\s*$"
        if not any(re.match(status_pattern, line) for line in lines[:20]):
            self._add_issue(
                file_path,
                1,
                1,
                "metadata-status",
                "error",
                "Missing or invalid Status metadata",
                "Add: **Status:** Active/Draft/Deprecated",
            )

        # Standard Code check (for non-UNIFIED files)
        if file_path.name != "UNIFIED_STANDARDS.md":
            code_pattern = r"^\*\*Standard Code:\*\*\s+[A-Z]{2,4}\s*$"
            if not any(re.match(code_pattern, line) for line in lines[:20]):
                self._add_issue(
                    file_path,
                    1,
                    1,
                    "metadata-code",
                    "warning",
                    "Missing Standard Code metadata",
                    "Add: **Standard Code:** XX (2-4 letters)",
                )

    def _check_structure(self, file_path: Path, content: str, lines: list[str]):
        """Check document structure requirements"""
        # Table of Contents
        if "Table of Contents" not in content and "## Contents" not in content:
            self._add_issue(
                file_path,
                1,
                1,
                "structure-toc",
                "warning",
                "Missing Table of Contents",
                "Add a Table of Contents section",
            )

        # Required sections
        required_sections = ["Overview", "Implementation"]
        for section in required_sections:
            pattern = rf"^#{1, 3}\s+{section}"
            if not re.search(pattern, content, re.MULTILINE):
                self._add_issue(
                    file_path,
                    1,
                    1,
                    f"structure-{section.lower()}",
                    "error",
                    f"Missing required section: {section}",
                    f"Add ## {section} section",
                )

        # Implementation Checklist
        if "Implementation Checklist" not in content and "checklist" not in content.lower():
            self._add_issue(
                file_path,
                1,
                1,
                "structure-checklist",
                "warning",
                "Missing Implementation Checklist",
                "Add an Implementation Checklist section",
            )

    def _check_requirement_tags(self, file_path: Path, content: str, lines: list[str]):
        """Check for [REQUIRED] and [RECOMMENDED] tags"""
        if "[REQUIRED]" not in content and "[RECOMMENDED]" not in content:
            self._add_issue(
                file_path,
                1,
                1,
                "tags-missing",
                "warning",
                "No [REQUIRED] or [RECOMMENDED] tags found",
                "Add requirement level tags to important sections",
            )

        # Check tag formatting
        tag_pattern = r"\[(REQUIRED|RECOMMENDED|OPTIONAL)\]"
        for i, line in enumerate(lines):
            if re.search(tag_pattern, line):
                # Tags should be in headers or at start of line
                if not (line.strip().startswith("#") or line.strip().startswith("[")):
                    self._add_issue(
                        file_path,
                        i + 1,
                        1,
                        "tags-placement",
                        "warning",
                        "Requirement tag should be in header or at start of line",
                        "Move tag to header: ### [REQUIRED] Section Name",
                    )

    def _check_cross_references(self, file_path: Path, content: str, lines: list[str]):
        """Check cross-reference validity and format"""
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"

        for i, line in enumerate(lines):
            for match in re.finditer(link_pattern, line):
                link_text = match.group(1)
                link_target = match.group(2)

                # Check relative links
                if link_target.startswith("./"):
                    target_path = (file_path.parent / link_target.split("#")[0]).resolve()
                    if not target_path.exists():
                        self._add_issue(
                            file_path,
                            i + 1,
                            match.start(),
                            "xref-broken",
                            "error",
                            f"Broken link: {link_target}",
                            "Fix the link path or remove",
                        )

                # Check link text quality
                if link_text.lower() in ["here", "click here", "this"]:
                    self._add_issue(
                        file_path,
                        i + 1,
                        match.start(),
                        "xref-text",
                        "warning",
                        f"Non-descriptive link text: '{link_text}'",
                        "Use descriptive link text",
                    )

    def _check_token_efficiency(self, file_path: Path, content: str):
        """Check for token efficiency issues"""
        # Estimate tokens (rough approximation)
        word_count = len(content.split())
        estimated_tokens = int(word_count * 0.75)

        if estimated_tokens > 15000:
            self._add_issue(
                file_path,
                1,
                1,
                "tokens-total",
                "warning",
                f"Document has ~{estimated_tokens} tokens (high)",
                "Consider splitting into multiple documents",
            )

        # Check section sizes
        sections = re.split(r"^##\s+", content, flags=re.MULTILINE)
        for _i, section in enumerate(sections[1:], 1):  # Skip first split
            section_words = len(section.split())
            section_tokens = int(section_words * 0.75)

            if section_tokens > 3000:
                # Find section name
                section_name = section.split("\n")[0].strip()
                self._add_issue(
                    file_path,
                    1,
                    1,
                    "tokens-section",
                    "info",
                    f"Section '{section_name}' has ~{section_tokens} tokens",
                    "Consider using progressive disclosure or splitting",
                )

    def _check_formatting(self, file_path: Path, lines: list[str]):
        """Check formatting issues"""
        for i, line in enumerate(lines):
            # Trailing whitespace
            if line.endswith(" ") or line.endswith("\t"):
                self._add_issue(
                    file_path,
                    i + 1,
                    len(line),
                    "format-trailing",
                    "error",
                    "Trailing whitespace",
                    "Remove trailing spaces",
                )

            # Line length (except URLs and code blocks)
            if len(line) > 120 and not line.strip().startswith("http") and not line.strip().startswith("```"):
                self._add_issue(
                    file_path,
                    i + 1,
                    121,
                    "format-line-length",
                    "warning",
                    f"Line too long ({len(line)} > 120)",
                    "Break line at appropriate point",
                )

            # Multiple blank lines
            if i > 0 and line == "" and lines[i - 1] == "":
                if i > 1 and lines[i - 2] == "":
                    self._add_issue(
                        file_path,
                        i + 1,
                        1,
                        "format-blank-lines",
                        "warning",
                        "Multiple consecutive blank lines",
                        "Use at most 2 consecutive blank lines",
                    )

    def _check_code_examples(self, file_path: Path, content: str, lines: list[str]):
        """Check code example quality"""
        code_blocks = re.findall(r"```(\w*)\n(.*?)\n```", content, re.DOTALL)

        if not code_blocks and "Implementation" in content:
            self._add_issue(
                file_path,
                1,
                1,
                "examples-missing",
                "warning",
                "No code examples found",
                "Add practical code examples",
            )

        for lang, code in code_blocks:
            if not lang:
                # Find line number
                for i, line in enumerate(lines):
                    if line == "```" and i + 1 < len(lines) and lines[i + 1].strip() == code.split("\n")[0].strip():
                        self._add_issue(
                            file_path,
                            i + 1,
                            1,
                            "examples-language",
                            "warning",
                            "Code block missing language specifier",
                            "Add language after ``` (e.g., ```python)",
                        )
                        break

    def _check_manifest_completeness(self):
        """Check all standards are in MANIFEST.yaml"""
        manifest_files = set()
        for _code, data in self.manifest.get("standards", {}).items():
            if "full_name" in data:
                manifest_files.add(data["full_name"])
            elif "filename" in data:
                manifest_files.add(data["filename"])

        for std_file in self.standards_files:
            if std_file.name not in manifest_files:
                self._add_issue(
                    std_file,
                    1,
                    1,
                    "manifest-missing",
                    "error",
                    "Not found in MANIFEST.yaml",
                    f"Add entry for {std_file.name} to MANIFEST.yaml",
                )

    def _check_index_coverage(self):
        """Check STANDARDS_INDEX.md coverage"""
        index_path = self.root / "STANDARDS_INDEX.md"
        if index_path.exists():
            with open(index_path) as f:
                index_content = f.read()

            for std_file in self.standards_files:
                if std_file.name not in index_content:
                    self._add_issue(
                        std_file,
                        1,
                        1,
                        "index-missing",
                        "warning",
                        "Not found in STANDARDS_INDEX.md",
                        f"Add {std_file.name} to index",
                    )

    def _check_graph_relationships(self):
        """Check STANDARDS_GRAPH.md relationships"""
        graph_path = self.root / "STANDARDS_GRAPH.md"
        if graph_path.exists():
            with open(graph_path) as f:
                graph_content = f.read()

            # Check for required relationship types
            rel_types = ["requires", "recommends", "enhances", "conflicts"]
            for rel_type in rel_types:
                if rel_type not in graph_content:
                    self._add_issue(
                        graph_path,
                        1,
                        1,
                        f"graph-{rel_type}",
                        "info",
                        f"Missing '{rel_type}' relationship type",
                        f"Document {rel_type} relationships",
                    )

    def _add_issue(
        self,
        file_path: Path,
        line: int,
        column: int,
        rule: str,
        severity: str,
        message: str,
        fix_suggestion: str | None = None,
    ):
        """Add a linting issue"""
        self.issues.append(
            LintIssue(
                file=str(file_path.relative_to(self.root)),
                line=line,
                column=column,
                rule=rule,
                severity=severity,
                message=message,
                fix_suggestion=fix_suggestion,
            )
        )

    def format_report(self, format_type: str = "text") -> str:
        """Format the linting report"""
        if format_type == "json":
            return json.dumps(
                [
                    {
                        "file": issue.file,
                        "line": issue.line,
                        "column": issue.column,
                        "rule": issue.rule,
                        "severity": issue.severity,
                        "message": issue.message,
                        "fix": issue.fix_suggestion,
                    }
                    for issue in self.issues
                ],
                indent=2,
            )

        # Group by file
        by_file = defaultdict(list)
        for issue in self.issues:
            by_file[issue.file].append(issue)

        # Count by severity
        counts = defaultdict(int)
        for issue in self.issues:
            counts[issue.severity] += 1

        # Format text report
        lines = [
            "Standards Linting Report",
            "=" * 50,
            f"Files checked: {len(self.standards_files)}",
            f"Issues found: {len(self.issues)}",
            f"  Errors: {counts['error']}",
            f"  Warnings: {counts['warning']}",
            f"  Info: {counts['info']}",
            "",
        ]

        for file, issues in sorted(by_file.items()):
            lines.append(f"\n{file}:")
            for issue in sorted(issues, key=lambda x: (x.line, x.column)):
                severity_icon = {"error": "✗", "warning": "⚠", "info": "ℹ"}.get(issue.severity, "?")
                lines.append(f"  {issue.line}:{issue.column} {severity_icon} [{issue.rule}] {issue.message}")
                if issue.fix_suggestion:
                    lines.append(f"         Fix: {issue.fix_suggestion}")

        return "\n".join(lines)


def main():
    """Run the linter"""
    import argparse

    parser = argparse.ArgumentParser(description="Lint standards repository")
    parser.add_argument("path", nargs="?", default=".", help="Path to repository root")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    parser.add_argument("--fix", action="store_true", help="Apply automatic fixes (not implemented)")

    args = parser.parse_args()

    linter = StandardsLinter(args.path)
    issues = linter.lint_all()

    print(linter.format_report(args.format))

    # Exit with error if errors found
    error_count = sum(1 for issue in issues if issue.severity == "error")
    if error_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
