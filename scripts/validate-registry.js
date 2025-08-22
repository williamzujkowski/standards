#!/usr/bin/env node
/**
 * validate-registry.js - Validate standards registry JSON structure and URLs
 */

const fs = require('fs');
const https = require('https');
const path = require('path');

// JSON Schema for registry
const REGISTRY_SCHEMA = {
  required: ['version', 'updated', 'standards'],
  properties: {
    version: { type: 'string', pattern: '^\\d+\\.\\d+\\.\\d+$' },
    updated: { type: 'string', pattern: '^\\d{4}-\\d{2}-\\d{2}$' },
    standards: {
      type: 'array',
      items: {
        required: ['id', 'title', 'category', 'source_url', 'retrieved'],
        properties: {
          id: { type: 'string', pattern: '^[a-z0-9-]+$' },
          title: { type: 'string', minLength: 1 },
          category: { type: 'string', enum: ['nist', 'owasp', 'supply-chain', 'cisa'] },
          source_url: { type: 'string', pattern: '^https?://' },
          retrieved: { type: 'string', pattern: '^\\d{4}-\\d{2}-\\d{2}$' },
          doc_version: { type: ['string', 'null'] },
          path: { type: ['string', 'null'], pattern: '^/standards/.*\\.md$' }
        }
      }
    }
  }
};

// Validate property against schema
function validateProperty(obj, prop, schema) {
  const value = obj[prop];
  const spec = schema.properties[prop];

  if (!spec) return true;

  // Check type
  if (spec.type) {
    const types = Array.isArray(spec.type) ? spec.type : [spec.type];
    const valueType = value === null ? 'null' : typeof value;
    if (!types.includes(valueType)) {
      if (!(spec.type === 'array' && Array.isArray(value))) {
        return `${prop}: expected ${spec.type}, got ${valueType}`;
      }
    }
  }

  // Check pattern
  if (spec.pattern && typeof value === 'string') {
    const regex = new RegExp(spec.pattern);
    if (!regex.test(value)) {
      return `${prop}: does not match pattern ${spec.pattern}`;
    }
  }

  // Check enum
  if (spec.enum && !spec.enum.includes(value)) {
    return `${prop}: must be one of [${spec.enum.join(', ')}]`;
  }

  // Check minLength
  if (spec.minLength && value.length < spec.minLength) {
    return `${prop}: must be at least ${spec.minLength} characters`;
  }

  return true;
}

// Check URL with HEAD request
function checkUrl(url) {
  return new Promise((resolve) => {
    const urlObj = new URL(url);
    const options = {
      method: 'HEAD',
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      timeout: 5000,
      headers: {
        'User-Agent': 'standards-registry-validator/1.0'
      }
    };

    const req = https.request(options, (res) => {
      if (res.statusCode >= 200 && res.statusCode < 400) {
        resolve({ url, status: res.statusCode, ok: true });
      } else {
        resolve({ url, status: res.statusCode, ok: false });
      }
    });

    req.on('error', (err) => {
      resolve({ url, error: err.message, ok: false });
    });

    req.on('timeout', () => {
      req.destroy();
      resolve({ url, error: 'timeout', ok: false });
    });

    req.end();
  });
}

// Main validation
async function main() {
  const registryPath = path.join(__dirname, '..', 'standards', 'registry.json');

  // Read and parse registry
  let registry;
  try {
    const content = fs.readFileSync(registryPath, 'utf8');
    registry = JSON.parse(content);
  } catch (err) {
    console.error(`Error reading registry: ${err.message}`);
    process.exit(1);
  }

  console.log('Validating registry structure...');

  // Check required fields
  for (const field of REGISTRY_SCHEMA.required) {
    if (!(field in registry)) {
      console.error(`Missing required field: ${field}`);
      process.exit(1);
    }
  }

  // Validate top-level fields
  for (const prop in registry) {
    const result = validateProperty(registry, prop, REGISTRY_SCHEMA);
    if (result !== true) {
      console.error(`Validation error: ${result}`);
      process.exit(1);
    }
  }

  // Validate each standard
  const errors = [];
  const standards = registry.standards || [];

  for (let i = 0; i < standards.length; i++) {
    const std = standards[i];

    // Check required fields
    const itemSchema = REGISTRY_SCHEMA.properties.standards.items;
    for (const field of itemSchema.required) {
      if (!(field in std)) {
        errors.push(`standards[${i}].${field}: missing required field`);
      }
    }

    // Validate properties
    for (const prop in std) {
      const result = validateProperty(std, prop, itemSchema);
      if (result !== true) {
        errors.push(`standards[${i}].${result}`);
      }
    }

    // Check path exists if specified
    if (std.path && std.path !== null) {
      const fullPath = path.join(__dirname, '..', std.path);
      if (!fs.existsSync(fullPath)) {
        errors.push(`standards[${i}].path: file does not exist: ${std.path}`);
      }
    }
  }

  if (errors.length > 0) {
    console.error('Validation errors:');
    errors.forEach(err => console.error(`  - ${err}`));
    process.exit(1);
  }

  console.log('✓ Registry structure valid');

  // Check URLs
  console.log('Checking source URLs...');
  const urls = standards.map(s => s.source_url).filter(u => u);
  const results = await Promise.all(urls.map(checkUrl));

  const failed = results.filter(r => !r.ok);
  if (failed.length > 0) {
    console.error('URL check failures:');
    failed.forEach(r => {
      console.error(`  - ${r.url}: ${r.error || `HTTP ${r.status}`}`);
    });
    // Don't fail on URL errors as some sites block HEAD requests
    console.warn('Warning: Some URLs could not be verified');
  } else {
    console.log('✓ All URLs reachable');
  }

  console.log('Registry validation complete');
}

main().catch(err => {
  console.error(`Unexpected error: ${err.message}`);
  process.exit(1);
});
