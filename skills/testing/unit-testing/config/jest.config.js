/**
 * Jest Configuration for JavaScript/TypeScript Projects
 *
 * This configuration defines Jest behavior, test discovery, coverage settings,
 * and reporter options for comprehensive unit testing.
 *
 * @see https://jestjs.io/docs/configuration
 */

module.exports = {
  // ===== Test Environment =====

  // Test environment (node, jsdom, or custom)
  testEnvironment: 'node',

  // Custom test environment options
  testEnvironmentOptions: {
    // url: 'http://localhost',
  },

  // ===== Test Discovery =====

  // Root directories for tests and modules
  roots: ['<rootDir>/src', '<rootDir>/tests'],

  // Test file patterns
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],

  // Patterns to ignore
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/build/',
    '/coverage/',
  ],

  // ===== Module Resolution =====

  // Module file extensions
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'node'],

  // Module name mapper (for path aliases)
  moduleNameMapper: {
    // Handle module aliases (update to match your paths)
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',
    '^@services/(.*)$': '<rootDir>/src/services/$1',
    '^@models/(.*)$': '<rootDir>/src/models/$1',

    // Handle CSS imports (with CSS modules)
    '\\.module\\.(css|less|sass|scss)$': 'identity-obj-proxy',

    // Handle CSS imports (without CSS modules)
    '\\.(css|less|sass|scss)$': '<rootDir>/__mocks__/styleMock.js',

    // Handle image imports
    '\\.(jpg|jpeg|png|gif|svg|webp)$': '<rootDir>/__mocks__/fileMock.js',
  },

  // Directories to search for modules
  modulePaths: ['<rootDir>/src'],

  // ===== Transforms =====

  // Transform files with babel-jest or ts-jest
  transform: {
    '^.+\\.(js|jsx)$': 'babel-jest',
    '^.+\\.(ts|tsx)$': 'ts-jest',
  },

  // Files to transform
  transformIgnorePatterns: [
    '/node_modules/(?!(module-to-transform)/)',
  ],

  // ===== Coverage Configuration =====

  // Collect coverage from these files
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.{js,jsx,ts,tsx}',
    '!src/**/__tests__/**',
    '!src/**/__mocks__/**',
    '!src/index.{js,jsx,ts,tsx}',
    '!src/setupTests.{js,ts}',
  ],

  // Coverage thresholds (fail if below these percentages)
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
    // Per-file thresholds
    './src/utils/': {
      branches: 90,
      functions: 90,
      lines: 90,
      statements: 90,
    },
  },

  // Coverage reporters
  coverageReporters: [
    'text',
    'text-summary',
    'html',
    'lcov',
    'json',
    'clover',
  ],

  // Coverage output directory
  coverageDirectory: 'coverage',

  // Paths to ignore for coverage
  coveragePathIgnorePatterns: [
    '/node_modules/',
    '/tests/',
    '/__tests__/',
    '/__mocks__/',
    '/dist/',
    '/build/',
  ],

  // ===== Setup Files =====

  // Setup files before tests run
  setupFiles: [
    // '<rootDir>/tests/setup.js',
  ],

  // Setup files after environment is set up
  setupFilesAfterEnv: [
    // '<rootDir>/tests/setupAfterEnv.js',
    // '@testing-library/jest-dom',
  ],

  // ===== Global Configuration =====

  // Global variables
  globals: {
    'ts-jest': {
      tsconfig: {
        jsx: 'react',
        esModuleInterop: true,
      },
    },
  },

  // ===== Test Execution =====

  // Maximum number of workers (default: number of CPUs - 1)
  maxWorkers: '50%',

  // Maximum concurrent tests per worker
  maxConcurrency: 5,

  // Bail after n test failures (0 = run all tests)
  bail: 0,

  // Verbose output
  verbose: true,

  // Clear mocks between tests
  clearMocks: true,

  // Reset mocks between tests
  resetMocks: false,

  // Restore mocks between tests
  restoreMocks: true,

  // ===== Timeouts =====

  // Test timeout in milliseconds (default: 5000)
  testTimeout: 10000,

  // ===== Reporters =====

  // Reporters for test results
  reporters: [
    'default',
    // JUnit reporter for CI/CD
    [
      'jest-junit',
      {
        outputDirectory: './test-results',
        outputName: 'junit.xml',
        classNameTemplate: '{classname}',
        titleTemplate: '{title}',
        ancestorSeparator: ' › ',
        usePathForSuiteName: true,
      },
    ],
    // HTML reporter
    [
      'jest-html-reporter',
      {
        pageTitle: 'Test Report',
        outputPath: './test-results/test-report.html',
        includeFailureMsg: true,
        includeConsoleLog: true,
        sort: 'status',
      },
    ],
  ],

  // ===== Watch Mode =====

  // Watch plugins
  watchPlugins: [
    'jest-watch-typeahead/filename',
    'jest-watch-typeahead/testname',
  ],

  // Patterns to ignore in watch mode
  watchPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/build/',
  ],

  // ===== Snapshot Testing =====

  // Snapshot resolver (custom snapshot location)
  // snapshotResolver: '<rootDir>/tests/snapshotResolver.js',

  // Snapshot serializers
  snapshotSerializers: [
    // 'enzyme-to-json/serializer',
  ],

  // ===== Miscellaneous =====

  // Automatically clear mock calls and instances between tests
  clearMocks: true,

  // Indicates whether each test should be reported during execution
  notify: false,

  // Notify on failure only
  notifyMode: 'failure-change',

  // Error on deprecated APIs
  errorOnDeprecated: true,

  // Prevent tests from printing messages through the console
  silent: false,

  // The number of seconds before test timeout
  slowTestThreshold: 5,

  // Stop running tests after the first failure
  // bail: 1,

  // Force exit after tests complete
  forceExit: false,

  // Detect memory leaks in tests
  detectLeaks: false,

  // Detect open handles preventing Jest from exiting
  detectOpenHandles: false,

  // ===== Cache =====

  // Cache directory
  cacheDirectory: '/tmp/jest_cache',

  // ===== Projects (for monorepos) =====

  // projects: [
  //   {
  //     displayName: 'client',
  //     testMatch: ['<rootDir>/packages/client/**/*.test.js'],
  //   },
  //   {
  //     displayName: 'server',
  //     testMatch: ['<rootDir>/packages/server/**/*.test.js'],
  //   },
  // ],

  // ===== Example Commands =====
  //
  // Run all tests:
  //   npm test
  //   jest
  //
  // Run tests in watch mode:
  //   npm test -- --watch
  //   jest --watch
  //
  // Run tests with coverage:
  //   npm test -- --coverage
  //   jest --coverage
  //
  // Run specific test file:
  //   npm test -- path/to/test.js
  //   jest path/to/test.js
  //
  // Run tests matching pattern:
  //   npm test -- --testNamePattern="should add"
  //   jest -t "should add"
  //
  // Update snapshots:
  //   npm test -- -u
  //   jest --updateSnapshot
  //
  // Run tests in CI mode:
  //   npm test -- --ci
  //   jest --ci
  //
  // Clear cache:
  //   npm test -- --clearCache
  //   jest --clearCache
  //
  // Show test configuration:
  //   jest --showConfig
  //
  // Debug tests:
  //   node --inspect-brk node_modules/.bin/jest --runInBand
};
