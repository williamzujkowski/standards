#!/usr/bin/env python3
"""
Skill Loader CLI - Load and manage development skills

This CLI tool provides skill discovery, loading, and management capabilities
for the standards repository's Skills-based architecture.

Usage:
    skill-loader.py discover --keyword "testing"
    skill-loader.py load python --level 2
    skill-loader.py load [python,typescript] --level 2
    skill-loader.py load product:api
    skill-loader.py list --category all
    skill-loader.py info python
    skill-loader.py validate python
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

import yaml


@dataclass
class Skill:
    """Represents a skill with metadata"""
    name: str
    path: Path
    description: str
    category: str
    level: int = 1
    related: List[str] = None

    def __post_init__(self):
        if self.related is None:
            self.related = []


@dataclass
class SkillLoader:
    """Main skill loader class"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.skills_dir = repo_root / "skills"
        self.config_dir = repo_root / "config"
        self.legacy_mappings = self._load_legacy_mappings()
        self.product_matrix = self._load_product_matrix()
        self.skills_cache: Dict[str, Skill] = {}
        self._discover_skills()

    def _load_legacy_mappings(self) -> Dict:
        """Load legacy pattern mappings"""
        mappings_file = self.skills_dir / "legacy-bridge" / "resources" / "legacy-mappings.yaml"
        if mappings_file.exists():
            with open(mappings_file) as f:
                return yaml.safe_load(f)
        return {}

    def _load_product_matrix(self) -> Dict:
        """Load product matrix configuration"""
        matrix_file = self.config_dir / "product-matrix.yaml"
        if matrix_file.exists():
            with open(matrix_file) as f:
                return yaml.safe_load(f)
        return {}

    def _discover_skills(self):
        """Discover all available skills in the skills directory"""
        if not self.skills_dir.exists():
            print(f"⚠️  Skills directory not found: {self.skills_dir}")
            return

        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue

            skill_file = skill_dir / "SKILL.md"
            if skill_file.exists():
                skill = self._parse_skill_file(skill_file)
                if skill:
                    self.skills_cache[skill.name] = skill

    def _parse_skill_file(self, skill_file: Path) -> Optional[Skill]:
        """Parse a SKILL.md file and extract metadata"""
        try:
            with open(skill_file) as f:
                content = f.read()

            # Extract YAML frontmatter
            frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not frontmatter_match:
                return None

            metadata = yaml.safe_load(frontmatter_match.group(1))

            skill_name = metadata.get('name', skill_file.parent.name)
            description = metadata.get('description', 'No description available')

            # Determine category from path
            category = skill_file.parent.name

            return Skill(
                name=skill_name,
                path=skill_file.parent,
                description=description,
                category=category,
                related=metadata.get('related', [])
            )
        except Exception as e:
            print(f"⚠️  Error parsing {skill_file}: {e}", file=sys.stderr)
            return None

    def discover(self, keyword: Optional[str] = None, category: Optional[str] = None) -> List[Skill]:
        """Discover skills by keyword or category"""
        results = []

        for skill in self.skills_cache.values():
            # Filter by keyword if provided
            if keyword:
                if keyword.lower() not in skill.name.lower() and \
                   keyword.lower() not in skill.description.lower():
                    continue

            # Filter by category if provided
            if category and category != 'all':
                if skill.category != category:
                    continue

            results.append(skill)

        return sorted(results, key=lambda s: s.name)

    def recommend(self, product_type: str) -> List[Skill]:
        """Recommend skills for a product type"""
        # Use legacy mappings to determine recommended skills
        product_mappings = self.legacy_mappings.get('product_mappings', {})

        if product_type not in product_mappings:
            print(f"⚠️  Unknown product type: {product_type}")
            print(f"Available types: {', '.join(product_mappings.keys())}")
            return []

        product_config = product_mappings[product_type]
        skill_names = product_config.get('skills', [])

        # Resolve skill names to skill objects
        recommended = []
        for skill_name in skill_names:
            # Extract base skill name (e.g., 'coding-standards/python' -> 'coding-standards')
            base_name = skill_name.split('/')[0]
            if base_name in self.skills_cache:
                skill = self.skills_cache[base_name]
                recommended.append(skill)

        return recommended

    def load_skill(self, skill_name: str, level: int = 2) -> Optional[Skill]:
        """Load a specific skill at the given level"""
        # Handle composite skill names (e.g., 'coding-standards/python')
        base_name = skill_name.split('/')[0]

        if base_name not in self.skills_cache:
            # Try legacy pattern translation
            return self._translate_legacy_pattern(skill_name)

        skill = self.skills_cache[base_name]
        skill.level = level
        return skill

    def _translate_legacy_pattern(self, pattern: str) -> Optional[Skill]:
        """Translate a legacy @load pattern to skills"""
        # Handle product types
        if pattern.startswith('product:'):
            product_type = pattern.replace('product:', '')
            skills = self.recommend(product_type)
            return skills[0] if skills else None

        # Handle standard codes (CS:, TS:, SEC:, etc.)
        code_pattern = r'([A-Z]+):(.*)'
        match = re.match(code_pattern, pattern)
        if match:
            code_type, code_value = match.groups()

            # Map to legacy mappings
            mapping_key = f"{code_type.lower()}_mappings"
            mappings = self.legacy_mappings.get(mapping_key, {})

            if code_value in mappings:
                skill_path = mappings[code_value].get('skill', '')
                base_name = skill_path.split('/')[0]
                if base_name in self.skills_cache:
                    return self.skills_cache[base_name]

        return None

    def list_skills(self, category: str = 'all') -> List[Skill]:
        """List all skills, optionally filtered by category"""
        return self.discover(category=category)

    def get_skill_info(self, skill_name: str) -> Optional[Skill]:
        """Get detailed information about a skill"""
        base_name = skill_name.split('/')[0]
        return self.skills_cache.get(base_name)

    def validate_skill(self, skill_name: str) -> bool:
        """Validate that a skill exists and is properly formatted"""
        skill = self.get_skill_info(skill_name)
        if not skill:
            print(f"❌ Skill not found: {skill_name}")
            return False

        skill_file = skill.path / "SKILL.md"
        if not skill_file.exists():
            print(f"❌ SKILL.md not found: {skill_file}")
            return False

        # Check for required sections
        with open(skill_file) as f:
            content = f.read()

        required_sections = [
            '## Overview',
            '## When to Use This Skill',
            '## Core Instructions'
        ]

        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            print(f"⚠️  Missing required sections in {skill_name}:")
            for section in missing_sections:
                print(f"   - {section}")
            return False

        print(f"✅ Skill validated: {skill_name}")
        return True


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Skill Loader CLI - Load and manage development skills',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Discover skills
  %(prog)s discover --keyword testing
  %(prog)s discover --category security

  # Load skills
  %(prog)s load python --level 2
  %(prog)s load [python,typescript] --level 2
  %(prog)s load product:api

  # List and info
  %(prog)s list --category all
  %(prog)s info python
  %(prog)s validate python

  # Recommendations
  %(prog)s recommend --product-type api
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='Command to run')

    # Discover command
    discover_parser = subparsers.add_parser('discover', help='Discover skills by keyword or category')
    discover_parser.add_argument('--keyword', help='Search keyword')
    discover_parser.add_argument('--category', help='Filter by category')

    # Load command
    load_parser = subparsers.add_parser('load', help='Load specific skills')
    load_parser.add_argument('skills', help='Skill name(s) to load (comma-separated or [a,b] format)')
    load_parser.add_argument('--level', type=int, default=2, help='Skill level to load (1-3)')
    load_parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')

    # List command
    list_parser = subparsers.add_parser('list', help='List all skills')
    list_parser.add_argument('--category', default='all', help='Filter by category')
    list_parser.add_argument('--format', choices=['text', 'json'], default='text', help='Output format')

    # Info command
    info_parser = subparsers.add_parser('info', help='Get detailed skill information')
    info_parser.add_argument('skill', help='Skill name')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate skill structure')
    validate_parser.add_argument('skill', help='Skill name')

    # Recommend command
    recommend_parser = subparsers.add_parser('recommend', help='Recommend skills for product type')
    recommend_parser.add_argument('--product-type', required=True, help='Product type (api, web-service, etc.)')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Initialize loader
    repo_root = Path(__file__).parent.parent
    loader = SkillLoader(repo_root)

    # Execute command
    if args.command == 'discover':
        skills = loader.discover(keyword=args.keyword, category=args.category)
        if not skills:
            print("No skills found matching criteria")
            return 1

        print(f"\n📚 Found {len(skills)} skill(s):\n")
        for skill in skills:
            print(f"  • {skill.name}")
            print(f"    {skill.description}")
            print(f"    Category: {skill.category}")
            print()

    elif args.command == 'load':
        # Parse skill names (handle [a,b] or a,b format)
        skills_input = args.skills.strip('[]')
        skill_names = [s.strip() for s in skills_input.split(',')]

        loaded_skills = []
        for skill_name in skill_names:
            skill = loader.load_skill(skill_name, level=args.level)
            if skill:
                loaded_skills.append(skill)
            else:
                print(f"⚠️  Could not load skill: {skill_name}", file=sys.stderr)

        if not loaded_skills:
            print("❌ No skills loaded", file=sys.stderr)
            return 1

        if args.format == 'json':
            output = {
                'skills': [
                    {
                        'name': s.name,
                        'path': str(s.path),
                        'description': s.description,
                        'level': s.level
                    }
                    for s in loaded_skills
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            print(f"\n✅ Loaded {len(loaded_skills)} skill(s) at level {args.level}:\n")
            for skill in loaded_skills:
                print(f"  • {skill.name}")
                print(f"    {skill.description}")
                print(f"    Path: {skill.path}")
                print()

    elif args.command == 'list':
        skills = loader.list_skills(category=args.category)

        if args.format == 'json':
            output = {
                'skills': [
                    {
                        'name': s.name,
                        'category': s.category,
                        'description': s.description
                    }
                    for s in skills
                ]
            }
            print(json.dumps(output, indent=2))
        else:
            # Group by category
            by_category = {}
            for skill in skills:
                if skill.category not in by_category:
                    by_category[skill.category] = []
                by_category[skill.category].append(skill)

            print(f"\n📚 Available Skills ({len(skills)} total):\n")
            for category, category_skills in sorted(by_category.items()):
                print(f"  {category}:")
                for skill in category_skills:
                    print(f"    • {skill.name}")
                print()

    elif args.command == 'info':
        skill = loader.get_skill_info(args.skill)
        if not skill:
            print(f"❌ Skill not found: {args.skill}", file=sys.stderr)
            return 1

        print(f"\n📖 Skill Information: {skill.name}\n")
        print(f"Description: {skill.description}")
        print(f"Category: {skill.category}")
        print(f"Path: {skill.path}")
        if skill.related:
            print(f"Related: {', '.join(skill.related)}")
        print()

    elif args.command == 'validate':
        success = loader.validate_skill(args.skill)
        return 0 if success else 1

    elif args.command == 'recommend':
        skills = loader.recommend(args.product_type)
        if not skills:
            return 1

        print(f"\n💡 Recommended skills for {args.product_type}:\n")
        for skill in skills:
            print(f"  • {skill.name}")
            print(f"    {skill.description}")
        print(f"\nTotal: {len(skills)} skills")
        print(f"\nTo load: skill-loader.py load product:{args.product_type}")
        print()

    return 0


if __name__ == '__main__':
    sys.exit(main())
