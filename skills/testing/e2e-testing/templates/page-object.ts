import { Page, Locator, expect } from '@playwright/test';

/**
 * Base Page Object
 * Provides common functionality for all page objects
 */
export abstract class BasePage {
  constructor(protected page: Page) {}

  /**
   * Navigate to a specific path
   */
  async navigate(path: string = '') {
    await this.page.goto(path);
  }

  /**
   * Wait for page to be fully loaded
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
  }

  /**
   * Get current page title
   */
  async getPageTitle(): Promise<string> {
    return await this.page.title();
  }

  /**
   * Get current URL
   */
  getCurrentUrl(): string {
    return this.page.url();
  }

  /**
   * Take a screenshot
   */
  async takeScreenshot(name: string, fullPage = true) {
    await this.page.screenshot({ 
      path: `screenshots/${name}.png`,
      fullPage 
    });
  }

  /**
   * Wait for navigation to complete
   */
  async waitForNavigation(urlPattern?: string | RegExp) {
    if (urlPattern) {
      await this.page.waitForURL(urlPattern);
    } else {
      await this.page.waitForLoadState('networkidle');
    }
  }

  /**
   * Reload current page
   */
  async reload() {
    await this.page.reload();
  }

  /**
   * Execute JavaScript in page context
   */
  async evaluate<T>(fn: () => T): Promise<T> {
    return await this.page.evaluate(fn);
  }
}

/**
 * Example: Login Page Object
 * Encapsulates login page interactions
 */
export class LoginPage extends BasePage {
  // Locators - defined once, reused throughout
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly rememberMeCheckbox: Locator;
  readonly forgotPasswordLink: Locator;
  readonly errorMessage: Locator;
  readonly successMessage: Locator;
  readonly signupLink: Locator;

  constructor(page: Page) {
    super(page);
    
    // Initialize locators
    this.usernameInput = page.getByTestId('username-input');
    this.passwordInput = page.getByTestId('password-input');
    this.loginButton = page.getByRole('button', { name: /log in/i });
    this.rememberMeCheckbox = page.getByLabel('Remember me');
    this.forgotPasswordLink = page.getByRole('link', { name: 'Forgot password?' });
    this.errorMessage = page.getByTestId('error-message');
    this.successMessage = page.getByTestId('success-message');
    this.signupLink = page.getByRole('link', { name: 'Sign up' });
  }

  /**
   * Navigate to login page
   */
  async goto() {
    await this.navigate('/login');
  }

  /**
   * Perform login with credentials
   */
  async login(username: string, password: string, rememberMe = false) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    
    if (rememberMe) {
      await this.rememberMeCheckbox.check();
    }
    
    await this.loginButton.click();
  }

  /**
   * Login using Enter key
   */
  async loginWithEnter(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.passwordInput.press('Enter');
  }

  /**
   * Click forgot password link
   */
  async clickForgotPassword() {
    await this.forgotPasswordLink.click();
  }

  /**
   * Click signup link
   */
  async clickSignup() {
    await this.signupLink.click();
  }

  /**
   * Get error message text
   */
  async getErrorText(): Promise<string> {
    return await this.errorMessage.textContent() || '';
  }

  /**
   * Check if error message is visible
   */
  async isErrorVisible(): Promise<boolean> {
    return await this.errorMessage.isVisible();
  }

  /**
   * Wait for successful login (redirects to dashboard)
   */
  async waitForSuccessfulLogin() {
    await this.page.waitForURL('/dashboard');
  }

  /**
   * Verify login failed
   */
  async verifyLoginFailed() {
    await expect(this.errorMessage).toBeVisible();
    await expect(this.page).toHaveURL(/login/);
  }

  /**
   * Clear login form
   */
  async clearForm() {
    await this.usernameInput.clear();
    await this.passwordInput.clear();
  }

  /**
   * Check if login button is enabled
   */
  async isLoginButtonEnabled(): Promise<boolean> {
    return await this.loginButton.isEnabled();
  }
}

/**
 * Example: Dashboard Page Object
 * Encapsulates dashboard interactions
 */
export class DashboardPage extends BasePage {
  readonly welcomeMessage: Locator;
  readonly logoutButton: Locator;
  readonly userMenu: Locator;
  readonly notificationBell: Locator;
  readonly searchInput: Locator;
  readonly navigationMenu: Locator;

  constructor(page: Page) {
    super(page);
    
    this.welcomeMessage = page.getByTestId('welcome-message');
    this.logoutButton = page.getByRole('button', { name: 'Logout' });
    this.userMenu = page.getByTestId('user-menu');
    this.notificationBell = page.getByTestId('notification-bell');
    this.searchInput = page.getByPlaceholder('Search...');
    this.navigationMenu = page.getByRole('navigation');
  }

  /**
   * Navigate to dashboard
   */
  async goto() {
    await this.navigate('/dashboard');
  }

  /**
   * Get welcome message text
   */
  async getWelcomeText(): Promise<string> {
    return await this.welcomeMessage.textContent() || '';
  }

  /**
   * Logout user
   */
  async logout() {
    await this.userMenu.click();
    await this.logoutButton.click();
  }

  /**
   * Search for content
   */
  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchInput.press('Enter');
  }

  /**
   * Navigate to section
   */
  async navigateTo(sectionName: string) {
    await this.navigationMenu
      .getByRole('link', { name: sectionName })
      .click();
  }

  /**
   * Get notification count
   */
  async getNotificationCount(): Promise<number> {
    const badge = this.notificationBell.locator('.badge');
    const text = await badge.textContent();
    return parseInt(text || '0', 10);
  }

  /**
   * Verify user is logged in
   */
  async verifyLoggedIn(username: string) {
    await expect(this.welcomeMessage).toContainText(username);
    await expect(this.page).toHaveURL('/dashboard');
  }
}

