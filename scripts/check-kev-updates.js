#!/usr/bin/env node

/**
 * CISA KEV Catalog Update Checker
 * Fetches the latest KEV catalog and compares with cached version
 * Reference: https://www.cisa.gov/resources-tools/resources/kev-catalog
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

// KEV Catalog JSON URL from CISA
const KEV_CATALOG_URL = 'https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json';
const CACHE_DIR = path.join(__dirname, '..', 'data');
const CACHE_FILE = path.join(CACHE_DIR, 'kev_latest.json');

/**
 * Fetch JSON data from URL
 */
function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (res) => {
      let data = '';

      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}: Failed to fetch ${url}`));
        return;
      }

      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`Failed to parse JSON: ${e.message}`));
        }
      });
    }).on('error', reject);
  });
}

/**
 * Load cached KEV data
 */
function loadCached() {
  if (!fs.existsSync(CACHE_FILE)) {
    return null;
  }

  try {
    const data = fs.readFileSync(CACHE_FILE, 'utf8');
    return JSON.parse(data);
  } catch (e) {
    console.error(`Warning: Failed to load cache: ${e.message}`);
    return null;
  }
}

/**
 * Save KEV data to cache
 */
function saveCache(data) {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }

  fs.writeFileSync(CACHE_FILE, JSON.stringify(data, null, 2));
}

/**
 * Find new vulnerabilities
 */
function findNewEntries(latest, cached) {
  if (!cached || !cached.vulnerabilities) {
    return latest.vulnerabilities || [];
  }

  const cachedCVEs = new Set(cached.vulnerabilities.map(v => v.cveID));
  return (latest.vulnerabilities || []).filter(v => !cachedCVEs.has(v.cveID));
}

/**
 * Format issue body for GitHub
 */
function formatIssueBody(newEntries, catalogUrl) {
  const lines = ['## New KEV Entries Detected', ''];

  lines.push(`**${newEntries.length} new vulnerabilities added to CISA KEV Catalog**`);
  lines.push('');
  lines.push('| CVE ID | Vendor | Product | Vulnerability | Date Added |');
  lines.push('|--------|--------|---------|--------------|------------|');

  newEntries.slice(0, 20).forEach(entry => {
    lines.push(`| ${entry.cveID} | ${entry.vendorProject} | ${entry.product} | ${entry.vulnerabilityName} | ${entry.dateAdded} |`);
  });

  if (newEntries.length > 20) {
    lines.push(`| ... and ${newEntries.length - 20} more | | | | |`);
  }

  lines.push('');
  lines.push(`**Full Catalog**: ${catalogUrl}`);
  lines.push('');
  lines.push('### Action Required');
  lines.push('- Review new vulnerabilities for applicability to your systems');
  lines.push('- Update patching priorities based on CISA deadlines');
  lines.push('- Document any compensating controls if patches cannot be applied');

  return lines.join('\n');
}

/**
 * Main execution
 */
async function main() {
  try {
    console.log('Fetching latest KEV catalog from CISA...');
    const latest = await fetchJSON(KEV_CATALOG_URL);

    if (!latest || !latest.vulnerabilities) {
      throw new Error('Invalid KEV catalog structure');
    }

    console.log(`Fetched ${latest.vulnerabilities.length} total vulnerabilities`);
    console.log(`Catalog version: ${latest.catalogVersion || 'unknown'}`);
    console.log(`Last updated: ${latest.dateReleased || 'unknown'}`);

    const cached = loadCached();
    const newEntries = findNewEntries(latest, cached);

    if (newEntries.length === 0) {
      console.log('No new entries found');
      process.exit(0);
    }

    console.log(`Found ${newEntries.length} new entries`);

    // Save updated cache
    saveCache(latest);
    console.log('Cache updated');

    // Output for GitHub Actions
    if (process.env.GITHUB_ACTIONS) {
      const issueBody = formatIssueBody(newEntries, KEV_CATALOG_URL);

      // Write to file for GitHub Actions to pick up
      const outputFile = path.join(CACHE_DIR, 'kev_issue_body.md');
      fs.writeFileSync(outputFile, issueBody);

      // Set outputs
      console.log(`::set-output name=has_updates::true`);
      console.log(`::set-output name=new_count::${newEntries.length}`);
      console.log(`::set-output name=issue_body_file::${outputFile}`);
    }

    // Exit with code 0 (success, updates found)
    process.exit(0);

  } catch (error) {
    console.error(`Error: ${error.message}`);

    if (error.message.includes('Failed to fetch')) {
      console.error('');
      console.error('Unable to fetch KEV catalog. Please check:');
      console.error(`1. URL is accessible: ${KEV_CATALOG_URL}`);
      console.error('2. Network connectivity');
      console.error('3. CISA website status');
      console.error('');
      console.error('TODO: @williamzujkowski - Verify KEV catalog URL or provide alternate source');
      console.error(`Due date: ${new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0]}`);
    }

    process.exit(1);
  }
}

// Run if executed directly
if (require.main === module) {
  main();
}

module.exports = { fetchJSON, findNewEntries, formatIssueBody };
