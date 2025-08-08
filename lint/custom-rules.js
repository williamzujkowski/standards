// Custom linting rules for Standards Repository
// Based on KNOWLEDGE_MANAGEMENT_STANDARDS.md

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

/**
 * Custom rule: Standards files must have version metadata
 */
function checkVersionMetadata(content, file) {
  const errors = [];
  const lines = content.split('\n');

  // Check for version metadata in first 20 lines
  const headerArea = lines.slice(0, 20).join('\n');

  if (file.endsWith('_STANDARDS.md') || file === 'UNIFIED_STANDARDS.md') {
    if (!headerArea.includes('Version:')) {
      errors.push({
        file,
        line: 1,
        rule: 'version-metadata',
        message: 'Standards files must include "Version:" metadata'
      });
    }

    if (!headerArea.includes('Last Updated:')) {
      errors.push({
        file,
        line: 1,
        rule: 'last-updated-metadata',
        message: 'Standards files must include "Last Updated:" metadata'
      });
    }

    if (!headerArea.includes('Status:')) {
      errors.push({
        file,
        line: 1,
        rule: 'status-metadata',
        message: 'Standards files must include "Status:" metadata'
      });
    }
  }

  return errors;
}

/**
 * Custom rule: Standards must have required sections
 */
function checkRequiredSections(content, file) {
  const errors = [];

  if (file.endsWith('_STANDARDS.md') && file !== 'UNIFIED_STANDARDS.md') {
    const requiredSections = ['Overview', 'Implementation'];

    requiredSections.forEach(section => {
      const pattern = new RegExp(`^#{1,3}\\s+${section}`, 'mi');
      if (!pattern.test(content)) {
        errors.push({
          file,
          line: 1,
          rule: 'required-sections',
          message: `Standards must include "${section}" section`
        });
      }
    });
  }

  return errors;
}

/**
 * Custom rule: Check for [REQUIRED] and [RECOMMENDED] tags
 */
function checkRequirementTags(content, file) {
  const errors = [];

  if (file.endsWith('_STANDARDS.md')) {
    if (!content.includes('[REQUIRED]') && !content.includes('[RECOMMENDED]')) {
      errors.push({
        file,
        line: 1,
        rule: 'requirement-tags',
        message: 'Standards should use [REQUIRED] or [RECOMMENDED] tags'
      });
    }
  }

  return errors;
}

/**
 * Custom rule: Cross-references must be valid
 */
function checkCrossReferences(content, file, allFiles) {
  const errors = [];
  const linkPattern = /\[([^\]]+)\]\(\.\/([^)]+)\)/g;
  const lines = content.split('\n');

  let match;
  while ((match = linkPattern.exec(content)) !== null) {
    const linkPath = match[2].split('#')[0];
    const fullPath = path.resolve(path.dirname(file), linkPath);

    if (!allFiles.includes(fullPath) && !fs.existsSync(fullPath)) {
      const lineNum = content.substring(0, match.index).split('\n').length;
      errors.push({
        file,
        line: lineNum,
        rule: 'valid-cross-references',
        message: `Broken link: ${linkPath}`
      });
    }
  }

  return errors;
}

/**
 * Custom rule: Standards must be in MANIFEST.yaml
 */
async function checkManifestInclusion(file, manifestPath) {
  const errors = [];

  if (file.endsWith('_STANDARDS.md') || file === 'UNIFIED_STANDARDS.md') {
    try {
      const manifestContent = fs.readFileSync(manifestPath, 'utf8');
      const manifest = yaml.load(manifestContent);

      const fileName = path.basename(file);
      let found = false;

      for (const [code, data] of Object.entries(manifest.standards || {})) {
        if (data.full_name === fileName || data.filename === fileName) {
          found = true;
          break;
        }
      }

      if (!found) {
        errors.push({
          file,
          line: 1,
          rule: 'manifest-inclusion',
          message: 'Standards file must be included in MANIFEST.yaml'
        });
      }
    } catch (e) {
      // Manifest not found or invalid
    }
  }

  return errors;
}