/**
 * Example: Product List Page Object
 * Encapsulates product listing interactions
 */
export class ProductListPage extends BasePage {
  readonly productCards: Locator;
  readonly addToCartButtons: Locator;
  readonly sortDropdown: Locator;
  readonly filterSidebar: Locator;
  readonly priceRangeFilter: Locator;
  readonly categoryFilter: Locator;
  readonly searchInput: Locator;
  readonly paginationNext: Locator;
  readonly paginationPrevious: Locator;

  constructor(page: Page) {
    super(page);
    
    this.productCards = page.getByTestId('product-card');
    this.addToCartButtons = page.getByRole('button', { name: /add to cart/i });
    this.sortDropdown = page.getByTestId('sort-dropdown');
    this.filterSidebar = page.getByTestId('filter-sidebar');
    this.priceRangeFilter = page.getByTestId('price-range-filter');
    this.categoryFilter = page.getByTestId('category-filter');
    this.searchInput = page.getByPlaceholder('Search products...');
    this.paginationNext = page.getByRole('button', { name: 'Next' });
    this.paginationPrevious = page.getByRole('button', { name: 'Previous' });
  }

  /**
   * Navigate to products page
   */
  async goto() {
    await this.navigate('/products');
  }

  /**
   * Get all product cards
   */
  async getProducts(): Promise<Locator> {
    return this.productCards;
  }

  /**
   * Get product count
   */
  async getProductCount(): Promise<number> {
    return await this.productCards.count();
  }

  /**
   * Get product by name
   */
  getProductByName(name: string): Locator {
    return this.productCards.filter({ hasText: name });
  }

  /**
   * Add product to cart by name
   */
  async addToCart(productName: string) {
    const product = this.getProductByName(productName);
    await product.getByRole('button', { name: /add to cart/i }).click();
  }

  /**
   * Sort products
   */
  async sortBy(option: string) {
    await this.sortDropdown.click();
    await this.page.getByRole('option', { name: option }).click();
  }

  /**
   * Filter by category
   */
  async filterByCategory(category: string) {
    await this.categoryFilter.getByLabel(category).check();
  }

  /**
   * Set price range
   */
  async setPriceRange(min: number, max: number) {
    await this.priceRangeFilter.getByTestId('min-price').fill(min.toString());
    await this.priceRangeFilter.getByTestId('max-price').fill(max.toString());
    await this.priceRangeFilter.getByRole('button', { name: 'Apply' }).click();
  }

  /**
   * Search products
   */
  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchInput.press('Enter');
  }

  /**
   * Go to next page
   */
  async nextPage() {
    await this.paginationNext.click();
  }

  /**
   * Go to previous page
   */
  async previousPage() {
    await this.paginationPrevious.click();
  }

  /**
   * Get first product name
   */
  async getFirstProductName(): Promise<string> {
    return await this.productCards.first()
      .getByTestId('product-name')
      .textContent() || '';
  }

  /**
   * Verify products are displayed
   */
  async verifyProductsDisplayed() {
    await expect(this.productCards.first()).toBeVisible();
    const count = await this.getProductCount();
    expect(count).toBeGreaterThan(0);
  }
}

/**
 * Example: Shopping Cart Page Object
 */
export class ShoppingCartPage extends BasePage {
  readonly cartItems: Locator;
  readonly checkoutButton: Locator;
  readonly continueShoppingButton: Locator;
  readonly emptyCartMessage: Locator;
  readonly totalPrice: Locator;
  readonly removeButtons: Locator;
  readonly quantityInputs: Locator;

  constructor(page: Page) {
    super(page);
    
    this.cartItems = page.getByTestId('cart-item');
    this.checkoutButton = page.getByRole('button', { name: /checkout/i });
    this.continueShoppingButton = page.getByRole('button', { name: /continue shopping/i });
    this.emptyCartMessage = page.getByText(/your cart is empty/i);
    this.totalPrice = page.getByTestId('total-price');
    this.removeButtons = page.getByRole('button', { name: /remove/i });
    this.quantityInputs = page.getByTestId('quantity-input');
  }

  /**
   * Navigate to cart
   */
  async goto() {
    await this.navigate('/cart');
  }

  /**
   * Get cart item count
   */
  async getItemCount(): Promise<number> {
    return await this.cartItems.count();
  }

  /**
   * Get total price
   */
  async getTotalPrice(): Promise<string> {
    return await this.totalPrice.textContent() || '';
  }

  /**
   * Remove item by name
   */
  async removeItem(productName: string) {
    const item = this.cartItems.filter({ hasText: productName });
    await item.getByRole('button', { name: /remove/i }).click();
  }

  /**
   * Update item quantity
   */
  async updateQuantity(productName: string, quantity: number) {
    const item = this.cartItems.filter({ hasText: productName });
    await item.getByTestId('quantity-input').fill(quantity.toString());
  }

  /**
   * Proceed to checkout
   */
  async proceedToCheckout() {
    await this.checkoutButton.click();
  }

  /**
   * Continue shopping
   */
  async continueShopping() {
    await this.continueShoppingButton.click();
  }

  /**
   * Verify cart is empty
   */
  async verifyCartEmpty() {
    await expect(this.emptyCartMessage).toBeVisible();
    await expect(this.checkoutButton).toBeDisabled();
  }

  /**
   * Verify item in cart
   */
  async verifyItemInCart(productName: string) {
    await expect(this.cartItems.filter({ hasText: productName })).toBeVisible();
  }
}
