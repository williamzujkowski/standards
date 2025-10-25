#!/usr/bin/env python3
"""
Advanced token counter for measuring actual token usage across the repository.

Features:
- Measures token usage for different file types
- Tracks token consumption by directory
- Compares against documented claims
- Supports multiple encoding schemes
- Generates detailed reports
"""

import argparse
import json
import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# Try to import tiktoken
try:
    import tiktoken

    TIKTOKEN_AVAILABLE = True
except ImportError:
    TIKTOKEN_AVAILABLE = False
    logger.warning("tiktoken not available - using estimation")


@dataclass
class TokenStats:
    """Token statistics for a file or directory."""

    path: str
    tokens: int
    chars: int
    lines: int
    file_type: str
    encoding: str = "estimation"
    children: List["TokenStats"] = field(default_factory=list)

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            "path": self.path,
            "tokens": self.tokens,
            "chars": self.chars,
            "lines": self.lines,
            "file_type": self.file_type,
            "encoding": self.encoding,
            "children": [c.to_dict() for c in self.children] if self.children else [],
        }


class TokenCounter:
    """Advanced token counter for repository analysis."""

    def __init__(self, repo_root: Path, encoding: str = "cl100k_base"):
        self.repo_root = repo_root
        self.encoding_name = encoding
        self.encoder = None

        if TIKTOKEN_AVAILABLE:
            try:
                self.encoder = tiktoken.get_encoding(encoding)
                logger.info(f"Using tiktoken encoding: {encoding}")
            except Exception as e:
                logger.warning(f"Failed to load tiktoken: {e}")
                self.encoder = None
        else:
            logger.info("Using estimation mode (~4 chars per token)")

        # File type mappings
        self.file_types = {
            ".md": "markdown",
            ".py": "python",
            ".yaml": "config",
            ".yml": "config",
            ".json": "config",
            ".sh": "shell",
            ".txt": "text",
        }

        # Exclusions
        self.exclude_patterns = {
            ".git",
            "__pycache__",
            "node_modules",
            ".venv",
            ".pytest_cache",
            ".ruff_cache",
            "site",
        }

    def count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        if self.encoder:
            return len(self.encoder.encode(text))
        else:
            # Fallback estimation: ~4 chars per token
            return len(text) // 4

    def should_exclude(self, path: Path) -> bool:
        """Check if path should be excluded."""
        parts = path.parts
        return any(pattern in parts for pattern in self.exclude_patterns)

    def count_file(self, file_path: Path) -> Optional[TokenStats]:
        """Count tokens in a single file."""
        if self.should_exclude(file_path):
            return None

        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            tokens = self.count_tokens(content)
            chars = len(content)
            lines = content.count("\n") + 1

            file_type = self.file_types.get(file_path.suffix, "other")

            return TokenStats(
                path=str(file_path.relative_to(self.repo_root)),
                tokens=tokens,
                chars=chars,
                lines=lines,
                file_type=file_type,
                encoding=self.encoding_name if self.encoder else "estimation",
            )

        except Exception as e:
            logger.debug(f"Error reading {file_path}: {e}")
            return None

    def count_directory(self, dir_path: Path, recursive: bool = True, file_pattern: str = "*") -> TokenStats:
        """Count tokens in a directory."""
        total_tokens = 0
        total_chars = 0
        total_lines = 0
        children: List[TokenStats] = []

        if recursive:
            files = dir_path.rglob(file_pattern)
        else:
            files = dir_path.glob(file_pattern)

        for file_path in files:
            if file_path.is_file() and not self.should_exclude(file_path):
                stats = self.count_file(file_path)
                if stats:
                    children.append(stats)
                    total_tokens += stats.tokens
                    total_chars += stats.chars
                    total_lines += stats.lines

        return TokenStats(
            path=str(dir_path.relative_to(self.repo_root)),
            tokens=total_tokens,
            chars=total_chars,
            lines=total_lines,
            file_type="directory",
            encoding=self.encoding_name if self.encoder else "estimation",
            children=children,
        )

    def analyze_by_type(self, stats: TokenStats) -> Dict[str, Dict[str, int]]:
        """Analyze token usage by file type."""
        by_type: Dict[str, Dict[str, int]] = {}

        def collect_stats(s: TokenStats):
            if s.file_type not in by_type:
                by_type[s.file_type] = {"tokens": 0, "chars": 0, "lines": 0, "files": 0}

            by_type[s.file_type]["tokens"] += s.tokens
            by_type[s.file_type]["chars"] += s.chars
            by_type[s.file_type]["lines"] += s.lines
            by_type[s.file_type]["files"] += 1 if s.file_type != "directory" else 0

            for child in s.children:
                collect_stats(child)

        collect_stats(stats)
        return by_type

    def analyze_by_directory(self, stats: TokenStats, max_depth: int = 2) -> Dict[str, int]:
        """Analyze token usage by directory."""
        by_dir: Dict[str, int] = {}

        def collect_by_dir(s: TokenStats, depth: int = 0):
            if depth <= max_depth:
                by_dir[s.path] = s.tokens

            for child in s.children:
                if child.file_type == "directory":
                    collect_by_dir(child, depth + 1)

        collect_by_dir(stats)
        return by_dir

    def find_largest_files(self, stats: TokenStats, limit: int = 10) -> List[TokenStats]:
        """Find files with most tokens."""
        all_files: List[TokenStats] = []

        def collect_files(s: TokenStats):
            if s.file_type != "directory":
                all_files.append(s)
            for child in s.children:
                collect_files(child)

        collect_files(stats)

        # Sort by token count
        all_files.sort(key=lambda x: x.tokens, reverse=True)
        return all_files[:limit]

    def compare_with_claims(self, stats: TokenStats) -> Dict[str, any]:
        """Compare actual token usage with documented claims."""
        comparisons = {}

        # Check CLAUDE.md token claim
        claude_md = self.repo_root / "CLAUDE.md"
        if claude_md.exists():
            claude_stats = self.count_file(claude_md)
            if claude_stats:
                comparisons["CLAUDE.md"] = {
                    "actual_tokens": claude_stats.tokens,
                    "file_size_chars": claude_stats.chars,
                    "lines": claude_stats.lines,
                }

        # Check skills directory token usage
        skills_dir = self.repo_root / "skills"
        if skills_dir.exists():
            skills_stats = self.count_directory(skills_dir)
            comparisons["skills"] = {
                "total_tokens": skills_stats.tokens,
                "file_count": len(skills_stats.children),
                "avg_tokens_per_skill": skills_stats.tokens // max(len(skills_stats.children), 1),
            }

        # Check documentation
        docs_dir = self.repo_root / "docs"
        if docs_dir.exists():
            docs_stats = self.count_directory(docs_dir)
            comparisons["docs"] = {
                "total_tokens": docs_stats.tokens,
                "file_count": len(docs_stats.children),
            }

        return comparisons

    def format_report(self, stats: TokenStats, by_type: Dict, largest: List[TokenStats], comparisons: Dict) -> str:
        """Format human-readable report."""
        lines = []
        lines.append("=" * 80)
        lines.append("TOKEN USAGE REPORT")
        lines.append("=" * 80)
        lines.append("")

        # Summary
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Total Tokens:    {stats.tokens:,}")
        lines.append(f"Total Characters: {stats.chars:,}")
        lines.append(f"Total Lines:      {stats.lines:,}")
        lines.append(f"Encoding:         {stats.encoding}")
        lines.append("")

        # By type
        lines.append("BY FILE TYPE")
        lines.append("-" * 80)
        for file_type, type_stats in sorted(by_type.items(), key=lambda x: x[1]["tokens"], reverse=True):
            if file_type != "directory":
                lines.append(
                    f"{file_type:15} {type_stats['tokens']:10,} tokens  "
                    f"{type_stats['files']:5,} files  "
                    f"{type_stats['chars']:10,} chars"
                )
        lines.append("")

        # Largest files
        lines.append("LARGEST FILES (by token count)")
        lines.append("-" * 80)
        for i, file_stats in enumerate(largest, 1):
            lines.append(f"{i:2}. {file_stats.tokens:7,} tokens  {file_stats.path}")
        lines.append("")

        # Comparisons
        if comparisons:
            lines.append("COMPARISON WITH DOCUMENTED CLAIMS")
            lines.append("-" * 80)
            for key, data in comparisons.items():
                lines.append(f"\n{key}:")
                for metric, value in data.items():
                    lines.append(f"  {metric}: {value:,}")
        lines.append("")

        lines.append("=" * 80)
        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Advanced token counter for repository analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Count tokens in entire repository
  python3 token-counter.py

  # Count specific directory
  python3 token-counter.py --directory docs/

  # Count only markdown files
  python3 token-counter.py --pattern "*.md"

  # Export JSON report
  python3 token-counter.py --export reports/token-usage.json

  # Use specific encoding
  python3 token-counter.py --encoding cl100k_base

  # Compare with claims
  python3 token-counter.py --compare-claims

