// Supertest API integration test template
const request = require('supertest');
const app = require('../../src/app');
const { setupTestDatabase, teardownTestDatabase } = require('../helpers/db-setup');

describe('User API Integration Tests', () => {
  let createdUserId;

  beforeAll(async () => {
    await setupTestDatabase();
  });

  afterAll(async () => {
    await teardownTestDatabase();
  });

  afterEach(async () => {
    // Cleanup between tests
    await cleanupTestData();
  });

  describe('POST /api/users', () => {
    it('should create a new user with valid data', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          name: 'Test User',
          password: 'SecurePass123!'
        })
        .expect('Content-Type', /json/)
        .expect(201);

      expect(response.body).toHaveProperty('id');
      expect(response.body.email).toBe('test@example.com');
      expect(response.body).not.toHaveProperty('password');
      createdUserId = response.body.id;
    });

    it('should reject duplicate email', async () => {
      await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          name: 'First User',
          password: 'Pass123!'
        })
        .expect(201);

      await request(app)
        .post('/api/users')
        .send({
          email: 'test@example.com',
          name: 'Duplicate User',
          password: 'Pass456!'
        })
        .expect(409);
    });

    it('should validate required fields', async () => {
      const response = await request(app)
        .post('/api/users')
        .send({ email: 'test@example.com' })
        .expect(400);

      expect(response.body).toHaveProperty('errors');
      expect(response.body.errors).toContainEqual(
        expect.objectContaining({ field: 'name' })
      );
    });
  });

  describe('GET /api/users/:id', () => {
    beforeEach(async () => {
      const response = await request(app)
        .post('/api/users')
        .send({
          email: 'retrieve@example.com',
          name: 'Retrieve Test',
          password: 'Pass123!'
        });
      createdUserId = response.body.id;
    });

    it('should retrieve user by ID', async () => {
      const response = await request(app)
        .get(`/api/users/${createdUserId}`)
        .expect(200);

      expect(response.body.id).toBe(createdUserId);
      expect(response.body.email).toBe('retrieve@example.com');
    });

    it('should return 404 for non-existent user', async () => {
      await request(app)
        .get('/api/users/99999')
        .expect(404);
    });
  });

  describe('PUT /api/users/:id', () => {
    it('should update user successfully', async () => {
      const response = await request(app)
        .put(`/api/users/${createdUserId}`)
        .send({ name: 'Updated Name' })
        .expect(200);

      expect(response.body.name).toBe('Updated Name');
      expect(response.body.email).toBe('retrieve@example.com');
    });
  });

  describe('DELETE /api/users/:id', () => {
    it('should delete user successfully', async () => {
      await request(app)
        .delete(`/api/users/${createdUserId}`)
        .expect(204);

      await request(app)
        .get(`/api/users/${createdUserId}`)
        .expect(404);
    });
  });
});
