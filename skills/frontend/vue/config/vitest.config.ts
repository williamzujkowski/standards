/**
 * Vitest Configuration for Vue 3 Projects
 * Features: Vue component testing, coverage, mocking, TypeScript support
 */

import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

export default defineConfig({
  plugins: [vue()],

  test: {
    // ========================================================================
    // Environment Configuration
    // ========================================================================

    // Use jsdom for DOM testing
    environment: 'jsdom',

    // Global test utilities
    globals: true,

    // ========================================================================
    // Setup Files
    // ========================================================================

    // Run before each test file
    setupFiles: ['./tests/setup.ts'],

    // ========================================================================
    // Coverage Configuration
    // ========================================================================

    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html', 'lcov'],

      // Coverage thresholds
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      },

      // Files to include/exclude
      include: ['src/**/*.{ts,tsx,vue}'],
      exclude: [
        'node_modules/',
        'tests/',
        '**/*.d.ts',
        '**/*.config.ts',
        '**/mockData/',
        '**/*.test.ts'
      ],

      // Clean coverage directory before running tests
      clean: true
    },

    // ========================================================================
    // Test Matching
    // ========================================================================

    // Test file patterns
    include: [
      '**/*.test.ts',
      '**/*.spec.ts',
      '**/__tests__/**/*.ts'
    ],

    exclude: [
      'node_modules',
      'dist',
      '.idea',
      '.git',
      '.cache'
    ],

    // ========================================================================
    // Performance & Behavior
    // ========================================================================

    // Test timeout (milliseconds)
    testTimeout: 10000,

    // Hook timeout
    hookTimeout: 10000,

    // Run tests in parallel
    threads: true,

    // Maximum number of threads
    maxThreads: 4,

    // Minimum number of threads
    minThreads: 1,

    // Isolate environment for each test file
    isolate: true,

    // ========================================================================
    // Reporting
    // ========================================================================

    reporters: ['default', 'html'],

    // Output file for HTML reporter
    outputFile: {
      html: './coverage/test-report.html'
    },

    // ========================================================================
    // Mocking
    // ========================================================================

    // Mock CSS modules
    css: {
      modules: {
        classNameStrategy: 'non-scoped'
      }
    },

    // Mock configuration
    mockReset: true,
    restoreMocks: true,
    clearMocks: true,

    // ========================================================================
    // Watch Mode
    // ========================================================================

    watch: false, // Disable watch in CI

    // Watch options
    watchExclude: [
      'node_modules',
      'dist',
      'coverage',
      '**/*.md'
    ]
  },

  // ==========================================================================
  // Path Resolution
  // ==========================================================================

  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
      '@components': fileURLToPath(new URL('./src/components', import.meta.url)),
      '@stores': fileURLToPath(new URL('./src/stores', import.meta.url)),
      '@composables': fileURLToPath(new URL('./src/composables', import.meta.url)),
      '@utils': fileURLToPath(new URL('./src/utils', import.meta.url)),
      '@types': fileURLToPath(new URL('./src/types', import.meta.url))
    }
  },

  // ==========================================================================
  // Define Global Constants
  // ==========================================================================

  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false
  }
});

// ============================================================================
// Example tests/setup.ts
// ============================================================================

/*
import { config } from '@vue/test-utils';
import { vi } from 'vitest';

// Mock window.matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(),
  })),
});

// Mock IntersectionObserver
global.IntersectionObserver = class IntersectionObserver {
  constructor() {}
  disconnect() {}
  observe() {}
  takeRecords() { return []; }
  unobserve() {}
};

// Global test utilities
config.global.mocks = {
  $t: (key: string) => key, // Mock i18n
};

// Mock Router
config.global.stubs = {
  RouterLink: true,
  RouterView: true,
};
*/
