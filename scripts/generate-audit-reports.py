#!/usr/bin/env python3
"""
Generate link check and structure audit reports for the standards repository.

- Reads config/audit-rules.yaml for orphan exclusions and hub requirements.
- Skips links inside fenced/inline code; ignores placeholder anchors (url, image-url).
- Resolves internal links robustly (../, ./, directory -> README.md, implicit .md).
- Emits Markdown + JSON reports; writes a hub-matrix.tsv for debugging.
- Ruff-friendly: no one-line compound statements.
"""

import fnmatch
import json
import re
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

import yaml


ROOT = Path(__file__).resolve().parents[1] if (Path(__file__).parent.name == "scripts") else Path.cwd()
OUTDIR = ROOT / "reports" / "generated"
POLICY = ROOT / "config" / "audit-rules.yaml"

DEFAULT_RULES: dict = {
    "orphans": {
        "exclude": [
            ".claude/**",
            "subagents/**",
            "memory/**",
            "prompts/**",
            "reports/generated/**",
            ".vscode/**",
            ".git/**",
            "node_modules/**",
            "__pycache__/**",
        ],
        "require_link_from": [
            {"pattern": "docs/standards/**/*.md", "hubs": ["docs/standards/UNIFIED_STANDARDS.md"]},
        ],
    }
}

PLACEHOLDER_LINK_PATTERNS = ("image-url", "(image-url)", "url", "(url)", "link", "(link)")

LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FENCE_REGEX = re.compile(r"```.*?```", flags=re.DOTALL)
TILDE_FENCE_REGEX = re.compile(r"~~~.*?~~~", flags=re.DOTALL)
INLINE_CODE_REGEX = re.compile(r"`[^`]*`")

# Deterministic AUTO-LINKS parsing
AUTO_BEGIN = "<!-- AUTO-LINKS:"
AUTO_END = "<!-- /AUTO-LINKS -->"


def parse_autolinks_section(text: str) -> list[tuple[str, str]]:
    """Return list of (text, link) from AUTO-LINKS blocks only - deterministic parse."""
    links = []
    start_idx = 0

    while True:
        start = text.find(AUTO_BEGIN, start_idx)
        if start == -1:
            break

        end = text.find(AUTO_END, start)
        if end == -1:
            break

        # Extract the block between markers
        block = text[start + len(AUTO_BEGIN) : end]

        # Extract all markdown links from this block
        for match in LINK_REGEX.findall(block):
            links.append(match)

        start_idx = end + len(AUTO_END)

    return links


def load_rules() -> dict:
    if POLICY.exists():
        try:
            user = yaml.safe_load(POLICY.read_text(encoding="utf-8")) or {}
            merged = DEFAULT_RULES.copy()
            merged["orphans"] = merged.get("orphans", {}).copy()
            uo = (user or {}).get("orphans", {})
            merged["orphans"]["exclude"] = list({*DEFAULT_RULES["orphans"]["exclude"], *uo.get("exclude", [])})
            merged["orphans"]["require_link_from"] = uo.get(
                "require_link_from", DEFAULT_RULES["orphans"]["require_link_from"]
            )
            # Add link_check exclusions
            merged["link_check"] = user.get("link_check", {})
            return merged
        except Exception as e:
            print(f"⚠️  Failed to read {POLICY}: {e}. Using defaults.")
    return DEFAULT_RULES


def strip_code(content: str) -> str:
    content = FENCE_REGEX.sub("", content)
    content = TILDE_FENCE_REGEX.sub("", content)
    content = INLINE_CODE_REGEX.sub("", content)
    return content


def normalize_repo_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except Exception:
        return path.resolve().as_posix()


def resolve_internal_link(source_file: Path, link: str) -> tuple[bool, str]:
    if link.startswith("mailto:") or link.strip() == "" or link.startswith("#"):
        return True, ""

    raw = unquote(link)
    target_no_anchor = raw.split("#", 1)[0].strip()
    base_dir = source_file.parent
    target_path = (base_dir / target_no_anchor).resolve()

    if target_path.exists():
        if target_path.is_dir():
            readme = target_path / "README.md"
            if readme.exists():
                return True, normalize_repo_path(readme)
            return True, normalize_repo_path(target_path)
        return True, normalize_repo_path(target_path)

    if not target_path.suffix and (target_path.with_suffix(".md")).exists():
        return True, normalize_repo_path(target_path.with_suffix(".md"))

    if (target_path / "README.md").exists():
        return True, normalize_repo_path(target_path / "README.md")

    return False, normalize_repo_path(target_path)


