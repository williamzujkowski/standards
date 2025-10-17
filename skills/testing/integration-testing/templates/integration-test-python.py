"""Integration test template with Testcontainers."""
import pytest
from testcontainers.postgres import PostgresContainer
from testcontainers.redis import RedisContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.services.user_service import UserService
from app.models.user import User

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

@pytest.fixture(scope="function")
def db_engine(postgres_container):
    """Create database engine with schema for each test."""
    engine = create_engine(postgres_container.get_connection_url())
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Create database session for each test."""
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

class TestUserServiceIntegration:
    """Integration tests for UserService with real database."""

    def test_create_user(self, db_session):
        """Test user creation with real database."""
        service = UserService(session=db_session)

        user_data = {
            'email': 'integration@test.com',
            'name': 'Integration Test',
            'password': 'SecurePass123!'
        }

        user = service.create_user(user_data)

        assert user.id is not None
        assert user.email == 'integration@test.com'
        assert user.password != 'SecurePass123!'  # Should be hashed

    def test_get_user_by_id(self, db_session):
        """Test retrieving user by ID."""
        service = UserService(session=db_session)

        # Create user
        created_user = service.create_user({
            'email': 'find@test.com',
            'name': 'Find Test'
        })

        # Retrieve user
        found_user = service.get_user_by_id(created_user.id)

        assert found_user is not None
        assert found_user.id == created_user.id
        assert found_user.email == 'find@test.com'

    def test_update_user(self, db_session):
        """Test updating user."""
        service = UserService(session=db_session)

        # Create user
        user = service.create_user({
            'email': 'update@test.com',
            'name': 'Original Name'
        })

        # Update user
        service.update_user(user.id, {'name': 'Updated Name'})

        # Verify update
        updated_user = service.get_user_by_id(user.id)
        assert updated_user.name == 'Updated Name'

    def test_delete_user(self, db_session):
        """Test deleting user."""
        service = UserService(session=db_session)

        # Create user
        user = service.create_user({
            'email': 'delete@test.com',
            'name': 'Delete Test'
        })

        # Delete user
        service.delete_user(user.id)

        # Verify deletion
        deleted_user = service.get_user_by_id(user.id)
        assert deleted_user is None

    def test_user_crud_complete_cycle(self, db_session):
        """Test complete CRUD cycle."""
        service = UserService(session=db_session)

        # Create
        user = service.create_user({
            'email': 'crud@test.com',
            'name': 'CRUD Test'
        })
        assert user.id is not None

        # Read
        found = service.get_user_by_id(user.id)
        assert found.email == 'crud@test.com'

        # Update
        service.update_user(user.id, {'name': 'Updated CRUD'})
        updated = service.get_user_by_id(user.id)
        assert updated.name == 'Updated CRUD'

        # Delete
        service.delete_user(user.id)
        assert service.get_user_by_id(user.id) is None

    def test_unique_email_constraint(self, db_session):
        """Test database enforces unique email constraint."""
        service = UserService(session=db_session)

        service.create_user({
            'email': 'unique@test.com',
            'name': 'First User'
        })

        with pytest.raises(Exception):  # IntegrityError or custom exception
            service.create_user({
                'email': 'unique@test.com',
                'name': 'Second User'
            })
