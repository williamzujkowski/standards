/**
 * Unit Testing Examples - JavaScript/Jest
 *
 * This file demonstrates best practices for writing unit tests with Jest,
 * including mocking, async testing, snapshot testing, and test coverage.
 *
 * @see https://jestjs.io/docs/getting-started
 */

// ===== Example Code Under Test =====

class Calculator {
  add(a, b) {
    return a + b;
  }

  subtract(a, b) {
    return a - b;
  }

  divide(a, b) {
    if (b === 0) {
      throw new Error('Cannot divide by zero');
    }
    return a / b;
  }

  multiply(a, b) {
    return a * b;
  }
}

class User {
  constructor(id, name, email, isActive = true) {
    this.id = id;
    this.name = name;
    this.email = email;
    this.isActive = isActive;
  }

  deactivate() {
    this.isActive = false;
  }

  getDisplayName() {
    return `${this.name} (${this.email})`;
  }
}

class UserRepository {
  constructor(database) {
    this.db = database;
  }

  async getUserById(userId) {
    const result = await this.db.query(`SELECT * FROM users WHERE id = ${userId}`);
    return new User(result.id, result.name, result.email, result.is_active);
  }

  async saveUser(user) {
    return await this.db.execute(`INSERT INTO users VALUES ${user.id}`);
  }
}

class ApiService {
  async fetchData(url) {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return await response.json();
  }
}

// ===== Basic Unit Tests =====

describe('Calculator', () => {
  let calculator;

  // Setup before each test
  beforeEach(() => {
    calculator = new Calculator();
  });

  // Teardown after each test
  afterEach(() => {
    // Clean up if needed
  });

  describe('add', () => {
    test('should add two positive numbers', () => {
      const result = calculator.add(2, 3);
      expect(result).toBe(5);
    });

    test('should add negative numbers', () => {
      const result = calculator.add(-2, -3);
      expect(result).toBe(-5);
    });

    test('should add zero', () => {
      const result = calculator.add(5, 0);
      expect(result).toBe(5);
    });
  });

  describe('subtract', () => {
    test('should subtract two numbers', () => {
      const result = calculator.subtract(10, 3);
      expect(result).toBe(7);
    });
  });

  describe('multiply', () => {
    test('should multiply two numbers', () => {
      const result = calculator.multiply(4, 5);
      expect(result).toBe(20);
    });
  });

  describe('divide', () => {
    test('should divide two numbers', () => {
      const result = calculator.divide(10, 2);
      expect(result).toBe(5);
    });

    test('should throw error when dividing by zero', () => {
      expect(() => calculator.divide(10, 0)).toThrow('Cannot divide by zero');
    });
  });
});

// ===== Parametrized Tests (using test.each) =====

describe('Calculator - Parametrized Tests', () => {
  const calculator = new Calculator();

  test.each([
    [2, 3, 5],
    [0, 0, 0],
    [-1, 1, 0],
    [100, 200, 300],
    [-5, -3, -8],
  ])('add(%i, %i) should return %i', (a, b, expected) => {
    expect(calculator.add(a, b)).toBe(expected);
  });

  test.each([
    [10, 2, 5],
    [100, 10, 10],
    [7, 2, 3.5],
    [-10, 2, -5],
  ])('divide(%i, %i) should return %i', (a, b, expected) => {
    expect(calculator.divide(a, b)).toBe(expected);
  });

  test.each([0, -0])('divide(10, %i) should throw error', (divisor) => {
    expect(() => calculator.divide(10, divisor)).toThrow();
  });
});

// ===== Mocking Tests =====

describe('UserRepository', () => {
  let mockDatabase;
  let userRepository;

  beforeEach(() => {
    // Create mock database
    mockDatabase = {
      query: jest.fn(),
      execute: jest.fn(),
    };

    userRepository = new UserRepository(mockDatabase);
  });

  describe('getUserById', () => {
    test('should retrieve user from database', async () => {
      // Arrange
      const mockUser = {
        id: 1,
        name: 'Alice',
        email: 'alice@example.com',
        is_active: true,
      };
      mockDatabase.query.mockResolvedValue(mockUser);

      // Act
      const user = await userRepository.getUserById(1);

      // Assert
      expect(mockDatabase.query).toHaveBeenCalledWith('SELECT * FROM users WHERE id = 1');
      expect(mockDatabase.query).toHaveBeenCalledTimes(1);
      expect(user).toBeInstanceOf(User);
      expect(user.id).toBe(1);
      expect(user.name).toBe('Alice');
      expect(user.email).toBe('alice@example.com');
      expect(user.isActive).toBe(true);
    });

    test('should handle database errors', async () => {
      // Arrange
      mockDatabase.query.mockRejectedValue(new Error('Database connection failed'));

      // Act & Assert
      await expect(userRepository.getUserById(1)).rejects.toThrow(
        'Database connection failed'
      );
    });
  });

  describe('saveUser', () => {
    test('should save user to database', async () => {
      // Arrange
      const user = new User(1, 'Bob', 'bob@example.com');
      mockDatabase.execute.mockResolvedValue(true);

      // Act
      const result = await userRepository.saveUser(user);

      // Assert
      expect(mockDatabase.execute).toHaveBeenCalledTimes(1);
      expect(result).toBe(true);
    });
  });
});

// ===== Async Tests =====