def check_links_in_file(
    filepath: Path,
) -> tuple[list[tuple[str, str]], list[tuple[str, str]], list[tuple[str, str, str]]]:
    internal_links: list[tuple[str, str]] = []
    external_links: list[tuple[str, str]] = []
    broken_links: list[tuple[str, str, str]] = []

    try:
        content = filepath.read_text(encoding="utf-8")

        # 1) Deterministic links from AUTO-LINKS blocks
        auto_links = parse_autolinks_section(content)
        for text, link in auto_links:
            link = link.strip()
            if not link.startswith(("http://", "https://", "#", "mailto:")):
                internal_links.append((text, link))

        # 2) Standard markdown links from entire doc (excluding code blocks)
        content_no_code = strip_code(content)

        for text, link in LINK_REGEX.findall(content_no_code):
            link = link.strip()

            if link.startswith("#"):
                continue
            if any(ph in link for ph in PLACEHOLDER_LINK_PATTERNS):
                continue

            if link.startswith(("http://", "https://")):
                external_links.append((text, link))
                continue

            internal_links.append((text, link))
            ok, _ = resolve_internal_link(filepath, link)
            if not ok:
                broken_links.append((text, link, normalize_repo_path(filepath)))

    except Exception as e:
        print(f"Error processing {filepath}: {e}")

    return internal_links, external_links, broken_links


def matches_any(path: str, patterns: Iterable[str]) -> bool:
    """Check if path matches any of the patterns, supporting ** glob patterns."""
    for pat in patterns:
        # Convert ** patterns for proper matching
        if "**" in pat:
            # Convert pattern to work with pathlib
            Path(path)
            Path(pat)

            # Simple implementation: check if path matches the pattern structure
            # e.g., "docs/standards/**/*.md" should match "docs/standards/FOO.md"
            # and "docs/standards/subdir/BAR.md"

            # Split pattern into parts
            pattern_parts = pat.split("/")
            path_parts = path.split("/")

            # Find where ** appears
            if "**" in pattern_parts:
                star_idx = pattern_parts.index("**")

                # Check prefix matches
                if star_idx > 0:
                    prefix = pattern_parts[:star_idx]
                    if len(path_parts) < len(prefix):
                        continue
                    if path_parts[: len(prefix)] != prefix:
                        continue

                # Check suffix matches (if any after **)
                if star_idx < len(pattern_parts) - 1:
                    suffix = pattern_parts[star_idx + 1 :]
                    # The suffix might contain wildcards
                    if len(suffix) == 1 and "*" in suffix[0]:
                        # Just check extension
                        if fnmatch.fnmatch(path_parts[-1], suffix[0]):
                            return True
                    elif len(path_parts) >= len(suffix):
                        # Match the suffix parts
                        if all(fnmatch.fnmatch(p, s) for p, s in zip(path_parts[-len(suffix) :], suffix, strict=False)):
                            return True
                else:
                    # No suffix after **, so everything under prefix matches
                    return True
            else:
                # No ** in this pattern but it's inside a ** block?
                # This shouldn't happen, but use path-aware matching anyway
                from pathlib import PurePath

                try:
                    if PurePath(path).match(pat):
                        return True
                except (ValueError, TypeError):
                    if path == pat:
                        return True
        else:
            # No ** in pattern, use path-aware matching
            # Use pathlib's match() which respects path boundaries
            from pathlib import PurePath

            try:
                if PurePath(path).match(pat):
                    return True
            except (ValueError, TypeError):
                # Fall back to simple string comparison for edge cases
                if path == pat:
                    return True
    return False


def build_link_graph(
    all_md_files: list[Path],
) -> tuple[dict[str, set[str]], list[tuple[str, str, str]], list[tuple[str, str, str]]]:
    graph: dict[str, set[str]] = {}
    all_broken: list[tuple[str, str, str]] = []
    all_external: list[tuple[str, str, str]] = []

    for md in all_md_files:
        key = normalize_repo_path(md)
        graph.setdefault(key, set())

    for md in all_md_files:
        src_key = normalize_repo_path(md)
        internal, external, broken = check_links_in_file(md)

        for text, link in external:
            all_external.append((src_key, text, link))

        if broken:
            all_broken.extend(broken)

        for _, link in internal:
            ok, resolved = resolve_internal_link(md, link)
            if ok and resolved:
                graph.setdefault(resolved, set()).add(src_key)

    pruned_graph = {}
    for k, v in graph.items():
        if not matches_any(k, ["reports/generated/**", ".git/**", "node_modules/**", "__pycache__/**"]):
            pruned_graph[k] = v

    return pruned_graph, all_broken, all_external