Exit codes:
  0 - Success
  1 - Error
        """,
    )

    parser.add_argument("--directory", type=Path, help="Directory to analyze (default: repository root)")

    parser.add_argument("--pattern", default="*", help="File pattern to match (default: *)")

    parser.add_argument("--encoding", default="cl100k_base", help="Tiktoken encoding to use")

    parser.add_argument("--export", type=Path, help="Export results to JSON file")

    parser.add_argument("--compare-claims", action="store_true", help="Compare with documented claims")

    parser.add_argument("--top-files", type=int, default=10, help="Number of largest files to show")

    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Get repository root
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    # Initialize counter
    counter = TokenCounter(repo_root, args.encoding)

    # Analyze directory
    target_dir = args.directory if args.directory else repo_root
    if not target_dir.is_absolute():
        target_dir = repo_root / target_dir

    logger.info(f"Analyzing: {target_dir}")

    stats = counter.count_directory(target_dir, recursive=True, file_pattern=args.pattern)

    # Analyze by type
    by_type = counter.analyze_by_type(stats)

    # Find largest files
    largest = counter.find_largest_files(stats, args.top_files)

    # Compare with claims
    comparisons = {}
    if args.compare_claims:
        comparisons = counter.compare_with_claims(stats)

    # Print report
    print(counter.format_report(stats, by_type, largest, comparisons))

    # Export if requested
    if args.export:
        report = {
            "summary": stats.to_dict(),
            "by_type": by_type,
            "largest_files": [f.to_dict() for f in largest],
            "comparisons": comparisons,
        }

        args.export.parent.mkdir(parents=True, exist_ok=True)
        args.export.write_text(json.dumps(report, indent=2) + "\n")
        logger.info(f"Report exported to: {args.export}")

    sys.exit(0)


if __name__ == "__main__":
    main()
