// Playwright tests for GitHub Pages documentation site
const { test, expect } = require('@playwright/test');

const BASE_URL = process.env.PAGES_URL || 'https://williamzujkowski.github.io/standards';

// Helper function to check for broken links
async function checkLinks(page, url) {
  const links = await page.locator('a[href]').all();
  const brokenLinks = [];
  
  for (const link of links) {
    const href = await link.getAttribute('href');
    if (href && !href.startsWith('#') && !href.startsWith('mailto:')) {
      try {
        const fullUrl = new URL(href, url).toString();
        if (fullUrl.startsWith('http')) {
          const response = await page.request.head(fullUrl).catch(() => null);
          if (!response || response.status() >= 400) {
            brokenLinks.push({ href, status: response?.status() || 'failed' });
          }
        }
      } catch (e) {
        console.log(`Error checking link ${href}:`, e.message);
      }
    }
  }
  
  return brokenLinks;
}

test.describe('GitHub Pages Documentation Site', () => {
  test.beforeEach(async ({ page }) => {
    // Set timeout for navigation
    page.setDefaultTimeout(30000);
  });

  test('Home page loads successfully', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Check page title
    await expect(page).toHaveTitle(/Software Development Standards/);
    
    // Check main heading
    const heading = page.locator('h1');
    await expect(heading).toContainText('Software Development Standards');
    
    // Check hero buttons exist
    await expect(page.locator('.hero-buttons')).toBeVisible();
    await expect(page.locator('.btn.btn-primary')).toContainText('Quick Start');
    await expect(page.locator('.btn.btn-secondary')).toContainText('Browse Standards');
  });

  test('Navigation works correctly', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Check main navigation exists
    const nav = page.locator('.main-nav');
    await expect(nav).toBeVisible();
    
    // Test navigation links
    const navLinks = [
      { text: 'Quick Start', url: '/guides/KICKSTART_PROMPT' },
      { text: 'Standards', url: '/standards/UNIFIED_STANDARDS' },
      { text: 'Guides', url: '/guides/STANDARDS_INDEX' }
    ];
    
    for (const link of navLinks) {
      const navLink = nav.locator(`a:has-text("${link.text}")`);
      await expect(navLink).toBeVisible();
      
      // Click and verify navigation
      await navLink.click();
      await expect(page).toHaveURL(new RegExp(link.url));
      
      // Go back to home
      await page.goto(BASE_URL);
    }
  });

  test('Search functionality works', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Find search input
    const searchInput = page.locator('#search-input');
    await expect(searchInput).toBeVisible();
    
    // Type a search query
    await searchInput.fill('coding standards');
    
    // Wait for search results
    await page.waitForTimeout(500); // Wait for debounce
    
    const searchResults = page.locator('#search-results');
    await expect(searchResults).toBeVisible();
    
    // Check that results are displayed
    const results = page.locator('.search-result');
    await expect(results).toHaveCount(await results.count());
  });

  test('Features grid displays correctly', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const featuresGrid = page.locator('.features-grid');
    await expect(featuresGrid).toBeVisible();
    
    // Check all feature cards
    const features = featuresGrid.locator('.feature');
    await expect(features).toHaveCount(4);
    
    // Check each feature has title and content
    for (let i = 0; i < 4; i++) {
      const feature = features.nth(i);
      await expect(feature.locator('h3')).toBeVisible();
      await expect(feature.locator('p')).toBeVisible();
      await expect(feature.locator('a')).toBeVisible();
    }
  });

  test('Standards pages load correctly', async ({ page }) => {
    const standardPages = [
      '/standards/UNIFIED_STANDARDS',
      '/standards/CODING_STANDARDS',
      '/standards/TESTING_STANDARDS',
      '/standards/MODERN_SECURITY_STANDARDS'
    ];
    
    for (const pagePath of standardPages) {
      await page.goto(`${BASE_URL}${pagePath}`);
      
      // Check page loads without errors
      await expect(page.locator('h1')).toBeVisible();
      
      // Check for console errors
      const consoleErrors = [];
      page.on('console', msg => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });
      
      await page.waitForTimeout(1000);
      expect(consoleErrors).toHaveLength(0);
    }
  });

  test('Mobile responsiveness', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE_URL);
    
    // Check that page is still functional
    await expect(page.locator('h1')).toBeVisible();
    
    // Check hero buttons stack vertically
    const heroButtons = page.locator('.hero-buttons');
    await expect(heroButtons).toBeVisible();
    
    // Check features grid becomes single column
    const features = page.locator('.features-grid .feature');
    await expect(features.first()).toBeVisible();
  });

  test('Dark mode support', async ({ page }) => {
    // Emulate dark mode
    await page.emulateMedia({ colorScheme: 'dark' });
    await page.goto(BASE_URL);
    
    // Check that page renders correctly
    await expect(page.locator('h1')).toBeVisible();
    
    // Take screenshot for visual validation
    await page.screenshot({ path: 'tests/screenshots/dark-mode.png' });
  });

  test('Breadcrumbs navigation', async ({ page }) => {
    await page.goto(`${BASE_URL}/guides/KICKSTART_PROMPT`);
    
    const breadcrumbs = page.locator('.breadcrumbs');
    await expect(breadcrumbs).toBeVisible();
    
    // Check home link in breadcrumbs
    const homeLink = breadcrumbs.locator('a:has-text("Home")');
    await expect(homeLink).toBeVisible();
    
    // Click home link
    await homeLink.click();
    await expect(page).toHaveURL(BASE_URL + '/');
  });

  test('Footer links are functional', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const footer = page.locator('.footer-links');
    await expect(footer).toBeVisible();
    
    // Check footer links exist
    await expect(footer.locator('a:has-text("Contributing")')).toBeVisible();
    await expect(footer.locator('a:has-text("Report Issue")')).toBeVisible();
    await expect(footer.locator('a:has-text("MIT License")')).toBeVisible();
  });

  test('Check for broken internal links', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const brokenLinks = await checkLinks(page, BASE_URL);
    
    // Report broken links
    if (brokenLinks.length > 0) {
      console.log('Broken links found:', brokenLinks);
    }
    
    expect(brokenLinks).toHaveLength(0);
  });

  test('SEO meta tags are present', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Check meta tags
    const metaDescription = page.locator('meta[name="description"]');
    await expect(metaDescription).toHaveAttribute('content', /Battle-tested standards/);
    
    // Check Open Graph tags
    const ogTitle = page.locator('meta[property="og:title"]');
    await expect(ogTitle).toHaveCount(1);
    
    const ogDescription = page.locator('meta[property="og:description"]');
    await expect(ogDescription).toHaveCount(1);
  });

  test('Performance metrics', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Get performance metrics
    const metrics = await page.evaluate(() => {
      const perf = window.performance;
      const navigation = perf.getEntriesByType('navigation')[0];
      
      return {
        domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
        loadComplete: navigation.loadEventEnd - navigation.loadEventStart,
        firstPaint: perf.getEntriesByName('first-paint')[0]?.startTime,
        firstContentfulPaint: perf.getEntriesByName('first-contentful-paint')[0]?.startTime
      };
    });
    
    console.log('Performance metrics:', metrics);
    
    // Assert reasonable performance
    expect(metrics.loadComplete).toBeLessThan(5000); // Page loads in under 5 seconds
  });
});