def compute_orphans(graph: dict[str, set[str]], rules: dict) -> list[str]:
    excludes = rules.get("orphans", {}).get("exclude", [])
    orphans: list[str] = []

    for f, inbound in graph.items():
        # Respect exclusions
        if matches_any(f, excludes):
            continue

        # Treat any README / index file as inherently "linked" (it's a hub/landing page)
        name = f.rsplit("/", 1)[-1].lower()
        if name in ("readme.md", "index.md", "_index.md", "changelog.md", "license.md"):
            continue

        # Orphan = no inbound links
        if len(inbound) == 0:
            orphans.append(f)

    return sorted(orphans)


def enforce_hub_rules(graph: dict[str, set[str]], rules: dict) -> tuple[list[str], dict[str, dict[str, bool]]]:
    violations: list[str] = []
    matrix: dict[str, dict[str, bool]] = {}

    reqs = rules.get("orphans", {}).get("require_link_from", [])
    all_hubs = {h for r in reqs for h in r.get("hubs", [])}

    for rule in reqs:
        pat = rule.get("pattern")
        hubs = set(rule.get("hubs", []))

        if not pat or not hubs:
            continue

        for f, inbound in graph.items():
            if not matches_any(f, [pat]):
                continue

            # Skip hub files and READMEs as targets for hub requirements
            if f in hubs:
                continue
            if f.endswith("/README.md") or f.endswith("README.md"):
                continue

            matrix.setdefault(f, {})
            linked = False

            for h in hubs:
                hit = h in inbound
                matrix[f][h] = hit
                if hit:
                    linked = True

            if not linked and not matches_any(f, rules.get("orphans", {}).get("exclude", [])):
                violations.append(f)

    # Add hub rows to matrix for visibility
    for h in all_hubs:
        matrix.setdefault(h, {})
        matrix[h][h] = True

    violations = sorted(set(violations))
    return violations, matrix


def analyze_repository_structure(rules: dict) -> dict:
    issues: dict = {
        "orphaned_files": [],
        "missing_cross_refs": [],
        "non_conforming_names": [],
        "duplicate_content": [],
        "missing_readmes": [],
        "structure_violations": [],
        "hub_violations": [],
    }

    expected_dirs = {
        "docs/standards": "Standard documents",
        "docs/nist": "NIST compliance docs",
        "docs/guides": "Implementation guides",
        "docs/core": "Core docs",
        "examples": "Example code",
        "scripts": "Utility scripts",
        "prompts": "LLM prompts",
        "config": "Configuration files",
        "reports/generated": "Generated reports",
    }
    for d, desc in expected_dirs.items():
        if not (ROOT / d).exists():
            issues["structure_violations"].append(f"Missing expected directory: {d} ({desc})")

    all_md_files: list[Path] = [p for p in ROOT.rglob("*.md")]
    graph, _, _ = build_link_graph(all_md_files)

    # Orphans (policy-aware)
    issues["orphaned_files"] = compute_orphans(graph, rules)

    # Filename convention check
    for md in all_md_files:
        rel = normalize_repo_path(md)
        if matches_any(rel, rules["orphans"]["exclude"]):
            continue
        if rel.startswith("docs/standards/"):
            name = md.name
            if name.upper() not in ("README.MD", "UNIFIED_STANDARDS.MD"):
                stem = name.rsplit(".", 1)[0]
                if not stem.replace("_", "").isupper():
                    issues["non_conforming_names"].append(f"{rel} - Standards should be UPPERCASE_WITH_UNDERSCORES.md")

    # Legacy cross-ref hint (info only)
    for md in all_md_files:
        rel = normalize_repo_path(md)
        if matches_any(rel, rules["orphans"]["exclude"]):
            continue
        if rel.startswith("docs/standards/") and md.name not in ("UNIFIED_STANDARDS.md", "README.md"):
            try:
                content = md.read_text(encoding="utf-8")
                if "UNIFIED_STANDARDS" not in content:
                    issues["missing_cross_refs"].append(f"{rel} - No reference to UNIFIED_STANDARDS.md")
            except Exception:
                pass

    # Missing READMEs
    # Directories that never need READMEs (cache, build artifacts, etc.)
    skip_readme_dirs = {
        "__pycache__",
        ".benchmarks",
        "node_modules",
        ".git",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        ".tox",
    }
    for d in ROOT.rglob("*"):
        if not d.is_dir():
            continue
        rel = normalize_repo_path(d)
        # Skip if any part of the path is a known skip directory
        if any(skip_dir in d.parts for skip_dir in skip_readme_dirs):
            continue
        if matches_any(
            rel,
            rules["orphans"]["exclude"]
            + [".git/**", "**/__pycache__/**", "**/node_modules/**", "reports/generated/**", "**/.benchmarks/**"],
        ):
            continue
        if rel and rel != "." and not (d / "README.md").exists():
            issues["missing_readmes"].append(rel)

    # Hub enforcement
    hub_violations, hub_matrix = enforce_hub_rules(graph, rules)
    issues["hub_violations"] = hub_violations

    # Write hub matrix
    OUTDIR.mkdir(parents=True, exist_ok=True)
    hubs_order: list[str] = sorted(
        {h for r in rules.get("orphans", {}).get("require_link_from", []) for h in r.get("hubs", [])}
    )
    with open(OUTDIR / "hub-matrix.tsv", "w", encoding="utf-8") as f:
        f.write("file\t" + "\t".join(hubs_order) + "\n")
        for file in sorted(hub_matrix.keys()):
            row = [file]
            for h in hubs_order:
                row.append("1" if hub_matrix[file].get(h) else "0")
            f.write("\t".join(row) + "\n")

    return issues


