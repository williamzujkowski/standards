#!/usr/bin/env python3
"""
Comprehensive test suite for skill-loader.py
Tests all 61 skills and product types with timing metrics
"""

import json
import subprocess
import sys
import time
from pathlib import Path


# Test configuration
REPO_ROOT = Path(__file__).parent.parent
SKILL_LOADER = REPO_ROOT / "scripts" / "skill-loader.py"

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


class TestResults:
    """Track test results and timing"""

    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
        self.timings = {}

    def add_pass(self, test_name: str, duration: float):
        self.passed += 1
        self.timings[test_name] = duration

    def add_fail(self, test_name: str, error: str, duration: float):
        self.failed += 1
        self.errors.append((test_name, error))
        self.timings[test_name] = duration

    def print_summary(self):
        total = self.passed + self.failed
        print(f"\n{'=' * 80}")
        print(f"{BLUE}TEST SUMMARY{RESET}")
        print(f"{'=' * 80}")
        print(f"Total Tests: {total}")
        print(f"{GREEN}Passed: {self.passed}{RESET}")
        print(f"{RED}Failed: {self.failed}{RESET}")
        print(f"Success Rate: {(self.passed / total * 100):.1f}%")

        if self.errors:
            print(f"\n{RED}FAILURES:{RESET}")
            for test_name, error in self.errors:
                print(f"  • {test_name}")
                print(f"    {error}")

        # Timing statistics
        if self.timings:
            print(f"\n{BLUE}PERFORMANCE METRICS:{RESET}")
            avg_time = sum(self.timings.values()) / len(self.timings)
            max_time = max(self.timings.values())
            min_time = min(self.timings.values())
            print(f"  Average: {avg_time:.3f}s")
            print(f"  Min: {min_time:.3f}s")
            print(f"  Max: {max_time:.3f}s")


def run_command(cmd: list[str], timeout: int = 10) -> tuple[bool, str, float]:
    """Run a command and return success status, output, and duration"""
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=REPO_ROOT,
        )
        duration = time.time() - start_time
        success = result.returncode == 0
        output = result.stdout + result.stderr
        return success, output, duration
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return False, f"Timeout after {timeout}s", duration
    except Exception as e:
        duration = time.time() - start_time
        return False, str(e), duration


def test_basic_individual_skills(results: TestResults):
    """Test loading individual skills"""
    print(f"\n{BLUE}TEST 1: Basic Individual Skill Loading{RESET}")

    test_skills = [
        "coding-standards/python",
        "security/api-security",
        "testing/unit-testing",
        "frontend/react",
        "database/sql",
    ]

    for skill in test_skills:
        test_name = f"load skill:{skill}"
        cmd = [sys.executable, str(SKILL_LOADER), "load", f"skill:{skill}"]
        success, output, duration = run_command(cmd)

        if success and "Loaded" in output:
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def test_product_types(results: TestResults):
    """Test all product types from product-matrix.yaml"""
    print(f"\n{BLUE}TEST 2: Product Type Loading{RESET}")

    product_types = [
        "api",
        "web-service",
        "frontend-web",
        "mobile",
        "data-pipeline",
        "ml-service",
        "cli",
        "infra-module",
        "documentation-site",
        "compliance-artifacts",
    ]

    for product in product_types:
        test_name = f"load product:{product}"
        cmd = [sys.executable, str(SKILL_LOADER), "load", f"product:{product}"]
        success, output, duration = run_command(cmd)

        if success:
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def test_wildcard_expansion(results: TestResults):
    """Test wildcard pattern expansion"""
    print(f"\n{BLUE}TEST 3: Wildcard Expansion{RESET}")

    wildcards = [
        "coding-standards/*",
        "security/*",
        "testing/*",
    ]

    for wildcard in wildcards:
        test_name = f"load skill:{wildcard}"
        cmd = [sys.executable, str(SKILL_LOADER), "load", f"skill:{wildcard}"]
        success, output, duration = run_command(cmd)

        # Wildcards should resolve to multiple skills
        if success and ("Loaded" in output or "No skills" in output):
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def test_error_handling(results: TestResults):
    """Test error handling for invalid inputs"""
    print(f"\n{BLUE}TEST 4: Error Handling{RESET}")

    invalid_inputs = [
        ("skill:nonexistent", "nonexistent skill"),
        ("product:invalid", "invalid product"),
        ("skill:invalid/path/too/deep", "invalid path"),
    ]

    for input_str, description in invalid_inputs:
        test_name = f"error handling: {description}"
        cmd = [sys.executable, str(SKILL_LOADER), "load", input_str]
        success, output, duration = run_command(cmd)

        # Should fail gracefully with error message
        if not success or "Could not load" in output or "Unknown" in output:
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name} - Expected error but succeeded")
            results.add_fail(test_name, "Should have failed gracefully", duration)


