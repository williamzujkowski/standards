// Jest configuration
module.exports = {
  // Test environment
  testEnvironment: 'node',

  // Coverage configuration
  coverageDirectory: 'coverage',
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.test.{js,jsx,ts,tsx}',
    '!src/**/__tests__/**',
    '!src/index.{js,ts}',
    '!**/node_modules/**',
    '!**/vendor/**',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  coverageReporters: ['text', 'text-summary', 'html', 'lcov'],

  // Test patterns
  testMatch: [
    '**/__tests__/**/*.[jt]s?(x)',
    '**/?(*.)+(spec|test).[jt]s?(x)',
  ],
  testPathIgnorePatterns: [
    '/node_modules/',
    '/dist/',
    '/build/',
  ],

  // Module resolution
  moduleFileExtensions: ['js', 'jsx', 'ts', 'tsx', 'json', 'node'],
  moduleDirectories: ['node_modules', 'src'],

  // Transform
  transform: {
    '^.+\\.(ts|tsx)$': 'ts-jest',
    '^.+\\.(js|jsx)$': 'babel-jest',
  },

  // Setup
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],

  // Timeouts
  testTimeout: 10000,

  // Reporting
  verbose: true,
  bail: false,
  maxWorkers: '50%',

  // Watch mode
  watchPathIgnorePatterns: [
    '/node_modules/',
    '/coverage/',
  ],
};
