# Contract Testing Guide

## Overview

Contract testing ensures that services can communicate correctly by verifying that providers meet the expectations of their consumers. This guide covers Pact-based contract testing.

## Consumer-Driven Contracts

### Consumer Test (Defines Contract)

The consumer defines what it expects from the provider:

```python
# consumer_test.py
from pact import Consumer, Provider, Like, EachLike, Term
import pytest

pact = Consumer('UserService').has_pact_with(
    Provider('APIGateway'),
    pact_dir='./pacts'
)

def test_get_user_by_id():
    """Consumer expects to get user data by ID."""
    user_id = 1
    expected = {
        'id': Like(1),
        'email': Like('test@example.com'),
        'name': Like('Test User'),
        'created_at': Term(
            r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
            '2024-01-01T12:00:00'
        )
    }

    (pact
     .given('user 1 exists')
     .upon_receiving('a request for user 1')
     .with_request('GET', f'/api/users/{user_id}')
     .will_respond_with(200, body=expected))

    with pact:
        result = api_gateway_client.get_user(user_id)
        assert result['id'] == 1
        assert result['email'] == 'test@example.com'

def test_get_users_list():
    """Consumer expects to get list of users."""
    expected = EachLike({
        'id': Like(1),
        'email': Like('test@example.com'),
        'name': Like('Test User')
    }, minimum=1)

    (pact
     .given('users exist')
     .upon_receiving('a request for all users')
     .with_request('GET', '/api/users')
     .will_respond_with(200, body=expected))

    with pact:
        result = api_gateway_client.get_users()
        assert len(result) > 0
        assert 'id' in result[0]

def test_create_user():
    """Consumer expects to create a user."""
    user_data = {
        'email': 'new@example.com',
        'name': 'New User'
    }

    expected = {
        'id': Like(1),
        'email': 'new@example.com',
        'name': 'New User'
    }

    (pact
     .given('no user with email new@example.com exists')
     .upon_receiving('a request to create a user')
     .with_request(
         'POST',
         '/api/users',
         body=user_data,
         headers={'Content-Type': 'application/json'}
     )
     .will_respond_with(201, body=expected))

    with pact:
        result = api_gateway_client.create_user(user_data)
        assert result['email'] == 'new@example.com'
```

### Provider Test (Verifies Contract)

The provider verifies it meets all consumer expectations:

```python
# provider_test.py
from pact import Verifier

def test_provider_honors_contracts():
    """Verify provider meets all consumer expectations."""
    verifier = Verifier(
        provider='APIGateway',
        provider_base_url='http://localhost:8000'
    )

    # Setup provider states
    provider_states = {
        'user 1 exists': setup_user_1_exists,
        'users exist': setup_users_exist,
        'no user with email new@example.com exists': setup_no_user_exists
    }

    output, logs = verifier.verify_pacts(
        './pacts/userservice-apigateway.json',
        provider_states_setup_url='http://localhost:8000/_pact/provider_states'
    )

    assert output == 0, f"Provider verification failed:\n{logs}"

def setup_user_1_exists():
    """Setup: Create user with ID 1."""
    db.execute("INSERT INTO users (id, email, name) VALUES (1, 'test@example.com', 'Test User')")

def setup_users_exist():
    """Setup: Create multiple users."""
    db.execute("INSERT INTO users (email, name) VALUES ('user1@test.com', 'User 1')")
    db.execute("INSERT INTO users (email, name) VALUES ('user2@test.com', 'User 2')")

def setup_no_user_exists():
    """Setup: Ensure no user with specific email exists."""
    db.execute("DELETE FROM users WHERE email = 'new@example.com'")
```

## Pact Broker Integration

### Publishing Contracts

```bash
# Publish consumer contract
pact-broker publish ./pacts \
  --consumer-app-version 1.2.3 \
  --broker-base-url https://pact-broker.example.com \
  --broker-token $PACT_BROKER_TOKEN

# Tag as production
pact-broker create-version-tag \
  --pacticipant UserService \
  --version 1.2.3 \
  --tag production
```

### Verification Before Deployment

```bash
# Check if safe to deploy
pact-broker can-i-deploy \
  --pacticipant UserService \
  --version 1.2.3 \
  --to production \
  --broker-base-url https://pact-broker.example.com

# Example output:
# Computer says yes \o/
#
# CONSUMER       | C.VERSION | PROVIDER    | P.VERSION | SUCCESS?
# ---------------|-----------|-------------|-----------|----------
# UserService    | 1.2.3     | APIGateway  | 2.1.0     | true
```

## CI/CD Integration

### Consumer CI Pipeline

```yaml
# .github/workflows/consumer-tests.yml
name: Consumer Contract Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run consumer tests
        run: pytest tests/consumer_tests/

      - name: Publish contracts
        if: github.ref == 'refs/heads/main'
        run: |
          pact-broker publish ./pacts \
            --consumer-app-version ${{ github.sha }} \
            --broker-base-url ${{ secrets.PACT_BROKER_URL }} \
            --broker-token ${{ secrets.PACT_BROKER_TOKEN }}
```

### Provider CI Pipeline

```yaml
# .github/workflows/provider-tests.yml
name: Provider Contract Verification

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Start provider
        run: docker-compose up -d app

      - name: Verify contracts
        run: |
          pytest tests/provider_verification/ \
            --pact-broker-url=${{ secrets.PACT_BROKER_URL }} \
            --pact-broker-token=${{ secrets.PACT_BROKER_TOKEN }}

      - name: Can I deploy?
        if: github.ref == 'refs/heads/main'
        run: |
          pact-broker can-i-deploy \
            --pacticipant APIGateway \
            --version ${{ github.sha }} \
            --to production
```

## Best Practices

1. **Consumer-Driven**: Let consumers define what they need
2. **Version Everything**: Tag contracts with semantic versions
3. **Provider States**: Use specific, minimal test data
4. **Pact Broker**: Centralize contract storage and verification
5. **Deployment Gates**: Use can-i-deploy before production
6. **Keep Contracts Small**: Test one interaction per contract test
7. **Regular Verification**: Run provider tests on every commit
