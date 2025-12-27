"""
Pytest configuration and shared fixtures for test suite.

London School TDD approach - provides mock factories and test utilities.
"""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def repo_root():
    """Repository root path fixture"""
    return Path("/home/william/git/standards")


@pytest.fixture
def temp_repo(tmp_path):
    """Temporary repository for isolated testing"""
    # Create minimal repo structure
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "standards").mkdir()
    (tmp_path / "docs" / "guides").mkdir()
    (tmp_path / "config").mkdir()
    (tmp_path / "tests").mkdir()

    return tmp_path


@pytest.fixture
def mock_product_matrix():
    """Mock product matrix configuration"""
    return {
        "products": {
            "api": {"standards": ["CS:python", "TS:pytest", "SEC:oauth"], "nist": ["NIST-IG:base"]},
            "web-service": {"standards": ["CS:javascript", "FE:react", "SEC:*"], "nist": ["NIST-IG:base"]},
        }
    }


@pytest.fixture
def mock_audit_rules():
    """Mock audit rules configuration"""
    return {
        "exclusions": [
            ".claude/**",
            "subagents/**",
            "memory/**",
            "prompts/**",
            "reports/generated/**",
            "__pycache__/**",
            ".git/**",
        ],
        "hubs": {
            "docs/standards/**/*.md": "docs/standards/UNIFIED_STANDARDS.md",
            "docs/guides/**/*.md": "docs/guides/STANDARDS_INDEX.md",
            "docs/core/**/*.md": "docs/core/README.md",
        },
    }


@pytest.fixture
def sample_markdown_with_commands():
    """Sample markdown content with various command syntaxes"""
    return """
# Sample Documentation

## Installation

```bash
npx claude-flow@alpha mcp start
```

## Python Scripts

```bash
python3 scripts/validate.py
```

## Invalid Example (should be fixed)

```bash
npm install claude-flow
```

## Not a Command

This is just text mentioning npm, not a command.

```python
# This is Python code
command = "npm install"  # String literal, not bash
```
"""


@pytest.fixture
def sample_load_directives():
    """Sample @load directives for testing"""
    return [
        "@load product:api",
        "@load CS:python",
        "@load SEC:*",
        "@load [product:api + CS:python + TS:pytest]",
        "@load NIST-IG:full",
    ]


class MockFileSystem:
    """Mock file system for testing without actual file I/O"""

    def __init__(self, root: Path):
        self.root = root
        self.files: dict[Path, str] = {}

    def create_file(self, path: Path, content: str):
        """Create a mock file"""
        self.files[path] = content

    def read_file(self, path: Path) -> str:
        """Read a mock file"""
        return self.files.get(path, "")

    def exists(self, path: Path) -> bool:
        """Check if mock file exists"""
        return path in self.files

    def glob(self, pattern: str) -> list[Path]:
        """Mock glob operation"""
        import fnmatch

        return [path for path in self.files.keys() if fnmatch.fnmatch(str(path), pattern)]


@pytest.fixture
def mock_fs(tmp_path):
    """Mock file system fixture"""
    return MockFileSystem(tmp_path)


class CommandCapture:
    """Capture and verify command executions in tests"""

    def __init__(self):
        self.commands: list[str] = []

    def execute(self, command: str):
        """Record command execution"""
        self.commands.append(command)

    def verify_called_with(self, expected: str):
        """Verify command was called"""
        assert expected in self.commands, f"Expected command '{expected}' not found in {self.commands}"

    def verify_not_called_with(self, unexpected: str):
        """Verify command was not called"""
        assert unexpected not in self.commands, f"Unexpected command '{unexpected}' found in {self.commands}"

    def reset(self):
        """Reset captured commands"""
        self.commands.clear()


@pytest.fixture
def command_capture():
    """Command capture fixture for testing"""
    return CommandCapture()


@pytest.fixture
def isolation_mode():
    """
    Context manager for isolated test execution.

    Ensures tests don't modify actual repository files.
    """

    class IsolationContext:
        def __enter__(self):
            self.original_cwd = Path.cwd()
            self.temp_dir = tempfile.mkdtemp()
            return Path(self.temp_dir)

        def __exit__(self, exc_type, exc_val, exc_tb):
            shutil.rmtree(self.temp_dir, ignore_errors=True)

    return IsolationContext()


# Pytest configuration
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
    config.addinivalue_line("markers", "requires_repo: mark test as requiring actual repository")


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers"""
    for item in items:
        # Auto-mark integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)

        # Auto-mark unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)

        # Mark tests requiring actual repo
        if "repo_root" in item.fixturenames:
            item.add_marker(pytest.mark.requires_repo)
