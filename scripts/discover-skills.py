#!/usr/bin/env python3
"""
Skill discovery and recommendation engine.

Search skills, filter by category, recommend based on product type,
and resolve dependencies.
"""

import argparse
import sys
from pathlib import Path
from typing import Dict, List, Set, Optional
import yaml
import json
import re
import logging


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class SkillDiscovery:
    """Skill search and recommendation engine."""

    def __init__(self, skills_dir: Path, product_matrix: Optional[Path] = None):
        self.skills_dir = skills_dir
        self.product_matrix_path = product_matrix
        self.skills: Dict[str, Dict] = {}
        self.product_matrix: Dict = {}

        self.load_skills()
        if product_matrix and product_matrix.exists():
            self.load_product_matrix()

    def load_skills(self) -> None:
        """Load all SKILL.md files and parse metadata."""
        skill_files = list(self.skills_dir.rglob("SKILL.md"))

        logger.info(f"Loading skills from {self.skills_dir}")

        for skill_file in skill_files:
            try:
                skill_data = self.parse_skill(skill_file)
                skill_slug = skill_file.parent.name
                self.skills[skill_slug] = skill_data
                logger.debug(f"Loaded skill: {skill_slug}")
            except Exception as e:
                logger.warning(f"Failed to load {skill_file}: {e}")

        logger.info(f"Loaded {len(self.skills)} skills")

    def parse_skill(self, skill_file: Path) -> Dict:
        """Parse SKILL.md file and extract metadata."""
        content = skill_file.read_text()

        # Extract YAML frontmatter
        if not content.startswith("---"):
            raise ValueError("Missing YAML frontmatter")

        parts = content.split("---", 2)
        if len(parts) < 3:
            raise ValueError("Invalid YAML frontmatter structure")

        frontmatter = yaml.safe_load(parts[1])

        # Extract additional metadata
        skill_data = {
            "name": frontmatter.get("name", ""),
            "description": frontmatter.get("description", ""),
            "category": frontmatter.get("category", "general"),
            "tags": frontmatter.get("tags", []),
            "path": skill_file,
            "slug": skill_file.parent.name
        }

        # Extract related skills
        related_skills = self.extract_related_skills(parts[2])
        skill_data["related_skills"] = related_skills

        return skill_data

    def extract_related_skills(self, content: str) -> List[str]:
        """Extract related skills from content."""
        related = []

        # Look for links to other SKILL.md files
        pattern = r'\[([^\]]+)\]\(\.\./([^/]+)/SKILL\.md\)'
        matches = re.findall(pattern, content)

        for _, skill_slug in matches:
            related.append(skill_slug)

        return related

    def load_product_matrix(self) -> None:
        """Load product-matrix.yaml."""
        try:
            content = self.product_matrix_path.read_text()
            self.product_matrix = yaml.safe_load(content)
            logger.info(f"Loaded product matrix from {self.product_matrix_path}")
        except Exception as e:
            logger.warning(f"Failed to load product matrix: {e}")

    def search_by_keyword(self, keyword: str) -> List[Dict]:
        """Search skills by keyword in name or description."""
        keyword_lower = keyword.lower()
        results = []

        for skill_slug, skill_data in self.skills.items():
            name = skill_data["name"].lower()
            description = skill_data["description"].lower()
            tags = [t.lower() for t in skill_data.get("tags", [])]

            if (keyword_lower in name or
                keyword_lower in description or
                keyword_lower in tags):
                results.append(skill_data)

        return results

    def filter_by_category(self, category: str) -> List[Dict]:
        """Filter skills by category."""
        results = []

        for skill_data in self.skills.values():
            if skill_data["category"].lower() == category.lower():
                results.append(skill_data)

        return results

    def recommend_for_product(self, product_type: str) -> List[Dict]:
        """Recommend skills based on product type."""
        if not self.product_matrix:
            logger.warning("Product matrix not loaded")
            return []

        products = self.product_matrix.get("products", {})

        if product_type not in products:
            logger.warning(f"Product type not found: {product_type}")
            return []

        product_config = products[product_type]

        # Get standard codes
        standards = []
        for key in ["coding_standards", "testing_standards", "security_standards"]:
            if key in product_config:
                standards.extend(product_config[key])

        # Map standards to skills (simplified mapping)
        # In real implementation, this would use a more sophisticated mapping
        recommended = []

        for standard_code in standards:
            # Try to find matching skill
            for skill_data in self.skills.values():
                if standard_code.lower() in skill_data["name"].lower():
                    recommended.append(skill_data)
                    break

        return recommended

    def resolve_dependencies(self, skill_slug: str, visited: Optional[Set[str]] = None) -> List[str]:
        """Resolve skill dependencies (related skills)."""
        if visited is None:
            visited = set()

        if skill_slug in visited:
            return []

        visited.add(skill_slug)

        if skill_slug not in self.skills:
            return []

        skill_data = self.skills[skill_slug]
        dependencies = [skill_slug]

        # Recursively resolve related skills
        for related_slug in skill_data.get("related_skills", []):
            if related_slug not in visited:
                sub_deps = self.resolve_dependencies(related_slug, visited)
                dependencies.extend(sub_deps)

        return dependencies

    def format_skill_result(self, skill_data: Dict, verbose: bool = False) -> str:
        """Format skill result for display."""
        lines = []

        lines.append(f"• {skill_data['name']}")
        lines.append(f"  Slug: {skill_data['slug']}")
        lines.append(f"  Category: {skill_data['category']}")

        if verbose:
            lines.append(f"  Description: {skill_data['description']}")
            lines.append(f"  Path: {skill_data['path']}")

            if skill_data.get("tags"):
                lines.append(f"  Tags: {', '.join(skill_data['tags'])}")

            if skill_data.get("related_skills"):
                lines.append(f"  Related: {', '.join(skill_data['related_skills'])}")

        return "\n".join(lines)

    def generate_load_command(self, skill_slugs: List[str]) -> str:
        """Generate load command for skills."""
        return f"@load skills:[{','.join(skill_slugs)}]"


