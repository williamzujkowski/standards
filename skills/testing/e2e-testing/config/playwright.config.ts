import { defineConfig, devices } from '@playwright/test';

/**
 * Production-ready Playwright configuration
 * Supports: Multi-browser, CI/CD, Visual regression, Network mocking
 */

export default defineConfig({
  testDir: './tests/e2e',

  // Run tests in files in parallel
  fullyParallel: true,

  // Fail the build on CI if you accidentally left test.only in the source code
  forbidOnly: !!process.env.CI,

  // Retry on CI only
  retries: process.env.CI ? 2 : 0,

  // Opt out of parallel tests on CI
  workers: process.env.CI ? 1 : undefined,

  // Reporter to use
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list'],
  ],

  // Shared settings for all the projects below
  use: {
    // Base URL to use in actions like `await page.goto('/')`
    baseURL: process.env.BASE_URL || 'http://localhost:3000',

    // Collect trace when retrying the failed test
    trace: 'on-first-retry',

    // Screenshot on failure
    screenshot: 'only-on-failure',

    // Video on failure
    video: 'retain-on-failure',

    // Maximum time each action such as `click()` can take
    actionTimeout: 10000,

    // Navigation timeout
    navigationTimeout: 30000,

    // Viewport size
    viewport: { width: 1280, height: 720 },

    // Ignore HTTPS errors
    ignoreHTTPSErrors: true,

    // Locale and timezone
    locale: 'en-US',
    timezoneId: 'America/New_York',

    // Permissions
    permissions: [],

    // Geolocation
    // geolocation: { longitude: -74.006, latitude: 40.7128 },

    // Color scheme
    colorScheme: 'light',
  },

  // Configure projects for major browsers
  projects: [
    // Setup project - runs once before all tests
    {
      name: 'setup',
      testMatch: /global\.setup\.ts/,
    },

    // Desktop browsers
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        // Use saved authentication state
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'firefox',
      use: {
        ...devices['Desktop Firefox'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'webkit',
      use: {
        ...devices['Desktop Safari'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Mobile browsers
    {
      name: 'mobile-chrome',
      use: {
        ...devices['Pixel 5'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    {
      name: 'mobile-safari',
      use: {
        ...devices['iPhone 12'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Tablet
    {
      name: 'tablet',
      use: {
        ...devices['iPad Pro'],
        storageState: 'playwright/.auth/user.json',
      },
      dependencies: ['setup'],
    },

    // Branded tests - tests that require specific browser features
    {
      name: 'chromium-branded',
      use: {
        ...devices['Desktop Chrome'],
        channel: 'chrome',
      },
      testMatch: /.*\.chrome\.spec\.ts/,
    },

    {
      name: 'edge-branded',
      use: {
        ...devices['Desktop Edge'],
        channel: 'msedge',
      },
      testMatch: /.*\.edge\.spec\.ts/,
    },
  ],

  // Global setup/teardown
  globalSetup: require.resolve('./tests/global-setup'),
  globalTeardown: require.resolve('./tests/global-teardown'),

  // Run your local dev server before starting the tests
  webServer: {
    command: 'npm run start',
    port: 3000,
    timeout: 120 * 1000,
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'pipe',
  },

  // Test timeouts
  timeout: 30 * 1000,
  expect: {
    timeout: 5000,
    toHaveScreenshot: {
      maxDiffPixels: 100,
      threshold: 0.2,
    },
  },

  // Global test options
  grep: process.env.TEST_TAG ? new RegExp(process.env.TEST_TAG) : undefined,
  grepInvert: process.env.SKIP_TAG ? new RegExp(process.env.SKIP_TAG) : undefined,
});
