#!/usr/bin/env python3
"""
Generate a comprehensive standards inventory from the repository.
Outputs JSON catalog with normalized metadata for each standard document.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional

# Standard document codes mapping
STANDARD_CODES = {
    "CODING_STANDARDS": "CS",
    "TESTING_STANDARDS": "TS",
    "MODERN_SECURITY_STANDARDS": "SEC",
    "FRONTEND_MOBILE_STANDARDS": "FE",
    "WEB_DESIGN_UX_STANDARDS": "WD",
    "CLOUD_NATIVE_STANDARDS": "CN",
    "DEVOPS_PLATFORM_STANDARDS": "DOP",
    "DATA_ENGINEERING_STANDARDS": "DE",
    "DATABASE_STANDARDS": "DB",
    "LEGAL_COMPLIANCE_STANDARDS": "LEG",
    "COMPLIANCE_STANDARDS": "COMP",
    "NIST_IMPLEMENTATION_GUIDE": "NIST-IG",
    "OBSERVABILITY_STANDARDS": "OBS",
    "EVENT_DRIVEN_STANDARDS": "EVT",
    "PROJECT_MANAGEMENT_STANDARDS": "PM",
    "COST_OPTIMIZATION_STANDARDS": "COST",
    "SEO_WEB_MARKETING_STANDARDS": "SEO",
    "KNOWLEDGE_MANAGEMENT_STANDARDS": "KM",
    "MODEL_CONTEXT_PROTOCOL_STANDARDS": "MCP",
    "UNIFIED_STANDARDS": "UNIFIED",
    "CONTENT_STANDARDS": "CONT",
    "MICROSERVICES_STANDARDS": "MS",
    "ML_AI_STANDARDS": "MLAI",
    "GITHUB_PLATFORM_STANDARDS": "GH",
    "TOOLCHAIN_STANDARDS": "TOOL",
}


def extract_nist_controls(content: str) -> List[str]:
    """Extract NIST control references from document content."""
    controls = set()
    # Look for patterns like AC-2, AC-2(1), SC-13, etc.
    pattern = r"\b([A-Z]{2}-\d+(?:\(\d+\))?)\b"
    matches = re.findall(pattern, content)
    for match in matches:
        if match.startswith(
            (
                "AC-",
                "AU-",
                "AT-",
                "CM-",
                "CP-",
                "IA-",
                "IR-",
                "MA-",
                "MP-",
                "PS-",
                "PE-",
                "PL-",
                "PM-",
                "RA-",
                "CA-",
                "SC-",
                "SI-",
                "SA-",
                "SR-",
            )
        ):
            controls.add(match)
    return sorted(list(controls))


def extract_title(content: str, filepath: str) -> str:
    """Extract title from markdown file."""
    lines = content.split("\n")
    for line in lines[:10]:  # Check first 10 lines
        if line.startswith("# "):
            return line.replace("# ", "").strip()
    # Fallback to filename
    return Path(filepath).stem.replace("_", " ").title()


def extract_description(content: str) -> str:
    """Extract description from markdown file."""
    lines = content.split("\n")
    in_header = False
    description_lines = []

    for line in lines:
        if line.startswith("# "):
            in_header = True
            continue
        if in_header and line.strip() and not line.startswith("#"):
            # First non-header paragraph after title
            description_lines.append(line.strip())
            if len(description_lines) >= 2:  # Get first 2 lines
                break
        if in_header and line.startswith("##"):
            break

    desc = " ".join(description_lines)
    # Truncate if too long
    if len(desc) > 200:
        desc = desc[:197] + "..."
    return desc


def get_standard_code(filename: str) -> str:
    """Get standard code from filename."""
    base = Path(filename).stem.upper()
    return STANDARD_CODES.get(base, base[:3])


def extract_related_standards(content: str) -> List[str]:
    """Extract references to other standards from content."""
    related = set()

    # Look for markdown links to other standards
    link_pattern = r"\[([^\]]+)\]\(([^)]+\.md)\)"
    matches = re.findall(link_pattern, content)

    for _text, link in matches:
        if "STANDARDS" in link.upper() or "NIST" in link.upper():
            # Extract filename without extension
            filename = Path(link).stem
            if filename.upper() in STANDARD_CODES:
                related.add(STANDARD_CODES[filename.upper()])
            elif "STANDARDS" in filename.upper():
                related.add(filename.upper().replace("_STANDARDS", ""))

    return sorted(list(related))


def extract_tags(content: str, filepath: str) -> List[str]:
    """Extract tags from document content and filepath."""
    tags = set()

    # Add tags based on filepath
    path_lower = filepath.lower()
    if "nist" in path_lower:
        tags.add("nist")
        tags.add("compliance")
    if "security" in path_lower or "SEC" in get_standard_code(Path(filepath).name):
        tags.add("security")
    if "frontend" in path_lower or "mobile" in path_lower:
        tags.add("frontend")
    if "backend" in path_lower or "api" in path_lower:
        tags.add("backend")
    if "cloud" in path_lower or "devops" in path_lower:
        tags.add("infrastructure")
    if "test" in path_lower:
        tags.add("testing")
    if "data" in path_lower or "database" in path_lower:
        tags.add("data")
    if "compliance" in path_lower or "legal" in path_lower:
        tags.add("compliance")
    if "project" in path_lower or "management" in path_lower:
        tags.add("management")

    # Look for common keywords in content
    content_lower = content.lower()[:5000]  # Check first 5000 chars
    keyword_tags = {
        "docker": "containers",
        "kubernetes": "k8s",
        "react": "react",
        "python": "python",
        "javascript": "javascript",
        "typescript": "typescript",
        "api": "api",
        "rest": "rest",
        "graphql": "graphql",
        "authentication": "auth",
        "authorization": "auth",
        "encryption": "encryption",
        "monitoring": "observability",
        "logging": "observability",
        "ci/cd": "cicd",
        "agile": "agile",
        "privacy": "privacy",
        "gdpr": "gdpr",
        "ml": "ml",
        "ai": "ai",
    }

    for keyword, tag in keyword_tags.items():
        if keyword in content_lower:
            tags.add(tag)

    return sorted(list(tags))


def process_standard_file(filepath: str) -> Optional[Dict]:
    """Process a single standard document file."""
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()

        # Skip empty files
        if not content.strip():
            return None

        # Create relative path from repo root
        try:
            rel_path = str(Path(filepath).relative_to(Path.cwd()))
        except ValueError:
            # If relative_to fails, just use the path as is
            rel_path = str(Path(filepath))

        # Generate unique ID
        doc_id = Path(filepath).stem.lower().replace("_", "-")
        if "nist" in filepath.lower():
            doc_id = "nist-" + doc_id

        return {
            "id": doc_id,
            "slug": Path(filepath).stem.lower(),
            "code": get_standard_code(Path(filepath).name),
            "title": extract_title(content, filepath),
            "path": rel_path,
            "tags": extract_tags(content, filepath),
            "description": extract_description(content),
            "related": extract_related_standards(content),
            "nist_controls": (
                extract_nist_controls(content) if "nist" in filepath.lower() or "compliance" in filepath.lower() else []
            ),
        }
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None


def main():
    """Generate standards inventory."""
    standards = []

    # Define search paths
    search_paths = [
        "docs/standards/*.md",
        "docs/nist/*.md",
        "docs/guides/KICKSTART*.md",
        "docs/guides/STANDARDS*.md",
        "docs/guides/ADOPTION*.md",
        "docs/guides/VALIDATION*.md",
        "standards/**/*.md",
        "prompts/nist-compliance/*.md",
        "examples/nist-templates/README.md",
        "CLAUDE.md",
    ]

    # Collect all standard files
    all_files = set()
    for pattern in search_paths:
        for filepath in Path(".").glob(pattern):
            if filepath.is_file():
                all_files.add(str(filepath))

    # Process each file
    for filepath in sorted(all_files):
        doc = process_standard_file(filepath)
        if doc:
            standards.append(doc)
            print(f"Processed: {doc['code']} - {doc['title']}")

    # Sort by code
    standards.sort(key=lambda x: x["code"])

    # Generate summary stats
    summary = {
        "total_documents": len(standards),
        "categories": len(set(s["code"] for s in standards)),
        "nist_enabled": len([s for s in standards if s.get("nist_controls")]),
        "unique_tags": sorted(list(set(tag for s in standards for tag in s["tags"]))),
        "generation_timestamp": "2025-08-23T00:00:00Z",
    }

    # Create output
    output = {
        "summary": summary,
        "standards": standards,
    }

    # Write to file
    output_path = Path("reports/generated/standards-inventory.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"\n✅ Generated inventory with {len(standards)} standards")
    print(f"📁 Output: {output_path}")

    # Also generate a quick reference markdown
    ref_path = Path("reports/generated/standards-quick-reference.md")
    with open(ref_path, "w", encoding="utf-8") as f:
        f.write("# Standards Quick Reference\n\n")
        f.write(f"Generated: 2025-08-23 | Total: {len(standards)} documents\n\n")
        f.write("| Code | Title | Tags | Path |\n")
        f.write("|------|-------|------|------|\n")
        for std in standards:
            tags = ", ".join(std["tags"][:3]) if std["tags"] else "-"
            f.write(f"| **{std['code']}** | {std['title']} | {tags} | [{std['path']}]({std['path']}) |\n")

    print(f"📄 Quick reference: {ref_path}")


if __name__ == "__main__":
    main()