def generate_linkcheck_report() -> tuple[str, int]:
    lines: list[str] = []
    lines.append("# Link Check Report")
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\n")

    # Load rules to get link_check exclusions
    rules = load_rules()
    link_exclusions = rules.get("link_check", {}).get("exclude_files", [])

    all_broken: list[tuple[str, str, str]] = []
    all_external: list[tuple[str, str, str]] = []
    file_count = 0

    for md in ROOT.rglob("*.md"):
        rel = normalize_repo_path(md)
        if matches_any(rel, ["reports/generated/**", ".git/**", "node_modules/**", "__pycache__/**"]):
            continue
        # Skip files matching link_check exclusions
        if link_exclusions and matches_any(rel, link_exclusions):
            continue
        file_count += 1
        _, external, broken = check_links_in_file(md)
        if broken:
            all_broken.extend(broken)
        if external:
            all_external.extend([(normalize_repo_path(md), t, link) for t, link in external])

    lines.append(f"\n## Broken Internal Links ({len(all_broken)} found)\n")
    if all_broken:
        for text, link, source in all_broken:
            lines.append(f"- **{source}**: [{text}]({link})")
    else:
        lines.append("✅ No broken internal links found!")

    lines.append(f"\n## External Links ({len(all_external)} found)\n")
    if all_external:
        by_domain: dict[str, list[tuple[str, str, str]]] = {}
        for source, text, link in all_external:
            domain = urlparse(link).netloc
            if domain not in by_domain:
                by_domain[domain] = []
            by_domain[domain].append((source, text, link))
        for domain in sorted(by_domain.keys()):
            links = by_domain[domain]
            lines.append(f"\n### {domain} ({len(links)} links)")
            for source, text, link in links[:5]:
                lines.append(f"- {source}: [{text}]({link})")
            if len(links) > 5:
                lines.append(f"- ... and {len(links) - 5} more")

    lines.append("\n## Summary\n")
    lines.append(f"- Files checked: {file_count}")
    lines.append(f"- Broken links: {len(all_broken)}")
    lines.append(f"- External links: {len(all_external)}")

    # Add trailing newline for pre-commit compliance
    return "\n".join(lines) + "\n", len(all_broken)