def test_all_skills_sequential(results: TestResults):
    """Test loading all 61 skills sequentially"""
    print(f"\n{BLUE}TEST 5: All Skills Sequential Load{RESET}")

    # Get list of all skills
    cmd = [sys.executable, str(SKILL_LOADER), "list", "--format", "json"]
    success, output, duration = run_command(cmd)

    if not success:
        results.add_fail("list all skills", output[:200], duration)
        return

    try:
        skills_data = json.loads(output)
        all_skills = skills_data.get("skills", [])
    except json.JSONDecodeError as e:
        results.add_fail("parse skills list", str(e), duration)
        return

    print(f"  Found {len(all_skills)} skills to test")

    # Test each skill
    failed_skills = []
    for skill in all_skills:
        skill_name = skill["name"]
        cmd = [sys.executable, str(SKILL_LOADER), "load", skill_name]
        success, output, duration = run_command(cmd)

        if not success or "Could not load" in output:
            failed_skills.append((skill_name, output[:100]))

    test_name = "sequential load all skills"
    if not failed_skills:
        print(f"  {GREEN}✓{RESET} All {len(all_skills)} skills loaded successfully")
        results.add_pass(test_name, duration)
    else:
        print(f"  {RED}✗{RESET} {len(failed_skills)} skills failed to load")
        error_msg = f"{len(failed_skills)} failures: {', '.join([s[0] for s in failed_skills[:5]])}"
        results.add_fail(test_name, error_msg, duration)


def test_skill_validation(results: TestResults):
    """Test skill validation functionality"""
    print(f"\n{BLUE}TEST 6: Skill Validation{RESET}")

    test_skills = [
        "coding-standards",
        "security",
        "testing",
    ]

    for skill in test_skills:
        test_name = f"validate {skill}"
        cmd = [sys.executable, str(SKILL_LOADER), "validate", skill]
        success, output, duration = run_command(cmd)

        if success and "validated" in output.lower():
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def test_json_output(results: TestResults):
    """Test JSON output format"""
    print(f"\n{BLUE}TEST 7: JSON Output Format{RESET}")

    test_name = "JSON output"
    cmd = [sys.executable, str(SKILL_LOADER), "load", "coding-standards", "--format", "json"]
    success, output, duration = run_command(cmd)

    if success:
        try:
            json.loads(output)
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        except json.JSONDecodeError as e:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, f"Invalid JSON: {e}", duration)
    else:
        print(f"  {RED}✗{RESET} {test_name}")
        results.add_fail(test_name, output[:200], duration)


def test_skill_discovery(results: TestResults):
    """Test skill discovery functionality"""
    print(f"\n{BLUE}TEST 8: Skill Discovery{RESET}")

    test_cases = [
        ("--keyword", "testing", "keyword search"),
        ("--category", "security", "category filter"),
    ]

    for flag, value, description in test_cases:
        test_name = f"discover {description}"
        cmd = [sys.executable, str(SKILL_LOADER), "discover", flag, value]
        success, output, duration = run_command(cmd)

        if success and "Found" in output:
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def test_skill_info(results: TestResults):
    """Test skill info command"""
    print(f"\n{BLUE}TEST 9: Skill Info{RESET}")

    test_skills = ["coding-standards", "security", "testing"]

    for skill in test_skills:
        test_name = f"info {skill}"
        cmd = [sys.executable, str(SKILL_LOADER), "info", skill]
        success, output, duration = run_command(cmd)

        if success and "Description:" in output:
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def test_recommend_command(results: TestResults):
    """Test skill recommendation"""
    print(f"\n{BLUE}TEST 10: Skill Recommendations{RESET}")

    product_types = ["api", "web-service", "frontend-web"]

    for product in product_types:
        test_name = f"recommend {product}"
        cmd = [sys.executable, str(SKILL_LOADER), "recommend", "--product-type", product]
        success, output, duration = run_command(cmd)

        if success and "Recommended" in output:
            print(f"  {GREEN}✓{RESET} {test_name} ({duration:.3f}s)")
            results.add_pass(test_name, duration)
        else:
            print(f"  {RED}✗{RESET} {test_name}")
            results.add_fail(test_name, output[:200], duration)


def main():
    """Run all tests"""
    print(f"{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}SKILL-LOADER.PY COMPREHENSIVE TEST SUITE{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}")
    print(f"Repository: {REPO_ROOT}")
    print(f"Script: {SKILL_LOADER}")

    if not SKILL_LOADER.exists():
        print(f"{RED}ERROR: skill-loader.py not found at {SKILL_LOADER}{RESET}")
        sys.exit(1)

    results = TestResults()

    # Run all test suites
    test_basic_individual_skills(results)
    test_product_types(results)
    test_wildcard_expansion(results)
    test_error_handling(results)
    test_all_skills_sequential(results)
    test_skill_validation(results)
    test_json_output(results)
    test_skill_discovery(results)
    test_skill_info(results)
    test_recommend_command(results)

    # Print summary
    results.print_summary()

    # Exit with appropriate code
    sys.exit(0 if results.failed == 0 else 1)


if __name__ == "__main__":
    main()
