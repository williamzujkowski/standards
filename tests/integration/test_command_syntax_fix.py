"""
Test suite for command syntax validation and npm/npx detection.

This test suite follows London School TDD - focusing on behavior verification
and interaction testing for command syntax validation across documentation.

RED PHASE: These tests will FAIL until command syntax is fixed.
"""

import pytest
from pathlib import Path
from typing import List, Dict
import re


class MockDocumentScanner:
    """Mock for document scanning behavior"""

    def scan_for_commands(self, path: Path) -> List[Dict[str, str]]:
        """Mock method - will be replaced with real implementation"""
        raise NotImplementedError("Implementation required")


class MockCommandValidator:
    """Mock for command validation behavior"""

    def validate_syntax(self, command: str) -> Dict[str, bool]:
        """Mock method - will be replaced with real implementation"""
        raise NotImplementedError("Implementation required")


class TestCommandSyntaxDetection:
    """Test detection of npm/npx command usage in documentation"""

    @pytest.fixture
    def mock_scanner(self):
        """Fixture for document scanner mock"""
        return MockDocumentScanner()

    @pytest.fixture
    def mock_validator(self):
        """Fixture for command validator mock"""
        return MockCommandValidator()

    def test_detects_npm_in_claude_md(self, mock_scanner):
        """Should detect npm commands in CLAUDE.md"""
        # GIVEN: CLAUDE.md contains npm commands
        claude_md = Path("/home/william/git/standards/CLAUDE.md")

        # WHEN: Scanning for commands
        commands = mock_scanner.scan_for_commands(claude_md)

        # THEN: Should find npm/npx commands
        npm_commands = [cmd for cmd in commands if "npm" in cmd["command"] or "npx" in cmd["command"]]
        assert len(npm_commands) > 0, "Should detect npm/npx commands in CLAUDE.md"
        assert any("claude-flow" in cmd["command"] for cmd in npm_commands), "Should detect claude-flow npm/npx usage"

    def test_validates_bash_fence_context(self, mock_scanner):
        """Should verify commands are in bash code fences"""
        # GIVEN: Commands in documentation
        doc_path = Path("/home/william/git/standards/CLAUDE.md")

        # WHEN: Scanning commands
        commands = mock_scanner.scan_for_commands(doc_path)

        # THEN: All commands should be in bash fences
        for cmd in commands:
            assert cmd.get("fence_type") in [
                "bash",
                "sh",
                "shell",
            ], f"Command '{cmd['command']}' should be in bash fence, found: {cmd.get('fence_type')}"

    def test_no_npm_in_python_code(self, mock_scanner):
        """Should not flag npm in Python string literals"""
        # GIVEN: Python code containing npm in strings
        test_content = """
        ```python
        command = "npm install"  # This is a string, not a command
        ```
        """

        # WHEN: Scanning content
        # Mock should differentiate between bash commands and Python strings

        # THEN: Should not report as bash command syntax issue
        # This tests the scanner's ability to understand code context
        pass  # Will implement with actual scanner

    def test_detects_command_in_markdown_callouts(self, mock_scanner):
        """Should detect commands in blockquotes and callouts"""
        # GIVEN: Commands in various markdown contexts
        doc_path = Path("/home/william/git/standards/docs/guides/KICKSTART_PROMPT.md")

        # WHEN: Scanning all contexts
        commands = mock_scanner.scan_for_commands(doc_path)

        # THEN: Should find commands in all valid contexts
        assert len(commands) > 0, "Should detect commands in various markdown contexts"


class TestCommandSyntaxValidation:
    """Test validation of command syntax correctness"""

    @pytest.fixture
    def validator(self):
        return MockCommandValidator()

    def test_rejects_npm_without_context(self, validator):
        """Should flag bare npm commands as invalid"""
        # GIVEN: Bare npm command
        command = "npm install claude-flow"

        # WHEN: Validating syntax
        result = validator.validate_syntax(command)

        # THEN: Should be invalid (needs npx or package manager context)
        assert result["valid"] is False, "Bare npm install should be flagged"
        assert "npm" in result["issues"], "Should explain npm issue"

    def test_accepts_npx_claude_flow(self, validator):
        """Should accept npx claude-flow commands"""
        # GIVEN: Valid npx command
        command = "npx claude-flow@alpha mcp start"

        # WHEN: Validating syntax
        result = validator.validate_syntax(command)

        # THEN: Should be valid
        assert result["valid"] is True, "npx claude-flow should be valid"

    def test_accepts_python_script_calls(self, validator):
        """Should accept python3 script calls"""
        # GIVEN: Python script command
        command = "python3 scripts/generate-audit-reports.py"

        # WHEN: Validating syntax
        result = validator.validate_syntax(command)

        # THEN: Should be valid
        assert result["valid"] is True, "Python script calls should be valid"

    def test_flags_mcp_add_syntax(self, validator):
        """Should validate claude mcp add syntax"""
        # GIVEN: MCP add command
        command = "claude mcp add claude-flow npx claude-flow@alpha mcp start"

        # WHEN: Validating syntax
        result = validator.validate_syntax(command)

        # THEN: Should be valid with proper structure
        assert result["valid"] is True, "MCP add command should be valid"
        assert result.get("command_type") == "mcp_config", "Should identify as MCP config"


