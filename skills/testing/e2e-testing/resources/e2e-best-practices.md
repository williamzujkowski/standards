# E2E Testing Best Practices: Anti-Flakiness Guide

A comprehensive guide to writing stable, maintainable, and reliable end-to-end tests.

## Table of Contents

1. [Selector Strategies](#selector-strategies)
2. [Wait Patterns](#wait-patterns)
3. [Test Isolation](#test-isolation)
4. [Data Management](#data-management)
5. [Network Handling](#network-handling)
6. [Common Anti-Patterns](#common-anti-patterns)
7. [Debugging Techniques](#debugging-techniques)
8. [Performance Optimization](#performance-optimization)

---

## Selector Strategies

### Priority Order

**1. Test IDs (Highest Priority)**

```typescript
// ✅ Best: Dedicated test attributes
<button data-testid="submit-button">Submit</button>
await page.getByTestId('submit-button').click();

// Why: Resistant to UI/CSS changes, clear intent
```

**2. Accessibility Attributes**

```typescript
// ✅ Good: Semantic and accessible
<button aria-label="Submit form">Submit</button>
await page.getByRole('button', { name: 'Submit form' }).click();

<label for="email">Email</label>
<input id="email" name="email" />
await page.getByLabel('Email').fill('user@example.com');

// Why: Tests accessibility + functionality
```

**3. Text Content**

```typescript
// ✅ Acceptable: Unique visible text
await page.getByText('Welcome back, John').click();

// ⚠️ Caution: Breaks with text changes, i18n
```

**4. CSS Selectors (Last Resort)**

```typescript
// ❌ Avoid: Brittle, breaks with styling
await page.locator('.btn.btn-primary.mt-3').click();

// Why: Couples tests to CSS implementation
```

### Selector Best Practices

```typescript
// ✅ Specific and scoped
await page.getByRole('navigation')
  .getByRole('link', { name: 'Products' })
  .click();

// ❌ Too generic
await page.locator('a').nth(2).click();

// ✅ Wait for specific state
await page.getByTestId('modal').waitFor({ state: 'visible' });
await page.getByTestId('modal-close').click();

// ❌ Assume element is ready
await page.getByTestId('modal-close').click(); // Might fail if modal animates
```

---

## Wait Patterns

### Auto-Waiting (Preferred)

Playwright and Cypress automatically wait for elements to be:

- Present in DOM
- Visible
- Enabled
- Stable (not animating)

```typescript
// ✅ No explicit wait needed
await page.click('button'); // Waits automatically
await page.fill('input', 'text'); // Waits automatically
```

### Explicit Waits (When Necessary)

**Wait for Element State**

```typescript
// ✅ Wait for specific condition
await page.waitForSelector('[data-testid="results"]', {
  state: 'visible',
  timeout: 5000
});

// ✅ Wait for element to disappear
await page.waitForSelector('[data-testid="loading"]', {
  state: 'detached'
});
```

**Wait for Network**

```typescript
// ✅ Wait for API response
const responsePromise = page.waitForResponse(
  response => response.url().includes('/api/users') && response.ok()
);
await page.click('[data-testid="load-users"]');
await responsePromise;

// ✅ Wait for network idle
await page.waitForLoadState('networkidle');
```

**Wait for Custom Conditions**

```typescript
// ✅ Wait for complex condition
await page.waitForFunction(() => {
  const items = document.querySelectorAll('.item');
  return items.length > 5 && items[0].textContent.trim() !== '';
});
```

### Anti-Patterns

```typescript
// ❌ NEVER: Hard-coded delays
await page.waitForTimeout(5000); // Brittle, slow, unreliable

// ✅ ALWAYS: Wait for specific condition
await page.waitForSelector('[data-testid="loaded"]');

// ❌ NEVER: Polling loops
let found = false;
while (!found) {
  found = await page.isVisible('.result');
  await page.waitForTimeout(100);
}

// ✅ ALWAYS: Built-in waits
await page.waitForSelector('.result', { state: 'visible', timeout: 10000 });

// ❌ NEVER: Ignore wait failures
try {
  await page.click('button');
} catch (e) {
  await page.waitForTimeout(1000);
  await page.click('button'); // Still might fail
}

// ✅ ALWAYS: Fix root cause
await page.waitForLoadState('networkidle');
await page.click('button'); // Now reliable
```

---

## Test Isolation

### Independent Tests

```typescript
// ✅ Each test is self-contained
test('create item', async ({ page }) => {
  // Setup
  const item = await createItemViaAPI();

  // Test
  await page.goto(`/items/${item.id}`);
  await expect(page.getByTestId('item-name')).toContainText(item.name);

  // Cleanup
  await deleteItemViaAPI(item.id);
});

// ❌ Tests depend on each other
test('create item', async ({ page }) => {
  await page.goto('/items/new');
  await page.fill('[name="name"]', 'Test Item');
  await page.click('[type="submit"]');
});

test('edit item', async ({ page }) => {
  // Assumes previous test created "Test Item" - FLAKY!
  await page.goto('/items');
  await page.click('text=Test Item');
  // ...
});
```

### Fresh State

```typescript
// ✅ Clear state before each test
test.beforeEach(async ({ page, context }) => {
  // Clear cookies
  await context.clearCookies();

  // Clear local storage
  await page.goto('/');
  await page.evaluate(() => localStorage.clear());

  // Reset database state
  await resetTestDatabase();
});

// ✅ Use unique test data
test('create user', async ({ page }) => {
  const uniqueEmail = `test-${Date.now()}@example.com`;
  await page.fill('[name="email"]', uniqueEmail);
  // ...
});

// ❌ Shared state between tests
let globalUser; // Don't do this!

test('create user', async () => {
  globalUser = await createUser();
});

test('login user', async () => {
  await login(globalUser); // Depends on previous test!
});
```

---

## Data Management

### Test Data Strategies

**1. API Setup (Fastest)**

```typescript
// ✅ Use API for data setup
test('display user profile', async ({ page, request }) => {
  // Setup via API
  const response = await request.post('/api/users', {
    data: { name: 'Test User', email: 'test@example.com' }
  });
  const user = await response.json();

  // Test UI
  await page.goto(`/users/${user.id}`);
  await expect(page.getByTestId('username')).toContainText('Test User');

  // Cleanup via API
  await request.delete(`/api/users/${user.id}`);
});

// ❌ Use UI for data setup (slow)
test('display user profile', async ({ page }) => {
  await page.goto('/users/new');
  await page.fill('[name="name"]', 'Test User');
  await page.fill('[name="email"]', 'test@example.com');
  await page.click('[type="submit"]');
  // This takes 10x longer!
});
```

**2. Database Seeding**

```typescript
// ✅ Seed database before tests
test.beforeEach(async () => {
  await prisma.user.deleteMany();
  await prisma.user.createMany({
    data: [
      { name: 'User 1', email: 'user1@example.com' },
      { name: 'User 2', email: 'user2@example.com' },
    ]
  });
});
```

**3. Fixtures**

```typescript
// ✅ Create reusable fixtures
import { test as base } from '@playwright/test';

type TestFixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<TestFixtures>({
  authenticatedPage: async ({ page, request }, use) => {
    // Setup authentication
    const token = await getAuthToken(request);
    await page.goto('/');
    await page.evaluate(token => {
      localStorage.setItem('auth_token', token);
    }, token);

    await use(page);

    // Cleanup
    await page.evaluate(() => localStorage.clear());
  }
});

// Usage
test('view dashboard', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/dashboard');
  // Already authenticated!
});
```

### Data Cleanup

```typescript
// ✅ Always clean up
test('create item', async ({ page, request }) => {
  let itemId;

  try {
    const response = await request.post('/api/items', {
      data: { name: 'Test Item' }
    });
    const item = await response.json();
    itemId = item.id;

    // Test logic
    await page.goto(`/items/${itemId}`);
    // ...
  } finally {
    // Cleanup even if test fails
    if (itemId) {
      await request.delete(`/api/items/${itemId}`);
    }
  }
});

// ✅ Use test hooks for cleanup
test.afterEach(async ({ request }, testInfo) => {
  // Clean up any data created in test
  const itemIds = testInfo.annotations
    .filter(a => a.type === 'item')
    .map(a => a.description);

  for (const id of itemIds) {
    await request.delete(`/api/items/${id}`);
  }
});
```

---

## Network Handling

### API Mocking

```typescript
// ✅ Mock unreliable external APIs
test('load user data', async ({ page }) => {
  await page.route('/api/users', route => {
    route.fulfill({
      status: 200,
      body: JSON.stringify({ name: 'John', email: 'john@example.com' })
    });
  });

  await page.goto('/profile');
  await expect(page.getByTestId('username')).toContainText('John');
});

// ✅ Mock error responses
test('handle API error', async ({ page }) => {
  await page.route('/api/users', route => {
    route.fulfill({
      status: 500,
      body: JSON.stringify({ error: 'Internal Server Error' })
    });
  });

  await page.goto('/profile');
  await expect(page.getByTestId('error-message')).toBeVisible();
});

// ✅ Mock slow responses
test('show loading state', async ({ page }) => {
  await page.route('/api/users', async route => {
    await new Promise(resolve => setTimeout(resolve, 2000)); // Delay 2s
    await route.fulfill({
      status: 200,
      body: JSON.stringify({ name: 'John' })
    });
  });

  await page.goto('/profile');
  await expect(page.getByTestId('loading-spinner')).toBeVisible();
});
```

### Network Stability

```typescript
// ✅ Wait for critical API calls
test('load dashboard', async ({ page }) => {
  const apiResponsePromise = page.waitForResponse(
    response => response.url().includes('/api/dashboard') && response.ok()
  );

  await page.goto('/dashboard');
  await apiResponsePromise; // Ensure API completes

  await expect(page.getByTestId('dashboard-content')).toBeVisible();
});

// ✅ Handle network retries
test('retry failed requests', async ({ page }) => {
  let attempts = 0;
  await page.route('/api/data', route => {
    attempts++;
    if (attempts < 3) {
      route.fulfill({ status: 500 }); // Fail first 2 attempts
    } else {
      route.fulfill({ status: 200, body: '{"data": "success"}' });
    }
  });

  await page.goto('/data');
  // App should retry and eventually succeed
  await expect(page.getByText('success')).toBeVisible();
});
```

---

## Common Anti-Patterns

### 1. Timing Issues

```typescript
// ❌ Assuming instant UI updates
await page.click('[data-testid="add-item"]');
expect(await page.locator('.item').count()).toBe(1); // Might be 0!

// ✅ Wait for UI update
await page.click('[data-testid="add-item"]');
await page.waitForSelector('.item');
expect(await page.locator('.item').count()).toBe(1);
```

### 2. Animation Interference

```typescript
// ❌ Clicking during animation
await page.click('[data-testid="open-modal"]');
await page.click('[data-testid="modal-button"]'); // Might miss if animating

// ✅ Wait for stable state
await page.click('[data-testid="open-modal"]');
await page.getByTestId('modal').waitFor({ state: 'visible' });
await page.waitForLoadState('networkidle'); // Ensure animations complete
await page.click('[data-testid="modal-button"]');
```

### 3. Race Conditions

```typescript
// ❌ Multiple async operations without coordination
await page.goto('/dashboard');
await page.click('[data-testid="load-data"]');
await expect(page.getByTestId('data-item')).toBeVisible(); // Might fail

// ✅ Wait for navigation to complete first
await page.goto('/dashboard');
await page.waitForLoadState('networkidle');
await page.click('[data-testid="load-data"]');
await page.waitForResponse(response => response.url().includes('/api/data'));
await expect(page.getByTestId('data-item')).toBeVisible();
```

### 4. Flaky Assertions

```typescript
// ❌ Checking unstable values
const timestamp = await page.textContent('[data-testid="timestamp"]');
expect(timestamp).toBe('2024-01-15 10:30:00'); // Flaky!

// ✅ Check format or range
const timestamp = await page.textContent('[data-testid="timestamp"]');
expect(timestamp).toMatch(/^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/);

// ❌ Exact count assertions on dynamic data
expect(await page.locator('.item').count()).toBe(42); // Flaky!

// ✅ Range or minimum assertions
expect(await page.locator('.item').count()).toBeGreaterThan(0);
```

---

## Debugging Techniques

### 1. Visual Debugging

```typescript
// Playwright Inspector
await page.pause(); // Pauses test and opens inspector

// Headed mode
test.use({ headless: false, slowMo: 100 }); // Slow down actions

// Screenshots on failure
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== 'passed') {
    await page.screenshot({ path: `failure-${testInfo.title}.png` });
  }
});
```

### 2. Trace Recording

```typescript
// Enable tracing in config
use: {
  trace: 'retain-on-failure', // or 'on', 'off'
}

// View trace
// npx playwright show-trace trace.zip
```

### 3. Console Logging

```typescript
// Capture console messages
page.on('console', msg => console.log('PAGE LOG:', msg.text()));

// Capture errors
page.on('pageerror', error => console.log('PAGE ERROR:', error));

// Capture failed requests
page.on('requestfailed', request => {
  console.log('FAILED REQUEST:', request.url(), request.failure());
});
```

---

## Performance Optimization

### 1. Parallel Execution

```typescript
// playwright.config.ts
export default defineConfig({
  fullyParallel: true,
  workers: process.env.CI ? 2 : undefined, // Use available cores
});

// Mark serial tests
test.describe.serial('sequential tests', () => {
  // These run one after another
});
```

### 2. Test Sharding

```bash
# Split tests across machines
npx playwright test --shard=1/4
npx playwright test --shard=2/4
npx playwright test --shard=3/4
npx playwright test --shard=4/4
```

### 3. Authentication Reuse

```typescript
// Setup once, reuse for all tests
// auth.setup.ts
test('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.fill('[name="username"]', process.env.TEST_USER);
  await page.fill('[name="password"]', process.env.TEST_PASSWORD);
  await page.click('button[type="submit"]');
  await page.context().storageState({ path: 'auth-state.json' });
});

// Use in config
projects: [{
  name: 'chromium',
  use: { storageState: 'auth-state.json' },
  dependencies: ['setup'],
}]
```

### 4. Selective Test Execution

```bash
# Run only smoke tests
npx playwright test --grep @smoke

# Skip flaky tests in CI
npx playwright test --grep-invert @flaky

# Run specific test file
npx playwright test tests/critical-path.spec.ts
```

---

## Summary Checklist

- [ ] Use `data-testid` for stable selectors
- [ ] Rely on framework auto-waiting
- [ ] Never use hard-coded timeouts
- [ ] Keep tests independent and isolated
- [ ] Use API for data setup/teardown
- [ ] Mock external dependencies
- [ ] Clean up test data
- [ ] Handle network delays properly
- [ ] Wait for animations to complete
- [ ] Use meaningful assertions
- [ ] Enable retries for CI
- [ ] Record traces on failure
- [ ] Run tests in parallel when possible
- [ ] Reuse authentication state
- [ ] Tag tests for selective execution

---

**Remember**: The key to non-flaky E2E tests is understanding async operations, waiting for the right conditions, and keeping tests independent. Invest time upfront to build stable tests—it pays dividends in CI reliability and developer confidence.
