// Jest unit test template with mocks and assertions

const { UserService } = require('../src/UserService');
const { validateEmail } = require('../src/validation');

// Mock external modules
jest.mock('../src/database');
const database = require('../src/database');

describe('UserService', () => {
  let userService;

  beforeEach(() => {
    // Setup before each test
    userService = new UserService(database);
    jest.clearAllMocks();
  });

  afterEach(() => {
    // Cleanup after each test
    jest.restoreAllMocks();
  });

  describe('createUser', () => {
    test('should create user successfully', async () => {
      // Arrange
      const userData = { email: 'test@example.com', name: 'Test User' };
      database.insert.mockResolvedValue({ id: 1, ...userData });

      // Act
      const result = await userService.createUser(userData);

      // Assert
      expect(result.id).toBe(1);
      expect(result.email).toBe('test@example.com');
      expect(database.insert).toHaveBeenCalledWith(userData);
    });

    test('should throw error for invalid email', async () => {
      // Arrange
      const userData = { email: 'invalid', name: 'Test' };

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects
        .toThrow('Invalid email format');
    });
  });

  describe('getUserById', () => {
    test('should return user when found', async () => {
      // Arrange
      const mockUser = { id: 1, email: 'test@example.com' };
      database.findById.mockResolvedValue(mockUser);

      // Act
      const user = await userService.getUserById(1);

      // Assert
      expect(user).toEqual(mockUser);
      expect(database.findById).toHaveBeenCalledWith(1);
    });

    test('should return null when user not found', async () => {
      // Arrange
      database.findById.mockResolvedValue(null);

      // Act
      const user = await userService.getUserById(999);

      // Assert
      expect(user).toBeNull();
    });
  });

  // Parametrized testing with test.each
  test.each([
    ['valid@example.com', true],
    ['invalid.email', false],
    ['@example.com', false],
    ['user@', false],
  ])('validateEmail(%s) should return %s', (email, expected) => {
    expect(validateEmail(email)).toBe(expected);
  });

  // Spy on methods
  test('should call validation before saving', async () => {
    const validateSpy = jest.spyOn(userService, 'validate');
    const userData = { email: 'test@example.com', name: 'Test' };

    await userService.createUser(userData);

    expect(validateSpy).toHaveBeenCalledWith(userData);
  });
});

// Async testing
describe('async operations', () => {
  test('should handle promise resolution', async () => {
    const promise = Promise.resolve('success');
    await expect(promise).resolves.toBe('success');
  });

  test('should handle promise rejection', async () => {
    const promise = Promise.reject(new Error('failed'));
    await expect(promise).rejects.toThrow('failed');
  });
});