/**
 * Custom rule: Check implementation checklist
 */
function checkImplementationChecklist(content, file) {
  const errors = [];

  if (file.endsWith('_STANDARDS.md') && file !== 'UNIFIED_STANDARDS.md') {
    if (!content.includes('Implementation Checklist') &&
        !content.includes('checklist') &&
        !content.includes('Checklist')) {
      errors.push({
        file,
        line: 1,
        rule: 'implementation-checklist',
        message: 'Standards should include an implementation checklist'
      });
    }
  }

  return errors;
}

/**
 * Custom rule: Token efficiency checks
 */
function checkTokenEfficiency(content, file) {
  const errors = [];
  const warnings = [];

  // Check section sizes
  const sections = content.split(/^##\s+/m);

  sections.forEach((section, index) => {
    if (section.trim()) {
      const wordCount = section.split(/\s+/).length;
      const estimatedTokens = Math.floor(wordCount * 0.75);

      if (estimatedTokens > 3000) {
        const lineNum = content.indexOf(section);
        warnings.push({
          file,
          line: lineNum,
          rule: 'token-efficiency',
          level: 'warning',
          message: `Section has ~${estimatedTokens} tokens. Consider splitting for better token efficiency.`
        });
      }
    }
  });

  return [...errors, ...warnings];
}

/**
 * Main linting function
 */
async function lintStandardsFiles(directory) {
  const results = {
    errors: [],
    warnings: [],
    files: 0
  };

  // Get all markdown files
  const allFiles = [];
  function walkDir(dir) {
    const files = fs.readdirSync(dir);
    files.forEach(file => {
      const fullPath = path.join(dir, file);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory() && !file.startsWith('.') && file !== 'node_modules') {
        walkDir(fullPath);
      } else if (file.endsWith('.md')) {
        allFiles.push(fullPath);
      }
    });
  }

  walkDir(directory);

  // Lint each file
  for (const file of allFiles) {
    const content = fs.readFileSync(file, 'utf8');
    const relativeFile = path.relative(directory, file);

    results.files++;

    // Run custom rules
    const errors = [
      ...checkVersionMetadata(content, relativeFile),
      ...checkRequiredSections(content, relativeFile),
      ...checkRequirementTags(content, relativeFile),
      ...checkCrossReferences(content, relativeFile, allFiles),
      ...await checkManifestInclusion(relativeFile, path.join(directory, 'MANIFEST.yaml')),
      ...checkImplementationChecklist(content, relativeFile),
      ...checkTokenEfficiency(content, relativeFile)
    ];

    errors.forEach(error => {
      if (error.level === 'warning') {
        results.warnings.push(error);
      } else {
        results.errors.push(error);
      }
    });
  }

  return results;
}

// Export for use in other scripts
module.exports = {
  lintStandardsFiles,
  checkVersionMetadata,
  checkRequiredSections,
  checkRequirementTags,
  checkCrossReferences,
  checkManifestInclusion,
  checkImplementationChecklist,
  checkTokenEfficiency
};

// Run if called directly
if (require.main === module) {
  const directory = process.argv[2] || '.';

  lintStandardsFiles(directory).then(results => {
    console.log('Standards Linting Report');
    console.log('=======================\n');

    console.log(`Files checked: ${results.files}`);
    console.log(`Errors found: ${results.errors.length}`);
    console.log(`Warnings found: ${results.warnings.length}\n`);

    if (results.errors.length > 0) {
      console.log('ERRORS:');
      results.errors.forEach(error => {
        console.log(`  ${error.file}:${error.line} - [${error.rule}] ${error.message}`);
      });
      console.log('');
    }

    if (results.warnings.length > 0) {
      console.log('WARNINGS:');
      results.warnings.forEach(warning => {
        console.log(`  ${warning.file}:${warning.line} - [${warning.rule}] ${warning.message}`);
      });
    }

    // Exit with error code if errors found
    if (results.errors.length > 0) {
      process.exit(1);
    }
  }).catch(error => {
    console.error('Linting failed:', error);
    process.exit(2);
  });
}
