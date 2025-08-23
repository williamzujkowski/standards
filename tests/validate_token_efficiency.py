#!/usr/bin/env python3
"""
Token Efficiency Validation Tests
Ensures documentation follows token-efficient patterns from KNOWLEDGE_MANAGEMENT_STANDARDS.md
"""

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

import yaml


@dataclass
class TokenMetrics:
    """Token usage metrics for a document"""

    file_name: str
    total_tokens: int
    section_tokens: Dict[str, int]
    efficiency_score: float
    recommendations: List[str]


class TokenEfficiencyValidator:
    """Validates token efficiency of documentation"""

    def __init__(self, root_path: str = "."):
        self.root = Path(root_path)
        self.token_multiplier = 0.75  # Approximate tokens per word

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count (roughly 0.75 tokens per word)"""
        words = len(text.split())
        return int(words * self.token_multiplier)

    def analyze_document(self, file_path: Path) -> TokenMetrics:
        """Analyze token efficiency of a document"""
        with open(file_path) as f:
            content = f.read()

        # Split into sections
        sections = self._split_sections(content)
        section_tokens = {name: self.estimate_tokens(text) for name, text in sections.items()}

        total_tokens = sum(section_tokens.values())
        efficiency_score = self._calculate_efficiency(sections)
        recommendations = self._generate_recommendations(sections, section_tokens)

        return TokenMetrics(
            file_name=file_path.name,
            total_tokens=total_tokens,
            section_tokens=section_tokens,
            efficiency_score=efficiency_score,
            recommendations=recommendations,
        )

    def _split_sections(self, content: str) -> Dict[str, str]:
        """Split document into sections by headers"""
        sections = {}
        current_section = "header"
        current_content = []

        for line in content.split("\n"):
            if line.startswith("## "):
                if current_content:
                    sections[current_section] = "\n".join(current_content)
                current_section = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)

        if current_content:
            sections[current_section] = "\n".join(current_content)

        return sections

    def _calculate_efficiency(self, sections: Dict[str, str]) -> float:
        """Calculate efficiency score (0-100)"""
        score = 100.0

        # Penalize overly long sections
        for _name, content in sections.items():
            tokens = self.estimate_tokens(content)
            if tokens > 2000:
                score -= 10
            elif tokens > 3000:
                score -= 20

        # Reward progressive disclosure patterns
        if any("quick" in name.lower() or "summary" in name.lower() for name in sections):
            score += 5

        # Check for code example efficiency
        code_blocks = len(re.findall(r"```", "\n".join(sections.values())))
        if code_blocks > 0:
            avg_tokens_per_block = sum(len(s) for s in sections.values()) / code_blocks / 4
            if avg_tokens_per_block < 500:  # Concise examples
                score += 5

        return max(0, min(100, score))

    def _generate_recommendations(self, sections: Dict[str, str], section_tokens: Dict[str, int]) -> List[str]:
        """Generate token optimization recommendations"""
        recommendations = []

        # Check for overly long sections
        for name, tokens in section_tokens.items():
            if tokens > 2000:
                recommendations.append(
                    f"Section '{name}' has {tokens} tokens. "
                    "Consider splitting into subsections or using progressive disclosure."
                )

        # Check for missing summaries
        has_summary = any("summary" in name.lower() or "overview" in name.lower() for name in sections)
        if not has_summary:
            recommendations.append("Add a summary or overview section for quick reference (100-500 tokens).")

        # Check total document size
        total = sum(section_tokens.values())
        if total > 15000:
            recommendations.append(
                f"Document has {total} tokens total. "
                "Consider splitting into multiple documents or using MANIFEST.yaml for progressive loading."
            )

        return recommendations

    def validate_manifest_alignment(self) -> Dict[str, List[str]]:
        """Validate that MANIFEST.yaml token counts align with actual content"""
        manifest_path = self.root / "MANIFEST.yaml"
        if not manifest_path.exists():
            return {"error": ["MANIFEST.yaml not found"]}

        with open(manifest_path) as f:
            manifest = yaml.safe_load(f)

        misalignments = {}

        for code, standard in manifest.get("standards", {}).items():
            file_name = standard.get("full_name") or standard.get("filename")
            if not file_name:
                continue

            file_path = self.root / file_name
            if not file_path.exists():
                continue

            # Check section token estimates
            with open(file_path) as f:
                content = f.read()

            for section_name, section_data in standard.get("sections", {}).items():
                manifest_tokens = section_data.get("tokens", 0)

                # Try to find section in actual file
                section_pattern = f"#+ {section_name.replace('-', ' ').title()}"
                if re.search(section_pattern, content, re.IGNORECASE):
                    # Extract section content (simplified)
                    section_start = content.lower().find(section_name.replace("-", " "))
                    if section_start > 0:
                        section_text = content[section_start : section_start + 5000]
                        actual_tokens = self.estimate_tokens(section_text)

                        # Allow 30% variance
                        if abs(actual_tokens - manifest_tokens) > manifest_tokens * 0.3:
                            if code not in misalignments:
                                misalignments[code] = []
                            misalignments[code].append(
                                f"{section_name}: manifest={manifest_tokens}, " f"estimated={actual_tokens}"
                            )

        return misalignments

    def generate_token_report(self) -> str:
        """Generate comprehensive token efficiency report"""
        report = ["TOKEN EFFICIENCY REPORT", "=" * 50, ""]

        # Analyze all standards files
        total_tokens = 0
        for std_file in sorted(self.root.glob("*_STANDARDS.md")):
            metrics = self.analyze_document(std_file)
            total_tokens += metrics.total_tokens

            report.append(f"\n{metrics.file_name}")
            report.append(f"  Total tokens: {metrics.total_tokens:,}")
            report.append(f"  Efficiency score: {metrics.efficiency_score:.1f}/100")

            if metrics.recommendations:
                report.append("  Recommendations:")
                for rec in metrics.recommendations:
                    report.append(f"    - {rec}")

        report.append(f"\n\nTOTAL REPOSITORY TOKENS: {total_tokens:,}")

        # Check MANIFEST alignment
        report.append("\n\nMANIFEST.yaml Alignment Check:")
        report.append("-" * 30)
        misalignments = self.validate_manifest_alignment()

        if not misalignments:
            report.append("✓ All MANIFEST token estimates align with actual content")
        else:
            for code, issues in misalignments.items():
                report.append(f"\n{code}:")
                for issue in issues:
                    report.append(f"  - {issue}")

        return "\n".join(report)


def main():
    """Run token efficiency validation"""
    validator = TokenEfficiencyValidator()

    print("Running token efficiency analysis...")
    print("")

    # Generate and print report
    report = validator.generate_token_report()
    print(report)

    # Quick summary
    print("\n" + "=" * 50)
    print("QUICK RECOMMENDATIONS:")
    print("=" * 50)

    recommendations = [
        "1. Keep individual sections under 2000 tokens",
        "2. Add summary/overview sections (100-500 tokens)",
        "3. Use MANIFEST.yaml for progressive loading of large docs",
        "4. Split documents over 15,000 tokens",
        "5. Keep code examples concise and focused",
    ]

    for rec in recommendations:
        print(f"  {rec}")

    print("\nFor detailed progressive loading setup, see KNOWLEDGE_MANAGEMENT_STANDARDS.md")


if __name__ == "__main__":
    main()
