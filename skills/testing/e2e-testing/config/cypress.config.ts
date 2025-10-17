import { defineConfig } from 'cypress';

/**
 * Production-ready Cypress configuration
 * Supports: Component testing, Network mocking, CI/CD, Video recording
 */

export default defineConfig({
  // E2E Testing configuration
  e2e: {
    baseUrl: process.env.BASE_URL || 'http://localhost:3000',

    // Viewport settings
    viewportWidth: 1280,
    viewportHeight: 720,

    // Video and screenshot settings
    video: true,
    videoCompression: 32,
    videosFolder: 'cypress/videos',
    screenshotOnRunFailure: true,
    screenshotsFolder: 'cypress/screenshots',

    // Test execution settings
    defaultCommandTimeout: 10000,
    requestTimeout: 10000,
    responseTimeout: 30000,
    pageLoadTimeout: 60000,

    // Retry settings
    retries: {
      runMode: 2,  // Retry 2 times in CI
      openMode: 0, // No retries in interactive mode
    },

    // Spec patterns
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    excludeSpecPattern: [
      '**/__snapshots__/*',
      '**/__image_snapshots__/*',
    ],

    // Support file
    supportFile: 'cypress/support/e2e.ts',

    // Fixtures
    fixturesFolder: 'cypress/fixtures',

    // Downloads
    downloadsFolder: 'cypress/downloads',

    // Test isolation
    testIsolation: true,

    // Browser launch options
    chromeWebSecurity: false,

    // Experimental features
    experimentalRunAllSpecs: true,
    experimentalMemoryManagement: true,

    setupNodeEvents(on, config) {
      // Implement node event listeners here

      // Task examples
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },

        // Database tasks
        async 'db:seed'() {
          // Seed database
          return null;
        },

        async 'db:reset'() {
          // Reset database
          return null;
        },

        // File system tasks
        async 'readFileMaybe'(filename: string) {
          const fs = require('fs');
          if (fs.existsSync(filename)) {
            return fs.readFileSync(filename, 'utf8');
          }
          return null;
        },
      });

      // Before/after hooks
      on('before:browser:launch', (browser, launchOptions) => {
        if (browser.family === 'chromium' && browser.name !== 'electron') {
          // Add Chrome flags
          launchOptions.args.push('--disable-dev-shm-usage');
          launchOptions.args.push('--disable-gpu');
        }

        if (browser.name === 'electron') {
          // Modify Electron launch options
          launchOptions.preferences.width = 1280;
          launchOptions.preferences.height = 720;
        }

        return launchOptions;
      });

      on('after:screenshot', (details) => {
        console.log('Screenshot taken:', details.path);
      });

      // Environment variables
      config.env = {
        ...config.env,
        apiUrl: process.env.API_URL || 'http://localhost:3001',
        coverage: process.env.COVERAGE === 'true',
      };

      return config;
    },
  },

  // Component Testing configuration
  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
    specPattern: 'src/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/component.ts',
    viewportWidth: 500,
    viewportHeight: 500,
    video: false,
  },

  // Global configuration
  env: {
    // Environment variables accessible via Cypress.env()
    apiUrl: 'http://localhost:3001',
    coverage: false,

    // Custom flags
    skipAuth: false,
    slowMo: 0, // Milliseconds to slow down commands
  },

  // Reporter options
  reporter: 'cypress-multi-reporters',
  reporterOptions: {
    configFile: 'reporter-config.json',
  },

  // Project ID for Cypress Dashboard (optional)
  // projectId: 'your-project-id',
});
