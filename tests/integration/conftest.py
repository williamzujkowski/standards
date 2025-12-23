"""
Pytest configuration for integration tests.

Provides shared fixtures and configuration for router validation tests.
"""

from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def repo_root():
    """Get repository root directory."""
    return Path(__file__).resolve().parents[2]


@pytest.fixture(scope="session")
def config_dir(repo_root):
    """Get config directory."""
    return repo_root / "config"


@pytest.fixture(scope="session")
def scripts_dir(repo_root):
    """Get scripts directory."""
    return repo_root / "scripts"


@pytest.fixture(scope="session")
def skills_dir(repo_root):
    """Get skills directory."""
    return repo_root / "skills"


@pytest.fixture(scope="session")
def docs_dir(repo_root):
    """Get docs directory."""
    return repo_root / "docs"
