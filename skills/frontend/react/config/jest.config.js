/**
 * Jest Configuration for React with TypeScript
 *
 * Optimized configuration for testing React components with:
 * - TypeScript support via ts-jest
 * - React Testing Library integration
 * - Coverage thresholds
 * - Module path mapping
 * - Transform handling for various file types
 */

module.exports = {
  // Test environment (jsdom for DOM APIs)
  testEnvironment: 'jsdom',

  // Setup files (run before each test)
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],

  // File extensions to look for
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  // Test file patterns
  testMatch: [
    '**/__tests__/**/*.(test|spec).(ts|tsx|js)',
    '**/*.(test|spec).(ts|tsx|js)',
  ],

  // Transform files with ts-jest
  transform: {
    '^.+\\.(ts|tsx)$': ['ts-jest', {
      tsconfig: {
        jsx: 'react',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true,
      },
    }],
  },

  // Module name mapping (for path aliases and assets)
  moduleNameMapper: {
    // Path aliases (adjust to match tsconfig.json)
    '^@/(.*)$': '<rootDir>/src/$1',
    '^@components/(.*)$': '<rootDir>/src/components/$1',
    '^@hooks/(.*)$': '<rootDir>/src/hooks/$1',
    '^@utils/(.*)$': '<rootDir>/src/utils/$1',

    // Style imports (CSS modules)
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',

    // Asset imports (images, fonts, etc.)
    '\\.(jpg|jpeg|png|gif|svg|webp)$': '<rootDir>/__mocks__/fileMock.js',
    '\\.(woff|woff2|eot|ttf|otf)$': '<rootDir>/__mocks__/fileMock.js',
  },

  // Paths to ignore
  testPathIgnorePatterns: [
    '/node_modules/',
    '/build/',
    '/dist/',
    '/.next/',
  ],

  // Coverage configuration
  collectCoverageFrom: [
    'src/**/*.{ts,tsx,js,jsx}',
    '!src/**/*.d.ts',
    '!src/**/*.stories.tsx',
    '!src/index.tsx',
    '!src/reportWebVitals.ts',
    '!src/setupTests.ts',
  ],

  // Coverage thresholds (enforce minimum coverage)
  coverageThresholds: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },

  // Coverage output directory
  coverageDirectory: 'coverage',

  // Coverage reporters
  coverageReporters: ['text', 'lcov', 'html', 'json-summary'],

  // Clear mocks between tests
  clearMocks: true,

  // Reset mocks between tests
  resetMocks: true,

  // Restore mocks between tests
  restoreMocks: true,

  // Timeout for tests (in ms)
  testTimeout: 10000,

  // Verbose output
  verbose: true,

  // Global setup/teardown
  // globalSetup: '<rootDir>/jest.globalSetup.js',
  // globalTeardown: '<rootDir>/jest.globalTeardown.js',

  // Watch plugins
  watchPlugins: [
    'jest-watch-typeahead/filename',
    'jest-watch-typeahead/testname',
  ],

  // Transform ignore patterns (don't transform node_modules except specific packages)
  transformIgnorePatterns: [
    '/node_modules/(?!(nanoid|uuid)/)',
  ],

  // Globals (for ts-jest)
  globals: {
    'ts-jest': {
      isolatedModules: true, // Faster compilation, skip type checking
    },
  },
};

/**
 * Setup Files
 *
 * Create src/setupTests.ts with:
 *
 * ```typescript
 * import '@testing-library/jest-dom';
 *
 * // Mock window.matchMedia
 * Object.defineProperty(window, 'matchMedia', {
 *   writable: true,
 *   value: jest.fn().mockImplementation(query => ({
 *     matches: false,
 *     media: query,
 *     onchange: null,
 *     addListener: jest.fn(),
 *     removeListener: jest.fn(),
 *     addEventListener: jest.fn(),
 *     removeEventListener: jest.fn(),
 *     dispatchEvent: jest.fn(),
 *   })),
 * });
 *
 * // Mock IntersectionObserver
 * global.IntersectionObserver = class IntersectionObserver {
 *   constructor() {}
 *   disconnect() {}
 *   observe() {}
 *   takeRecords() { return []; }
 *   unobserve() {}
 * };
 * ```
 */

/**
 * File Mocks
 *
 * Create __mocks__/fileMock.js with:
 *
 * ```javascript
 * module.exports = 'test-file-stub';
 * ```
 */

/**
 * Package.json Scripts
 *
 * Add these scripts to package.json:
 *
 * ```json
 * {
 *   "scripts": {
 *     "test": "jest",
 *     "test:watch": "jest --watch",
 *     "test:coverage": "jest --coverage",
 *     "test:ci": "jest --ci --coverage --maxWorkers=2"
 *   }
 * }
 * ```
 */

/**
 * Required Dependencies
 *
 * Install these packages:
 *
 * ```bash
 * npm install --save-dev \
 *   jest \
 *   @types/jest \
 *   ts-jest \
 *   @testing-library/react \
 *   @testing-library/jest-dom \
 *   @testing-library/user-event \
 *   jest-environment-jsdom \
 *   identity-obj-proxy \
 *   jest-watch-typeahead
 * ```
 */

/**
 * TypeScript Configuration
 *
 * Ensure tsconfig.json includes:
 *
 * ```json
 * {
 *   "compilerOptions": {
 *     "types": ["jest", "@testing-library/jest-dom"]
 *   }
 * }
 * ```
 */
