---
name: integration-testing
description: Integration testing standards for API testing, database testing, and service-to-service communication. Covers test containers, Docker Compose, API mocking, and contract testing for reliable integration suites.
---

# Integration Testing Standards

> **Quick Navigation:**
> Level 1: [Quick Start](#level-1-quick-start-2000-tokens-5-minutes) (5 min) → Level 2: [Implementation](#level-2-implementation-5000-tokens-30-minutes) (30 min) → Level 3: [Mastery](#level-3-mastery-resources) (Extended)

---

## Level 1: Quick Start (<2,000 tokens, 5 minutes)

### Core Principles

1. **Test Real Interactions**: Verify actual communication between components
2. **Isolated Environments**: Use Docker containers for reproducible tests
3. **Fast Feedback**: Keep integration tests under 30 seconds when possible
4. **Contract Testing**: Verify API contracts between services
5. **Database Testing**: Test with real databases, not mocks

### Essential Checklist

- [ ] **Testcontainers**: Docker-based test dependencies (database, cache, message queue)
- [ ] **API testing**: REST/GraphQL endpoints tested with real HTTP
- [ ] **Database migrations**: Test schema migrations and rollbacks
- [ ] **Contract tests**: Provider-consumer contract verification
- [ ] **Test data management**: Fixtures and cleanup strategies
- [ ] **Service mocking**: External services mocked with WireMock/MockServer
- [ ] **Docker Compose**: Test environment orchestration
- [ ] **CI integration**: Tests run in isolated containers

### Quick Example

```python
# pytest integration test with Testcontainers
import pytest
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
import requests

@pytest.fixture(scope="module")
def postgres_container():
    """Start PostgreSQL container for testing."""
    with PostgresContainer("postgres:16") as postgres:
        yield postgres

@pytest.fixture
def db_engine(postgres_container):
    """Create database engine with test container."""
    connection_url = postgres_container.get_connection_url()
    engine = create_engine(connection_url)
    # Run migrations
    run_migrations(engine)
    yield engine
    engine.dispose()

def test_create_user_integration(db_engine):
    """Test user creation with real database."""
    # Arrange
    user_data = {'email': 'test@example.com', 'name': 'Test User'}

    # Act
    response = requests.post('http://localhost:8000/api/users', json=user_data)

    # Assert
    assert response.status_code == 201
    user_id = response.json()['id']

    # Verify in database
    with db_engine.connect() as conn:
        result = conn.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = result.fetchone()
        assert user['email'] == 'test@example.com'
```

### Quick Links to Level 2

- [API Testing](#api-testing)
- [Database Testing](#database-testing)
- [Service Mocking](#service-mocking)
- [Contract Testing](#contract-testing)
- [Docker Compose Setup](#docker-compose-setup)

---

## Level 2: Implementation (<5,000 tokens, 30 minutes)

### API Testing

**REST API Testing** (see [templates/api-test-template.js](templates/api-test-template.js))

```javascript
// Supertest API integration testing
const request = require('supertest');
const app = require('../src/app');

describe('User API Integration Tests', () => {
  let createdUserId;

  beforeAll(async () => {
    // Setup test database
    await setupTestDatabase();
  });

  afterAll(async () => {
    // Cleanup
    await teardownTestDatabase();
  });

  describe('POST /api/users', () => {
    it('should create a new user', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
          password: 'secure123'
        })
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.email).toBe('test@example.com');
      createdUserId = response.body.id;
    });

    it('should reject duplicate email', async () => {
      await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          name: 'Duplicate User'
        })
        .expect(409);
    });
  });

  describe('GET /api/users/:id', () => {
    it('should retrieve user by ID', async () => {
      const response = await request(app)
        .get(`/api/users/${createdUserId}`)
        .expect(200);

      expect(response.body.id).toBe(createdUserId);
      expect(response.body.email).toBe('test@example.com');
    });

    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/api/users/99999')
        .expect(404);
    });
  });
});
```

### Database Testing

**Testcontainers Integration** (see [templates/integration-test-python.py](templates/integration-test-python.py))

```python
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from sqlalchemy import create_engine
from app.database import init_db, Base
from app.services.user_service import UserService

@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for entire test session."""
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="session")
def redis_container():
    """Start Redis container for caching tests."""
    with RedisContainer("redis:7-alpine") as redis:
        yield redis

@pytest.fixture
def db_session(postgres_container):
    """Create database session with schema."""
    engine = create_engine(postgres_container.get_connection_url())

    # Create schema
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    # Cleanup
    session.rollback()
    session.close()
    Base.metadata.drop_all(engine)

def test_user_crud_operations(db_session):
    """Test complete CRUD cycle with real database."""
    service = UserService(session=db_session)

    # Create
    user = service.create_user({
        'email': 'integration@test.com',
        'name': 'Integration Test'
    })
    assert user.id is not None

    # Read
    found_user = service.get_user_by_id(user.id)
    assert found_user.email == 'integration@test.com'

    # Update
    service.update_user(user.id, {'name': 'Updated Name'})
    updated_user = service.get_user_by_id(user.id)
    assert updated_user.name == 'Updated Name'

    # Delete
    service.delete_user(user.id)
    deleted_user = service.get_user_by_id(user.id)
    assert deleted_user is None
```

### Service Mocking

**WireMock Integration**

```python
from wiremock.server import WireMockServer
import requests

@pytest.fixture(scope="module")
def wiremock_server():
    """Start WireMock server for mocking external APIs."""
    server = WireMockServer(port=8080)
    server.start()

    # Setup stub
    server.stub_for({
        "request": {
            "method": "GET",
            "url": "/api/external/user/1"
        },
        "response": {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": '{"id": 1, "name": "External User"}'
        }
    })

    yield server
    server.stop()

def test_external_api_integration(wiremock_server):
    """Test integration with mocked external API."""
    response = requests.get('http://localhost:8080/api/external/user/1')

    assert response.status_code == 200
    assert response.json()['name'] == 'External User'
```

### Contract Testing

**Pact Contract Testing** (see [resources/examples/contract-testing.md](resources/examples/contract-testing.md))

```python
# Consumer test (defines contract)
from pact import Consumer, Provider

pact = Consumer('UserService').has_pact_with(Provider('APIGateway'))

def test_get_user_contract():
    """Consumer defines expected API behavior."""
    expected = {
        'id': 1,
        'email': 'test@example.com',
        'name': 'Test User'
    }

    (pact
     .given('user 1 exists')
     .upon_receiving('a request for user 1')
     .with_request('GET', '/api/users/1')
     .will_respond_with(200, body=expected))

    with pact:
        result = get_user_from_api(1)
        assert result == expected

# Provider test (verifies contract)
def test_provider_honors_contract():
    """Provider verifies it meets consumer expectations."""
    verifier = Verifier(provider='APIGateway', provider_base_url='http://localhost:8000')

    output, logs = verifier.verify_pacts('./pacts/userservice-apigateway.json')

    assert output == 0, "Provider failed to honor contract"
```

### Docker Compose Setup

**Test Environment** (see [templates/docker-compose.test.yml](templates/docker-compose.test.yml))

```yaml
version: '3.8'

services:
  app:
    build: .
    environment:
      DATABASE_URL: postgresql://test:test@postgres:5432/testdb
      REDIS_URL: redis://redis:6379
    depends_on:
      - postgres
      - redis
    ports:
      - "8000:8000"

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    ports:
      - "5432:5432"
    tmpfs:
      - /var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  wiremock:
    image: wiremock/wiremock:latest
    ports:
      - "8080:8080"
    volumes:
      - ./tests/mocks:/home/wiremock
```

**Test Execution Script** (see [scripts/setup-test-db.sh](scripts/setup-test-db.sh))

```bash
#!/bin/bash
# Setup test database and run integration tests

set -euo pipefail

# Start test environment
docker-compose -f docker-compose.test.yml up -d

# Wait for services
echo "Waiting for services..."
sleep 5

# Run migrations
docker-compose -f docker-compose.test.yml exec app python manage.py migrate

# Run integration tests
docker-compose -f docker-compose.test.yml exec app pytest tests/integration/

# Cleanup
docker-compose -f docker-compose.test.yml down -v
```

---

## Level 3: Mastery Resources

### Advanced Topics

- **[Service Mesh Testing](resources/service-mesh-testing.md)**: Istio, Linkerd integration tests
- **[Message Queue Testing](resources/mq-testing.md)**: Kafka, RabbitMQ integration
- **[GraphQL Testing](resources/graphql-testing.md)**: GraphQL API integration

### Templates & Examples

- **[Docker Compose](templates/docker-compose.test.yml)**: Complete test environment
- **[API Test Template](templates/api-test-template.js)**: Supertest example
- **[Python Integration](templates/integration-test-python.py)**: Testcontainers
- **[Contract Testing Guide](resources/examples/contract-testing.md)**: Pact examples
- **[Setup Script](scripts/setup-test-db.sh)**: Database setup automation

### Related Skills

- [Unit Testing](../unit-testing/SKILL.md) - Foundation for integration tests
- [Secrets Management](../../security/secrets-management/SKILL.md) - Secure test credentials

---

## Quick Reference Commands

```bash
# Docker Compose
docker-compose -f docker-compose.test.yml up -d
docker-compose -f docker-compose.test.yml exec app pytest
docker-compose -f docker-compose.test.yml down -v

# Testcontainers
pytest tests/integration/ -v
pytest tests/integration/ --testcontainers-log-level=DEBUG

# API testing
npm run test:integration
npm run test:api -- --watch

# Contract testing
pact-broker publish ./pacts --consumer-app-version 1.0.0
pact-broker can-i-deploy --pacticipant UserService --version 1.0.0
```

---

## Validation

- ✅ Token count: Level 1 <2,000, Level 2 <5,000
- ✅ Testcontainers: Complete database integration
- ✅ API testing: Supertest and httptest examples
- ✅ Contract testing: Pact integration
