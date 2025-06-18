#!/usr/bin/env node

/**
 * Generate OSCAL System Security Plan (SSP)
 *
 * Usage: npm run generate-ssp -- [options]
 */

import { OSCALSystemSecurityPlanGenerator } from '../automation/oscal-ssp-generator';
import { writeFile, mkdir } from 'fs/promises';
import * as path from 'path';

interface Options {
  baseline: 'low' | 'moderate' | 'high';
  output: string;
  format: 'json' | 'yaml';
  projectPath: string;
  systemName?: string;
  systemId?: string;
}

async function parseArgs(): Promise<Options> {
  const args = process.argv.slice(2);
  const options: Options = {
    baseline: 'moderate',
    output: 'oscal-output',
    format: 'json',
    projectPath: process.cwd()
  };

  for (let i = 0; i < args.length; i++) {
    switch (args[i]) {
      case '--baseline':
      case '-b':
        options.baseline = args[++i] as 'low' | 'moderate' | 'high';
        break;
      case '--output':
      case '-o':
        options.output = args[++i];
        break;
      case '--format':
      case '-f':
        options.format = args[++i] as 'json' | 'yaml';
        break;
      case '--project':
      case '-p':
        options.projectPath = args[++i];
        break;
      case '--system-name':
        options.systemName = args[++i];
        break;
      case '--system-id':
        options.systemId = args[++i];
        break;
      case '--help':
      case '-h':
        printHelp();
        process.exit(0);
    }
  }

  return options;
}

function printHelp(): void {
  console.log(`
OSCAL System Security Plan Generator

Usage: npm run generate-ssp -- [options]

Options:
  -b, --baseline <level>    Security baseline: low, moderate, high (default: moderate)
  -o, --output <dir>        Output directory (default: oscal-output)
  -f, --format <format>     Output format: json, yaml (default: json)
  -p, --project <path>      Project path to analyze (default: current directory)
  --system-name <name>      System name (default: from project)
  --system-id <id>          System identifier (default: auto-generated)
  -h, --help               Show this help message

Examples:
  npm run generate-ssp
  npm run generate-ssp -- --baseline high --format yaml
  npm run generate-ssp -- --project /path/to/project --system-name "My App"
`);
}

async function main() {
  console.log('🚀 OSCAL System Security Plan Generator\n');

  const options = await parseArgs();

  // Create project context
  const projectContext = {
    repositoryPath: options.projectPath,
    systemId: options.systemId || `system-${Date.now()}`,
    systemName: options.systemName || path.basename(options.projectPath),
    systemNameShort: options.systemName?.substring(0, 10) || 'SYS',
    description: `System security plan for ${options.systemName || path.basename(options.projectPath)}`
  };

  console.log('📋 Generating SSP with settings:');
  console.log(`   Baseline: ${options.baseline}`);
  console.log(`   System: ${projectContext.systemName}`);
  console.log(`   Project: ${projectContext.repositoryPath}`);
  console.log(`   Format: ${options.format}\n`);

  try {
    // Create SSP generator
    const generator = new OSCALSystemSecurityPlanGenerator();

    // Generate SSP
    console.log('⚙️  Analyzing project and generating SSP...');
    const ssp = await generator.generateOSCALSSP(projectContext, options.baseline);

    // Ensure output directory exists
    await mkdir(options.output, { recursive: true });

    // Generate filename
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `ssp-${projectContext.systemId}-${timestamp}.${options.format}`;
    const outputPath = path.join(options.output, filename);

    // Save SSP
    if (options.format === 'json') {
      await writeFile(outputPath, JSON.stringify(ssp, null, 2));
    } else if (options.format === 'yaml') {
      const yaml = await import('js-yaml');
      await writeFile(outputPath, yaml.dump(ssp));
    }

    console.log(`\n✅ SSP generated successfully!`);
    console.log(`   Output: ${outputPath}`);

    // Show summary
    const implementedCount = ssp['system-security-plan']['control-implementation']['implemented-requirements'].length;
    console.log(`\n📊 Summary:`);
    console.log(`   Total controls in baseline: ${implementedCount}`);
    console.log(`   System components: ${ssp['system-security-plan']['system-implementation'].components.length}`);
    console.log(`   Information types: ${ssp['system-security-plan']['system-characteristics']['system-information']['information-types'].length}`);

  } catch (error: any) {
    console.error('❌ Error generating SSP:', error.message);
    process.exit(1);
  }
}

// Run if called directly
if (require.main === module) {
  main();
}

export { main as generateSSP };