def generate_structure_audit_report(issues: dict) -> str:
    lines: list[str] = []
    lines.append("# Structure Audit Report")
    lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d')}\n")

    total_issues = sum(len(v) for v in issues.values() if isinstance(v, list))
    lines.append("## Summary\n")
    lines.append(f"Total issues found: {total_issues}\n")

    lines.append(f"\n## Orphaned Files ({len(issues['orphaned_files'])})\n")
    lines.append("Files not linked from any other document:\n")
    if issues["orphaned_files"]:
        for file in issues["orphaned_files"]:
            lines.append(f"- {file}")
    else:
        lines.append("✅ No orphaned files found")

    lines.append(f"\n## Missing Cross-References ({len(issues['missing_cross_refs'])})\n")
    lines.append("Standards documents not referencing UNIFIED_STANDARDS.md:\n")
    if issues["missing_cross_refs"]:
        for i in issues["missing_cross_refs"]:
            lines.append(f"- {i}")
    else:
        lines.append("✅ All standards properly cross-referenced")

    lines.append(f"\n## Non-Conforming Filenames ({len(issues['non_conforming_names'])})\n")
    if issues["non_conforming_names"]:
        for i in issues["non_conforming_names"]:
            lines.append(f"- {i}")
    else:
        lines.append("✅ All filenames follow conventions")

    lines.append(f"\n## Directories Missing README ({len(issues['missing_readmes'])})\n")
    if issues["missing_readmes"]:
        for d in issues["missing_readmes"]:
            lines.append(f"- {d}/")
    else:
        lines.append("✅ All directories have README files")

    lines.append(f"\n## Structure Violations ({len(issues['structure_violations'])})\n")
    if issues["structure_violations"]:
        for v in issues["structure_violations"]:
            lines.append(f"- {v}")
    else:
        lines.append("✅ Repository structure follows standards")

    lines.append(f"\n## Hub Violations ({len(issues['hub_violations'])})\n")
    if issues["hub_violations"]:
        lines.append("Files that must be linked from required hub(s) but are not:")
        for f in issues["hub_violations"]:
            lines.append(f"- {f}")
    else:
        lines.append("✅ All hub-link requirements satisfied")

    lines.append("\n## Recommendations\n")
    if total_issues > 0 or issues["hub_violations"]:
        lines.append("1. **Fix broken links**: Update or remove broken internal links")
        lines.append("2. **Link orphaned files**: Add references or extend exclusions in config/audit-rules.yaml")
        lines.append("3. **Add cross-references**: Link standards to UNIFIED_STANDARDS.md")
        lines.append("4. **Standardize names**: Rename files to follow conventions")
        lines.append("5. **Add READMEs**: Create README.md for directories lacking them")
        lines.append("6. **Satisfy hub rules**: Ensure required hub(s) link to required files")
    else:
        lines.append("✅ Repository structure is well-organized and compliant!")

    # Add trailing newline for pre-commit compliance
    return "\n".join(lines) + "\n"


def main() -> None:
    print("🔍 Generating audit reports (policy-aware)...")
    OUTDIR.mkdir(parents=True, exist_ok=True)
    rules = load_rules()

    print("Checking links...")
    link_md, broken_count = generate_linkcheck_report()
    (OUTDIR / "linkcheck.txt").write_text(link_md, encoding="utf-8")
    print(f"✅ Link check report: {OUTDIR / 'linkcheck.txt'}")

    print("Auditing structure...")
    issues = analyze_repository_structure(rules)
    struct_md = generate_structure_audit_report(issues)
    (OUTDIR / "structure-audit.md").write_text(struct_md, encoding="utf-8")
    print(f"✅ Structure audit: {OUTDIR / 'structure-audit.md'}")

    summary = {
        "broken_links": broken_count,
        "orphans": len(issues["orphaned_files"]),
        "hub_violations": len(issues["hub_violations"]),
        "timestamp": datetime.now().isoformat(),
    }
    # Write JSON with proper formatting and ending newline for pre-commit compliance
    (OUTDIR / "structure-audit.json").write_text(json.dumps(summary, indent=4) + "\n", encoding="utf-8")

    total_issues = sum(len(v) for v in issues.values() if isinstance(v, list))
    print("\n📊 Audit Summary:")
    print(f"  - Broken links: {broken_count}")
    print(f"  - Orphans: {summary['orphans']}")
    print(f"  - Hub violations: {summary['hub_violations']}")
    print(f"  - Structure issues (listed): {total_issues}")
    print(f"  - Reports generated in: {OUTDIR}/")


if __name__ == "__main__":
    main()
