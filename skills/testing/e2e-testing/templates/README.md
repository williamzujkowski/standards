# E2E Testing Templates

Reusable templates for Page Object Models and test suites.

## Files

- `page-object.ts` - Complete Page Object Model examples with BasePage pattern
- `test-template.spec.ts` - Comprehensive test suite template with all common patterns

## Usage

### Page Objects

```typescript
// Copy BasePage pattern
import { BasePage } from './templates/page-object';

// Create your own page objects
export class YourPage extends BasePage {
  // Define locators and methods
}
```

### Test Templates

```typescript
// Copy test patterns
import { test, expect } from '@playwright/test';
import { YourPage } from './page-objects/YourPage';

test.describe('Your Feature', () => {
  test('should work', async ({ page }) => {
    // Your test logic
  });
});
```

## Patterns Included

- Authentication flows
- CRUD operations
- Network mocking
- Error handling
- Accessibility testing
- Visual regression
- Mobile responsive testing
