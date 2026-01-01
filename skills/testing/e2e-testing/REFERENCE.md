# E2E Testing Standards - Reference Guide

This reference document contains complete examples, advanced configurations, and production-ready templates for E2E testing with Playwright and Cypress.

## Table of Contents

- [Complete Page Object Examples](#complete-page-object-examples)
- [Full Test Suite Templates](#full-test-suite-templates)
- [Advanced Configuration](#advanced-configuration)
- [Visual Regression Testing](#visual-regression-testing)
- [Cross-Browser Testing](#cross-browser-testing)
- [Docker Integration](#docker-integration)
- [Database Seeding](#database-seeding)
- [CI/CD Complete Workflows](#cicd-complete-workflows)
- [Comprehensive Flakiness Prevention](#comprehensive-flakiness-prevention)

---

## Complete Page Object Examples

### Base Page with Full Utilities

```typescript
// BasePage.ts
import { Page } from '@playwright/test';

export abstract class BasePage {
  constructor(protected page: Page) {}

  async navigate(path: string = '') {
    await this.page.goto(path);
  }

  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  async getPageTitle(): Promise<string> {
    return await this.page.title();
  }

  async takeScreenshot(name: string) {
    await this.page.screenshot({
      path: `screenshots/${name}.png`,
      fullPage: true
    });
  }

  async scrollToElement(selector: string) {
    await this.page.locator(selector).scrollIntoViewIfNeeded();
  }

  async waitForUrl(urlPattern: string | RegExp) {
    await this.page.waitForURL(urlPattern);
  }

  async clearLocalStorage() {
    await this.page.evaluate(() => localStorage.clear());
  }

  async setLocalStorageItem(key: string, value: string) {
    await this.page.evaluate(([k, v]) => localStorage.setItem(k, v), [key, value]);
  }
}
```

### Complete Login Page Object

```typescript
// LoginPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class LoginPage extends BasePage {
  // Locators
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;
  readonly rememberMeCheckbox: Locator;
  readonly socialLoginGoogle: Locator;
  readonly socialLoginGithub: Locator;

  constructor(page: Page) {
    super(page);
    this.usernameInput = page.getByTestId('username-input');
    this.passwordInput = page.getByTestId('password-input');
    this.loginButton = page.getByRole('button', { name: 'Log in' });
    this.errorMessage = page.getByTestId('error-message');
    this.forgotPasswordLink = page.getByRole('link', { name: /forgot password/i });
    this.rememberMeCheckbox = page.getByLabel('Remember me');
    this.socialLoginGoogle = page.getByTestId('google-login');
    this.socialLoginGithub = page.getByTestId('github-login');
  }

  async navigateToLogin() {
    await this.navigate('/login');
    await this.waitForPageLoad();
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  async loginWithRememberMe(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.rememberMeCheckbox.check();
    await this.loginButton.click();
  }

  async loginWithEnter(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.passwordInput.press('Enter');
  }

  async getErrorText(): Promise<string> {
    return await this.errorMessage.textContent() || '';
  }

  async isErrorVisible(): Promise<boolean> {
    return await this.errorMessage.isVisible();
  }

  async clickForgotPassword() {
    await this.forgotPasswordLink.click();
  }

  async loginWithGoogle() {
    await this.socialLoginGoogle.click();
  }

  async loginWithGithub() {
    await this.socialLoginGithub.click();
  }

  async expectLoginSuccess(expectedUrl: string = '/dashboard') {
    await this.page.waitForURL(expectedUrl);
    await expect(this.page).toHaveURL(expectedUrl);
  }

  async expectLoginFailure(expectedError: string) {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.errorMessage).toContainText(expectedError);
  }
}
```

### Dashboard Page Object with Complex Interactions

```typescript
// DashboardPage.ts
import { Page, Locator, expect } from '@playwright/test';
import { BasePage } from './BasePage';

export class DashboardPage extends BasePage {
  readonly welcomeMessage: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;
  readonly navigationItems: Locator;
  readonly notificationBell: Locator;
  readonly notificationCount: Locator;
  readonly searchInput: Locator;
  readonly sidebarToggle: Locator;

  constructor(page: Page) {
    super(page);
    this.welcomeMessage = page.getByTestId('welcome-message');
    this.userMenu = page.getByTestId('user-menu');
    this.logoutButton = page.getByRole('button', { name: 'Logout' });
    this.navigationItems = page.getByRole('navigation').getByRole('link');
    this.notificationBell = page.getByTestId('notification-bell');
    this.notificationCount = page.getByTestId('notification-count');
    this.searchInput = page.getByRole('searchbox');
    this.sidebarToggle = page.getByTestId('sidebar-toggle');
  }

  async navigateToDashboard() {
    await this.navigate('/dashboard');
    await this.waitForPageLoad();
  }

  async getWelcomeText(): Promise<string> {
    return await this.welcomeMessage.textContent() || '';
  }

  async logout() {
    await this.userMenu.click();
    await this.logoutButton.click();
  }

  async navigateTo(linkName: string) {
    await this.page.getByRole('navigation').getByRole('link', { name: linkName }).click();
  }

  async getNotificationCount(): Promise<number> {
    const text = await this.notificationCount.textContent();
    return parseInt(text || '0', 10);
  }

  async openNotifications() {
    await this.notificationBell.click();
    await this.page.waitForSelector('[data-testid="notification-panel"]', { state: 'visible' });
  }

  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchInput.press('Enter');
    await this.page.waitForLoadState('networkidle');
  }

  async toggleSidebar() {
    await this.sidebarToggle.click();
  }

  async expectDashboardLoaded() {
    await expect(this.welcomeMessage).toBeVisible();
    await expect(this.userMenu).toBeVisible();
  }
}
```

### E-Commerce Page Objects

```typescript
// ProductListPage.ts
import { Page, Locator } from '@playwright/test';
import { BasePage } from './BasePage';

export class ProductListPage extends BasePage {
  readonly productCards: Locator;
  readonly filterPanel: Locator;
  readonly sortDropdown: Locator;
  readonly priceRangeMin: Locator;
  readonly priceRangeMax: Locator;
  readonly applyFiltersButton: Locator;
  readonly resultsCount: Locator;
  readonly loadMoreButton: Locator;

  constructor(page: Page) {
    super(page);
    this.productCards = page.getByTestId('product-card');
    this.filterPanel = page.getByTestId('filter-panel');
    this.sortDropdown = page.getByLabel('Sort by');
    this.priceRangeMin = page.getByTestId('price-min');
    this.priceRangeMax = page.getByTestId('price-max');
    this.applyFiltersButton = page.getByRole('button', { name: 'Apply Filters' });
    this.resultsCount = page.getByTestId('results-count');
    this.loadMoreButton = page.getByRole('button', { name: 'Load More' });
  }

  async getProductCount(): Promise<number> {
    return await this.productCards.count();
  }

  async sortBy(option: string) {
    await this.sortDropdown.selectOption(option);
    await this.page.waitForLoadState('networkidle');
  }

  async filterByPriceRange(min: number, max: number) {
    await this.priceRangeMin.fill(min.toString());
    await this.priceRangeMax.fill(max.toString());
    await this.applyFiltersButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async clickProduct(index: number) {
    await this.productCards.nth(index).click();
  }

  async addToCart(productIndex: number) {
    const product = this.productCards.nth(productIndex);
    await product.getByRole('button', { name: 'Add to Cart' }).click();
  }

  async loadMoreProducts() {
    await this.loadMoreButton.click();
    await this.page.waitForLoadState('networkidle');
  }
}

// CartPage.ts
export class CartPage extends BasePage {
  readonly cartItems: Locator;
  readonly totalPrice: Locator;
  readonly checkoutButton: Locator;
  readonly emptyCartMessage: Locator;
  readonly quantityInputs: Locator;

  constructor(page: Page) {
    super(page);
    this.cartItems = page.getByTestId('cart-item');
    this.totalPrice = page.getByTestId('cart-total');
    this.checkoutButton = page.getByRole('button', { name: 'Proceed to Checkout' });
    this.emptyCartMessage = page.getByText('Your cart is empty');
    this.quantityInputs = page.locator('[data-testid="quantity-input"]');
  }

  async getItemCount(): Promise<number> {
    return await this.cartItems.count();
  }

  async getTotalPrice(): Promise<string> {
    return await this.totalPrice.textContent() || '$0.00';
  }

  async updateQuantity(itemIndex: number, quantity: number) {
    await this.quantityInputs.nth(itemIndex).fill(quantity.toString());
    await this.page.waitForLoadState('networkidle');
  }

  async removeItem(itemIndex: number) {
    await this.cartItems.nth(itemIndex).getByRole('button', { name: 'Remove' }).click();
  }

  async proceedToCheckout() {
    await this.checkoutButton.click();
  }
}
```

---

## Full Test Suite Templates

### Complete Authentication Test Suite

```typescript
// auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../page-objects/LoginPage';
import { DashboardPage } from '../page-objects/DashboardPage';
import { testUsers } from '../fixtures/test-data';

test.describe('Authentication', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    await loginPage.navigateToLogin();
  });

  test.describe('Successful Login', () => {
    test('user can login with valid credentials', async ({ page }) => {
      await loginPage.login(testUsers.user.email, testUsers.user.password);
      await loginPage.expectLoginSuccess('/dashboard');
      await dashboardPage.expectDashboardLoaded();
    });

    test('user can login with remember me checked', async ({ page }) => {
      await loginPage.loginWithRememberMe(testUsers.user.email, testUsers.user.password);
      await loginPage.expectLoginSuccess('/dashboard');

      // Verify session persists
      await page.reload();
      await dashboardPage.expectDashboardLoaded();
    });

    test('user can login by pressing Enter', async ({ page }) => {
      await loginPage.loginWithEnter(testUsers.user.email, testUsers.user.password);
      await loginPage.expectLoginSuccess('/dashboard');
    });

    test('admin user sees admin dashboard', async ({ page }) => {
      await loginPage.login(testUsers.admin.email, testUsers.admin.password);
      await expect(page).toHaveURL('/admin/dashboard');
    });
  });

  test.describe('Failed Login', () => {
    test('shows error for invalid credentials', async () => {
      await loginPage.login('invalid@example.com', 'wrongpassword');
      await loginPage.expectLoginFailure('Invalid email or password');
    });

    test('shows error for empty email', async () => {
      await loginPage.login('', testUsers.user.password);
      await loginPage.expectLoginFailure('Email is required');
    });

    test('shows error for empty password', async () => {
      await loginPage.login(testUsers.user.email, '');
      await loginPage.expectLoginFailure('Password is required');
    });

    test('shows error for invalid email format', async () => {
      await loginPage.login('notanemail', testUsers.user.password);
      await loginPage.expectLoginFailure('Please enter a valid email');
    });
  });

  test.describe('Password Reset', () => {
    test('user can navigate to forgot password page', async ({ page }) => {
      await loginPage.clickForgotPassword();
      await expect(page).toHaveURL('/forgot-password');
    });
  });

  test.describe('Logout', () => {
    test('user can logout successfully', async ({ page }) => {
      await loginPage.login(testUsers.user.email, testUsers.user.password);
      await loginPage.expectLoginSuccess('/dashboard');

      await dashboardPage.logout();
      await expect(page).toHaveURL('/login');
    });

    test('cannot access dashboard after logout', async ({ page }) => {
      await loginPage.login(testUsers.user.email, testUsers.user.password);
      await loginPage.expectLoginSuccess('/dashboard');

      await dashboardPage.logout();
      await page.goto('/dashboard');
      await expect(page).toHaveURL('/login');
    });
  });
});
```

### E-Commerce Purchase Flow Test Suite

```typescript
// purchase-flow.spec.ts
import { test, expect } from '@playwright/test';
import { ProductListPage } from '../page-objects/ProductListPage';
import { CartPage } from '../page-objects/CartPage';
import { CheckoutPage } from '../page-objects/CheckoutPage';
import { testProducts, testUsers } from '../fixtures/test-data';

test.describe('E-Commerce Purchase Flow', () => {
  test.describe('Product Browsing', () => {
    test('user can view product list', async ({ page }) => {
      const productListPage = new ProductListPage(page);
      await productListPage.navigate('/products');

      const count = await productListPage.getProductCount();
      expect(count).toBeGreaterThan(0);
    });

    test('user can sort products by price', async ({ page }) => {
      const productListPage = new ProductListPage(page);
      await productListPage.navigate('/products');

      await productListPage.sortBy('price-low-high');
      // Verify sorting is applied
      const firstProduct = page.getByTestId('product-card').first();
      await expect(firstProduct).toBeVisible();
    });

    test('user can filter by price range', async ({ page }) => {
      const productListPage = new ProductListPage(page);
      await productListPage.navigate('/products');

      await productListPage.filterByPriceRange(10, 50);
      const count = await productListPage.getProductCount();
      expect(count).toBeGreaterThan(0);
    });
  });

  test.describe('Shopping Cart', () => {
    test('user can add product to cart', async ({ page }) => {
      const productListPage = new ProductListPage(page);
      const cartPage = new CartPage(page);

      await productListPage.navigate('/products');
      await productListPage.addToCart(0);

      await page.goto('/cart');
      const itemCount = await cartPage.getItemCount();
      expect(itemCount).toBe(1);
    });

    test('user can update quantity in cart', async ({ page }) => {
      const cartPage = new CartPage(page);

      // Setup: Add item via API
      await page.request.post('/api/cart', {
        data: { productId: 1, quantity: 1 }
      });

      await page.goto('/cart');
      await cartPage.updateQuantity(0, 3);

      const total = await cartPage.getTotalPrice();
      expect(total).not.toBe('$0.00');
    });

    test('user can remove item from cart', async ({ page }) => {
      const cartPage = new CartPage(page);

      // Setup
      await page.request.post('/api/cart', {
        data: { productId: 1, quantity: 1 }
      });

      await page.goto('/cart');
      await cartPage.removeItem(0);

      await expect(cartPage.emptyCartMessage).toBeVisible();
    });
  });

  test.describe('Checkout Process', () => {
    test.beforeEach(async ({ page }) => {
      // Setup: Add items to cart and login
      await page.request.post('/api/cart', {
        data: { productId: 1, quantity: 2 }
      });
    });

    test('user can complete checkout', async ({ page }) => {
      const cartPage = new CartPage(page);

      await page.goto('/cart');
      await cartPage.proceedToCheckout();

      await expect(page).toHaveURL('/checkout');

      // Fill shipping info
      await page.getByLabel('Full Name').fill('Test User');
      await page.getByLabel('Address').fill('123 Test St');
      await page.getByLabel('City').fill('Test City');
      await page.getByLabel('Zip Code').fill('12345');

      // Complete order
      await page.getByRole('button', { name: 'Place Order' }).click();

      await expect(page).toHaveURL(/\/order-confirmation/);
      await expect(page.getByText('Thank you for your order')).toBeVisible();
    });
  });
});
```

---

## Advanced Configuration

### Complete Playwright Configuration

```typescript
// playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  reporter: [
    ['html', { open: 'never' }],
    ['junit', { outputFile: 'test-results/junit.xml' }],
    ['json', { outputFile: 'test-results/results.json' }],
    ['list'],
  ],

  globalSetup: require.resolve('./tests/global-setup'),
  globalTeardown: require.resolve('./tests/global-teardown'),

  use: {
    baseURL: process.env.BASE_URL || 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',

    // Browser context options
    viewport: { width: 1280, height: 720 },
    ignoreHTTPSErrors: true,

    // Authentication
    storageState: 'playwright/.auth/user.json',

    // Timeouts
    actionTimeout: 10000,
    navigationTimeout: 30000,
  },

  timeout: 60000,
  expect: {
    timeout: 10000,
  },

  projects: [
    // Setup project for authentication
    {
      name: 'setup',
      testMatch: /.*\.setup\.ts/,
      teardown: 'cleanup',
    },
    {
      name: 'cleanup',
      testMatch: /.*\.teardown\.ts/,
    },

    // Desktop browsers
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
      dependencies: ['setup'],
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
      dependencies: ['setup'],
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
      dependencies: ['setup'],
    },

    // Mobile browsers
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
      dependencies: ['setup'],
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
      dependencies: ['setup'],
    },

    // Branded browsers
    {
      name: 'Microsoft Edge',
      use: { ...devices['Desktop Edge'], channel: 'msedge' },
      dependencies: ['setup'],
    },
    {
      name: 'Google Chrome',
      use: { ...devices['Desktop Chrome'], channel: 'chrome' },
      dependencies: ['setup'],
    },
  ],

  webServer: {
    command: 'npm run start:test',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

### Complete Cypress Configuration

```typescript
// cypress.config.ts
import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:3000',
    viewportWidth: 1280,
    viewportHeight: 720,
    video: true,
    screenshotOnRunFailure: true,
    trashAssetsBeforeRuns: true,

    // Timeouts
    defaultCommandTimeout: 10000,
    pageLoadTimeout: 30000,
    requestTimeout: 10000,
    responseTimeout: 30000,

    // Retries
    retries: {
      runMode: 2,
      openMode: 0,
    },

    // Test files
    specPattern: 'cypress/e2e/**/*.cy.{js,jsx,ts,tsx}',
    supportFile: 'cypress/support/e2e.ts',

    // Environment
    env: {
      apiUrl: 'http://localhost:3000/api',
      coverage: true,
    },

    setupNodeEvents(on, config) {
      // Code coverage
      require('@cypress/code-coverage/task')(on, config);

      // Custom tasks
      on('task', {
        log(message) {
          console.log(message);
          return null;
        },
        async seedDatabase() {
          // Database seeding logic
          return null;
        },
        async clearDatabase() {
          // Database cleanup logic
          return null;
        },
      });

      return config;
    },
  },

  component: {
    devServer: {
      framework: 'react',
      bundler: 'vite',
    },
  },
});
```

---

## Visual Regression Testing

### Playwright Visual Comparisons

```typescript
import { test, expect } from '@playwright/test';

test.describe('Visual Regression', () => {
  test('homepage visual regression', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    await expect(page).toHaveScreenshot('homepage.png', {
      maxDiffPixels: 100,
      threshold: 0.2,
      animations: 'disabled',
    });
  });

  test('component visual regression', async ({ page }) => {
    await page.goto('/products');
    const productCard = page.locator('[data-testid="product-card"]').first();

    await expect(productCard).toHaveScreenshot('product-card.png', {
      maxDiffPixelRatio: 0.05,
    });
  });

  test('responsive visual regression', async ({ page }) => {
    const viewports = [
      { width: 375, height: 667, name: 'mobile' },
      { width: 768, height: 1024, name: 'tablet' },
      { width: 1920, height: 1080, name: 'desktop' },
    ];

    for (const viewport of viewports) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto('/');
      await expect(page).toHaveScreenshot(`homepage-${viewport.name}.png`);
    }
  });

  test('dark mode visual regression', async ({ page }) => {
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto('/');
    await expect(page).toHaveScreenshot('homepage-dark.png');
  });
});
```

### Percy Integration

```typescript
// With Percy for cross-browser visual testing
import percySnapshot from '@percy/playwright';

test('visual test with Percy', async ({ page }) => {
  await page.goto('/');
  await percySnapshot(page, 'Homepage');

  // With options
  await percySnapshot(page, 'Homepage - Logged In', {
    widths: [375, 768, 1280],
    minHeight: 1024,
    percyCSS: '.dynamic-content { visibility: hidden; }',
  });
});
```

**Update Baselines**

```bash
# Generate new baseline screenshots
npx playwright test --update-snapshots

# Update specific test
npx playwright test homepage.spec.ts --update-snapshots

# Run with Percy
PERCY_TOKEN=your_token npx percy exec -- playwright test
```

---

## Cross-Browser Testing

### Browser-Specific Tests

```typescript
test('feature only available in chromium', async ({ page, browserName }) => {
  test.skip(browserName !== 'chromium', 'Chromium-only feature');

  await page.goto('/chrome-features');
  // Test chromium-specific feature
});

test('webkit-specific behavior', async ({ page, browserName }) => {
  test.skip(browserName !== 'webkit', 'WebKit-only test');

  await page.goto('/');
  // Test webkit-specific behavior
});

test('responsive behavior varies by browser', async ({ page, browserName }) => {
  await page.goto('/responsive');

  if (browserName === 'webkit') {
    // Safari-specific assertions
    await expect(page.locator('.safari-only')).toBeVisible();
  } else {
    await expect(page.locator('.safari-only')).not.toBeVisible();
  }
});
```

### Running Cross-Browser Tests

```bash
# All browsers
npx playwright test

# Specific browser
npx playwright test --project=firefox

# Multiple browsers
npx playwright test --project=chromium --project=webkit

# Mobile browsers only
npx playwright test --project='Mobile*'
```

---

## Docker Integration

### Dockerfile for E2E Tests

```dockerfile
# Dockerfile.e2e
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app

# Copy package files
COPY package*.json ./
RUN npm ci

# Copy source and tests
COPY . .

# Run tests
CMD ["npx", "playwright", "test"]
```

### Docker Compose for Full Stack Testing

```yaml
# docker-compose.e2e.yml
version: '3.8'

services:
  # Database
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: testdb
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test"]
      interval: 5s
      timeout: 5s
      retries: 5

  # Application
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=test
      - DATABASE_URL=postgresql://test:test@postgres:5432/testdb
    depends_on:
      postgres:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 10s
      timeout: 5s
      retries: 5

  # E2E Tests
  e2e-tests:
    build:
      context: .
      dockerfile: Dockerfile.e2e
    depends_on:
      app:
        condition: service_healthy
    environment:
      - BASE_URL=http://app:3000
      - CI=true
    volumes:
      - ./test-results:/app/test-results
      - ./playwright-report:/app/playwright-report
    command: npx playwright test --reporter=html
```

### E2E Test Runner Script

```bash
#!/bin/bash
# scripts/run-e2e-tests.sh

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}Starting E2E test environment...${NC}"

# Clean up from previous runs
docker-compose -f docker-compose.e2e.yml down -v

# Build and start services
docker-compose -f docker-compose.e2e.yml build
docker-compose -f docker-compose.e2e.yml up -d postgres app

# Wait for app to be ready
echo -e "${YELLOW}Waiting for application to be ready...${NC}"
timeout 60 bash -c 'until curl -s http://localhost:3000/health; do sleep 2; done'

# Run E2E tests
echo -e "${YELLOW}Running E2E tests...${NC}"
docker-compose -f docker-compose.e2e.yml run --rm e2e-tests

# Capture exit code
EXIT_CODE=$?

# Clean up
echo -e "${YELLOW}Cleaning up...${NC}"
docker-compose -f docker-compose.e2e.yml down -v

if [ $EXIT_CODE -eq 0 ]; then
  echo -e "${GREEN}E2E tests passed!${NC}"
else
  echo -e "${RED}E2E tests failed!${NC}"
fi

exit $EXIT_CODE
```

---

## Database Seeding

### Complete Database Helper

```typescript
// helpers/database.ts
import { PrismaClient } from '@prisma/client';
import { testUsers, testProducts } from '../fixtures/test-data';

export class TestDatabase {
  private prisma: PrismaClient;

  constructor() {
    this.prisma = new PrismaClient();
  }

  async connect() {
    await this.prisma.$connect();
  }

  async disconnect() {
    await this.prisma.$disconnect();
  }

  async seed() {
    // Clear existing data
    await this.reset();

    // Seed users
    await this.prisma.user.createMany({
      data: Object.values(testUsers).map(user => ({
        email: user.email,
        password: await hashPassword(user.password),
        role: user.role,
      })),
    });

    // Seed products
    await this.prisma.product.createMany({
      data: testProducts,
    });

    // Seed categories
    await this.prisma.category.createMany({
      data: [
        { id: 1, name: 'Electronics' },
        { id: 2, name: 'Clothing' },
        { id: 3, name: 'Books' },
      ],
    });
  }

  async reset() {
    // Delete in order to respect foreign keys
    await this.prisma.orderItem.deleteMany();
    await this.prisma.order.deleteMany();
    await this.prisma.cartItem.deleteMany();
    await this.prisma.cart.deleteMany();
    await this.prisma.product.deleteMany();
    await this.prisma.category.deleteMany();
    await this.prisma.user.deleteMany();
  }

  async cleanup() {
    await this.reset();
    await this.disconnect();
  }

  // Helper methods for tests
  async createUser(data: Partial<User>) {
    return this.prisma.user.create({ data: { ...testUsers.user, ...data } });
  }

  async createProduct(data: Partial<Product>) {
    return this.prisma.product.create({ data: { ...testProducts[0], ...data } });
  }

  async createOrder(userId: string, items: { productId: number; quantity: number }[]) {
    return this.prisma.order.create({
      data: {
        userId,
        items: {
          create: items.map(item => ({
            productId: item.productId,
            quantity: item.quantity,
          })),
        },
      },
    });
  }
}

// Global setup/teardown
export async function globalSetup() {
  const db = new TestDatabase();
  await db.connect();
  await db.seed();
  await db.disconnect();
}

export async function globalTeardown() {
  const db = new TestDatabase();
  await db.connect();
  await db.cleanup();
}
```

### Using Database in Tests

```typescript
// Using fixtures with database
import { test as base } from '@playwright/test';
import { TestDatabase } from '../helpers/database';

type TestFixtures = {
  db: TestDatabase;
  authenticatedUser: { token: string; userId: string };
};

export const test = base.extend<TestFixtures>({
  db: async ({}, use) => {
    const db = new TestDatabase();
    await db.connect();
    await use(db);
    await db.disconnect();
  },

  authenticatedUser: async ({ request, db }, use) => {
    // Create unique user for this test
    const email = `test-${Date.now()}@example.com`;
    const user = await db.createUser({ email });

    // Get auth token
    const response = await request.post('/api/auth/login', {
      data: { email, password: 'Test123!' },
    });
    const { token } = await response.json();

    await use({ token, userId: user.id });

    // Cleanup
    await db.prisma.user.delete({ where: { id: user.id } });
  },
});
```

---

## CI/CD Complete Workflows

### Complete GitHub Actions Workflow

```yaml
# .github/workflows/e2e-tests.yml
name: E2E Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 6 * * *'  # Daily at 6 AM

env:
  CI: true
  DATABASE_URL: postgresql://test:test@localhost:5432/testdb

jobs:
  # Lint and type check first
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run type-check

  # Run E2E tests in parallel across browsers
  e2e:
    needs: lint
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        browser: [chromium, firefox, webkit]
        shard: [1, 2, 3, 4]

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: testdb
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright browser
        run: npx playwright install --with-deps ${{ matrix.browser }}

      - name: Setup database
        run: npm run db:migrate && npm run db:seed

      - name: Start application
        run: npm run start:test &
        env:
          PORT: 3000

      - name: Wait for app
        run: npx wait-on http://localhost:3000 --timeout 60000

      - name: Run E2E tests
        run: npx playwright test --project=${{ matrix.browser }} --shard=${{ matrix.shard }}/4
        env:
          BASE_URL: http://localhost:3000

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report-${{ matrix.browser }}-${{ matrix.shard }}
          path: |
            playwright-report/
            test-results/
          retention-days: 30

      - name: Upload traces on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: traces-${{ matrix.browser }}-${{ matrix.shard }}
          path: test-results/
          retention-days: 7

  # Merge reports and publish
  report:
    needs: e2e
    if: always()
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Download all reports
        uses: actions/download-artifact@v4
        with:
          pattern: playwright-report-*
          path: all-reports

      - name: Merge reports
        run: npx playwright merge-reports --reporter html ./all-reports

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        if: github.ref == 'refs/heads/main'
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./playwright-report
          destination_dir: e2e-report

  # Notify on failure
  notify:
    needs: [e2e, report]
    if: failure() && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - name: Notify Slack
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          fields: repo,message,commit,author,action,eventName
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

---

## Comprehensive Flakiness Prevention

### Common Causes and Solutions

**1. Race Conditions**

```typescript
// Flaky: Might click before element is ready
await page.goto('/dashboard');
await page.click('[data-testid="menu-button"]');

// Stable: Wait for specific state
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
await page.getByTestId('menu-button').click();
```

**2. Timing Issues**

```typescript
// Flaky: Hardcoded wait
await page.fill('[data-testid="search"]', 'query');
await page.waitForTimeout(2000);
await page.click('[data-testid="first-result"]');

// Stable: Wait for specific element
await page.fill('[data-testid="search"]', 'query');
await page.waitForSelector('[data-testid="first-result"]', { state: 'visible' });
await page.click('[data-testid="first-result"]');
```

**3. Test Interdependence**

```typescript
// Flaky: Tests share state
test('create item', async ({ page }) => {
  await page.goto('/items');
  await page.click('[data-testid="add-item"]');
  // Creates item in shared database
});

test('list items', async ({ page }) => {
  await page.goto('/items');
  await expect(page.getByTestId('item-list')).toContainText('New item');
  // Depends on previous test!
});

// Stable: Each test is independent
test('create item', async ({ page, request }) => {
  // Setup via API
  await request.post('/api/items', { data: { name: 'Test Item' } });

  await page.goto('/items');
  await expect(page.getByTestId('item-list')).toContainText('Test Item');

  // Cleanup via API
  await request.delete('/api/items/test-item');
});
```

**4. Animation Interference**

```typescript
// Flaky: Click during animation
await page.click('[data-testid="modal-button"]');
await page.click('[data-testid="modal-close"]');

// Stable: Wait for stable state
await page.click('[data-testid="modal-button"]');
await page.waitForSelector('[data-testid="modal"]', { state: 'visible' });
await page.getByTestId('modal-close').click();
```

**5. Network Instability**

```typescript
// Flaky: Depends on real API
test('loads user data', async ({ page }) => {
  await page.goto('/profile');
  await expect(page.getByTestId('username')).toContainText('John');
});

// Stable: Mock API responses
test('loads user data', async ({ page }) => {
  await page.route('/api/user', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify({ name: 'John', email: 'john@example.com' }),
    });
  });

  await page.goto('/profile');
  await expect(page.getByTestId('username')).toContainText('John');
});
```

### Flakiness Detection Script

```typescript
// scripts/detect-flaky-tests.ts
import { execSync } from 'child_process';

const RUNS = 10;
const results: Record<string, { passed: number; failed: number }> = {};

for (let i = 0; i < RUNS; i++) {
  console.log(`Run ${i + 1}/${RUNS}`);

  try {
    const output = execSync('npx playwright test --reporter=json', {
      encoding: 'utf8',
    });
    const report = JSON.parse(output);

    for (const suite of report.suites) {
      for (const spec of suite.specs) {
        const key = `${suite.title} > ${spec.title}`;
        if (!results[key]) {
          results[key] = { passed: 0, failed: 0 };
        }

        if (spec.ok) {
          results[key].passed++;
        } else {
          results[key].failed++;
        }
      }
    }
  } catch (error) {
    console.error(`Run ${i + 1} failed`);
  }
}

// Report flaky tests
console.log('\n=== Flaky Test Report ===\n');
for (const [test, { passed, failed }] of Object.entries(results)) {
  if (passed > 0 && failed > 0) {
    const flakyRate = (failed / (passed + failed) * 100).toFixed(1);
    console.log(`FLAKY (${flakyRate}%): ${test}`);
    console.log(`  Passed: ${passed}, Failed: ${failed}`);
  }
}
```

---

## Test Data Fixtures

### Complete Fixture File

```typescript
// fixtures/test-data.ts
import { faker } from '@faker-js/faker';

export const testUsers = {
  admin: {
    email: 'admin@test.com',
    password: 'Admin123!',
    role: 'admin',
    firstName: 'Admin',
    lastName: 'User',
  },
  user: {
    email: 'user@test.com',
    password: 'User123!',
    role: 'user',
    firstName: 'Test',
    lastName: 'User',
  },
  guest: {
    email: 'guest@test.com',
    password: 'Guest123!',
    role: 'guest',
  },
};

export const testProducts = [
  { id: 1, name: 'Laptop', price: 999.99, category: 'Electronics', stock: 50 },
  { id: 2, name: 'Mouse', price: 29.99, category: 'Electronics', stock: 200 },
  { id: 3, name: 'Keyboard', price: 79.99, category: 'Electronics', stock: 100 },
  { id: 4, name: 'Monitor', price: 299.99, category: 'Electronics', stock: 30 },
  { id: 5, name: 'Headphones', price: 149.99, category: 'Electronics', stock: 75 },
];

export const testAddresses = {
  valid: {
    street: '123 Test Street',
    city: 'Test City',
    state: 'TC',
    zip: '12345',
    country: 'Test Country',
  },
  international: {
    street: '456 International Ave',
    city: 'London',
    state: '',
    zip: 'SW1A 1AA',
    country: 'United Kingdom',
  },
};

// Factory functions for dynamic data
export function createRandomUser() {
  return {
    email: faker.internet.email(),
    password: 'Test123!',
    firstName: faker.person.firstName(),
    lastName: faker.person.lastName(),
    phone: faker.phone.number(),
  };
}

export function createRandomProduct() {
  return {
    name: faker.commerce.productName(),
    price: parseFloat(faker.commerce.price()),
    category: faker.commerce.department(),
    description: faker.commerce.productDescription(),
    stock: faker.number.int({ min: 1, max: 100 }),
  };
}

export function createRandomOrder(userId: string, productIds: number[]) {
  return {
    userId,
    items: productIds.map(id => ({
      productId: id,
      quantity: faker.number.int({ min: 1, max: 5 }),
    })),
    shippingAddress: testAddresses.valid,
    paymentMethod: 'card',
  };
}
```

---

## External Resources

### Official Documentation

- **Playwright**: https://playwright.dev/docs/intro
- **Cypress**: https://docs.cypress.io/guides/overview/why-cypress
- **Playwright Best Practices**: https://playwright.dev/docs/best-practices
- **Cypress Best Practices**: https://docs.cypress.io/guides/references/best-practices

### Books and Courses

- "Playwright: The Definitive Guide" by Debbie O'Brien
- "End-to-End Web Testing with Cypress" by Waweru Mwaura
- Test Automation University: https://testautomationu.applitools.com/

### Tools and Extensions

- **Percy** (Visual Testing): https://percy.io/
- **Axe** (Accessibility): https://github.com/dequelabs/axe-core-npm
- **Faker.js** (Test Data): https://fakerjs.dev/
- **MSW** (API Mocking): https://mswjs.io/

### Community Resources

- Playwright Discord: https://aka.ms/playwright/discord
- Cypress Discord: https://discord.com/invite/cypress
- Ministry of Testing: https://www.ministryoftesting.com/
