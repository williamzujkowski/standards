#!/usr/bin/env node

import { Command } from 'commander';
import * as fs from 'fs/promises';
import * as path from 'path';
import { glob } from 'glob';
import { AnnotationParserFactory, NistAnnotation } from './parsers';
import './parsers'; // Initialize parsers

const program = new Command();

interface ScanOptions {
  output?: string;
  format: 'json' | 'markdown' | 'csv';
  include?: string;
  exclude?: string;
}

async function scanDirectory(directory: string, options: ScanOptions): Promise<void> {
  console.log(`Scanning directory: ${directory}`);

  // Get supported extensions
  const extensions = AnnotationParserFactory.getSupportedExtensions();
  const pattern = `**/*{${extensions.join(',')}}`;

  // Find files
  const files = await glob(pattern, {
    cwd: directory,
    ignore: options.exclude ? options.exclude.split(',') : ['**/node_modules/**', '**/dist/**', '**/build/**'],
    absolute: true
  });

  console.log(`Found ${files.length} files to scan`);

  const allAnnotations: NistAnnotation[] = [];
  const errors: Array<{ file: string; error: string }> = [];

  // Parse each file
  for (const file of files) {
    const result = await AnnotationParserFactory.parseFile(file);
    allAnnotations.push(...result.annotations);

    if (result.errors.length > 0) {
      result.errors.forEach(error => {
        errors.push({ file, error });
      });
    }
  }

  console.log(`Found ${allAnnotations.length} NIST annotations`);

  // Output results
  const output = formatOutput(allAnnotations, errors, options.format);

  if (options.output) {
    await fs.writeFile(options.output, output);
    console.log(`Results written to: ${options.output}`);
  } else {
    console.log(output);
  }
}

function formatOutput(
  annotations: NistAnnotation[],
  errors: Array<{ file: string; error: string }>,
  format: 'json' | 'markdown' | 'csv'
): string {
  switch (format) {
    case 'json':
      return JSON.stringify({ annotations, errors }, null, 2);

    case 'markdown':
      let md = '# NIST Annotation Scan Results\n\n';

      if (errors.length > 0) {
        md += '## Errors\n\n';
        errors.forEach(({ file, error }) => {
          md += `- **${file}**: ${error}\n`;
        });
        md += '\n';
      }

      md += `## Summary\n\n`;
      md += `- Total annotations found: ${annotations.length}\n`;
      md += `- Unique controls: ${new Set(annotations.map(a => a.controlId)).size}\n`;
      md += `- Files with annotations: ${new Set(annotations.map(a => a.file)).size}\n\n`;

      // Group by control
      md += '## Annotations by Control\n\n';
      const byControl = groupBy(annotations, 'controlId');

      Object.entries(byControl).forEach(([controlId, items]) => {
        md += `### ${controlId} (${items.length} occurrences)\n\n`;
        items.forEach(annotation => {
          const relativePath = path.relative(process.cwd(), annotation.file);
          md += `- **${relativePath}:${annotation.line}** - ${annotation.description || 'No description'}\n`;
          if (annotation.implements) {
            md += `  - Implements: ${annotation.implements}\n`;
          }
          if (annotation.evidence) {
            md += `  - Evidence: ${annotation.evidence.join(', ')}\n`;
          }
        });
        md += '\n';
      });

      return md;

    case 'csv':
      let csv = 'Control ID,Description,File,Line,Column,Language,Implements,Evidence\n';
      annotations.forEach(annotation => {
        const relativePath = path.relative(process.cwd(), annotation.file);
        csv += [
          annotation.controlId,
          `"${annotation.description.replace(/"/g, '""')}"`,
          relativePath,
          annotation.line,
          annotation.column,
          annotation.language,
          annotation.implements || '',
          annotation.evidence ? annotation.evidence.join(';') : ''
        ].join(',') + '\n';
      });
      return csv;

    default:
      throw new Error(`Unknown format: ${format}`);
  }
}

function groupBy<T>(array: T[], key: keyof T): Record<string, T[]> {
  return array.reduce((result, item) => {
    const group = String(item[key]);
    if (!result[group]) {
      result[group] = [];
    }
    result[group].push(item);
    return result;
  }, {} as Record<string, T[]>);
}

program
  .name('scan-annotations')
  .description('Scan codebase for NIST control annotations')
  .version('1.0.0');

program
  .command('scan [directory]')
  .description('Scan a directory for NIST annotations')
  .option('-o, --output <file>', 'Output file path')
  .option('-f, --format <format>', 'Output format (json, markdown, csv)', 'markdown')
  .option('-i, --include <pattern>', 'Include file pattern')
  .option('-e, --exclude <pattern>', 'Exclude file pattern')
  .action(async (directory = '.', options: ScanOptions) => {
    try {
      await scanDirectory(directory, options);
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program
  .command('validate [directory]')
  .description('Validate NIST annotations in a directory')
  .action(async (directory = '.') => {
    try {
      const result = await scanDirectory(directory, { format: 'json' });
      // TODO: Add validation logic (check control IDs against OSCAL catalog)
      console.log('Validation complete');
    } catch (error) {
      console.error('Error:', error);
      process.exit(1);
    }
  });

program.parse();
