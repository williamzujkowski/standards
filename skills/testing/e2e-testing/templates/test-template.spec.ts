import { test, expect, Page } from '@playwright/test';
import { LoginPage, DashboardPage, ProductListPage, ShoppingCartPage } from '../page-objects';

/**
 * Complete E2E Test Template
 * Demonstrates: Authentication, Page Objects, Fixtures, Assertions, Network mocking
 */

// Test suite with hooks
test.describe('E2E Test Suite Template', () => {
  let loginPage: LoginPage;
  let dashboardPage: DashboardPage;
  let productListPage: ProductListPage;
  let cartPage: ShoppingCartPage;

  // Run before each test
  test.beforeEach(async ({ page }) => {
    // Initialize page objects
    loginPage = new LoginPage(page);
    dashboardPage = new DashboardPage(page);
    productListPage = new ProductListPage(page);
    cartPage = new ShoppingCartPage(page);

    // Setup: Navigate to starting point
    await page.goto('/');
  });

  // Run after each test
  test.afterEach(async ({ page }, testInfo) => {
    // Cleanup or diagnostics
    if (testInfo.status !== testInfo.expectedStatus) {
      // Test failed - take screenshot
      const timestamp = new Date().getTime();
      await page.screenshot({ 
        path: `test-results/failure-${testInfo.title}-${timestamp}.png`,
        fullPage: true 
      });
    }
  });

  test.describe('Authentication Flow', () => {
    test('should login successfully with valid credentials', async ({ page }) => {
      await loginPage.goto();
      await loginPage.login('user@example.com', 'ValidPass123!');
      
      await dashboardPage.waitForSuccessfulLogin();
      await dashboardPage.verifyLoggedIn('user@example.com');
    });

    test('should show error with invalid credentials', async ({ page }) => {
      await loginPage.goto();
      await loginPage.login('user@example.com', 'WrongPassword');
      
      await loginPage.verifyLoginFailed();
      expect(await loginPage.getErrorText()).toContain('Invalid credentials');
    });

    test('should support login with Enter key', async ({ page }) => {
      await loginPage.goto();
      await loginPage.loginWithEnter('user@example.com', 'ValidPass123!');
      
      await expect(page).toHaveURL('/dashboard');
    });

    test('should remember user when checkbox is checked', async ({ page, context }) => {
      await loginPage.goto();
      await loginPage.login('user@example.com', 'ValidPass123!', true);
      
      // Verify cookie/localStorage
      const cookies = await context.cookies();
      expect(cookies.some(c => c.name === 'remember_token')).toBeTruthy();
    });

    test('should logout successfully', async ({ page }) => {
      // Setup: Login first
      await loginPage.goto();
      await loginPage.login('user@example.com', 'ValidPass123!');
      await dashboardPage.waitForSuccessfulLogin();
      
      // Test logout
      await dashboardPage.logout();
      await expect(page).toHaveURL('/login');
    });
  });

  test.describe('Product Browsing', () => {
    test.beforeEach(async ({ page }) => {
      // Login before each product test
      await loginPage.goto();
      await loginPage.login('user@example.com', 'ValidPass123!');
      await dashboardPage.waitForSuccessfulLogin();
    });

    test('should display product list', async ({ page }) => {
      await productListPage.goto();
      await productListPage.verifyProductsDisplayed();
      
      const count = await productListPage.getProductCount();
      expect(count).toBeGreaterThan(0);
    });

    test('should filter products by category', async ({ page }) => {
      await productListPage.goto();
      await productListPage.filterByCategory('Electronics');
      
      await page.waitForLoadState('networkidle');
      const firstProduct = await productListPage.getFirstProductName();
      expect(firstProduct).toBeTruthy();
    });

    test('should sort products by price', async ({ page }) => {
      await productListPage.goto();
      await productListPage.sortBy('Price: Low to High');
      
      await page.waitForLoadState('networkidle');
      const products = await productListPage.getProducts();
      expect(await products.count()).toBeGreaterThan(0);
    });

    test('should search for products', async ({ page }) => {
      await productListPage.goto();
      await productListPage.search('laptop');
      
      await page.waitForLoadState('networkidle');
      const firstProduct = await productListPage.getFirstProductName();
      expect(firstProduct.toLowerCase()).toContain('laptop');
    });

    test('should paginate through product list', async ({ page }) => {
      await productListPage.goto();
      
      const firstPageProduct = await productListPage.getFirstProductName();
      await productListPage.nextPage();
      
      await page.waitForLoadState('networkidle');
      const secondPageProduct = await productListPage.getFirstProductName();
      
      expect(firstPageProduct).not.toBe(secondPageProduct);
    });
  });

  test.describe('Shopping Cart Flow', () => {
    test.beforeEach(async ({ page }) => {
      // Login before each cart test
      await loginPage.goto();
      await loginPage.login('user@example.com', 'ValidPass123!');
      await dashboardPage.waitForSuccessfulLogin();
    });

    test('should add product to cart', async ({ page }) => {
      await productListPage.goto();
      await productListPage.addToCart('Laptop');
      
      await cartPage.goto();
      await cartPage.verifyItemInCart('Laptop');
    });

    test('should update product quantity', async ({ page }) => {
      // Setup: Add product first
      await productListPage.goto();
      await productListPage.addToCart('Laptop');
      
      // Update quantity
      await cartPage.goto();
      await cartPage.updateQuantity('Laptop', 2);
      
      await page.waitForLoadState('networkidle');
      const total = await cartPage.getTotalPrice();
      expect(total).toBeTruthy();
    });

    test('should remove product from cart', async ({ page }) => {
      // Setup: Add product first
      await productListPage.goto();
      await productListPage.addToCart('Laptop');
      
      // Remove product
      await cartPage.goto();
      await cartPage.removeItem('Laptop');
      
      await cartPage.verifyCartEmpty();
    });

    test('should calculate correct total', async ({ page }) => {
      await productListPage.goto();
      await productListPage.addToCart('Laptop'); // $999
      await productListPage.addToCart('Mouse');  // $29
      
      await cartPage.goto();
      const total = await cartPage.getTotalPrice();
      expect(total).toContain('1028'); // $1028 total
    });
  });

  test.describe('Complete Purchase Flow', () => {
    test('should complete full purchase journey', async ({ page }) => {
      // Step 1: Login
      await loginPage.goto();
      await loginPage.login('user@example.com', 'ValidPass123!');
      await dashboardPage.waitForSuccessfulLogin();
      
      // Step 2: Browse products
      await productListPage.goto();
      await productListPage.search('laptop');
      
      // Step 3: Add to cart
      await productListPage.addToCart('Laptop');
      
      // Step 4: View cart
      await cartPage.goto();
      await cartPage.verifyItemInCart('Laptop');
      
      // Step 5: Proceed to checkout
      await cartPage.proceedToCheckout();
      
      // Step 6: Verify on checkout page
      await expect(page).toHaveURL(/checkout/);
    });
  });

  test.describe('Network Mocking', () => {
    test('should handle API errors gracefully', async ({ page }) => {
      // Mock failed API response
      await page.route('/api/products', route => {
        route.fulfill({
          status: 500,
          contentType: 'application/json',
          body: JSON.stringify({ error: 'Internal Server Error' }),
        });
      });

      await productListPage.goto();
      
      // Verify error state
      await expect(page.getByTestId('error-message'))
        .toContainText('Failed to load products');
    });

    test('should mock successful API response', async ({ page }) => {
      // Mock successful API response with custom data
      await page.route('/api/products', route => {
        route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            products: [
              { id: 1, name: 'Mocked Product', price: 99.99 },
            ],
          }),
        });
      });

      await productListPage.goto();
      await expect(page.getByText('Mocked Product')).toBeVisible();
    });

    test('should wait for API response', async ({ page }) => {
      // Wait for specific API call
      const responsePromise = page.waitForResponse(
        response => response.url().includes('/api/products') && response.status() === 200
      );

      await productListPage.goto();
      
      const response = await responsePromise;
      expect(response.ok()).toBeTruthy();
    });
  });

  test.describe('Accessibility', () => {
    test('should be keyboard navigable', async ({ page }) => {
      await loginPage.goto();
      
      // Tab through form
      await page.keyboard.press('Tab'); // Focus username
      await page.keyboard.type('user@example.com');
      await page.keyboard.press('Tab'); // Focus password
      await page.keyboard.type('ValidPass123!');
      await page.keyboard.press('Enter'); // Submit
      
      await expect(page).toHaveURL('/dashboard');
    });

    test('should have proper ARIA labels', async ({ page }) => {
      await loginPage.goto();
      
      const usernameInput = page.getByLabel(/username|email/i);
      await expect(usernameInput).toBeVisible();
      
      const passwordInput = page.getByLabel(/password/i);
      await expect(passwordInput).toBeVisible();
    });
  });

  test.describe('Visual Regression', () => {
    test('should match homepage snapshot', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveScreenshot('homepage.png', {
        maxDiffPixels: 100,
      });
    });

    test('should match product card snapshot', async ({ page }) => {
      await productListPage.goto();
      const firstProduct = productListPage.productCards.first();
      await expect(firstProduct).toHaveScreenshot('product-card.png');
    });
  });

  test.describe('Mobile Responsive', () => {
    test.use({ viewport: { width: 375, height: 667 } }); // iPhone SE

    test('should display mobile menu', async ({ page }) => {
      await dashboardPage.goto();
      
      const mobileMenu = page.getByTestId('mobile-menu-button');
      await expect(mobileMenu).toBeVisible();
      await mobileMenu.click();
      
      await expect(page.getByTestId('mobile-navigation')).toBeVisible();
    });
  });
});

/**
 * Advanced Test Patterns
 */

test.describe('Advanced Patterns', () => {
  // Custom fixture
  test.use({
    storageState: 'playwright/.auth/admin.json', // Use admin auth
  });

  test('should use custom authentication state', async ({ page }) => {
    await page.goto('/admin');
    await expect(page.getByText('Admin Dashboard')).toBeVisible();
  });

  // Parameterized tests
  for (const user of ['admin', 'user', 'guest']) {
    test(`should handle ${user} role correctly`, async ({ page }) => {
      // Load role-specific auth state
      // Test role-specific functionality
    });
  }

  // Tagged tests
  test('critical user flow @smoke @critical', async ({ page }) => {
    // Smoke test - runs on every commit
  });

  test('performance test @performance', async ({ page }) => {
    // Performance test - runs nightly
  });

  // Retry specific test
  test('flaky API test', async ({ page }) => {
    test.setTimeout(60000); // Extend timeout for this test
    // Flaky test that might need retries
  });

  // Conditional test
  test('browser-specific feature', async ({ page, browserName }) => {
    test.skip(browserName !== 'chromium', 'Chromium-only feature');
    // Test chromium-specific functionality
  });
});
