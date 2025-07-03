# Comprehensive Testing Manifesto for LLM Coding Projects

**Version:** 1.0.0
**Last Updated:** 2025-01-13
**Status:** Active
**Standard Code:** TS

---

## Table of Contents

1. [Core Testing Principles](#core-testing-principles)
   - [Hypothesis Tests for Behavior Validation](#1-hypothesis-tests-for-behavior-validation)
   - [Regression Tests for Known Fail States](#2-regression-tests-for-known-fail-states)
   - [Benchmark Tests with SLA Enforcement](#3-benchmark-tests-with-sla-enforcement)
   - [Grammatical Evolution for Fuzzing](#4-grammatical-evolution-ge-for-fuzzing--edge-discovery)
   - [Structured Logs for Agent Feedback](#5-structured-logs-for-agent-feedback)
2. [Quality Assurance Standards](#quality-assurance-standards)
   - [Code Coverage Requirements](#6-code-coverage-requirements)
   - [Static Analysis Rules](#7-static-analysis-rules)
   - [Contract Testing Framework](#8-contract-testing-framework)
   - [Mutation Testing Guidelines](#9-mutation-testing-guidelines)
   - [Property-Based Testing Framework](#10-property-based-testing-framework)
3. [Security and Resilience](#security-and-resilience)
   - [Security Testing Guidelines](#11-security-testing-guidelines)
   - [Resilience Testing Framework](#12-resilience-testing-framework)
4. [Documentation and Integration](#documentation-and-integration)
   - [Documentation Testing](#13-documentation-testing)
   - [Integration Testing Patterns](#14-integration-testing-patterns)
   - [Testability Guidelines](#15-testability-guidelines)

## Overview

This standard provides comprehensive guidelines and best practices for the subject area.
It aims to ensure consistency, quality, and maintainability across all related implementations.

## Core Testing Principles

<!-- @nist-controls: [si-10, si-11, au-2, au-3] -->

### 1. Hypothesis Tests for Behavior Validation

```text
When implementing a new feature or function, create hypothesis tests that
validate expected behaviors:

1. For each function, identify the core hypothesis of what it should accomplish
2. Write tests that:
   - Define clear expectations ("Given X, the function should return Y")
   - Test both positive and negative cases
   - Include boundary conditions
   - Verify error handling behaviors
3. Express these tests in the appropriate testing framework (e.g., pytest, Jest)
4. Include descriptive test names that document the behavior being validated

Example structure:
```python
def test_user_authentication_valid_credentials():
    """HYPOTHESIS: Given valid credentials, authentication should succeed.
    @nist ia-2 "Test authentication mechanism"
    @nist si-10 "Validate input credentials"
    """
    # Arrange
    valid_username = "test_user"
    valid_password = "correct_password"

    # Act
    result = authenticate_user(valid_username, valid_password)

    # Assert
    assert result.success is True
    assert result.error_message is None
```

### 2. Regression Tests for Known Fail States

```text
When fixing bugs or addressing edge cases, always create regression tests:

1. For each bug fix, create a test that:
   - Documents the original issue clearly in the test description
   - Recreates the exact conditions that caused the failure
   - Verifies the fix works as expected
   - Includes issue/ticket references for context
2. Maintain a dedicated regression test suite that runs with every build
3. Label regression tests appropriately for traceability
4. Include timestamps and version information where relevant

Example structure:
```python
def test_calculation_with_zero_division_protection():
    """REGRESSION: Bug #1234 - Division by zero crash in calculation module.
    @nist si-11 "Test error handling"
    @nist si-10 "Input validation testing"

    This test ensures that when a divisor of zero is provided, the function
    returns a default value rather than raising an exception.
    """
    # Arrange
    input_value = 10
    divisor = 0
    expected_result = None  # Our fix returns None instead of raising ZeroDivisionError

    # Act
    result = safe_divide(input_value, divisor)

    # Assert
    assert result == expected_result
```

### 3. Benchmark Tests with SLA Enforcement

```text
Implement benchmark tests that enforce Service Level Agreements (SLAs):

1. Define clear performance metrics for your system:
   - Response time / latency (milliseconds)
   - Throughput (requests per second)
   - Resource usage (memory, CPU)
   - Error rates
2. Create benchmark tests that:
   - Establish baseline performance expectations
   - Run consistently in controlled environments
   - Measure against defined thresholds
   - Alert on SLA violations
3. Include both average and percentile measurements (p95, p99)
4. Document the testing environment and conditions

Example structure:
```python
def test_api_response_time_sla():
    """BENCHMARK: API must respond within 200ms for 95% of requests.

    SLA Requirements:
    - p95 response time: < 200ms
    - p99 response time: < 500ms
    - Error rate: < 0.1%
    """
    # Arrange
    num_requests = 1000
    endpoint = "/api/users"

    # Act
    response_times = []
    errors = 0
    for _ in range(num_requests):
        start_time = time.time()
        try:
            response = client.get(endpoint)
            if response.status_code >= 400:
                errors += 1
        except Exception:
            errors += 1
        finally:
            response_times.append((time.time() - start_time) * 1000)  # Convert to ms

    # Assert
    error_rate = errors / num_requests
    p95 = numpy.percentile(response_times, 95)
    p99 = numpy.percentile(response_times, 99)

    assert p95 < 200, f"95th percentile response time {p95}ms exceeds SLA of 200ms"
    assert p99 < 500, f"99th percentile response time {p99}ms exceeds SLA of 500ms"
    assert error_rate < 0.001, f"Error rate {error_rate} exceeds SLA of 0.1%"
```

### 4. Grammatical Evolution (GE) for Fuzzing + Edge Discovery

```text
Implement Grammatical Evolution (GE) for advanced fuzzing and edge case
discovery:

1. Define a grammar that represents valid inputs for your system:
   - Create BNF (Backus-Naur Form) or similar grammar definition
   - Include all possible input variations, formats, and structures
   - Define mutation operations that preserve grammatical correctness
2. Implement an evolutionary algorithm that:
   - Generates test cases based on the grammar
   - Evolves test cases using fitness functions
   - Prioritizes edge cases and unexpected inputs
   - Tracks code coverage to focus on unexplored paths
3. Log and analyze failures to identify patterns
4. Automatically add discovered edge cases to regression tests

Example structure:
```python
def test_with_grammatical_evolution():
    """FUZZING: Use GE to discover edge cases in the input parser.

    This test uses grammatical evolution to generate various inputs
    that conform to our API grammar but might trigger unexpected behaviors.
    """
    # Define grammar for API requests
    grammar = {
        'start': ['<request>'],
        'request': ['{"command": "<command>", "params": <params>}'],
        'command': ['get', 'set', 'update', 'delete', '<random_string>'],
        'params': ['<simple_param>', '<complex_param>', '<nested_param>', '<malformed_param>'],
        # ... additional grammar rules
    }

    # Configure GE parameters
    max_generations = 50
    population_size = 100
    mutation_rate = 0.1

    # Run GE-based fuzzing
    fuzzer = GrammaticalEvolutionFuzzer(grammar=grammar,
                                      coverage_tracker=CoverageTracker(),
                                      target_function=api_request_handler)

    results = fuzzer.run(max_generations, population_size, mutation_rate)

    # Analyze results
    edge_cases = results.filter(lambda r: r.status == 'failure')

    # Assert
    assert not edge_cases.has_critical_failures(), \
        f"Critical failures found: {edge_cases.critical_failures}"

        # Add discovered edge cases to regression suite
    for case in edge_cases:
        add_to_regression_suite(case)
```

### 5. Structured Logs for Agent Feedback

```text
Implement structured logging for comprehensive agent feedback:

1. Design a structured logging system that captures:
   - Input/output pairs for each agent operation
   - Decision points with considered alternatives
   - Confidence scores for predictions or responses
   - Time and resource utilization metrics
   - Any deviation from expected behavior
2. Use a consistent JSON or similar structured format
3. Include correlation IDs to track actions across system components
4. Implement log levels that enable filtering for different analysis needs
5. Create analyzers that process logs to identify patterns and issues

Example structure:
```python
def test_agent_logging_completeness():
    """AGENT FEEDBACK: Verify agent produces comprehensive structured logs.

    This test ensures our agent properly logs all required information
    for debugging, monitoring, and improvement purposes.
    """
    # Arrange
    test_input = "Process this complex request with multiple steps"
    expected_log_fields = [
        "request_id", "timestamp", "input", "parsed_intent",
        "selected_action", "considered_alternatives", "confidence_score",
        "execution_time_ms", "output", "status"
    ]

    # Setup log capture
    log_capture = LogCapture()

    # Act
    agent.process(test_input, log_handler=log_capture)

    # Assert
    logs = log_capture.get_logs_as_json()
    assert len(logs) > 0, "No logs were produced"

    # Check if all required fields are present in the logs
    for log in logs:
        for field in expected_log_fields:
            assert field in log, f"Required log field '{field}' is missing"

    # Verify log sequence completeness
    assert "agent_started" in [log["event"] for log in logs]
    assert "agent_completed" in [log["event"] for log in logs]

    # Verify decision points are logged with alternatives
    decision_logs = [log for log in logs if log["event"] == "decision_point"]
    assert len(decision_logs) > 0, "No decision points were logged"
    for decision in decision_logs:
        assert "considered_alternatives" in decision
        assert len(decision["considered_alternatives"]) > 0
```

## Quality Assurance Standards

### 6. Code Coverage Requirements

```text
Implement comprehensive code coverage standards in your testing:

1. Establish minimum code coverage thresholds:
   - 85%+ overall line coverage
   - 95%+ coverage for critical components (authentication, data processing, API layers)
   - 100% coverage for utility functions and shared libraries

2. Track coverage trends over time:
   - Prevent coverage regression in established code
   - Allow temporary exemptions for prototype code with documented expiration

3. Cover all code paths and branches:
   - Test error handling and exception paths
   - Verify both positive and negative conditions for each branch
   - Ensure conditional logic is fully exercised

4. Include coverage reports in CI/CD pipelines:
   - Block merges that decrease coverage below thresholds
   - Highlight uncovered code sections for reviewer attention

Example implementation:
```python
# Coverage configuration (in pytest.ini, pyproject.toml, or similar)
[coverage]
fail_under = 85
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if TYPE_CHECKING:
    pass

# Critical component coverage validation
def test_coverage_critical_components():
    """Verify critical components meet 95% code coverage requirement."""
    coverage_report = get_coverage_report()
    critical_modules = [
        "app/auth",
        "app/data_processing",
        "app/api"
    ]

    for module in critical_modules:
        coverage = coverage_report.get_module_coverage(module)
        assert coverage >= 95, f"Critical module {module} has insufficient coverage: {coverage}%"
```

### 7. Static Analysis Rules

```text
Implement static analysis rules to catch issues before runtime:

1. Configure linters and static analyzers with appropriate rules:
   - Enforce consistent code style (PEP 8, ESLint, etc.)
   - Find potential bugs (unused variables, unreachable code)
   - Identify security vulnerabilities
   - Detect performance anti-patterns

2. Create custom rules specific to your project:
   - Domain-specific constraints and conventions
   - Architectural boundaries enforcement
   - Resource management patterns

3. Integrate static analysis into development workflow:
   - Run checks before commits (pre-commit hooks)
   - Include in CI/CD pipeline
   - Generate reports for code reviews

4. Maintain a "zero warnings" policy:
   - Treat warnings as errors in CI builds
   - Document temporary exceptions with clear justification
   - Schedule resolution of allowed exceptions

Example configuration:
```python
# Example pylint configuration
[MASTER]
ignore=CVS,build,dist
persistent=yes

[MESSAGES CONTROL]
disable=
    missing-docstring,
    invalid-name,
    too-few-public-methods

[CUSTOM]
# Project-specific rules
banned-modules=dangerous_module,insecure_library
required-imports=app.telemetry,app.validation

# Example pre-commit hook configuration
repos:
-   repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
    -   id: flake8
        additional_dependencies: [
            flake8-bandit,
            flake8-bugbear,
            flake8-docstrings,
        ]
```

### 8. Contract Testing Framework

```text
Implement contract testing to verify interface stability between components:

1. Define explicit contracts for all service interfaces:
   - Document expected request/response formats
   - Specify error handling behaviors
   - Define performance characteristics
   - Document version compatibility

2. Implement consumer-driven contract tests:
   - Have consumers define their expectations of providers
   - Verify providers meet all consumer expectations
   - Run tests on both consumer and provider sides

3. Maintain a contract registry:
   - Track all service interface contracts
   - Version contracts explicitly
   - Document migration paths for breaking changes

4. Automate contract verification:
   - Test against contract definitions, not implementations
   - Include contract verification in CI/CD pipelines
   - Alert on contract violations

Example implementation:
```python
def test_user_service_contract():
    """Verify the User Service meets its consumer contract requirements."""
    # Load contract definitions
    contract = ContractRegistry.load("user_service", version="2.1")

    # Test all required endpoints
    for endpoint in contract.endpoints:
        # Prepare test request based on contract
        request = endpoint.create_sample_request()

        # Execute request against service
        response = client.request(
            method=endpoint.method,
            url=endpoint.path,
            json=request.payload
        )

        # Verify response matches contract
        assert response.status_code == endpoint.expected_status
        assert validate_schema(response.json(), endpoint.response_schema)

        # Verify performance requirements
        assert response.elapsed.total_seconds() < endpoint.sla_response_time
```

### 9. Mutation Testing Guidelines

```text
Implement mutation testing to verify test quality:

1. Apply systematic code mutations to verify test effectiveness:
   - Replace conditional operators (>, <, ==, etc.)
   - Modify boundary values (+1, -1, etc.)
   - Remove conditional blocks
   - Change logical operators (AND to OR, etc.)
   - Swap function calls with similar signatures

2. Establish mutation score thresholds:
   - Minimum 80% killed mutations overall
   - 90%+ for critical components
   - 100% for security-sensitive code

3. Integrate into quality workflows:
   - Run periodically (weekly/monthly) or on significant changes
   - Review surviving mutations in code reviews
   - Address test gaps revealed by surviving mutations

4. Focus on high-value targets:
   - Business logic
   - Data transformation code
   - Security controls
   - Error handling

Example implementation:
```python
# Configuration for mutation testing
[mutmut]
paths_to_mutate=src/
backup=False
runner=pytest
tests_dir=tests/
use_coverage_data=True

# CI integration script
def test_mutation_score():
    """Run mutation testing and verify mutation score meets requirements."""
    # Run mutation testing
    result = subprocess.run(
        ["mutmut", "run", "--ci"],
        capture_output=True,
        text=True
    )

    # Parse results
    stats = parse_mutation_results(result.stdout)

    # Verify overall score
    assert stats["score"] >= 80, f"Mutation score too low: {stats['score']}%"

    # Verify critical components
    for component in CRITICAL_COMPONENTS:
        component_score = stats["component_scores"].get(component, 0)
        assert component_score >= 90, \
            f"Critical component {component} has insufficient mutation score: {component_score}%"
```

### 10. Property-Based Testing Framework

```text
Implement property-based testing to discover edge cases:

1. Define invariant properties your code must satisfy:
   - Reversible operations (encode/decode, serialize/deserialize)
   - Mathematical properties (commutativity, associativity)
   - Business rule invariants
   - Data transformation consistency

2. Generate diverse test inputs automatically:
   - Configure generators for your domain types
   - Include edge cases and boundary values
   - Combine generators for complex structures
   - Shrink failing cases to minimal examples

3. Define explicit property assertions:
   - Focus on what must be true, not specific examples
   - Cover both functional and non-functional requirements
   - Include performance and resource usage properties

4. Incorporate failure analysis:
   - Document discovered edge cases
   - Add specific regression tests for found issues
   - Refine generators based on findings

Example implementation:
```python
from hypothesis import given, strategies as st

@given(st.lists(st.integers()))
def test_sort_idempotence(values):
    """PROPERTY: Sorting an already sorted list produces the same result."""
    once = sorted(values)
    twice = sorted(once)
    assert once == twice

@given(st.lists(st.integers()))
def test_sort_size_invariant(values):
    """PROPERTY: Sorting preserves the size of the input list."""
    assert len(sorted(values)) == len(values)

@given(st.text())
def test_search_found_if_present(needle):
    """PROPERTY: If a string is in the text, search should find it."""
    # Skip empty strings
    if not needle:
        return

    haystack = f"prefix {needle} suffix"
    assert search(haystack, needle) is not None

@given(st.dictionaries(st.text(), st.text()))
def test_serialization_roundtrip(data):
    """PROPERTY: Serialize+deserialize should return the original data."""
    serialized = serialize_to_json(data)
    deserialized = deserialize_from_json(serialized)
    assert deserialized == data
```

## Security and Resilience

### 11. Security Testing Guidelines

<!-- @nist-controls: [si-10, si-11, ac-3, ac-6, ia-2, sc-8, sc-13, au-2] -->

```text
Implement comprehensive security testing practices:

1. Apply security testing at multiple levels:
   - Static analysis for known vulnerable patterns
   - Dependency scanning for known vulnerabilities
   - Dynamic testing (DAST) for runtime vulnerabilities
   - Interactive testing (IAST) for complex attack vectors

2. Test against established security standards:
   - OWASP Top 10 vulnerabilities
   - CWE/SANS Top 25 programming errors
   - Domain-specific security requirements (HIPAA, PCI-DSS, etc.)

3. Implement specific test cases for common vulnerabilities:
   - Injection attacks (SQL, NoSQL, OS command, etc.)
   - Authentication and authorization bypass
   - Sensitive data exposure
   - XXE and SSRF vulnerabilities
   - Security misconfigurations

4. Incorporate security tests into CI/CD:
   - Block deployment on critical findings
   - Generate security reports for review
   - Track security debt and remediation

Example implementation:
```python
def test_sql_injection_prevention():
    """Verify protection against SQL injection attacks.
    @nist si-10 "Input validation testing"
    @evidence test
    """
    # Arrange
    attack_vectors = [
        "' OR '1'='1",
        "'; DROP TABLE users; --",
        "' UNION SELECT username, password FROM users; --",
        # More attack vectors...
    ]

    # Act & Assert
    for attack in attack_vectors:
        # Test each input point that might reach database
        result = user_service.find_by_name(attack)
        assert not any_user_data_leaked(result)

        result = user_service.authenticate(attack, "password")
        assert result.authenticated is False

def test_authorization_controls():
    """Verify proper enforcement of authorization controls.
    @nist ac-3 "Access enforcement testing"
    @nist ac-6 "Least privilege verification"
    @evidence test
    """
    # Arrange
    regular_user = create_user(role="user")
    admin_user = create_user(role="admin")

    # Act & Assert
    # Test vertical privilege escalation
    regular_user_client = get_client_for_user(regular_user)
    response = regular_user_client.get("/admin/users")
    assert response.status_code == 403

    # Test horizontal privilege escalation
    other_user = create_user(role="user")
    response = regular_user_client.get(f"/users/{other_user.id}/profile")
    assert response.status_code == 403
```

### 12. Resilience Testing Framework

```text
Implement resilience testing to verify system stability under adverse
conditions:

1. Design chaos engineering experiments:
   - Service/dependency failures
   - Network degradation/partitioning
   - Resource exhaustion (CPU, memory, disk)
   - Clock skew and time-related issues
   - High latency and throughput scenarios

2. Define steady-state hypotheses for each experiment:
   - Explicit metrics that define normal operation
   - Acceptable degradation limits
   - Recovery time objectives

3. Run controlled experiments in production-like environments:
   - Start with minimal blast radius
   - Increase scope progressively
   - Always have abort conditions
   - Monitor closely during execution

4. Incorporate findings into architecture:
   - Document discovered weaknesses
   - Implement additional safeguards
   - Create regression tests for found issues

Example implementation:
```python
def test_resilience_to_database_failure():
    """Verify system resilience when database becomes unavailable.
    @nist si-11 "Error handling under failure conditions"
    @evidence test
    """
    # Define steady state
    def check_steady_state():
        response = client.get("/api/health")
        return (
            response.status_code == 200 and
            response.json()["status"] == "healthy" and
            response.elapsed.total_seconds() < 0.5
        )

    # Verify initial steady state
    assert check_steady_state()

    # Introduce chaos - database failure
    with simulate_database_failure():
        # Verify degraded but operational state
        response = client.get("/api/users")

        # Read operations should work from cache
        assert response.status_code == 200
        assert response.headers["X-Data-Source"] == "cache"

        # Write operations should fail gracefully
        create_response = client.post("/api/users", json={"name": "test"})
        assert create_response.status_code == 503  # Service Unavailable
        assert "retry_after" in create_response.headers

    # Verify recovery
    # Wait for recovery - max 30 seconds
    wait_for_condition(check_steady_state, timeout=30)

    # Verify writes work after recovery
    create_response = client.post("/api/users", json={"name": "test"})
    assert create_response.status_code == 201  # Created
```

## Documentation and Integration

### 13. Documentation Testing

```text
Implement documentation testing to ensure accuracy and reliability:

1. Test all code examples in documentation:
   - Extract code blocks from documentation
   - Execute in isolated environments
   - Verify expected outputs match documented claims
   - Update examples when APIs change

2. Validate API documentation completeness:
   - Test that all endpoints are documented
   - Verify all parameters are described
   - Ensure all response codes are documented
   - Check that examples cover common use cases

3. Test documentation for user journeys:
   - Verify step-by-step tutorials work as written
   - Test installation and setup instructions
   - Validate troubleshooting guides

4. Automate documentation testing:
   - Run doc tests in CI/CD pipelines
   - Generate documentation from tests
   - Flag documentation drift

Example implementation:
```python
def test_readme_examples():
    """Verify all code examples in README.md work as documented."""
    # Extract code examples from README
    readme_path = Path("README.md")
    readme_content = readme_path.read_text()
    code_blocks = extract_code_blocks(readme_content)

    for i, code in enumerate(code_blocks):
        # Skip non-executable examples (e.g., console output)
        if is_executable_code(code):
            # Create temporary module for execution
            module_path = tmp_path / f"example_{i}.py"
            module_path.write_text(code)

            # Execute example
            result = subprocess.run(
                [sys.executable, str(module_path)],
                capture_output=True,
                text=True
            )

            # Verify execution succeeds
            assert result.returncode == 0, f"Example {i} failed: {result.stderr}"

            # Verify output matches if specified
            expected_output = extract_expected_output(readme_content, i)
            if expected_output:
                assert expected_output in result.stdout

def test_api_documentation_completeness():
    """Verify API documentation covers all actual endpoints."""
    # Get actual API endpoints
    actual_endpoints = list_all_api_endpoints()

    # Get documented endpoints
    documented_endpoints = extract_endpoints_from_docs()

    # Verify all actual endpoints are documented
    for endpoint in actual_endpoints:
        assert endpoint in documented_endpoints, f"Endpoint {endpoint} is not documented"

        # Verify all parameters are documented
        actual_params = get_endpoint_parameters(endpoint)
        documented_params = get_documented_parameters(endpoint)
        assert set(actual_params) == set(documented_params), \
            f"Parameter mismatch for {endpoint}: actual {actual_params}, " \
            f"documented {documented_params}"
```

### 14. Integration Testing Patterns

```text
Implement robust integration testing patterns:

1. Define integration boundaries explicitly:
   - Component interactions
   - Service dependencies
   - Third-party integrations
   - Database and persistence layers

2. Use appropriate testing approaches for each boundary:
   - Mocks for uncontrollable dependencies
   - Stubs for simplified behavior
   - Spies for interaction verification
   - Real instances for critical paths

3. Implement end-to-end test scenarios:
   - Complete user journeys
   - Multi-step business processes
   - Cross-component workflows

4. Manage test environments effectively:
   - Containerize dependencies
   - Use test doubles when appropriate
   - Reset state between tests
   - Parallel testing support

Example implementation:
```python
def test_user_registration_end_to_end():
    """Verify the complete user registration process across all components."""
    # Arrange
    email = f"test-{uuid.uuid4()}@example.com"
    password = "secure_password123"

    # Use real email service in test mode
    email_service = configure_real_email_service(test_mode=True)

    # Act - Start registration process
    response = client.post("/api/register", json={
        "email": email,
        "password": password
    })

    # Assert - Initial response
    assert response.status_code == 202  # Accepted
    registration_id = response.json()["registration_id"]

    # Verify email was sent
    sent_emails = email_service.get_sent_emails()
    assert len(sent_emails) == 1
    verification_email = sent_emails[0]
    assert verification_email.recipient == email

    # Extract verification code
    verification_code = extract_verification_code(verification_email.body)

    # Complete verification
    response = client.post("/api/verify", json={
        "registration_id": registration_id,
        "verification_code": verification_code
    })
    assert response.status_code == 201  # Created

    # Verify user is created in database
    with db_connection() as conn:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
        assert user is not None
        assert user["email"] == email
        assert user["is_verified"] is True

    # Verify login works
    response = client.post("/api/login", json={
        "email": email,
        "password": password
    })
    assert response.status_code == 200
    assert "auth_token" in response.json()
```

### 15. Testability Guidelines

```text
Implement testability guidelines to ensure code is designed for effective
testing:

1. Design for testability:
   - Use dependency injection
   - Separate concerns clearly
   - Avoid global state
   - Create pure functions where possible

2. Create testability interfaces:
   - Time providers instead of direct datetime usage
   - File system abstractions
   - Network/API abstractions
   - Randomness control

3. Implement testing hooks:
   - Instrumentation points
   - State inspection methods
   - Execution trace capabilities
   - Test-only extension points

4. Establish testability reviews:
   - Include testability in code reviews
   - Measure test effort as metric
   - Refactor hard-to-test code

Example implementation:
```python
# Instead of this:
class HardToTestService:
    def process_data(self, input_data):
        current_time = datetime.now()
        processed = self._transform(input_data)
        if random.random() < 0.5:
            return self._special_case(processed, current_time)
        return processed

# Do this:
class TestableService:
    def __init__(self, time_provider=None, random_provider=None):
        self.time_provider = time_provider or (lambda: datetime.now())
        self.random_provider = random_provider or random.random

    def process_data(self, input_data):
        current_time = self.time_provider()
        processed = self._transform(input_data)
        if self.random_provider() < 0.5:
            return self._special_case(processed, current_time)
        return processed

# Now testing becomes straightforward:
def test_process_data_normal_path():
    """Test the normal processing path."""
    # Arrange
    service = TestableService(
        time_provider=lambda: datetime(2023, 1, 1, 12, 0, 0),
        random_provider=lambda: 0.6  # Ensures we skip the special case
    )
    input_data = {"key": "value"}

    # Act
    result = service.process_data(input_data)

    # Assert
    assert result == expected_transformed_data

def test_process_data_special_case():
    """Test the special case processing path."""
    # Arrange
    fixed_time = datetime(2023, 1, 1, 12, 0, 0)
    service = TestableService(
        time_provider=lambda: fixed_time,
        random_provider=lambda: 0.4  # Ensures we take the special case
    )
    input_data = {"key": "value"}

    # Act
    result = service.process_data(input_data)

    # Assert
    assert result == expected_special_case_result
```

## Master Prompt for Test Suite Generation

```text
Generate a comprehensive test suite for this code that follows the Complete Testing Manifesto:

1. Core Testing Principles:
   - Hypothesis tests that validate core behaviors and expectations
   - Regression tests that prevent known bugs from reappearing
   - Benchmark tests that enforce performance SLAs
   - Grammatical Evolution for fuzzing and edge case discovery
   - Structured logs for agent feedback and analysis

2. Quality Assurance:
   - Code coverage meeting standards (85%+ overall, 95%+ for critical paths)
   - Static analysis rules to catch potential issues early
   - Contract tests for interface stability between components
   - Mutation testing to verify test suite effectiveness
   - Property-based testing to validate code invariants

3. Security and Resilience:
   - Security tests for common vulnerabilities and attacks
   - Resilience tests that verify system behavior under adverse conditions

4. Documentation and Integration:
   - Documentation tests to ensure examples and guides remain accurate
   - Integration tests for key component interactions and user journeys
   - Testability improvements to make the code more easily verifiable

For each test:
- Include clear documentation of purpose and expected behavior
- Provide detailed setup and context for test conditions
- Write explicit assertions with descriptive failure messages
- Categorize appropriately (unit, integration, security, etc.)

The test suite should be maintainable, provide fast feedback, and serve as
living documentation of the system's behavior and constraints.

## Implementation

### Getting Started

1. Review the relevant sections of this standard for your use case
2. Identify which guidelines apply to your project
3. Implement the required practices and patterns
4. Validate compliance using the provided checklists

### Implementation Checklist

- [ ] Review and understand applicable standards
- [ ] Implement required practices
- [ ] Follow recommended patterns
- [ ] Validate implementation against guidelines
- [ ] Document any deviations with justification

## Related Standards

- [Knowledge Management Standards](KNOWLEDGE_MANAGEMENT_STANDARDS.md) - Documentation practices
- [CREATING_STANDARDS_GUIDE.md](../guides/CREATING_STANDARDS_GUIDE.md) - Standards creation guide
- [COMPLIANCE_STANDARDS.md](COMPLIANCE_STANDARDS.md) - NIST compliance testing requirements
- [Model Context Protocol Standards](MODEL_CONTEXT_PROTOCOL_STANDARDS.md) - MCP testing patterns
