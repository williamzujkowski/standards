# E2E Testing Configuration Files

Production-ready configuration files for Playwright and Cypress.

## Files

- `playwright.config.ts` - Playwright configuration with multi-browser support, CI/CD integration, and advanced features
- `cypress.config.ts` - Cypress configuration with component testing, network mocking, and CI/CD support

## Usage

### Playwright

```bash
# Copy to project root
cp playwright.config.ts your-project/

# Install dependencies
npm install -D @playwright/test

# Install browsers
npx playwright install --with-deps

# Run tests
npx playwright test
```

### Cypress

```bash
# Copy to project root
cp cypress.config.ts your-project/

# Install dependencies
npm install -D cypress

# Run tests
npx cypress run
```

## Customization

Both configurations support environment variables:
- `BASE_URL` - Application URL to test
- `CI` - Enables CI-specific settings
- `BROWSER` - Browser to use for tests