test.describe('Accessibility', () => {
  test('Page has proper heading hierarchy', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Check h1 exists and is unique
    const h1 = page.locator('h1');
    await expect(h1).toHaveCount(1);
    
    // Check heading hierarchy
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    const headingLevels = await Promise.all(
      headings.map(async h => {
        const tagName = await h.evaluate(el => el.tagName);
        return parseInt(tagName.substring(1));
      })
    );
    
    // Check that heading levels don't skip
    for (let i = 1; i < headingLevels.length; i++) {
      const diff = headingLevels[i] - headingLevels[i - 1];
      expect(diff).toBeLessThanOrEqual(1);
    }
  });

  test('Images have alt text', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const images = await page.locator('img').all();
    
    for (const img of images) {
      const alt = await img.getAttribute('alt');
      expect(alt).toBeTruthy();
    }
  });

  test('Links have descriptive text', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const links = await page.locator('a').all();
    
    for (const link of links) {
      const text = await link.textContent();
      const ariaLabel = await link.getAttribute('aria-label');
      
      // Either text content or aria-label should be present
      expect(text || ariaLabel).toBeTruthy();
      
      // Avoid generic link text
      if (text) {
        expect(text.toLowerCase()).not.toMatch(/^(click here|here|read more)$/);
      }
    }
  });
});