def main():
    parser = argparse.ArgumentParser(
        description="Skill discovery and recommendation engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by keyword
  python3 discover-skills.py --search "security"

  # Filter by category
  python3 discover-skills.py --category "testing"

  # Recommend for product type
  python3 discover-skills.py --product-type "api" \\
    --product-matrix config/product-matrix.yaml

  # Resolve dependencies
  python3 discover-skills.py --resolve-deps "api-security"

  # Generate load command
  python3 discover-skills.py --search "api" --generate-command

  # List all skills
  python3 discover-skills.py --list-all
        """
    )

    parser.add_argument(
        "--skills-dir",
        type=Path,
        default=Path("skills"),
        help="Directory containing skills (default: ./skills)"
    )

    parser.add_argument(
        "--product-matrix",
        type=Path,
        help="Path to product-matrix.yaml"
    )

    parser.add_argument(
        "--search",
        help="Search skills by keyword"
    )

    parser.add_argument(
        "--category",
        help="Filter skills by category"
    )

    parser.add_argument(
        "--product-type",
        help="Recommend skills for product type"
    )

    parser.add_argument(
        "--resolve-deps",
        help="Resolve dependencies for skill slug"
    )

    parser.add_argument(
        "--list-all",
        action="store_true",
        help="List all available skills"
    )

    parser.add_argument(
        "--generate-command",
        action="store_true",
        help="Generate @load command for results"
    )

    parser.add_argument(
        "--output-json",
        type=Path,
        help="Export results to JSON file"
    )

    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    # Initialize discovery engine
    discovery = SkillDiscovery(args.skills_dir, args.product_matrix)

    results = []

    # Execute requested operation
    if args.search:
        results = discovery.search_by_keyword(args.search)
        print(f"\nSearch results for '{args.search}': {len(results)} found\n")

    elif args.category:
        results = discovery.filter_by_category(args.category)
        print(f"\nSkills in category '{args.category}': {len(results)} found\n")

    elif args.product_type:
        results = discovery.recommend_for_product(args.product_type)
        print(f"\nRecommended skills for '{args.product_type}': {len(results)} found\n")

    elif args.resolve_deps:
        dep_slugs = discovery.resolve_dependencies(args.resolve_deps)
        print(f"\nDependencies for '{args.resolve_deps}':\n")
        for slug in dep_slugs:
            if slug in discovery.skills:
                print(discovery.format_skill_result(discovery.skills[slug], args.verbose))
                print()

        if args.generate_command:
            cmd = discovery.generate_load_command(dep_slugs)
            print(f"\nLoad command:\n{cmd}\n")

        sys.exit(0)

    elif args.list_all:
        results = list(discovery.skills.values())
        print(f"\nAll available skills: {len(results)}\n")

    else:
        parser.print_help()
        sys.exit(0)

    # Display results
    for skill_data in results:
        print(discovery.format_skill_result(skill_data, args.verbose))
        print()

    # Generate load command
    if args.generate_command and results:
        skill_slugs = [s["slug"] for s in results]
        cmd = discovery.generate_load_command(skill_slugs)
        print(f"\nLoad command:\n{cmd}\n")

    # Export JSON
    if args.output_json:
        output_data = {
            "count": len(results),
            "skills": results
        }
        args.output_json.write_text(json.dumps(output_data, indent=2, default=str))
        logger.info(f"Exported results to: {args.output_json}")

    sys.exit(0)


if __name__ == "__main__":
    main()