class TestCommandSyntaxFix:
    """Test automated fixing of command syntax issues"""

    def test_replaces_npm_with_npx(self):
        """Should replace npm with npx for claude-flow"""
        # GIVEN: Document with npm claude-flow
        original = "```bash\nnpm install claude-flow@alpha\n```"
        expected = "```bash\nnpx claude-flow@alpha mcp start\n```"

        # WHEN: Applying fix
        # Implementation will handle this transformation

        # THEN: Should convert to npx usage
        # assert fixed == expected
        pass  # Will implement with actual fixer

    def test_preserves_valid_commands(self):
        """Should not modify valid commands"""
        # GIVEN: Valid command
        original = "```bash\npython3 scripts/validate.py\n```"

        # WHEN: Applying fix
        # fixed = fixer.fix_syntax(original)

        # THEN: Should remain unchanged
        # assert fixed == original
        pass  # Will implement with actual fixer

    def test_handles_multiline_commands(self):
        """Should handle commands with line continuations"""
        # GIVEN: Multi-line command
        original = """```bash
npm install \\
  claude-flow@alpha \\
  --save
```"""

        # WHEN: Applying fix
        # Should handle \ continuations

        # THEN: Should properly transform entire command
        pass  # Will implement with actual fixer


class TestCommandSyntaxReport:
    """Test reporting of command syntax issues"""

    def test_generates_issue_report(self):
        """Should generate structured report of issues"""
        # GIVEN: Multiple files with issues

        # WHEN: Running full scan
        # report = scanner.generate_report()

        # THEN: Should have structured output
        # assert 'files_scanned' in report
        # assert 'issues_found' in report
        # assert 'fixes_available' in report
        pass  # Will implement with actual scanner

    def test_groups_issues_by_type(self):
        """Should group issues by command type"""
        # GIVEN: Various command issues

        # WHEN: Generating report
        # report = scanner.generate_report()

        # THEN: Should group by issue type
        # assert 'npm_usage' in report['issue_types']
        # assert 'invalid_syntax' in report['issue_types']
        pass  # Will implement with actual scanner


# Integration test that will FAIL until fixes are applied
class TestCommandSyntaxIntegration:
    """Integration tests for command syntax across repository"""

    def test_no_npm_in_claude_md(self):
        """CLAUDE.md should not contain npm install commands"""
        claude_md = Path("/home/william/git/standards/CLAUDE.md")
        content = claude_md.read_text()

        # Should not find npm install (except in explanatory context)
        npm_pattern = r"```(?:bash|sh|shell)\s+npm\s+install"
        matches = re.findall(npm_pattern, content, re.MULTILINE)

        assert len(matches) == 0, f"Found {len(matches)} npm install commands in CLAUDE.md bash fences"

    def test_npx_usage_consistent(self):
        """All claude-flow usage should be via npx"""
        claude_md = Path("/home/william/git/standards/CLAUDE.md")
        content = claude_md.read_text()

        # Find all claude-flow references in bash fences
        bash_fence_pattern = r"```(?:bash|sh|shell)(.*?)```"
        bash_sections = re.findall(bash_fence_pattern, content, re.DOTALL)

        for section in bash_sections:
            if "claude-flow" in section:
                # Should use npx, not npm
                assert "npm install claude-flow" not in section, "claude-flow should be used via npx, not npm install"

    def test_all_commands_in_fences(self):
        """All executable commands should be in code fences"""
        claude_md = Path("/home/william/git/standards/CLAUDE.md")
        content = claude_md.read_text()

        # Look for command patterns outside fences
        # This is a simplified check - real implementation will be more sophisticated
        lines = content.split("\n")
        in_fence = False
        fence_type = None

        for line in lines:
            if line.strip().startswith("```"):
                if in_fence:
                    in_fence = False
                    fence_type = None
                else:
                    in_fence = True
                    fence_type = line.strip()[3:].split()[0] if len(line.strip()) > 3 else None
            elif not in_fence and line.strip().startswith(("python3 ", "npx ", "npm ")):
                # Found command outside fence
                pytest.fail(f"Command outside code fence: {line.strip()}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
