#!/usr/bin/env python3
"""
Python module wrapper for skill-loader.py

This wrapper allows tests to import skill-loader.py as a Python module,
despite the hyphenated filename which normally cannot be imported directly.

Usage:
    from skill_loader import Skill, SkillLoader
"""

import importlib.util
import sys
from pathlib import Path

# Load the hyphenated script as a module
script_path = Path(__file__).parent / "skill-loader.py"
spec = importlib.util.spec_from_file_location("_skill_loader_internal", script_path)
_module = importlib.util.module_from_spec(spec)
sys.modules["_skill_loader_internal"] = _module
spec.loader.exec_module(_module)

# Re-export the main classes and functions
Skill = _module.Skill
SkillLoader = _module.SkillLoader

# Re-export any other public symbols
__all__ = ["Skill", "SkillLoader"]