describe('ApiService', () => {
  let apiService;

  beforeEach(() => {
    apiService = new ApiService();
  });

  describe('fetchData', () => {
    test('should fetch data successfully', async () => {
      // Arrange
      const mockData = { id: 1, name: 'Test' };
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: true,
          json: () => Promise.resolve(mockData),
        })
      );

      // Act
      const result = await apiService.fetchData('https://api.example.com/data');

      // Assert
      expect(fetch).toHaveBeenCalledWith('https://api.example.com/data');
      expect(result).toEqual(mockData);
    });

    test('should throw error on HTTP failure', async () => {
      // Arrange
      global.fetch = jest.fn(() =>
        Promise.resolve({
          ok: false,
          status: 404,
        })
      );

      // Act & Assert
      await expect(apiService.fetchData('https://api.example.com/data')).rejects.toThrow(
        'HTTP error! status: 404'
      );
    });

    test('should handle network errors', async () => {
      // Arrange
      global.fetch = jest.fn(() => Promise.reject(new Error('Network error')));

      // Act & Assert
      await expect(apiService.fetchData('https://api.example.com/data')).rejects.toThrow(
        'Network error'
      );
    });
  });
});

// ===== User Class Tests =====

describe('User', () => {
  describe('constructor', () => {
    test('should create user with correct properties', () => {
      const user = new User(1, 'Alice', 'alice@example.com');

      expect(user.id).toBe(1);
      expect(user.name).toBe('Alice');
      expect(user.email).toBe('alice@example.com');
      expect(user.isActive).toBe(true);
    });

    test('should create inactive user when specified', () => {
      const user = new User(1, 'Bob', 'bob@example.com', false);

      expect(user.isActive).toBe(false);
    });
  });

  describe('deactivate', () => {
    test('should deactivate user', () => {
      const user = new User(1, 'Alice', 'alice@example.com');

      user.deactivate();

      expect(user.isActive).toBe(false);
    });
  });

  describe('getDisplayName', () => {
    test('should return formatted display name', () => {
      const user = new User(1, 'Alice', 'alice@example.com');

      const displayName = user.getDisplayName();

      expect(displayName).toBe('Alice (alice@example.com)');
    });

    test('should match snapshot', () => {
      const user = new User(1, 'Alice', 'alice@example.com');

      expect(user.getDisplayName()).toMatchSnapshot();
    });
  });
});

// ===== Spy Tests =====

describe('Spies', () => {
  test('should spy on method calls', () => {
    const user = new User(1, 'Alice', 'alice@example.com');
    const spy = jest.spyOn(user, 'getDisplayName');

    user.getDisplayName();

    expect(spy).toHaveBeenCalled();
    expect(spy).toHaveBeenCalledTimes(1);

    spy.mockRestore(); // Clean up spy
  });

  test('should mock method return value', () => {
    const user = new User(1, 'Alice', 'alice@example.com');
    const spy = jest.spyOn(user, 'getDisplayName').mockReturnValue('Mocked Name');

    const displayName = user.getDisplayName();

    expect(displayName).toBe('Mocked Name');

    spy.mockRestore();
  });
});

// ===== Timer Mocks =====

describe('Timer Mocks', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('should execute callback after timeout', () => {
    const callback = jest.fn();

    setTimeout(callback, 1000);

    expect(callback).not.toHaveBeenCalled();

    jest.advanceTimersByTime(1000);

    expect(callback).toHaveBeenCalled();
    expect(callback).toHaveBeenCalledTimes(1);
  });

  test('should execute multiple timeouts', () => {
    const callback1 = jest.fn();
    const callback2 = jest.fn();

    setTimeout(callback1, 1000);
    setTimeout(callback2, 2000);

    jest.advanceTimersByTime(1500);

    expect(callback1).toHaveBeenCalled();
    expect(callback2).not.toHaveBeenCalled();

    jest.advanceTimersByTime(500);

    expect(callback2).toHaveBeenCalled();
  });
});

// ===== Test Organization Best Practices =====
//
// 1. Use describe blocks to group related tests
// 2. Use beforeEach/afterEach for setup/teardown
// 3. Use clear, descriptive test names
// 4. Follow AAA pattern: Arrange, Act, Assert
// 5. Keep tests independent and isolated
// 6. Mock external dependencies
// 7. Test edge cases and error conditions
// 8. Use parametrized tests for similar test cases
// 9. Aim for >80% code coverage
// 10. Keep tests fast and focused

// ===== Jest Matchers Reference =====
//
// Common Matchers:
// - expect(value).toBe(expected)              // Strict equality (===)
// - expect(value).toEqual(expected)           // Deep equality
// - expect(value).toBeTruthy()                // Truthy value
// - expect(value).toBeFalsy()                 // Falsy value
// - expect(value).toBeNull()                  // Null value
// - expect(value).toBeUndefined()             // Undefined value
// - expect(value).toBeDefined()               // Defined value
// - expect(fn).toThrow()                      // Function throws error
// - expect(fn).toThrow('error message')       // Function throws specific error
// - expect(array).toContain(item)             // Array contains item
// - expect(string).toMatch(/regex/)           // String matches regex
// - expect(fn).toHaveBeenCalled()             // Mock was called
// - expect(fn).toHaveBeenCalledWith(arg)      // Mock called with argument
// - expect(fn).toHaveBeenCalledTimes(n)       // Mock called n times
// - expect(promise).resolves.toBe(value)      // Promise resolves to value
// - expect(promise).rejects.toThrow()         // Promise rejects with error

module.exports = {
  Calculator,
  User,
  UserRepository,
  ApiService,
};
