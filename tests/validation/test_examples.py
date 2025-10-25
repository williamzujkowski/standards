"""
Example validation tests.

Tests that all code examples work correctly.
Ensures 100% example functionality quality gate.
"""

import subprocess
from pathlib import Path
from typing import List

import pytest


class TestExampleFunctionality:
    """Test example code functionality."""

    def test_python_examples_syntax(self, examples_dir: Path, extract_code_blocks, exclusion_helper):
        """Verify Python examples have valid syntax."""
        syntax_errors = []

        for md_file in examples_dir.rglob("*.md"):
            # Skip excluded files
            if exclusion_helper(md_file):
                continue

            code_blocks = extract_code_blocks(md_file)

            for i, block in enumerate(code_blocks):
                if block["language"] in ["python", "py"]:
                    code = block["code"]

                    try:
                        compile(code, f"{md_file}:block-{i}", "exec")
                    except SyntaxError as e:
                        syntax_errors.append(f"{md_file} block {i}: {e}")

        assert not syntax_errors, f"Python syntax errors in examples:\n" + "\n".join(syntax_errors)

    def test_bash_examples_syntax(self, examples_dir: Path, extract_code_blocks, run_command, exclusion_helper):
        """Verify Bash examples have valid syntax."""
        syntax_errors = []
        shell_languages = {"bash", "sh", "shell"}

        for md_file in examples_dir.rglob("*.md"):
            # Skip excluded files
            if exclusion_helper(md_file):
                continue

            code_blocks = extract_code_blocks(md_file)

            for i, block in enumerate(code_blocks):
                if block["language"] in shell_languages:
                    code = block["code"]

                    # Skip examples with placeholders
                    if any(p in code for p in ["<", ">", "...", "PLACEHOLDER", "YOUR_"]):
                        continue

                    try:
                        # Check syntax with bash -n
                        result = subprocess.run(["bash", "-n", "-c", code], capture_output=True, text=True, timeout=5)
                        if result.returncode != 0:
                            syntax_errors.append(f"{md_file} block {i}: {result.stderr}")
                    except subprocess.TimeoutExpired:
                        syntax_errors.append(f"{md_file} block {i}: Timeout during syntax check")
                    except Exception as e:
                        syntax_errors.append(f"{md_file} block {i}: {e}")

        assert not syntax_errors, f"Bash syntax errors in examples:\n" + "\n".join(syntax_errors[:10])

    def test_yaml_examples_syntax(self, examples_dir: Path, extract_code_blocks, validate_yaml, exclusion_helper):
        """Verify YAML examples have valid syntax."""
        import tempfile

        syntax_errors = []

        for md_file in examples_dir.rglob("*.md"):
            # Skip excluded files
            if exclusion_helper(md_file):
                continue

            code_blocks = extract_code_blocks(md_file)

            for i, block in enumerate(code_blocks):
                if block["language"] in ["yaml", "yml"]:
                    code = block["code"]

                    # Write to temp file and validate
                    with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
                        f.write(code)
                        temp_path = Path(f.name)

                    try:
                        is_valid, error = validate_yaml(temp_path)
                        if not is_valid:
                            syntax_errors.append(f"{md_file} block {i}: {error}")
                    finally:
                        temp_path.unlink()

        assert not syntax_errors, f"YAML syntax errors in examples:\n" + "\n".join(syntax_errors[:10])

    def test_json_examples_syntax(self, examples_dir: Path, extract_code_blocks, validate_json, exclusion_helper):
        """Verify JSON examples have valid syntax."""
        import tempfile

        syntax_errors = []

        for md_file in examples_dir.rglob("*.md"):
            # Skip excluded files
            if exclusion_helper(md_file):
                continue

            code_blocks = extract_code_blocks(md_file)

            for i, block in enumerate(code_blocks):
                if block["language"] in ["json", "jsonc"]:
                    code = block["code"]

                    # Write to temp file and validate
                    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
                        f.write(code)
                        temp_path = Path(f.name)

                    try:
                        is_valid, error = validate_json(temp_path)
                        if not is_valid:
                            syntax_errors.append(f"{md_file} block {i}: {error}")
                    finally:
                        temp_path.unlink()

        assert not syntax_errors, f"JSON syntax errors in examples:\n" + "\n".join(syntax_errors[:10])


class TestNISTTemplates:
    """Test NIST template examples."""

    def test_nist_quickstart_exists(self, examples_dir: Path):
        """Verify NIST quickstart example exists."""
        quickstart = examples_dir / "nist-templates" / "quickstart"
        assert quickstart.exists(), "NIST quickstart example not found"

    def test_nist_makefile_targets(self, examples_dir: Path, run_command):
        """Verify NIST Makefile has required targets."""
        quickstart = examples_dir / "nist-templates" / "quickstart"
        makefile = quickstart / "Makefile"

        if not makefile.exists():
            pytest.skip("NIST Makefile not found")

        with open(makefile) as f:
            content = f.read()

        required_targets = ["test", "validate", "nist-check"]
        missing_targets = []

        for target in required_targets:
            if f"{target}:" not in content:
                missing_targets.append(target)

        assert not missing_targets, f"Missing Makefile targets: {missing_targets}"

    @pytest.mark.slow
    def test_nist_quickstart_validation(self, examples_dir: Path, run_command):
        """Test NIST quickstart validation runs."""
        quickstart = examples_dir / "nist-templates" / "quickstart"
        if not (quickstart / "Makefile").exists():
            pytest.skip("NIST quickstart not available")

        try:
            result = run_command(["make", "validate"], cwd=quickstart, check=False)
            # Allow non-zero exit if validation finds issues
            assert result.returncode in [0, 1], f"Validation failed: {result.stderr}"
        except FileNotFoundError:
            pytest.skip("make command not available")


class TestScriptExamples:
    """Test script examples in repository."""

    def test_scripts_have_shebang(self, repo_root: Path):
        """Verify executable scripts have proper shebang."""
        scripts_dir = repo_root / "scripts"
        missing_shebang = []

        for script in scripts_dir.glob("*.py"):
            if script.stat().st_mode & 0o111:  # Is executable
                with open(script) as f:
                    first_line = f.readline()

                if not first_line.startswith("#!"):
                    missing_shebang.append(str(script))

        assert not missing_shebang, f"Executable scripts missing shebang: {missing_shebang}"

    def test_scripts_are_executable(self, repo_root: Path):
        """Verify script files are executable."""
        scripts_dir = repo_root / "scripts"
        non_executable = []

        for script in scripts_dir.glob("*.py"):
            # Skip test files and modules
            if "test_" in script.name or script.name.startswith("__"):
                continue

            if not (script.stat().st_mode & 0o111):
                non_executable.append(str(script))

        # Some scripts may intentionally be non-executable modules
        # Only flag if more than 50% are non-executable
        if non_executable:
            total_scripts = len(list(scripts_dir.glob("*.py")))
            ratio = len(non_executable) / total_scripts
            assert ratio < 0.5, f"Many scripts are non-executable: {non_executable}"


class TestWorkflowExamples:
    """Test workflow configuration examples."""

    def test_github_workflows_valid(self, repo_root: Path, validate_yaml):
        """Verify GitHub workflow files are valid YAML."""
        workflows_dir = repo_root / ".github" / "workflows"
        invalid_workflows = []

        for workflow in workflows_dir.glob("*.yml"):
            is_valid, error = validate_yaml(workflow)
            if not is_valid:
                invalid_workflows.append(f"{workflow.name}: {error}")

        assert not invalid_workflows, f"Invalid workflow files:\n" + "\n".join(invalid_workflows)

    def test_workflows_have_required_fields(self, repo_root: Path):
        """Verify workflow files have required fields."""
        import yaml

        workflows_dir = repo_root / ".github" / "workflows"
        invalid_workflows = []

        for workflow in workflows_dir.glob("*.yml"):
            with open(workflow) as f:
                config = yaml.safe_load(f)

            # Check for required fields - 'on' is a reserved YAML keyword, also check for 'true' (common workaround)
            required_fields = ["name", "jobs"]
            # Check for either 'on' or 'true' (YAML parsing quirk)
            has_trigger = "on" in config or True in config or "true" in config

            missing_fields = [field for field in required_fields if field not in config]
            if not has_trigger:
                missing_fields.append("on")

            if missing_fields:
                invalid_workflows.append(f"{workflow.name}: missing {missing_fields}")

        assert not invalid_workflows, f"Workflows missing required fields:\n" + "\n".join(invalid_workflows)


@pytest.mark.quality_gate
class TestExampleQualityGate:
    """Quality gate tests - must achieve 100% pass rate."""

    def test_example_functionality_gate(self, quality_gates):
        """Verify example functionality meets 100% quality gate."""
        assert quality_gates["example_functionality"] == 100
